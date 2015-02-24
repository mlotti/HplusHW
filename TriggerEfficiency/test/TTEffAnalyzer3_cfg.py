import FWCore.ParameterSet.Config as cms
import copy

#dataVersion="53XmcS10"
dataVersion="53XdataPromptCv2"
#isData = False
runL1Emulator = False
runOpenHLT = False
analysis = "TauLeg"
#analysis = "MetLeg"
hltType = "HLT"
#hltType = "TEST"

from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
options, dataVersion = getOptionsDataVersion(dataVersion)

if not options.trgAnalysis == "":
    analysis = options.trgAnalysis

process = cms.Process("TTEff")

### Add HLT stuff (it may contain maxEvents and MessageLogger, so it
### should be loaded first before or maxEvents nad MessageLogger would
### be reset)
process.load("HiggsAnalysis.TriggerEfficiency.TTEffAnalysisHLT_cfi")
process.prefer("magfield")
process.hltGctDigis.hltMode = cms.bool(False) # Making L1CaloRegions

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(-1)
)

process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.categories.append("TTEffAnalyzer")
process.MessageLogger.cerr.FwkReport.reportEvery = 100 # print the event number for every 100th event
process.MessageLogger.cerr.TTEffAnalyzer = cms.untracked.PSet(limit = cms.untracked.int32(100)) # print max 100 warnings from TTEffAnalyzer
# process.MessageLogger.debugModules = cms.untracked.vstring("TTEffAnalyzer")
# process.MessageLogger.cerr.threshold = cms.untracked.string("DEBUG")   # pring LogDebugs and above
# process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")    # print LogInfos and above
# process.MessageLogger.cerr.threshold = cms.untracked.string("WARNING") # print LogWarnings and above

process.options = cms.untracked.PSet(
#    wantSummary = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False),
    SkipEvent = cms.untracked.vstring("TrajectoryState") # FIXME: problem with cmssw42X TSGFromL2Muon
)

#Mike needs Calo Geometry
####process.load('Configuration.Geometry.GeometryPilot2_cff')

if dataVersion.isMC():
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
#       "file:TTEffSkim.root"
#	"root://madhatter.csc.fi:1094/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/TriggerMETLeg/CMSSW_5_3_X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1/638a70bdbf1f7414f9f442a75689ed2b/pattuple_486_2_ZHP.root"
	"root://madhatter.csc.fi:1094/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/TriggerTauLeg/CMSSW_5_3_X/DYToTauTau_M-20_CT10_TuneZ2star_8TeV-powheg-tauola-pythia6/Summer12_DR53X_PU_S8_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v2/8728052812930676480ae2a242229ec9/pattuple_32_1_0N1.root"
#        "file:/tmp/slehti/TauTriggerEff_DYToTauTau_M_20_TuneZ2star_8TeV_pythia6_tauola_Summer12_PU_S8_START52_V9_v1_AODSIM_TTEffSkim_v525_V00_10_04_v2_TTEffSkim_70_1_hQW.root"
        )
    )
else:
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(   
#        "file:/afs/cern.ch/work/s/slehti/TriggerMETLeg_Tau_173236-173692_2011A_Nov08_pattuple_9_1_LSf.root"
#        "file:TTEffSkim.root"
#	"file:/tmp/slehti/TriggerMETLeg_Tau_Run2012C_PromptReco_v2_AOD_202792_203742_analysis_metleg_v53_v1_pattuple_28_1_L19.root"
       'root://madhatter.csc.fi:1094/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/TriggerMETLeg/CMSSW_5_3_X/TauParked/Run2012D_22Jan2013_v1_AOD_203777_208686_triggerMetLeg_skim_v53_3c/65583ace3198f0f55b2cd7d093b9f259/pattuple_3940_3_oJW.root'
        )
    )

