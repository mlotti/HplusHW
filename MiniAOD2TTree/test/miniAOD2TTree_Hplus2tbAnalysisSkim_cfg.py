'''
For miniAOD instructions see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015 
'''
#================================================================================================  
# Import Modules
#================================================================================================  
import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git
from HiggsAnalysis.MiniAOD2TTree.tools.HChOptions import getOptionsDataVersion


#================================================================================================  
# Options
#================================================================================================  
maxEvents    = 1000
maxWarnings  = 100
reportEvery  = 100
testWithData = True
if testWithData:
    dataVersion  = "80Xdata"
    datasetFiles = [
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/000C9243-5634-E711-A2A8-0CC47A7C3612.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/04BFE78E-5D34-E711-BCA5-0025905A48D8.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/0A3F8104-6434-E711-9E9A-0CC47A4D76C6.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/0C95C3F7-3534-E711-8FBB-0CC47A7C3612.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/1032026F-4334-E711-84CE-0CC47A4C8E3C.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/10898316-5034-E711-8167-0CC47A4D7644.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/12062AF2-3A34-E711-BA6A-003048FFD79E.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/12A273CE-2235-E711-A7C7-0025905A605E.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/12CED57A-4334-E711-961B-003048FFD734.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/14BEF0C3-4234-E711-B811-0025905A48E4.root',
        '/store/data/Run2016C/JetHT/MINIAOD/18Apr2017-v1/100000/16E75845-5634-E711-915E-0025905A60DE.root'
        ]
else:
    dataVersion  = "80Xmc" 
    datasetFiles = [
        # '/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root',
        # '/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0806AB92-99BE-E611-9ECD-0025905A6138.root',
        # '/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/165F54A0-A3BE-E611-B3F7-0025905A606A.root',
        # '/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/18E31463-B3BE-E611-B6A3-0CC47A4D7678.root',
        # '/store/mc/RunIISummer16MiniAODv2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/110000/0055B499-54B6-E611-9F86-FA163E1F94C5.root',
        # '/store/mc/RunIISummer16MiniAODv2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/110000/02B77462-7CB5-E611-A061-0025905B8568.root',
        # '/store/mc/RunIISummer16MiniAODv2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/110000/02CDB360-51B5-E611-A568-002590747E0E.root',
        # '/store/mc/RunIISummer16MiniAODv2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/110000/0486046D-0BB6-E611-B533-002590D9D8C0.root',
        '/store/mc/RunIISummer16MiniAODv2/ZJetsToQQ_HT600toInf_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/16DC0526-F4FA-E611-938E-6CC2173BBA40.root',
        '/store/mc/RunIISummer16MiniAODv2/ZJetsToQQ_HT600toInf_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/18DFBF7B-B5FC-E611-80D2-002481DE49B6.root',
        '/store/mc/RunIISummer16MiniAODv2/ZJetsToQQ_HT600toInf_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/110000/20C84FF5-11FB-E611-AA3C-C4346BC70B58.root'
        ]
    
# For debugging purposes
debug       = False
RunNum_1    = 1
LumiBlock_1 = 2
EvtNum_1    = 240
RunNum_2    = 1
LumiBlock_2 = 2
EvtNum_2    = 260


#================================================================================================  
# Setup the Process
#================================================================================================  
process = cms.Process("TTreeDump")
process.options = cms.untracked.PSet(
    #SkipEvent         = cms.untracked.vstring('ProductNotFound'),
    wantSummary       = cms.untracked.bool(debug),
    printDependencies = cms.untracked.bool(debug),
)
process.maxEvents = cms.untracked.PSet(
    input         = cms.untracked.int32(maxEvents)
    )


#================================================================================================  
# Tracer service is for debugging purposes (Tells user what cmsRun is accessing)
#================================================================================================  
if debug:
    process.Tracer = cms.Service("Tracer")


#================================================================================================  
# Setup the Process
#================================================================================================  
process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.categories.append("TriggerBitCounter")
process.MessageLogger.cerr.FwkReport.reportEvery = reportEvery # print the event number for every 100th event
process.MessageLogger.cerr.TriggerBitCounter = cms.untracked.PSet(limit = cms.untracked.int32(maxWarnings)) # print max 100 warnings

#================================================================================================  
# Set the process options -- Display summary at the end, enable unscheduled execution
#================================================================================================  
process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
    )

#================================================================================================  
# Define the input files 
#================================================================================================  
process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring('/store/data/Run2016B/JetHT/MINIAOD/PromptReco-v2/000/273/150/00000/66051AAF-D819-E611-BD3D-02163E011D55.root',)
                            fileNames = cms.untracked.vstring(datasetFiles)
                            #eventsToProcess = cms.untracked.VEventRange('%s:%s:%s-%s:%s:%s' % (RunNum_1, LumiBlock_1, EvtNum_1, RunNum_2, LumiBlock_2, EvtNum_2) ), 
                            )


#================================================================================================  
# Get Dataset version and Global tag
#================================================================================================  
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
options, dataVersion = getOptionsDataVersion(dataVersion)
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')


