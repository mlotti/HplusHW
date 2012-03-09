## \package plots
# Plot utilities and classes
#
# The package is intended to gather the following commonalities in the
# plots of H+ analysis (signal analysis, QCD and EWK background
# analyses)
# \li Dataset merging (see plots._datasetMerge)
# \li Dataset order (see plots._datasetOrder)
# \li Dataset legend labels (see plots._legendLabels)
# \li Dataset plot styles (see plots._plotStyles)
# \li Various datasets.DatasetManager operations (see plots.mergeRenameReorderForDataMC())
# \li Various histograms.HistoManager operations (see plots.PlotBase and the derived classes)
# \li Plot customisation, drawing, and saving (see plots.PlotDrawer)
#
# The intended usage is to 
# \li construct datasets.DatasetManager as usual
# \li call plots.mergeRenameReorderForDataMC()
# \li construct an object of the appropriate plots.PlotBase derived class
# \li customise, draw, and save the plot with plots.drawPlot (or something derived from plots.PlotDrawer, or more manually)
#
# Manually further customisations and operations can be done via the
# interface of the plots.PlotBase derived class, or directly with the
# histograms.HistoManager object contained by the plot object (via
# histoMgr member). Some automation is provided with plots.PlotDrawer.
#
# Although the intended usage is described above, it does \b not mean
# that it would be the only way to use the classes. You should use
# them only if they help you, and in a way which helps you. For
# example, plots.PlotBase (or plots.ComparisonPlot,
# plots.ComparisonManyPlot) doesn't care at all where the
# histograms/graphs come from. If your problem is solved with direct
# access to TFile and TH1/TGraph objects, or from TTree, more easily
# than with datasetsd.DatasetManager, there is absolutely no problem
# in doing so.

import ROOT
import array
import math

import dataset
import histograms
import styles

## Map the physical dataset names to logical names
#
# Map the physical dataset names (in multicrab.cfg) to logical names
# used in plots._legendLabels and plots._plotStyles. The mapping is
# used in the mergeRenameReorderForDataMC() function.
_physicalToLogical = {
    "TTToHplusBWB_M90_Winter10":  "TTToHplusBWB_M90", 
    "TTToHplusBWB_M100_Winter10": "TTToHplusBWB_M100",
    "TTToHplusBWB_M120_Winter10": "TTToHplusBWB_M120",
    "TTToHplusBWB_M140_Winter10": "TTToHplusBWB_M140",
    "TTToHplusBWB_M160_Winter10": "TTToHplusBWB_M160",
    "TTToHplusBWB_M80_Spring11":  "TTToHplusBWB_M80",
    "TTToHplusBWB_M90_Spring11":  "TTToHplusBWB_M90",
    "TTToHplusBWB_M100_Spring11": "TTToHplusBWB_M100",
    "TTToHplusBWB_M120_Spring11": "TTToHplusBWB_M120",
    "TTToHplusBWB_M140_Spring11": "TTToHplusBWB_M140",
    "TTToHplusBWB_M150_Spring11": "TTToHplusBWB_M150",
    "TTToHplusBWB_M155_Spring11": "TTToHplusBWB_M155",
    "TTToHplusBWB_M160_Spring11": "TTToHplusBWB_M160",
    "TTToHplusBWB_M80_Summer11":  "TTToHplusBWB_M80",
    "TTToHplusBWB_M90_Summer11":  "TTToHplusBWB_M90",
    "TTToHplusBWB_M100_Summer11": "TTToHplusBWB_M100",
    "TTToHplusBWB_M120_Summer11": "TTToHplusBWB_M120",
    "TTToHplusBWB_M140_Summer11": "TTToHplusBWB_M140",
    "TTToHplusBWB_M150_Summer11": "TTToHplusBWB_M150",
    "TTToHplusBWB_M155_Summer11": "TTToHplusBWB_M155",
    "TTToHplusBWB_M160_Summer11": "TTToHplusBWB_M160",
    "TTToHplusBWB_M80_Fall11":  "TTToHplusBWB_M80",
    "TTToHplusBWB_M90_Fall11":  "TTToHplusBWB_M90",
    "TTToHplusBWB_M100_Fall11": "TTToHplusBWB_M100",
    "TTToHplusBWB_M120_Fall11": "TTToHplusBWB_M120",
    "TTToHplusBWB_M140_Fall11": "TTToHplusBWB_M140",
    "TTToHplusBWB_M150_Fall11": "TTToHplusBWB_M150",
    "TTToHplusBWB_M155_Fall11": "TTToHplusBWB_M155",
    "TTToHplusBWB_M160_Fall11": "TTToHplusBWB_M160",

    "TTToHplusBHminusB_M80_Spring11": "TTToHplusBHminusB_M80",
    "TTToHplusBHminusB_M100_Spring11": "TTToHplusBHminusB_M100",
    "TTToHplusBHminusB_M120_Spring11": "TTToHplusBHminusB_M120",
    "TTToHplusBHminusB_M140_Spring11": "TTToHplusBHminusB_M140",
    "TTToHplusBHminusB_M150_Spring11": "TTToHplusBHminusB_M150",
    "TTToHplusBHminusB_M155_Spring11": "TTToHplusBHminusB_M155",
    "TTToHplusBHminusB_M160_Spring11": "TTToHplusBHminusB_M160",
    "TTToHplusBHminusB_M80_Summer11": "TTToHplusBHminusB_M80",
    "TTToHplusBHminusB_M90_Summer11": "TTToHplusBHminusB_M90",
    "TTToHplusBHminusB_M100_Summer11": "TTToHplusBHminusB_M100",
    "TTToHplusBHminusB_M120_Summer11": "TTToHplusBHminusB_M120",
    "TTToHplusBHminusB_M140_Summer11": "TTToHplusBHminusB_M140",
    "TTToHplusBHminusB_M150_Summer11": "TTToHplusBHminusB_M150",
    "TTToHplusBHminusB_M155_Summer11": "TTToHplusBHminusB_M155",
    "TTToHplusBHminusB_M160_Summer11": "TTToHplusBHminusB_M160",
    "TTToHplusBHminusB_M80_Fall11": "TTToHplusBHminusB_M80",
    "TTToHplusBHminusB_M90_Fall11": "TTToHplusBHminusB_M90",
    "TTToHplusBHminusB_M100_Fall11": "TTToHplusBHminusB_M100",
    "TTToHplusBHminusB_M120_Fall11": "TTToHplusBHminusB_M120",
    "TTToHplusBHminusB_M140_Fall11": "TTToHplusBHminusB_M140",
    "TTToHplusBHminusB_M150_Fall11": "TTToHplusBHminusB_M150",
    "TTToHplusBHminusB_M155_Fall11": "TTToHplusBHminusB_M155",
    "TTToHplusBHminusB_M160_Fall11": "TTToHplusBHminusB_M160",

    "HplusTB_M180_Summer11": "HplusTB_M180",
    "HplusTB_M190_Summer11": "HplusTB_M190",
    "HplusTB_M200_Summer11": "HplusTB_M200",
    "HplusTB_M220_Summer11": "HplusTB_M220",
    "HplusTB_M250_Summer11": "HplusTB_M250",
    "HplusTB_M300_Summer11": "HplusTB_M300",
    "HplusTB_M180_Fall11": "HplusTB_M180",
    "HplusTB_M190_Fall11": "HplusTB_M190",
    "HplusTB_M200_Fall11": "HplusTB_M200",
    "HplusTB_M220_Fall11": "HplusTB_M220",
    "HplusTB_M250_Fall11": "HplusTB_M250",
    "HplusTB_M300_Fall11": "HplusTB_M300",

    "TTJets_TuneD6T_Winter10": "TTJets",
    "TTJets_TuneZ2_Winter10": "TTJets",
    "TTJets_TuneZ2_Spring11": "TTJets",
    "TTJets_TuneZ2_Summer11": "TTJets",
    "TTJets_TuneZ2_Fall11": "TTJets",
    "TT_TuneZ2_Summer11": "TT",

    "WJets_TuneD6T_Winter10": "WJets",
    "WJets_TuneZ2_Winter10": "WJets",
    "WJets_TuneZ2_Winter10_noPU": "WJets",
    "WJets_TuneZ2_Spring11": "WJets",
    "WJets_TuneZ2_Summer11": "WJets",
    "WJets_TuneZ2_Fall11": "WJets",
    "WToTauNu_TuneZ2_Summer11": "WToTauNu",

    "W3Jets_TuneZ2_Summer11": "W3Jets",

    "DYJetsToLL_TuneZ2_Winter10":          "DYJetsToLL_M50",
    "DYJetsToLL_M50_TuneZ2_Winter10":      "DYJetsToLL_M50",
    "DYJetsToLL_M10to50_TuneD6T_Winter10": "DYJetsToLL_M10to50",
    "DYJetsToLL_M50_TuneD6T_Winter10":     "DYJetsToLL_M50",
    "DYJetsToLL_M50_TuneZ2_Spring11":      "DYJetsToLL_M50",
    "DYJetsToLL_M50_TuneZ2_Summer11":      "DYJetsToLL_M50",
    "DYJetsToLL_M50_TuneZ2_Fall11":      "DYJetsToLL_M50",

    "TToBLNu_s-channel_TuneZ2_Winter10": "TToBLNu_s-channel",
    "TToBLNu_t-channel_TuneZ2_Winter10": "TToBLNu_t-channel",
    "TToBLNu_tW-channel_TuneZ2_Winter10": "TToBLNu_tW-channel",
    "TToBLNu_s-channel_TuneZ2_Spring11": "TToBLNu_s-channel",
    "TToBLNu_t-channel_TuneZ2_Spring11": "TToBLNu_t-channel",
    "TToBLNu_tW-channel_TuneZ2_Spring11": "TToBLNu_tW-channel",
    "T_t-channel_TuneZ2_Summer11":     "T_t-channel",
    "Tbar_t-channel_TuneZ2_Summer11":  "Tbar_t-channel",
    "T_tW-channel_TuneZ2_Summer11":    "T_tW-channel",
    "Tbar_tW-channel_TuneZ2_Summer11": "Tbar_tW-channel",
    "T_s-channel_TuneZ2_Summer11":     "T_s-channel",
    "Tbar_s-channel_TuneZ2_Summer11":  "Tbar_s-channel",
    "T_t-channel_TuneZ2_Fall11":     "T_t-channel",
    "Tbar_t-channel_TuneZ2_Fall11":  "Tbar_t-channel",
    "T_tW-channel_TuneZ2_Fall11":    "T_tW-channel",
    "Tbar_tW-channel_TuneZ2_Fall11": "Tbar_tW-channel",
    "T_s-channel_TuneZ2_Fall11":     "T_s-channel",
    "Tbar_s-channel_TuneZ2_Fall11":  "Tbar_s-channel",

    "QCD_Pt30to50_TuneZ2_Winter10":   "QCD_Pt30to50",
    "QCD_Pt50to80_TuneZ2_Winter10":   "QCD_Pt50to80",
    "QCD_Pt80to120_TuneZ2_Winter10":  "QCD_Pt80to120",
    "QCD_Pt120to170_TuneZ2_Winter10": "QCD_Pt120to170",
    "QCD_Pt170to300_TuneZ2_Winter10": "QCD_Pt170to300",
    "QCD_Pt300to470_TuneZ2_Winter10": "QCD_Pt300to470",
    "QCD_Pt30to50_TuneZ2_Spring11":   "QCD_Pt30to50",
    "QCD_Pt50to80_TuneZ2_Spring11":   "QCD_Pt50to80",
    "QCD_Pt80to120_TuneZ2_Spring11":  "QCD_Pt80to120",
    "QCD_Pt120to170_TuneZ2_Spring11": "QCD_Pt120to170",
    "QCD_Pt170to300_TuneZ2_Spring11": "QCD_Pt170to300",
    "QCD_Pt300to470_TuneZ2_Spring11": "QCD_Pt300to470",
    "QCD_Pt30to50_TuneZ2_Summer11":   "QCD_Pt30to50",
    "QCD_Pt50to80_TuneZ2_Summer11":   "QCD_Pt50to80",
    "QCD_Pt80to120_TuneZ2_Summer11":  "QCD_Pt80to120",
    "QCD_Pt120to170_TuneZ2_Summer11": "QCD_Pt120to170",
    "QCD_Pt170to300_TuneZ2_Summer11": "QCD_Pt170to300",
    "QCD_Pt300to470_TuneZ2_Summer11": "QCD_Pt300to470",
    "QCD_Pt30to50_TuneZ2_Fall11":   "QCD_Pt30to50",
    "QCD_Pt50to80_TuneZ2_Fall11":   "QCD_Pt50to80",
    "QCD_Pt80to120_TuneZ2_Fall11":  "QCD_Pt80to120",
    "QCD_Pt120to170_TuneZ2_Fall11": "QCD_Pt120to170",
    "QCD_Pt170to300_TuneZ2_Fall11": "QCD_Pt170to300",
    "QCD_Pt300to470_TuneZ2_Fall11": "QCD_Pt300to470",

    "QCD_Pt20_MuEnriched_TuneZ2_Winter10": "QCD_Pt20_MuEnriched",
    "QCD_Pt20_MuEnriched_TuneZ2_Spring11": "QCD_Pt20_MuEnriched",
    "QCD_Pt20_MuEnriched_TuneZ2_Summer11": "QCD_Pt20_MuEnriched",
    "QCD_Pt20_MuEnriched_TuneZ2_Fall11": "QCD_Pt20_MuEnriched",

    "WW_TuneZ2_Winter10": "WW",
    "WZ_TuneZ2_Winter10": "WZ",
    "ZZ_TuneZ2_Winter10": "ZZ",
    "WW_TuneZ2_Spring11": "WW",
    "WZ_TuneZ2_Spring11": "WZ",
    "ZZ_TuneZ2_Spring11": "ZZ",
    "WW_TuneZ2_Summer11": "WW",
    "WZ_TuneZ2_Summer11": "WZ",
    "ZZ_TuneZ2_Summer11": "ZZ",
    "WW_TuneZ2_Fall11": "WW",
    "WZ_TuneZ2_Fall11": "WZ",
    "ZZ_TuneZ2_Fall11": "ZZ",
}