#if(isData):
#    process.source = cms.Source("PoolSource",
#        fileNames = cms.untracked.vstring(
##	"file:/tmp/slehti/hlt_100_1_yct.root"
##	"file:/afs/cern.ch/work/s/slehti/TriggerMETLeg_Tau_Run2012C_PromptReco_v2_AOD_202792_203742_analysis_metleg_v53_v1_pattuple_28_1_L19.root"
#	"file:/afs/cern.ch/work/s/slehti/TriggerMETLeg_Tau_173236-173692_2011A_Nov08_pattuple_9_1_LSf.root"
##        "file:TTEffSkim.root"
##	"file:/afs/cern.ch/work/s/slehti/TTEffSkim_Run2012A_TauPlusX_801ev.root"
##        "file:TauPlusX_Run2012B_PromptReco_v1_AOD_TTEffSkim_v525_V00_10_06_v1.root"
##	"/store/user/luiggi/MinimumBias/TTEffSkimRun2011A_GoldenPlusESIgnoredJSON/a6b050dc4acb87f74e46528e006dff64/TTEffSkim_1_1_Zd8.root",
##	"/store/user/luiggi/MinimumBias/TTEffSkimRun2011A_GoldenPlusESIgnoredJSON/a6b050dc4acb87f74e46528e006dff64/TTEffSkim_2_1_IA6.root",
##	"/store/user/luiggi/MinimumBias/TTEffSkimRun2011A_GoldenPlusESIgnoredJSON/a6b050dc4acb87f74e46528e006dff64/TTEffSkim_3_1_I9j.root"
##	"/store/group/pflow-tau/TauTriggerEfficiencyMeasurementData/TauPlusX_Run2012B_PromptReco_v1_AOD_TTEffSkim_v525_V00_10_06_v1/TauPlusX/TauTriggerEff_TauPlusX_Run2012B_PromptReco_v1_AOD_TTEffSkim_v525_V00_10_06_v1/be6ecd52f198917de1be5ff208a419ce/TTEffSkim_939_1_ceG.root"
#	)
#    )
#else:
#    process.source = cms.Source("PoolSource",
#	fileNames = cms.untracked.vstring(
##	"file:/tmp/slehti/TauTriggerEff_DYToTauTau_M_20_TuneZ2star_8TeV_pythia6_tauola_Summer12_PU_S8_START52_V9_v1_AODSIM_TTEffSkim_v525_V00_10_04_v2_TTEffSkim_70_1_hQW.root"
##	"file:TTEffSkim.root"
#	"file:/tmp/slehti/TTJets_TuneZ2_7TeV_Fall11_START44_V9B_v1_AODSIM_pattuple_244_1_vQB.root"
##        "file:/tmp/slehti/TTToHplusBWB_M_160_7TeV_pythia6_tauola_Fall11_E7TeV_Ave23_50ns_v2_RAW_RECO_TTEffSkim_160_1_OZG.root"
#	)
#    )

process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
print "GlobalTag="+dataVersion.getGlobalTag()
#if (isData):
##    process.GlobalTag.globaltag = 'GR_H_V29::All'
#    process.GlobalTag.globaltag = 'GR_R_44_V15::All'
##    process.GlobalTag.globaltag = 'GR_R_53_V2::All'
##    process.GlobalTag.globaltag = 'TESTL1_GR_P::All'
#else:
#    #process.GlobalTag.globaltag = 'START52_V9::All'
#    process.GlobalTag.globaltag = 'START44_V13::All'
#process.GlobalTag.connect   = 'frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'
#process.GlobalTag.pfnPrefix = cms.untracked.string('frontier://FrontierProd/')
#print process.GlobalTag.globaltag

from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)

import HiggsAnalysis.HeavyChHiggsToTauNu.TopPtWeight_cfi as topPtWeight
process.topPtWeight = topPtWeight.topPtWeight.clone()
if options.sample == "TTJets":
    topPtWeight.addTtGenEvent(process, process.commonSequence)
    process.topPtWeight.enabled = True
    process.commonSequence += process.topPtWeight

if dataVersion.isMC():
    process.TauMCProducer = cms.EDProducer("HLTTauMCProducer",
        GenParticles  = cms.untracked.InputTag("genParticles"),
        ptMinTau      = cms.untracked.double(3),
        ptMinMuon     = cms.untracked.double(3),
        ptMinElectron = cms.untracked.double(3),
        BosonID       = cms.untracked.vint32(23),
        EtaMax         = cms.untracked.double(2.5)
    )

    process.commonSequence += (
####        process.hltPhysicsDeclared+
	process.TauMCProducer
    )

