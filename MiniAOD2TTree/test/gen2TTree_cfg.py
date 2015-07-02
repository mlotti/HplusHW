import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git

process = cms.Process("TTreeDump")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	'file:events_MG5_aMCatNLO_TTbar_H160_taunu_13TeV_GEN_6.root'
#	'file:PYTHIA8_Tauola_TTbar_H160_taunu_13TeV_cff_py_GEN.root'
#	'file:MG5_aMCatNLO_PYTHIA8_Tauola_TTbar_H160_taunu_13TeV_GEN.root'
#       'file:/afs/cern.ch/work/e/epekkari/GEN2015/events_MG5_aMCatNLO_TTbar_H200_taunu_13TeV_GEN_4.root'
#       'file:/afs/cern.ch/work/e/epekkari/GEN/PYTHIA8_Tauola_TB_H200_taunu_13TeV_cff_py_GEN.root'
#       'file:/afs/cern.ch/work/e/epekkari/GEN/events_MG5_aMCatNLO_TTbar_H160_taunu_13TeV_GEN_0.root'
    )
)

process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName = cms.string("miniaod2tree.root"),
    CodeVersion = cms.string(git.getCommitId()),
    DataVersion = cms.string('MC'),#remove?
    EventInfo = cms.PSet(),
    CMEnergy = cms.int32(13),
    GenParticles = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenParticles"),
            src = cms.InputTag("genParticles"),
            filter = cms.untracked.bool(False)
        )
    ),
    GenWeights = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenWeights"),
            src = cms.InputTag("generator"),
            filter = cms.untracked.bool(False)
        )
    ),
)

# module execution
process.runEDFilter = cms.Path(process.dump)

