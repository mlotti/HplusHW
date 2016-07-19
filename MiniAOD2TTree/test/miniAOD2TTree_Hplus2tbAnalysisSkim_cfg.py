# For miniAOD instructions see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015 

import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
from HiggsAnalysis.MiniAOD2TTree.tools.HChOptions import getOptionsDataVersion


#================================================================================================  
# Options
#================================================================================================  
maxEvents    = 100
maxWarnings  = 100
reportEvery  = 100
dataVersion  = "80Xdata"
datasetFiles = ['/store/data/Run2016B/JetHT/MINIAOD/PromptReco-v2/000/273/150/00000/66051AAF-D819-E611-BD3D-02163E011D55.root']
#dataVersion  = "80Xmc" 
#datasetFiles = ['/store/mc/RunIISpring16MiniAODv2/ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/20000/04F56101-3739-E611-90EE-0CC47A78A41C.root']

process = cms.Process("TTreeDump")

dataVersion = "76Xmc"
#dataVersion = "76Xdata"

options, dataVersion = getOptionsDataVersion(dataVersion)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.categories.append("TriggerBitCounter")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000 # print the event number for every 100th event
process.MessageLogger.cerr.TriggerBitCounter = cms.untracked.PSet(limit = cms.untracked.int32(10)) # print max 100 warnings

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       '/store/mc/RunIIFall15MiniAODv1/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/20000/007E40C9-B4A4-E511-BD19-842B2B7680DF.root'
    )
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, cms.string(dataVersion.getGlobalTag()), '')
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')
print "GlobalTag="+dataVersion.getGlobalTag()

# ===== Set up tree dumper =====
process.load("HiggsAnalysis/MiniAOD2TTree/PUInfo_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/TopPt_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Tau_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Electron_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Muon_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Jet_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Top_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/MET_cfi")

process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName = cms.string("miniaod2tree.root"),
    PUInfoInputFileName = process.PUInfo.OutputFileName,
    TopPtInputFileName = process.TopPtProducer.OutputFileName,
    CodeVersion = cms.string(git.getCommitId()),
    DataVersion = cms.string(str(dataVersion.version)),
    CMEnergy = cms.int32(13),
    Skim = cms.PSet(
	Counters = cms.VInputTag(
	    "skimCounterAll",
            "skimCounterPassed"
        ),
    ),
    EventInfo = cms.PSet(
        PileupSummaryInfoSrc = process.PUInfo.PileupSummaryInfoSrc, 
	LHESrc = cms.untracked.InputTag("externalLHEProducer"),
	OfflinePrimaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
	TopPtProducer = cms.InputTag("TopPtProducer"),
    ),
    Trigger = cms.PSet(
	TriggerResults = cms.InputTag("TriggerResults::HLT"),
	TriggerBits = cms.vstring(
            "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_v",
            "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET80_JetIdCleaned_v",
            "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v",
            "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_JetIdCleaned_v",
        ),
	L1Extra = cms.InputTag("l1extraParticles:MET"),
	TriggerObjects = cms.InputTag("selectedPatTrigger"),
        TriggerMatch = cms.untracked.vstring(
            "LooseIsoPFTau50_Trk30_eta2p1",
        ),
	filter = cms.untracked.bool(False)
    ),
    METNoiseFilter = cms.PSet(
        triggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getMETFilteringProcess())),
        printTriggerResultsList = cms.untracked.bool(False),
        filtersFromTriggerResults = cms.vstring(
            "Flag_HBHENoiseFilter",
            "Flag_HBHENoiseIsoFilter",
            "Flag_CSCTightHaloFilter",
#            "Flag_CSCTightHalo2015Filter",
            "Flag_EcalDeadCellTriggerPrimitiveFilter",
            "Flag_goodVertices",
            "Flag_eeBadScFilter",
        ),
        hbheNoiseTokenRun2LooseSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Loose'),
        hbheNoiseTokenRun2TightSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Tight'),
        hbheIsoNoiseTokenSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHEIsoNoiseFilterResult'),
    ),
    Taus      = process.Taus,
    Electrons = process.Electrons,
    Muons     = process.Muons,
    Jets      = process.Jets,
    Top       = process.Top,
    METs      = process.METs,
    GenWeights = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenWeights"),
            src = cms.InputTag("generator"),
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
    GenJets = cms.VPSet(      
        cms.PSet(
            branchname = cms.untracked.string("GenJets"),
            src = cms.InputTag("slimmedGenJets"), # ak4
        )
    ),
    GenParticles = cms.VPSet(      
        cms.PSet(
            branchname = cms.untracked.string("genParticles"),
            src = cms.InputTag("prunedGenParticles"),
            saveAllGenParticles = cms.untracked.bool(True),
#            saveGenElectrons = cms.untracked.bool(True),
#            saveGenMuons = cms.untracked.bool(True),
#            saveGenTaus = cms.untracked.bool(True),
#            saveGenNeutrinos = cms.untracked.bool(True),
#            saveTopInfo = cms.untracked.bool(True),
#            saveWInfo = cms.untracked.bool(True),
#            saveHplusInfo = cms.untracked.bool(True),
        )
    ),
)

# === Setup skim counters
process.load("HiggsAnalysis.MiniAOD2TTree.Hplus2tbAnalysisSkim_cfi")
process.skimCounterAll        = cms.EDProducer("HplusEventCountProducer")
process.skimCounterPassed     = cms.EDProducer("HplusEventCountProducer")

# === Setup customizations
from HiggsAnalysis.MiniAOD2TTree.CommonFragments import produceCustomisations
produceCustomisations(process,dataVersion.isData()) # This produces process.CustomisationsSequence which needs to be included to path

# module execution
process.runEDFilter = cms.Path(process.PUInfo*
                               process.TopPtProducer*
                               process.skimCounterAll*
                               process.skim*
                               process.skimCounterPassed*
                               process.CustomisationsSequence*
                               process.dump)

#process.output = cms.OutputModule("PoolOutputModule",
#   outputCommands = cms.untracked.vstring(
#       "keep *",
#   ),
#   fileName = cms.untracked.string("CMSSW.root")
#)
#process.out_step = cms.EndPath(process.output)
