import multicrabDatasetsCommon as common

# for generation (skim): ~1 kev ev/job
# for embedding (generation): ~5-10 kev/job
# for analysis (embedding): ~5-10 kev/job

def addTo(datasets):
#    datasets[""]["data"]["tauembedding_skim_v5"] = {
#        "dbs_url": common.pattuple_dbs,
#        "datasetpath": "",
#        "number_of_jobs":  # ~100 ev/job
#    }


################################################################################

    datasets["Mu_136035-144114_Dec22"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_skim_v9-6397f6a55608eebafbc76539fb48fc8d/USER",
                "number_of_jobs": 5#1 # ~3600 ev/job  #5 # ~600 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_generation_v9b_pt40-63a3abcff1280f0a104de095775cda8a/USER",
                "number_of_jobs": 1 # ~1200 ev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 1 # ~1200 ev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_generation_v9_pt30-9a329dd137bf629b37ee4df7ac809cdf/USER",
                "number_of_jobs": 1 # ~2700 ev/job
            },
            })
    datasets["Mu_146428-147116_Dec22"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_skim_v9-6397f6a55608eebafbc76539fb48fc8d/USER",
                "number_of_jobs": 10#2 # ~2500 ev/job #10 # ~500 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_generation_v9b_pt40-63a3abcff1280f0a104de095775cda8a/USER",
                "number_of_jobs": 1 # ~2100 ev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 1 # ~2100 ev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_generation_v9_pt30-9a329dd137bf629b37ee4df7ac809cdf/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["Mu_147196-149294_Dec22"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_skim_v9-6c79cc5a252f5183f923b05982b89b14/USER",
                "number_of_jobs": 25#5 # ~5500 ev/job #25 # ~1100 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_generation_v9b_pt40-63a3abcff1280f0a104de095775cda8a/USER",
                "number_of_jobs": 2 # ~6 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 1 # ~12 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_generation_v9_pt30-9a329dd137bf629b37ee4df7ac809cdf/USER",
                "number_of_jobs": 6 # ~5 kev/job
            },
            })
    datasets["SingleMu_160431-161016_Prompt"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_skim_v9-4067cec3a37dbb567632ac52f5e8496d/USER",
                "number_of_jobs": 5 # ~1 kev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_generation_v9_pt40-63a3abcff1280f0a104de095775cda8a/USER",
                "number_of_jobs": 1 # ~2.5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 1 # ~2.5 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_generation_v9_pt30-9a329dd137bf629b37ee4df7ac809cdf/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["SingleMu_162803-162828_Prompt"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_skim_v9-4067cec3a37dbb567632ac52f5e8496d/USER",
                "number_of_jobs": 5 # ~1 kev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_generation_v9_pt40-63a3abcff1280f0a104de095775cda8a/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_generation_v9_pt30-9a329dd137bf629b37ee4df7ac809cdf/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["SingleMu_162803-163261_Prompt"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_skim_v9_1b-09337ee4d42c2162b752fa4dfecfe7d8/USER",
                "number_of_jobs": 20 # ~1 kev/job
            },
            })
    datasets["SingleMu_163270-163369_Prompt"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_163270_tauembedding_skim_v9_1b-12c8c1dfda9f2afe10c3d45e706200ed/USER",
                "number_of_jobs": 20 # ~1 kev/job
            },
            })

    
    datasets["WJets_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 50#10 # ~5500 ev/job #50 # ~1100 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 8 # ~5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 4 # ~10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 12 # ~5 kev/job
            },
            })
    datasets["TTJets_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 130#30 # ~4800 ev/job #130 # ~1200 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 25 # ~5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 12 # ~10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 35 # ~5 kev/job
            },
            })
    datasets["TToBLNu_s-channel_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 30#10 # ~5200 ev/job  #30 # ~1800 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 7 # 5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 4 # 10 kev/job
            },
            })
    datasets["TToBLNu_t-channel_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 30#10 # ~4800 ev/job #30 # ~1600 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 6 # ~5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 3 # ~10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 10 # ~5 kev/job
            },
            })
    datasets["TToBLNu_tW-channel_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 35#10 # ~5200 ev/job #35 # ~1600 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 8 # ~5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 4 # ~10 kev/job
            },
            })

    datasets["QCD_Pt20_MuEnriched_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 180#60 # ~4800 ev/job #180 # ~1600 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 20 # 5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 10 # 10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 60 # 5 kev/job
            },
            })

    datasets["DYJetsToLL_M50_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 30 # ~3500 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 30 # ~3500 ev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 5 # ~10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 10 # ~5 kev/job
            },
            })

    datasets["WW_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 45#15 # ~4800 ev/job #45 # ~1600 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 10 # 5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 5 # 10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 14 # 5 kev/job
            },
            })
    datasets["WZ_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 45#15 # ~4800 ev/job #45 # ~1800 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 5 # 10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 14 # 5 kev/job
            },
            })
    datasets["ZZ_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 40#10 # ~6800 ev/job #40 # ~1700 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 12 # 5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 6 # 10 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 14 # 5 kev/job
            },
            })


    datasets["TTToHplusBWB_M120_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 6#2 # ~5200 ev/job #6 # ~1800 ev/job
            },
            "tauembedding_generation_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 2 # 3.5 kev/job
            },
            "tauembedding_embedding_v9_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v9_pt40-9fa4df4950a5013c36bb04ce6d0a226a/USER",
                "number_of_jobs": 1 # 7 kev/job
            },
            "tauembedding_generation_v9_pt30": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9_pt30-23c5106e29fd8da5b4da3e4417dc71b8/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            })

