import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "39Xredigi"
#dataVersion = "39Xdata"
dataVersion = "311Xredigi"

################################################################################

# Command line arguments (options) and DataVersion object
options = VarParsing.VarParsing()
options.register("WDecaySeparate",
                 0,
                 options.multiplicity.singleton,
                 options.varType.int,
                 "Separate W decays from MC information")
options, dataVersion = getOptionsDataVersion(dataVersion, options)

#options.doPat=1

process = cms.Process("HChMuonAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
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
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Spring11/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9/00c200b343cbc3d5ec3f111d1d98acde/skim_107_1_CZl.root"
  )
)

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
           "doPatMuonPFIsolation": True,
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs)
process.commonSequence.remove(process.goodPrimaryVertices10)

# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff as MuonSelection
additionalCounters.extend(MuonSelection.muonSelectionCounters)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
import RecoTauTag.Configuration.RecoPFTauTag_cff as RecoPFTauTag
process.patMuonsWithTight = cms.EDProducer("HPlusPATMuonViewTauLikeIsolationEmbedder",
    candSrc = cms.InputTag("selectedPatMuons"),
    pfCandSrc = cms.InputTag("particleFlow"),
    vertexSrc = cms.InputTag("firstPrimaryVertex"),
    embedPrefix = cms.string("byTight"),
    signalCone = cms.double(0.1),
    isolationCone = cms.double(0.5)
)
process.patMuonsWithMedium = process.patMuonsWithTight.clone(
    candSrc = "patMuonsWithTight",
    embedPrefix = "byMedium",
)
process.patMuonsWithLoose = process.patMuonsWithTight.clone(
    candSrc = "patMuonsWithMedium",
    embedPrefix = "byLoose",
)
process.patMuonsWithVLoose = process.patMuonsWithTight.clone(
    candSrc = "patMuonsWithLoose",
    embedPrefix = "byVLoose",
)

HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByTightIsolation.qualityCuts.isolationQualityCuts, process.patMuonsWithTight)
HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByMediumIsolation.qualityCuts.isolationQualityCuts, process.patMuonsWithMedium)
HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByLooseIsolation.qualityCuts.isolationQualityCuts, process.patMuonsWithLoose)
HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByVLooseIsolation.qualityCuts.isolationQualityCuts, process.patMuonsWithVLoose)

process.patMuonsWithTightNoSignalCone = process.patMuonsWithTight.clone(
    candSrc = "patMuonsWithVLoose",
    embedPrefix = "byTightNoSignalCone",
    signalCone = 0.0
)

import PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi as muonSelector
process.selectedPatMuonsWithIso = muonSelector.selectedPatMuons.clone(
    src = "patMuonsWithVLoose"
)

process.commonSequence *= (
    process.patMuonsWithTight *
    process.patMuonsWithMedium *
    process.patMuonsWithLoose *
    process.patMuonsWithVLoose *
    process.selectedPatMuonsWithIso
)

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonAnalysis as muonAnalysis

# Configuration
trigger = options.trigger
if len(trigger) == 0:
#    trigger = "HLT_Mu9"
    trigger = "HLT_Mu15_v1"

def createAnalysis(name, postfix="", **kwargs):
    def create(**kwargs):
        muonAnalysis.createAnalysis(process, dataVersion, additionalCounters, name=name,
                                    trigger=trigger, jets="goodJets", met="pfMet",
                                    **kwargs)

    prefix = name+postfix
    create(prefix=prefix, **kwargs)
    if not "doIsolationWithTau" in kwargs:
        for iso in [
            "VLoose",
            "Loose",
            "Medium",
            "Tight",
            ]:
            create(prefix=prefix+"IsoTauLike"+iso, doMuonIsolation=True, muonIsolation="tau%sIso"%iso, muonIsolationCut=1.0, **kwargs)

#    if not "doIsolationWithTau" in kwargs:
#        for iso in [
#            "VLoose",
#            "Loose",
#            "Medium",
#            "Tight",
#            ]:
#            create(prefix=prefix+"IsoTau"+iso, doIsolationWithTau=True, isolationWithTauDiscriminator="by%sIsolation"%iso, **kwargs)
        
    create(prefix=prefix+"Aoc", afterOtherCuts=True, **kwargs)

def createAnalysis2(**kwargs):
#    createAnalysis("topMuJetRefMet", doIsolationWithTau=False, **kwargs)

    args = {}
    args.update(kwargs)
    postfix = kwargs.get("postfix", "")
    for pt, met, njets in [
        (30, 20, 2),
        (30, 20, 3),
#        (40, 20, 2),
        (40, 20, 3)
        ]:
        args["postfix"] = "Pt%dMet%dNJets%d%s" % (pt, met, njets, postfix)
        args["muonPtCut"] = pt
        args["metCut"] = met
        args["njets"] = njets
        createAnalysis("muonSelectionPF", **args)

createAnalysis2(muons="selectedPatMuonsWithIso", allMuons="selectedPatMuonsWithIso")
#createAnalysis2(muons="tightMuonsZ")

# process.out = cms.OutputModule("PoolOutputModule",
#     fileName = cms.untracked.string('foo.root'),
#     outputCommands = cms.untracked.vstring(["keep *_*MuonVeto*_*_*"])
# )
# process.endPath = cms.EndPath(
#     process.out
# )

