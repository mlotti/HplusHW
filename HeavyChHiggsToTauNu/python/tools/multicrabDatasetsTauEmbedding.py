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


    datasets["Mu_135821-144114"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/Mu/local-Run2010A_Nov4ReReco_v1_RECO_tauembedding_skim_v5-d9acfcd152bd91559f102d8a462838a1/USER",
        "number_of_jobs": 7 # ~100 ev/job
    }
    datasets["Mu_146240-147116"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/Mu/local-Run2010B_Nov4ReReco_v1_RECO_tauembedding_skim_v5-d9acfcd152bd91559f102d8a462838a1/USER",
        "number_of_jobs": 12 # ~100 ev/job
    }
    datasets["Mu_147196-149442"]["data"]["tauembedding_skim_v5"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/Mu/local-Run2010B_Nov4ReReco_v1_RECO_tauembedding_skim_v5-1b92bf46a5f97420ad6d4abe5c819f95/USER",
        "number_of_jobs": 70 # ~100 ev/job
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

