import FWCore.ParameterSet.Config as cms

import time

import HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions as HChOptions
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching as HChTriggerMatching
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
import HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation as jesVariation
import HiggsAnalysis.HeavyChHiggsToTauNu.WJetsWeight as wjetsWeight
import HiggsAnalysis.HeavyChHiggsToTauNu.TopPtWeight_cfi as topPtWeight
from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.pileupReweightedAllEvents import PileupWeightType

tooManyAnalyzersLimit = 100

class Timer:
    def __init__(self):
        self._start = time.time()

    def stop(self, message):
        stop = time.time()
        print message, "%.0f s" % (stop-self._start)

## Infrastucture to help analysis configuration building
#
# This is the "master configuration" for analysis jobs. It is
# organized as a class to keep the complexity under control (having
# all the flags in a flat file, and all structure copy-pasted between
# the different analysis configuration files started to become
# unmanageable).
#
# Various options are set in the constructor, and the configuration
# itself is built with e.g. buildSignalAnalysis(), which returns the
# cms.Process object which should be assigned to a local 'process'
# variable. It can, of course, be further customized in the analysis
# job configuration file.
#
# Since there are now many dimensions creating arrays of analyzers
# (data era, optimisation, systematics), the builder keeps track of
# the number of analyzers created in each category and prints the
# counts in the end. If the total count is too high
# (tooManyAnalyzersLimit) and allowTooManyAnalyzers flag is False
# (default), an exception is raised. These checks are made in order to
# not to accidentally have gazillion analyzers.
class ConfigBuilder:
    ## Constructor
    #
    # \param dataVersion   String for data version
    # \param dataEras      List of strings of data (or PU weight) eras. One
    #                      analyzer per era is constructed
    #
    # Other parameters are optional, and have their default values in
    # below.
    def __init__(self, dataVersion, dataEras,
                 # Job options
                 processName = "Analysis",
                 maxEvents = -1,
                 useDefaultInputFiles = True,
                 edmOutput = False,
                 # Optional options
                 doAgainstElectronScan = False, # Scan against electron and muon discriminators
                 doTauIsolationAndJetPUScan = False, # Scan tau isolation and jet PU discriminators
                 doBTagScan = False, # Scan various btag working points to obtain MC efficiencies
                 doBTagTree = False, # fill tree for btagging eff study
                 doMETResolution = False, # Make MET resolution histograms
                 tauEmbeddingFinalizeMuonSelection = True, # With tau embedding input, tighten the muon selection
                 doPrescalesForData = False, # Keep / Ignore prescaling for data (suppresses greatly error messages in datasets with or-function of triggers)
                 doFillTree = False, # Tree filling
                 histogramAmbientLevel = "Debug", # Set level of how many histograms are stored to files options are: 'Vital' (least histograms), 'Informative', 'Debug' (all histograms),
                 histogramAmbientLevelOptimization = "Systematics", #"Vital",
                 histogramAmbientLevelSystematics = "Systematics",
                 applyTauTriggerScaleFactor = True, # Apply tau trigger scale factor or not
                 applyTauTriggerLowPurityScaleFactor = False, # Apply tau trigger scale factor or not
                 applyMETTriggerScaleFactor = False, # Apply MET trigger scale factor or not
                 applyL1ETMScaleFactor = True, # Apply L1ETM scale factor or not
                 applyPUReweight = True, # Apply PU weighting or not
                 applyTopPtReweight = True, # Apply Top Pt reweighting on TTJets sample
                 topPtReweightScheme = None, # None for default, see TopPtWeight_cfi.py for allowed values
                 tauSelectionOperatingMode = "standard", # standard, tauCandidateSelectionOnly
                # tauSelectionOperatingMode = "tauCandidateSelectionOnly",   
                 doTriggerMatching = True,
                 useCHSJets = False,
                 useJERSmearedJets = True,
                 customizeLightAnalysis = None,
                 customizeHeavyAnalysis = None,
                 doLightAnalysis = True,
                 doHeavyAnalysis = False,
                 pickEvents = True, # Produce pickEvents.txt
                 doSystematics = False, # Running of systematic variations is controlled by the global flag (below), or the individual flags
                 doTauIDandMisIDSystematicsAsShapes = False, # If systematic variations are produced, variations are produced also for misidentified tau systematics
                 doAsymmetricTriggerUncertainties = True, # If true, will vary the efficiency uncertainties instead of the scale factor uncertainty
                 doQCDTailKillerScenarios = False, # Run different scenarios of the QCD tail killer (improved delta phi cuts)
                 doJESVariation = False, # Perform the signal analysis with the JES variations in addition to the "golden" analysis
                 doPUWeightVariation = False, # Perform the signal analysis with the PU weight variations
                 doTopPtWeightVariation = False, # Perform the signal analysis with the Top pt weight variations
                 doScaleFactorVariation = False, # Perform the signal analysis with the scale factor variations
                 doOptimisation = False, optimisationScheme=None, # Do variations for optimisation
                 allowTooManyAnalyzers = False, # Allow arbitrary number of analyzers (beware, it might take looong to run and merge)
                 printAnalyzerNames = False,
                 inputWorkflow = "pattuple_v53_3", # Name of the workflow, whose output is used as an input, needed for WJets weighting
                 ):
        self.options, self.dataVersion = HChOptions.getOptionsDataVersion(dataVersion)
        self.dataEras = dataEras

        self.processName = processName
        self.maxEvents = maxEvents
        self.useDefaultInputFiles = useDefaultInputFiles
        self.edmOutput = edmOutput

        self.doQCDTailKillerScenarios = doQCDTailKillerScenarios
        self.doAgainstElectronScan = doAgainstElectronScan
        self.doTauIsolationAndJetPUScan = doTauIsolationAndJetPUScan
        self.doBTagScan = doBTagScan
        self.doBTagTree = doBTagTree
        self.doMETResolution = doMETResolution
        self.tauEmbeddingFinalizeMuonSelection = tauEmbeddingFinalizeMuonSelection
        self.doPrescalesForData = doPrescalesForData
        self.doFillTree = doFillTree
        self.histogramAmbientLevel = histogramAmbientLevel
        self.histogramAmbientLevelSystematics = histogramAmbientLevelSystematics
        self.applyTauTriggerScaleFactor = applyTauTriggerScaleFactor
        self.applyTauTriggerLowPurityScaleFactor = applyTauTriggerLowPurityScaleFactor
        self.applyMETTriggerScaleFactor = applyMETTriggerScaleFactor
        self.applyL1ETMScaleFactor = applyL1ETMScaleFactor
        self.applyPUReweight = applyPUReweight
        self.applyTopPtReweight = applyTopPtReweight
        self.topPtReweightScheme = topPtReweightScheme
        self.tauSelectionOperatingMode = tauSelectionOperatingMode
        self.doTriggerMatching = doTriggerMatching
        self.useCHSJets = useCHSJets
        self.useJERSmearedJets = useJERSmearedJets
        self.customizeLightAnalysis = customizeLightAnalysis
        self.customizeHeavyAnalysis = customizeHeavyAnalysis

        if self.applyMETTriggerScaleFactor and self.applyL1ETMScaleFactor:
            raise Exception("Only one of applyMETTriggerScaleFactor and applyL1ETMScaleFactor can be set to True")

        self.doLightAnalysis = doLightAnalysis
        self.doHeavyAnalysis = doHeavyAnalysis
        if not self.doLightAnalysis and not self.doHeavyAnalysis:
            raise Exception("At least one of doLightAnalysis and doHeavyAnalysis must be set to True (otherwise nothing is done)")

        self.pickEvents = pickEvents
        self.doSystematics = doSystematics
        self.doTauIDandMisIDSystematicsAsShapes = doTauIDandMisIDSystematicsAsShapes
        self.doAsymmetricTriggerUncertainties = doAsymmetricTriggerUncertainties
        self.doJESVariation = doJESVariation
        self.doPUWeightVariation = doPUWeightVariation
        self.doTopPtWeightVariation = doTopPtWeightVariation
        self.doScaleFactorVariation = doScaleFactorVariation
        self.doOptimisation = doOptimisation
        self.optimisationScheme = optimisationScheme
        self.allowTooManyAnalyzers = allowTooManyAnalyzers
        self.printAnalyzerNames = printAnalyzerNames

        self.inputWorkflow = inputWorkflow

        if self.applyTauTriggerScaleFactor or self.applyTauTriggerLowPurityScaleFactor or self.applyMETTriggerScaleFactor or self.applyL1ETMScaleFactor:
            for trg in self.options.trigger:
                if not "IsoPFTau" in trg and self.options.tauEmbeddingInput == 0:
                    print "applyTauTriggerScaleFactor=True or applyTauTriggerLowPurityScaleFactor=True or applyMETTriggerScaleFactor=True or applyL1ETMScaleFactor=True, and got non-tau trigger for non-embedding input, setting applyTauTriggerScaleFactor=False and applyMETTriggerScaleFactor=False"
                    self.applyTauTriggerScaleFactor = False
                    self.applyTauTriggerLowPurityScaleFactor = False
                    self.applyMETTriggerScaleFactor = False
                    self.applyL1ETMScaleFactor = False

        if self.doMETResolution and self.doOptimisation:
            raise Exception("doMETResolution and doOptimisation conflict")

        if self.options.wjetsWeighting != 0:
            if not self.dataVersion.isMC():
                raise Exception("Command line option 'wjetsWeighting' works only with MC")
