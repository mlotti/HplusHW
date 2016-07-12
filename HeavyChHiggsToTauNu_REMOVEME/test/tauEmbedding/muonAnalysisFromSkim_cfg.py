import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "39Xredigi"
#dataVersion = "39Xdata"
#dataVersion = "311Xredigi"
#dataVersion = "44XmcS6"
#dataVersion = "44Xdata"
dataVersion = "53XmcS10"
#dataVersion = "53Xdata22Jan2013"

#PF2PATVersion = "PFlow"

################################################################################

# Command line arguments (options) and DataVersion object
options = VarParsing.VarParsing()
options.register("WDecaySeparate",
                 0,
                 options.multiplicity.singleton,
                 options.varType.int,
                 "Separate W decays from MC information")
options, dataVersion = getOptionsDataVersion(dataVersion, options, useDefaultSignalTrigger=False)
if dataVersion.isMC() and len(options.trigger) == 0:
    options.trigger = ["HLT_Mu40_eta2p1_v1"]


#options.doPat=1

process = cms.Process("HChMuonAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        #dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
#        "file:skim.root"
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_5_3_X/TTJets_TuneZ2star_Summer12/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_tauembedding_skim_v53_3/9a24e6fe0421ec76a55ad5183bef176f/skim_172_1_F0R.root"
  )
)
if dataVersion.isData():
    process.source.fileNames = ["/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_5_3_X/SingleMu_200466-203742_2012C_Jan22/SingleMu/Run2012C_22Jan2013_v1_AOD_200466_203742_tauembedding_skim_v53_3/bf6e26bfda4583e5a02e30bcb8e788ff/skim_1000_1_yfC.root"]
    if len(options.trigger) == 0:
        options.trigger = ["HLT_Mu40_eta2p1_v11"]

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.options.wantSummary = cms.untracked.bool(True)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.MessageLogger.categories.append("TauIsolationSelector")

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects
patArgs = {"doPatTrigger": False,
#           "doPatTaus": False,
#           "doHChTauDiscriminators": False,
           "doPatElectronID": True,
           "doTauHLTMatching": False,
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs,
                                                            doHBHENoiseFilter=False,
                                                            )
# hack
if "allEvents" in additionalCounters and not hasattr(process, "allEvents"):
    del additionalCounters[additionalCounters.index("allEvents")]
if "passedTrigger" in additionalCounters and not hasattr(process, "allEvents"):
    del additionalCounters[additionalCounters.index("passedTrigger")]

# Add configuration information to histograms.root
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
process.infoPath = HChTools.addConfigInfo(process, options, dataVersion)

# PU weights
import HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration as AnalysisConfiguration
dataEras = [
    "Run2012ABCD",
    "Run2012AB",
    "Run2012C",
    "Run2012D",
]
#puWeights = AnalysisConfiguration.addPuWeightProducers(dataVersion, process, process.commonSequence, dataEras)
if dataVersion.isMC():
    process.puWeightSequence = cms.Sequence()
    puEraSuffixWeights = AnalysisConfiguration.addPuWeightProducersVariations(dataVersion, process, process.puWeightSequence, dataEras, doVariations=True)
    process.commonSequence.insert(0, process.puWeightSequence)

    # W+jets weights
    import HiggsAnalysis.HeavyChHiggsToTauNu.WJetsWeight as WJetsWeight
    wjetsEraSuffixWeights = []
    for era, suffix, weight in puEraSuffixWeights:
        weight = WJetsWeight.getWJetsWeight(dataVersion, options, "embedding_skim_v53_3", era, suffix, useInclusiveIfNotFound=True)
        name = "wjetsWeight"+era+suffix
        weight.enabled = False
        weight.alias = name
        setattr(process, name, weight)
        process.commonSequence += weight
        wjetsEraSuffixWeights.append( (era, suffix, name) )
        if options.wjetsWeighting != 0:
            weight.enabled = True

    # Top pt reweighting
    import HiggsAnalysis.HeavyChHiggsToTauNu.TopPtWeight_cfi as topPtWeight
    process.topPtWeight = topPtWeight.topPtWeight.clone()
    process.topPtWeightSeparate = process.topPtWeight.clone(scheme="TopPtSeparate")
    topPtWeights = [
        (process.topPtWeight.scheme.value(), "topPtWeight"),
        (process.topPtWeightSeparate.scheme.value(), "topPtWeightSeparate")
        ]
    if options.sample == "TTJets":
        topPtWeight.addTtGenEvent(process, process.commonSequence)
        process.topPtWeight.enabled = True
        process.topPtWeightSeparate.enabled = True
        process.configInfo.topPtReweightScheme = cms.untracked.string(process.topPtWeight.scheme.value())
    process.commonSequence += (process.topPtWeight+process.topPtWeightSeparate)

    # variations
    for label, name in topPtWeights[:]:
        mod = getattr(process, name).clone(
            variationEnabled=True,
            variationDirection=+1
        )
        setattr(process, name+"Plus", mod)
        process.commonSequence += mod
        topPtWeights.append( (mod.scheme.value()+"Plus", name+"Plus") )

        mod = mod.clone(
            variationDirection=-1
        )
        setattr(process, name+"Minus", mod)
        process.commonSequence += mod
        topPtWeights.append( (mod.scheme.value()+"Minus", name+"Minus") )


# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as MuonSelection
tmp = additionalCounters[:]
additionalCounters = []
additionalCounters.extend(MuonSelection.getMuonPreSelectionCountersForEmbedding())
additionalCounters.extend(MuonSelection.getMuonSelectionCountersForEmbedding(dataVersion))
additionalCounters.extend(tmp)

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
#customisations.PF2PATVersion = PF2PATVersion

muons = "selectedPatMuons"
#muons = "selectedPatMuons"+PF2PATVersion+"All"
#muons = "selectedPatMuons"+PF2PATVersion
#muons = "tightMuons"+PF2PATVersion
#muons = customisations.addMuonIsolationEmbedding(process, process.commonSequence, muons)
isolation = customisations.constructMuonIsolationOnTheFly(muons)
muons = muons+"Iso"
setattr(process, muons, isolation)
process.commonSequence *= isolation

# Electron Veto
import HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalElectronVetoFilter_cfi as ElectronVeto
process.eveto = ElectronVeto.hPlusGlobalElectronVetoFilter.clone(
    filter = False
)
process.commonSequence *= process.eveto

# Muon preselection (without isolation)
# start from 'selectedPatMuons' to double-check the selections in embedding job
# store muons before pt>41 and trigger matching to allow muon veto in the ntuple-analysis
process.preselectedMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag(muons),
    cut = cms.string(
        "isGlobalMuon() && isTrackerMuon()"
        # Take out chi2<10 cut for testing TuneP cocktail
#        "&& muonID('GlobalMuonPromptTight')"
        "&& globalTrack().hitPattern().numberOfValidMuonHits() > 0"
        "&& numberOfMatchedStations() > 1"
        "&& abs(dB()) < 0.2" 
        "&& innerTrack().hitPattern().numberOfValidPixelHits() > 0"
        "&& track().hitPattern().trackerLayersWithMeasurement() > 8"
    )
)
muons = "preselectedMuons" # this is common to embedding muon selection and muon veto
process.preselectedMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("preselectedMuons"),
    minNumber = cms.uint32(1)
)
process.preselectedMuonsCount = cms.EDProducer("EventCountProducer")
process.commonSequence += (
    process.preselectedMuons +
    process.preselectedMuonsFilter +
    process.preselectedMuonsCount
)
additionalCounters.append("preselectedMuonsCount")
# Trigger matching
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching as HChTriggerMatching
process.preselectedMuonsMatched = HChTriggerMatching.createMuonTriggerMatchingInAnalysis(options.trigger, "preselectedMuons")
process.preselectedMuonsMatchedFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("preselectedMuonsMatched"),
    minNumber = cms.uint32(1)
)
process.preselectedMuonsMatchedCount = cms.EDProducer("EventCountProducer")
process.commonSequence += (
    process.preselectedMuonsMatched +
    process.preselectedMuonsMatchedFilter +
    process.preselectedMuonsMatchedCount
)
additionalCounters.append("preselectedMuonsMatchedCount")
# Kinematic cuts
process.preselectedMuons41 = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("preselectedMuonsMatched"),
    cut = cms.string("pt() > 41 && abs(eta) < 2.1")
)
process.preselectedMuons41Filter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("preselectedMuons41"),
    minNumber = cms.uint32(1)
)
process.preselectedMuons41Count = cms.EDProducer("EventCountProducer")
process.commonSequence *= (
    process.preselectedMuons41 *
    process.preselectedMuons41Filter *
    process.preselectedMuons41Count
)
additionalCounters.append("preselectedMuons41Count")
# MuScleFit correction
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/MuScleFitCorrections2012
muscle = cms.EDProducer("MuScleFitPATMuonCorrector", 
    src = cms.InputTag(muons), 
    debug = cms.bool(False), 
    identifier = cms.string("Data2012_53X_ReReco"),
    applySmearing = cms.bool(False),
    fakeSmearing = cms.bool(False)
)
setattr(process, muons+"Muscle", muscle)
process.commonSequence += muscle
if dataVersion.isMC():
    muscle.identifier = "Summer12_DR53X_smearReReco"
    muscle.applySmearing = True



