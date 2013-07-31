from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTools import TaskDef
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTriggerEff import addTauLegSkim_53X,addMetLegSkim_53X,addQuadJetSkim_53X

#skimVersion = "V00_12_03_CMSSW537_v1"
#skimVersion = "V00_12_05_CMSSW537p6_v1"
skimVersion = "V53_3_CMSSW539p3_v2"

def addTauLegSkim(datasets):
    definitions = {
	"TauPlusX_190456-193621_2012A_Jan22":				TaskDef("/TauPlusX/local-Run2012A_22Jan2013_v1_AOD_190456_193621_triggerTauLeg_skim_v53_v3-ab0edd69780ab754cbf6aaa760343e0e/USER"),
	"TauPlusX_193834-196531_2012B_Jan22":     			TaskDef("/TauPlusX/local-Run2012B_22Jan2013_v1_AOD_193834_196531_triggerTauLeg_skim_v53_v3-90dde5f694db916cf2ea3dc4c540f69c/USER"),
	"TauPlusX_198022-203742_2012C_Jan22":     			TaskDef("/TauPlusX/local-Run2012C_22Jan2013_v1_AOD_198022_203742_triggerTauLeg_skim_v53_v3-9deb66986c607f9bebda7c7c1c86e94c/USER"),
	"TauPlusX_203777-208686_2012D_Jan22":     			TaskDef("/TauPlusX/local-Run2012D_22Jan2013_v1_AOD_203777_208686_triggerTauLeg_skim_v53_v3-f62bc98791684c36f1551d5d5c8e780d/USER"),

        "DYToTauTau_M_20_CT10_TuneZ2star_powheg_tauola_Summer12":       TaskDef("/DYToTauTau_M-20_CT10_TuneZ2star_8TeV-powheg-tauola-pythia6/local-Summer12_DR53X_PU_S8_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
	"DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12":    TaskDef("/DYToTauTau_M-20_CT10_TuneZ2star_v2_8TeV-powheg-tauola-pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),

        "QCD_Pt30to50_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt50to80_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt80to120_TuneZ2star_Summer12":            TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt120to170_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt170to300_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt300to470_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),

        "WW_TuneZ2star_Summer12":                       TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "WZ_TuneZ2star_Summer12":                       TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "ZZ_TuneZ2star_Summer12":                       TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "TTJets_TuneZ2star_Summer12":                   TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "WJets_TuneZ2star_v1_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "WJets_TuneZ2star_v2_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "W1Jets_TuneZ2star_Summer12":                   TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "W2Jets_TuneZ2star_Summer12":                   TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "W3Jets_TuneZ2star_Summer12":                   TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "W4Jets_TuneZ2star_Summer12":                   TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "DYJetsToLL_M50_TuneZ2star_Summer12":           TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12":       TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        
        "T_t-channel_TuneZ2star_Summer12":              TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "Tbar_t-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "T_tW-channel_TuneZ2star_Summer12":             TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "Tbar_tW-channel_TuneZ2star_Summer12":          TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "T_s-channel_TuneZ2star_Summer12":              TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "Tbar_s-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
    }                                                                                                                             
                                                                                                                                  
    addTauLegSkim_53X(skimVersion, datasets, definitions)

def addTauLegSkim_V00_12_05_CMSSW537p6_v1(datasets):
    definitions = {
        "TauPlusX_190456-193621_2012A_Jan22":       			TaskDef("/TauPlusX/local-Run2012A_22Jan2013_v1_AOD_190456_193621_triggerTauLeg_skim_v53_v3-ab0edd69780ab754cbf6aaa760343e0e/USER"),
        "TauPlusX_193834-196531_2012B_Jan22":       			TaskDef("/TauPlusX/local-Run2012B_22Jan2013_v1_AOD_193834_196531_triggerTauLeg_skim_v53_v3-90dde5f694db916cf2ea3dc4c540f69c/USER"),
        "TauPlusX_198022-203742_2012C_Jan22":       			TaskDef("/TauPlusX/local-Run2012C_22Jan2013_v1_AOD_198022_203742_triggerTauLeg_skim_v53_v3-9deb66986c607f9bebda7c7c1c86e94c/USER"),
        "TauPlusX_203777-208686_2012D_Jan22":                           TaskDef("/TauPlusX/local-Run2012D_22Jan2013_v1_AOD_203777_208686_triggerTauLeg_skim_v53_v3-f62bc98791684c36f1551d5d5c8e780d/USER"),

        "DYToTauTau_M_20_CT10_TuneZ2star_powheg_tauola_Summer12":       TaskDef("/DYToTauTau_M-20_CT10_TuneZ2star_8TeV-powheg-tauola-pythia6/local-Summer12_DR53X_PU_S8_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
        "DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12":    TaskDef("/DYToTauTau_M-20_CT10_TuneZ2star_v2_8TeV-powheg-tauola-pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v3-bec3178d66007202ae729a1677c5df02/USER"),
    }

    addTauLegSkim_53X(skimVersion, datasets, definitions)

def addTauLegSkim_V00_12_05_CMSSW537p6_v1(datasets):
    definitions = {
        "TauPlusX_190456-190738_2012A_Jul13":                           TaskDef("/TauPlusX/local-Run2012A_13Jul2012_v1_AOD_190456_190738_triggerTauLeg_skim_v53_v2-3ca67b5668ffc41c3fc637191cd01817/USER"),
        "TauPlusX_190782-190949_2012A_Aug06":                           TaskDef("/TauPlusX/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_triggerTauLeg_skim_v53_v2-4a0e265274a3a3c62fcbddf6d3f521be/USER"),
        "TauPlusX_191043-193621_2012A_Jul13":                           TaskDef("/TauPlusX/local-Run2012A_13Jul2012_v1_AOD_191043_193621_triggerTauLeg_skim_v53_v2-4a0e265274a3a3c62fcbddf6d3f521be/USER"),
        "TauPlusX_193834-196531_2012B_Jul13":                           TaskDef("/TauPlusX/local-Run2012B_13Jul2012_v1_AOD_193834_196531_triggerTauLeg_skim_v53_v2-663eba0a1a1c787b38ec317ab3b7fbc4/USER"),
        "TauPlusX_198022-198523_2012C_Aug24":                           TaskDef("/TauPlusX/local-Run2012C_24Aug2012_v1_AOD_198022_198523_triggerTauLeg_skim_v53_v2-744e53f03db2187c746febe32d910383/USER"),
        "TauPlusX_198941-199608_2012C_Prompt":                          TaskDef("/TauPlusX/local-Run2012C_PromptReco_v2_AOD_198941_199608_triggerTauLeg_skim_v53_v2-0201062118f04784a4143f7133fbc494/USER"),
        "TauPlusX_199698-203742_2012C_Prompt":                          TaskDef("/TauPlusX/local-Run2012C_PromptReco_v2_AOD_199698_203742_triggerTauLeg_skim_v53_v2-9d3ec449a3910d6ec6611ff095d9eeb8/USER"),
        "TauPlusX_203777-208686_2012D_Prompt":                          TaskDef("/TauPlusX/local-Run2012D_PromptReco_v1_AOD_203777_208686_triggerTauLeg_skim_v53_v2-9d3ec449a3910d6ec6611ff095d9eeb8/USER"),

        "DYToTauTau_M_20_CT10_TuneZ2star_powheg_tauola_Summer12":       TaskDef("/DYToTauTau_M-20_CT10_TuneZ2star_8TeV-powheg-tauola-pythia6/local-Summer12_DR53X_PU_S8_START53_V7A_v1_AODSIM_triggerTauLeg_skim_v53_v2-8728052812930676480ae2a242229ec9/USER"),
        "DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12":    TaskDef("/DYToTauTau_M-20_CT10_TuneZ2star_v2_8TeV-powheg-tauola-pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerTauLeg_skim_v53_v2-8728052812930676480ae2a242229ec9/USER"),
    }

    addTauLegSkim_53X(skimVersion, datasets, definitions)

def addMetLegSkim_CaloMETCorr(datasets):
    definitions = {
        "Tau_190456-193621_2012A_Jan22":                TaskDef("/Tau/local-Run2012A_22Jan2013_v1_AOD_190456_193621_triggerMetLeg_skim_v53_3c-5f19905a1c0c96f32d768336134dd1cc/USER"),
        "TauParked_193834-196531_2012B_Jan22":          TaskDef("/TauParked/local-Run2012B_22Jan2013_v1_AOD_193834_196531_triggerMetLeg_skim_v53_3c-132d8eee399ddeed0a387ede14aa8b8b/USER"),
        "TauParked_198022-202504_2012C_Jan22":          TaskDef("/TauParked/local-Run2012C_22Jan2013_v1_AOD_198022_202504_triggerMetLeg_skim_v53_3c-9b68e225c5babe62a4656316fe1be8d5/USER"),
        "TauParked_202972-203742_2012C_Jan22":          TaskDef("/TauParked/local-Run2012C_22Jan2013_v1_AOD_202972_203742_triggerMetLeg_skim_v53_3c-65583ace3198f0f55b2cd7d093b9f259/USER"),
        "TauParked_203777-208686_2012D_Jan22":          TaskDef("/TauParked/local-Run2012D_22Jan2013_v1_AOD_203777_208686_triggerMetLeg_skim_v53_3c-65583ace3198f0f55b2cd7d093b9f259/USER"),
                                                                                                                                                                              
        "QCD_Pt30to50_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt50to80_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt80to120_TuneZ2star_Summer12":            TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt120to170_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt170to300_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt300to470_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
                                                                                                                                                                              
        "WW_TuneZ2star_Summer12":                       TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "WZ_TuneZ2star_Summer12":                       TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "ZZ_TuneZ2star_Summer12":                       TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "TTJets_TuneZ2star_Summer12":                   TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "WJets_TuneZ2star_v1_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "WJets_TuneZ2star_v2_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "W1Jets_TuneZ2star_Summer12":                   TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "W2Jets_TuneZ2star_Summer12":                   TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "W3Jets_TuneZ2star_Summer12":                   TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "W4Jets_TuneZ2star_Summer12":                   TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "DYJetsToLL_M50_TuneZ2star_Summer12":           TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12":       TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
                                                                                                                                                                              
        "T_t-channel_TuneZ2star_Summer12":              TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "Tbar_t-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "T_tW-channel_TuneZ2star_Summer12":             TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "Tbar_tW-channel_TuneZ2star_Summer12":          TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "T_s-channel_TuneZ2star_Summer12":              TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER"),
        "Tbar_s-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_3c-43dc92c0c207b3c8306900dc42897adc/USER")
    }

    addMetLegSkim_53X(skimVersion, datasets, definitions)

