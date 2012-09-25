import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions as HChOptions
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
import HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation as jesVariation

tooManyAnalyzersLimit = 100

## Infrastucture to help analysis configuration building
class ConfigBuilder:
    ## Constructor
    #
    # \param dataVersion   String for data version
    # \param dataEras      List of strings of data (or PU weight) eras. One
    #                      analyzer per era is constructed
    def __init__(self, dataVersion, dataEras,
                 # Job options
                 processName = "Analysis",
                 maxEvents = -1,
                 useDefaultInputFiles = True,
                 edmOutput = False,
                 # Optional options
                 doAgainstElectronScan = False, # Scan against electron discriminators
                 doBTagTree = False, # fill tree for btagging eff study
                 doMETResolution = False, # Make MET resolution histograms
                 tauEmbeddingFinalizeMuonSelection = True, # With tau embedding input, tighten the muon selection
                 doPrescalesForData = False, # Keep / Ignore prescaling for data (suppresses greatly error messages in datasets with or-function of triggers)
                 doFillTree = False, # Tree filling
                 histogramAmbientLevel = "Debug", # Set level of how many histograms are stored to files options are: 'Vital' (least histograms), 'Informative', 'Debug' (all histograms),
                 applyTriggerScaleFactor = True, # Apply trigger scale factor or not
                 tauSelectionOperatingMode = "standard", # standard, tauCandidateSelectionOnly
                 useTriggerMatchedTaus = True,
                 useJERSmearedJets = True,
                 useBTagDB = False,
                 customizeAnalysis = None,

                 doSystematics = False, # Running of systematic variations is controlled by the global flag (below), or the individual flags
                 doJESVariation = False, # Perform the signal analysis with the JES variations in addition to the "golden" analysis
                 doPUWeightVariation = False, # Perform the signal analysis with the PU weight variations
                 doOptimisation = False, optimisationScheme=None, # Do variations for optimisation
                 allowTooManyAnalyzers = False, # Allow arbitrary number of analyzers (beware, it might take looong to run and merge)
                 ):
        self.options, self.dataVersion = HChOptions.getOptionsDataVersion(dataVersion)
        self.dataEras = dataEras

        self.processName = processName
        self.maxEvents = maxEvents
        self.useDefaultInputFiles = useDefaultInputFiles
        self.edmOutput = edmOutput

        self.doAgainstElectronScan = doAgainstElectronScan
        self.doBTagTree = doBTagTree
        self.doMETResolution = doMETResolution
        self.doPrescalesForData = doPrescalesForData
        self.doFillTree = doFillTree
        self.histogramAmbientLevel = histogramAmbientLevel
        self.applyTriggerScaleFactor = applyTriggerScaleFactor
        self.tauSelectionOperatingMode = tauSelectionOperatingMode
        self.useTriggerMatchedTaus = useTriggerMatchedTaus
        self.useJERSmearedJets = useJERSmearedJets
        self.useBTagDB = useBTagDB
        self.customizeAnalysis = customizeAnalysis

        self.doSystematics = doSystematics
        self.doJESVariation = doJESVariation
        self.doPUWeightVariation = doPUWeightVariation
        self.doOptimisation = doOptimisation
        self.optimisationScheme = optimisationScheme
        self.allowTooManyAnalyzers = allowTooManyAnalyzers

        if self.doMETResolution and self.doOptimisation:
            raise Exception("doMETResolution and doOptimisation conflict")
            

        if self.doOptimisation:
            self.doSystematics = True            # Make sure that systematics are run
            self.doFillTree = False              # Make sure that tree filling is disabled or root file size explodes
            self.histogramAmbientLevel = "Vital" # Set histogram level to least histograms to reduce output file sizes

        if self.doBTagTree:
            self.tauSelectionOperatingMode = 'tauCandidateSelectionOnly'

        self.numberOfAnalyzers = {}
        self.analyzerCategories = []


    def buildSignalAnalysis(self):
        import HiggsAnalysis.HeavyChHiggsToTauNu.signalAnalysis as signalAnalysis
        def create(param):
            return [signalAnalysis.createEDFilter(param)]
        return self._build(create, ["signalAnalysis"])

    def _accumulateAnalyzers(self, key, number):
        if not key in self.numberOfAnalyzers:
            self.analyzerCategories.append(key)

        self.numberOfAnalyzers[key] = self.numberOfAnalyzers.get(key, 0) + number

    def _checkNumberOfAnalyzers(self):
        print "Created analyzers in following categories"
        width = max([len(cat) for cat in self.analyzerCategories]) 
        fmt = "  %%-%ds: %%d" % width
        s = 0
        for cat in self.analyzerCategories:
            n = self.numberOfAnalyzers[cat]
            s += n
            print fmt % (cat, n)
        print "  "+("-" * (width+4))
        print fmt % ("Total", s)
        print

        if s > tooManyAnalyzersLimit:
            if self.allowTooManyAnalyzers:
                print "Total number of analyzers (%d) is over the suggested limit (%d), it might take loong to run and merge output" % (s, tooManyAnalyzersLimit)
            else:
                raise Exception("Total number of analyzers (%d) exceeds the suggested limit (%d). If you're sure you want to run so many analyzers, add 'allowTooManyAnalyzers=True' to the ConfigBuilder() constructor call." % (s, tooManyAnalyzersLimit))

    def _build(self, createAnalysesFunction, analysisNames_):
        # Common initialization
        (process, additionalCounters) = self._buildCommon()

        # Import and customize HChSignalAnalysisParameters
        param = self._buildParam()

        # Btagging DB
        self._useBTagDB(process, param)

        # Tau embedding input handling
        self._customizeTauEmbeddingInput(process, param)

        # Create analysis module(s)
        modules = createAnalysesFunction(param)
        if self.dataVersion.isData():
            analysisModules = modules
            analysisNames = analysisNames_[:]
        else:
            # For MC, produce the PU-reweighted analyses
            analysisModules = []
            analysisNames = []
            for module, name in zip(modules, analysisNames_):
                for dataEra in self.dataEras:
                    mod = module.clone()
                    param.setDataTriggerEfficiency(self.dataVersion, era=dataEra, pset=mod.triggerEfficiencyScaleFactor)
                    param.setPileupWeight(self.dataVersion, process=process, commonSequence=process.commonSequence, pset=mod.vertexWeight, psetReader=mod.vertexWeightReader, era=dataEra)
                    print "Added analysis for PU weight era =", dataEra
                    analysisModules.append(mod)
                    analysisNames.append(name+dataEra)

        analysisNamesForSystematics = analysisNames[:]
        self._accumulateAnalyzers("Data eras", len(analysisModules))

        for module in analysisModules:
            module.Tree.fill = self.doFillTree
            module.histogramAmbientLevel = self.histogramAmbientLevel
            module.tauEmbeddingStatus = (self.options.tauEmbeddingInput != 0)
            if len(additionalCounters) > 0:
                module.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])
        analysisModules[0].eventCounter.printMainCounter = cms.untracked.bool(True)
        #analysisModules[0].eventCounter.printSubCounters = cms.untracked.bool(True)

        # Prescale fetching done automatically for data
        if self.dataVersion.isData() and self.options.tauEmbeddingInput == 0 and self.doPrescalesForData:
            process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
            process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(self.dataVersion.getTriggerProcess())
            process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
            process.commonSequence *= process.hplusPrescaleWeightProducer
            process.signalAnalysis.prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer")

        # Allow customization AFTER all settings have been applied, and BEFORE the printout
        if self.customizeAnalysis != None:
            for module in analysisModules:
                self.customizeAnalysis(module)
        
        # Print output
        self._printModule(analysisModules[0])

        # Construct normal path
        if not self.doOptimisation:
            process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
            for module, name in zip(analysisModules, analysisNames):
                setattr(process, name, module)
                path = cms.Path(process.commonSequence * module)
                setattr(process, name+"Path", path)
            # PickEvens only for the first analysis path
            p = getattr(process, analysisNames[0]+"Path")
            p *= process.PickEvents

            if self.doMETResolution:
                process.load("HiggsAnalysis.HeavyChHiggsToTauNu.METResolutionAnalysis_cfi")
                p *= process.metResolutionAnalysis
        # Construct paths for optimisation
        else:
            for module, name in zip(analysisModules, analysisNames):
                names = self.optimisationScheme.generateVariations(process, additionalCounters, process.commonSequence, module, name)
                self._accumulateAnalyzers("Optimisation", len(names))
                analysisNamesForSystematics.extend(names)

        # Against electron scan
        self._buildAgainstElectronScan(process, analysisModules, analysisNames)

        # Tau embedding-like preselection for normal MC
        analysisNamesForSystematics.extend(self._buildTauEmbeddingLikePreselection(process, analysisModules, analysisNames, additionalCounters))

        # Additional analyses for tau embedding input (with caloMET>60 and tau-efficiency)
        analysisNamesForSystematics.extend(self._additionalTauEmbeddingAnalyses(process, analysisModules, analysisNames))

        ## Systematics
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

        self._checkNumberOfAnalyzers()

        return process

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
            process.source.fileNames.append(self.dataVersion.getAnalysisDefaultFileMadhatter())
        if self.options.tauEmbeddingInput != 0:
            if options.doPat == 0:
                raise Exception("In tau embedding input mode, set also doPat=1")
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

        # JER-smeared jets
        if self.useJERSmearedJets:
            param.setJERSmearedJets(self.dataVersion)

        # Trigger with scale factors (at the moment hard coded)
        if self.applyTriggerScaleFactor and self.dataVersion.isMC():
            param.triggerEfficiencyScaleFactor.mode = "scaleFactor"

        if self.doBTagTree:
            param.tree.fillNonIsoLeptonVars = True
            param.MET.METCut = 0.0
            param.bTagging.discriminatorCut = -999
            param.GlobalMuonVeto.MuonPtCut = 999

        return param

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

    def _customizeTauEmbeddingInput(self, process, param):
        if self.options.tauEmbeddingInput != 0:
            #tauEmbeddingCustomisations.addMuonIsolationEmbeddingForSignalAnalysis(process, process.commonSequence)
            tauEmbeddingCustomisations.setCaloMetSum(process, process.commonSequence, options, self.dataVersion)
            tauEmbeddingCustomisations.customiseParamForTauEmbedding(param, options, self.dataVersion)
            if self.tauEmbeddingFinalizeMuonSelection:
                # applyIsolation = not doTauEmbeddingMuonSelectionScan
                applyIsolation = False
                additionalCounters.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param,
                                                                                           enableIsolation=applyIsolation))
    def _printModule(self, module):
        #print "\nAnalysis is blind:", module.blindAnalysisStatus, "\n"
        print "Histogram level:", module.histogramAmbientLevel.value()
        print "Trigger:", module.trigger
        print "Trigger scale factor mode:", module.triggerEfficiencyScaleFactor.mode.value()
        print "Trigger scale factor data:", module.triggerEfficiencyScaleFactor.dataSelect.value()
        print "Trigger scale factor MC:", module.triggerEfficiencyScaleFactor.mcSelect.value()
        print "VertexWeight data distribution:",module.vertexWeight.dataPUdistribution.value()
        print "VertexWeight mc distribution:",module.vertexWeight.mcPUdistribution.value()
        print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", module.trigger.hltMetCut.value()
        #print "TauSelection algorithm:", module.tauSelection.selection.value()
        print "TauSelection algorithm:", module.tauSelection.selection.value()
        print "TauSelection src:", module.tauSelection.src.value()
        print "TauVetoSelection src:", module.vetoTauSelection.tauSelection.src.value()
        print "TauSelection isolation:", module.tauSelection.isolationDiscriminator.value()
        print "TauSelection operating mode:", module.tauSelection.operatingMode.value()
        print "VetoTauSelection src:", module.vetoTauSelection.tauSelection.src.value()
        print "Beta cut: ", module.jetSelection.betaCutSource.value(), module.jetSelection.betaCutDirection.value(), module.jetSelection.betaCut.value()
        print "electrons: ", module.GlobalElectronVeto
        print "muons: ", module.GlobalMuonVeto
        print "jets: ", module.jetSelection

    def _buildAgainstElectronScan(self, process, analysisModules, analysisNames):
        if not self.doAgainstElectronScan:
            return

        myTauIsolation = "byMediumCombinedIsolationDeltaBetaCorr"
        electronDiscriminators = [
            "againstElectronLoose",
            "againstElectronMedium",
            "againstElectronTight",
            "againstElectronMVA"
            ]
        N = 0
        for module, name in zip(analysisModules, analysisNames):
            for eleDisc in electronDiscriminators:
                mod = module.clone()
                mod.tauSelection.isolationDiscriminator = myTauIsolation
                mod.tauSelection.againstElectronDiscriminator = eleDisc
                modName = name+eleDisc[0].upper()+eleDisc[1:]
                setattr(process, modName, mod)
                path = cms.Path(process.commonSequence * mod)
                setattr(process, modName+"Path", path)
                N += 1
        self._accumulateAnalyzers("AgainstElectron scan", N)
 

    def _buildTauEmbeddingLikePreselection(self, process, analysisModules, analysisNames, additionalCounters):
        if self.options.doTauEmbeddingLikePreselection == 0:
            return []

        if self.dataVersion.isData():
            raise Exception("doTauEmbeddingLikePreselection is meaningless for data")
        if self.options.tauEmbeddingInput != 0:
            raise Exception("tauEmbegginInput clashes with doTauEmbeddingLikePreselection")
        
        def add(name, sequence, module, counters):
            module.eventCounter.counters = [cms.InputTag(c) for c in counters]
            setattr(process, name+"Sequence", sequence)
            setattr(process, name, module)
            path = cms.Path(sequence * module)
            setattr(process, name+"Path", path)

        retNames = []

        N = 0
        for module, name in zip(analysisModules, analysisNames):
            # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), no tau+MET trigger required
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, seq, mod, prefix=name+"EmbeddingLikePreselection"))
            add(name+"TauEmbeddingLikePreselection", seq, mod, counters)
            N += 1

            # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), tau+MET trigger required
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, seq, mod, prefix=name+"EmbeddingLikeTriggeredPreselection", disableTrigger=False))
            add(name+"TauEmbeddingLikeTriggeredPreselection", seq, mod, counters)
            N += 1
            
            # Genuine tau preselection
            seq = cms.Sequence(process.commonSequence)
            mod = module.clone()
            counters = additionalCounters[:]
            counters.extend(tauEmbeddingCustomisations.addGenuineTauPreselection(process, seq, mod, prefix=name+"GenuineTauPreselection"))
            add(name+"GenuineTauPreselection", seq, mod, counters)
            N += 1

            # Require genuine tau after tau ID in analysis
            mod = module.clone()
            module.onlyGenuineTaus = cms.untracked.bool(True)
            setattr(process, name+"GenuineTau", mod)
            path = cms.Path(process.commonSequence * mod)
            setattr(process, name+"GenuineTauPath", path)
            retNames.append(name+"GenuineTau")
            N += 1
        self._accumulateAnalyzers("Tau embedding -like preselection", N)
        return retNames

    def _additionalTauEmbeddingAnalyses(self, process, analysisModules, analysisNames):
        if self.options.tauEmbeddingInput == 0:
            return []

        retNames = []
        N = 0
        for module, name in zip(analysisModules, analysisNames):
            mod = module.clone()
            mod.trigger.caloMetSelection.metEmulationCut = 60.0
            path = cms.Path(process.commonSequence * mod)
            setattr(process, name+"CaloMet60", mod)
            setattr(process, name+"CaloMet60Path", path)
            N += 1

            mod = mod.clone()
            mod.triggerEfficiencyScaleFactor.mode = "efficiency"
            path = cms.Path(process.commonSequence * mod)
            setattr(process, name+"CaloMet60TEff", mod)
            setattr(process, name+"CaloMet60TEffPath", path)
            retNames.append(name+"CaloMet60TEff")
            N += 1
        self._accumulateAnalyzers("Tau embedding analyses", N)
        return retNames

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


    def _addJESVariation(self, process, name, doJetUnclusteredVariation):
        module = getattr(process, name)

        module = module.clone()
        module.Tree.fill = False        
        module.Tree.fillJetEnergyFractions = False # JES variation will make the fractions invalid

        jesVariation.addTESVariation(process, name, "TESPlus",  module, "Up")
        jesVariation.addTESVariation(process, name, "TESMinus", module, "Down")
        N = 2

        if doJetUnclusteredVariation:
            # Do all variations beyond TES
            jesVariation.addJESVariation(process, name, "JESPlus",  module, "Up")
            jesVariation.addJESVariation(process, name, "JESMinus", module, "Down")
            N += 2
    
            jesVariation.addJERVariation(process, name, "JERPlus",  module, "Up")
            jesVariation.addJERVariation(process, name, "JERMinus", module, "Down")
            N += 2
    
            jesVariation.addUESVariation(process, name, "METPlus",  module, "Up")
            jesVariation.addUESVariation(process, name, "METMinus", module, "Down")
            N += 2

        self._accumulateAnalyzers("JES variation", N)

    def _buildPUWeightVariation(self, process, analysisNamesForSystematics, param):
        if not (self.doPUWeightVariation or self.doSystematics):
            return

        if self.dataVersion.isMC():
            for name in analysisNamesForSystematics:
                self._addPUWeightVariation(process, name, param)
            print "Added PU weight variation for %d modules"%len(analysisNamesForSystematics)
        else:
            print "PU weight variation disabled for data (not meaningful for data)"

    def _addPUWeightVariation(self, process, name, param):
        # Up variation
        module = getattr(process, name).clone()
        module.Tree.fill = False
        module.eventCounter.printMainCounter = cms.untracked.bool(False)

        param.setPileupWeightForVariation(self.dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.vertexWeightReader, suffix="up")
        path = cms.Path(process.commonSequence * module)
        setattr(process, name+"PUWeightPlus", module)
        setattr(process, name+"PUWeightPlusPath", path)

        # Down variation
        module = getattr(process, name).clone()
        module.Tree.fill = False
        module.eventCounter.printMainCounter = cms.untracked.bool(False)

        param.setPileupWeightForVariation(self.dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.vertexWeightReader, suffix="down")
        path = cms.Path(process.commonSequence * module)
        setattr(process, name+"PUWeightMinus", module)
        setattr(process, name+"PUWeightMinusPath", path)

        self._accumulateAnalyzers("PU weight variation", 2)
