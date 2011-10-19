import multicrabDatasetsCommon as common

# for generation (skim): ~1 kev ev/job
# for analysis (embedding): 2 hours / job (~5-10 kev/job)

def addTo(datasets):
#    datasets[""]["data"]["tauembedding_skim_v5"] = {
#        "dbs_url": common.pattuple_dbs,
#        "datasetpath": "",
#        "number_of_jobs":  # ~100 ev/job
#    }


    # MC v11_pt, v11_2, v11_3, v11_4, v11_5, v11_6, v11_7
    # data v11_2, v11_3, v11_4

################################################################################

    datasets["SingleMu_Mu_160431-163261_May10"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_skim_v11-d2154bd8672d0356e956d91d6de8768f/USER",
                "number_of_jobs": 40 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 4 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_160431_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 4 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_163270-163869_May10"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_skim_v11-70589c75c0f200e88d1c5de9db6d6775/USER",
                "number_of_jobs": 140 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 14 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_163270_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 14 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_165088-166150_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_skim_v11-abfc57ac41b6cbeafd703784696c55e4/USER",
                "number_of_jobs": 200 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 19 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165088_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 19 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_166161-166164_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_skim_v11-fd101d50b7132f2b7e5cdb84fbfeca3a/USER",
                "number_of_jobs": 2 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166161_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_166346-166346_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_skim_v11-9736d74f55daa4ad8a2f5971d065efc8/USER",
                "number_of_jobs": 2 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166346_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_166374-167043_Prompt"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_skim_v11-fd101d50b7132f2b7e5cdb84fbfeca3a/USER",
                "number_of_jobs": 188 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 37 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_166374_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 37 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_167078-167784_Prompt"]["data"].update({
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
            "tauembedding_generation_v11_5_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_generation_v11_5_pt40-e61ac0316a142e65ba1469fa062e0502/USER",
                "number_of_jobs": 11 # ~1 kev/job
            },
            "tauembedding_embedding_v11_6_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_embedding_v11_6_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 10 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 10 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167078_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 10 # ~1 kev/job
            },
            })

    datasets["SingleMu_Mu_161119-161119_May10_Wed"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_161119_tauembedding_skim_v11_2-dd0ba640832535163e436f105f8c8a37/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_161119_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_May10ReReco_v1_AOD_161119_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_165103-165103_Prompt_Wed"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_165103_tauembedding_skim_v11_2-4315f4ee024065925a864d01ae9da7fa/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            })
    datasets["SingleMu_Mu_167786-167913_Prompt_Wed"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167786_tauembedding_skim_v11_2-3025e13c2442dda4f3739b5f37145f27/USER",
                "number_of_jobs": 46 # ~1 kev/job
            },
            "tauembedding_generation_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167786_tauembedding_generation_v11_8_pt40-dd4694aacf1066a904be68d33c0ffb5c/USER",
                "number_of_jobs": 9 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-Run2011A_PromptReco_v4_AOD_167786_tauembedding_embedding_v11_8_pt40-ac085343fdb44ba8377c1f709923eacd/USER",
                "number_of_jobs": 9 # ~1 kev/job
            },
            })


    datasets["TTJets_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 490 # ~1 kev/job
            },
            "tauembedding_generation_v11_5_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_5_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 129 # ~1 kev/job
            },
            "tauembedding_embedding_v11_6_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_6_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 129 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "fallback": "tauembedding_embedding_v11_6_pt40"
            },
            })
    datasets["WJets_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 206 # ~1 kev/job
            },
            "tauembedding_generation_v11_5_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_5_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 62 # ~1 kev/job
            },
            "tauembedding_embedding_v11_6_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_6_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 60 # ~1 kev/job
            }, 
            "tauembedding_embedding_v11_8_pt40": {
                "fallback": "tauembedding_embedding_v11_6_pt40"
            },
            })
    datasets["DYJetsToLL_M50_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11_1-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 400 # ~1 kev/job
            },
            "tauembedding_generation_v11_5_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_5_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 175 # ~2 kev/job
            },
            "tauembedding_embedding_v11_6_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_6_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 170 # ~2 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "fallback": "tauembedding_embedding_v11_6_pt40"
            },
            })
    datasets["QCD_Pt20_MuEnriched_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v11-50e9a4e9bac98baa56423a829b7f0fda/USER",
                "number_of_jobs": 150 # ~1 kev/job
            },
            "tauembedding_generation_v11_5_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_generation_v11_5_pt40-7b7c65a5a8d29ee0d475920888840478/USER",
                "number_of_jobs": 1 # ~2 kev/job
            },
            "tauembedding_embedding_v11_6_pt40": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_6_pt40-af0b4aa82477426f47ec012132b67081/USER",
                "number_of_jobs": 1 # ~1 kev/job
            },
            "tauembedding_embedding_v11_8_pt40": {
                "fallback": "tauembedding_embedding_v11_6_pt40"
            },
            })