################################################################################

    datasets["Mu_136035-144114_Dec22"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_skim_v10-6e37fea81fa740c69cb63f9eda393091/USER",
                "number_of_jobs": 3 # ~1 kev/job 
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_generation_v10_pt40-2e94a29a39e067876e90268e9726e74b/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_embedding_v10_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_embedding_v10_1_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_embedding_v10_2_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            })
    datasets["Mu_146428-147116_Dec22"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_skim_v10-6e37fea81fa740c69cb63f9eda393091/USER",
                "number_of_jobs": 5 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_generation_v10_pt40-2e94a29a39e067876e90268e9726e74b/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_embedding_v10_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_embedding_v10_1_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_embedding_v10_2_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            })
    datasets["Mu_147196-149294_Dec22"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_skim_v10-1130e004fa4b44415f9ad0db3646fe2b/USER",
                "number_of_jobs": 28 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_generation_v10_pt40-2e94a29a39e067876e90268e9726e74b/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_embedding_v10_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_embedding_v10_1_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            })
    datasets["SingleMu_160431-161016_Prompt"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_skim_v10-7ac1abd2c3a191d20458b2dead0b6623/USER",
                "number_of_jobs": 6 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_generation_v10_pt40-2e94a29a39e067876e90268e9726e74b/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_embedding_v10_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_embedding_v10_1_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v1_AOD_160431_tauembedding_embedding_v10_2_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 1 # 5 kev/job
            },
            })
    datasets["SingleMu_162803-163261_Prompt"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_skim_v10-7ac1abd2c3a191d20458b2dead0b6623/USER",
                "number_of_jobs": 29 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_generation_v10_pt40-2e94a29a39e067876e90268e9726e74b/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_embedding_v10_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_embedding_v10_1_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_162803_tauembedding_embedding_v10_2_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            })
    datasets["SingleMu_163270-163869_Prompt"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_163270_tauembedding_skim_v10-6dd53ec7a9bb64748d7c6d67304b769d/USER",
                "number_of_jobs": 178 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_163270_tauembedding_generation_v10_pt40-2e94a29a39e067876e90268e9726e74b/USER",
                "number_of_jobs": 15 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_163270_tauembedding_embedding_v10_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 15 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_163270_tauembedding_embedding_v10_1_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 15 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v2_AOD_163270_tauembedding_embedding_v10_2_pt40-cee94be795a40bbb5b546b09a0917318/USER",
                "number_of_jobs": 15 # 5 kev/job
            },
            })

    
    datasets["WJets_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 63 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 8 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 8 # 7 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 8 # 7 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 8 # 7 kev/job
            },
            })
    datasets["TTJets_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 165 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 24 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 24 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 24 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 24 # 5 kev/job
            },
            })
    datasets["TToBLNu_s-channel_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 56 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 8 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 8 # 7 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 8 # 7 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 8 # 7 kev/job
            },
            })
    datasets["TToBLNu_t-channel_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 48 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 6 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 6 # 7 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 6 # 7 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 6 # 7 kev/job
            },
            })
    datasets["TToBLNu_tW-channel_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 58 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 9 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 9 # 7 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 9 # 7 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 9 # 7 kev/job
            },
            })

    datasets["QCD_Pt20_MuEnriched_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 200 # ~1.5 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 20 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 20 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 20 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 20 # 5 kev/job
            },
            })

    datasets["DYJetsToLL_M50_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 54 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 9 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 9 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 9 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 9 # 5 kev/job
            },
            })

    datasets["WW_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 75 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            })
    datasets["WZ_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 73 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 11 # 5 kev/job
            },
            })
    datasets["ZZ_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 72 # ~1 kev/job
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 12 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 12 # 5 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 12 # 5 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 12 # 5 kev/job
            },
            })


    datasets["TTToHplusBWB_M120_Spring11"]["data"].update({
            "tauembedding_skim_v10": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10-b3c16f1ee121445edb6d9b12e0772d8e/USER",
                "number_of_jobs": 11 # ~1 kev/job 
            },
            "tauembedding_generation_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40-407f41e7ada5cc209b7b3dca1b2a4528/USER",
                "number_of_jobs": 2 # 5 kev/job
            },
            "tauembedding_embedding_v10_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 1 # 7 kev/job
            },
            "tauembedding_embedding_v10_1_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 1 # 7 kev/job
            },
            "tauembedding_embedding_v10_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_2_pt40-ac95b0c9ecfd651039bbe079053aed03/USER",
                "number_of_jobs": 1 # 7 kev/job
            },
            })


