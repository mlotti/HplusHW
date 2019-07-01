# For miniAOD instructions see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015

import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git
from HiggsAnalysis.MiniAOD2TTree.tools.HChOptions import getOptionsDataVersion

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
from HiggsAnalysis.MiniAOD2TTree.CommonFragments import produceCustomisations





process = cms.Process("TTreeDump")



#dataVersion = "80Xdata"
dataVersion = "80Xmc"




options, dataVersion = getOptionsDataVersion(dataVersion)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)


process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.categories.append("TriggerBitCounter")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.MessageLogger.cerr.TriggerBitCounter = cms.untracked.PSet(limit = cms.untracked.int32(1000))



# Set the process options -- Display summary at the end, enable unscheduled execution
process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)




process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#     'file:cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT.root'
#     '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_1/180830_140204/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root'
#    '/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root',
#    '/store/data/Run2016B/Tau/MINIAOD/PromptReco-v2/000/273/150/00000/64EFFDF2-D719-E611-A0C3-02163E01421D.root',
#    '/store/user/mlotti/MinBias/CRAB3_test5_PAT/180531_132305/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#    '/store/user/mlotti/MinBias/CRAB3_test5_PAT/180531_132305/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_2.root',
#    '/store/user/mlotti/MinBias/CRAB3_test5_PAT/180531_132305/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_3.root'
#     '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT/180613_123703/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_2.root'
#	'/store/mc/RunIISummer16MiniAODv2/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/066DC28C-02CB-E611-B4F0-5065F382B2D1.root'

#     '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT/180613_123703/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_11.root' #real
#     '/store/data/Run2016H/Tau/MINIAOD/03Feb2017_ver2-v1/100000/00A17AC6-8AEB-E611-9A86-A0369F83627E.root',
     '/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root'
#      '/store/mc/RunIISummer16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/80000/F283191C-11C4-E611-973D-00215E2EB74E.root'
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_1/180911_130929/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_2/180911_131520/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_3/180911_131616/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_4/180911_131722/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_5/180911_131853/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_6/180911_131948/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_7/180911_132140/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_8/180911_132807/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_10/180911_133053/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root',
#      '/store/user/mlotti/CRAB_PrivateMC/CRAB3_Hplus_PAT_11/180911_133146/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root'
#       '/store/user/mlotti/CRAB_PrivateMC/Hplus2hw_4l_PAT_m350_f/181120_122629/0000/cHiggs_13TeV_TuneCUETP8M1_cfi_GEN_SIM_RECOBEFMIX_DIGIPREMIX_S2_DATAMIX_L1_DIGI2RAW_L1Reco_RECO_HLT_PAT_1.root'
    )
)


process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')
print "GlobalTag="+dataVersion.getGlobalTag()


process.load("HiggsAnalysis/MiniAOD2TTree/PUInfo_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/TopPt_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Tau_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Electron_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Muon_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Jet_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Top_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/MET_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/METNoiseFilter_cfi")
process.METNoiseFilter.triggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getMETFilteringProcess()))




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
        TriggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getTriggerProcess())),
        TriggerBits = cms.vstring(
	     "HLT_IsoMu24_v",
	     "HLT_IsoTkMu24_v",
	     "HLT_Ele27_eta2p1_WPTight_Gsf_v",
        ),
	L1Extra = cms.InputTag("l1extraParticles:MET"),
        L1EtSumObjects = cms.InputTag("caloStage2Digis:EtSum"),
        TriggerObjects = cms.InputTag("selectedPatTrigger"),
        TriggerMatch = cms.untracked.vstring(
	     "HLT_IsoMu24_v",
	     "HLT_Ele27_eta2p1_WPTight_Gsf_v" ,
        ),
	TriggerPrescales = cms.untracked.PSet(
            src   = cms.InputTag("patTrigger",""),
            paths = cms.vstring(
		"HLT_IsoMu24_v", 
	        "HLT_Ele27_eta2p1_WPTight_Gsf_v",
            )
	),
	filter = cms.untracked.bool(False)
    ),

    METNoiseFilter = process.METNoiseFilter,
    Taus      = process.Taus,
    Electrons = process.Electrons,
    Muons     = process.Muons,
    Jets      = process.Jets,
    #Top       = process.Top,
    METs      = process.METs,
    GenWeights = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenWeights"),
            src = cms.InputTag("generator"),
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
            saveGenBooleans     = cms.untracked.bool(False),
            saveGenStatusFlags  = cms.untracked.bool(False),
#            saveGenElectrons = cms.untracked.bool(True),
#            saveGenMuons = cms.untracked.bool(True),
#            saveGenTaus = cms.untracked.bool(True),
#            saveGenNeutrinos = cms.untracked.bool(True),
#            saveTopInfo = cms.untracked.bool(True),
#            saveWInfo = cms.untracked.bool(True),
#            saveHplusInfo = cms.untracked.bool(True),
        )
    ),
    #Tracks =  cms.VPSet( # Caution: this effectively doubles disc space usage
    #    cms.PSet(
    #        branchname = cms.untracked.string("PFcandidates"),
    #        src = cms.InputTag("packedPFCandidates"),
    #        OfflinePrimaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    #        ptCut = cms.untracked.double(0.0), # pt < value
    #        etaCut = cms.untracked.double(2.5), # abs(eta) < value
    #        saveOnlyChargedParticles = cms.untracked.bool(True),
    #        IPvsPVz = cms.untracked.double(5), # abs(IPz-PVz) < value
    #    )
    #),
)









# === Setup skim counters
process.load("HiggsAnalysis.MiniAOD2TTree.Hplus2hwAnalysisSkim_cfi")
process.skimCounterAll        = cms.EDProducer("HplusEventCountProducer")
process.skimCounterPassed     = cms.EDProducer("HplusEventCountProducer")
process.skim.TriggerResults   = cms.InputTag("TriggerResults::"+str(dataVersion.getTriggerProcess()))

# === Setup customizations
produceCustomisations(process,dataVersion.isData()
) # This produces process.CustomisationsSequence which needs to be included to path

# module execution
process.runEDFilter = cms.Path(process.PUInfo*
                               process.TopPtProducer*
                               process.skimCounterAll*
                               process.skim*
                               process.skimCounterPassed*
                               process.CustomisationsSequence*
                               process.dump
)
