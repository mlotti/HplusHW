import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "39Xredigi"
#dataVersion = "39Xdata"
#dataVersion = "311Xredigi"
dataVersion = "44XmcS6"
#dataVersion = "44Xdata"

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
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_skim_v44_1_TTJets_TuneZ2_Fall11//2f6341f5a210122b891e378fe7516bcf/skim_1001_1_qUS.root"
  )
)
if dataVersion.isData():
    process.source.fileNames = ["/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Tauembedding_skim_v44_1_SingleMu_Mu_173693-177452_2011B_Nov19//079054b3ab4c4121ae105c34f9c44ff5/skim_100_1_Khr.root"]

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
#process.commonSequence.remove(process.goodPrimaryVertices10)
# if options.doPat == 0:
#     process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
#     process.commonSequence *= (
#         process.goodPrimaryVertices *
#         process.goodPrimaryVertices10
#     )

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
# Pileup weights
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
#param.changeCollectionsToPF2PAT(PF2PATVersion)
puWeights = [
    ("Run2011A", "Run2011A"),
    ("Run2011B", "Run2011B"),
    ("Run2011AB", "Run2011AB")
    ]
for era, name in puWeights:
    modname = "pileupWeight"+name
    setattr(process, modname, cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string(modname),
    ))
    param.setPileupWeight(dataVersion, process=process, commonSequence=process.commonSequence, era=era)
    insertPSetContentsTo(param.vertexWeight.clone(), getattr(process, modname))
    process.commonSequence.insert(0, getattr(process, modname))
# FIXME: this is only a consequence of the swiss-knive effect...
process.commonSequence.remove(process.goodPrimaryVertices)
process.commonSequence.insert(0, process.goodPrimaryVertices)
# FIXME: and this one because HBHENoiseFilter is not stored in embedding skims of v44_1
#if dataVersion.isData():
#    process.HBHENoiseSequence = cms.Sequence()
#    process.commonSequence.replace(process.HBHENoiseFilter, process.HBHENoiseSequence*process.HBHENoiseFilter)
#    import HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection as DataSelection
#    DataSelection.addHBHENoiseFilterResultProducer(process, process.HBHENoiseSequence)
    
# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as MuonSelection
additionalCounters.extend(MuonSelection.getMuonSelectionCountersForEmbedding(dataVersion))

# Add configuration information to histograms.root
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

#process.firstPrimaryVertex = cms.EDProducer("HPlusFirstVertexSelector",
#    src = cms.InputTag("offlinePrimaryVertices")
#)
#process.commonSequence *= process.firstPrimaryVertex


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

import HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalElectronVetoFilter_cfi as ElectronVeto
process.eveto = ElectronVeto.hPlusGlobalElectronVetoFilter.clone(
    filter = False
)
process.commonSequence *= process.eveto

process.preselectedMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag(muons),
    cut = cms.string(
        "isGlobalMuon() && isTrackerMuon()"
        "&& muonID('GlobalMuonPromptTight')"
        "&& innerTrack().numberOfValidHits() > 10"
        "&& innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
        "&& numberOfMatches() > 1"
    )
)
process.preselectedMuons40 = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("preselectedMuons"),
    cut = cms.string("pt() > 40 && abs(eta) < 2.1")
)
process.preselectedMuons40Filter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("preselectedMuons40"),
    minNumber = cms.uint32(1)
)
process.preselectedMuons40Count = cms.EDProducer("EventCountProducer")
process.commonSequence *= (
    process.preselectedMuons *
    process.preselectedMuons40 *
    process.preselectedMuons40Filter *
    process.preselectedMuons40Count
)
additionalCounters.append("preselectedMuons40Count")

process.preselectedJets = cms.EDFilter("PATJetSelector",
#    src = cms.InputTag("goodJets"+PF2PATVersion),
#    src = cms.InputTag("goodJets"),
    src = cms.InputTag("selectedPatJets"),
    cut = cms.string(customisations.jetSelection)
)
process.preselectedJetsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("preselectedJets"),
    minNumber = cms.uint32(3)
)
process.preselectedJetsCount = cms.EDProducer("EventCountProducer")
process.commonSequence *= (
    process.preselectedJets *
#    process.preselectedJetsFilter * 
    process.preselectedJetsCount
)
additionalCounters.append("preselectedJetsCount")

# Configuration
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.analysisConfig as analysisConfig
import HiggsAnalysis.HeavyChHiggsToTauNu.Ntuple as Ntuple
ntuple = cms.EDAnalyzer("HPlusMuonNtupleAnalyzer",
    patTriggerEvent = cms.InputTag("patTriggerEvent"),
    genParticleSrc = cms.InputTag("genParticles"),
    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),

    muons = Ntuple.muons.clone(
        src = "preselectedMuons",
        functions = analysisConfig.muonFunctions.clone()
    )

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

    mets = analysisConfig.mets.clone(),
    doubles = cms.PSet(),
    bools = cms.PSet(
        ElectronVetoPassed = cms.InputTag("eveto")
    ),
)
for era, name in puWeights:
    setattr(ntuple.doubles, "weightPileup_"+name, cms.InputTag("pileupWeight"+name))
if dataVersion.isData():
    ntuple.bools.HBHENoiseFilter = cms.InputTag("HBHENoiseFilterResultProducer", "HBHENoiseFilterResult")
    ntuple.bools.HBHENoiseFilterMETWG = cms.InputTag("HBHENoiseFilterResultProducerMETWG", "HBHENoiseFilterResult")


addAnalysis(process, "muonNtuple", ntuple,
            preSequence=process.commonSequence,
            additionalCounters=additionalCounters,
            signalAnalysisCounters=False)
process.muonNtupleCounters.printMainCounter = True

# Replace all event counters with the weighted one
eventCounters = []
for label, module in process.producers_().iteritems():
    if module.type_() == "EventCountProducer":
        eventCounters.append(label)
prototype = cms.EDProducer("HPlusEventCountProducer",
    weightSrc = cms.InputTag("pileupWeight"+puWeights[-1][1])
)
for label in eventCounters:
    process.globalReplace(label, prototype.clone())


#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