def addMetLegSkim(datasets):
    definitions = {
	"Tau_190456-193621_2012A_Jan22": 		TaskDef("/Tau/local-Run2012A_22Jan2013_v1_AOD_190456_193621_triggerMetLeg_skim_v53_v3-56beb3a2e79a8b14c82b89183fef0535/USER"),
	"TauParked_193834-196531_2012B_Jan22":		TaskDef("/TauParked/local-Run2012B_22Jan2013_v1_AOD_193834_196531_triggerMetLeg_skim_v53_v3-91526bc7daeb9a1da9e649cb639be3ec/USER"),
	"TauParked_198022-202504_2012C_Jan22": 		TaskDef("/TauParked/local-Run2012C_22Jan2013_v1_AOD_198022_202504_triggerMetLeg_skim_v53_v3-9f113b1ddfbc3e3d4f22dcd2477c6dfc/USER"),
	"TauParked_202972-203742_2012C_Jan22":		TaskDef("/TauParked/local-Run2012C_22Jan2013_v1_AOD_202972_203742_triggerMetLeg_skim_v53_v3-21138ca7d5b6f45d688be5148bf48f97/USER"),
	"TauParked_203777-208686_2012D_Jan22":		TaskDef("/TauParked/local-Run2012D_22Jan2013_v1_AOD_203777_208686_triggerMetLeg_skim_v53_v3-21138ca7d5b6f45d688be5148bf48f97/USER"),

        "QCD_Pt30to50_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt50to80_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt80to120_TuneZ2star_Summer12":            TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt120to170_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt170to300_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt300to470_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),

        "WW_TuneZ2star_Summer12":                       TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "WZ_TuneZ2star_Summer12":                       TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "ZZ_TuneZ2star_Summer12":                       TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "TTJets_TuneZ2star_Summer12":                   TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "WJets_TuneZ2star_v1_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "WJets_TuneZ2star_v2_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "W1Jets_TuneZ2star_Summer12":                   TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "W2Jets_TuneZ2star_Summer12":                   TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "W3Jets_TuneZ2star_Summer12":                   TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "W4Jets_TuneZ2star_Summer12":                   TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "DYJetsToLL_M50_TuneZ2star_Summer12":           TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12":       TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),

        "T_t-channel_TuneZ2star_Summer12":              TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "Tbar_t-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "T_tW-channel_TuneZ2star_Summer12":             TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "Tbar_tW-channel_TuneZ2star_Summer12":          TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
        "T_s-channel_TuneZ2star_Summer12":              TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),                                    
        "Tbar_s-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v3-9377a1f4d9f2bf86d76a13a22516e937/USER"),
    }

    addMetLegSkim_53X(skimVersion, datasets, definitions)

