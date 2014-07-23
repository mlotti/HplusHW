# Generated on Thu Nov 29 13:47:54 2012 by multicrabDatasetsCfgCreator.py 
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTools import TaskDef
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTriggerEff import addTauLegSkim_44X,addMetLegSkim_44X

skimVersion = "v44_v5_CMSSW445_v1"

def addTauLegSkim_v44_v5(datasets):
    definitions = {
        "SingleMu_165970-167913_2011A_Nov08_RAWRECO":     TaskDef("/SingleMu/local-Pattuple_v447_v2_SingleMu_165970-167913_2011A_Nov08_RAWRECO-c2fceaf17541a3727dcd188db4ac87bb/USER"),
        "SingleMu_170722-173198_2011A_Nov08_RAWRECO":     TaskDef("/SingleMu/local-Pattuple_v447_v2_SingleMu_170722-173198_2011A_Nov08_RAWRECO-c2fceaf17541a3727dcd188db4ac87bb/USER"),
        "SingleMu_173236-173692_2011A_Nov08_RAWRECO":     TaskDef("/SingleMu/local-Pattuple_v447_v2_SingleMu_173236-173692_2011A_Nov08_RAWRECO-c2fceaf17541a3727dcd188db4ac87bb/USER"),
        "SingleMu_175832-180252_2011B_Nov19_RAWRECO":     TaskDef("/SingleMu/local-Pattuple_v447_v2_SingleMu_175832-180252_2011B_Nov19_RAWRECO-c2fceaf17541a3727dcd188db4ac87bb/USER"),

#        "DYJetsToLL_TuneZ2_MPIoff_M50_7TeV_madgraph_tauola_GENRAW": TaskDef("/DYJetsToLL_TuneZ2_MPIoff_M-50_7TeV-madgraph-tauola/local-pattuple_v25bfix_TTEffSkim_DYJetsToLL_TuneZ2_MPIoff_M50_7TeV_madgraph_tauola_GENRAW-7cc2aee836bd13479c6162f567a9f02e/USER"),
	"DYToTauTau_M20_CT10_TuneZ2_7TeV_powheg_pythia_tauola_TTEffSkim_v447_v1": TaskDef("/DYToTauTau_M-20_CT10_TuneZ2_7TeV-powheg-pythia-tauola/local-Pattuple_v447_v1_DYToTauTau_M20_CT10_TuneZ2_7TeV_powheg_pythia_tauola_GENRAW-6ea86f9382cabec5be838e8d7ccbdd3c/USER"),
    }

    addTauLegSkim_44X(skimVersion, datasets, definitions)

def addMetLegSkim_v44_v5(datasets):
    definitions = {
        "Tau_165970-167913_2011A_Nov08":          TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_165970_167913_triggerMetLeg_skim_v44_v5-f9a55c21c2e0744a8a120b83f0dd2316/USER"),
        "Tau_170722-173198_2011A_Nov08":          TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_170722_173198_triggerMetLeg_skim_v44_v5-16b2920db34657f1b4c8e746a65635c4/USER"),
        "Tau_173236-173692_2011A_Nov08":          TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_173236_173692_triggerMetLeg_skim_v44_v5-46c617c0ab2c127c57890c12c286f579/USER"),
        "Tau_175832-180252_2011B_Nov19":          TaskDef("/Tau/local-Run2011B_19Nov2011_v1_AOD_175832_180252_triggerMetLeg_skim_v44_v5-428837ef15cd9a9f94b001400f1034d7/USER"),

#	"DYJetsToLL_M-10To50_TuneZ2_Fall11":      TaskDef("/DYJetsToLL_M-10To50_TuneZ2_7TeV-madgraph/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "DYJetsToLL_M50_TuneZ2_Fall11":           TaskDef("/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "QCD_Pt120to170_TuneZ2_Fall11":           TaskDef("/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "QCD_Pt170to300_TuneZ2_Fall11":           TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "QCD_Pt300to470_TuneZ2_Fall11":           TaskDef("/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "QCD_Pt30to50_TuneZ2_Fall11":             TaskDef("/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "QCD_Pt50to80_TuneZ2_Fall11":             TaskDef("/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "QCD_Pt80to120_TuneZ2_Fall11":            TaskDef("/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "TTJets_TuneZ2_Fall11":                   TaskDef("/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "T_s-channel_TuneZ2_Fall11":              TaskDef("/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "T_t-channel_TuneZ2_Fall11":              TaskDef("/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "T_tW-channel_TuneZ2_Fall11":             TaskDef("/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "Tbar_s-channel_TuneZ2_Fall11":           TaskDef("/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "Tbar_t-channel_TuneZ2_Fall11":           TaskDef("/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "Tbar_tW-channel_TuneZ2_Fall11":          TaskDef("/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "W2Jets_TuneZ2_Fall11":                   TaskDef("/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "W3Jets_TuneZ2_Fall11":                   TaskDef("/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v2_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "W4Jets_TuneZ2_Fall11":                   TaskDef("/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "WJets_TuneZ2_Fall11":                    TaskDef("/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "WW_TuneZ2_Fall11":                       TaskDef("/WW_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "WZ_TuneZ2_Fall11":                       TaskDef("/WZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
        "ZZ_TuneZ2_Fall11":                       TaskDef("/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_triggerMetLeg_skim_v44_v5-61ebb3092efc504522b10118087ff38f/USER"),
    }

    addMetLegSkim_44X(skimVersion, datasets, definitions)

