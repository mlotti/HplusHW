import multicrabDatasetsCommon as common

def addTo(datasets):
    datasets["Mu_146240-147116"]["data"]["tauembedding_skim_v2"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/Mu/local-Run2010B_PromptReco_v2_AOD_tauembedding_skim_v2-df8d5a0675762f7704edd4730bf7a6a7/USER",
        "number_of_jobs": 1
    }

    datasets["WJets"]["data"]["tauembedding_skim_v2"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v2-52e54222a22093cabccf53a197393901/USER",
        "number_of_jobs": 10
    }
    datasets["WJets"]["data"]["tauembedding_generation_v2"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJets_7TeV-madgraph-tauola/local-local_Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v2_52e54222a22093cabccf53a197393901_USER_tauembedding_generation_v2-30de4d1810b82a43ef34b86cea04d93e/USER",
        "number_of_jobs": 2
    }
    datasets["WJets"]["data"]["tauembedding_embedding_v2"] = {
        "dbs_url": common.pattuple_dbs,
        "datasetpath": "/WJets_7TeV-madgraph-tauola/local-local_local_Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v2_52e54222a22093cabccf53a197393901_USER_tauembedding_generation_v2_30de4d1810b82a43ef34b86cea04d93e_USER_tauembedding_embedding_v2-ed6563e15d1b423a9bd5d11109ca1e30/USER",
        "number_of_jobs": 2
    }