def addMetLegSkim_V00_12_05_CMSSW537p6_v1(datasets):
    definitions = {
        "Tau_190456-190738_2012A_Jul13":                TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_190456_190738_triggerMetLeg_skim_v53_v2-213f3f77afa722905dc0ce5ce7597bca/USER"),
        "Tau_190782-190949_2012A_Aug06":                TaskDef("/Tau/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_triggerMetLeg_skim_v53_v2-0e21f8367f184cd38d906ca6ced7b830/USER"),
        "Tau_191043-193621_2012A_Jul13":                TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_191043_193621_triggerMetLeg_skim_v53_v2-62478b3be0d9ff7809b16dff1575cafa/USER"),
        "Tau_193834-196531_2012B_Jul13":                TaskDef("/Tau/local-Run2012B_13Jul2012_v1_AOD_193834_196531_triggerMetLeg_skim_v53_v2-1e56d0198e950718da01ef6c534d1a08/USER"),
        "Tau_198022-198523_2012C_Aug24":                TaskDef("/Tau/local-Run2012C_24Aug2012_v1_AOD_198022_198523_triggerMetLeg_skim_v53_v2-e60f6c72afa479d1fe2c6961810cbbfe/USER"),
        "Tau_198941-200601_2012C_Prompt":               TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_198941_200601_triggerMetLeg_skim_v53_v2-7eacfb6ed5a0df48331061e03d5fe86e/USER"),
        "Tau_200961-202504_2012C_Prompt":               TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_200961_202504_triggerMetLeg_skim_v53_v2-095e5d8c31759686e6fb7203de4796b0/USER"),
        "Tau_202792-203742_2012C_Prompt":               TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_202792_203742_triggerMetLeg_skim_v53_v2-a6d3d28828969820827adc8b02337486/USER"),
        "Tau_203777-208686_2012D_Prompt":               TaskDef("/Tau/local-Run2012D_PromptReco_v1_AOD_203777_208686_triggerMetLeg_skim_v53_v2-a6d3d28828969820827adc8b02337486/USER"),
        
        "QCD_Pt30to50_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt50to80_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt80to120_TuneZ2star_Summer12":            TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt120to170_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt170to300_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt300to470_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        
        "WW_TuneZ2star_Summer12":                       TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "WZ_TuneZ2star_Summer12":                       TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "ZZ_TuneZ2star_Summer12":                       TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "TTJets_TuneZ2star_Summer12":                   TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "WJets_TuneZ2star_v1_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "WJets_TuneZ2star_v2_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "W1Jets_TuneZ2star_Summer12":                   TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "W2Jets_TuneZ2star_Summer12":                   TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "W3Jets_TuneZ2star_Summer12":                   TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "W4Jets_TuneZ2star_Summer12":                   TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "DYJetsToLL_M50_TuneZ2star_Summer12":           TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12":       TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "T_t-channel_TuneZ2star_Summer12":              TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "Tbar_t-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "T_tW-channel_TuneZ2star_Summer12":             TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "Tbar_tW-channel_TuneZ2star_Summer12":          TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "T_s-channel_TuneZ2star_Summer12":              TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
        "Tbar_s-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_triggerMetLeg_skim_v53_v2-81c88d482dfcc6722e719d6aad502c85/USER"),
    }
        
    addMetLegSkim_53X(skimVersion, datasets, definitions)