from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import *
addPrimaryVertexSelection(process,process.commonSequence)
process.selectedPrimaryVertexFilter = cms.EDFilter("VertexCountFilter",
                                                    src = cms.InputTag("selectedPrimaryVertex"),
                                                    minNumber = cms.uint32(1),
                                                    maxNumber = cms.uint32(999)
                                                    )
process.commonSequence *= process.selectedPrimaryVertexFilter

# Reproduce the mu-tau pair objects, as they are not kept in the skim at the moment
if analysis == "TauLeg":
    import HiggsAnalysis.HeavyChHiggsToTauNu.TauLegZMuTauFilter as zmutau
    process.muTauPairs = zmutau.muTauPairs.clone()
    process.muTauPairs.decay = cms.string('selectedPatMuons@+ selectedPatTaus@-')
    process.commonSequence *= process.muTauPairs
    additionalCounters.extend(zmutau.getSelectionCounters())

# Correction of reco::PFJets (from 5xy configuration due to JetMETCorrections/Modules ...
process.ak5PFL1Offset = cms.ESProducer('L1OffsetCorrectionESProducer',
    level = cms.string('L1Offset'),
    algorithm = cms.string('AK5PF'),
    vertexCollection = cms.string('offlinePrimaryVertices'),
    minVtxNdof = cms.int32(4)
)
process.ak5PFL2Relative = cms.ESProducer('LXXXCorrectionESProducer',
    level     = cms.string('L2Relative'),
    algorithm = cms.string('AK5PF')
)
process.ak5PFL3Absolute = cms.ESProducer('LXXXCorrectionESProducer',
    level     = cms.string('L3Absolute'),
    algorithm = cms.string('AK5PF')
)
process.ak5PFL1L2L3 = cms.ESProducer('JetCorrectionESChain',
    correctors = cms.vstring('ak5PFL1Offset','ak5PFL2Relative','ak5PFL3Absolute')
)
process.ak5PFJetsL1L2L3   = cms.EDProducer('PFJetCorrectionProducer',
    src         = cms.InputTag('ak5PFJets'),
    correctors  = cms.vstring('ak5PFL1L2L3')
)
####process.commonSequence *= process.ak5PFJetsL1L2L3

# Good vertex selection
process.goodPrimaryVertices = cms.EDFilter("VertexSelector",
    filter = cms.bool(False),
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) < 24.0 && position.rho < 2.0")
)
process.commonSequence *= process.goodPrimaryVertices

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChMETFilter_cfi")
process.commonSequence *= process.hPlusMETNoiseFilters