# Jet selection
# Cannot do filtering because of jet systematic variations
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.setJERSmearedJets(dataVersion)
import HiggsAnalysis.HeavyChHiggsToTauNu.HChJetFilter_cfi as jetFilter_cfi
process.selectedJets = jetFilter_cfi.hPlusJetPtrSelectorFilter.clone(
    tauSrc = "",
    removeTau = False,
    histogramAmbientLevel = "Systematics",
    producePt20 = True,
    filter=False,
)
#process.selectedJetsCount = cms.EDProducer("EventCountProducer")
process.commonSequence += (
    process.selectedJets #+
#    process.selectedJetsCount
)
#additionalCounters.append("selectedJetsCount")

# Calculate b-tagging quantities
import HiggsAnalysis.HeavyChHiggsToTauNu.HChBTaggingFilter_cfi as btagFilter_cfi
process.btagging = btagFilter_cfi.hPlusBTaggingPtrSelectorFilter.clone(
#    jetSrc = cms.InputTag("selectedJets", "selectedJetsPt20"),
    jetSrc = process.selectedJets.jetSelection.src.value(),
    histogramAmbientLevel = "Systematics",
    filter = False,
)
process.btagging.btagging.ptCut = 0
process.btagging.btagging.etaCut = 9999
process.commonSequence += process.btagging
#process.debug = cms.EDAnalyzer("EventContentAnalyzer")
#process.commonSequence += process.debug

# MET filters
# disabled for now due to a bug in v44_5_1 skim
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMETFilter_cfi as METFilter_cfi
process.metNoiseFilters = METFilter_cfi.hPlusMETNoiseFilters.clone(
    filter = False,
)
process.metNoiseFilters.metFilters.triggerResultsSrc.setProcessName("MUONSKIM")
#process.metNoiseFilters.metFilters.beamHaloEnabled = False
#process.metNoiseFilters.metFilters.trackingFailureFilterEnabled = False
#process.metNoiseFilters.metFilters.EcalDeadCellEventFilterEnabled = False
#process.metNoiseFilters.metFilters.EcalDeadCellTPFilterEnabled = False
process.commonSequence += process.metNoiseFilters


# process.preselectedJets = cms.EDFilter("PATJetSelector",
# #    src = cms.InputTag("goodJets"+PF2PATVersion),
# #    src = cms.InputTag("goodJets"),
#     src = cms.InputTag("selectedPatJets"),
#     cut = cms.string(customisations.jetSelection)
# )
# process.preselectedJetsFilter = cms.EDFilter("CandViewCountFilter",
#     src = cms.InputTag("preselectedJets"),
#     minNumber = cms.uint32(3)
# )
# process.preselectedJetsCount = cms.EDProducer("EventCountProducer")
# process.commonSequence *= (
#     process.preselectedJets *
# #    process.preselectedJetsFilter * 
#     process.preselectedJetsCount
# )
# additionalCounters.append("preselectedJetsCount")

# Configuration
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.analysisConfig as analysisConfig
import HiggsAnalysis.HeavyChHiggsToTauNu.Ntuple as Ntuple
ntuple = cms.EDAnalyzer("HPlusMuonNtupleAnalyzer",
    patTriggerEvent = cms.InputTag("patTriggerEvent"),

    genParticleSrc = cms.InputTag("genParticles"),
    genTTBarEnabled = cms.bool(False),

    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),

    muons = Ntuple.muons.clone(
        src = muons,
        correctedEnabled = cms.bool(True),
        correctedSrc = muons+"Muscle",
        tunePEnabled = True,
        functions = analysisConfig.muonFunctions.clone(),
        bools = cms.PSet(
            triggerMatched = cms.InputTag(muons+"Matched")
        ),
    ),
    muonEfficiencies = cms.PSet(
        id_Run2012ABCD = param.embeddingMuonIdEfficiency.clone(),
        trigger = param.embeddingMuonTriggerEfficiency.clone(),
    ),