################################################################################

    datasets["SingleMu_160431-163261_May10"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_skim_v11-d2154bd8672d0356e956d91d6de8768f/USER",
                "number_of_jobs": 40 # ~1 kev/job
            },
            "tauembedding_generation_v11_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_generation_v11_1_pt40-e5b5099752982e6e41b65ceeebe69acd/USER",
                "number_of_jobs": 9 # ~2 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_generation_v11_2_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 2 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 2 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 2 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 2 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 2 # ~2 kev/job
            },
            })
    datasets["SingleMu_163270-163869_May10"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_skim_v11-70589c75c0f200e88d1c5de9db6d6775/USER",
                "number_of_jobs": 140 # ~1 kev/job
            },
            "tauembedding_generation_v11_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_generation_v11_2_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 7 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 7 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 7 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 7 # ~2 kev/job
            },
            })
    datasets["SingleMu_165088-166150_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_skim_v11-abfc57ac41b6cbeafd703784696c55e4/USER",
                "number_of_jobs": 170 # ~1 kev/job
            },
            "tauembedding_generation_v11_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_generation_v11_2_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 8 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 8 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 8 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 8 # ~2 kev/job
            },
            })
    datasets["SingleMu_166161-166164_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_skim_v11-fd101d50b7132f2b7e5cdb84fbfeca3a/USER",
                "number_of_jobs": 2 # ~1 kev/job
            },
            "tauembedding_generation_v11_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_generation_v11_1_pt40-e5b5099752982e6e41b65ceeebe69acd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_generation_v11_2_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            })
    datasets["SingleMu_166346-166346_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_skim_v11-9736d74f55daa4ad8a2f5971d065efc8/USER",
                "number_of_jobs": 2 # ~1 kev/job
            },
            "tauembedding_generation_v11_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_generation_v11_pt40-f82b684d417761cff96b7fe7dd1c6ca2/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_generation_v11_2_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            })
    datasets["SingleMu_166374-167043_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_skim_v11-fd101d50b7132f2b7e5cdb84fbfeca3a/USER",
                "number_of_jobs": 188 # ~1 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_generation_v11_2_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 19 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 19 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 19 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 19 # ~2 kev/job
            },
            })
    datasets["SingleMu_167078-167784_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_skim_v11_1-8f4b803c9184c7433c2172bc17a46dec/USER",
                "number_of_jobs": 51 # ~1 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 4 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 4 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 4 # ~2 kev/job
            },
            })

    datasets["SingleMu_161119-161119_May10_Wed"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_161119_tauembedding_skim_v11_2-dd0ba640832535163e436f105f8c8a37/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_161119_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_161119_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_161119_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            })
    datasets["SingleMu_165103-165103_Prompt_Wed"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165103_tauembedding_skim_v11_2-4315f4ee024065925a864d01ae9da7fa/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            })
    datasets["SingleMu_167786-167913_Prompt_Wed"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167786_tauembedding_skim_v11_2-3025e13c2442dda4f3739b5f37145f27/USER",
                "number_of_jobs": 46 # ~1 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167786_tauembedding_generation_v11_3_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 5 # ~2 kev/job
            },
            "tauembedding_embedding_v11_3_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167786_tauembedding_embedding_v11_3_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 5 # ~2 kev/job
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167786_tauembedding_embedding_v11_4_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            })



    datasets["TTJets_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 490 # ~1 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_2_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 65 # ~2 kev/job
            },
            "tauembedding_embedding_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_2_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 65 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "fallback": "tauembedding_generation_v11_2_pt40"
            },
            "tauembedding_embedding_v11_3_pt40": {
                "fallback": "tauembedding_embedding_v11_2_pt40"
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_4_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 65 # ~2 kev/job
            },
            })
    datasets["WJets_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 206 # ~1 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_2_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 35 # ~2 kev/job
            },
            "tauembedding_embedding_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_2_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 35 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "fallback": "tauembedding_generation_v11_2_pt40"
            },
            "tauembedding_embedding_v11_3_pt40": {
                "fallback": "tauembedding_embedding_v11_2_pt40"
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_4_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 35 # ~2 kev/job
            },
            })
    datasets["DYJetsToLL_M50_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11_1-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 240 # ~1 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_2_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 55 # ~2 kev/job
            },
            "tauembedding_embedding_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_2_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 55 # ~2 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "fallback": "tauembedding_generation_v11_2_pt40"
            },
            "tauembedding_embedding_v11_3_pt40": {
                "fallback": "tauembedding_embedding_v11_2_pt40"
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_4_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 55 # ~2 kev/job
            },
            })
    datasets["QCD_Pt20_MuEnriched_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 150 # ~1 kev/job
            },
            "tauembedding_generation_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_2_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_2_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_2_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            "tauembedding_generation_v11_3_pt40": {
                "fallback": "tauembedding_generation_v11_2_pt40"
            },
            "tauembedding_embedding_v11_3_pt40": {
                "fallback": "tauembedding_embedding_v11_2_pt40"
            },
            "tauembedding_embedding_v11_4_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_4_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            })