# Analyzer definition
process.TTEffAnalysisHLTPFTauHPS = cms.EDAnalyzer("TTEffAnalyzer2",
####        LoopingOver	        = cms.InputTag("selectedPatTausHpsPFTau"),
	LoopingOver		= cms.InputTag("selectedPatTaus"),
	PFTauDiscriminators     = cms.vstring(
            "decayModeFinding",
            "againstMuonLoose",
            "againstMuonMedium",
            "againstMuonTight",
            "againstMuonLoose2",
            "againstMuonMedium2",
            "againstMuonTight2",
            "againstElectronLoose",
            "againstElectronMedium",
            "againstElectronTight",
	    "againstElectronMVA",
	    "againstElectronLooseMVA3",
            "againstElectronMediumMVA3",
            "againstElectronTightMVA3",
            "againstElectronVTightMVA3",
#            "byVLooseIsolation",
#            "byLooseIsolation",
#            "byMediumIsolation",
#            "byTightIsolation",
#            "byVLooseIsolationDeltaBetaCorr",
#            "byLooseIsolationDeltaBetaCorr",
#            "byMediumIsolationDeltaBetaCorr",
#            "byTightIsolationDeltaBetaCorr",
            "byVLooseCombinedIsolationDeltaBetaCorr",
            "byLooseCombinedIsolationDeltaBetaCorr",
            "byMediumCombinedIsolationDeltaBetaCorr",
            "byTightCombinedIsolationDeltaBetaCorr",
	    "byLooseCombinedIsolationDeltaBetaCorr3Hits",
	    "byMediumCombinedIsolationDeltaBetaCorr3Hits",
            "byTightCombinedIsolationDeltaBetaCorr3Hits",
            "byLooseIsolationMVA2",
            "byMediumIsolationMVA2",
            "byTightIsolationMVA2",
        ),
	Counters                = cms.VInputTag([cms.InputTag(c) for c in additionalCounters]),
	Selections = cms.vstring(
	    "hPlusGlobalElectronVetoFilter",
	    "hPlusGlobalMuonVetoFilter",
	),

        METs = cms.PSet(
	    PFMET = cms.InputTag("patPFMet"),
	    PFMETtype1 = cms.InputTag("patType1CorrectedPFMet"),
##            PFMET = cms.InputTag("pfMet"),
##	    PFMETtype1 = cms.InputTag("pfType1CorrectedMet"),
##            HLTMET = cms.InputTag("hltMet"),
##            HLTMHT = cms.InputTag("hltPFMHTProducer"),
##            CaloMET = cms.InputTag("met")
            CaloMET = cms.InputTag("patCaloMET"),
#            CaloMETresidualCorrected = cms.InputTag("patResidualCorrectedCaloMET"),
#            CaloMETnoHF = cms.InputTag("patCaloMETnoHF"),
#            CaloMETnoHFresidualCorrected = cms.InputTag("patResidualCorrectedCaloMETnoHF"),
        ),

	MuonSource        = cms.InputTag("selectedPatMuons"),
	MuonTauPairSource = cms.InputTag("muTauPairs"),

#        Jets = cms.InputTag("ak5PFJetsL1L2L3"),
	Jets = cms.InputTag("selectedPatJets"),
	JetPUIDsrc = cms.InputTag("puJetMva", "fullId"), # options: 'full' (BDT based), 'cutbased', 'philv1', 'simple'

	lheSrc 			= cms.InputTag("source", "", "LHE"),
	VisibleTauSrc		= cms.InputTag("VisibleTaus","HadronicTauOneAndThreeProng"),
	GenParticleCollection	= cms.InputTag("genParticles"),
	MCMatchingCone		= cms.double(0.2),

        offlineVertexSrc = cms.InputTag("goodPrimaryVertices"),

	L1extraTauJetSource			= cms.InputTag("l1extraParticles", "Tau"),
	L1extraCentralJetSource			= cms.InputTag("l1extraParticles", "Central"),

	L1extraMETSource			= cms.InputTag("l1extraParticles", "MET"),
	L1extraMHTSource			= cms.InputTag("l1extraParticles", "MHT"),

        L1GtReadoutRecord       		= cms.InputTag("gtDigis",""),
        L1GtObjectMapRecord     		= cms.InputTag("hltL1GtObjectMap","",hltType),
#	L1GtObjectMapRecord			= cms.InputTag("l1L1GtObjectMap"),
        L1Paths = cms.vstring(
            "L1_SingleMu7",
            "L1_SingleMu10",
            "L1_SingleMu12",
            "L1_SingleMu14_Eta2p1",
            "L1_SingleMu16_Eta2p1",

            "L1_SingleTauJet52", "L1_SingleJet68",
            "L1_SingleJet52_Central",
            "L1_Jet52_Central_ETM30",
            "L1_TripleJet28_Central",
	    "L1_TripleJetC_52_28_28",
            "L1_ETM30",
	    "L1_ETM36",
	    "L1_ETM40",
	    "L1_ETM50",
	    "L1_Mu12er_ETM20"
        ),
        HltResults      = cms.InputTag("TriggerResults","",hltType),
	TriggerEvent    = cms.InputTag("hltTriggerSummaryAOD","",hltType),
	PatTriggerEvent = cms.InputTag("patTriggerEvent"),
        HltObjectLastFilter = cms.InputTag("hltPFTau35TrackPt20LooseIsoProng2","",hltType),
        HltObjectFilters = cms.VInputTag([cms.InputTag(f, "", hltType) for f in [
                "hltPFTau35",
                "hltPFTau35Track",
                "hltPFTau35TrackPt20",
                "hltPFTau35TrackPt20LooseIso",
                "hltPFTau35TrackPt20LooseIsoProng2",
            ]]
        ),
#        HltObjectFilter = cms.InputTag("hltQuadJet80L1FastJet","",hltType),
        HltPaths = cms.vstring(
            "HLT_IsoMu17_v5", "HLT_IsoMu17_v6", "HLT_IsoMu17_v8", "HLT_IsoMu17_v9", "HLT_IsoMu17_v10", "HLT_IsoMu17_v11", "HLT_IsoMu17_v13", "HLT_IsoMu17_v14",
            "HLT_IsoMu17_eta2p1_v1",
            "HLT_IsoMu20_v8", "HLT_IsoMu20_v9", "HLT_IsoMu20_v12", "HLT_IsoMu20_v13",
            "HLT_IsoMu20_eta2p1_v1","HLT_IsoMu20_eta2p1_v2","HLT_IsoMu20_eta2p1_v3","HLT_IsoMu20_eta2p1_v4","HLT_IsoMu20_eta2p1_v5","HLT_IsoMu20_eta2p1_v6","HLT_IsoMu20_eta2p1_v7",
            "HLT_IsoMu24_v1", "HLT_IsoMu24_v2", "HLT_IsoMu24_v4", "HLT_IsoMu24_v5", "HLT_IsoMu24_v6", "HLT_IsoMu24_v7", "HLT_IsoMu24_v8", "HLT_IsoMu24_v9", "HLT_IsoMu24_v12", "HLT_IsoMu24_v13",
            "HLT_IsoMu24_eta2p1_v3", "HLT_IsoMu24_eta2p1_v6", "HLT_IsoMu24_eta2p1_v7","HLT_IsoMu24_eta2p1_v8","HLT_IsoMu24_eta2p1_v9",
	    "HLT_IsoMu24_eta2p1_v10","HLT_IsoMu24_eta2p1_v11","HLT_IsoMu24_eta2p1_v12","HLT_IsoMu24_eta2p1_v13","HLT_IsoMu24_eta2p1_v14","HLT_IsoMu24_eta2p1_v15",
            "HLT_IsoMu30_v1", "HLT_IsoMu30_v2", "HLT_IsoMu30_v4", "HLT_IsoMu30_v5", "HLT_IsoMu30_v6", "HLT_IsoMu30_v7", "HLT_IsoMu30_v8",
            "HLT_IsoMu30_eta2p1_v3", "HLT_IsoMu30_eta2p1_v6", "HLT_IsoMu30_eta2p1_v7",
            "HLT_IsoMu34_eta2p1_v1",

	    "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v7",

	    "HLT_IsoMu15_eta2p1_L1ETM20_v1",
            "HLT_IsoMu15_eta2p1_L1ETM20_v2",
            "HLT_IsoMu15_eta2p1_L1ETM20_v3",
            "HLT_IsoMu15_eta2p1_L1ETM20_v4",
            "HLT_IsoMu15_eta2p1_L1ETM20_v5",
            "HLT_IsoMu15_eta2p1_L1ETM20_v6",
            "HLT_IsoMu15_eta2p1_L1ETM20_v7",

	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v1",
	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2",
            "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v3",
            "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4",
            "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v5",
            "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6",
	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7",
	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v8",
	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9",
	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v10",
	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L2PixelIsoTrk2_L1ETM20_v2",
	    "HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_L1ETM20_v2",

	    "HLT_L1ETM40_v1","HLT_L1ETM40_v2",

            "HLT_IsoPFTau35_Trk20_MET45_v1", "HLT_IsoPFTau35_Trk20_MET45_v2", "HLT_IsoPFTau35_Trk20_MET45_v4", "HLT_IsoPFTau35_Trk20_MET45_v6",
            "HLT_IsoPFTau35_Trk20_v2", "HLT_IsoPFTau35_Trk20_v3", "HLT_IsoPFTau35_Trk20_v4", "HLT_IsoPFTau35_Trk20_v6",
            "HLT_IsoPFTau35_Trk20_MET60_v2", "HLT_IsoPFTau35_Trk20_MET60_v3", "HLT_IsoPFTau35_Trk20_MET60_v4", "HLT_IsoPFTau35_Trk20_MET60_v6",
            "HLT_IsoPFTau45_Trk20_MET60_v2", "HLT_IsoPFTau45_Trk20_MET60_v3", "HLT_IsoPFTau45_Trk20_MET60_v4",
            "HLT_IsoPFTau35_Trk20_MET70_v2",
            "HLT_MediumIsoPFTau35_Trk20_v1", "HLT_MediumIsoPFTau35_Trk20_v5", "HLT_MediumIsoPFTau35_Trk20_v6",
            "HLT_MediumIsoPFTau35_Trk20_MET60_v1", "HLT_MediumIsoPFTau35_Trk20_MET60_v5", "HLT_MediumIsoPFTau35_Trk20_MET60_v6",
            "HLT_MediumIsoPFTau35_Trk20_MET70_v1", "HLT_MediumIsoPFTau35_Trk20_MET70_v5", "HLT_MediumIsoPFTau35_Trk20_MET70_v6",

	    "HLT_LooseIsoPFTau35_Trk20_Prong1_v1",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v2",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v3",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v4",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v5",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v6",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v7",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v8",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v9",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_v10",

	    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v1",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v5",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v8",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10",


	    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v1",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v2",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v3",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v4",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v5",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v6",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v7",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v8",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v9",
            "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v10",

        ),
        L1TauTriggerSource      		= cms.InputTag("tteffL1GTSeed"),
	L1JetMatchingCone			= cms.double(0.5),
	L1JetMatchingMode			= cms.string("nearestDR"), # "nearestDR", "highestEt"
        L1IsolationThresholds   		= cms.vuint32(1,2,3,4), # count regions with "et() < threshold", these are in GeV

	L2AssociationCollection 		= cms.InputTag("openhltL2TauIsolationProducer"),
        L2matchingDeltaR        		= cms.double(0.2),

        hltVertexSrc                            = cms.InputTag("hltPixelVertices"),
        L25TauSource                            = cms.InputTag("hltPFTaus"),
        L25MatchingCone                         = cms.double(0.3),
        L25Discriminators = cms.PSet(
            TrackFinding = cms.InputTag("hltPFTauTrackFindingDiscriminator"),
            LooseIso = cms.InputTag("hltPFTauLooseIsolationDiscriminator"),
            TrackPt20 = cms.InputTag("hltPFTauTrackPt20Discriminator"),
        ),
        L25Selections = cms.PSet(
            VertexSelection = cms.InputTag("pfTauVertexSelector")
        ),
        L3IsoQualityCuts                        = process.hltPFTauLooseIsolationDiscriminator.qualityCuts.isolationQualityCuts.clone(),

        PileupSummaryInfoSource                 = cms.InputTag("addPileupInfo"),
        outputFileName          		= cms.string("tteffAnalysis-hltpftau-hpspftau.root"),
	triggerBitsOnly				= cms.bool(False),
	TopPtWeight                             = cms.InputTag("topPtWeight")
)