#    electronSrc = cms.InputTag("selectedPatElectrons"),
#    electronConversionSrc = cms.InputTag("allConversions"),
#    beamspotSrc = cms.InputTag("offlineBeamSpot"),
#    electronRhoSrc =  cms.InputTag("kt6PFJetsForEleIso", "rho"),
#    electronFunctions = analysisConfig.electronFunctions.clone(),

    jets = cms.PSet(
        jets = Ntuple.jets.clone(
            src = cms.InputTag("selectedJets", "selectedJetsPt20"),
            floats = cms.PSet(
                btagScaleFactor = cms.InputTag("btagging", "scaleFactor"),
                btagScaleFactorUncertainty = cms.InputTag("btagging", "scaleFactorUncertainty"),
            ),
            bools = cms.PSet(
                btagged = cms.InputTag("btagging", "tagged"),
            ),
        ),
    ),

    mets = analysisConfig.mets.clone(
        pfMetRaw_p4 = cms.InputTag("patPFMet"),
        pfMetType1_p4 = cms.InputTag("patType1CorrectedPFMet"), # this is automatically from smeared jets for MC
#        pfMetType1p2_p4 = cms.InputTag("patType1p2CorrectedPFMet"), # this is automatically from smeared jets for MC
    ),
    doubles = cms.PSet(),
    bools = cms.PSet(
        METNoiseFiltersPassed = cms.InputTag("metNoiseFilters"),
        ElectronVetoPassed = cms.InputTag("eveto"),
    ),

    eventCounter = param.eventCounter.clone(),
    histogramAmbientLevel = cms.untracked.string("Informative"),
)
del ntuple.mets.pfMet_p4
if dataVersion.isMC():
    for era, suffix, weight in puEraSuffixWeights:
        setattr(ntuple.doubles, "weightPileup_"+era+suffix, cms.InputTag(weight))
    for era, suffix, weight in wjetsEraSuffixWeights:
        setattr(ntuple.doubles, "weightWJets_"+era+suffix, cms.InputTag(weight))
    for label, tag in topPtWeights:
        setattr(ntuple.doubles, "weightTopPt_"+label, cms.InputTag(tag))

    for name in ntuple.muonEfficiencies.parameterNames_():
        pset = getattr(ntuple.muonEfficiencies, name)
        pset.mode = "scaleFactor"

    def addMetVariation(name, metSrc):
        for d in ["Up", "Down"]:
            midfix = name%d
            setattr(ntuple.mets, "pfMetType1%s_p4" % midfix, cms.InputTag(metSrc%d))

    def addJetVariation(name, src, metName, metSrc):
        addMetVariation(metName, metSrc)
        for d in ["Up", "Down"]:
            postfix = src%d
            selectedJets = process.selectedJets.clone()
            selectedJets.jetSelection.src = postfix
            param.setJetPUIdSrc(selectedJets.jetSelection, "selectedJets"+postfix)
            setattr(process, "selectedJets"+postfix, selectedJets)
            process.commonSequence += selectedJets

            btagging = process.btagging.clone()
            btagging.jetSrc = selectedJets.jetSelection.src.value()
            setattr(process, "btagging"+postfix, btagging)
            process.commonSequence += btagging

            jets = ntuple.jets.jets.clone()
            jets.detailsEnabled = False
            jets.functions = cms.PSet()
            jets.src.setModuleLabel("selectedJets"+postfix)
            jets.floats.btagScaleFactor.setModuleLabel("btagging"+postfix)
            del jets.floats.btagScaleFactorUncertainty
            jets.bools.btagged.setModuleLabel("btagging"+postfix)

            setattr(ntuple.jets, name%d, jets)

#    addJetVariation("jetsEn%s", "shiftedPatJetsEn%sForCorrMEt", "JetEn%s", "patType1CorrectedPFMetJetEn%s")
#    addJetVariation("jetsRes%s", "smearedPatJetsRes%s", "JetRes%s", "patType1CorrectedPFMetJetRes%s")
#    addMetVariation("UnclusteredEn%s", "patType1CorrectedPFMetUnclusteredEn%s")

HChTools.addAnalysis(process, "muonNtuple", ntuple,
                     preSequence=process.commonSequence,
                     additionalCounters=additionalCounters)
process.muonNtuple.eventCounter.printMainCounter = True

# Replace all event counters with the weighted one
if dataVersion.isMC():
    eventCounters = []
    for label, module in process.producers_().iteritems():
        if module.type_() == "EventCountProducer":
            eventCounters.append(label)
    prototype = cms.EDProducer("HPlusEventCountProducer",
        weightSrc = cms.InputTag(puEraSuffixWeights[0][2])
    )
    for label in eventCounters:
        process.globalReplace(label, prototype.clone())
    

f = open("configDumpMuonAnalysis.py", "w")
f.write(process.dumpPython())
f.close()