#            if self.options.tauEmbeddingInput != 0:
#                raise Exception("There are no WJets weights for embedding yet")

        if self.applyTopPtReweight and not self.applyPUReweight:
            raise Exception("When applyTopPtReweight=True, also applyPUReweight must be True (you had it False)")

        if self.doOptimisation or self.doAgainstElectronScan or self.doTauIsolationAndJetPUScan:
            #self.doSystematics = True            # Make sure that systematics are run
            self.doFillTree = False              # Make sure that tree filling is disabled or root file size explodes
            self.histogramAmbientLevel = histogramAmbientLevelOptimization # Set histogram level to least histograms to reduce output file sizes

        if self.doBTagTree:
            self.tauSelectionOperatingMode = 'tauCandidateSelectionOnly'

        if self.options.tauEmbeddingInput != 0:
            print "Tau embedding input, disabling trigger matching (mu-trigger matching done in embedding jobs)"
            self.doTriggerMatching = False

        self.systPrefix = "SystVar"

        self.numberOfAnalyzers = {}
        self.analyzerCategories = []


    ## Build configuration for signal analysis job
    #
    # \return cms.Process object, should be assigned to a local
    #         'process' variable in the analysis job configuration file
    def buildSignalAnalysis(self):
        import HiggsAnalysis.HeavyChHiggsToTauNu.signalAnalysis as signalAnalysis
        def create(param):
            return [signalAnalysis.createEDFilter(param)]
        return self._build(create, ["signalAnalysis"])

    ## Build configuration for signal analysis inverted tau job
    #
    # \return cms.Process object, should be assigned to a local
    #         'process' variable in the analysis job configuration file
    def buildSignalAnalysisInvertedTau(self):
        import HiggsAnalysis.HeavyChHiggsToTauNu.signalAnalysisInvertedTau as signalAnalysisInvertedTau

        # Enforce tau candidate selection
        self.tauSelectionOperatingMode = "tauCandidateSelectionOnly"
        
        def create(param):
            return [signalAnalysisInvertedTau.createEDFilter(param)]
        return self._build(create, ["signalAnalysisInvertedTau"])

    ## Build configuration for signal analysis job
    #
    # \return cms.Process object, should be assigned to a local
    #         'process' variable in the analysis job configuration file
    def buildQCDMeasurementFactorised(self):
        import HiggsAnalysis.HeavyChHiggsToTauNu.QCDMeasurementFactorised as QCDMeasurementFactorised
        def create(param):
            return [QCDMeasurementFactorised.createEDFilter(param)]
        return self._build(create, ["QCDMeasurement"])

    ## Build configuration for EWK background coverage analysis job
    #
    # \return cms.Process object, should be assigned to a local
    #         'process' variable in the analysis job configuration file
    def buildEwkBackgroundCoverageAnalysis(self):
        import HiggsAnalysis.HeavyChHiggsToTauNu.ewkBackgroundCoverageAnalysis as ewkBackgroundCoverageAnalysis
        def create(param):
            return [ewkBackgroundCoverageAnalysis.createEDAnalyze(param)]
        return self._build(create, ["ewkBackgroundCoverageAnalysis"])

    ## Accumulate the number of analyzers to a category
    #
    # \param key     Analyzer category name
    # \param names   List of analyzer names to add to the category
    def _accumulateAnalyzers(self, key, names):
        if not key in self.numberOfAnalyzers:
            self.analyzerCategories.append(key)

        self.numberOfAnalyzers[key] = self.numberOfAnalyzers.get(key, []) + names

    ## Checks that the number of analyzers is sensible
    #
    # I.e. prints stats and might raise an exception)
    def _checkNumberOfAnalyzers(self):
        print "Created analyzers in following categories"
        width = max([len(cat) for cat in self.analyzerCategories]) 
        fmt = "  %%-%ds: %%d" % width
        s = 0
        for cat in self.analyzerCategories:
            n = len(self.numberOfAnalyzers[cat])
            s += n
            print fmt % (cat, n)
        print "  "+("-" * (width+4))
        print fmt % ("Total", s)
        print

        if self.printAnalyzerNames:
            print "Analyzer module names:"
            names = self.getAnalyzerModuleNames()
            names.sort()
            for name in names:
                print "  %s" % name
            print


        if s > tooManyAnalyzersLimit:
            if self.allowTooManyAnalyzers:
                print "Total number of analyzers (%d) is over the suggested limit (%d), it might take loong to run and merge output" % (s, tooManyAnalyzersLimit)
            else:
                raise Exception("Total number of analyzers (%d) exceeds the suggested limit (%d). If you're sure you want to run so many analyzers, add 'allowTooManyAnalyzers=True' to the ConfigBuilder() constructor call." % (s, tooManyAnalyzersLimit))

    def getAnalyzerModuleNames(self):
        names = []
        for x in self.numberOfAnalyzers.itervalues():
            names.extend(x)
        return names

    ## Do the actual building of the configuration
    #
    # \param createAnalysesFunction Function, which takes
    #                               HChSignalAnalysisParameters_cff as
    #                               an argument, and returns a list of
    #                               analysis modules (cms.EDFilter)
    # \param analysisNames_         List of analysis module names
    #
    # \return cms.Process object
    #
    # We need to take in functions instead of the modules themselves,
    # because the HChSignalAnalysisParameters_cff is configured in the
    # body of this function.
    #
    # The modules created by the function are taken as the "main
    # modules". E.g. data era, optimisation, systematic variation
    # modules are created for each of the main modules.
    def _build(self, createAnalysesFunction, analysisNames_):
        # Common initialization
        (process, additionalCounters) = self._buildCommon()

        # Import and customize HChSignalAnalysisParameters
        param = self._buildParam(process)

        # Tau embedding input handling
        additionalCounters.extend(self._customizeTauEmbeddingInput(process, param))

        # Create analysis module(s)
        modules = createAnalysesFunction(param)
        analysisLightModules = []
        analysisLightNames = []
        analysisHeavyModules = []
        analysisHeavyNames = []
        if self.dataVersion.isData():
            if self.doLightAnalysis:
                analysisLightModules = modules
                analysisLightNames = [n+"Light" for n in analysisNames_]
            if self.doHeavyAnalysis:
                analysisHeavyModules = [param.cloneForHeavyAnalysis(mod) for mod in modules]
                analysisHeavyNames = [n+"Heavy" for n in analysisNames_]
        else:
            # For MC, produce the PU-reweighted analyses
            # No PU reweighting, it is sufficient to do calculate WJets weights only one
            if self.options.wjetsWeighting != 0 and not self.applyPUReweight:
                process.wjetsWeight = wjetsWeight.getWJetsWeight(self.dataVersion, self.options, self.inputWorkflow, None)
                process.commonSequence *= process.wjetsWeight
                for module in modules:
                    module.wjetsWeightReader.weightSrc = "wjetsWeight"
                    module.wjetsWeightReader.enabled = True

            for dataEra in self.dataEras:
                # With PU reweighting, must produce one per data era
                if self.options.wjetsWeighting != 0 and self.applyPUReweight:
                    weightMod = wjetsWeight.getWJetsWeight(self.dataVersion, self.options, self.inputWorkflow, dataEra)
                    setattr(process, "wjetsWeight"+dataEra, weightMod)
                    process.commonSequence *= weightMod

                if self.options.sample == "TTJets" and self.applyTopPtReweight:
                    weightMod = topPtWeight.topPtWeight.clone(enabled=True)
                    if self.topPtReweightScheme is not None:
                        weightMod.scheme = self.topPtReweightScheme
                    setattr(process, "topPtWeight"+dataEra, weightMod)
                    process.commonSequence += weightMod

                for module, name in zip(modules, analysisNames_):
                    mod = module.clone()
                    if self.applyTauTriggerScaleFactor or self.applyTauTriggerLowPurityScaleFactor:
                        param.setTauTriggerEfficiencyForEra(self.dataVersion, era=dataEra, pset=mod.tauTriggerEfficiencyScaleFactor)
                    if self.applyMETTriggerScaleFactor:
                        print "########################################"
                        print "#"
                        print "# MET trigger efficiency/scale factor is from the whole Run2012ABCD for the moment (dataEra was %s)." % dataEra
                        print "# This is suitable only for preliminary testing."
                        print "#"
                        print "########################################"
                        param.setMetTriggerEfficiencyForEra(self.dataVersion, era="Run2012ABCD", pset=mod.metTriggerEfficiencyScaleFactor)
                    if self.applyL1ETMScaleFactor:
                        print "########################################"
                        print "#"
                        print "# L1ETM trigger efficiency/scale factor is from 190456-202585 for eras 2012ABC and 202807-208686 for 2012D."
                        print "# The division comes from the high-pt tau bugfix, which does NOT coincide with C-D transition."
                        print "#"
                        print "########################################"
                        param.setL1ETMEfficiencyForEra(self.dataVersion, era=dataEra, pset=mod.metTriggerEfficiencyScaleFactor)
                    if self.applyPUReweight:
                        param.setPileupWeight(self.dataVersion, process=process, commonSequence=process.commonSequence, pset=mod.vertexWeight, psetReader=mod.pileupWeightReader, era=dataEra)
                        mod.configInfo.pileupReweightType = PileupWeightType.toString[PileupWeightType.NOMINAL]
                        if self.options.wjetsWeighting != 0:
                            mod.wjetsWeightReader.weightSrc = "wjetsWeight"+dataEra
                            mod.wjetsWeightReader.enabled = True
                        if self.options.sample == "TTJets" and self.applyTopPtReweight:
                            mod.topPtWeightReader.weightSrc = "topPtWeight"+dataEra
                            mod.topPtWeightReader.enabled = True
                            mod.configInfo.topPtReweightType = PileupWeightType.toString[PileupWeightType.NOMINAL]

                    if self.doLightAnalysis:
                        analysisLightModules.append(mod)
                        analysisLightNames.append(name+"Light"+dataEra)
                    if self.doHeavyAnalysis:
                        analysisLightModules.append(param.cloneForHeavyAnalysis(mod))
                        analysisLightNames.append(name+"Heavy"+dataEra)

                    print "Added analysis for PU weight era =", dataEra

        analysisModules = analysisLightModules+analysisHeavyModules
        analysisNames = analysisLightNames+analysisHeavyNames


        for module in analysisModules:
            module.Tree.fill = self.doFillTree
            module.histogramAmbientLevel = self.histogramAmbientLevel
            module.tauEmbeddingStatus = (self.options.tauEmbeddingInput != 0)
            if len(additionalCounters) > 0:
                module.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])
        if len(analysisLightModules) > 0:
            analysisLightModules[0].eventCounter.printMainCounter = cms.untracked.bool(True)
            #analysisLightModules[0].eventCounter.printSubCounters = cms.untracked.bool(True)
            if hasattr(analysisLightModules[0], "tauTriggerEfficiencyScaleFactor"):
                analysisLightModules[0].tauTriggerEfficiencyScaleFactor.printScaleFactors = cms.untracked.bool(True)
            if hasattr(analysisLightModules[0], "metTriggerEfficiencyScaleFactor"):
                analysisLightModules[0].metTriggerEfficiencyScaleFactor.printScaleFactors = cms.untracked.bool(True)
        if len(analysisHeavyModules) > 0:
            analysisHeavyModules[0].eventCounter.printMainCounter = cms.untracked.bool(True)
            #analysisHeavyModules[0].eventCounter.printSubCounters = cms.untracked.bool(True)
            if hasattr(analysisHeavyModules[0], "tauTriggerEfficiencyScaleFactor"):
                analysisHeavyModules[0].tauTriggerEfficiencyScaleFactor.printScaleFactors = cms.untracked.bool(True)
            if hasattr(analysisHeavyModules[0], "metTriggerEfficiencyScaleFactor"):
                analysisHeavyModules[0].metTriggerEfficiencyScaleFactor.printScaleFactors = cms.untracked.bool(True)

        # Prescale fetching done automatically for data
        if self.dataVersion.isData() and self.options.tauEmbeddingInput == 0 and self.doPrescalesForData:
            process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
            process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(self.dataVersion.getTriggerProcess())
            process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
            process.commonSequence *= process.hplusPrescaleWeightProducer
            for module in analysisModules:
                module.prescaleWeightReader.weightSrc = "hplusPrescaleWeightProducer"
                module.prescaleWeightReader.enabled = True

        # Allow customization AFTER all settings have been applied, and BEFORE the printout
        if self.customizeLightAnalysis is not None:
            for module in analysisLightModules:
                self.customizeLightAnalysis(module)
        if self.customizeHeavyAnalysis is not None:
            for module in analysisHeavyModules:
                self.customizeHeavyAnalysis(module)
        
        # Print output
        self._printModule(analysisModules[0])

        (analysisModules, analysisNames) = self._setupTauEmbeddingAnalyses(process, analysisModules, analysisNames)

        analysisNamesForSystematics = []
        # For optimisation, the modules for systematics are added to
        # analysisNamesForSystematics later
        if not self.doOptimisation:
            analysisNamesForSystematics = analysisNames[:]

        # Construct normal path
        analysisNamesForTailKillerScenarios = analysisNames
        if not self.doOptimisation:
            for module, name in zip(analysisModules, analysisNames):
                setattr(process, name, module)
                path = cms.Path(process.commonSequence * module)
                setattr(process, name+"Path", path)
            if self.pickEvents:
                process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
                # PickEvens only for the first analysis path
                p = getattr(process, analysisNames[0]+"Path")
                p *= process.PickEvents

            self._accumulateAnalyzers("Data eras", analysisNames)

            if self.doMETResolution:
                process.load("HiggsAnalysis.HeavyChHiggsToTauNu.METResolutionAnalysis_cfi")
                p *= process.metResolutionAnalysis
        # Construct paths for optimisation
        else:
            if self.optimisationScheme is None:
                raise Exception("You specified doOptimisation=True, but did not specify optimisationScheme. It must be a name of a module in HiggsAnalysis.HeavyChHiggsToTauNu.python.optimisation.")

            try:
                module = __import__("HiggsAnalysis.HeavyChHiggsToTauNu.optimisation."+self.optimisationScheme, fromlist=[self.optimisationScheme])
            except ImportError, e:
                print
                print "Module HiggsAnalysis.HeavyChHiggsToTauNu.optimisation."+self.optimisationScheme+" does not exist or has an error."
                raise
            try:
                optimisationScheme = module.optimisation
            except AttributeError:
                raise Exception("Module HiggsAnalysis.HeavyChHiggsToTauNu.optimisation."+self.optimisationScheme+" does not have an object 'optimisation'")

            timer = Timer()
            analysisNamesForTailKillerScenarios = []
            for module, name in zip(analysisModules, analysisNames):
                names = optimisationScheme.generateVariations(process, additionalCounters, process.commonSequence, module, name)
                self._accumulateAnalyzers("Optimisation", names)
                #analysisNamesForTailKillerScenarios = names
                analysisNamesForTailKillerScenarios.extend(names)
                analysisNamesForSystematics.extend(names)
            timer.stop("Added optimisation modules in")

        # QCD tail killer scenarios (do them also for optimisation variations)
        qcdTailKillerNames = self._buildQCDTailKillerScenarios(process, analysisNamesForTailKillerScenarios)
        analysisNamesForSystematics.extend(qcdTailKillerNames)

        # Against electron scan
        self._buildAgainstElectronScan(process, analysisModules, analysisNames)

        # scan for tau isolation and jet PU ID
        self._buildTauIsolationAndJetPUScan(process, analysisModules, analysisNames)

        # scan various btagging working points
        self._buildBTagScan(process, analysisModules, analysisNames)

        # Tau embedding-like preselection for normal MC (overrides te list of analysisNamesForSystematics)
        analysisNamesForSystematics = self._buildTauEmbeddingLikePreselection(process, analysisNamesForSystematics, additionalCounters)

        ## Systematics
        #if "QCDMeasurement" not in analysisNames_: # Need also for QCD measurements, since they contain MC EWK
        self._buildTauIDandMisIdVariation(process, analysisNamesForSystematics, param)
        self._buildJESVariation(process, analysisNamesForSystematics)
        self._buildPUWeightVariation(process, analysisNamesForSystematics, param)
        self._buildTopPtWeightVariation(process, analysisNamesForSystematics)
        # Disabled for now, seems like it would be better to
        #handle SF uncertainties by error propagation after all
        # Re-enabled for test
        self._buildScaleFactorVariation(process, analysisNamesForSystematics)

        def runSetter(func):
            for name in self.getAnalyzerModuleNames():
                func(getattr(process, name), name)
        # Set trigger efficiencies
        runSetter(lambda module, name: param.setTauTriggerEfficiencyScaleFactorBasedOnTau(module.tauTriggerEfficiencyScaleFactor, module.tauSelection, name))
        if self.applyMETTriggerScaleFactor:
            runSetter(lambda module, name: param.setMetTriggerEfficiencyScaleFactorBasedOnTau(module.metTriggerEfficiencyScaleFactor, module.tauSelection, name))
        if self.applyL1ETMScaleFactor:
            runSetter(lambda module, name: param.setL1ETMEfficiencyScaleFactorBasedOnTau(module.metTriggerEfficiencyScaleFactor, module.tauSelection, name))
        # Set fake tau SF
        runSetter(lambda module, name: param.setFakeTauSFAndSystematics(module.fakeTauSFandSystematics, module.tauSelection, name))
        # Set PU ID src for modules
        runSetter(lambda module, name: param.setJetPUIdSrc(module.jetSelection, name))
        # Set embedding mT weight, not needed for fit-based
        #if self.options.tauEmbeddingInput != 0:
        #    runSetter(param.setEmbeddingMTWeightBasedOnSelection)

        # Optional output
        if self.edmOutput:
            process.out = cms.OutputModule("PoolOutputModule",
                fileName = cms.untracked.string('output.root'),
                outputCommands = cms.untracked.vstring(
                    "keep *_*_*_HChSignalAnalysis",
                    "drop *_*_counterNames_*",
                    "drop *_*_counterInstances_*"
                    #	"drop *",
                    #	"keep *",
                    #        "keep edmMergeableCounter_*_*_*"
                )
            )
            process.outpath = cms.EndPath(process.out)

        # Check number of analyzers
        self._checkNumberOfAnalyzers()

        return process

    ## Build common part of the analysis configuration
    #
    # \return Tuple of cms.Process object, and list of additional counter names (to be read from the event)
    #
    # The steps include
    # \li Create process
    # \li Create source, set maxEvents
    # \li Set GlobalTag
    # \li Load HchCommon_cfi
    # \li Run HChPatTuple.addPatOnTheFly
    # \li Setup ConfigInfoAnalyzer
    def _buildCommon(self):
        # Setup process
        process = cms.Process(self.processName)

        # Maximum number of events to be processed
        process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(self.maxEvents) )

        # Input source
        process.source = cms.Source('PoolSource',
            fileNames = cms.untracked.vstring()
        )
        if self.useDefaultInputFiles:
            if self.options.doPat == 0:
                process.source.fileNames.append(self.dataVersion.getAnalysisDefaultFileMadhatter())
            else:
                process.source.fileNames.append(self.dataVersion.getPatDefaultFileMadhatter())
        if self.options.tauEmbeddingInput != 0:
            if self.options.doPat != 0:
                raise Exception("In tau embedding input mode, doPat must be 0 (from v44_4 onwards)")
            process.source.fileNames = []

        # Global tag
        process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
        process.GlobalTag.globaltag = cms.string(self.dataVersion.getGlobalTag())
        if self.options.tauEmbeddingInput != 0:
            process.GlobalTag.globaltag = "START53_V21::All"
        print "GlobalTag="+process.GlobalTag.globaltag.value()

        # Common stuff
        process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")

        # MessageLogger
        # Uncomment the following in order to print the counters at the end of
        # the job (note that if many other modules are being run in the same
        # job, their INFO messages are printed too)
        #process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
        #process.MessageLogger.cerr.FwkReport.reportEvery = 1
        #process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

        # Fragment to run PAT on the fly if requested from command line
        from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
        process.commonSequence, additionalCounters = addPatOnTheFly(process, self.options, self.dataVersion, selectedPrimaryVertexFilter=True)

        # For top pt reweighting
        if self.options.sample == "TTJets" and self.applyTopPtReweight:
            topPtWeight.addTtGenEvent(process, process.commonSequence)

        # Add configuration information to histograms.root
        from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
        process.infoPath = addConfigInfo(process, self.options, self.dataVersion)
        if self.options.sample == "TTJets" and self.applyTopPtReweight:
            if self.topPtReweightScheme is None:
                process.configInfo.topPtReweightScheme = cms.untracked.string(topPtWeight.topPtWeight.scheme.value())
            else:
                process.configInfo.topPtReweightScheme = cms.untracked.string(self.topPtReweightScheme)
        if self.dataVersion.isMC() and self.applyPUReweight:
            process.configInfo.isPileupReweighted = cms.untracked.bool(True)

        return (process, additionalCounters)

    ## Configure HChSignalAnalysisParameters_cff
    #
    # \return HChSignalAnalysisParameters_cff module object
    def _buildParam(self, process):
        # Trigger from command line options
        import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
        param.overrideTriggerFromOptions(self.options)
        param.trigger.triggerSrc.setProcessName(self.dataVersion.getTriggerProcess())

        # Tau selection operating mode
        param.setAllTauSelectionOperatingMode(self.tauSelectionOperatingMode)

        # Trigger-matched taus
        if self.doTriggerMatching:
            HChTriggerMatching.triggerMatchingInAnalysis(process, process.commonSequence, self.options.trigger, param)

        # CHS jets
        if self.useCHSJets:
            print "Using CHS jets"
            param.changeJetCollection(moduleLabel="selectedPatJetsChs")

        # JER-smeared jets
        if self.useJERSmearedJets:
            param.setJERSmearedJets(self.dataVersion)

        # Trigger with scale factors (at the moment hard coded)
        if self.dataVersion.isMC():
            if self.applyTauTriggerScaleFactor:
                print "Applying high purity trigger tau leg scale factor"
                param.tauTriggerEfficiencyScaleFactor.mode = "scaleFactor"
                if self.applyTauTriggerLowPurityScaleFactor:
                    raise Exception("Config error: You set both applyTauTriggerScaleFactor=True and applyTauTriggerLowPurityScaleFactor=True! Please set only either one of them as true.")
            elif self.applyTauTriggerLowPurityScaleFactor:
                print "Applying low purity trigger tau leg scale factor"
                param.tauTriggerEfficiencyScaleFactor = param.setTriggerEfficiencyLowPurityScaleFactorBasedOnTau(param.tauSelection)
                param.tauTriggerEfficiencyScaleFactor.mode = "scaleFactor"
            if self.applyMETTriggerScaleFactor:
                print "Applying trigger MET leg scale factor"
                param.metTriggerEfficiencyScaleFactor.mode = "scaleFactor"
            if self.applyL1ETMScaleFactor:
                print "Applying L1ETM scale factor"
                param.metTriggerEfficiencyScaleFactor.mode = "scaleFactor" # yes, we re-use the MET-leg scale factor weighting code here

        if self.doBTagTree:
            param.tree.fillNonIsoLeptonVars = True
            param.MET.METCut = 0.0
            param.bTagging.discriminatorCut = -999
            param.GlobalMuonVeto.MuonPtCut = 999

        return param

    ## Setup for tau embedding input
    #
    # \param process  cms.Process object
    # \param param    HChSignalAnalysisParameters_cff module object
    def _customizeTauEmbeddingInput(self, process, param):
        ret = []
        if self.options.tauEmbeddingInput != 0:
            process.load("HiggsAnalysis.HeavyChHiggsToTauNu.WTauMuWeight_cfi")
            process.commonSequence += process.wtaumuWeight

            # This was supposed to be saved in embedded pattuples, but apparently in v53_3 is not
            process.embeddedTau = tauEmbeddingCustomisations.addTauEmbeddingMuonTausUsingVisible(process)
            process.commonSequence += process.embeddedTau

            #tauEmbeddingCustomisations.addMuonIsolationEmbeddingForSignalAnalysis(process, process.commonSequence)
            tauEmbeddingCustomisations.setCaloMetSum(process, process.commonSequence, self.options, self.dataVersion)
            tauEmbeddingCustomisations.customiseParamForTauEmbedding(process, param, self.options, self.dataVersion)
            if self.tauEmbeddingFinalizeMuonSelection:
                # applyIsolation = not doTauEmbeddingMuonSelectionScan
                applyIsolation = False
                ret.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param,
                                                                            enableIsolation=applyIsolation))
        return ret

    ## Print module configuration
    #
    # \param module   Analysis module
    def _printModule(self, module):
        #print "\nAnalysis is blind:", module.blindAnalysisStatus, "\n"
        print "Histogram level:", module.histogramAmbientLevel.value()
        print "Trigger:", module.trigger
        print "Tau trigger scale factor mode:", module.tauTriggerEfficiencyScaleFactor.mode.value()
        print "Tau trigger scale factor data:", module.tauTriggerEfficiencyScaleFactor.dataSelect.value()
        print "Tau trigger scale factor MC:", module.tauTriggerEfficiencyScaleFactor.mcSelect.value()
        print "MET trigger scale factor mode:", module.metTriggerEfficiencyScaleFactor.mode.value()
        print "MET trigger scale factor data:", module.metTriggerEfficiencyScaleFactor.dataSelect.value()
        print "MET trigger scale factor MC:", module.metTriggerEfficiencyScaleFactor.mcSelect.value()
        if hasattr(module, "metFilters"):
            print "MET filters", module.metFilters
        print "VertexWeight data distribution:",module.vertexWeight.dataPUdistribution.value()
        print "VertexWeight mc distribution:",module.vertexWeight.mcPUdistribution.value()
        print "Cut on L1 MET", module.trigger.l1MetCut.value()
        print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", module.trigger.hltMetCut.value()
        #print "TauSelection algorithm:", module.tauSelection.selection.value()
        print "TauSelection algorithm:", module.tauSelection.selection.value()
        print "TauSelection src:", module.tauSelection.src.value()
        if hasattr(module, "vetoTauSelection"):
            print "TauVetoSelection src:", module.vetoTauSelection.tauSelection.src.value()
        print "TauSelection isolation:", module.tauSelection.isolationDiscriminator.value()
        print "TauSelection operating mode:", module.tauSelection.operatingMode.value()
        if hasattr(module, "vetoTauSelection"):
            print "VetoTauSelection src:", module.vetoTauSelection.tauSelection.src.value()
        #if hasattr(module, "jetSelection"):
        #    print "Beta cut: ", module.jetSelection.betaCutSource.value(), module.jetSelection.betaCutDirection.value(), module.jetSelection.betaCut.value()
        print "electrons: ", module.ElectronSelection
        print "muons: ", module.MuonSelection
        if hasattr(module, "jetSelection"):
            print "jets: ", module.jetSelection
        print "QCD Tail-Killer: ", module.QCDTailKiller.scenarioLabel.value()
        print "Invariant mass reconstruction: ", module.invMassReco

    ## Build array of analyzers to scan various QCD tail killer scenarios
    #
    # \param process          cms.Process object
    # \param analysisNames    List of analysis module names
    def _buildQCDTailKillerScenarios(self, process, analysisNames):
        def createQCDTailKillerModule(process, modulePrefix, mod, names, modules):
            modName = name+"Opt"+modulePrefix
            if "Opt" in name:
                modName = name+modulePrefix
            setattr(process, modName, mod)
            names.append(modName)
            modules.append(mod)
            path = cms.Path(process.commonSequence * mod)
            setattr(process, modName+"Path", path)

        if not self.doQCDTailKillerScenarios:
            return []

        timer = Timer()
        import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
        names = []
        modules = []
        for name in analysisNames:
            module = getattr(process, name)
            for scenName in param.QCDTailKillerScenarios:
                mod = module.clone()
                obj = getattr(param, scenName, None)
                if obj == None:
                    raise Exception("Config error: tried to access tail killer scenario '%s', but its PSet is not present in HChSignalAnalysisParameters_cff.py!"%scenName)
                mod.QCDTailKiller = obj.clone()
                mod.QCDTailKiller.disableCollinearCuts = module.QCDTailKiller.disableCollinearCuts
                createQCDTailKillerModule(process, "QCDTailKiller%s"%mod.QCDTailKiller.scenarioLabel.value(), mod, names, modules)
        timer.stop("Added QCD tail killer scenarios in")
        self._accumulateAnalyzers("Modules for QCDTailKiller scenarios", names)

        return names

    ## Build array of analyzers to scan various tau againstElectron discriminators
    #
    # \param process          cms.Process object
    # \param analysisModules  List of analysis modules to be used as prototypes
    # \param analysisNames    List of analysis module names
    def _buildAgainstElectronScan(self, process, analysisModules, analysisNames):
        if not self.doAgainstElectronScan:
            return

        myTauIsolation = [
            "byLooseCombinedIsolationDeltaBetaCorr3Hits",
            "byMediumCombinedIsolationDeltaBetaCorr",
            "byMediumCombinedIsolationDeltaBetaCorr3Hits",
            #"byMediumIsolationMVA2"
            ]
        muonDiscriminators = [
            #"againstMuonLoose2",
            #"againstMuonMedium2",
            "againstMuonTight2"
            ]
        electronDiscriminators = [
            #"againstElectronLooseMVA3",
            #"againstElectronMediumMVA3",
            "againstElectronTight",
            "againstElectronTightMVA3",
            "againstElectronVTightMVA3"
            ]
        names = []
        modules = []
        for module, name in zip(analysisModules, analysisNames):
            for eleDisc in electronDiscriminators:
                for muonDisc in muonDiscriminators:
                    for tauIsol in myTauIsolation:
                        mod = module.clone()
                        mod.tauSelection.isolationDiscriminator = tauIsol
                        mod.tauSelection.againstElectronDiscriminator = eleDisc
                        mod.tauSelection.againstMuonDiscriminator = muonDisc
                        modName = name+"Opt"+eleDisc[0].upper()+eleDisc[1:]+muonDisc[0].upper()+muonDisc[1:]+tauIsol[0].upper()+tauIsol[1:]
                        setattr(process, modName, mod)
                        names.append(modName)
                        modules.append(mod)
                        path = cms.Path(process.commonSequence * mod)
                        setattr(process, modName+"Path", path)
        self._accumulateAnalyzers("AgainstElectron/AgainstMuon scan", names)

    ## Build array of analyzers to scan various tau isolation and jet PU ID discriminators
    #
    # \param process          cms.Process object
    # \param analysisModules  List of analysis modules to be used as prototypes
    # \param analysisNames    List of analysis module names
    def _buildTauIsolationAndJetPUScan(self, process, analysisModules, analysisNames):
        if not self.doTauIsolationAndJetPUScan:
            return

        myTauIsolation = [
            "byLooseCombinedIsolationDeltaBetaCorr3Hits",
            "byMediumCombinedIsolationDeltaBetaCorr3Hits",
            "byTightCombinedIsolationDeltaBetaCorr3Hits",
            "byLooseIsolationMVA2",
            "byMediumIsolationMVA2"
            ]
        jetPUIDType = ["none",
                       "full",
                       #"cutbased",
                       #"philv1",
                       #"simple"
                       ]
        jetPUIDWP = ["tight",
                     #"medium",
                     #"loose"
                     ]

        names = []
        modules = []
        for module, name in zip(analysisModules, analysisNames):
            for idType in jetPUIDType:
                for idWP in jetPUIDWP:
                    for tauIsol in myTauIsolation:
                        mod = module.clone()
                        mod.tauSelection.isolationDiscriminator = tauIsol
                        mod.jetSelection.jetPileUpType = idType
                        mod.jetSelection.jetPileUpWorkingPoint = idWP
                        modName = name+"Opt"+idType[0].upper()+idType[1:]+idWP[0].upper()+idWP[1:]+tauIsol[0].upper()+tauIsol[1:]
                        setattr(process, modName, mod)
                        names.append(modName)
                        modules.append(mod)
                        path = cms.Path(process.commonSequence * mod)
                        setattr(process, modName+"Path", path)
        self._accumulateAnalyzers("TauIsolation/JetPUID scan", names)

    ## Build array of analyzers to scan various tau isolation and jet PU ID discriminators
    #
    # \param process          cms.Process object
    # \param analysisModules  List of analysis modules to be used as prototypes
    # \param analysisNames    List of analysis module names
    def _buildBTagScan(self, process, analysisModules, analysisNames):
        if not self.doBTagScan:
            return
        #OP: JPL = 0.275, JPM = 0.545, JPT = 0.790, CSVL = 0.244, CSVM = 0.679, CSVT = 0.898
        myCSVWorkingPoints = [0.244, 0.679, 0.898]
        myJPTWorkingPoints = [] # Efficiencies and scale factors need to be added to BTagging.cc before this can be used!
        #myJPTWorkingPoints = [0.275, 0.545, 0.790]

        names = []
        modules = []
        for module, name in zip(analysisModules, analysisNames):
            for csv in myCSVWorkingPoints:
                mod = module.clone()
                mod.bTagging.discriminator = cms.untracked.string("combinedSecondaryVertexBJetTags")
                mod.bTagging.leadingDiscriminatorCut = csv
                modName = name+"OptBtagCSV"+str(csv).replace(".","")
                setattr(process, modName, mod)
                names.append(modName)
                modules.append(mod)
                path = cms.Path(process.commonSequence * mod)
                setattr(process, modName+"Path", path)
        for module, name in zip(analysisModules, analysisNames):
            for jpt in myJPTWorkingPoints:
                mod = module.clone()
                mod.bTagging.discriminator = cms.untracked.string("jetProbabilityBJetTags")
                mod.bTagging.leadingDiscriminatorCut = jpt
                modName = name+"OptBtagJPT"+str(jpt).replace(".","")
                setattr(process, modName, mod)
                names.append(modName)
                modules.append(mod)
                path = cms.Path(process.commonSequence * mod)
                setattr(process, modName+"Path", path)
        self._accumulateAnalyzers("btag efficiency scan", names)

    ## Build "tau embedding"-like preselection for normal MC
    #
    # \param process             cms.Process object
    # \param analysisNames       List of analysis module names
    # \param additionalCounters  List of strings for additional counters
    def _buildTauEmbeddingLikePreselection(self, process, analysisNames, additionalCounters):
        if self.options.doTauEmbeddingLikePreselection == 0:
            return analysisNames

        if self.dataVersion.isData():
            raise Exception("doTauEmbeddingLikePreselection is meaningless for data")
        if self.options.tauEmbeddingInput != 0:
            raise Exception("tauEmbegginInput clashes with doTauEmbeddingLikePreselection")

        def makeName(name, postfix):
            for n in ["Light", "Heavy"]:
                if n in name:
                    return name.replace(n, postfix+n)
            raise Exception("Analysis name '%s' broke assumptions on naming convention")

        allNames = []
        def add(name, sequence, module, counters):
            module.eventCounter.counters = [cms.InputTag(c) for c in counters]
            setattr(process, name+"Sequence", sequence)
            setattr(process, name, module)
            allNames.append(name)
            path = cms.Path(sequence * module)
            setattr(process, name+"Path", path)

        maxGenTaus = None # not set
        maxGenTaus = 1 # events with exactly one genuine tau in acceptance

        namesForSyst = []
        for name in analysisNames:
            module = getattr(process, name)
            # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), no tau+MET trigger required
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, seq, mod, prefix=name+"EmbeddingLikePreselection", maxGenTaus=maxGenTaus, pileupWeight=mod.pileupWeightReader.weightSrc.value()))
            add(makeName(name, "TauEmbeddingLikePreselection"), seq, mod, counters)

            # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), tau+MET trigger required
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, seq, mod, prefix=name+"EmbeddingLikeTriggeredPreselection", maxGenTaus=maxGenTaus, pileupWeight=mod.pileupWeightReader.weightSrc.value(), disableTrigger=False))
            add(makeName(name, "TauEmbeddingLikeTriggeredPreselection"), seq, mod, counters)

            # Genuine tau preselection
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addGenuineTauPreselection(process, seq, mod, prefix=name+"GenuineTauPreselection", maxGenTaus=maxGenTaus, pileupWeight=mod.pileupWeightReader.weightSrc.value()))
            add(makeName(name, "GenuineTauPreselection"), seq, mod, counters)

            # Require genuine tau after tau ID in analysis
            mod = module.clone()
            mod.trigger.selectionType = "disabled"
            mod.onlyEmbeddingGenuineTaus = cms.untracked.bool(True)
            modName = makeName(name, "GenuineTau")
            add(modName, process.commonSequence, mod, additionalCounters)

            mod2 = mod.clone()
            mod2.trigger.caloMetSelection.metEmulationCut = 70
            modName = makeName(name, "GenuineTauCaloMet70")
            add(modName, process.commonSequence, mod2, additionalCounters)

            mod = mod.clone()
            mod.trigger.selectionType = module.trigger.selectionType
            modName = makeName(name, "GenuineTauTriggered")
            add(modName, process.commonSequence, mod, additionalCounters)
            namesForSyst.append(modName)

        self._accumulateAnalyzers("Tau embedding -like preselection", allNames)
        return namesForSyst

    ## Build additional analyses for tau embedding input
    #
    # \param process          cms.Process object
    # \param analysisModules  List of analysis modules to be used as prototypes
    # \param analysisNames    List of analysis module names
    def _setupTauEmbeddingAnalyses(self, process, analysisModules, analysisNames):
        if self.options.tauEmbeddingInput == 0:
            return (analysisModules, analysisNames)

        def makeName(name, postfix):
            for n in ["Light", "Heavy"]:
                if n in name:
                    return name.replace(n, postfix+n)
            raise Exception("Analysis name '%s' broke assumptions on naming convention")

        def disablePrintCounter(mod):
            if hasattr(mod.eventCounter, "printMainCounter"):
                mod.eventCounter.printMainCounter = False
        def enablePrintCounter(mod):
            if hasattr(mod.eventCounter, "printMainCounter"):
                mod.eventCounter.printMainCounter = True
        def setLevelToVital(mod):
            if mod.histogramAmbientLevel != "Systematics":
                mod.histogramAmbientLevel = "Vital"
        def setLevelToInformative(mod):
            if mod.histogramAmbientLevel != "Debug":
                mod.histogramAmbientLevel = "Informative"


