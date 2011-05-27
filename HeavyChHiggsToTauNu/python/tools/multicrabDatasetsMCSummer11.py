import multicrabDatasetsCommon as common

# Goal: ~3kev/job

datasets = {
    # QCD backgrounds
    # Cross sections are from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
    "QCD_Pt15to30_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 8.159e+08,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-15to30_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "use_server": 1,
                "number_of_jobs": 2000, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt30to50_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 5.312e+07,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "use_server": 1,
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt50to80_TuneZ2_Summer11": {
        "dataVersion":  "42Xmc",
        "crossSection": 6.359e+06,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt80to120_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7.843e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt120to170_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 1.151e+05,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
            },
        },
    },
    "QCD_Pt170to300_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 2.426e+04,
        "data": {
            "AOD": {
                "datasetpath": "/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "use_server": 1,
                "number_of_jobs": 1000, # Adjusted for PATtuple file size
            },
        },
    },

    # EWK pythia
    "TT_TuneZ2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 165,
        "data": {
            "AOD": {
                "datasetpath": "/TT_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "use_server": 1,
                "number_of_jobs": 350, # Adjusted for PATtuple file size
            },
        },
    },
    "WToTauNu_Z2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7899,
        "data": {
            "AOD": {
                "datasetpath": "/WToTauNu_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "use_server": 1,
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
        },
    },
    "WToMuNu_Z2_Summer11": {
        "dataVersion": "42Xmc",
        "crossSection": 7899,
        "data": {
            "AOD": {
                "datasetpath": "/WToMuNu_TuneZ2_7TeV-pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM",
                "use_server": 1,
                "number_of_jobs": 490, # Adjusted for PATtuple file size
            },
        },
    },
}