## Map the datasets to be merged to the name of the merged dataset.
_signalMerge = [
    ("TTToHplusBWB_M80",  "TTToHplusBHminusB_M80",  "TTToHplus_M80"),
    ("TTToHplusBWB_M90",  "TTToHplusBHminusB_M90",  "TTToHplus_M90"),
    ("TTToHplusBWB_M100", "TTToHplusBHminusB_M100", "TTToHplus_M100"),
    ("TTToHplusBWB_M120", "TTToHplusBHminusB_M120", "TTToHplus_M120"),
    ("TTToHplusBWB_M140", "TTToHplusBHminusB_M140", "TTToHplus_M140"),
    ("TTToHplusBWB_M150", "TTToHplusBHminusB_M150", "TTToHplus_M150"),
    ("TTToHplusBWB_M155", "TTToHplusBHminusB_M155", "TTToHplus_M155"),
    ("TTToHplusBWB_M160", "TTToHplusBHminusB_M160", "TTToHplus_M160"),
]
_datasetMerge = {
    "QCD_Pt30to50":   "QCD",
    "QCD_Pt50to80":   "QCD",
    "QCD_Pt80to120":  "QCD",
    "QCD_Pt120to170": "QCD",
    "QCD_Pt170to300": "QCD",
    "QCD_Pt300to470": "QCD",

    "TToBLNu_s-channel": "SingleTop",
    "TToBLNu_t-channel": "SingleTop",
    "TToBLNu_tW-channel": "SingleTop",
    "T_t-channel":     "SingleTop",
    "Tbar_t-channel":  "SingleTop",
    "T_tW-channel":    "SingleTop",
    "Tbar_tW-channel": "SingleTop",
    "T_s-channel":     "SingleTop",
    "Tbar_s-channel":  "SingleTop",

    "DYJetsToLL_M10to50": "DYJetsToLL",
    "DYJetsToLL_M50": "DYJetsToLL",

    "WW": "Diboson",
    "WZ": "Diboson",
    "ZZ": "Diboson",
}

## Default ordering of datasets
_datasetOrder = [
    "Data",
    "TTToHplusBWB_M80", 
    "TTToHplusBWB_M90", 
    "TTToHplusBWB_M100",
    "TTToHplusBWB_M120",
    "TTToHplusBWB_M140",
    "TTToHplusBWB_M150",
    "TTToHplusBWB_M155",
    "TTToHplusBWB_M160",
    "TTToHplusBHminusB_M80",
    "TTToHplusBHminusB_M90",
    "TTToHplusBHminusB_M100",
    "TTToHplusBHminusB_M120",
    "TTToHplusBHminusB_M140",
    "TTToHplusBHminusB_M150",
    "TTToHplusBHminusB_M155",
    "TTToHplusBHminusB_M160",
    "TTToHplus_M80",
    "TTToHplus_M90",
    "TTToHplus_M100",
    "TTToHplus_M120",
    "TTToHplus_M140",
    "TTToHplus_M150",
    "TTToHplus_M155",
    "TTToHplus_M160",
    "HplusTB_M180",
    "HplusTB_M190",
    "HplusTB_M290",
    "HplusTB_M220",
    "HplusTB_M250",
    "HplusTB_M300",
    "QCD",
    "QCDdata",
    "QCD_Pt20_MuEnriched",
    "WJets",
    "W3Jets",
    "WToTauNu",
    "TTJets",
    "TT",
    "DYJetsToLL",
    "SingleTop",
    "Diboson",
]

## Map the logical dataset names to legend labels
_legendLabels = {
    "Data":                  "Data",

    "TTToHplusBWB_M80":  "H^{+}W^{-} m_{H^{#pm}}=80", 
    "TTToHplusBWB_M90":  "H^{+}W^{-} m_{H^{#pm}}=90", 
    "TTToHplusBWB_M100": "H^{+}W^{-} m_{H^{#pm}}=100",
    "TTToHplusBWB_M120": "H^{+}W^{-} m_{H^{#pm}}=120",
    "TTToHplusBWB_M140": "H^{+}W^{-} m_{H^{#pm}}=140",
    "TTToHplusBWB_M150": "H^{+}W^{-} m_{H^{#pm}}=150",
    "TTToHplusBWB_M155": "H^{+}W^{-} m_{H^{#pm}}=155",
    "TTToHplusBWB_M160": "H^{+}W^{-} m_{H^{#pm}}=160",

    "TTToHplusBHminusB_M80":  "H^{+}H^{-} m_{H^{#pm}}=80",
    "TTToHplusBHminusB_M90":  "H^{+}H^{-} m_{H^{#pm}}=90",
    "TTToHplusBHminusB_M100": "H^{+}H^{-} m_{H^{#pm}}=100",
    "TTToHplusBHminusB_M120": "H^{+}H^{-} m_{H^{#pm}}=120",
    "TTToHplusBHminusB_M140": "H^{+}H^{-} m_{H^{#pm}}=140",
    "TTToHplusBHminusB_M150": "H^{+}H^{-} m_{H^{#pm}}=150",
    "TTToHplusBHminusB_M155": "H^{+}H^{-} m_{H^{#pm}}=155",
    "TTToHplusBHminusB_M160": "H^{+}H^{-} m_{H^{#pm}}=160",

    "TTToHplus_M80":  "H^{#pm} m_{H^{#pm}}=80",
    "TTToHplus_M90":  "H^{#pm} m_{H^{#pm}}=90",
    "TTToHplus_M100": "H^{#pm} m_{H^{#pm}}=100",
    "TTToHplus_M120": "H^{#pm} m_{H^{#pm}}=120",
    "TTToHplus_M140": "H^{#pm} m_{H^{#pm}}=140",
    "TTToHplus_M150": "H^{#pm} m_{H^{#pm}}=150",
    "TTToHplus_M155": "H^{#pm} m_{H^{#pm}}=155",
    "TTToHplus_M160": "H^{#pm} m_{H^{#pm}}=160",

    "HplusTB_M180": "H^{#pm} m_{H^{#pm}}=180",
    "HplusTB_M190": "H^{#pm} m_{H^{#pm}}=190",
    "HplusTB_M200": "H^{#pm} m_{H^{#pm}}=200",
    "HplusTB_M220": "H^{#pm} m_{H^{#pm}}=220",
    "HplusTB_M250": "H^{#pm} m_{H^{#pm}}=250",
    "HplusTB_M300": "H^{#pm} m_{H^{#pm}}=300",

    "TTJets":                "t#bar{t}+jets",
    "TT":                    "t#bar{t}",

    "WJets":                 "W+jets",
    "WToTauNu":              "W#to#tau#nu",
    "W3Jets":                "W+3 jets",

    "QCD_Pt30to50":          "QCD, 30 < #hat{p}_{T} < 50",
    "QCD_Pt50to80":          "QCD, 50 < #hat{p}_{T} < 80",
    "QCD_Pt80to120":         "QCD, 80 < #hat{p}_{T} < 120",
    "QCD_Pt120to170":        "QCD, 120 < #hat{p}_{T} < 170",
    "QCD_Pt170to300":        "QCD, 170 < #hat{p}_{T} < 300",
    "QCD_Pt300to470":        "QCD, 300 < #hat{p}_{T} < 470",

    "QCDdata": "QCD (data driven)",

    "DYJetsToLL":            "DY+jets",
    "QCD_Pt20_MuEnriched":   "QCD (#mu enr.), #hat{p}_{T} > 20",

    "SingleTop":             "Single t",
    "TToBLNu_s-channel":     "Single t (s channel)",
    "TToBLNu_t-channel":     "Single t (t channel)",
    "TToBLNu_tW-channel":    "Single t (tW channel)",
    "T_t-channel":           "Single t (t channel)",
    "Tbar_t-channel":        "Single #bar{t} (t channel)",
    "T_tW-channel":          "Single t (tW channel)",
    "Tbar_tW-channel":       "Single #bar{t} (tW channel)",
    "T_s-channel":           "Single t (s channel)",
    "Tbar_s-channel":        "Single #bar{t} (s channel)",
}