#        disableIntermediateAnalyzers = (self.doQCDTailKillerScenarios or self.doOptimisation)
        disableIntermediateAnalyzers = self.doOptimisation
#        disableIntermediateAnalyzers = False

        useCaloMet = not self.applyMETTriggerScaleFactor

        additionalNames = []
        retNames = []
        retModules = []
        def addIntermediateAnalyzer(module, name, postfix):
            if disableIntermediateAnalyzers:
                return
            modName = name
            if postfix is not None:
                modName = makeName(name, postfix)
            path = cms.Path(process.commonSequence * module)
            setattr(process, modName, module)
            setattr(process, modName+"Path", path)
            additionalNames.append(modName)
            return path

        for module, name in zip(analysisModules, analysisNames):
            disablePrintCounter(module)
            addIntermediateAnalyzer(module, name, None)

            postfix = "MIdEff"
            mod = module.clone()
            setLevelToVital(mod)
            mod.embeddingMuonIdEfficiency.mode = "dataEfficiency"
            mod.embeddingMuonIdEfficiency.muonSrc = mod.Tree.tauEmbedding.muons.src.value()
            addIntermediateAnalyzer(mod, name, postfix)

            postfix += "TrgEff"
            mod = mod.clone()
            mod.embeddingMuonTriggerEfficiency.mode = "dataEfficiency"
            mod.embeddingMuonTriggerEfficiency.muonSrc = mod.embeddingMuonIdEfficiency.muonSrc.value()
            addIntermediateAnalyzer(mod, name, postfix)

            postfix += "WTauMu"
            mod = mod.clone()
            mod.embeddingWTauMuWeightReader.enabled = True
            setLevelToInformative(mod)
            addIntermediateAnalyzer(mod, name, postfix)

            # already here for met-leg efficiency
            postfix += "TEff"
            mod = mod.clone()
            mod.tauTriggerEfficiencyScaleFactor.mode = "dataEfficiency"
            setLevelToInformative(mod)
            addIntermediateAnalyzer(mod, name, postfix)

            if useCaloMet:
                postfix += "CaloMet70"
                mod = mod.clone()
                mod.trigger.caloMetSelection.metEmulationCut = 70.0

                mod2 = mod.clone()
                mod2.tauTriggerEfficiencyScaleFactor.mode = module.tauTriggerEfficiencyScaleFactor.mode
                setLevelToInformative(mod2)
                addIntermediateAnalyzer(mod2, name, postfix.replace("TEff", ""))
            else:
                postfix += "MetEff"
                mod = mod.clone()
                mod.metTriggerEfficiencyScaleFactor.mode = "dataEfficiency"

            if self.applyL1ETMScaleFactor:
                addIntermediateAnalyzer(mod, name, postfix)

                postfix += "L1ETMEff"
                mod = mod.clone()
                mod.metTriggerEfficiencyScaleFactor.mode = "dataEfficiency"

            # Reject at gen level W->tau->mu
            if False:
                mod2 = mod.clone()
                mod2.embeddingWTauMuWeightReader.enabled = False
                postfix2 = postfix.replace("WTauMu", "") + "GenWTau"

                genmatchFilter = cms.EDFilter("HPlusMuonGenMatchFilter",
                    genParticleSrc = cms.InputTag("genParticles", "", "SIM"),
                    muonSrc = cms.InputTag(tauEmbeddingCustomisations.tauEmbeddingMuons),
                    motherPdgIds = cms.vint32(24)
                )
                genmatchCount = cms.EDProducer("EventCountProducer")
                setattr(process, postfix+"GenMatchFilter", genmatchFilter)
                setattr(process, postfix+"GenMatchCount", genmatchCount)

                path = addIntermediateAnalyzer(mod2, name, postfix2)
                path.replace(process.commonSequence,
                             process.commonSequence+genmatchFilter+genmatchCount)
                mod2.eventCounter.counters.append(postfix+"GenMatchCount")

            if True:
                addIntermediateAnalyzer(mod, name, postfix)

                postfix += "MTWeight"
                mod = mod.clone()
                #mod.embeddingMTWeight.mode = "dataEfficiency" # bin-based
                mod.embeddingMTWeight.enabled = True # fit-based

            enablePrintCounter(mod)
            mod.histogramAmbientLevel = self.histogramAmbientLevel
            path = cms.Path(process.commonSequence * mod)
            modName = makeName(name, postfix)