#process.TTEffAnalysisHLTPFtauHPS.clone(
#    L2AssociationCollection = "openhltL2TauGlobalIsolationProducer",
#    outputFileName = cms.string("tteffAnalysis-hltpftaul2global-hpspftau.root")
#)
# process.TTEffAnalysisHLTPFTauTightHPS = process.TTEffAnalysisHLTPFTauHPS.clone(
#     L25TauSource = "hltPFTausTightIso",
#     L3IsoQualityCuts = process.hltPFTauTightIsoIsolationDiscriminator.qualityCuts.isolationQualityCuts.clone(),
#     outputFileName = "tteffAnalysis-hltpftautight-hpspftau.root",
# )
process.TTEffAnalysisHLTPFTauMediumHPS = process.TTEffAnalysisHLTPFTauHPS.clone(
    L25TauSource = "hltPFTausMediumIso",
    L3IsoQualityCuts = process.hltPFTauMediumIsoIsolationDiscriminator.qualityCuts.isolationQualityCuts.clone(),
    outputFileName = "tteffAnalysis-hltpftaumedium-hpspftau.root",
    L25Discriminators = cms.PSet(
        MediumIso = cms.InputTag("hltPFTauMediumIsoIsolationDiscriminator"),
        TrackFinding = cms.InputTag("hltPFTauMediumIsoTrackFindingDiscriminator"),
        TrackPt20 = cms.InputTag("hltPFTauMediumIsoTrackPt20Discriminator")
    ),
    L25Selections = cms.PSet(
        VertexSelection = cms.InputTag("pfTauVertexSelectorMediumIso")
    ),
)
process.TTEffAnalysisHLTPFTauMediumHPSL2Global = process.TTEffAnalysisHLTPFTauHPS.clone(
    L2AssociationCollection = "openhltL2TauGlobalIsolationProducer",
    outputFileName = "tteffAnalysis-hltpftaumediuml2global-hpspftau.root"
)