## Map the logical dataset names to plot styles
_plotStyles = {
    "Data":                  styles.dataStyle,

    "TTToHplusBWB_M80":           styles.signal80Style,
    "TTToHplusBWB_M90":           styles.signal90Style,
    "TTToHplusBWB_M100":          styles.signal100Style,
    "TTToHplusBWB_M120":          styles.signal120Style,
    "TTToHplusBWB_M140":          styles.signal140Style,
    "TTToHplusBWB_M150":          styles.signal150Style,
    "TTToHplusBWB_M155":          styles.signal155Style,
    "TTToHplusBWB_M160":          styles.signal160Style,

    "TTToHplusBHminusB_M80":       styles.signalHH80Style,
    "TTToHplusBHminusB_M90":       styles.signalHH90Style,
    "TTToHplusBHminusB_M100":      styles.signalHH100Style,
    "TTToHplusBHminusB_M120":      styles.signalHH120Style,
    "TTToHplusBHminusB_M140":      styles.signalHH140Style,
    "TTToHplusBHminusB_M150":      styles.signalHH150Style,
    "TTToHplusBHminusB_M155":      styles.signalHH155Style,
    "TTToHplusBHminusB_M160":      styles.signalHH160Style,

    "TTToHplus_M80":           styles.signal80Style,
    "TTToHplus_M90":           styles.signal90Style,
    "TTToHplus_M100":          styles.signal100Style,
    "TTToHplus_M120":          styles.signal120Style,
    "TTToHplus_M140":          styles.signal140Style,
    "TTToHplus_M150":          styles.signal150Style,
    "TTToHplus_M155":          styles.signal155Style,
    "TTToHplus_M160":          styles.signal160Style,

    "HplusTB_M180": styles.signal180Style,
    "HplusTB_M190": styles.signal190Style,
    "HplusTB_M200": styles.signal200Style,
    "HplusTB_M220": styles.signal220Style,
    "HplusTB_M250": styles.signal250Style,
    "HplusTB_M300": styles.signal300Style,

    "TTJets":                styles.ttStyle,
    "TT":                    styles.ttStyle,

    "WJets":                 styles.wStyle,
    "WToTauNu":              styles.wStyle,
    "W3Jets":                styles.wStyle,

    "QCD":                   styles.qcdStyle,
    "QCDdata":               styles.qcdStyle,

    "DYJetsToLL":            styles.dyStyle,
    "QCD_Pt20_MuEnriched":   styles.qcdStyle,
    "SingleTop":             styles.stStyle,
    "Diboson":               styles.dibStyle,
}

## Return True if name is from a signal dataset
def isSignal(name):
    return "TTToHplus" in name or "HplusTB" in name


## Update the default legend labels
def updateLegendLabel(datasetName, legendLabel):
    _legendLabels[datasetName] = legendLabel

## Helper class for setting properties
#
# Helper class for setting properties of histograms.Histo objects (legend label, plot style)
class SetProperty:
    ## Constructor
    #
    # \param properties  Dictionary of properties (from name of
    #                    histograms.Histo to the property understood
    #                    by the setter)
    # \param setter      Function for setting the property. It should take
    #                    two parameters, first one is the
    #                    histograms.Histo object, second one is the
    #                    property to be set
    def __init__(self, properties, setter):
        self.properties = properties
        self.setter = setter

    ## Set the property of a given object
    #
    # \param histoData   histograms.Histo object for which to set the property
    #
    # If there is no property to be set for a given histo, nothing is done to it
    def __call__(self, histoData):
        prop = self._getProperty(histoData.getName())
        if prop != None:
            self.setter(histoData, prop)

    ## Get the property
    #
    # \param name  Name of the property
    #
    # \todo Replace this with self.properties.get(name, None)...
    def _getProperty(self, name):
        if name in self.properties:
            return self.properties[name]
        else:
            return None

    ## \var properties
    # Dictionary of properties (see __init__())
    ## \var setter
    # Function setting the property (see __init__())

## Construct a "function" to set legend labels
#
# \param labels   Dictionary of labels (from the histo name to the legend label)
#
# \return   Object with implemented function call operator " to be used
#           with histograms.HistoManagerImpl.forEachHisto().
def SetLegendLabel(labels):
    return SetProperty(labels, lambda hd, label: hd.setLegendLabel(label))

## Construct a "function" to set plot styles
#
# \param styleMap   Dictionary of styles (from the histo name to the style)
#
# \return   Object with implemented function call operator " to be used
#           with histograms.HistoManagerImpl.forEachHisto().
def SetPlotStyle(styleMap):
    return SetProperty(styleMap, lambda hd, style: hd.call(style))

## Construct a "function" to update some styles to filled
#
# \param styleMap       Dictionary of styles (from the histo name to the style)
# \param namesToFilled  List of histogram names for which to apply the filled style
#
# \return   Object with implemented function call operator " to be used
#           with histograms.HistoManagerImpl.forEachHisto().
#
# The filled style is implemented via style.StyleFill
def UpdatePlotStyleFill(styleMap, namesToFilled):
    def update(hd, style):
        if hd.getName() in namesToFilled:
            hd.call(styles.StyleFill(style))

    return SetProperty(styleMap, update)

## Default dataset merging, naming and reordering for data/MC comparison
#
# \param datasetMgr  dataset.DatasetManager object
#
# Merges data datasets and the MC datasets as specified in
# plots._datasetMerge. The intention is that the datasets to be merged
# as one are kind of binned ones, and the final merged dataset forms a
# logical entity. For example, data in multiple run periods, QCD in
# pthat bins, single top in the separate channels, WW, WZ and ZZ for
# diboson.
#
# Renames the datasets as specified in plots._physicalToLogical. The
# intention is that the physical dataset names (i.e. the crab task
# names in multicrab.cfg) can contain some rather specific information
# (e.g. the pythia tune, MC production era) which is not that relevant
# in actual plotting (i.e. TTJets in TuneZ2 and TuneD6T, and from
# Fall10 and Winter10, all are logically TTJets sample). This choice
# makes e.g. the plots._datasetMerge, plots._datasetOrder,
# plots._legendLabels and plots._plotStyles shorter and more generic.
#
# Finally orders the datasets as specified in plots._datasetOrder. The
# datasets not in the plots._datasetOrder list are left at the end in
# the same order they were originally.
def mergeRenameReorderForDataMC(datasetMgr, keepSourcesMC=False):
    datasetMgr.mergeData()
    datasetMgr.renameMany(_physicalToLogical, silent=True)

    datasetMgr.mergeMany(_datasetMerge, keepSources=keepSourcesMC)

    mcNames = datasetMgr.getAllDatasetNames()
    newOrder = []
    for name in _datasetOrder:
        try:
            i = mcNames.index(name)
            newOrder.append(name)
            del mcNames[i]
        except ValueError:
            pass
    newOrder.extend(mcNames)
    datasetMgr.selectAndReorder(newOrder)

## Merge WH and HH datasets for each mass point
#
# The dataset names to be merged are defined in plots._signalMerge list
def mergeWHandHH(datasetMgr):
    names = datasetMgr.getAllDatasetNames()
    for signalWH, signalHH, target in _signalMerge:
        if signalWH in names and signalHH in names:
            datasetMgr.merge(target, [signalWH, signalHH])

def replaceQCDFromData(datasetMgr, datasetQCDdata):
    names = datasetMgr.getAllDatasetNames()
    index = names.index("QCD")
    names.pop(index)
    names.insert(index, datasetQCDdata.getName())
    datasetMgr.remove("QCD")
    datasetMgr.append(datasetQCDdata)
    datasetMgr.selectAndReorder(names)

