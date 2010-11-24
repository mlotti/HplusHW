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
