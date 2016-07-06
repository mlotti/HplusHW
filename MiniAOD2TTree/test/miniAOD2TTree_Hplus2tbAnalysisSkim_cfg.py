'''
For miniAOD instructions see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015 
'''
#================================================================================================  
# Import Modules
#================================================================================================  
import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

process = cms.Process("TTreeDump")

dataVersion = "80Xmc"
#dataVersion = "80Xdata"

options, dataVersion = getOptionsDataVersion(dataVersion)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000) #-1
)

process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.categories.append("TriggerBitCounter")
process.MessageLogger.cerr.FwkReport.reportEvery = 100 # print the event number for every 100th event
process.MessageLogger.cerr.TriggerBitCounter = cms.untracked.PSet(limit = cms.untracked.int32(10)) # print max 100 warnings

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'/store/data/Run2016B/JetHT/MINIAOD/PromptReco-v2/000/273/150/00000/66051AAF-D819-E611-BD3D-02163E011D55.root',
        '/store/mc/RunIISpring16MiniAODv2/ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/20000/04F56101-3739-E611-90EE-0CC47A78A41C.root',
        )
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, cms.string(dataVersion.getGlobalTag()), '')
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')
print "GlobalTag="+dataVersion.getGlobalTag()

# ===== Set up tree dumper =====
TrgResultsSource = "TriggerResults::PAT"
if dataVersion.isData():
    TrgResultsSource = "TriggerResults::RECO"
print "Trigger source has been set to:",TrgResultsSource

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
            "HLT_QuadJet45_DoubleBTagCSV_p087_v2",
            "HLT_QuadPFJet_VBF_v5",
            "HLT_PFHT300_v3",
            "HLT_PFHT400_v3",
            "HLT_PFHT475_v3",
            "HLT_PFHT600_v4",
            "HLT_PFHT650_v4",
            "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v2",
            "HLT_PFHT450_SixJet40_BTagCSV_p056_v2",
            "HLT_PFHT400_SixJet30_v4",
            "HLT_PFHT450_SixJet40_v4",
            "HLT_HT200_v2",
            "HLT_HT275_v2",
            "HLT_HT325_v2",
            "HLT_HT425_v2",
            "HLT_HT575_v2",
            "HLT_HT650_v3",
            "HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq200_v2",
            "HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq460_v2",
            "HLT_QuadPFJet_BTagCSV_p016_p11_VBF_Mqq240_v2",
            "HLT_QuadPFJet_BTagCSV_p016_VBF_Mqq500_v2",
            "HLT_QuadPFJet_VBF_v5",
        ),
	L1Extra = cms.InputTag("l1extraParticles:MET"),
	TriggerObjects = cms.InputTag("selectedPatTrigger"),
        TriggerMatch = cms.untracked.vstring(
            #"LooseIsoPFTau50_Trk30_eta2p1",
        ),
	filter = cms.untracked.bool(False)
    ),
    METNoiseFilter = cms.PSet(
        triggerResults = cms.InputTag(TrgResultsSource),
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
produceCustomisations(process) # This produces process.CustomisationsSequence which needs to be included to path

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
