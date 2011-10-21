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
options, dataVersion = getOptionsDataVersion(dataVersion, options, useDefaultSignalTrigger=False)

process = cms.Process("HChMuonAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        #dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        dataVersion.getAnalysisDefaultFileMadhatter()
  )
)
if options.doPat != 0:
    process.source.fileNames = cms.untracked.vstring(
        #dataVersion.getPatDefaultFileCastor()
        dataVersion.getPatDefaultFileMadhatter()
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
if dataVersion.isMC():
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param

    # Pileup weighting
    process.pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("pileupWeight"),
    )
    param.setPileupWeightFor2011()
    insertPSetContentsTo(param.vertexWeight, process.pileupWeight)

    # Vertex weighting
    process.vertexWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("vertexWeight"),
    )
    param.setVertexWeightFor2011()
    insertPSetContentsTo(param.vertexWeight, process.vertexWeight)

    process.commonSequence *= (process.pileupWeight*process.vertexWeight)

# Add configuration information to histograms.root
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

process.firstPrimaryVertex = cms.EDProducer("HPlusFirstVertexSelector",
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
    trigger = "HLT_Mu15_v1"

def createAnalysis(name, postfix="", weightSrc=None, **kwargs):
    wSrc = weightSrc
    if dataVersion.isData():
        wSrc = None
    def create(**kwargs):
        muonAnalysis.createAnalysis(process, dataVersion, additionalCounters, name=name,
                                    trigger=trigger, weightSrc=wSrc, **kwargs)

    prefix = name+postfix
    create(prefix=prefix, **kwargs)
    create(prefix=prefix+"IsoTauLikeTightIc04", doMuonIsolation=True, muonIsolation="tauTightIc04Iso", muonIsolationCut=1.0, **kwargs)

def createAnalysis2(**kwargs):
#    createAnalysis("topMuJetRefMet", doIsolationWithTau=False, **kwargs)
    postfix = ""
    if "postfix" in kwargs:
        postfix = kwargs["postfix"]
        del kwargs["postfix"]

    #for pt, met, njets in [(30, 20, 1), (30, 20, 2),
    #                       (30, 20, 3), (30, 30, 3), (30, 40, 3),
    #                       (40, 20, 3), (40, 30, 3), (40, 40, 3)]:
    for pt, met, njets in [(40, 20, 3)]:
        kwargs["postfix"] = "Pt%dMet%dNJets%d%s" % (pt, met, njets, postfix)
        kwargs["muonPtCut"] = pt
        kwargs["metCut"] = met
        kwargs["njets"] = njets
        createAnalysis("muonSelectionPF", **kwargs)


createAnalysis2()
createAnalysis2(weightSrc="vertexWeight", postfix="VertexWeight")
createAnalysis2(weightSrc="pileupWeight", postfix="PileupWeight")


if options.WDecaySeparate > 0:
    process.mcEventTopology = cms.EDFilter("HPlusGenEventTopologyFilter",
        src = cms.InputTag("genParticles"),
        particle = cms.string("abs(pdgId()) == 24"),
        daughter = cms.string("abs(pdgId()) == 13"),
        minParticles = cms.uint32(1),
        minDaughters = cms.uint32(1)
    )
    process.wMuNuSequence = cms.Sequence(
        process.mcEventTopology
    )
    process.wOtherSequence = cms.Sequence(
        ~process.mcEventTopology
    )

    createAnalysis2(postfix="Wmunu", beginSequence=process.wMuNuSequence)
    createAnalysis2(postfix="WOther", beginSequence=process.wOtherSequence)


#print process.dumpPython()

