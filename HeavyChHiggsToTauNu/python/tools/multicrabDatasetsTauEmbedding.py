import multicrabDatasetsCommon as common

def addTo(datasets):
    # datasets["Mu_146240-147116"]["data"]["tauembedding_skim_v2"] = {
    #     "dbs_url": common.pattuple_dbs,
    #     "datasetpath": "/Mu/local-Run2010B_PromptReco_v2_AOD_tauembedding_skim_v2-df8d5a0675762f7704edd4730bf7a6a7/USER",
    #     "number_of_jobs": 14
    # }
    # datasets["Mu_146240-147116"]["data"]["tauembedding_generation_v2"] = {
    #     "dbs_url": common.pattuple_dbs,
    #     "datasetpath": "/Mu/local-local-Run2010B_PromptReco_v2_AOD_tauembedding_generation_v2-82f01f8276126324da0436a1c37f3326/USER",
    #     "number_of_jobs": 14
    # }

    datasets["WJets"]["data"]["tauembedding_skim_v3"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v3-1e74944f713fc616dfdc12e43491e68c/USER",
        "number_of_jobs": 10
    }
    datasets["WJets"]["data"]["tauembedding_generation_v3"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJets_7TeV-madgraph-tauola/local-local-Summer10_START36_V9_S09_v1_AODSIM_tauembedding_generation_v3-9f5e22d4b16076b49568a537f31b168c/USER",
        "number_of_jobs": 10
    }
    datasets["WJets"]["data"]["tauembedding_embedding_v3_2"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM_tauembedding_embedding_v3_2-ed6563e15d1b423a9bd5d11109ca1e30/USER",
        "number_of_jobs": 5
    }
    datasets["WJets"]["data"]["tauembedding_embedding_v3_3"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM_tauembedding_embedding_v3_3-ed6563e15d1b423a9bd5d11109ca1e30/USER",
        "number_of_jobs": 5
    }


#    datasets[""]["data"]["tauembedding_skim_v5"] = {
#        "dbs_url": common.pattuple_dbs,
#        "datasetpath": "",
#        "number_of_jobs":  # ~100 ev/job
#    }

    datasets["Mu_135821-144114"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/Mu/local-Run2010A_Nov4ReReco_v1_RECO_135821_tauembedding_skim_v5-d9acfcd152bd91559f102d8a462838a1/USER",
        "number_of_jobs": 10 # ~100 ev/job
    }


    datasets["TTJets_PU"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_skim_v5-f0f5761dbef0a56e664c9bfa3bb2c570/USER",
        "number_of_jobs": 300 # ~500 ev/job
    }

    datasets["WJets_Fall10_PU"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_AODSIM_tauembedding_skim_v5-f0f5761dbef0a56e664c9bfa3bb2c570/USER",
        "number_of_jobs": 50 # ~200 ev/job
    }

    datasets["TToBLNu_s-channel_PU"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_skim_v5b-f0f5761dbef0a56e664c9bfa3bb2c570/USER",
        "number_of_jobs": 56 # ~100 ev/job
    }

    datasets["TToBLNu_t-channel_PU"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_skim_v5b-f0f5761dbef0a56e664c9bfa3bb2c570/USER",
        "number_of_jobs": 95 # ~100 ev/job
    }

    datasets["TToBLNu_tW-channel_PU"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_skim_v5b-f0f5761dbef0a56e664c9bfa3bb2c570/USER",
        "number_of_jobs": 68 # ~500 ev/job
    }

    datasets["QCD_Pt20_MuEnriched_PU"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_skim_v5-f0f5761dbef0a56e664c9bfa3bb2c570/USER",
        "number_of_jobs": 140 # ~400 ev/job
    }

    datasets["DYJetsToLL_PU"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_skim_v5-f0f5761dbef0a56e664c9bfa3bb2c570/USER",
        "number_of_jobs": 30 # ~200 ev/job
    }
    datasets["DYJetsToLL_PU"]["data"]["tauembedding_generation_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_generation_v5-9f5e22d4b16076b49568a537f31b168c/USER",
        "number_of_jobs": 30 # ~200 ev/job
    }
    datasets["DYJetsToLL_PU"]["data"]["tauembedding_embedding_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_embedding_v5-ed6563e15d1b423a9bd5d11109ca1e30/USER",
        "number_of_jobs": 30 # ~200 ev/job
    }