def addMetLegSkim_V00_12_03_CMSSW537_v1(datasets):
    definitions = {
	"Tau_190456-190738_2012A_Jul13":		TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_190456_190738_analysis_metleg_v53_v1-165ff7ea0b6b7dc6426443c42f2a9122/USER"),
	"Tau_190782-190949_2012A_Aug06":             	TaskDef("/Tau/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_analysis_metleg_v53_v1-de59482928f61dc06955dcb204f66afe/USER"),
	"Tau_191043-193621_2012A_Jul13":             	TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_191043_193621_analysis_metleg_v53_v1-43665de791ab95ebca4e518ee6c20319/USER"),
	"Tau_193834-196531_2012B_Jul13":             	TaskDef("/Tau/local-Run2012B_13Jul2012_v1_AOD_193834_196531_analysis_metleg_v53_v1-24eee222e7d7579368f51155ee8c17c1/USER"),
	"Tau_198022-198523_2012C_Aug24":             	TaskDef("/Tau/local-Run2012C_24Aug2012_v1_AOD_198022_198523_analysis_metleg_v53_v1-16cf49e1333af46ec078168d0a11d2bc/USER"),
	"Tau_198941-200601_2012C_Prompt":             	TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_198941_200601_analysis_metleg_v53_v1-7a1c0e3252a37dec457bef41ab89bd2b/USER"),
	"Tau_200961-202504_2012C_Prompt":             	TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_200961_202504_analysis_metleg_v53_v1-fe7b61f7d8aa75fa2fdc2671653816c0/USER"),
	"Tau_202792-203742_2012C_Prompt":             	TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_202792_203742_analysis_metleg_v53_v1-122fb14a264e8e421d259fc9ade8407a/USER"),
	"Tau_203777-208686_2012D_Prompt":             	TaskDef("/Tau/local-Run2012D_PromptReco_v1_AOD_203777_208686_analysis_metleg_v53_v1-4edeba655e16935bfbce88d52178887d/USER"),

	"QCD_Pt30to50_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt50to80_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt80to120_TuneZ2star_Summer12":            TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt120to170_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt170to300_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt170to300_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt300to470_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt300to470_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"QCD_Pt300to470_TuneZ2star_v3_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),

	"WW_TuneZ2star_Summer12":             		TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"WZ_TuneZ2star_Summer12":             		TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"ZZ_TuneZ2star_Summer12":             		TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"TTJets_TuneZ2star_Summer12":           	TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"WJets_TuneZ2star_v1_Summer12":         	TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"WJets_TuneZ2star_v2_Summer12":         	TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"W1Jets_TuneZ2star_Summer12":           	TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"W2Jets_TuneZ2star_Summer12":           	TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"W3Jets_TuneZ2star_Summer12":           	TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"W4Jets_TuneZ2star_Summer12":           	TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"DYJetsToLL_M50_TuneZ2star_Summer12":           TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"DYJetsToLL_M10to50_TuneZ2star_Summer12":	TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"T_t-channel_TuneZ2star_Summer12":             	TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"Tbar_t-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"T_tW-channel_TuneZ2star_Summer12":             TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"Tbar_tW-channel_TuneZ2star_Summer12":          TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"T_s-channel_TuneZ2star_Summer12":             	TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
	"Tbar_s-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
    }

    addMetLegSkim_53X(skimVersion, datasets, definitions)


