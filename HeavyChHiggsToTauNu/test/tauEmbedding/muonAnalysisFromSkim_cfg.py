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

process = cms.Process("HChMuonAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

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
        #dataVersion.getPatDefaultFileMadhatter(dcap=True)
        #"file:skim_1000.root"
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/WJets_TuneZ2_Spring11/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9/00c200b343cbc3d5ec3f111d1d98acde/skim_127_2_AUw.root"
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
           "doHChTauDiscriminators": False,
           "doPatElectronID": False,
           "doTauHLTMatching": False,
           "doPatMuonPFIsolation": True,
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonAnalysis as muonAnalysis

# Configuration
trigger = options.trigger
if len(trigger) == 0:
#    trigger = "HLT_Mu9"
    trigger = "HLT_Mu15_v1"

def createAnalysis(name, postfix="", **kwargs):
    def create(**kwargs):
        muonAnalysis.createAnalysis(process, dataVersion, additionalCounters, name=name, trigger=trigger, **kwargs)

    prefix = name+postfix
    create(prefix=prefix)
    if not "doIsolationWithTau" in kwargs:
        create(prefix=prefix+"IsoTau", doIsolationWithTau=True, **kwargs)

    create(prefix=prefix+"Aoc", afterOtherCuts=True, **kwargs)

def createAnalysis2(**kwargs):
    #createAnalysis("topMuJetRefMet", doIsolationWithTau=False, **kwargs)

    postfix = kwargs.get("postfix", "")
    for pt, met, njets in [
        (30, 20, 2),
        (30, 20, 3),
        (40, 20, 3)
        ]:
        kwargs["postfix"] = "Pt%dMet%dNJets%d%s" % (pt, met, njets, postfix)
        kwargs["muonPtCut"] = pt
        kwargs["metCut"] = met
        kwargs["njets"] = njets
        createAnalysis("muonSelectionPF", **kwargs)

createAnalysis2()

# process.out = cms.OutputModule("PoolOutputModule",
#     fileName = cms.untracked.string('foo.root'),
#     outputCommands = cms.untracked.vstring(["keep *_*MuonVeto*_*_*"])
# )
# process.endPath = cms.EndPath(
#     process.out
# )

