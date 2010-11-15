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