process.TTEffAnalysisMETLeg = process.TTEffAnalysisHLTPFTauHPS.clone(
    outputFileName  = "tteffAnalysis-metleg.root",
    triggerBitsOnly = cms.bool(True)
)

process.TTEffAnalysisQuadJet = process.TTEffAnalysisHLTPFTauHPS.clone(
#    LoopingOver = cms.InputTag("selectedPatTausHpsPFTau"), # FIXME: 53_v1 pattuples, remove this line for 53_v2 pattuples
    outputFileName  = "tteffAnalysis-quadjet.root",
    triggerBitsOnly = cms.bool(True)
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalElectronVetoFilter_cfi")
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalMuonVetoFilter_cfi")   
process.hPlusGlobalElectronVetoFilter.filter = False
process.hPlusGlobalMuonVetoFilter.filter     = False
process.TFileService = cms.Service("TFileService",fileName = cms.string('tfileservice.root'))
#from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import *
#addPrimaryVertexSelection(process,process.commonSequence)

process.runTTEffAna = cms.Path(process.commonSequence)
process.runTTEffAna += process.hPlusGlobalElectronVetoFilter
process.runTTEffAna += process.hPlusGlobalMuonVetoFilter
if analysis == "TauLeg":
    process.runTTEffAna += process.TTEffAnalysisHLTPFTauHPS
    #process.runTTEffAna += process.TTEffAnalysisHLTPFTauTightHPS
    process.runTTEffAna += process.TTEffAnalysisHLTPFTauMediumHPS
#    process.runTTEffAna += process.TTEffAnalysisHLTPFTauMediumHPSL2Global
if analysis == "MetLeg":
#    process.runTTEffAna += process.kt6PFJets
#    process.runTTEffAna += process.producePFMETCorrections
    process.runTTEffAna += process.TTEffAnalysisMETLeg
####    if isData:
####	process.pfJetMETcorr.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")
if analysis == "QuadJet":
    process.runTTEffAna += process.TTEffAnalysisQuadJet

# The high purity selection (mainly for H+)
process.load("HiggsAnalysis.TriggerEfficiency.HighPuritySelection_cff")
import HiggsAnalysis.TriggerEfficiency.HighPuritySelection_cff as HighPurity
highPurityCounters = additionalCounters
highPurityCounters.extend(HighPurity.getSelectionCounters())
process.TTEffAnalysisHLTPFTauHPSHighPurity = process.TTEffAnalysisHLTPFTauHPS.clone(
    LoopingOver = "selectedPatTausHpsPFTauHighPurity",
    MuonSource = "selectedPatMuonsHighPurity",
    MuonTauPairSource = "muTauPairsHighPurity",
    Counters = cms.VInputTag([cms.InputTag(c) for c in highPurityCounters]),
    outputFileName = "tteffAnalysis-hltpftau-hpspftau-highpurity.root"
)
process.runTTEffAnaHighPurity = cms.Path(
    process.commonSequence +
    process.highPuritySequence +
    process.TTEffAnalysisHLTPFTauHPSHighPurity
)

# L1 emulator
process.L1simulation_step = cms.Path()
if runL1Emulator:
    if isData:
        process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
    else:
        process.load('Configuration.StandardSequences.RawToDigi_cff')
    process.L1simulation_step = cms.Path(
        process.RawToDigi *
        process.SimL1Emulator
    )
    import L1Trigger.Configuration.customise_l1EmulatorFromRaw as l1emulator
    l1emulator.customise(process)

    process.l1emuL1extraParticles = process.hltL1extraParticles.clone(
        muonSource = cms.InputTag( 'simGmtDigis' ),
        isolatedEmSource = cms.InputTag( 'simGctDigis','isoEm' ),
        nonIsolatedEmSource = cms.InputTag( 'simGctDigis','nonIsoEm' ),
        centralJetSource = cms.InputTag( 'simGctDigis','cenJets' ),
        forwardJetSource = cms.InputTag( 'simGctDigis','forJets' ),
        tauJetSource = cms.InputTag( 'simGctDigis','tauJets' ),
        etTotalSource = cms.InputTag( 'simGctDigis' ),
        etHadSource = cms.InputTag( 'simGctDigis' ),
        etMissSource = cms.InputTag( 'simGctDigis' )
    )
    process.l1emuL1GtObjectMap = process.hltL1GtObjectMap.clone(
        GmtInputTag = "simGmtDigis",
        GctInputTag = "simGctDigis"
    )
    process.L1simulation_step *= (process.l1emuL1extraParticles *
                                  process.l1emuL1GtObjectMap)


    def setL1Emu(module):
        module.L1extraTauJetSource = cms.InputTag("l1emuL1extraParticles", "Tau")
        module.L1extraCentralJetSource = cms.InputTag("l1emuL1extraParticles", "Central")
        module.L1extraMETSource = cms.InputTag("l1emuL1extraParticles", "MET")
        module.L1extraMHTSource = cms.InputTag("l1emuL1extraParticles", "MHT")
        module.L1CaloRegionSource = "simRctDigis"
        module.L1GtReadoutRecord = "simGtDigis"
        module.L1GtObjectMapRecord = "l1emuL1GtObjectMap"

    process.TEffAnalysisHLTPFTauTightHPSL1Emu = process.TTEffAnalysisHLTPFTauTightHPS.clone(
        outputFileName = "tteffAnalysis-hltpftautight-hpspftau-l1emu.root"
    )
    setL1Emu(process.TEffAnalysisHLTPFTauTightHPSL1Emu)
    process.runTTEffAna += process.TEffAnalysisHLTPFTauTightHPSL1Emu

    process.TTEffAnalysisHLTPFTauTightHPSHighPurityL1Emu = process.TTEffAnalysisHLTPFTauTightHPSHighPurity.clone(
        outputFileName = "tteffAnalysis-hltpftautight-hpspftau-l1emu-highpurity.root"
    )
    setL1Emu(process.TTEffAnalysisHLTPFTauTightHPSHighPurityL1Emu)
    process.runTTEffAnaHighPurity *= process.TTEffAnalysisHLTPFTauTightHPSHighPurityL1Emu

process.o1 = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring("keep *"),
    fileName = cms.untracked.string('cmssw.root')
)
#process.outpath = cms.EndPath(process.o1)