#            setattr(process, modName, mod)
#            setattr(process, modName+"Path", path)
            retNames.append(modName)
            retModules.append(mod)


        if len(additionalNames) > 0:
            self._accumulateAnalyzers("Tau embedding intermediate analyses", additionalNames)
        return (retModules, retNames)

    def _cloneForVariation(self, module):
        mod = module.clone()
        mod.Tree.fill = False
        if hasattr(mod, "GenParticleAnalysis"):
            mod.GenParticleAnalysis.enabled = False
        mod.eventCounter.printMainCounter = cms.untracked.bool(False)
        mod.histogramAmbientLevel = self.histogramAmbientLevelSystematics
        return mod

    ## Build tau ID and mis-ID variation
    #
    # \param process                      cms.Process object
    # \param analysisNamesForSystematics  Names of the analysis modules for which the JES variation should be done
    # \param param     HChSignalAnalysisParameters_cff module object
    def _buildTauIDandMisIdVariation(self, process, analysisNamesForSystematics, param):
        #if not (self.doTauIDandMisIDSystematicsAsShapes or self.doSystematics):
        if not (self.doTauIDandMisIDSystematicsAsShapes): # FIXME: for now, do not run as part of systematics unless explicitly asked
            return
        if self.dataVersion.isMC():
            timer = Timer()
            for name in analysisNamesForSystematics:
                self._addTauIDandMisIdVariation(process, name)
            timer.stop("Added tau ID and mis-ID variation for %d modules in"%len(analysisNamesForSystematics))
        else:
            print "Tau ID and mis-ID variation disabled for data (not meaningful for data)"

    ## Add tau ID and mis-ID variation
    #
    # \param process                    cms.Process object
    # \param name                       Name of the module to be used as a prototype
    def _addTauIDandMisIdVariation(self, process, name):
        def addVariation(directionName):
            module = self._cloneForVariation(getattr(process, name))
            # NOTE: The actual variation of the values is done in params.setFakeTauSFAndSystematics()
            # which is called after the creation of the syst. variations based on the name of the module
            return self._addVariationModule(process, module, name+self.systPrefix+directionName)

        names = []
        # Add genuine tau ID systematics
        names.append(addVariation("GenuineTauPlus"))
        names.append(addVariation("GenuineTauMinus"))
        # Do not add fake tau mis-ID systematics for embedding
        if self.options.tauEmbeddingInput == 0:
            # Add e->tau systematics for barrel
            names.append(addVariation("FakeTauBarrelElectronPlus"))
            names.append(addVariation("FakeTauBarrelElectronMinus"))
            # Add e->tau systematics for endcap
            names.append(addVariation("FakeTauEndcapElectronPlus"))
            names.append(addVariation("FakeTauEndcapElectronMinus"))
            # Add e->tau systematics
            names.append(addVariation("FakeTauMuonPlus"))
            names.append(addVariation("FakeTauMuonMinus"))
            # Add jet->tau systematics
            names.append(addVariation("FakeTauJetPlus"))
            names.append(addVariation("FakeTauJetMinus"))
        # Accumulate
        self._accumulateAnalyzers("Fake tau variation", names)

    ## Build JES variation
    #
    # \param process                      cms.Process object
    # \param analysisNamesForSystematics  Names of the analysis modules for which the JES variation should be done
    def _buildJESVariation(self, process, analysisNamesForSystematics):
        if not (self.doJESVariation or self.doSystematics):
            return

        doJetUnclusteredVariation = True
        if self.options.tauEmbeddingInput != 0 and self.dataVersion.isData():
            doJetUnclusteredVariation = False

        if self.dataVersion.isMC() or self.options.tauEmbeddingInput != 0:
            timer = Timer()
            for name in analysisNamesForSystematics:
                self._addJESVariation(process, name, doJetUnclusteredVariation)
            timer.stop("Added JES variation for %d modules in"%len(analysisNamesForSystematics))
        else:
            print "JES variation disabled for data (not meaningful for data)"


    ## Add JES variation for one module
    #
    # \param process                    cms.Process object
    # \param name                       Name of the module to be used as a prototype
    # \param doJetUnclusteredVariation  Flag if JES+JER+UES variations should be done
    def _addJESVariation(self, process, name, doJetUnclusteredVariation):
        module = self._cloneForVariation(getattr(process, name))
        module.Tree.fillJetEnergyFractions = False # JES variation will make the fractions invalid

        postfix = ""
        if module.jetSelection.src.value()[-3:] == "Chs":
            postfix = "Chs"

        names = []
        names.append(jesVariation.addTESVariation(process, name, self.systPrefix+"TESPlus",  module, "Up", histogramAmbientLevel=self.histogramAmbientLevelSystematics))
        names.append(jesVariation.addTESVariation(process, name, self.systPrefix+"TESMinus", module, "Down", histogramAmbientLevel=self.histogramAmbientLevelSystematics))

        if doJetUnclusteredVariation:
            # Do all variations beyond TES
            names.append(jesVariation.addJESVariation(process, name, self.systPrefix+"JESPlus",  module, "Up", postfix))
            names.append(jesVariation.addJESVariation(process, name, self.systPrefix+"JESMinus", module, "Down", postfix))
    
            names.append(jesVariation.addJERVariation(process, name, self.systPrefix+"JERPlus",  module, "Up", postfix))
            names.append(jesVariation.addJERVariation(process, name, self.systPrefix+"JERMinus", module, "Down", postfix))
    
            names.append(jesVariation.addUESVariation(process, name, self.systPrefix+"METPlus",  module, "Up", postfix))
            names.append(jesVariation.addUESVariation(process, name, self.systPrefix+"METMinus", module, "Down", postfix))

        self._accumulateAnalyzers("JES variation", names)

    ## Add variation module to process, create a path for it
    #
    # \param process    cms.Process object
    # \param module     EDModule to insert
    # \param postfix    Name of the module
    #
    # \return name
    def _addVariationModule(self, process, module, name):
        path = cms.Path(process.commonSequence * module)
        setattr(process, name, module)
        setattr(process, name+"Path", path)
        return name

    ## Build PU weight variation
    #
    # \param process                      cms.Process object
    # \param analysisNamesForSystematics  Names of the analysis modules for which the PU weight variation should be done
    # \param param     HChSignalAnalysisParameters_cff module object
    def _buildPUWeightVariation(self, process, analysisNamesForSystematics, param):
        if not self.applyPUReweight:
            return
        if not (self.doPUWeightVariation or self.doSystematics):
            return

        if self.dataVersion.isMC():
            timer = Timer()
            for name in analysisNamesForSystematics:
                self._addPUWeightVariation(process, name, param)
            timer.stop("Added PU weight variation for %d modules in"%len(analysisNamesForSystematics))
        else:
            print "PU weight variation disabled for data (not meaningful for data)"

    ## Add PU weight variation for one module
    #
    # \param process   cms.Process object
    # \param name      Name of the module to be used as a prototype
    # \param param     HChSignalAnalysisParameters_cff module object
    def _addPUWeightVariation(self, process, name, param):
        # Assume that the wjetsWeightReader.weightSrc is "wjetsWeight"+dataEra
        def addWJetsWeight(mod, suffix):
            dataEra = mod.wjetsWeightReader.weightSrc.value().replace("wjetsWeight", "")
            weightName = "wjetsWeight"+dataEra+suffix
            if not hasattr(process, weightName):
                weightMod = wjetsWeight.getWJetsWeight(self.dataVersion, self.options, self.inputWorkflow, dataEra, suffix)
                setattr(process, weightName, weightMod)
                process.commonSequence *= weightMod
            mod.wjetsWeightReader.weightSrc = weightName

        names = []

        # Up variation
        module = self._cloneForVariation(getattr(process, name))

        if self.options.wjetsWeighting != 0:
            addWJetsWeight(module, "up")

        param.setPileupWeightForVariation(self.dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.pileupWeightReader, suffix="up")
        module.configInfo.pileupReweightType = PileupWeightType.toString[PileupWeightType.UP]
        names.append(self._addVariationModule(process, module, name+self.systPrefix+"PUWeightPlus"))

        # Down variation
        module = self._cloneForVariation(getattr(process, name))

        if self.options.wjetsWeighting != 0:
            addWJetsWeight(module, "down")

        param.setPileupWeightForVariation(self.dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.pileupWeightReader, suffix="down")
        module.configInfo.pileupReweightType = PileupWeightType.toString[PileupWeightType.DOWN]
        names.append(self._addVariationModule(process, module, name+self.systPrefix+"PUWeightMinus"))

        self._accumulateAnalyzers("PU weight variation", names)

    ## Build Top pt weight variation
    #
    # \param process                      cms.Process object
    # \param analysisNamesForSystematics  Names of the analysis modules for which the PU weight variation should be done
    def _buildTopPtWeightVariation(self, process, analysisNamesForSystematics):
        if not self.applyTopPtReweight:
            return
        if not (self.doTopPtWeightVariation or self.doSystematics):
            return

        if self.dataVersion.isMC():
            timer = Timer()
            for name in analysisNamesForSystematics:
                self._addTopPtWeightVariation(process, name)
            timer.stop("Added Top pt weight variation for %d modules in" % len(analysisNamesForSystematics))
        else:
            print "PU weight variation disabled for data (not meaningful for data)"

    ## Add Top pt weight variation
    #
    # \param process   cms.Process object
    # \param name      Name of the module to be used as a prototype
    def _addTopPtWeightVariation(self, process, name):
        def addVariation(direction, directionName, directionMode):
            module = self._cloneForVariation(getattr(process, name))
            if self.options.sample == "TTJets":
                weightName = module.topPtWeightReader.weightSrc.getModuleLabel()
                varyName = weightName+directionName
                if not hasattr(process, varyName):
                    varyMod = getattr(process, weightName).clone(
                        variationEnabled = True,
                        variationDirection = direction
                    )
                    setattr(process, varyName, varyMod)
                    process.commonSequence += varyMod
                module.topPtWeightReader.weightSrc = varyName
                module.configInfo.topPtReweightType = PileupWeightType.toString[directionMode]
            return self._addVariationModule(process, module, name+self.systPrefix+"TopPtWeight"+directionName)

        names = []
        names.append(addVariation(+1, "Plus", PileupWeightType.UP))
        names.append(addVariation(-1, "Minus", PileupWeightType.DOWN))
        self._accumulateAnalyzers("Top pt variation", names)

    ## Add scale factor variation
    #
    # \param process                      cms.Process object
    # \param analysisNamesForSystematics  Names of the analysis modules for which the PU weight variation should be done
    def _buildScaleFactorVariation(self, process, analysisNamesForSystematics):
        if not (self.doScaleFactorVariation or self.doSystematics):
            return

        if self.dataVersion.isMC() or self.options.tauEmbeddingInput != 0:
            timer = Timer()
            for name in analysisNamesForSystematics:
                self._addScaleFactorVariation(process, name)
            timer.stop("Added scale factor variation for %d modules in" % len(analysisNamesForSystematics))
        else:
            print "SF variation disabled for data (not meaningful for data"

    # Add scale factor variation for one module
    #
    # \param process   cms.Process object
    # \param name      Name of the module to be used as a prototype
    def _addScaleFactorVariation(self, process, name):
        embeddingData = self.options.tauEmbeddingInput != 0 and self.dataVersion.isData()

        def disablePrint(pset):
            if hasattr(pset, "printScaleFactors"):
                pset.printScaleFactors = False
        def variationBy(pset, shiftBy):
            setattr(pset, {
                "scaleFactor": "variationSFShiftBy",
                "dataEfficiency": "variationDataShiftBy",
                "mcEfficiency": "variationMCShiftBy"}[pset.mode.value()],
                    cms.double(shiftBy))
        def addTrgSF(attr, shiftBy, postfix):
            module = self._cloneForVariation(getattr(process, name))
            effSF = getattr(module, attr)
            effSF.variationEnabled = True
            effSF.useMaxUncertainty = True
            variationBy(effSF, shiftBy)
            disablePrint(effSF)
            return self._addVariationModule(process, module, name+self.systPrefix+postfix)
        def addTrgDataEff(attr, shiftBy, postfix):
            module = self._cloneForVariation(getattr(process, name))
            effSF = getattr(module, attr)
            effSF.variationEnabled = True
            effSF.useMaxUncertainty = False
            effSF.variationDataShiftBy = cms.double(shiftBy)
            effSF.variationMCShiftBy = cms.double(0.0)
            disablePrint(effSF)
            return self._addVariationModule(process, module, name+self.systPrefix+postfix)
        def addTrgMCEff(attr, shiftBy, postfix):
            module = self._cloneForVariation(getattr(process, name))
            effSF = getattr(module, attr)
            effSF.variationEnabled = True
            effSF.useMaxUncertainty = False
            effSF.variationMCShiftBy = cms.double(shiftBy)
            effSF.variationDataShiftBy = cms.double(0.0)
            disablePrint(effSF)
            return self._addVariationModule(process, module, name+self.systPrefix+postfix)

        def addTauTrgSF(shiftBy, postfix):
            return addTrgSF("tauTriggerEfficiencyScaleFactor", shiftBy, "TauTrgSF"+postfix)
        def addTauTrgDataEff(shiftBy, postfix):
            return addTrgDataEff("tauTriggerEfficiencyScaleFactor", shiftBy, "TauTrgDataEff"+postfix)
        def addTauTrgMCEff(shiftBy, postfix):
            return addTrgMCEff("tauTriggerEfficiencyScaleFactor", shiftBy, "TauTrgMCEff"+postfix)

        def addMETTrgSF(shiftBy, postfix, prefix):
            return addTrgSF("metTriggerEfficiencyScaleFactor", shiftBy, prefix+"SF"+postfix)
        def addMETTrgDataEff(shiftBy, postfix, prefix):
            return addTrgDataEff("metTriggerEfficiencyScaleFactor", shiftBy, prefix+"DataEff"+postfix)
        def addMETTrgMCEff(shiftBy, postfix, prefix):
            return addTrgMCEff("metTriggerEfficiencyScaleFactor", shiftBy, prefix+"MCEff"+postfix)

        def addMuonTrgDataEff(shiftBy, postfix):
            return addTrgDataEff("embeddingMuonTriggerEfficiency", shiftBy, "MuonTrgDataEff"+postfix)
        def addMuonIdDataEff(shiftBy, postfix):
            return addTrgDataEff("embeddingMuonIdEfficiency", shiftBy, "MuonIdDataEff"+postfix)

        def addEmbeddingMTWeight(shiftBy, postfix):
            # bin-based
            # return addTrgDataEff("embeddingMTWeight", shiftBy, "EmbMTWeight"+postfix)
            # fit-based
            module = self._cloneForVariation(getattr(process, name))
            module.embeddingMTWeight.variationEnabled = True
            module.embeddingMTWeight.variationDirection = shiftBy
            return self._addVariationModule(process, module, name+self.systPrefix+"EmbMTWeight"+postfix)

        def addBTagSF(shiftBy, postfix):
            module = self._cloneForVariation(getattr(process, name))
            module.bTagging.variationEnabled = True
            module.bTagging.variationShiftBy = shiftBy
            return self._addVariationModule(process, module, name+self.systPrefix+"BTagSF"+postfix)

        names = []

        # Tau trigger SF
        if self.applyTauTriggerScaleFactor or self.applyTauTriggerLowPurityScaleFactor:
            if self.options.tauEmbeddingInput != 0:
                names.append(addTauTrgDataEff( 1.0, "Plus"))
                names.append(addTauTrgDataEff(-1.0, "Minus"))
            else:
                if self.doAsymmetricTriggerUncertainties:
                    names.append(addTauTrgDataEff( 1.0, "Plus"))
                    names.append(addTauTrgDataEff(-1.0, "Minus"))
                    names.append(addTauTrgMCEff( 1.0, "Plus"))
                    names.append(addTauTrgMCEff(-1.0, "Minus"))
                else:
                    names.append(addTauTrgSF( 1.0, "Plus"))
                    names.append(addTauTrgSF(-1.0, "Minus"))

        # MET trigger SF
        if self.applyMETTriggerScaleFactor or self.applyL1ETMScaleFactor:
            prefix = "MetTrg"
            if self.applyL1ETMScaleFactor:
                prefix = "L1ETM"

            if self.options.tauEmbeddingInput != 0:
                names.append(addMETTrgDataEff( 1.0, "Plus", prefix))
                names.append(addMETTrgDataEff(-1.0, "Minus", prefix))
            else:
                if self.doAsymmetricTriggerUncertainties:
                    names.append(addMETTrgDataEff( 1.0, "Plus", prefix))
                    names.append(addMETTrgDataEff(-1.0, "Minus", prefix))
                    names.append(addMETTrgMCEff( 1.0, "Plus", prefix))
                    names.append(addMETTrgMCEff(-1.0, "Minus", prefix))
                else:
                    names.append(addMETTrgSF( 1.0, "Plus", prefix))
                    names.append(addMETTrgSF(-1.0, "Minus", prefix))

        # Embedding-specific
        if self.options.tauEmbeddingInput != 0:
            names.append(addMuonTrgDataEff( 1.0, "Plus"))
            names.append(addMuonTrgDataEff( -1.0, "Minus"))

            names.append(addMuonIdDataEff( 1.0, "Plus"))
            names.append(addMuonIdDataEff( -1.0, "Minus"))

            names.append(addEmbeddingMTWeight(1, "Plus"))
            names.append(addEmbeddingMTWeight(-1, "Minus"))

            if not hasattr(process, "wtaumuWeightPlus"):
                process.wtaumuWeightPlus = process.wtaumuWeight.clone(variationEnabled=True)
                process.wtaumuWeightMinus = process.wtaumuWeightPlus.clone(
                    variationAmount = -process.wtaumuWeightPlus.variationAmount.value()
                )
                process.commonSequence += (process.wtaumuWeightPlus + process.wtaumuWeightMinus)
            mod = self._cloneForVariation(getattr(process, name))
            mod.embeddingWTauMuWeightReader.weightSrc = "wtaumuWeightPlus"
            names.append(self._addVariationModule(process, mod, name+self.systPrefix+"WTauMuPlus"))

            mod = mod.clone()
            mod.embeddingWTauMuWeightReader.weightSrc = "wtaumuWeightMinus"
            names.append(self._addVariationModule(process, mod, name+self.systPrefix+"WTauMuMinus"))

        # BTag SF
        if not embeddingData:
            names.append(addBTagSF( 1.0, "Plus"))
            names.append(addBTagSF(-1.0, "Minus"))

        self._accumulateAnalyzers("SF variation", names)


def addPuWeightProducers(dataVersion, process, commonSequence, dataEras, firstInSequence=False):
    names = []
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
    for era in dataEras:
        names.append(param.setPileupWeight(dataVersion, process, commonSequence, era=era))

    if firstInSequence:
        for name in names:
            mod = getattr(process, name)
            commonSequence.remove(mod)
            commonSequence.insert(0, mod)

    return names

def addPuWeightProducersVariations(dataVersion, process, commonSequence, dataEras, doVariations=True):
    ret = []
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
    for era in dataEras:
        name = param.setPileupWeight(dataVersion, process, commonSequence, era=era)
        ret.append( (era, "",  name) )
        nominalModule = getattr(process, name)
        if doVariations:
            for suffix in ["up", "down"]:
                ret.append( (era, suffix,
                             param.setPileupWeightForVariation(dataVersion, process, commonSequence, suffix=suffix,
                                                               pset=nominalModule.clone(), psetReader=param.pileupWeightReader))
                            )

    return ret
