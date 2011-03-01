import multicrabDatasetsCommon as common

def addTo(datasets):
#    datasets[""]["data"]["tauembedding_skim_v5"] = {
#        "dbs_url": common.pattuple_dbs,
#        "datasetpath": "",
#        "number_of_jobs":  # ~100 ev/job
#    }

    datasets["Mu_136035-144114_Dec22"]["data"].update({
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010A_Dec22ReReco_v1_AOD_136035_tauembedding_skim_v6-e1e03911ddc3956a926ce92e843b1f3e/USER",
                "number_of_jobs": 10 # ~70 ev/job
            },
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
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_146428_tauembedding_skim_v6-e1e03911ddc3956a926ce92e843b1f3e/USER",
                "number_of_jobs": 8 # ~150 ev/job
            },
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
            "tauembedding_skim_v6": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Mu/local-Run2010B_Dec22ReReco_v1_AOD_147196_tauembedding_skim_v6-12ac7b1bb8dedc3750515b605b2bbaa4/USER",
                "number_of_jobs": 30 # ~270 ev/job
            },
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
            "tauembedding_generation_v6_1_test1": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1_test1-aae70947ef6f8ef68bcfe22c92f22781/USER",
                "number_of_jobs": 30 # ~600 ev/job
            },
            "tauembedding_generation_v6_1_test2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_generation_v6_1_test2-e186a9fcb0f6b229006bacc604d044d9/USER",
                "number_of_jobs": 30 # ~600 ev/job
            },
            "tauembedding_embedding_v6_1_test2": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1_test2-a19686e39e81c7cc3074cf9dcfd07453/USER",
                "number_of_jobs": 30 # ~600 ev/job
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