process.HLTPFTauSequence+= process.hltPFTausTightIso
process.DoMiscHLT = cms.Path(process.hltPFMHTProducer)

process.schedule = cms.Schedule(
#    process.runMETCleaning,
    process.runTTEffAna,
    process.runTTEffAnaHighPurity
#    ,process.outpath
)
if analysis == "MetLeg" or analysis == "QuadJet":
    process.schedule = cms.Schedule(
        process.runTTEffAna
#	,process.outpath
    )
if runOpenHLT:
    process.schedule = cms.Schedule(process.DoHLTJets,
#				process.DoHltMuon,
				process.DoHLTPhoton,
				process.DoHLTElectron,
				process.DoHLTTau,
				process.DoHLTMinBiasPixelTracks,
                                process.DoMiscHLT,
				process.runMETCleaning,
                                process.L1simulation_step,
				process.runTTEffAna,
#                                process.runTTEffAnaHighPurity
#				process.outpath
)

if not dataVersion.isMC():
#if isData:  # replace all instances of "rawDataCollector" with "source" in In$
    from FWCore.ParameterSet import Mixins
    for module in process.__dict__.itervalues():
        if isinstance(module, Mixins._Parameterizable):
            for parameter in module.__dict__.itervalues():
                if isinstance(parameter, cms.InputTag):
                    if parameter.moduleLabel == 'rawDataCollector':
                        parameter.moduleLabel = 'source'

