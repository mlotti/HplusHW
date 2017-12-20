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
maxEvents    = 10000
maxWarnings  = 100
reportEvery  = 100
testWithData = True
if testWithData:
    dataVersion  = "80Xdata"
    datasetFiles = [
        #'/store/data/Run2016H/SingleElectron/MINIAOD/03Feb2017_ver2-v1/100000/00553E5F-29EC-E611-ADB0-00259074AE8C.root',
        #'/store/data/Run2016H/SingleMuon/MINIAOD/03Feb2017_ver2-v1/110000/00633FF0-85EA-E611-811C-001E674FB25C.root',
        '/store/data/Run2016H/JetHT/MINIAOD/03Feb2017_ver2-v1/50000/001AD386-94EB-E611-B49D-001517E73B9C.root',
        ]
else:
    dataVersion  = "80Xmc" 
    datasetFiles = [
        '/store/mc/RunIISummer16MiniAODv2/ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/100000/0A978AC8-86DD-E611-9594-002590E7DD98.root',
#        '/store/mc/RunIISummer16MiniAODv2/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/00000/0028537E-E758-E711-9315-0025905A497A.root',
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
)

#================================================================================================ 
# Setup skim counters
#================================================================================================ 
process.load("HiggsAnalysis.MiniAOD2TTree.Hplus2tbAnalysisSync_cfi")
process.skimCounterAll        = cms.EDProducer("HplusEventCountProducer")
process.skimCounterPassed     = cms.EDProducer("HplusEventCountProducer")
process.skim.TriggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getTriggerProcess()))

#================================================================================================ 
# Setup customizations
#================================================================================================ 
from HiggsAnalysis.MiniAOD2TTree.CommonFragments import produceCustomisations
produceCustomisations(process, dataVersion.isData()) # This produces process.CustomisationsSequence which needs to be included to path

# Marina 
# ===============================================================================================
# Set up electron MVA ID
# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

print "=== Adding Electron MVA: ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)

for idmod in ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff']:
    setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)

#================================================================================================ 
# Module execution
#================================================================================================ 
process.runEDFilter = cms.Path(process.PUInfo*
                               process.TopPtProducer*
                               process.egmGsfElectronIDSequence*
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
