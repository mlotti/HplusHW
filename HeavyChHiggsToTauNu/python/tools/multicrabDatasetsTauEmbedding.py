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


    datasets["Mu_136035-144114_Dec22"]["data"].update({
            "tauembedding_skim_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_skim_v6_2-14362b39675aa2d1a1be898bd8d6ef08/USER",
                "number_of_jobs": 10 # ~70 ev/job
            },
            "tauembedding_generation_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_generation_v6_2-6aea81f6d245f91e632a791a3c2d020d/USER",
                "number_of_jobs": 10 # ~70 ev/job
            },
            "tauembedding_embedding_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_embedding_v6_2-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 1 # ~700 ev/job
            },
            })
    datasets["Mu_146428-147116_Dec22"]["data"].update({
            "tauembedding_skim_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_skim_v6_2-14362b39675aa2d1a1be898bd8d6ef08/USER",
                "number_of_jobs": 8 # ~150 ev/job
            },
            "tauembedding_generation_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_generation_v6_2-6aea81f6d245f91e632a791a3c2d020d/USER",
                "number_of_jobs": 8 # ~150 ev/job
            },
            "tauembedding_embedding_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_embedding_v6_2-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 1 # ~1200 ev/job
            },
            })
    datasets["Mu_147196-149294_Dec22"]["data"].update({
            "tauembedding_skim_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_skim_v6_2-02482c90013e67a404a9ffaab5714305/USER",
                "number_of_jobs": 30 # ~270 ev/job
            },
            "tauembedding_generation_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_generation_v6_2-6aea81f6d245f91e632a791a3c2d020d/USER",
                "number_of_jobs": 30 # ~270 ev/job
            },
            "tauembedding_embedding_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_embedding_v6_2-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 4 # ~2000 ev/job
            },
            })


    datasets["TTJets_TuneZ2_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 130 # ~1000 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 110 # ~1000 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 60 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })
    datasets["TTJets_TuneD6T_Winter10"]["data"].update({
            "tauembedding_skim_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6_2-fcfdd342282f14f16d1961a4572a9199/USER",
                "number_of_jobs": 105 # ~1300 ev/job
            },
            "tauembedding_generation_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_2-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 105 # ~1300 ev/job
            },
            "tauembedding_embedding_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_2-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 50 # ~2600 ev/job
            },
            })
    datasets["WJets_TuneZ2_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2011Flat_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 100 # ~300 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2011Flat_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 80 # ~1000 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2011Flat_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 15 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })
    datasets["WJets_TuneD6T_Winter10"]["data"].update({
            "tauembedding_skim_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6_2-fcfdd342282f14f16d1961a4572a9199/USER",
                "number_of_jobs": 15 # ~1000 ev/job
            },
            "tauembedding_generation_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_2-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 15 # ~1000 ev/job
            },
            "tauembedding_embedding_v6_2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_2-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 15 # ~1000 ev/job
            },
            })
    datasets["TToBLNu_s-channel_TuneZ2_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 60 # ~300 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 60 # ~300 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 7 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })
    datasets["TToBLNu_t-channel_TuneZ2_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 60 # ~400 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 60 # ~400 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 7 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })
    datasets["TToBLNu_tW-channel_TuneZ2_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 60 # ~500 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 60 # ~400 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 15 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })

    datasets["DYJetsToLL_M50_TuneZ2_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 30 # ~400 ev/job
            },
            "tauembedding_generation_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6-7715dfdca5d016542df257cd85f54436/USER",
                "number_of_jobs": 20 # ~600 ev/job
            },
            "tauembedding_embedding_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6-a19686e39e81c7cc3074cf9dcfd07453/USER",
                "number_of_jobs": 15 # ~850 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 30 # ~600 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 6 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })

    datasets["QCD_Pt20_MuEnriched_TuneZ2_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 150 # ~500 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 150 # ~500 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 35 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })

    datasets["TTToHplusBWB_M120_Winter10"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_skim_v6-356976479e058d2236b19259096d6dbe/USER",
                "number_of_jobs": 15 # ~700 ev/job
            },
            "tauembedding_generation_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 10 # ~700 ev/job
            },
            "tauembedding_embedding_v6_1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1-105b277d7ebabf8cba6c221de6c7ed8a/USER",
                "number_of_jobs": 3 # ~2000 ev/job
            },
            # Fake the v6_2 for MC for time being
            "tauembedding_embedding_v6_2": {
                "fallback": "tauembedding_embedding_v6_1"
            }
            })

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
            })

    datasets["DYJetsToLL_M50_TuneZ2_Spring11"]["data"].update({
            "tauembedding_skim_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v9-00c200b343cbc3d5ec3f111d1d98acde/USER",
                "number_of_jobs": 30 # ~3500 ev/job
            },
            "tauembedding_generation_v9": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v9b_pt40-5a3132437ea5e90a451f1212cd453846/USER",
                "number_of_jobs": 30 # ~3500 ev/job
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
            })