################################################################################

    datasets["SingleMu_Mu_160431-163261_May10"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-May10ReReco_v1_AOD_160431_tauembedding_skim_v13-9cdf0eb8900aa637b61ccc82f152c6ed/USER",
                "number_of_jobs": 6 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-May10ReReco_v1_AOD_160431_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_163270-163869_May10"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-May10ReReco_v1_AOD_163270_tauembedding_skim_v13-c61b4e9bdf1ffeec75e33c6424b25cdb/USER",
                "number_of_jobs": 40 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-May10ReReco_v1_AOD_163270_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 4 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_165088-166150_Prompt"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_165088_tauembedding_skim_v13-a425e273cc15b943339437b345a2e98d/USER",
                "number_of_jobs": 40 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_165088_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 5 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_166161-166164_Prompt"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_166161_tauembedding_skim_v13_2-46d2cb331c30c7a82a30d66aa5cd1785/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_166161_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_166346-166346_Prompt"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_166346_tauembedding_skim_v13_2-5838507f6e8a0c16a243ee2686c03016/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_166346_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_166374-167043_Prompt"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_166374_tauembedding_skim_v13-46d2cb331c30c7a82a30d66aa5cd1785/USER",
                "number_of_jobs": 45 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_166374_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 10 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_167078-167913_Prompt"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_167078_tauembedding_skim_v13-0cb7eab6610b4f67800452f2685ea477/USER",
                "number_of_jobs": 25 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v4_AOD_167078_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 5 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_170722-172619_Aug05"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-05Aug2011_v1_AOD_170722_tauembedding_skim_v13-23d3791c980dcc1a59a485ca5d8ad22e/USER",
                "number_of_jobs": 45 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-05Aug2011_v1_AOD_170722_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 8 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_172620-173198_Prompt"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v6_AOD_172620_tauembedding_skim_v13-23d3791c980dcc1a59a485ca5d8ad22e/USER",
                "number_of_jobs": 50 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v6_AOD_172620_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 9 # ~5 kev/job
            },
            })
    datasets["SingleMu_Mu_173236-173692_Prompt"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v6_AOD_173236_tauembedding_skim_v13-19b79d7dc2d65f948070055429ce37d3/USER",
                "number_of_jobs": 25 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/SingleMu/local-PromptReco_v6_AOD_173236_tauembedding_embedding_v13-9a509078f648b588515c15f2e17e813c/USER",
                "number_of_jobs": 6 # ~5 kev/job
            },
            })

    datasets["TTJets_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13_2-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 90 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 27 # ~5 kev/job
            },
            })
    datasets["WJets_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 100 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 27 # ~5 kev/job
            },
            })
    datasets["DYJetsToLL_M50_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13_2-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs":  230 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 96 # ~5 kev/job
            },
            })
    datasets["T_t-channel_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 20 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 6 # ~5 kev/job
            },
            })
    datasets["Tbar_t-channel_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 12 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 3 # ~5 kev/job
            },
            })
    datasets["T_tW-channel_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 20 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 6 # ~5 kev/job
            },
            })
    datasets["Tbar_tW-channel_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 20 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 6 # ~5 kev/job
            },
            })
    datasets["T_s-channel_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 2 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["Tbar_s-channel_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
    datasets["WW_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WW_TuneZ2_7TeV_pythia6_tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 35 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WW_TuneZ2_7TeV_pythia6_tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 11 # ~5 kev/job
            },
            })
    datasets["WZ_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZ_TuneZ2_7TeV_pythia6_tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 35 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/WZ_TuneZ2_7TeV_pythia6_tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 12 # ~5 kev/job
            },
            })
    datasets["ZZ_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 30 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 13 # ~5 kev/job
            },
            })
    datasets["QCD_Pt20_MuEnriched_TuneZ2_Summer11"]["data"].update({
            "tauembedding_skim_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13-6ce8de2c5b6c0c9ed414998577b7e28d/USER",
                "number_of_jobs": 15 # ~5 kev/job
            },
            "tauembedding_embedding_v13": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v13-ed34c604d92bb4d3e5bcb4943b860e5e/USER",
                "number_of_jobs": 1 # ~5 kev/job
            },
            })
