import multicrabDatasetsCommon as common

datasets = {
    ############################################################
    # Collision data
    #
    # BTau PD (for signal analysis)
    "JetMETTau_Tau_132440-139980_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_SingleLooseIsoTau20",
        "runs": (0, 0), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMETTau/Run2010A-Apr21ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 300, # Adjusted for PATtuple file size
                "lumiMask": "Apr21ReReco"
            },
        }
    },
    "JetMETTau_Tau_140058-141881_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_SingleLooseIsoTau20_Trk5",
        "runs": (140058, 141881), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/JetMETTau/Run2010A-Apr21ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 300, # Adjusted for PATtuple file size
                "lumiMask": "Apr21ReReco"
            },
        }
    },
    "BTau_141956-144114_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "runs": (141956, 144114), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010A-Apr21ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
                "use_server": 1,
                "lumiMask": "Apr21ReReco"
            },
        }
    },
    "BTau_146428-148058_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146428, 148058), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Apr21ReReco-v1/AOD ",
                "luminosity": 0,
                "number_of_jobs": 490, # Adjusted for PATtuple file size
                "lumiMask": "Apr21ReReco"
            },
        }
    },
    "BTau_148108-149182_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v3",
        "runs": (0, 149182), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Apr21ReReco-v1/AOD ",
                "luminosity": 0,
                "number_of_jobs": 450, # Adjusted for PATtuple file size
                "lumiMask": "Apr21ReReco"
            },
        }
    },
    "BTau_149291-149442_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25_v4",
        "runs": (149291, 0), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/BTau/Run2010B-Apr21ReReco-v1/AOD ",
                "luminosity": 0,
                "number_of_jobs": 60, # Adjusted for PATtuple file size
                "lumiMask": "Apr21ReReco"
            },
        }
    },



    # Mu PD (for electroweak background analysis)
    "Mu_133446-144114_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu9",
        "runs": (0, 144114), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010A-Apr21ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 80, # Adjusted for PAT on the fly
                "lumiMask": "Apr21ReReco"
            },
        }
    },
    "Mu_146428-147116_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu9",
        "runs": (146428, 147116), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-Apr21ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PAT on the fly
                "lumiMask": "Apr21ReReco"
            },
        }
    },
    "Mu_147196-149442_Apr21": {
        "dataVersion": "42Xdata",
        "trigger": "HLT_Mu15_v1",
        "runs": (147196, 0), # The real range for this trigger (from Run Registry and the Apr21 JSON file)
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-Apr21ReReco-v1/AOD",
                "luminosity": 0,
                "number_of_jobs": 50, # Adjusted for PAT on the fly
                "lumiMask": "Apr21ReReco"
            },
        }
    },
}
