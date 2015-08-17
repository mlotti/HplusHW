import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

process = cms.Process("TTreeDump")

dataVersion = "74Xmc"

options, dataVersion = getOptionsDataVersion(dataVersion)
print dataVersion

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	'file:ChargedHiggs_heavy_M200_v2.root'
#	'file:PYTHIA8_Tauola_TTbar_H160_taunu_13TeV_cff_py_GEN.root'
#	'file:MG5_aMCatNLO_PYTHIA8_Tauola_TTbar_H160_taunu_13TeV_GEN.root'
#       'file:/afs/cern.ch/work/e/epekkari/GEN2015/events_MG5_aMCatNLO_TTbar_H200_taunu_13TeV_GEN_4.root'
#       'file:/afs/cern.ch/work/e/epekkari/GEN/PYTHIA8_Tauola_TB_H200_taunu_13TeV_cff_py_GEN.root'
#       'file:/afs/cern.ch/work/e/epekkari/GEN/events_MG5_aMCatNLO_TTbar_H160_taunu_13TeV_GEN_0.root'
    )
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')
print "GlobalTag="+dataVersion.getGlobalTag()

process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName = cms.string("miniaod2tree.root"),
    CodeVersion = cms.string(git.getCommitId()),
    DataVersion = cms.string('74Xmc'),
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
    ),
)

# module execution
process.runEDFilter = cms.Path(process.dump)

