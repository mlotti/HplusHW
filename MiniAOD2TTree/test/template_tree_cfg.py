import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git

process = cms.Process("TTreeDump")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        "file:/mnt/flustre/epekkari/2HDMIINLO100K/light/PROCNLO_2HDMtypeII_0/Events/run_01_decayed_1/events.root"
    )
)

process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName = cms.string("miniaod2tree.root"),
    CodeVersion = cms.string(git.getCommitId()),
    DataVersion = cms.string('MC'),
    EventInfo = cms.PSet(),
    CMEnergy = cms.int32(13),
    GenParticles = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenParticles"),
            src = cms.InputTag("genParticles"),
            filter = cms.untracked.bool(False)
        )
    ),
    GenMETs = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenMET"),
            src = cms.InputTag("genMetTrue"),
            filter = cms.untracked.bool(False)
        )
    ),
    GenWeights = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenWeight"),
            src = cms.InputTag("generator"),
            filter = cms.untracked.bool(False)
        )
    )
)

# module execution
process.runEDFilter = cms.Path(process.dump)