#================================================================================================  
# Print Settings
#================================================================================================  
msgAlign = "{:<10} {:<55} {:<25} {:<25}"
title    =  msgAlign.format("Data", "Global Tag", "Trigger Source", "Trigger Tag")
print "="*len(title)
print title
print "="*len(title)
print msgAlign.format(dataVersion.version, dataVersion.getGlobalTag(), dataVersion.getMETFilteringProcess(), dataVersion.getTriggerProcess())
print 


#================================================================================================
# Load processes
#================================================================================================
process.load("HiggsAnalysis/MiniAOD2TTree/PUInfo_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/TopPt_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Tau_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Electron_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Muon_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Jet_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/FatJet_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/SecondaryVertex_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Top_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/MET_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/METNoiseFilter_cfi")

process.METNoiseFilter.triggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getMETFilteringProcess())) 
print "check tau",process.Taus_TauPOGRecommendation[0]
process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName      = cms.string("miniaod2tree.root"),
    PUInfoInputFileName = process.PUInfo.OutputFileName,
    TopPtInputFileName  = process.TopPtProducer.OutputFileName,
    CodeVersion         = cms.string(git.getCommitId()),
    DataVersion         = cms.string(str(dataVersion.version)),
    CMEnergy            = cms.int32(13),
    Skim = cms.PSet(
	Counters = cms.VInputTag(
	    "skimCounterAll",
            "skimCounterPassed"
        ),
    ),
    EventInfo = cms.PSet(
        PileupSummaryInfoSrc        = process.PUInfo.PileupSummaryInfoSrc, 
	LHESrc                      = cms.untracked.InputTag("externalLHEProducer"),
	OfflinePrimaryVertexSrc     = cms.InputTag("offlineSlimmedPrimaryVertices"),
	TopPtProducer               = cms.InputTag("TopPtProducer"),
    ),
    Trigger = cms.PSet(
	TriggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getTriggerProcess())),
	TriggerBits    = cms.vstring(
            "HLT_PFHT300_v",
            "HLT_PFHT350_v",
            "HLT_PFHT400_v",
            #"HLT_PFHT475_v",
            #"HLT_PFHT600_v",
            #"HLT_PFHT650_v",
            "HLT_PFJet450_v", # for efficiency recovery in 2016H
            "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v",
            "HLT_PFHT450_SixJet40_BTagCSV_p056_v",
            "HLT_PFHT400_SixJet30_v",
            "HLT_PFHT450_SixJet40_v",
        ),
	L1Extra        = cms.InputTag("l1extraParticles:MET"),
	TriggerObjects = cms.InputTag("selectedPatTrigger"),
        TriggerMatch   = cms.untracked.vstring(
            "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056_v",
            "HLT_PFHT450_SixJet40_BTagCSV_p056_v",
        ),
	filter = cms.untracked.bool(False)
    ),
    METNoiseFilter = process.METNoiseFilter,
    Taus      = process.Taus_TauPOGRecommendation,
    Electrons = process.Electrons,
    Muons     = process.Muons,
    Jets      = process.Jets,
    SoftBTag  = process.SoftBTag,
    Top       = process.Top,
    METs      = process.METs,
    GenWeights = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenWeights"),
            src        = cms.InputTag("generator"),
            filter     = cms.untracked.bool(False)
        )
    ),
    GenMETs = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenMET"),
            src        = cms.InputTag("genMetTrue"),
            filter     = cms.untracked.bool(False)
        )
    ),
    GenJets = cms.VPSet(      
        cms.PSet(
            branchname = cms.untracked.string("GenJets"),
            src        = cms.InputTag("slimmedGenJets"), # ak4
        )
    ),
    GenParticles = cms.VPSet(      
        cms.PSet(
            branchname          = cms.untracked.string("genParticles"),
            src                 = cms.InputTag("prunedGenParticles"),
            saveAllGenParticles = cms.untracked.bool(True),
            saveGenBooleans     = cms.untracked.bool(True),
            saveGenStatusFlags  = cms.untracked.bool(True),
            saveGenElectrons    = cms.untracked.bool(False),
            saveGenMuons        = cms.untracked.bool(False),
            saveGenTaus         = cms.untracked.bool(False),
            saveGenNeutrinos    = cms.untracked.bool(False),
            saveTopInfo         = cms.untracked.bool(False),
            saveWInfo           = cms.untracked.bool(False),
            saveHplusInfo       = cms.untracked.bool(False),
        )
    ),
    FatJets = process.FatJets,
)

#================================================================================================ 
# Setup skim counters
#================================================================================================ 
process.load("HiggsAnalysis.MiniAOD2TTree.Hplus2tbAnalysisSkim_cfi")
process.skimCounterAll        = cms.EDProducer("HplusEventCountProducer")
process.skimCounterPassed     = cms.EDProducer("HplusEventCountProducer")
process.skim.TriggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getTriggerProcess()))

#================================================================================================ 
# Setup customizations
#================================================================================================ 
from HiggsAnalysis.MiniAOD2TTree.CommonFragments import produceCustomisations
produceCustomisations(process, dataVersion.isData()) # This produces process.CustomisationsSequence which needs to be included to path


#================================================================================================ 
# Module execution
#================================================================================================ 
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