## Creates a ratio histogram
#
# \param rootHisto1  TH1/TGraph dividend
# \param rootHisto2  TH1/TGraph divisor
# \param ytitle      Y axis title of the final ratio histogram
# \param isBinomial  True if the division has a binomial nature (e.g. efficnecy). Supported only for TH1s
#
# \return TH1 of rootHisto1/rootHisto2
#
# If the ratio has a binomial nature, the uncertainty estimation is
# done via TGraphAsymmErrors and Clopper-Pearson method (one of the
# methods recommended by statistics committee).
def _createRatio(rootHisto1, rootHisto2, ytitle, isBinomial=False):
    if isinstance(rootHisto1, ROOT.TH1) and isinstance(rootHisto2, ROOT.TH1):
        if isBinomial:
            eff = ROOT.TGraphAsymmErrors(rootHisto1, rootHisto2)
            styles.getDataStyle().apply(eff)
            return eff
        else:
            ratio = rootHisto1.Clone()
            ratio.SetDirectory(0)
            ratio.Divide(rootHisto2)
            styles.getDataStyle().apply(ratio)
            ratio.GetYaxis().SetTitle(ytitle)
            return ratio
    elif isinstance(rootHisto1, ROOT.TGraph) and isinstance(rootHisto2, ROOT.TGraph):
        if isBinomial:
            raise Exception("isBinomial is not supported for TGraph input")
        xvalues = []
        yvalues = []
        yerrs = []
        for i in xrange(0, rootHisto1.GetN()):
            yval = rootHisto2.GetY()[i]
            if yval == 0:
                continue
            xvalues.append(rootHisto1.GetX()[i])
            yvalues.append(rootHisto1.GetY()[i] / yval)
            err1 = max(rootHisto1.GetErrorYhigh(i), rootHisto1.GetErrorYlow(i))
            err2 = max(rootHisto2.GetErrorYhigh(i), rootHisto2.GetErrorYlow(i))
            yerrs.append( yvalues[i]* math.sqrt( _divideOrZero(err1, rootHisto1.GetY()[i])**2 +
                                                 _divideOrZero(err2, rootHisto2.GetY()[i])**2 ) )

        gr = ROOT.TGraphAsymmErrors()
        if len(xvalues) > 0:
            gr = ROOT.TGraphAsymmErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues),
                                        rootHisto1.GetEXlow(), rootHisto1.GetEXhigh(),
                                        array.array("d", yerrs), array.array("d", yerrs))
        return gr
    else:
        raise Exception("Arguments are of unsupported type, rootHisto1 is %s and rootHisto2 is %s" % (type(rootHisto1).__name__, type(rootHisto2).__name__))