def addQuadJetSkim(datasets):
    definitions = {

        "QCD_Pt30to50_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt50to80_TuneZ2star_Summer12":             TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt80to120_TuneZ2star_Summer12":            TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt120to170_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt170to300_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt300to470_TuneZ2star_Summer12":           TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":        TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),

#       "WW_TuneZ2star_Summer12":                       TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
#       "WZ_TuneZ2star_Summer12":                       TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
#       "ZZ_TuneZ2star_Summer12":                       TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_metleg_v53_v1-638a70bdbf1f7414f9f442a75689ed2b/USER"),
        "TTJets_TuneZ2star_Summer12":                   TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "WJets_TuneZ2star_v1_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "WJets_TuneZ2star_v2_Summer12":                 TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "W1Jets_TuneZ2star_Summer12":                   TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "W3Jets_TuneZ2star_Summer12":                   TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "W2Jets_TuneZ2star_Summer12":                   TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "W4Jets_TuneZ2star_Summer12":                   TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "DYJetsToLL_M50_TuneZ2star_Summer12":           TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12":       TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "T_t-channel_TuneZ2star_Summer12":              TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "Tbar_t-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "T_tW-channel_TuneZ2star_Summer12":             TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "Tbar_tW-channel_TuneZ2star_Summer12":          TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "T_s-channel_TuneZ2star_Summer12":              TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),
        "Tbar_s-channel_TuneZ2star_Summer12":           TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_analysis_quadjetleg_v53_v1-62bd3915f912e9f9a79b2505deb22977/USER"),

        "SingleMu_190456-190738_2012A_Jul13":           TaskDef("/SingleMu/local-Run2012A_13Jul2012_v1_AOD_190456_190738_triggerQuadJet_skim_v53_v1-4e187338c8491ab8d4532aa337c0330b/USER"),
        "SingleMu_190782-190949_2012A_Aug06":           TaskDef("/SingleMu/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_triggerQuadJet_skim_v53_v1-4a991cfb02214d9a059671d3ed8e570c/USER"),
        "SingleMu_191043-193621_2012A_Jul13":           TaskDef("/SingleMu/local-Run2012A_13Jul2012_v1_AOD_191043_193621_triggerQuadJet_skim_v53_v1-85bd6cc806f9a5f3fe08b681e571cf08/USER"),
        "SingleMu_193834-196531_2012B_Jul13":           TaskDef(""),
        "SingleMu_198022-198523_2012C_Aug24":           TaskDef("/SingleMu/local-Run2012C_24Aug2012_v1_AOD_198022_198523_triggerQuadJet_skim_v53_v1-18ccba83a5f3551c140a84815c942852/USER"),
        "SingleMu_198941-199608_2012C_Prompt":          TaskDef("/SingleMu/local-Run2012C_PromptReco_v2_AOD_198941_199608_triggerQuadJet_skim_v53_v1-ea00fdab66c8ad87fea336fe735365a2/USER"),
        "SingleMu_199698-202504_2012C_Prompt":          TaskDef(""),
        "SingleMu_202970-203742_2012C_Prompt":          TaskDef("/SingleMu/local-Run2012C_PromptReco_v2_AOD_202970_203742_triggerQuadJet_skim_v53_v1-069b1dba0f3e9f837438e4e74bdf8d37/USER"),
        "SingleMu_203777-208686_2012D_Prompt":          TaskDef(""),
    }

    addQuadJetSkim_53X(skimVersion, datasets, definitions)
