import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git

process = cms.Process("TTreeDump")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#	'file:PYTHIA6_Tauola_TTbar_H160_taunu_13TeV_cff_py_GEN.root'
#	'file:PYTHIA8_Tauola_TTbar_H160_taunu_13TeV_cff_py_GEN.root'
	'file:MG5_aMCatNLO_PYTHIA8_Tauola_TTbar_H160_taunu_13TeV_GEN.root'
    )
)

process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName = cms.string("miniaod2tree.root"),
    CodeVersion = cms.string(git.getCommitId()),
    EventInfo = cms.PSet(),
    GenParticles = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenParticles"),
            src = cms.InputTag("genParticles"),
            filter = cms.untracked.bool(False)
        )
    )
)

# module execution
process.runEDFilter = cms.Path(process.dump)

