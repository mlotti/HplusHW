import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions as HChOptions
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
import HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation as jesVariation
import HiggsAnalysis.HeavyChHiggsToTauNu.WJetsWeight as wjetsWeight
from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme

tooManyAnalyzersLimit = 100

defaultOptimisation = HPlusOptimisationScheme()
#defaultOptimisation.addTauPtVariation([40.0, 50.0])

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
                 histogramAmbientLevelOptimization = "Vital",
                 histogramAmbientLevelSystematics = "Systematics",
                 applyTauTriggerScaleFactor = True, # Apply tau trigger scale factor or not
                 applyMETTriggerScaleFactor = False, # Apply MET trigger scale factor or not
                 applyPUReweight = True, # Apply PU weighting or not
                 tauSelectionOperatingMode = "standard", # standard, tauCandidateSelectionOnly
                # tauSelectionOperatingMode = "tauCandidateSelectionOnly",   
                 useTriggerMatchedTaus = True,
                 useCHSJets = False,
                 useJERSmearedJets = True,
                 useBTagDB = False,
                 customizeLightAnalysis = None,
                 customizeHeavyAnalysis = None,

                 doLightAnalysis = True,
                 doHeavyAnalysis = False,

                 pickEvents = True, # Produce pickEvents.txt
                 doSystematics = False, # Running of systematic variations is controlled by the global flag (below), or the individual flags
                 doQCDTailKillerScenarios = False, # Run different scenarios of the QCD tail killer (improved delta phi cuts)
                 doJESVariation = False, # Perform the signal analysis with the JES variations in addition to the "golden" analysis
                 doPUWeightVariation = False, # Perform the signal analysis with the PU weight variations
                 doOptimisation = False, optimisationScheme=defaultOptimisation, # Do variations for optimisation
                 allowTooManyAnalyzers = False, # Allow arbitrary number of analyzers (beware, it might take looong to run and merge)
                 printAnalyzerNames = False,
                 inputWorkflow = "pattuple_v44_5", # Name of the workflow, whose output is used as an input, needed for WJets weighting
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
        self.applyMETTriggerScaleFactor = applyMETTriggerScaleFactor
        self.applyPUReweight = applyPUReweight
        self.tauSelectionOperatingMode = tauSelectionOperatingMode
        self.useTriggerMatchedTaus = useTriggerMatchedTaus
        self.useCHSJets = useCHSJets
        self.useJERSmearedJets = useJERSmearedJets
        self.useBTagDB = useBTagDB
        self.customizeLightAnalysis = customizeLightAnalysis
        self.customizeHeavyAnalysis = customizeHeavyAnalysis

        self.doLightAnalysis = doLightAnalysis
        self.doHeavyAnalysis = doHeavyAnalysis
        if not self.doLightAnalysis and not self.doHeavyAnalysis:
            raise Exception("At least one of doLightAnalysis and doHeavyAnalysis must be set to True (otherwise nothing is done)")

        self.pickEvents = pickEvents
        self.doSystematics = doSystematics
        self.doJESVariation = doJESVariation
        self.doPUWeightVariation = doPUWeightVariation
        self.doOptimisation = doOptimisation
        self.optimisationScheme = optimisationScheme
        self.allowTooManyAnalyzers = allowTooManyAnalyzers
        self.printAnalyzerNames = printAnalyzerNames

        self.inputWorkflow = inputWorkflow

        if self.doMETResolution and self.doOptimisation:
            raise Exception("doMETResolution and doOptimisation conflict")

        if self.options.wjetsWeighting != 0:
            if not self.dataVersion.isMC():
                raise Exception("Command line option 'wjetsWeighting' works only with MC")
            if self.options.tauEmbeddingInput != 0:
                raise Exception("There are no WJets weights for embedding yet")

        if self.doOptimisation or self.doAgainstElectronScan or self.doTauIsolationAndJetPUScan:
            #self.doSystematics = True            # Make sure that systematics are run
            self.doFillTree = False              # Make sure that tree filling is disabled or root file size explodes
            self.histogramAmbientLevel = histogramAmbientLevelOptimization # Set histogram level to least histograms to reduce output file sizes

        if self.doBTagTree:
            self.tauSelectionOperatingMode = 'tauCandidateSelectionOnly'

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
        param = self._buildParam()

        # Btagging DB
        self._useBTagDB(process, param)

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

                for module, name in zip(modules, analysisNames_):
                    mod = module.clone()
                    if self.applyTauTriggerScaleFactor:
                        param.setDataTriggerEfficiency(self.dataVersion, era=dataEra, pset=mod.tauTriggerEfficiencyScaleFactor)
                    if self.applyPUReweight:
                        param.setPileupWeight(self.dataVersion, process=process, commonSequence=process.commonSequence, pset=mod.vertexWeight, psetReader=mod.pileupWeightReader, era=dataEra)
                        if self.options.wjetsWeighting != 0:
                            mod.wjetsWeightReader.weightSrc = "wjetsWeight"+dataEra
                            mod.wjetsWeightReader.enabled = True

                    if self.doLightAnalysis:
                        analysisLightModules.append(mod)
                        analysisLightNames.append(name+"Light"+dataEra)
                    if self.doHeavyAnalysis:
                        analysisLightModules.append(param.cloneForHeavyAnalysis(mod))
                        analysisLightNames.append(name+"Heavy"+dataEra)

                    print "Added analysis for PU weight era =", dataEra

        analysisModules = analysisLightModules+analysisHeavyModules
        analysisNames = analysisLightNames+analysisHeavyNames

        analysisNamesForSystematics = []
        # For optimisation, no systematics
        # For embedding input, the systematics should be evaluated with the analyzer with Muon eff, Tau trigger eff, CaloMET>60 (this is added to analysisNamesForSystematics later)
        if not self.doOptimisation and self.options.tauEmbeddingInput == 0:
            analysisNamesForSystematics = analysisNames[:]

        for module in analysisModules:
            module.Tree.fill = self.doFillTree
            module.histogramAmbientLevel = self.histogramAmbientLevel
            module.tauEmbeddingStatus = (self.options.tauEmbeddingInput != 0)
            if len(additionalCounters) > 0:
                module.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])
        if len(analysisLightModules) > 0:
            analysisLightModules[0].eventCounter.printMainCounter = cms.untracked.bool(True)
            #analysisLightModules[0].eventCounter.printSubCounters = cms.untracked.bool(True)
        if len(analysisHeavyModules) > 0:
            analysisHeavyModules[0].eventCounter.printMainCounter = cms.untracked.bool(True)
            #analysisHeavyModules[0].eventCounter.printSubCounters = cms.untracked.bool(True)

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

        # Construct normal path
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
            for module, name in zip(analysisModules, analysisNames):
                names = self.optimisationScheme.generateVariations(process, additionalCounters, process.commonSequence, module, name)
                self._accumulateAnalyzers("Optimisation", names)
                analysisNamesForSystematics.extend(names)

        # QCD tail killer scenarios
        self._buildQCDTailKillerScenarios(process, analysisModules, analysisNames)

        # Against electron scan
        self._buildAgainstElectronScan(process, analysisModules, analysisNames)

        # scan for tau isolation and jet PU ID
        self._buildTauIsolationAndJetPUScan(process, analysisModules, analysisNames)

        # scan various btagging working points
        self._buildBTagScan(process, analysisModules, analysisNames)

        # Tau embedding-like preselection for normal MC
        analysisNamesForSystematics.extend(self._buildTauEmbeddingLikePreselection(process, analysisModules, analysisNames, additionalCounters))

        # Additional analyses for tau embedding input (with caloMET>60 and tau-efficiency)
        analysisNamesForSystematics.extend(self._additionalTauEmbeddingAnalyses(process, analysisModules, analysisNames))

        ## Systematics
        if "QCDMeasurement" not in analysisNames_:
            self._buildJESVariation(process, analysisNamesForSystematics)
            self._buildPUWeightVariation(process, analysisNamesForSystematics, param)

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

        # Set PU ID src for modules
        for name in self.getAnalyzerModuleNames():
            param.setJetPUIdSrc(getattr(process, name).jetSelection, name)

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
            process.GlobalTag.globaltag = "START44_V13::All"
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
        process.commonSequence, additionalCounters = addPatOnTheFly(process, self.options, self.dataVersion)

        # Add configuration information to histograms.root
        from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
        process.infoPath = addConfigInfo(process, self.options, self.dataVersion)

        return (process, additionalCounters)

    ## Configure HChSignalAnalysisParameters_cff
    #
    # \return HChSignalAnalysisParameters_cff module object
    def _buildParam(self):
        # Trigger from command line options
        import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
        param.overrideTriggerFromOptions(self.options)
        param.trigger.triggerSrc.setProcessName(self.dataVersion.getTriggerProcess())

        # Tau selection operating mode
        param.setAllTauSelectionOperatingMode(self.tauSelectionOperatingMode)

        # Trigger-matched taus
        if self.useTriggerMatchedTaus:
            param.setAllTauSelectionSrcSelectedPatTausTriggerMatched()
        else:
            param.setAllTauSelectionSrcSelectedPatTaus()

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
                param.tauTriggerEfficiencyScaleFactor.mode = "scaleFactor"
            if self.applyMETTriggerScaleFactor:
                param.metTriggerEfficiencyScaleFactor.mode = "scaleFactor"

        if self.doBTagTree:
            param.tree.fillNonIsoLeptonVars = True
            param.MET.METCut = 0.0
            param.bTagging.discriminatorCut = -999
            param.GlobalMuonVeto.MuonPtCut = 999

        return param

    ## Setup b tag DB
    #
    # \param process  cms.Process object
    # \param param    HChSignalAnalysisParameters_cff module object
    def _useBTagDB(self, process, param):
        if not self.useBTagDB:
            return

        process.load("CondCore.DBCommon.CondDBCommon_cfi")
        #MC measurements 
        process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDBMC36X")
        process.load ("RecoBTag.PerformanceDB.BTagPerformanceDBMC36X")
        #Data measurements
        process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1107")
        process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1107")
        #User DB for btag eff
        if options.runOnCrab != 0:
            print "BTagDB: Assuming that you are running on CRAB"
            btagDB = "sqlite_file:src/HiggsAnalysis/HeavyChHiggsToTauNu/data/DBs/BTAGTCHEL_hplusBtagDB_TTJets.db"
        else:
            print "BTagDB: Assuming that you are not running on CRAB (if you are running on CRAB, add to job parameters in multicrab.cfg runOnCrab=1)"
            # This way signalAnalysis can be ran from any directory
            import os
            btagDB = "sqlite_file:%s/src/HiggsAnalysis/HeavyChHiggsToTauNu/data/DBs/BTAGTCHEL_hplusBtagDB_TTJets.db" % os.environ["CMSSW_BASE"]
        process.CondDBCommon.connect = btagDB
        process.load ("HiggsAnalysis.HeavyChHiggsToTauNu.Pool_BTAGTCHEL_hplusBtagDB_TTJets")
        process.load ("HiggsAnalysis.HeavyChHiggsToTauNu.Btag_BTAGTCHEL_hplusBtagDB_TTJets")
        param.bTagging.UseBTagDB  = False

    ## Setup for tau embedding input
    #
    # \param process  cms.Process object
    # \param param    HChSignalAnalysisParameters_cff module object
    def _customizeTauEmbeddingInput(self, process, param):
        ret = []
        if self.options.tauEmbeddingInput != 0:
            #tauEmbeddingCustomisations.addMuonIsolationEmbeddingForSignalAnalysis(process, process.commonSequence)
            tauEmbeddingCustomisations.setCaloMetSum(process, process.commonSequence, self.options, self.dataVersion)
            tauEmbeddingCustomisations.customiseParamForTauEmbedding(param, self.options, self.dataVersion)
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


    ## Build array of analyzers to scan various QCD tail killer scenarios
    #
    # \param process          cms.Process object
    # \param analysisModules  List of analysis modules to be used as prototypes
    # \param analysisNames    List of analysis module names
    def _buildQCDTailKillerScenarios(self, process, analysisModules, analysisNames):
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
            return

        from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import QCDTailKillerBin
        names = []
        modules = []
        for module, name in zip(analysisModules, analysisNames):
            # Loose scenario
            mod = module.clone()
            mod.QCDTailKiller.backToBack = cms.untracked.VPSet(
                QCDTailKillerBin("circular", 40.0, 40.0), # jet 1
                QCDTailKillerBin("circular", 40.0, 40.0), # jet 2
                QCDTailKillerBin("circular", 40.0, 40.0), # jet 3
                QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
            )
            mod.QCDTailKiller.collinear = cms.untracked.VPSet()
            createQCDTailKillerModule(process, "QCDTailKillerLoose", mod, names, modules)
            # Medium scenario
            mod = module.clone()
            mod.QCDTailKiller.backToBack = cms.untracked.VPSet(
                QCDTailKillerBin("circular", 60.0, 60.0), # jet 1
                QCDTailKillerBin("circular", 60.0, 60.0), # jet 2
                QCDTailKillerBin("circular", 60.0, 60.0), # jet 3
                QCDTailKillerBin("noCut", 60.0, 60.0), # jet 4
            )
            mod.QCDTailKiller.collinear = cms.untracked.VPSet()
            createQCDTailKillerModule(process, "QCDTailKillerMedium", mod, names, modules)
            # Medium plus scenario
            mod = module.clone()
            mod.QCDTailKiller.backToBack = cms.untracked.VPSet(
                QCDTailKillerBin("circular", 60.0, 60.0), # jet 1
                QCDTailKillerBin("circular", 60.0, 60.0), # jet 2
                QCDTailKillerBin("circular", 60.0, 60.0), # jet 3
                QCDTailKillerBin("noCut", 60.0, 60.0), # jet 4
            )
            mod.QCDTailKiller.collinear = cms.untracked.VPSet(
                QCDTailKillerBin("triangular", 40.0, 40.0), # jet 1
                QCDTailKillerBin("triangular", 40.0, 40.0), # jet 2
                QCDTailKillerBin("triangular", 40.0, 40.0), # jet 3
                QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
            )
            createQCDTailKillerModule(process, "QCDTailKillerMediumPlus", mod, names, modules)
            # Tight scenario
            mod = module.clone()
            mod.QCDTailKiller.backToBack = cms.untracked.VPSet(
                QCDTailKillerBin("circular", 80.0, 80.0), # jet 1
                QCDTailKillerBin("circular", 80.0, 80.0), # jet 2
                QCDTailKillerBin("circular", 80.0, 80.0), # jet 3
                QCDTailKillerBin("noCut", 80.0, 80.0), # jet 4
            )
            mod.QCDTailKiller.collinear = cms.untracked.VPSet()
            createQCDTailKillerModule(process, "QCDTailKillerTight", mod, names, modules)
            # Tight plus scenario
            mod = module.clone()
            mod.QCDTailKiller.backToBack = cms.untracked.VPSet(
                QCDTailKillerBin("circular", 80.0, 80.0), # jet 1
                QCDTailKillerBin("circular", 80.0, 80.0), # jet 2
                QCDTailKillerBin("circular", 80.0, 80.0), # jet 3
                QCDTailKillerBin("noCut", 80.0, 80.0), # jet 4
            )
            mod.QCDTailKiller.collinear = cms.untracked.VPSet(
                QCDTailKillerBin("triangular", 40.0, 40.0), # jet 1
                QCDTailKillerBin("triangular", 40.0, 40.0), # jet 2
                QCDTailKillerBin("triangular", 40.0, 40.0), # jet 3
                QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
            )
            createQCDTailKillerModule(process, "QCDTailKillerTightPlus", mod, names, modules)
        self._accumulateAnalyzers("Modules for QCDTailKiller scenarios", names)
        analysisModules.extend(modules)
        analysisNames.extend(names)

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
        analysisModules.extend(modules)
        analysisNames.extend(names)

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
        analysisModules.extend(modules)
        analysisNames.extend(names)

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
        myJPTWorkingPoints = [0.275, 0.545, 0.790]

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
        analysisModules.extend(modules)
        analysisNames.extend(names)

    ## Build "tau embedding"-like preselection for normal MC
    #
    # \param process             cms.Process object
    # \param analysisModules     List of analysis modules to be used as prototypes
    # \param analysisNames       List of analysis module names
    # \param additionalCounters  List of strings for additional counters
    def _buildTauEmbeddingLikePreselection(self, process, analysisModules, analysisNames, additionalCounters):
        if self.options.doTauEmbeddingLikePreselection == 0:
            return []

        if self.dataVersion.isData():
            raise Exception("doTauEmbeddingLikePreselection is meaningless for data")
        if self.options.tauEmbeddingInput != 0:
            raise Exception("tauEmbegginInput clashes with doTauEmbeddingLikePreselection")
        
        allNames = []
        def add(name, sequence, module, counters):
            module.eventCounter.counters = [cms.InputTag(c) for c in counters]
            setattr(process, name+"Sequence", sequence)
            setattr(process, name, module)
            allNames.append(name)
            path = cms.Path(sequence * module)
            setattr(process, name+"Path", path)

        retNames = []

        for module, name in zip(analysisModules, analysisNames):
            # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), no tau+MET trigger required
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, seq, mod, prefix=name+"EmbeddingLikePreselection"))
            add(name+"TauEmbeddingLikePreselection", seq, mod, counters)

            # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), tau+MET trigger required
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, seq, mod, prefix=name+"EmbeddingLikeTriggeredPreselection", disableTrigger=False))
            add(name+"TauEmbeddingLikeTriggeredPreselection", seq, mod, counters)
            
            # Genuine tau preselection
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addGenuineTauPreselection(process, seq, mod, prefix=name+"GenuineTauPreselection"))
            add(name+"GenuineTauPreselection", seq, mod, counters)

            # Require genuine tau after tau ID in analysis
            mod = module.clone()
            module.onlyGenuineTaus = cms.untracked.bool(True)
            setattr(process, name+"GenuineTau", mod)
            path = cms.Path(process.commonSequence * mod)
            setattr(process, name+"GenuineTauPath", path)
            retNames.append(name+"GenuineTau")
        self._accumulateAnalyzers("Tau embedding -like preselection", allNames)
        return retNames

    ## Build additional analyses for tau embedding input
    #
    # \param process          cms.Process object
    # \param analysisModules  List of analysis modules to be used as prototypes
    # \param analysisNames    List of analysis module names
    def _additionalTauEmbeddingAnalyses(self, process, analysisModules, analysisNames):
        if self.options.tauEmbeddingInput == 0:
            return []

        allNames = []
        retNames = []
        for module, name in zip(analysisModules, analysisNames):
            postfix = "MEff"
            mod = module.clone()
            mod.embeddingMuonEfficiency.mode = "efficiency"
            path = cms.Path(process.commonSequence * mod)
            setattr(process, name+postfix, mod)
            setattr(process, name+postfix+"Path", path)
            allNames.append(name+postfix)

            postfix += "CaloMet60"
            mod = mod.clone()
            mod.trigger.caloMetSelection.metEmulationCut = 60.0
            path = cms.Path(process.commonSequence * mod)
            setattr(process, name+postfix, mod)
            setattr(process, name+postfix+"Path", path)
            allNames.append(name+postfix)

            postfix += "TEff"
            mod = mod.clone()
            mod.tauTriggerEfficiencyScaleFactor.mode = "efficiency"
            path = cms.Path(process.commonSequence * mod)
            setattr(process, name+postfix, mod)
            setattr(process, name+postfix+"Path", path)
            allNames.append(name+postfix)
            retNames.append(name+postfix)
        self._accumulateAnalyzers("Tau embedding analyses", allNames)
        return retNames

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
            for name in analysisNamesForSystematics:
                self._addJESVariation(process, name, doJetUnclusteredVariation)
            print "Added JES variation for %d modules"%len(analysisNamesForSystematics)
        else:
            print "JES variation disabled for data (not meaningful for data)"


    ## Add JES variation for one module
    #
    # \param process                    cms.Process object
    # \param name                       Name of the module to be used as a prototype
    # \param doJetUnclusteredVariation  Flag if JES+JER+UES variations should be done
    def _addJESVariation(self, process, name, doJetUnclusteredVariation):
        module = getattr(process, name)

        module = module.clone()
        module.Tree.fill = False
        module.Tree.fillJetEnergyFractions = False # JES variation will make the fractions invalid
        module.histogramAmbientLevel = self.histogramAmbientLevelSystematics

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

    ## Build PU weight variation
    #
    # \param process                      cms.Process object
    # \param analysisNamesForSystematics  Names of the analysis modules for which the PU weight variation should be done
    def _buildPUWeightVariation(self, process, analysisNamesForSystematics, param):
        if not self.applyPUReweight:
            return
        if not (self.doPUWeightVariation or self.doSystematics):
            return

        if self.dataVersion.isMC():
            for name in analysisNamesForSystematics:
                self._addPUWeightVariation(process, name, param)
            print "Added PU weight variation for %d modules"%len(analysisNamesForSystematics)
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
        module = getattr(process, name).clone()
        module.Tree.fill = False
        module.eventCounter.printMainCounter = cms.untracked.bool(False)
        module.histogramAmbientLevel = self.histogramAmbientLevelSystematics

        if self.options.wjetsWeighting != 0:
            addWJetsWeight(module, "up")

        param.setPileupWeightForVariation(self.dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.pileupWeightReader, suffix="up")
        path = cms.Path(process.commonSequence * module)
        modName = name+self.systPrefix+"PUWeightPlus"
        setattr(process, modName, module)
        setattr(process, modName+"Path", path)
        names.append(modName)

        # Down variation
        module = getattr(process, name).clone()
        module.Tree.fill = False
        module.eventCounter.printMainCounter = cms.untracked.bool(False)
        module.histogramAmbientLevel = self.histogramAmbientLevelSystematics

        if self.options.wjetsWeighting != 0:
            addWJetsWeight(module, "down")

        param.setPileupWeightForVariation(self.dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.pileupWeightReader, suffix="down")
        path = cms.Path(process.commonSequence * module)
        modName = name+self.systPrefix+"PUWeightMinus"
        setattr(process, modName, module)
        setattr(process, modName+"Path", path)
        names.append(modName)

        self._accumulateAnalyzers("PU weight variation", names)