def addMetLegSkim_V00_10_11_CMSSW445_v4(datasets):
    definitions = {
        "Tau_165970-167913_2011A_Nov08":          TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_Tau_165970-167913_2011A_Nov08-6622fb303c37fbff7f780987cd32ef79/USER"),
        "Tau_170722-173198_2011A_Nov08":          TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_Tau_170722-173198_2011A_Nov08-34206e622a65128e416942acdeb84d11/USER"),
        "Tau_173236-173692_2011A_Nov08":          TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_Tau_173236-173692_2011A_Nov08-00ca2619f609574ec52af16eab2d2a3c/USER"),
        "Tau_175832-180252_2011B_Nov19":          TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_Tau_175832-180252_2011B_Nov19-3f33223e665aae41ac3a174ca8d4a2d9/USER"),

#	"DYJetsToLL_M-10To50_TuneZ2_Fall11":      TaskDef("/DYJetsToLL_M-10To50_TuneZ2_7TeV-madgraph/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_DYJetsToLL_M10to50_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "DYJetsToLL_M50_TuneZ2_Fall11":           TaskDef("/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_DYJetsToLL_M50_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "QCD_Pt120to170_TuneZ2_Fall11":           TaskDef("/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_QCD_Pt120to170_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "QCD_Pt170to300_TuneZ2_Fall11":           TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_QCD_Pt170to300_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "QCD_Pt300to470_TuneZ2_Fall11":           TaskDef("/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_QCD_Pt300to470_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "QCD_Pt30to50_TuneZ2_Fall11":             TaskDef("/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_QCD_Pt30to50_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "QCD_Pt50to80_TuneZ2_Fall11":             TaskDef("/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_QCD_Pt50to80_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "QCD_Pt80to120_TuneZ2_Fall11":            TaskDef("/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_QCD_Pt80to120_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "TTJets_TuneZ2_Fall11":                   TaskDef("/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_TTJets_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "T_s-channel_TuneZ2_Fall11":              TaskDef("/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_T_s-channel_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "T_t-channel_TuneZ2_Fall11":              TaskDef("/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_T_t-channel_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "T_tW-channel_TuneZ2_Fall11":             TaskDef("/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_T_tW-channel_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "Tbar_s-channel_TuneZ2_Fall11":           TaskDef("/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_Tbar_s-channel_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "Tbar_t-channel_TuneZ2_Fall11":           TaskDef("/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_Tbar_t-channel_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "Tbar_tW-channel_TuneZ2_Fall11":          TaskDef("/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_Tbar_tW-channel_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "W2Jets_TuneZ2_Fall11":                   TaskDef("/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_W2Jets_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "W3Jets_TuneZ2_Fall11":                   TaskDef("/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_W3Jets_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "W4Jets_TuneZ2_Fall11":                   TaskDef("/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_W4Jets_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "WJets_TuneZ2_Fall11":                    TaskDef("/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_WJets_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "WW_TuneZ2_Fall11":                       TaskDef("/WW_TuneZ2_7TeV_pythia6_tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_WW_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "WZ_TuneZ2_Fall11":                       TaskDef("/WZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_WZ_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
        "ZZ_TuneZ2_Fall11":                       TaskDef("/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_ZZ_TuneZ2_Fall11-b213557560c4d4efb319dea1726f2180/USER"),
    }

    addMetLegSkim_44X(skimVersion, datasets, definitions)