def _divideOrZero(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator/denominator

## Copy (some) style attributes from one ROOT object to another
#
# \param src  Source object (copy attributes from)
# \param dst  Destination object (copy attributes to)
def copyStyle(src, dst):
    properties = []
    if hasattr(src, "GetLineColor") and hasattr(dst, "SetLineColor"):
        properties.extend(["LineColor", "LineStyle", "LineWidth"])
    if hasattr(src, "GetFillColor") and hasattr(dst, "SetFillColor"):
        properties.extend(["FillColor", "FillStyle"])
    if hasattr(src, "GetMarkerColor") and hasattr(dst, "SetMarkerColor"):
        properties.extend(["MarkerColor", "MarkerSize", "MarkerStyle"])

    for prop in properties:
        getattr(dst, "Set"+prop)(getattr(src, "Get"+prop)())


## Creates a horizontal line
#
# \param xmin    Minimum x value
# \param xmax    Maximum x value
# \param yvalue  Y value
#
# \return TGraph of line from (xmin, yvalue) to (xmax, yvalue)
#
# First use case: 1-line for ratio plots
def _createRatioLine(xmin, xmax, yvalue=1.0):
    line = ROOT.TGraph(2, array.array("d", [xmin, xmax]), array.array("d", [yvalue, yvalue]))
#    line.SetLineColor(ROOT.kBlack)
    line.SetLineColor(ROOT.kRed)
    line.SetLineWidth(2)
    line.SetLineStyle(3)
    return line

## Creates a cover pad
#
# \param xmin  X left coordinate
# \param ymin  Y lower coordinate
# \param xmax  X right coordinate
# \param ymax  Y upper coordinate
#
# If distributions and data/MC ratios are plotted on the same TCanvas
# such that the lower X axis of distributions TPad and the upper X
# axis of the ratio TPad coincide, the Y axis labels of the two TPads
# go on top of each others and it may happen that the greatest Y axis
# value of the lower TPad is directly on top of the smallest Y axis
# value of the upper TPad.
#
# This function can be used to create a blank TPad which is drawn
# after the lower TPad Y axis and before the upper TPad Y axis. Then
# only the smallest Y axis value of the upper TPad is drawn.
#
# See plots.DataMCPlot.draw() and plots.ComparisonPlot.draw() for
# examples.
#
# \return TPad 
def _createCoverPad(xmin=0.065, ymin=0.285, xmax=0.165, ymax=0.33):
    coverPad = ROOT.TPad("coverpad", "coverpad", xmin, ymin, xmax, ymax)
    coverPad.SetBorderMode(0)
    return coverPad

## Create cut box and/or line
#
# \param frame      TH1 representing the frame
# \param cutValue   Value of the cut
# \param fillColor  Fill color for the box
# \param box        If true, draw cut box
# \param line       If true, draw cut line
# \param kwargs     Keyword arguments (\a lessThan or \a greaterThan, forwarded to histograms.isLessThan())
def _createCutBoxAndLine(frame, cutValue, fillColor=18, box=True, line=True, **kwargs):
    xmin = frame.GetXaxis().GetXmin()
    xmax = frame.GetXaxis().GetXmax()
    ymin = frame.GetYaxis().GetXmin()
    ymax = frame.GetYaxis().GetXmax()
    
    ret = []

    if box:
        if histograms.isLessThan(**kwargs):
            xmin = cutValue
        else:
            xmax = cutValue

        b = ROOT.TBox(xmin, ymin, xmax, ymax)
        b.SetFillColor(fillColor)
        ret.append(b)

    if line:
        l = ROOT.TLine(cutValue, ymin, cutValue, ymax)
        l.SetLineWidth(3)
        l.SetLineStyle(ROOT.kDashed)
        l.SetLineColor(ROOT.kBlack)
        ret.append(l)

    return ret

## Helper function for creating a histograms.Histo object from a ROOT object based on the ROOT object type
#
# \param rootObject   ROOT object (TH1 or TGraph)
# \param kwargs       Keyword arguments (forwarded to histograms.Histo.__init__() or histograms.HistoGraph.__init__())
def _createHisto(rootObject, **kwargs):
    if isinstance(rootObject, ROOT.TH1):
        return histograms.Histo(rootObject, rootObject.GetName(), **kwargs)
    elif isinstance(rootObject, ROOT.TGraph):
        return histograms.HistoGraph(rootObject, rootObject.GetName(), **kwargs)
    elif not isinstance(rootObject, histograms.Histo):
        raise Exception("rootObject is not TH1, TGraph, nor histograms.Histo, it is %s" % type(rootObject).__name__)

    return rootObject

## Base class for plots
#
# This class can also be used as for plots which don't need the
# features provided by the derived classes. E.g. for plots without the
# need for ratio pad, or stacking of MC histograms, this class is perfect.
#
# In addition of the plot histograms/graphs, the class also provides
# hooks for other objects (lines, arrows, text, whatever implementing
# Draw() method) to be drawn before and after the plot
# histograms/graphs.
class PlotBase:
    ## Construct plot from DatasetManager and histogram name
    #
    # \param datasetRootHistos  List of dataset.DatasetRootHistoBase or histograms.Histo or TH1/TGraph objects to plot
    # \param saveFormats        List of suffixes for formats for which to save the plot
    def __init__(self, datasetRootHistos=[], saveFormats=[".png", ".eps", ".C"]):
        # Create the histogram manager
        if len(datasetRootHistos) > 0:
            if isinstance(datasetRootHistos[0], dataset.DatasetRootHistoBase):
                for i, drh in enumerate(datasetRootHistos[1:]):
                    if not isinstance(drh, dataset.DatasetRootHistoBase):
                        raise Exception("Input types can't be a mixture of DatasetRootHistoBase and something, datasetRootHistos[%d] is %s" % (i, type(drh).__name__))

                self.histoMgr = histograms.HistoManager(datasetRootHistos = datasetRootHistos)
            else:
                histoList = datasetRootHistos
                if isinstance(datasetRootHistos[0], ROOT.TH1):
                    for i, h in enumerate(datasetRootHistos[1:]):
                        if not isinstance(h, ROOT.TH1):
                            raise Exception("Input types can't be a mixture of ROOT.TH1 and something, datasetRootHistos[%d] is %s" % (i, type(h).__name__))
                    histoList = [histograms.Histo(th1, th1.GetName()) for th1 in datasetRootHistos]
                elif isinstance(datasetRootHistos[0], ROOT.TGraph):
                    for i, h in enumerate(datasetRootHistos[1:]):
                        if not isinstance(h, ROOT.TGraph):
                            raise Exception("Input types can't be a mixture of ROOT.TGraph and someting, datasetRootHistos[%d] is %s" % (i, type(h).__name__))
                        if len(h.GetName()) == 0:
                            raise Exception("For TGraph input, the graph name must be set with TGraph.SetName() (name for datasetRootHistos[%d] is empty)" % i)
                    histoList = [histograms.HistoGraph(gr, gr.GetName()) for gr in datasetRootHistos]

                self.histoMgr = histograms.HistoManager()
                for histo in histoList:
                    self.histoMgr.appendHisto(histo)
        else:
            self.histoMgr = histograms.HistoManager()


        # Save the format
        self.saveFormats = saveFormats

        self.plotObjectsBefore = []
        self.plotObjectsAfter = []

    ## Set the default legend styles
    #
    # Default is "F", except for data "P" and for signal MC "L"
    # 
    # Intended to be called from the deriving classes
    def _setLegendStyles(self):
        self.histoMgr.setHistoLegendStyleAll("F")
        for h in self.histoMgr.getHistos():
            if h.isData():
                h.setLegendStyle("P")
            elif "TTTo" in h.getName():
                h.setLegendStyle("L")

    ## Set the default legend labels
    #
    # Labels are taken from the plots._legendLabels dictionary
    #
    # Intended to be called from the deriving classes
    def _setLegendLabels(self):
        self.histoMgr.forEachHisto(SetLegendLabel(_legendLabels))

    ## Set the default plot styles
    #
    # Styles are taken from the plots._plotStyles dictionary
    #
    # Intended to be called from the deriving classes
    def _setPlotStyles(self):
        self.histoMgr.forEachHisto(SetPlotStyle(_plotStyles))
        if self.histoMgr.hasHisto("Data"):
            self.histoMgr.setHistoDrawStyle("Data", "EP")

    ## Set default legend labels and styles, and plot styles
    def setDefaultStyles(self):
        self._setLegendStyles()
        self._setLegendLabels()
        self._setPlotStyles()

    ## Get the bin width (assuming it is constant)
    def binWidth(self):
        return self.histoMgr.getHistos()[0].getBinWidth(1)

    ## Add a format for which to save the plot
    #
    # \param format  Suffix recognised by ROOT
    def appendSaveFormat(self, format):
        self.saveFormats.append(format)

    ## Set the legend object
    # 
    # \param legend   TLegend object
    #
    # All histograms in the plot are added to the legend object
    def setLegend(self, legend):
        self.legend = legend
        self.histoMgr.addToLegend(legend)

    ## Remove the legend object
    def removeLegend(self):
        delattr(self, "legend")

    ## Add an additional object to be drawn before the plot histograms/graphs
    #
    # \param obj      Object
    # \param option   Drawing option (given to obj.Draw())
    def prependPlotObject(self, obj, option=""):
        self.plotObjectsBefore.append( (obj, option) )

    ## Add an additional object to be drawn after the plot histograms/graphs
    #
    # \param obj      Object
    # \param option   Drawing option (given to obj.Draw())
    def appendPlotObject(self, obj, option=""):
        self.plotObjectsAfter.append( (obj, option) )

    ## Add cut box and/or line
    #
    # \param args    Positional arguments (forwarded to plots._createCutBoxAndLine())
    # \param kwargs  Keyword arguments (forwarded to plots._createCutBoxAndLine())
    def addCutBoxAndLine(self, *args, **kwargs):
        objs = _createCutBoxAndLine(self.getFrame(), *args, **kwargs)
        for o in objs:
            self.appendPlotObject(o)

    ## Add MC uncertainty histogram
    def addMCUncertainty(self):
        self.histoMgr.addMCUncertainty(styles.getErrorStyle())

    ## Create TCanvas and frames for the histogram and a data/MC ratio
    #
    # \param filename   Name for TCanvas (becomes the file name)
    # \param kwargs     Keyword arguments, forwarded to histograms.CanvasFrame.__init__()
    def createFrame(self, filename, **kwargs):
        self.cf = histograms.CanvasFrame(self.histoMgr, filename, **kwargs)
        self.frame = self.cf.frame

    ## Set the name of the canvas for the output file
    #
    # \param filename  New name
    def setFileName(self, filename):
        self.cf.canvas.SetName(filename)

    ## Get the frame TH1
    def getFrame(self):
        return self.frame

    ## Get the TPad
    def getPad(self):
        return self.cf.pad

    ## Draw the plot
    #
    # Draw also the legend if one has been associated
    def draw(self):
        for obj, option in self.plotObjectsBefore:
            obj.Draw(option+"same")

        self.histoMgr.draw()

        for obj, option in self.plotObjectsAfter:
            obj.Draw(option+"same")

        if hasattr(self, "legend"):
            self.legend.Draw()

        # Redraw the axes in order to get the tick marks on top of the
        # histogram
        self.getPad().RedrawAxis()

    ## Add text for integrated luminosity
    #
    # \param x   X coordinate (in NDC, None for the default value)
    # \param y   Y coordinate (in NDC, None for the default value)
    def addLuminosityText(self, x=None, y=None):
        self.histoMgr.addLuminosityText(x, y)

    ## Save the plot to file(s)
    #
    # \param formats   Save to these formats (if not given, the values
    #                  given in the constructor and in
    #                  appendSaveFormat() are used
    def save(self, formats=None):
        if formats == None:
            formats = self.saveFormats

        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

        for f in formats:
            self.cf.canvas.SaveAs(f)

        ROOT.gErrorIgnoreLevel = backup

    ## \var histoMgr
    # histograms.HistoManager object for histogram management
    ## \var saveFormats
    # List of formats to which to save the plot
    ## \var plotObjectsBefore
    # List of objects to be drawn before histoMgr
    ## \var plotObjectsAfter
    # List of objects to be drawn after histoMgr
    ## \var legend
    # TLegend object if legend has been added to the plot
    ## \var cf
    # histograms.CanvasFrame object to hold the TCanvas and TH1 for frame
    ## \var frame
    # TH1 object for the frame (from the cf object)

## Base class for plots with ratio (intended for multiple inheritance)
#
# This class should not be instantiated!
class PlotRatioBase:
    ## Constructor
    def __init__(self):
        self.ratioPlotObjectsBefore = []
        self.ratioPlotObjectsAfter = []
        self.ratios = []

    ## Add an additional object to be drawn before the ratio histogram(s)
    #
    # \param obj      Object
    # \param option   Drawing option (given to obj.Draw())
    def prependPlotObjectToRatio(self, obj, option=""):
        self.ratioPlotObjectsBefore.append( (obj, option) )

    ## Add an additional object to be drawn after the ratio histogram(s)
    #
    # \param obj      Object
    # \param option   Drawing option (given to obj.Draw())
    def appendPlotObjectToRatio(self, obj, option=""):
        self.ratioPlotObjectsAfter.append( (obj, option) )

    ## Add cut box and/or line to the ratio pad
    #
    # \param args    Positional arguments (forwarded to plots._createCutBoxAndLine())
    # \param kwargs  Keyword arguments (forwarded to plots._createCutBoxAndLine())
    def addCutBoxAndLineToRatio(self, *args, **kwargs):
        if len(self.ratios) == 0:
            return

        objs = _createCutBoxAndLine(self.getFrame2(), *args, **kwargs)
        for o in objs:
            self.prependPlotObjectToRatio(o)

    ## Get the upper frame TH1
    def getFrame1(self):
        return self.cf.frame1

    ## Get the lower frame TH1
    def getFrame2(self):
        return self.cf.frame2

    ## Get the upper TPad
    def getPad1(self):
        return self.cf.pad1

    ## Get the lower TPad
    def getPad2(self):
        return self.cf.pad2

    ## Set the ratio histograms
    #
    # \param ratios  List of TH1/TGraph objects
    def setRatios(self, ratios):
        self.ratios = []
        self.extendRatios(ratios)

    ## Create Histo object from ROOT object
    #
    # \param ratio  TH1/TGraph object
    #
    # \return histograms.Histo object
    #
    # Main point of this is setting the drawing style to 'EP'.
    #
    # Intended for internal use only
    def _createRatioObject(self, ratio):
        r = _createHisto(ratio)
        r.setDrawStyle("EP")
        return r

    ## Add TH1/TGraph object to ratio pad
    #
    # \param ratio  TH1/TGraph object
    def appendRatio(self, ratio):
        self.ratios.append(self._createRatioObject(ratio))

    ## Addend TH1/TGraph objects to ratio pad
    #
    # \param ratios  List of TH1/TGraph objects
    def extendRatios(self, ratios):
        self.ratios.extend([self._createRatioObject(r) for r in ratios])

    ## Create TCanvas and frame with ratio pad for single ratio
    #
    # \param filename         Name of the frame
    # \param numerator        Numerator TH1/TGraph
    # \param denominator      Denominator TH1/TGraph
    # \param ytitle           Y axis title for the ratio pad
    # \param invertRatio      Invert the roles of numerator and denominator
    # \param ratioIsBinomial  True for binomial ratio (e.g. efficiency)
    # \param kwargs           Keyword arguments (forwarded to _createFrame())
    #
    # Intended for internal use only
    def _createFrameRatio(self, filename, numerator, denominator, ytitle, invertRatio=False, ratioIsBinomial=False, **kwargs):
        (num, denom) = (numerator, denominator)
        if invertRatio:
            (num, denom) = (denom, num)

        self.setRatios([_createRatio(num, denom, ytitle, isBinomial=ratioIsBinomial)])
        self._createFrame(filename, **kwargs)

    ## Create TCanvas and frame with ratio pad for many ratios
    #
    # \param filename         Name of the frame
    # \param numerators       List of numerator TH1/TGraph objects
    # \param denominators     List of denominator TH1/TGraph objects
    # \param ytitle           Y axis title for the ratio pad
    # \param invertRatio      Invert the roles of numerator and denominator
    # \param ratioIsBinomial  True for binomial ratio (e.g. efficiency)
    # \param kwargs           Keyword arguments (forwarded to _createFrame())
    #
    # Intended for internal use only
    def _createFrameRatioMany(self, filename, numerators, denominator, invertRatio=False, ratioIsBinomial=False, **kwargs):
        self.ratios = []
        for numer in numerators:
            (num, denom) = (numer, denominator)
            if invertRatio:
                (num, denom) = (denom, num)
            ratio = _createRatio(num, denom, "Ratio", isBinomial=ratioIsBinomial)
            copyStyle(num, ratio)
            self.appendRatio(ratio)

        self._createFrame(filename, **kwargs)

    ## Create TCanvas with ratio pads and frames
    #
    # \param filename       Name of frame
    # \param coverPadOpts   Options for overriding cover pad placement (see plots._createCoverPad)
    # \param kwargs         Keyword arguments (forwarded to histograms.CanvasFrameTwo.__init__())
    def _createFrame(self, filename, coverPadOpts={}, **kwargs):
        self.cf = histograms.CanvasFrameTwo(self.histoMgr, self.ratios, filename, **kwargs)
        self.frame = self.cf.frame
        self.cf.frame2.GetYaxis().SetNdivisions(505)
        self.coverPadOpts = coverPadOpts

    ## Draw the ratio histograms to the ratio pad
    def _draw(self):
        if len(self.ratios) == 0:
            return

        self.cf.canvas.cd(2)

        for obj, option in self.ratioPlotObjectsBefore:
            obj.Draw(option+"same")

        self.ratioLine = _createRatioLine(self.cf.frame.getXmin(), self.cf.frame.getXmax())
        self.ratioLine.Draw("L")
       
        ratios = self.ratios[:]
        ratios.reverse()
        for r in ratios:
            r.draw("same")

        for obj, option in self.ratioPlotObjectsAfter:
            obj.Draw(option+"same")

        # Redraw the axes in order to get the tick marks on top of the
        # histogram
        self.getPad2().RedrawAxis()
        self.getPad1().RedrawAxis()

        self.cf.canvas.cd()

        # Create an empty, white-colored pad to hide the topmost
        # label of the y-axis of the lower pad. Then move the
        # upper pad on top, so that the lowest label of the y-axis
        # of it is shown
        self.ratioCoverPad = _createCoverPad(**self.coverPadOpts)
        self.ratioCoverPad.Draw()

        self.cf.canvas.cd(1)
        self.cf.pad1.Pop() # Move the first pad on top

    ## \var ratios
    # Holds the TH1 for data/MC ratio, if exists
    ## \var ratioLine
    # Holds the TGraph for ratio line, if ratio exists
    ## \var ratioCoverPad
    # Holds TPad to cover the larget Y axis value of the ratio TPad,
    # if ratio exists

## Base class for plots with same histogram from many datasets.
class PlotSameBase(PlotBase):
    ## Construct from DatasetManager and a histogram path
    #
    # \param datasetMgr      DatasetManager for datasets
    # \param name            Path of the histogram in the ROOT files
    # \param normalizeToOne  Should the histograms be normalized to unit area?
    # \param kwargs          Keyword arguments, forwarded to PlotBase.__init__()
    def __init__(self, datasetMgr, name, normalizeToOne=False, **kwargs):
        PlotBase.__init__(self, datasetMgr.getDatasetRootHistos(name), **kwargs)
        self.datasetMgr = datasetMgr
        self.rootHistoPath = name
        self.normalizeToOne = normalizeToOne

    ## Get the path of the histograms in the ROOT files
    def getRootHistoPath(self):
        return self.rootHistoPath

    ## Stack MC histograms
    #
    # \param stackSignal  Should the signal histograms be stacked too?
    #
    # Signal histograms are identified with plots.isSignal() function
    def stackMCHistograms(self, stackSignal=False):
        #mcNames = self.datasetMgr.getMCDatasetNames()
        mcNames = [h.getName() for h in filter(lambda h: h.isMC(), self.histoMgr.getHistos())]
        mcNamesNoSignal = filter(lambda n: not isSignal(n) and not "StackedMCSignal" in n, mcNames)
        if not stackSignal:
            mcNames = mcNamesNoSignal

        # Leave the signal datasets unfilled
        self.histoMgr.forEachHisto(UpdatePlotStyleFill( _plotStyles, mcNamesNoSignal))
        self.histoMgr.stackHistograms("StackedMC", mcNames)

    ## Stack MC signal histograms
    def stackMCSignalHistograms(self):
        mcSignal = filter(lambda n: isSignal(n), self.datasetMgr.getMCDatasetNames())
        self.histoMgr.stackHistograms("StackedMCSignal", mcSignal)

    ## Add MC uncertainty band
    def addMCUncertainty(self):
        if not self.histoMgr.hasHisto("StackedMC"):
            raise Exception("Must call stackMCHistograms() before addMCUncertainty()")
        self.histoMgr.addMCUncertainty(styles.getErrorStyle(), nameList=["StackedMC"])

    ## Create TCanvas and frame
    #
    # \param filename   Frame name
    # \param kwargs     Keyword arguments (forwarded to plots.PlotBase.createFrame())
    def createFrame(self, filename, **kwargs):
        self._normalizeToOne()
        PlotBase.createFrame(self, filename, **kwargs)

    ## Helper function to do the work for "normalization to one"
    def _normalizeToOne(self):
        # First check that the normalizeToOne is enabled
        if not self.normalizeToOne:
            return

        # If the MC histograms have not been stacked, the
        # normalization is straighforward (normalize all histograms to
        # one)
        if not self.histoMgr.hasHisto("StackedMC"):
            self.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
            return

        # Normalize the stacked histograms
        handled = []
        h = self.histoMgr.getHisto("StackedMC")
        sumInt = h.getSumRootHisto().Integral()
        for th1 in h.getAllRootHistos():
            dataset._normalizeToFactor(th1, 1.0/sumInt)
        handled.append("StackedMC")

        # Normalize the the uncertainty histogram if it exists
        if self.histoMgr.hasHisto("MCuncertainty"):
            dataset._normalizeToFactor(self.histoMgr.getHisto("MCuncertainty").getRootHisto(), 1.0/sumInt)
            handled.append("MCuncertainty")
        
        # Normalize the rest
        for h in self.histoMgr.getHistos():
            if not h.getName() in handled:
                dataset._normalizeToOne(h.getRootHisto())

    ## \var datasetMgr
    # datasets.DatasetManager object to have the datasets at hand
    ## \var rootHistoPath
    # Path to the histogram in the ROOT files
    ## \var normalizeToOne
    # Flag to indicate if histograms should be normalized to unit area

## Class for MC plots.
#
#
#
class MCPlot(PlotSameBase):
    ## Construct from DatasetManager and a histogram path
    #
    # \param datasetMgr      DatasetManager for datasets
    # \param name            Path of the histogram in the ROOT files
    # \param kwargs          Keyword arguments, see below
    #
    # <b>Keyword arguments</b>
    # \li \a normalizeToOne           Normalize the histograms to one (True/False)
    # \li \a normalizeByCrossSection  Normalize the histograms by the dataset cross sections (True/False)
    # \li \a normalizeToLumi          Normalize the histograms to a given luminosity (number)
    # \li Rest are forwarded to PlotSameBase.__init__()
    #
    # One of the normalization keyword arguments must be given, only
    # one can be True or have a number.
    def __init__(self, datasetMgr, name, **kwargs):
        arg = {}
        normalizationModes = ["normalizeToOne", "normalizeByCrossSection", "normalizeToLumi"]
        for a in normalizationModes:
            if a in kwargs and kwargs[a]:
                if len(arg) != 0:
                    raise Exception("Only one of %s can be given, got %s and %s" % (",".join(normalizationModes), arg.items()[0], a))
                arg[a] = kwargs[a]
                # This one we have to keep
                if a != "normalizeToOne":
                    del kwargs[a]

        if len(arg) == 0:
            raise Exception("One of the %s must be given" % ",".join(normalizationModes))

        # Base class constructor
        PlotSameBase.__init__(self, datasetMgr, name, **kwargs)
        
        # Normalize the histograms
        if self.normalizeToOne or arg.get("normalizeByCrossSection", False):
            self.histoMgr.normalizeMCByCrossSection()
        else:
            self.histoMgr.normalizeMCToLuminosity(arg["normalizeToLumi"])
        
        self._setLegendStyles()
        self._setLegendLabels()
        self._setPlotStyles()

    ## This is provided to have similar interface with DataMCPlot
    def createFrameFraction(self, filename, **kwargs):
        if "opts2" in kwargs:
            del kwargs["opts2"]
        self.createFrame(filename, **kwargs)

## Class for data-MC comparison plot.
# 
# Several assumptions have been made for this plotting class. If these
# are not met, one should consider either adding the feature to this
# class (if the required change is relatively small), or creating
# another class (if the change is large).
# <ul>
# <li> There is always one histogram with the name "Data" for collision data </li>
# <li> There is always at least one MC histogram </li>
# <li> Only the MC histograms are stacked, and it should be done with the
#      stackMCHistograms() method </li>
# <li> Data/MC ratio pad can be added to the same TCanvas, the MC
#      considered in the ratio are the stacked ones </li>
# <li> The MC is normalized by the integrated luminosity of the collision
#      data by default
#      <ul>
#      <li> Normalization to unit area (normalizeToOne) is also supported
#           such that all non-stacked histograms are normalized to unit
#           area, and the total area of stacked histograms is normalized to
#           unit area while the ratios of the individual datasets is
#           determined from the cross sections. The support is in the base class. </li>
#     </ul></li>
# </ul>
class DataMCPlot(PlotSameBase, PlotRatioBase):
    ## Construct from DatasetManager and a histogram path
    #
    # \param datasetMgr      DatasetManager for datasets
    # \param name            Path of the histogram in the ROOT files
    # \param kwargs          Keyword arguments, forwarded to PlotSameBase.__init__()
    def __init__(self, datasetMgr, name, normalizeToLumi=None, **kwargs):
        PlotSameBase.__init__(self, datasetMgr, name, **kwargs)
        PlotRatioBase.__init__(self)
        
        # Normalize the MC histograms to the data luminosity
        if normalizeToLumi == None:
            self.histoMgr.normalizeMCByLuminosity()
        else:
            self.histoMgr.normalizeMCToLuminosity(normalizeToLumi)

        self._setLegendStyles()
        self._setLegendLabels()
        self._setPlotStyles()

    ## Create TCanvas and frames for the histogram and a data/MC ratio
    #
    # \param filename     Name for TCanvas (becomes the file name)
    # \param createRatio  Create also the ratio pad?
    # \param kwargs       Keyword arguments, forwarded to PlotSameBase.createFrame() or PlotRatioBase._createFrameRatio()
    def createFrame(self, filename, createRatio=False, **kwargs):
        if not createRatio:
            PlotSameBase.createFrame(self, filename, **kwargs)
        else:
            if not self.histoMgr.hasHisto("StackedMC"):
                raise Exception("Must call stackMCHistograms() before createFrame() with ratio")

            self._normalizeToOne()
            self._createFrameRatio(filename,
                                   self.histoMgr.getHisto("Data").getRootHisto(),
                                   self.histoMgr.getHisto("StackedMC").getSumRootHisto(),
                                   "Data/MC", **kwargs)

    ## Create TCanvas and frames for the histogram and a data/MC ratio
    #
    # \param filename   Name for TCanvas (becomes the file name)
    # \param kwargs     Keyword arguments, forwarded to createFrame()
    def createFrameFraction(self, filename, **kwargs):
        print "Please move to use createFrame(..., createRatio=True) instead of createFrameFraction()"
        self.createFrame(filename, createRatio=True, **kwargs)

    ## Add cut box and/or line
    #
    # \param args    Positional arguments (forwarded to plots._createCutBoxAndLine())
    # \param kwargs  Keyword arguments (forwarded to plots._createCutBoxAndLine())
    def addCutBoxAndLine(self, *args, **kwargs):
        PlotSameBase.addCutBoxAndLine(self, *args, **kwargs)
        PlotRatioBase.addCutBoxAndLineToRatio(self, *args, **kwargs)

    def draw(self):
        PlotSameBase.draw(self)
        PlotRatioBase._draw(self)

## Same goal as dataset.DataMCPlot, but with explicit histograms instead of construction from DatasetManager
#
# From the given histograms, data and MC histograms are identified by
# their name such that data histogram name(s) are given, and all other
# histograms than data histograms are assumed to be MC. The default
# data histogram name is "Data", but this can be set with
# setDataDatasetNames() method.
class DataMCPlot2(PlotBase, PlotRatioBase):
    ## Constructor
    #
    # \param histos           List of histograms.Histo or TH1/TGraph objects to plot
    # \param normalizeToOne   Should the histograms be normalized to unit area?
    # \param kwargs           Keyword arguments (forwarded to plots.PlotBase.__init__()
    def __init__(self, histos, normalizeToOne=False, **kwargs):
        PlotBase.__init__(self, histos, **kwargs)
        PlotRatioBase.__init__(self)
        self.normalizeToOne = normalizeToOne
        self.dataDatasetNames = ["Data"]

    def setDefaultStyles(self):
        self._setLegendStyles()
        self._setLegendLabels()
        self._setPlotStyles()

    ## Set the names of data histograms
    #
    # \param names   List of names of data histograms
    def setDataDatasetNames(self, names):
        self.dataDatasetNames = names

    
    ## Stack MC histograms
    #
    # \param stackSignal  Should the signal histograms be stacked too?
    #
    # Signal histograms are identified with plots.isSignal() function
    def stackMCHistograms(self, stackSignal=False):
        mcNames = filter(lambda n: not n in self.dataDatasetNames, [h.getName() for h in self.histoMgr.getHistos()])
        mcNamesNoSignal = filter(lambda n: not isSignal(n) and not "StackedMCSignal" in n, mcNames)
        if not stackSignal:
            mcNames = mcNamesNoSignal

        # Leave the signal datasets unfilled
        self.histoMgr.forEachHisto(UpdatePlotStyleFill( _plotStyles, mcNamesNoSignal))
        self.histoMgr.stackHistograms("StackedMC", mcNames)

    ## Stack MC signal histograms
    def stackMCSignalHistograms(self):
        mcSignal = filter(lambda n: isSignal(n), self.datasetMgr.getMCDatasetNames())
        self.histoMgr.stackHistograms("StackedMCSignal", mcSignal)

    ## Add MC uncertainty band
    def addMCUncertainty(self):
        if not self.histoMgr.hasHisto("StackedMC"):
            raise Exception("Must call stackMCHistograms() before addMCUncertainty()")
        self.histoMgr.addMCUncertainty(styles.getErrorStyle(), nameList=["StackedMC"])

    ## Create TCanvas and frames for the histogram and a data/MC ratio
    #
    # \param filename     Name for TCanvas (becomes the file name)
    # \param createRatio  Create also the ratio pad?
    # \param kwargs       Keyword arguments, forwarded to PlotSameBase.createFrame() or PlotRatioBase._createFrameRatio()
    def createFrame(self, filename, createRatio=False, **kwargs):
        self._normalizeToOne()
        if not createRatio:
            PlotBase.createFrame(self, filename, **kwargs)
        else:
            if not self.histoMgr.hasHisto("StackedMC"):
                raise Exception("Must call stackMCHistograms() before createFrameFraction()")

            self._normalizeToOne()
            self._createFrameRatio(filename,
                                   self.histoMgr.getHisto("Data").getRootHisto(),
                                   self.histoMgr.getHisto("StackedMC").getSumRootHisto(),
                                   "Data/MC", **kwargs)

    ## Set the integrated luminosity of the data
    #
    # \param lumi   Integrated luminosity (in pb^-1)
    def setLuminosity(self, lumi):
        self.luminosity = lumi

    def addLuminosityText(self, x=None, y=None):
        if hasattr(self, "luminosity"):
            histograms.addLuminosityText(x, y, self.luminosity)

    ## Add cut box and/or line
    #
    # \param args    Positional arguments (forwarded to plots._createCutBoxAndLine())
    # \param kwargs  Keyword arguments (forwarded to plots._createCutBoxAndLine())
    def addCutBoxAndLine(self, *args, **kwargs):
        PlotBase.addCutBoxAndLine(self, *args, **kwargs)
        PlotRatioBase.addCutBoxAndLineToRatio(self, *args, **kwargs)

    def draw(self):
        PlotBase.draw(self)
        PlotRatioBase._draw(self)

    ## Helper function to do the work for "normalization to one"
    def _normalizeToOne(self):
        # First check that the normalizeToOne is enabled
        if not self.normalizeToOne:
            return

        # If the MC histograms have not been stacked, the
        # normalization is straighforward (normalize all histograms to
        # one)
        if not self.histoMgr.hasHisto("StackedMC"):
            self.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
            return

        # Normalize the stacked histograms
        handled = []
        h = self.histoMgr.getHisto("StackedMC")
        sumInt = h.getSumRootHisto().Integral()
        for th1 in h.getAllRootHistos():
            dataset._normalizeToFactor(th1, 1.0/sumInt)
        handled.append("StackedMC")

        # Normalize the the uncertainty histogram if it exists
        if self.histoMgr.hasHisto("MCuncertainty"):
            dataset._normalizeToFactor(self.histoMgr.getHisto("MCuncertainty").getRootHisto(), 1.0/sumInt)
            handled.append("MCuncertainty")
        
        # Normalize the rest
        for h in self.histoMgr.getHistos():
            if not h.getName() in handled:
                dataset._normalizeToOne(h.getRootHisto())


## Class to create comparison plots of two quantities.
#
# Although plots.PlotBase can be used to plot two arbitrary
# histograms, with this class you can also draw the ratio pad.
class ComparisonPlot(PlotBase, PlotRatioBase):
    ## Constructor.
    #
    # \param datasetRootHisto1  Numerator dataset.DatasetRootHistoBase or histograms.Histo or TH1/TGraph object
    # \param datasetRootHisto2  Denominator dataset.DatasetRootHistoBase or histograms.Histo or TH1/TGraph object
    #
    # The possible ratio is calculated as datasetRootHisto1/datasetRootHisto2
    def __init__(self, datasetRootHisto1, datasetRootHisto2, **kwargs):
        PlotBase.__init__(self,[datasetRootHisto1, datasetRootHisto2], **kwargs)
        PlotRatioBase.__init__(self)

    ## Create TCanvas and frames for the histogram and a data/MC ratio
    #
    # \param filename     Name for TCanvas (becomes the file name)
    # \param createRatio  Create also the ratio pad?
    # \param invertRatio  Invert the roles of numerator and denominator
    # \param coverPadOpts Options for cover TPad, forwarded to _createCoverPad()
    # \param kwargs       Keyword arguments, forwarded to PlotBase.createFrame() or PlotRatioBase._createFrameRatio()
    #
    # By default the ratio is calculated as __init__() argument
    # datasetRootHisto1/datasetRootHisto2. With \a invertRatio this
    # can be reversed to datasetRootHisto2/datasetRootHisto1.
    def createFrame(self, filename, createRatio=False, invertRatio=False, coverPadOpts={}, **kwargs):
        if not createRatio:
            PlotBase.createFrame(self, filename, **kwargs)
        else:
            histos = self.histoMgr.getHistos()
            self._createFrameRatio(filename, histos[0].getRootHisto(), histos[1].getRootHisto(), "Ratio",
                                   invertRatio=invertRatio, coverPadOpts=coverPadOpts, **kwargs)

    ## Add cut box and/or line
    #
    # \param args    Positional arguments (forwarded to plots._createCutBoxAndLine())
    # \param kwargs  Keyword arguments (forwarded to plots._createCutBoxAndLine())
    def addCutBoxAndLine(self, *args, **kwargs):
        PlotBase.addCutBoxAndLine(self, *args, **kwargs)
        PlotRatioBase.addCutBoxAndLineToRatio(self, *args, **kwargs)

    def draw(self):
        PlotBase.draw(self)
        PlotRatioBase._draw(self)

    ## Set the integrated luminosity of the data
    #
    # \param lumi   Integrated luminosity (in pb^-1)
    def setLuminosity(self, lumi):
        self.luminosity = lumi

    def addLuminosityText(self, x=None, y=None):
        if hasattr(self, "luminosity"):
            histograms.addLuminosityText(x, y, self.luminosity)



## Class to compare many histograms to one histogram
#
# One histogram is treated as a reference histogram, and all other
# histograms are compared with respect to that. Although
# plots.PlotBase can be used to plot arbitrary number of arbitrary
# histograms, with this class you can also draw the ratio pad.
class ComparisonManyPlot(PlotBase, PlotRatioBase):
    ## Constructor
    #
    # \param histoReference    Reference dataset.DatasetRootHistoBase or histograms.Histo or TH1/TGraph object 
    # \param histoCompares     List of dataset.DatasetRootHistoBase or histograms.Histo or TH1/TGraph objects to compare with the reference
    def __init__(self, histoReference, histoCompares, **kwargs):
        PlotBase.__init__(self, [histoReference]+histoCompares, **kwargs)
        PlotRatioBase.__init__(self)

        # To allow reordering of histograms within histogram manager,
        # only assume the name of the reference histogram stays the
        # same
        self.referenceName = self.histoMgr.getHistos()[0].getName()

    ## Create TCanvas and frame
    #
    # 
    # \param filename     Name for TCanvas (becomes the file name)
    # \param createRatio  Create also the ratio pad?
    # \param invertRatio  Invert the roles of numerator and denominator
    # \param kwargs       Keyword arguments, forwarded to PlotBase.createFrame() or PlotRatioBase._createFrameRatioMany()
    #
    # By default the ratios are calculated as comparisons/reference,
    # with \a invertRatio this can be reversed to
    # reference/comparisons.
    def createFrame(self, filename, createRatio=False, invertRatio=False, coverPadOpts={}, **kwargs):
        if not createRatio:
            PlotBase.createFrame(self, filename, **kwargs)
        else:
            histos = filter(lambda h: h.getName() != self.referenceName, self.histoMgr.getHistos())
            reference = self.histoMgr.getHisto(self.referenceName)
            self._createFrameRatioMany(filename, [h.getRootHisto() for h in histos], reference.getRootHisto(),
                                       invertRatio=invertRatio, coverPadOpts={}, **kwargs)

    ## Add cut box and/or line
    #
    # \param args    Positional arguments (forwarded to plots._createCutBoxAndLine())
    # \param kwargs  Keyword arguments (forwarded to plots._createCutBoxAndLine())
    def addCutBoxAndLine(self, *args, **kwargs):
        PlotBase.addCutBoxAndLine(self, *args, **kwargs)
        PlotRatioBase.addCutBoxAndLineToRatio(self, *args, **kwargs)

    def draw(self):
        PlotBase.draw(self)
        PlotRatioBase._draw(self)

    ## Set the integrated luminosity of the data
    #
    # \param lumi   Integrated luminosity (in pb^-1)
    def setLuminosity(self, lumi):
        self.luminosity = lumi

    def addLuminosityText(self, x=None, y=None):
        if hasattr(self, "luminosity"):
            histograms.addLuminosityText(x, y, self.luminosity)


## Base class for plot drawing functions
#
# The point of this class (and the deriving classes) is to provide
# sensible defaults for drawing the plots (plots.PlotBase and the
# deriving classes). The defaults can be easily overridden both
# globally and per function call.
#
# The customisations covered here are below. For possible default
# values please see the constructor (__init__())
# \li Rebinning
# \li Stacking of MC histograms, and adding total MC (stat) uncertainty
# \li Is y axis in log or linear scale
# \li Frame bounds (X/Y axis min/max) (separate defaults for linear and log scale, and for ratio pad)
# \li Adding the ratio pad
# \li Legend positioning
# \li Adding cut box and/or line
# \li Arbitrary customisation function
# \li X and Y axis titles (x axis title is required explicitly, for Y axis title a default is provided)
# \li Drawing the luminosity value
#
# The default values can be set in the constructor, and later modified
# with setDefaults(). In each function call the default values can be
# overridden with the call arguments. The keyword argument names for
# the setting/modifying the parameters are the same for all ways.
#
# With this class, adding a new plot to a plotscript can be as short
# as one line of code. There are plenty of examples in the existing
# plot scripts, but some examples are shown below to demonstrate the
# possibilities. In below, \a plot refers always to a plots.PlotBase
# object.
# \code
# # Draw a plot, save it to file "filename", Y axis is in log scale,
# # X axis minimum is set to 10 and Y axis maximum to 100, other are taken from defaults
# plots.drawPlot(plot, "filename", "X axis title", ylabel="Y axis title", log=True, opts={"xmin":10, "ymax": 100}) 
#
# # Modify the defaults, from now on on each drawPlot() call the ratio pad is created, MC histograms are stacked,
# # MC total (stat) uncertainty is added, and total integrated luminosity is drawn
# plots.drawPlot.setDefaults(ratio=True, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True)
#
# 
# # Create a new plot drawer, with log scale Y axis, adding the ratio pad,
# # and ratio pad to have Y axis minimum to 0 and maximum to 2
# drawPlot = plots.PlotDrawer(log=True, ratio=True, opts2={"ymin": 0, "ymax": 2})
#
# # Use the new drawer with a customisation function
# def customYTitleOffset(p):
#     # Modify the Y axis title offset for this one plot only
#     yaxis = p.getFrame().GetYaxis()
#     yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
# drawPlot(plot, "filename2", "X axis title", customise=customYTitleOffset)
# \endcode
#
# The work done here is divided to methods to make deriving from this
# class easy for customisations more complex than provided by this
# class alone.
class PlotDrawer:
    ## Constructor, set the defaults here
    #
    # \param ylabel              Default Y axis title
    # \param log                 Should Y axis be in log scale by default?
    # \param opts                Default frame bounds linear scale (see histograms._boundsArgs())
    # \param optsLog             Default frame bounds for log scale (see histograms._boundsArgs())
    # \param opts2               Default bounds for ratio pad (see histograms.CanvasFrameTwo and histograms._boundsArgs())
    # \param addLuminosityText   Should luminosity text be drawn?
    # \param stackMCHistograms   Should MC histograms be stacked?
    # \param addMCUncertainty    Should MC total (stat) uncertainty be drawn()
    def __init__(self,
                 ylabel="Occurrances / %.0f",
                 log=False,
                 ratio=False,
                 opts={},
                 optsLog={},
                 opts2={},
                 addLuminosityText=False,
                 stackMCHistograms=False,
                 addMCUncertainty=False,
                 ):
        self.ylabelDefault = ylabel
        self.logDefault = log
        self.ratioDefault = ratio
        self.optsDefault = {"ymin": 0, "ymaxfactor": 1.1}
        self.optsDefault.update(opts)
        self.optsLogDefault = {"ymin": 0.01, "ymaxfactor": 2}
        self.optsLogDefault.update(optsLog)
        self.opts2Default = {"ymin": 0.5, "ymax": 1.5}
        self.opts2Default.update(opts2)
        self.addLuminosityTextDefault = addLuminosityText
        self.stackMCHistogramsDefault = stackMCHistograms
        self.addMCUncertainty = addMCUncertainty

    ## Modify the defaults
    #
    # \param kwargs   Keyword arguments (same arguments as for __init__())
    def setDefaults(self, **kwargs):
        for name, value in kwargs.iteritems():
            if not hasattr(self, name+"Default"):
                raise Exception("No default value for '%s'"%name)
            setattr(self, name+"Default", value)

    ## Draw the plot with function call syntax
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param name    Plot file name
    # \param xlabel  X axis title
    # \param kwargs  Keyword arguments (see below)
    #
    # Keyword arguments are forwarded to the methods doing the actual
    # work. These methods pick the arguments they are interested of.
    # For further documentation, please look the individual methods
    def __call__(self, p, name, xlabel, **kwargs):
        self.rebin(p, **kwargs)
        self.stackMCHistograms(p, **kwargs)
        self.createFrame(p, name, **kwargs)
        self.setLegend(p, **kwargs)
        self.addCutLineBox(p, **kwargs)
        self.customise(p, **kwargs)
        self.finish(p, xlabel, **kwargs)

    ## Rebin all histograms in the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a  rebin  If given and large than 1, rebin all histograms in the plot
    def rebin(self, p, **kwargs):
        reb = kwargs.get("rebin", 1)
        if reb > 1:
            p.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(reb))

    ## Stack MC histograms
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a  stackMCHistograms   Should MC histograms be stacked? (default given in __init__()/setDefaults())
    # \li\a  addMCUncertainty    If MC histograms are stacked, should MC total (stat) uncertainty be drawn? (default given in __init__()/setDefaults())
    def stackMCHistograms(self, p, **kwargs):
        stack = kwargs.get("stackMCHistograms", self.stackMCHistogramsDefault)
        if stack:
            p.stackMCHistograms()
            if kwargs.get("addMCUncertainty", self.addMCUncertainty):
                p.addMCUncertainty()

    ## Stack MC histograms
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param name    Plot file name
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a log      Should Y axis be in log scale? (default given in __init__()/setDefaults())
    # \li\a opts     Frame bounds (defaults given in __init__()/setDefaults())
    # \li\a opts2    Ratio pad bounds (defaults given in __init__()/setDefaults())
    # \li\a ratio    Should ratio pad be drawn? (default given in __init__()/setDefaults())
    def createFrame(self, p, name, **kwargs):
        log = kwargs.get("log", self.logDefault)

        # Default values
        _opts = {}
        if log:
            _opts.update(self.optsLogDefault)
        else:
            _opts.update(self.optsDefault)
        _opts2 = {}
        _opts2.update(self.opts2Default)

        # Update from arg
        _opts.update(kwargs.get("opts", {}))
        _opts2.update(kwargs.get("opts2", {}))

        # Create frame
        p.createFrame(name, createRatio=kwargs.get("ratio", self.ratioDefault), opts=_opts, opts2=_opts2)
        if log:
            p.getPad().SetLogy(log)

    ## Add a legend to the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a moveLegend    Dictionary forwarded to histograms.moveLegend() after creating the legend
    #
    # The default legend position should be set by modifying histograms.createLegend (see histograms.LegendCreator())
    def setLegend(self, p, **kwargs):
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **(kwargs.get("moveLegend", {}))))

    ## Add cut box and/or line to the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a   cutLine   If given (and not None), should be a cut value or a list of cut values. Cut lines are drawn to the value points.
    # \li\a   cutBox    If given (and not None), should be a cut box specification or a list of specifications. For each specification, cut box and/or line is drawn according to the specification. Specification is a dictionary holding the parameters to plots._createCutBoxAndLine
    def addCutLineBox(self, p, **kwargs):
        cutLine = kwargs.get("cutLine", None)
        cutBox = kwargs.get("cutBox", None)
        if cutLine != None and cutBox != None:
            raise Exception("Both cutLine and cutBox were given, only either one can exist")

        # Add cut line and/or box
        if cutLine != None:
            lst = cutLine
            if not isinstance(lst, list):
                lst = [lst]
    
            for line in lst:
                p.addCutBoxAndLine(line, box=False, line=True)
        if cutBox != None:
            lst = cutBox
            if not isinstance(lst, list):
                lst = [lst]
    
            for box in lst:
                p.addCutBoxAndLine(**box)

    ## Provide hook for arbitrary customisation function just before drawing the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a customise     Function taking the plot (\a p) as the only argument. Return value is not used
    def customise(self, p, **kwargs):
        if "customise" in kwargs:
            kwargs["customise"](p)

    ## Draw and save the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param xlabel  X axis title
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a ylabel              Y axis title. If contains a '%', it is assumed to be a format string containing one double and the bin width of the plot is given to the format string. (default given in __init__()/setDefaults())
    # \li\a addLuminosityText   Should luminosity text be drawn? (default given in __init__()/setDefaults())
    #
    # In addition of drawing and saving the plot, handles the X and Y
    # axis titles, and "CMS Preliminary", "sqrt(s)" and luminosity
    # texts.
    def finish(self, p, xlabel, **kwargs):
        ylab = kwargs.get("ylabel", self.ylabelDefault)
        if "%" in ylab:
            ylab = ylab % p.binWidth()

        p.frame.GetXaxis().SetTitle(xlabel)
        p.frame.GetYaxis().SetTitle(ylab)
        p.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        if kwargs.get("addLuminosityText", self.addLuminosityTextDefault):
            p.addLuminosityText()
        p.save()


drawPlot = PlotDrawer()
