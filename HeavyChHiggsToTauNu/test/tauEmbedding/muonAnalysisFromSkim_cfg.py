import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "39Xredigi"
#dataVersion = "39Xdata"
#dataVersion = "311Xredigi"
dataVersion = "42Xmc"

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
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        #dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
    #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Spring11/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10/b3c16f1ee121445edb6d9b12e0772d8e/skim_104_1_sYD.root"
    "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11/50e9a4e9bac98baa56423a829b7f0fda/skim_113_1_B6e.root"
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
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, plainPatArgs=patArgs)
#process.commonSequence.remove(process.goodPrimaryVertices10)
if options.doPat == 0:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
    process.commonSequence *= (
        process.goodPrimaryVertices *
        process.goodPrimaryVertices10
    )

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
# Pileup weighting
weight = None
if dataVersion.isMC():
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param

    # Pileup weighting
    process.pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("pileupWeight"),
    )
    param.setPileupWeightFor2011()
    insertPSetContentsTo(param.vertexWeight.clone(), process.pileupWeight)

    # Vertex weighting
    process.vertexWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("vertexWeight"),
    )
    param.setVertexWeightFor2011()
    insertPSetContentsTo(param.vertexWeight.clone(), process.vertexWeight)

    process.commonSequence *= (process.pileupWeight*process.vertexWeight)
    
# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff as MuonSelection
additionalCounters.extend(MuonSelection.muonSelectionCounters)

# Add configuration information to histograms.root
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
muons = customisations.addMuonIsolationEmbedding(process, process.commonSequence, "selectedPatMuons")




import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonAnalysis as muonAnalysis

# Configuration
trigger = options.trigger
if len(trigger) == 0:
#    trigger = "HLT_Mu9"
    trigger = "HLT_Mu20_v1"

def createAnalysis(name, postfix="", weightSrc=None, **kwargs):
    wSrc = weightSrc
    if dataVersion.isData():
        wSrc = None
    def create(**kwargs):
        muonAnalysis.createAnalysis(process, dataVersion, additionalCounters, name=name,
                                    trigger=trigger, jets="goodJets", met="pfMet",
                                    weightSrc = wSrc,
                                    **kwargs)

    prefix = name+postfix
    create(prefix=prefix, **kwargs)
    if not "doIsolationWithTau" in kwargs:
        for iso in [
#            "VLoose",
#            "Loose",
#            "Medium",
#            "Tight",
#            "TightSc015",
#            "TightSc02",
            "TightIc04",
#            "TightSc015Ic04",
#            "TightSc02Ic04",
            ]:
            create(prefix=prefix+"IsoTauLike"+iso, doMuonIsolation=True, muonIsolation="tau%sIso"%iso, muonIsolationCut=0.5, **kwargs)

#         for iso in [
#             "Tight",
#             "TightSc0",
#             "TightSc0Ic04",
#             "TightSc0Ic04Noq",
#             create(prefix=prefix+"IsoTauLikeRel"+iso, doMuonIsolation=True, muonIsolation="tau%sIsoRel"%iso, muonIsolationCut=

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
#        (30, 20, 2),
#        (30, 20, 3),
#        (40, 20, 2),
        (40, 20, 3)
        ]:
        args["postfix"] = "Pt%dMet%dNJets%d%s" % (pt, met, njets, postfix)
        args["muonPtCut"] = pt
        args["metCut"] = met
        args["njets"] = njets
        createAnalysis("muonSelectionPF", **args)

createAnalysis2(muons=muons, allMuons=muons)
createAnalysis2(muons=muons, allMuons=muons, weightSrc="vertexWeight", postfix="VertexWeight")
#createAnalysis2(muons=muons, allMuons=muons, weightSrc="pileupWeight", postfix="PileupWeight")
#createAnalysis2(muons="tightMuonsZ")

# process.out = cms.OutputModule("PoolOutputModule",
#     fileName = cms.untracked.string('foo.root'),
#     outputCommands = cms.untracked.vstring(["keep *_*MuonVeto*_*_*"])
# )
# process.endPath = cms.EndPath(
#     process.out
# )

