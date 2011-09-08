import multicrabDatasetsCommon as common

datasets = {
    ############################################################
    # Collision data
    #
    # BTau PD (for signal analysis)
    "BTau_141956-144114_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Dec22ReReco_v1_AOD_141956_pattuple_v11b-b20aa4dd1fd1c459fb67271e0123029e/USER",
                "luminosity": 2.846104,
                "number_of_jobs": 30
            },
        }
    },
    "BTau_146428-148058_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146428, 148058), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_146428_pattuple_v11b-75700c75be7f6a8374de48ec67ff8dc8/USER",
                "luminosity": 14.523250,
                "number_of_jobs": 20
            },
        }
    },
    "BTau_148822-149182_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (148822, 149182), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_148822_pattuple_v11b-43988546d882e8b92cda5441042504d2/USER",
                "luminosity": 16.084022,
                "number_of_jobs": 10
            },
        }
    },
    "BTau_149291-149294_Dec22": {
        "dataVersion": "39Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 149294), # The real range for this trigger (from Run Registry and the Dec22 JSON file)
        "data": {
            "pattuple_v11": {
                "dbs_url": common.pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_Dec22ReReco_v1_AOD_149291_pattuple_v11b-23a75132a46243066ab1a7d1af0bcffa/USER",
                "luminosity": 2.270373,
                "number_of_jobs": 2
            },
        }
    },
}
