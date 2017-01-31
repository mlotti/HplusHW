'''
\package plots
Plot utilities and classes

The package is intended to gather the following commonalities in the
plots of H+ analysis (signal analysis, QCD and EWK background
analyses)
\li Dataset merging (see plots._datasetMerge)
\li Dataset order (see plots._datasetOrder)
\li Dataset legend labels (see plots._legendLabels)
\li Dataset plot styles (see plots._plotStyles)
\li Various datasets.DatasetManager operations (see plots.mergeRenameReorderForDataMC())
\li Various histograms.HistoManager operations (see plots.PlotBase and the derived classes)
\li Plot customisation, drawing, and saving (see plots.PlotDrawer)

The intended usage is to 
\li construct datasets.DatasetManager as usual
\li call plots.mergeRenameReorderForDataMC()
\li construct an object of the appropriate plots.PlotBase derived class
\li customise, draw, and save the plot with plots.drawPlot (or something derived from plots.PlotDrawer, or more manually)

Manually further customisations and operations can be done via the
interface of the plots.PlotBase derived class, or directly with the
histograms.HistoManager object contained by the plot object (via
histoMgr member). Some automation is provided with plots.PlotDrawer.

Although the intended usage is described above, it does \b not mean
that it would be the only way to use the classes. You should use
them only if they help you, and in a way which helps you. For
example, plots.PlotBase (or plots.ComparisonPlot,
plots.ComparisonManyPlot) doesn't care at all where the
histograms/graphs come from. If your problem is solved with direct
access to TFile and TH1/TGraph objects, or from TTree, more easily
than with datasetsd.DatasetManager, there is absolutely no problem
in doing so.
'''

#================================================================================================
# Import Modules
#================================================================================================
import sys
import array
import math
import copy

import ROOT

import dataset
import histograms
import styles
import aux

#================================================================================================
# Global Definitions
#================================================================================================
_lightHplusMasses        = [ 80,  90, 100, 120, 140, 150, 155, 160]
_heavyHplusMasses        = [180, 200, 220, 250, 300, 350, 400, 500, 600, 700, 750,  800, 1000, 2000, 3000]
_heavyHplusToTBbarMasses = [180, 200, 220, 240, 250, 260, 280, 300, 350, 400, 500,  600,  700,  750, 1000, 2000, 3000]

## These MC datasets must be added together before any
## merging/renaming. They are split to two datasets just for more
## statistics. The mapping is used in the
## mergeRenameReorderForDataMC() function.
_physicalMcAdd = {
    #"TT"    : "TT",
    "TT_ext": "TT", # covered by "TT"

    #"TTTT"      : "TTTT", # covered by "TT"
    "TTTT_ext1" : "TTTT", # covered by "TT"

    "WZ"     : "WZ",
    "WZ_ext1": "WZ",

    "ST_tW_antitop_5f_inclusiveDecays"     : "ST_tW_antitop_5f_inclusiveDecays",
    "ST_tW_antitop_5f_inclusiveDecays_ext1": "ST_tW_antitop_5f_inclusiveDecays",

    "ST_tW_top_5f_inclusiveDecays"     : "ST_tW_top_5f_inclusiveDecays",
    "ST_tW_top_5f_inclusiveDecays_ext1": "ST_tW_top_5f_inclusiveDecays",

    "ttbb_4FS_ckm_amcatnlo_madspin_pythia8"     : "TTBB",
    "ttbb_4FS_ckm_amcatnlo_madspin_pythia8_ext1": "TTBB",
}

#for mass in _lightHplusMasses:
    #_physicalMcAdd["TTToHplusBWB_M%d_Summer12"%mass] = "TTToHplusBWB_M%d_Summer12"%mass
    #_physicalMcAdd["TTToHplusBWB_M%d_ext_Summer12"%mass] = "TTToHplusBWB_M%d_Summer12"%mass
    #if mass != 90:
        #_physicalMcAdd["TTToHplusBHminusB_M%d_Summer12"%mass] = "TTToHplusBHminusB_M%d_Summer12"%mass
        #_physicalMcAdd["TTToHplusBHminusB_M%d_ext_Summer12"%mass] = "TTToHplusBHminusB_M%d_Summer12"%mass
#for mass in [180, 190, 200, 220, 250, 300]:
    #_physicalMcAdd["HplusTB_M%d_Summer12"%mass] = "HplusTB_M%d_Summer12"%mass
    #_physicalMcAdd["HplusTB_M%d_ext_Summer12"%mass] = "HplusTB_M%d_Summer12"%mass
#for bquark in [0, 1, 2, 3, 4]:
    #_physicalMcAdd["WJets_%dbquark_TuneZ2star_v1_Summer12"%bquark] = "WJets_%dbquark_TuneZ2star_Summer12"%bquark
    #_physicalMcAdd["WJets_%dbquark_TuneZ2star_v2_Summer12"%bquark] = "WJets_%dbquark_TuneZ2star_Summer12"%bquark
#for mass in _heavyHplusToTBbarMasses:
    #_physicalMcAdd["HplusToTBbar_M%d_Summer12"%mass] = "HplusToTBbar_M%d_Summer12"%mass

## Map the physical dataset names to logical names
#
# Map the physical dataset names (in multicrab.cfg) to logical names
# used in plots._legendLabels and plots._plotStyles. The mapping is
# used in the mergeRenameReorderForDataMC() function.
_physicalToLogical = {
    #"TT_TuneZ2_Summer11": "TT",

    #"WToTauNu_TuneZ2_Summer11": "WToTauNu",

    #"W3Jets_TuneZ2_Summer11": "W3Jets",

    #"W3Jets_TuneZ2_v2_Fall11": "W3Jets",
}
for mass in _lightHplusMasses:
    _physicalToLogical["ChargedHiggs_TTToHplusBWB_HplusToTauNu_M_%d"%(mass)] = "TTToHplusBWB_M%d"%mass

for mass in _heavyHplusMasses:
    _physicalToLogical["ChargedHiggs_HplusTB_HplusToTauNu_M_%d"%(mass)] = "HplusTB_M%d"%mass

#for mass in _heavyHplusToTBbarMasses:
    #_physicalToLogical["HplusToTBbar_M%d_%s"%(mass, mcEra)] = "HplusToTBbar_M%d" % mass

_physicalToLogical.update({
        "TTJets"         : "TTJets",
        "TTJets_FullLept": "TTJets_FullLept",
        "TTJets_SemiLept": "TTJets_SemiLept",
        "TTJets_Hadronic".replace("_", "_ext_"): "TTJets_Hadronic",
        
        # powheg ttbar
        "TT": "TT",
        
        "WJetsToLNu": "WJetsToLNu",
        # "W1Jets"    : "W1Jets",
        # "W2Jets"    : "W2Jets",
        # "W3Jets"    : "W3Jets",
        # "W4Jets"    : "W4Jets",
        "WJetsToLNu_HT_100To200"  : "WJetsToLNu_HT_100To200",
        "WJetsToLNu_HT_200To400"  : "WJetsToLNu_HT_200To400",
        "WJetsToLNu_HT_400To600"  : "WJetsToLNu_HT_400To600",
        "WJetsToLNu_HT_600To800"  : "WJetsToLNu_HT_600To800",
        "WJetsToLNu_HT_800To1200" : "WJetsToLNu_HT_800To1200",
        "WJetsToLNu_HT_1200To2500": "WJetsToLNu_HT_1200To2500",
        "WJetsToLNu_HT_2500ToInf" : "WJetsToLNu_HT_2500ToInf",
        
        "DYJetsToLL_M_50"            : "DYJetsToLL_M_50",
        "DYJetsToLL_M_10to50"        : "DYJetsToLL_M_10to50",
        "DYJetsToLL_M_50_HT_100to200": "DYJetsToLL_M_50_HT_100to200",
        "DYJetsToLL_M_50_HT_200to400": "DYJetsToLL_M_50_HT_200to400",
        "DYJetsToLL_M_50_HT_400to600": "DYJetsToLL_M_50_HT_400to600",
        "DYJetsToLL_M_50_HT_600toInf": "DYJetsToLL_M_50_HT_600toInf",
        "DYJetsToQQ_HT180"           : "DYJetsToQQ_HT180",
        
        "QCD_Pt_15to30"    : "QCD_Pt_15to30",
        "QCD_Pt_30to50"    : "QCD_Pt_30to50",
        "QCD_Pt_50to80"    : "QCD_Pt_50to80",
        "QCD_Pt_80to120"   : "QCD_Pt_80to120",
        "QCD_Pt_120to170"  : "QCD_Pt_120to170",
        "QCD_Pt_170to300"  : "QCD_Pt_170to300",
        "QCD_Pt_300to470"  : "QCD_Pt_300to470",
        "QCD_Pt_470to600"  : "QCD_Pt_470to600",
        "QCD_Pt_600to800"  : "QCD_Pt_600to800",
        "QCD_Pt_800to1000" : "QCD_Pt_800to1000",
        "QCD_Pt_1000to1400": "QCD_Pt_1000to1400",
        "QCD_Pt_1400to1800": "QCD_Pt_1400to1800",
        "QCD_Pt_1800to2400": "QCD_Pt_1800to2400",
        "QCD_Pt_2400to3200": "QCD_Pt_2400to3200",
        "QCD_Pt_3200toInf" : "QCD_Pt_3200toInf",
        
        "QCD_bEnriched_HT100to200"  : "QCD_bEnriched_HT100to200",
        "QCD_bEnriched_HT200to300"  : "QCD_bEnriched_HT200to300",
        "QCD_bEnriched_HT300to500"  : "QCD_bEnriched_HT300to500",
        "QCD_bEnriched_HT500to700"  : "QCD_bEnriched_HT500to700",
        "QCD_bEnriched_HT700to1000" : "QCD_bEnriched_HT700to1000",
        "QCD_bEnriched_HT1000to1500": "QCD_bEnriched_HT1000to1500",
        "QCD_bEnriched_HT1500to2000": "QCD_bEnriched_HT1500to2000",
        "QCD_bEnriched_HT2000toInf" : "QCD_bEnriched_HT2000toInf",
 
        "QCD_HT50to100"   : "QCD_HT50to100",
        "QCD_HT100to200"  : "QCD_HT100to200",
        "QCD_HT200to300"  : "QCD_HT200to300",
        "QCD_HT300to500"  : "QCD_HT300to500",
        "QCD_HT500to700"  : "QCD_HT500to700",
        "QCD_HT700to1000" : "QCD_HT700to1000",
        "QCD_HT1000to1500": "QCD_HT1000to1500",
        "QCD_HT1500to2000": "QCD_HT1500to2000",
        "QCD_HT2000toInf" : "QCD_HT2000toInf",
       
        "QCD_Pt20_MuEnriched"          : "QCD_Pt20_MuEnriched",
        "QCD_Pt_50to80_MuEnrichedPt5"  : "QCD_Pt_50to80_MuEnrichedPt5",
        "QCD_Pt_80to120_MuEnrichedPt5" : "QCD_Pt_80to120_MuEnrichedPt5",
        "QCD_Pt_120to170_MuEnrichedPt5": "QCD_Pt_120to170_MuEnrichedPt5",
        "QCD_Pt_170to300_MuEnrichedPt5": "QCD_Pt_170to300_MuEnrichedPt5",
        "QCD_Pt_300to470_MuEnrichedPt5": "QCD_Pt_300to470_MuEnrichedPt5",
        
        "ST_schannel_4f_leptonDecays"          : "ST_schannel_4f_leptonDecays",
        "ST_tW_antitop_5f_inclusiveDecays"     : "ST_tW_antitop_5f_inclusiveDecays",
        "ST_tW_top_5f_inclusiveDecays"         : "ST_tW_top_5f_inclusiveDecays",
        "ST_tchannel_antitop_4f_leptonDecays"  : "ST_tchannel_antitop_4f_leptonDecays",
        "ST_tchannel_top_4f_leptonDecays"      : "ST_tchannel_top_4f_leptonDecays",

        "WW": "WW",
        "WZ": "WZ",
        "ZZ": "ZZ",

        })

## Map the datasets to be merged to the name of the merged dataset.
_ttSignalMerge    = {}
_tSignalMerge     = {}
_lightSignalMerge = {}
#for mass in _lightHplusMasses:

    #_lightSignalMerge["TTToHplus_M%d"%mass] = "TTOrTToHplus_M%d"%mass
    #_lightSignalMerge["Hplus_taunu_M%d" % mass] = "TTOrTToHplus_M%d"%mass

_datasetMerge = {
    "QCD_Pt_15to30"    : "QCD",
    "QCD_Pt_30to50"    : "QCD",
    "QCD_Pt_50to80"    : "QCD",
    "QCD_Pt_80to120"   : "QCD",
    "QCD_Pt_120to170"  : "QCD",
    "QCD_Pt_170to300"  : "QCD",
    "QCD_Pt_300to470"  : "QCD",
    "QCD_Pt_470to600"  : "QCD",
    "QCD_Pt_600to800"  : "QCD",
    "QCD_Pt_800to1000" : "QCD",
    "QCD_Pt_1000to1400": "QCD",
    "QCD_Pt_1400to1800": "QCD",
    "QCD_Pt_1800to2400": "QCD",
    "QCD_Pt_2400to3200": "QCD",
    "QCD_Pt_3200toInf" : "QCD",

    "QCD_Pt_50to80_MuEnrichedPt5"  : "QCD",
    "QCD_Pt_80to120_MuEnrichedPt5" : "QCD",
    "QCD_Pt_120to170_MuEnrichedPt5": "QCD",
    "QCD_Pt_170to300_MuEnrichedPt5": "QCD",
    "QCD_Pt_300to470_MuEnrichedPt5": "QCD",

    "QCD_bEnriched_HT100to200"  : "QCD-b",
    "QCD_bEnriched_HT200to300"  : "QCD-b",
    "QCD_bEnriched_HT300to500"  : "QCD-b",
    "QCD_bEnriched_HT500to700"  : "QCD-b",
    "QCD_bEnriched_HT700to1000" : "QCD-b",
    "QCD_bEnriched_HT1000to1500": "QCD-b",
    "QCD_bEnriched_HT1500to2000": "QCD-b",
    "QCD_bEnriched_HT2000toInf" : "QCD-b",
 
    "QCD_HT50to100"   : "QCD",
    "QCD_HT100to200"  : "QCD",
    "QCD_HT200to300"  : "QCD",
    "QCD_HT300to500"  : "QCD",
    "QCD_HT500to700"  : "QCD",
    "QCD_HT700to1000" : "QCD",
    "QCD_HT1000to1500": "QCD",
    "QCD_HT1500to2000": "QCD",
    "QCD_HT2000toInf" : "QCD",

    "ST_s_channel_4f_InclusiveDecays"        : "SingleTop",
    "ST_tW_antitop_5f_inclusiveDecays"       : "SingleTop",
    "ST_tW_top_5f_inclusiveDecays"           : "SingleTop", 
    "ST_t_channel_antitop_4f_inclusiveDecays": "SingleTop",
    "ST_t_channel_top_4f_inclusiveDecays"    : "SingleTop",

    # "TT"      : "TT",
    "TT_ext"  : "TT",
    "TT_ext3" : "TT",
    "TTJets"  : "TTJets",    
    # "TTTT"    : "TTTT",
    #"TTJets_FullLept": "TTJets",
    #"TTJets_SemiLept": "TTJets",
    #"TTJets_Hadronic": "TTJets",

    "WJetsToLNu": "WJets",
    # "W1Jets"    : "WJets",
    # "W2Jets"    : "WJets",
    # "W3Jets"    : "WJets",
    # "W4Jets"    : "WJets",
    "WJetsToLNu_HT_100To200"  : "WJetsHT",
    "WJetsToLNu_HT_200To400"  : "WJetsHT",
    "WJetsToLNu_HT_400To600"  : "WJetsHT",
    "WJetsToLNu_HT_600To800"  : "WJetsHT",
    "WJetsToLNu_HT_800To1200" : "WJetsHT",
    "WJetsToLNu_HT_1200To2500": "WJetsHT",
    "WJetsToLNu_HT_2500ToInf" : "WJetsHT",
    # "WJetsToQQ_HT_600ToInf"   : "WJetsToQQ",

    "DYJetsToLL_M_10to50"        : "DYJetsToLLHT",
    "DYJetsToLL_M_50"            : "DYJetsToLL",
    "DYJetsToLL_M_50_HT_100to200": "DYJetsToLLHT",
    "DYJetsToLL_M_50_HT_200to400": "DYJetsToLLHT",
    "DYJetsToLL_M_50_HT_400to600": "DYJetsToLLHT",
    "DYJetsToLL_M_50_HT_600toInf": "DYJetsToLLHT",
    "DYJetsToQQ_HT180"           : "DYJetsToQQHT",

    # Diboson merge, comment this away to keep WW, WZ, ZZ samples separate
    "WWTo4Q": "Diboson",
    "ZZTo4Q": "Diboson",
    "WW"    : "Diboson",
    "WZ"    : "Diboson",
    "ZZ"    : "Diboson",

    "ttbb_4FS_ckm_amcatnlo_madspin_pythia8"     : "TTBB",

    #"ChargedHiggs_HplusTB_HplusToTauNu_M_200": "ChargedHiggs_HplusTB_HplusToTauNu_M_200",
    #"ChargedHiggs_HplusTB_HplusToTauB_M_200": "ChargedHiggs_HplusTB_HplusToTauNu_M_200",

    #"TTWJetsToQQ"          : "TTWJetsToQQ",
    #"TTZToQQ"              : "TTZToQQ",
    #"WWTo4Q"               : "WWTo4Q",
    #"ZJetsToQQ_HT600toInf" : "ZJetsToQQ_HT600toInf",
    #"ZZTo4Q"               : "ZZTo4Q",
    }

#================================================================================================
# Dataset ordering (default)
#================================================================================================
_datasetOrder = ["Data"]
for process in ["TTToHplusBWB_M%d", "TTToHplusBHminusB_M%d", "TTToHplus_M%d", "Hplus_taunu_t-channel_M%d", "Hplus_taunu_tW-channel_M%d", "Hplus_taunu_s-channel_M%d", "Hplus_taunu_M%d", "TTOrTToHplus_M%d"]:
    for mass in _lightHplusMasses:
        _datasetOrder.append(process%mass)
for mass in _heavyHplusMasses:
    _datasetOrder.append("HplusTB_M%d"%mass)
_datasetOrder.extend([
    "QCD",
    "QCDdata",
    "QCD-b",
    "QCD_Pt20_MuEnriched",
    "EWK", #merged    
    "WJets",
    "W1Jets",
    "W2Jets",
    "W3Jets",
    "W4Jets",
    "WJets_0bquark",
    "WJets_1bquark",
    "WJets_2bquark",
    "WJets_3bquark",
    "WJets",
    "WJetsHT",
    "WToTauNu",
    "TTJets",
    "TT",
    "ZJetsToQQ_HT600toInf", # Htb
    "TTandSingleTop", #merged
    "DYJetsToLL",
    "DYJetsToLLHT",
    "DYJetsToQQHT",  # Htb
    "SingleTop",
    "WJetsToQQ_HT_600ToInf", # Htb
    "TTZToQQ",     # Htb
    "TTWJetsToQQ", # Htb
    "Diboson",
    "WW",
    "WZ",
    "ZZ"
    "WWTo4Q",      # Htb
    "TTBB",        # Htb
    "TTTT",        # Htb
    ]) 

## Map the logical dataset names to legend labels
_legendLabels = {
    "Data"     : "Data",
    "EWK"      : "EWK",
    "Diboson"  : "Diboson",
    "SingleTop": "Single t",
    "QCD"      : "QCD",
    "QCD-b"    : "QCD (b enr.)",
    "QCDdata"  : "Mis-ID. #tau_{h} (data)", #"QCD (data driven)"

    "TTJets"        : "t#bar{t}+jets",
    "TT"            : "t#bar{t}",
    "TTTT"          : "t#bar{t}t#bar{t}",
    "TTWJetsToQQ"   : "t#bar{t}+W", # (W#rightarrowq#bar{q'})
    "TTZToQQ"       : "t#bar{t}+Z", # (Z#rightarrowq#bar{q'})
    "WWTo4Q"        : "WW",         # (W#rightarrowq#bar{q'})
    'ZZTo4Q'        : "ZZ",         # (Z#rightarrowq#bar{q})
    "TTBB"          : "t#bar{t}b#bar{b}",
    "TTandSingleTop": "t#bar{t}+single top",
    "DYJetsToLL"    : "Z/#gamma*+jets", #"DY+jets"
    "DYJetsToLLHT"  : "Z/#gamma*+jets",
    "DYJetsToQQHT"  : "Z/#gamma*+jets",

    "WJetsToQQ_HT_600ToInf": "W+jets", #, 600 < H_{T} < Inf", # (W#rightarrowq#bar{q'})
    "ZJetsToQQ_HT600toInf" : "Z+jets", #, 600 < H_{T} < Inf", # (Z#rightarrowq#bar{q})

    "WJets"        : "W+jets",
    "WJetsHT"      : "W+jets",
    "WToTauNu"     : "W#rightarrow#tau#nu",
    "W1Jets"       : "W+1 jets",
    "W2Jets"       : "W+2 jets",
    "W3Jets"       : "W+3 jets",
    "W4Jets"       : "W+4 jets",
    "WJets_0bquark": "W+jets (0 b)",
    "WJets_1bquark": "W+jets (1 b)",
    "WJets_2bquark": "W+jets (2 b)",
    "WJets_3bquark": "W+jets (#geq3 b)",   

    "QCD_Pt15to30"    : "QCD,   15 < #hat{p}_{T} <   30",
    "QCD_Pt30to50"    : "QCD,   30 < #hat{p}_{T} <   50",
    "QCD_Pt50to80"    : "QCD,   50 < #hat{p}_{T} <   80",
    "QCD_Pt80to120"   : "QCD,   80 < #hat{p}_{T} <  120",
    "QCD_Pt120to170"  : "QCD,  120 < #hat{p}_{T} <  170",
    "QCD_Pt170to300"  : "QCD,  170 < #hat{p}_{T} <  300",
    "QCD_Pt300to470"  : "QCD,  300 < #hat{p}_{T} <  470",
    "QCD_Pt470to600"  : "QCD,  470 < #hat{p}_{T} <  600",
    "QCD_Pt600to800"  : "QCD,  600 < #hat{p}_{T} <  800",
    "QCD_Pt800to1000" : "QCD,  800 < #hat{p}_{T} < 1000",
    "QCD_Pt1000to1400": "QCD, 1400 < #hat{p}_{T} < 1400",
    "QCD_Pt1400to1800": "QCD, 1800 < #hat{p}_{T} < 1800",
    "QCD_Pt1800to2400": "QCD, 2400 < #hat{p}_{T} < 2400",
    "QCD_Pt2400to3200": "QCD, 3200 < #hat{p}_{T} < 3200",
    "QCD_Pt3200toInf" : "QCD, #hat{p}_{T} > 3200",
    
    "QCD_Pt_15to30"    : "QCD,   15 < #hat{p}_{T} <   30",
    "QCD_Pt_30to50"    : "QCD,   30 < #hat{p}_{T} <   50",
    "QCD_Pt_50to80"    : "QCD,   50 < #hat{p}_{T} <   80",
    "QCD_Pt_80to120"   : "QCD,   80 < #hat{p}_{T} <  120",
    "QCD_Pt_120to170"  : "QCD,  120 < #hat{p}_{T} <  170",
    "QCD_Pt_170to300"  : "QCD,  170 < #hat{p}_{T} <  300",
    "QCD_Pt_300to470"  : "QCD,  300 < #hat{p}_{T} <  470",
    "QCD_Pt_470to600"  : "QCD,  470 < #hat{p}_{T} <  600",
    "QCD_Pt_600to800"  : "QCD,  600 < #hat{p}_{T} <  800",
    "QCD_Pt_800to1000" : "QCD,  800 < #hat{p}_{T} < 1000",
    "QCD_Pt_1000to1400": "QCD, 1400 < #hat{p}_{T} < 1400",
    "QCD_Pt_1400to1800": "QCD, 1800 < #hat{p}_{T} < 1800",
    "QCD_Pt_1800to2400": "QCD, 2400 < #hat{p}_{T} < 2400",
    "QCD_Pt_2400to3200": "QCD, 3200 < #hat{p}_{T} < 3200",
    "QCD_Pt_3200toInf" : "QCD, #hat{p}_{T} > 3200",

    "QCD_bEnriched_HT100to200"   : "QCD-b,  100 < H_{T} <  200",
    "QCD_bEnriched_HT200to300"   : "QCD-b,  200 < H_{T} <  300",
    "QCD_bEnriched_HT300to500"   : "QCD-b,  300 < H_{T} <  500",
    "QCD_bEnriched_HT500to700"   : "QCD-b,  500 < H_{T} <  700",
    "QCD_bEnriched_HT700to1000"  : "QCD-b,  700 < H_{T} < 1500",
    "QCD_bEnriched_HT1000to1500" : "QCD-b, 1000 < H_{T} < 1500",
    "QCD_bEnriched_HT1500to2000" : "QCD-b, 1500 < H_{T} < 2000",
    "QCD_bEnriched_HT2000toInf"  : "QCD-b, 2000 < H_{T} <  Inf",

    "QCD_HT50to100"   : "QCD,   50 < H_{T} <   100",
    "QCD_HT100to200"  : "QCD,  100 < H_{T} <   200",
    "QCD_HT200to300"  : "QCD,  200 < H_{T} <   300",
    "QCD_HT300to500"  : "QCD,  300 < H_{T} <   500",
    "QCD_HT500to700"  : "QCD,  500 < H_{T} <   700",
    "QCD_HT700to1000" : "QCD,  700 < H_{T} <  1000",
    "QCD_HT1000to1500": "QCD, 1000 < H_{T} <  1500",
    "QCD_HT1500to2000": "QCD, 1500 < H_{T} <  2000",
    "QCD_HT2000toInf" : "QCD, 2000 < H_{T} <  Inf",

    "QCD_Pt20_MuEnriched"          : "QCD (#mu enr.), #hat{p}_{T} >  20",
    "QCD_Pt_50to80_MuEnrichedPt5"  : "QCD (#mu enr.),  50 > #hat{p}_{T} <  80",
    "QCD_Pt_80to120_MuEnrichedPt5" : "QCD (#mu enr.),  80 > #hat{p}_{T} < 120",
    "QCD_Pt_120to170_MuEnrichedPt5": "QCD (#mu enr.), 120 > #hat{p}_{T} < 170",
    "QCD_Pt_170to300_MuEnrichedPt5": "QCD (#mu enr.), 170 > #hat{p}_{T} < 300",
    "QCD_Pt_300to470_MuEnrichedPt5": "QCD (#mu enr.), 300 > #hat{p}_{T} < 470",

    "TToBLNu_s-channel" : "Single t (s channel)",
    "TToBLNu_t-channel" : "Single t (t channel)",
    "TToBLNu_tW-channel": "Single t (tW channel)",
    "T_t-channel"       : "Single t (t channel)",
    "Tbar_t-channel"    : "Single #bar{t} (t channel)",
    "T_tW-channel"      : "Single t (tW channel)",
    "Tbar_tW-channel"   : "Single #bar{t} (tW channel)",
    "T_s-channel"       : "Single t (s channel)",
    "Tbar_s-channel"    : "Single #bar{t} (s channel)",

    # Ratio uncertainties
    "BackgroundStatError"    : "Stat. unc.",
    "BackgroundSystError"    : "Syst. unc.",
    "BackgroundStatSystError": "Stat.#oplussyst. unc.",
    "MCStatError"            : "Sim. stat. unc.",
    "MCSystError"            : "Sim. syst. unc.",
    "MCStatSystError"        : "Sim. stat.#oplussyst. unc.",
    }

for mass in _lightHplusMasses:
    _legendLabels["TTToHplusBWB_M%d"%mass] = "H^{+}W^{-} m_{H^{#pm}}=%d GeV"%mass
    _legendLabels["TTToHplusBHminusB_M%d"%mass] = "H^{+}H^{-} m_{H^{#pm}}=%d GeV" % mass
    _legendLabels["TTToHplus_M%d"%mass] = "H^{+} m_{H^{+}}=%d GeV" % mass

    #_legendLabels["Hplus_taunu_s-channel_M%d"%mass] = "t#rightarrowH^{+} (s) m_{H^{+}}=%d GeV" % mass
    #_legendLabels["Hplus_taunu_t-channel_M%d"%mass] = "t#rightarrowH^{+} (t) m_{H^{+}}=%d GeV" % mass
    #_legendLabels["Hplus_taunu_tW-channel_M%d"%mass] = "t#rightarrowH^{+} (tW) m_{H^{+}}=%d GeV" % mass
    _legendLabels["Hplus_taunu_M%d"%mass] = "t#rightarrowH^{+} m_{H^{+}}=%d" % mass

    _legendLabels["TTOrTToHplus_M%d"%mass] = "H^{+} m_{H^{+}}=%d GeV" % mass

for mass in _heavyHplusMasses:
    _legendLabels["HplusTB_M%d"%mass] = "H^{+} m_{H^{+}}=%d GeV" % mass
    _legendLabels["ChargedHiggs_HplusTB_HplusToTB_M_%d"%mass] = "H^{+} m_{H^{+}}=%d GeV" % mass

for mass in _heavyHplusToTBbarMasses:
    _legendLabels["HplusToTBbar_M%d"%mass] = "H^{+}#rightarrowtb m_{H^{+}}=%d GeV" % mass
    

## Map the logical dataset names to plot styles
_plotStyles = {
    "ChargedHiggs_HplusTB_HplusToTB_M_200": styles.signal200Style,
    "ChargedHiggs_HplusTB_HplusToTB_M_300": styles.signal300Style,
    "ChargedHiggs_HplusTB_HplusToTB_M_500": styles.signal500Style,

    "DYJetsToLL"    : styles.dyStyle,
    "DYJetsToLLHT"  : styles.dyStyle,
    "DYJetsToQQHT"  : styles.dyStyle,
    "Data"          : styles.dataStyle,
    "Diboson"       : styles.dibStyle,
    "EWK"           : styles.wStyle,
    "QCD"           : styles.qcdStyle,
    "QCD-b"         : styles.qcdBEnrichedStyle,
    "QCDdata"       : styles.qcdStyle,
    "SingleTop"     : styles.stStyle,
    "TT"            : styles.ttStyle,
    "TTBB"          : styles.ttbbStyle, 
    "TTJets"        : styles.ttjetsStyle,
    "TTTT"          : styles.ttttStyle, 
    "TTWJetsToQQ"   : styles.ttwStyle, 
    "TTZToQQ"       : styles.ttzStyle, 
    "TTandSingleTop": styles.ttStyle,
    "W3Jets"        : styles.wStyle,
    "WJets"         : styles.wStyle,
    "WJetsHT"       : styles.wStyle,
    "WToTauNu"      : styles.wStyle,
    "WW"            : styles.dibStyle,
    "WWTo4Q"        : styles.dibStyle,
    "WZ"            : styles.dibStyle,
    "ZZ"            : styles.dibStyle,

    "WJets_0bquark": styles.Style(ROOT.kFullTriangleDown, ROOT.kRed+1),
    "WJets_1bquark": styles.Style(ROOT.kFullTriangleDown, ROOT.kRed+4),
    "WJets_2bquark": styles.Style(ROOT.kFullTriangleDown, ROOT.kRed+3),
    "WJets_3bquark": styles.Style(ROOT.kFullTriangleDown, ROOT.kRed-7),

    "QCD_Pt20_MuEnriched"          : styles.qcdStyle,
    "QCD_Pt_50to80_MuEnrichedPt5"  : styles.qcdStyle,
    "QCD_Pt_80to120_MuEnrichedPt5" : styles.qcdStyle,
    "QCD_Pt_120to170_MuEnrichedPt5": styles.qcdStyle,
    "QCD_Pt_170to300_MuEnrichedPt5": styles.qcdStyle,
    "QCD_Pt_300to470_MuEnrichedPt5": styles.qcdStyle,
    
    "ZJetsToQQ_HT600toInf" : styles.zjetsStyle,
    "WJetsToQQ_HT_600ToInf": styles.wjetsStyle,
    
    "Ratio"                  : styles.ratioStyle,
    "BackgroundStatError"    : styles.errorRatioStatStyle,
    "BackgroundSystError"    : styles.errorRatioSystStyle,
    "BackgroundStatSystError": styles.errorRatioSystStyle,
    "RatioLine"              : styles.ratioLineStyle,
    }

# Other
_plotStyles["Embedding"] = _plotStyles["TTJets"].clone()
for mass in _lightHplusMasses:
    _plotStyles["TTToHplusBWB_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)
    _plotStyles["TTToHplusBHminusB_M%d"%mass] = getattr(styles, "signalHH%dStyle"%mass)
    _plotStyles["TTToHplus_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)

    _plotStyles["Hplus_taunu_s-channel_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)
    _plotStyles["Hplus_taunu_t-channel_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)
    _plotStyles["Hplus_taunu_tW-channel_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)
    _plotStyles["Hplus_taunu_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)

    _plotStyles["TTOrTToHplus_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)

for mass in _heavyHplusMasses:
    _plotStyles["HplusTB_M%d"%mass] = getattr(styles, "signal%dStyle"%mass)


## Return True if name is from a signal dataset
def isSignal(name):
    return "TTToHplus" in name or "Hplus_taunu" in name or "TTOrTToHplus" in name or "HplusTB" in name


## Update the default legend labels
def updateLegendLabel(datasetName, legendLabel):
    _legendLabels[datasetName] = legendLabel

class SetProperty:
    '''
    Helper class for setting properties
    
    Helper class for setting properties of histograms.Histo objects (legend label, plot style)
    '''
    def __init__(self, properties, setter):
        '''
        Constructor
        
        \param properties  Dictionary of properties (from name of
        histograms.Histo to the property understood by the setter)
        
        \param setter      Function for setting the property. It should take
        two parameters, first one is the histograms.Histo object, second one is the
        property to be set
        '''
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
# \param datasetMgr     dataset.DatasetManager object
# \param keepSourcesMC  If True, for MC keep also the merged dataset.Dataset objects in the dataset.DatasetManager (see dataset.DatasetManager.merge)
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
    datasetMgr.mergeData(allowMissingDatasets=True)
    datasetMgr.mergeMany(_physicalMcAdd, addition=True)
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
# The dataset names to be merged are defined in plots._ttSignalMerge list
def mergeWHandHH(datasetMgr):
    datasetMgr.mergeMany(_ttSignalMerge)

def mergeSingleTopHplus(datasetMgr):
    datasetMgr.mergeMany(_tSignalMerge)

def mergeLightHplus(datasetMgr):
    mergeWHandHH(datasetMgr)
    mergeSingleTopHplus(datasetMgr)
    datasetMgr.mergeMany(_lightSignalMerge)    

def replaceLightHplusWithSignalPlusBackground(datasetMgr, backgroundsWithoutTT=None):
    if backgroundsWithoutTT is None:
        backgroundsWithoutTT=["WJets", "DYJetsToLL", "SingleTop", "Diboson", "QCD"]

    signalDatasetNames = filter(lambda name: "TTToHplus_M" in name, datasetMgr.getAllDatasetNames())
    if len(signalDatasetNames) == 0:
        raise Exception("Did not find any light H+ signal dataset (containing 'TTToHplus_M' string), maybe something is wrong in your datasets? List of available datasets: %s" % ", ".join(datasetMgr.getAllDatasetNames()))

    def extractBR(dset):
        try:
            tmp = dset.getProperty("BRtH")
        except KeyError:
            raise Exception("Did not find propery 'BRtH' from signal datasets %s, did you run crosssection.setHplusCrossSectionsTo*() function?" % dset.getName())
        return (tmp, dset.getName())

    BRtH = None
    for name in signalDatasetNames:
        d = datasetMgr.getDataset(name)
        lst = d.forEach(extractBR)
        for br, rawname in lst:
            if BRtH is None:
                BRtH = br
            else:
                if abs(br-BRtH)/max(abs(br), abs(BRtH)) > 0.001:
                    raise Exception("There are signal datasets with different BR(t->H+), got %f in %s, was before %f" % (br, rawname, BRtH))

    ttjets2 = datasetMgr.getDataset("TTJets").deepCopy()
    ttjets2.setName("TTJetsScaledByBR")
    scaledXsect = (1-BRtH)*(1-BRtH) * ttjets2.getCrossSection()
    ttjets2.setCrossSection(scaledXsect)
    print "Setting TTJetsScaledByBR cross section to %f pb (scaled with BR(t->H+)=%f" % (scaledXsect, BRtH)

    datasetMgr.append(ttjets2)
    datasetMgr.merge("BkgNoTT", backgroundsWithoutTT, keepSources=True)
    for name in signalDatasetNames:
        isLast = (name == signalDatasetNames[-1])
        datasetMgr.merge(name+"Tmp", [name, "BkgNoTT","TTJetsScaledByBR"], keepSources=not isLast)
        if not isLast:
            datasetMgr.remove(name, close=False)
        datasetMgr.rename(name+"Tmp", name)
        _legendLabels[name] = "with H^{+}#rightarrow#tau^{+}#nu"


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
    if isBinomial:
        function = _createRatioBinomial
    else:
        function = _createRatioErrorPropagation
    return function(rootHisto1, rootHisto2, ytitle)

def _createRatioHistos(histo1, histo2, ytitle, ratioType=None, ratioErrorOptions={}):
    if ratioType is None:
        ratioType = "errorPropagation"

    ret = []
    if ratioType == "errorPropagation":
        ret.extend(_createRatioErrorPropagation(histo1, histo2, ytitle, returnHisto=True))
    elif ratioType == "binomial":
        h = _createHisto(_createRatioBinomial(histo1, histo2, ytitle))
        h.setDrawStyle("EP")
        h.setLegendLabel(None)
        ret.append(h)
    elif ratioType == "errorScale":
        ret.extend(_createRatioHistosErrorScale(histo1, histo2, ytitle, **ratioErrorOptions))
    else:
        raise Exception("Invalid value for argument ratioType '%s', valid are 'errorPropagation', 'binomial', 'errorScale'")
    return ret        

## Creates a ratio histogram by propagating the uncertainties to the ratio
#
# \param histo1  TH1/TGraph/RootHistoWithUncertainties dividend
# \param histo2  TH1/TGraph/RootHistoWithUncertainties divisor
# \param ytitle  Y axis title of the final ratio histogram/graph
#
# \return TH1 or TGraphAsymmErrors of histo1/histo2
#
# In case of asymmetric uncertainties, the uncertainties are added in
# quadrature for both sides separately (a rather crude approximation).
def _createRatioErrorPropagation(histo1, histo2, ytitle, returnHisto=False):
    if isinstance(histo1, ROOT.TH1) and isinstance(histo2, ROOT.TH1):
        ratio = histo1.Clone()
        ratio.SetDirectory(0)
        ratio.Divide(histo2)
        if histograms.uncertaintyMode.equal(histograms.Uncertainty.SystOnly):
            for i in xrange(0, ratio.GetNbinsX()+2):
                ratio.SetBinError(i, 0)

        _plotStyles["Ratio"].apply(ratio)
        ratio.GetYaxis().SetTitle(ytitle)

        if returnHisto:
            return [_createHisto(ratio, drawStyle="EP", legendLabel=None)]
        else:
            return ratio
    elif isinstance(histo1, ROOT.TGraph) and isinstance(histo2, ROOT.TGraph):
        if histo1.GetN() != histo2.GetN():
            (histo1, histo2) = _graphRemoveNoncommonPoints(histo1, histo2)

        xvalues = []
        yvalues = []
        yerrs = []
        for i in xrange(0, histo1.GetN()):
            yval = histo2.GetY()[i]
            if yval == 0:
                continue
            xvalues.append(histo1.GetX()[i])
            yvalue = histo1.GetY()[i] / yval
            yvalues.append(yvalue)
            if histograms.uncertaintyMode.equal(histograms.Uncertainty.SystOnly):
                yerrs.append(0)
            else:
                err1 = max(histo1.GetErrorYhigh(i), histo1.GetErrorYlow(i))
                err2 = max(histo2.GetErrorYhigh(i), histo2.GetErrorYlow(i))
                yerrs.append( yvalue * math.sqrt( _divideOrZero(err1, histo1.GetY()[i])**2 +
                                                  _divideOrZero(err2, histo2.GetY()[i])**2 ) )

        if len(xvalues) > 0:
            gr = ROOT.TGraphAsymmErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues),
                                        histo1.GetEXlow(), histo1.GetEXhigh(),
                                        array.array("d", yerrs), array.array("d", yerrs))
        else:
            gr = ROOT.TGraphAsymmErrors()
        _plotStyles["Ratio"].apply(gr)
        gr.GetYaxis().SetTitle(ytitle)

        if returnHisto:
            return [_createHisto(gr, drawStyle="EPZ", legendLabel=None)]
        else:
            return gr
    elif isinstance(histo1, dataset.RootHistoWithUncertainties) and isinstance(histo2, dataset.RootHistoWithUncertainties):
        if histograms.uncertaintyMode.equal(histograms.Uncertainty.StatOnly) or \
                (not (histo1.hasSystematicUncertainties() or histo2.hasSystematicUncertainties())):
            return _createRatioErrorPropagation(histo1.getRootHisto(), histo2.getRootHisto(), ytitle, returnHisto)

        ratio = _createRatioErrorPropagation(histo1.getRootHisto(), histo2.getRootHisto(), ytitle)

        addStat = histograms.uncertaintyMode.addStatToSyst()
        unc1 = histo1.getSystematicUncertaintyGraph(addStatistical=addStat)
        unc2 = histo2.getSystematicUncertaintyGraph(addStatistical=addStat)

        for i in xrange(0, unc1.GetN()):
            yval1 = unc1.GetY()[i]
            yval2 = unc2.GetY()[i]
            if yval2 == 0.0:
                unc1.SetPoint(i, unc1.GetX()[i], 0)
                unc1.SetPointEYhigh(i, 0)
                unc1.SetPointEYlow(i, 0)
                continue
            if yval1 == 0.0:
                unc1.SetPoint(i, unc1.GetX()[i], 0)
                unc1.SetPointEYhigh(i, unc1.GetErrorYhigh(i)/yval2)
                unc1.SetPointEYlow(i, unc1.GetErrorYlow(i)/yval2)
                continue

            unc1.SetPoint(i, unc1.GetX()[i], yval1/yval2)
            unc1.SetPointEYhigh(i, math.sqrt( (unc1.GetErrorYhigh(i)/yval1)**2 + (unc2.GetErrorYhigh(i)/yval2)**2 ))
            unc1.SetPointEYlow( i, math.sqrt( (unc1.GetErrorYlow(i)/yval1)**2  + (unc2.GetErrorYlow(i)/yval2)**2 ))
        ratioSyst = unc1
        _plotStyles["Ratio"].apply(ratioSyst)
        ratioSyst.GetYaxis().SetTitle(ytitle)

        if returnHisto:
            ret = []
            systStyle = "EPZ"
            if histograms.uncertaintyMode.showStatOnly():
                ret.append(_createHisto(ratio, drawStyle="EPZ", legendLabel=None))
                systStyle = "[]"
            ret.append(_createHisto(ratioSyst, drawStyle=systStyle, legendLabel=None))
            return ret
        else:
            if addRatioStat:
                return [ratio, ratioSyst]
            else:
                return ratioSyst
    else:
        raise Exception("Arguments are of unsupported type, histo1 is %s and histo2 is %s" % (histo1.__class__.__name__, histo2.__class__.__name__))


## Removes non-common points of two graph
#
# Non-commonality is defined with the X value.
def _graphRemoveNoncommonPoints(graph1, graph2):
    ret1 = graph1.Clone()
    ret2 = graph2.Clone()
    xfound = []
    for i in range(graph1.GetN()):
        for j in range(graph2.GetN()):
            if graph1.GetX()[i] == graph2.GetX()[j]:
        	xfound.append(graph1.GetX()[i])
    remove1 = []
    for i in range(graph1.GetN()):
        found = False
        for x in xfound:
            if graph1.GetX()[i] == x:
        	found = True
        if not found:
            remove1.append(i)
    remove2 = []
    for j in range(graph2.GetN()):
        found = False
        for x in xfound:
            if graph2.GetX()[j] == x:
                found = True
        if not found:
            remove2.append(j)

    remove1.reverse()
    for i in remove1:
        ret1.RemovePoint(i)
    remove2.reverse()
    for i in remove2:
        ret2.RemovePoint(i)

    return (ret1, ret2)

## Creates a ratio histogram by binomial assumption
#
# \param histo1  TH1 dividend
# \param histo2  TH1 divisor
# \param ytitle  Y axis title
#
# \return TGraphAsymmErrors of histo1/histo2
#
# The uncertainty estimation is done via TGraphAsymmErrors and
# Clopper-Pearson method (one of the methods recommended by statistics
# committee).
def _createRatioBinomial(histo1, histo2, ytitle):
    if isinstance(histo1, ROOT.TH1) and isinstance(histo2, ROOT.TH1):
        if histograms.uncertaintyNode != histograms.Uncertainty.StatOnly:
            print >>sys.stderr, "Warning: uncertainty mode is not 'StatOnly' (but %s). Nevertheless, the binomial uncertainty is calculated incorporating the uncertainty from the number of events in the input histograms" % (histograms.uncertaintyMode.getName())

        eff = ROOT.TGraphAsymmErrors(rootHisto1, rootHisto2)
        styles.getDataStyle().apply(eff)
        eff.GetYaxis().SetTitle(ytitle)
        return eff
    elif isinstance(histo1, ROOT.TGraph) and isinstance(histo2, ROOT.TGraph):
        raise Exception("isBinomial is not supported for TGraph input")
    else:
        raise Exception("Arguments are of unsupported type, histo1 is %s and histo2 is %s" % (histo1.__class__.__name__, histo2.__class__.__name__))

## Creates ratio histograms by scaling everything to the divisor value
#
# \param histo1  TH1 dividend
# \param histo2  TH1 divisor
# \param ytitle  Y axis title
# \param numeratorStatSyst   Include stat.+syst. to numerator (if syst globally enabled)
# \param denominatorStatSyst Include stat.+syst. to denominator (if syst globally enabled)
#
# \return list of histograms.Histo objects for histo1/histo2
#
# Scales the histo1 values+uncertainties, and histo2 uncertainties by
# histo2 values. Creates separate entries for histo2 statistical and
# stat+syst uncertainties, if systematic uncertainties exist.
def _createRatioHistosErrorScale(histo1, histo2, ytitle, numeratorStatSyst=True, denominatorStatSyst=True, numeratorOriginatesFromTH1=False):
    addAlsoHatchedUncertaintyHisto = False
    #addAlsoHatchedUncertaintyHisto = True

    ret = []

    if (isinstance(histo1, ROOT.TH1) or isinstance(histo1, ROOT.TGraph)) and \
       (isinstance(histo2, ROOT.TH1) or isinstance(histo2, ROOT.TGraph)):
        
        class WrapTH1:
            def __init__(self, th1):
                self._th1 = th1
                self._ratio = False
            def ratioDrawStyle(self):
                return "EP"
            def begin(self):
                return 1
            def end(self):
                return self._th1.GetNbinsX()+1
            def xvalues(self, bin):
                xval = self._th1.GetBinCenter(bin)
                xlow = xval-self._th1.GetXaxis().GetBinLowEdge(bin)
                xhigh = self._th1.GetXaxis().GetBinUpEdge(bin)-xval
                return (xval, xlow, xhigh)
            def yvalues(self, bin):
                yval = self._th1.GetBinContent(bin)
                yerr = self._th1.GetBinError(bin)
                return (yval, yerr, yerr)
            def y(self, bin):
                return self._th1.GetBinContent(bin)
            def asRatio(self):
                self._th1 = self._th1.Clone()
                self._th1.SetDirectory(0)
                self._ratio = True
            def _ensureRatio(self):
                if not self._ratio:
                    raise Exception("I'm not a ratio TH1!")
            def divide(self, bin, scale, xcenter):
                self._ensureRatio()
                self._th1.SetBinContent(bin, _divideOrZero(self._th1.GetBinContent(bin), scale))
                self._th1.SetBinError(bin, _divideOrZero(self._th1.GetBinError(bin), scale))
            def getRatio(self):
                self._ensureRatio()
                return self._th1
            
        class WrapTGraph:
            def __init__(self, gr):
                self._gr = gr
                self._ratio = False
            def ratioDrawStyle(self):
                return "PZ"
            def begin(self):
                return 0
            def end(self):
                return self._gr.GetN()
            def xvalues(self, bin):
                return (self._gr.GetX()[bin], self._gr.GetErrorXlow(bin), self._gr.GetErrorXhigh(bin))
            def yvalues(self, bin):
                return (self._gr.GetY()[bin], self._gr.GetErrorYlow(bin), self._gr.GetErrorYhigh(bin))
            def y(self, bin):
                return self._gr.GetY()[bin]
            def asRatio(self):
                self.xvalues = []
                self.xerrslow = []
                self.xerrshigh = []
                self.yvalues = []
                self.yerrshigh = []
                self.yerrslow = []
                self.binOffset = 0
                self._ratio = True
            def _ensureRatio(self):
                if not self._ratio:
                    raise Exception("I'm not a ratio TGraph!")
            def divide(self, bin, scale, xcenter):
                # Ignore bin if denominator is zero
                if scale == 0:
                    return
                # No more items in the numerator
                if bin >= self._gr.GetN():
                    return
                # denominator is missing an item
                trueBin = bin + self.binOffset
                xval = self._gr.GetX()[trueBin]
                epsilon = 1e-3 * xval # to allow floating-point difference between TGraph and TH1
                if xval+epsilon < xcenter:
                    self.binOffset -= 1
                    return
                # numerator is missing an item
                elif xval-epsilon > xcenter:
                    self.binOffset += 1
                    return

                if numeratorOriginatesFromTH1 and self._gr.GetY()[trueBin] == 0 and self._gr.GetErrorYlow(trueBin) == 0 and self._gr.GetErrorYhigh(trueBin) == 0:
                    return

                self.xvalues.append(xval)
                if numeratorOriginatesFromTH1 and ROOT.gStyle.GetErrorX() < 0.1:
                    self.xerrslow.append(0.0)
                    self.xerrshigh.append(0.0)
                else:
                    self.xerrslow.append(self._gr.GetErrorXlow(trueBin))
                    self.xerrshigh.append(self._gr.GetErrorXhigh(trueBin))
                self.yvalues.append(self._gr.GetY()[trueBin] / scale)
                self.yerrslow.append(self._gr.GetErrorYlow(trueBin) / scale)
                self.yerrshigh.append(self._gr.GetErrorYhigh(trueBin) / scale)
            def getRatio(self):
                self._ensureRatio()
                if len(self.xvalues) == 0:
                    return ROOT.TGraphAsymmErrors()
                return ROOT.TGraphAsymmErrors(len(self.xvalues), array.array("d", self.xvalues), array.array("d", self.yvalues),
                                              array.array("d", self.xerrslow), array.array("d", self.xerrshigh), 
                                              array.array("d", self.yerrslow), array.array("d", self.yerrshigh))

        if isinstance(histo1, ROOT.TH1):
            h1 = WrapTH1(histo1)
            ratioWrapped = WrapTH1(histo1)
        elif isinstance(histo1, ROOT.TGraph):
            h1 = WrapTGraph(histo1)
            ratioWrapped = WrapTGraph(histo1)
        if isinstance(histo2, ROOT.TH1):
            h2 = WrapTH1(histo2)
        elif isinstance(histo2, ROOT.TGraph):
            h2 = WrapTGraph(histo2)

        # For numerator (foreground)
        ratioWrapped.asRatio()
        # For denominator (background)
        xvalues = []
        xerrhigh = []
        xerrlow = []
        yvalues = []
        yerrhigh = []
        yerrlow = []
        for bin in xrange(h2.begin(), h2.end()): # important to use h2 because of TGraph logic
            (scale, ylow, yhigh) = h2.yvalues(bin)
            (xval, xlow, xhigh) = h2.xvalues(bin)
            ratioWrapped.divide(bin, scale, xval)

            xvalues.append(xval)
            xerrlow.append(xlow)
            xerrhigh.append(xhigh)
            yvalues.append(1.0)
            yerrlow.append(_divideOrZero(ylow, scale))
            yerrhigh.append(_divideOrZero(yhigh, scale))

        ratio = ratioWrapped.getRatio()
        ratioErr = ROOT.TGraphAsymmErrors(len(xvalues), array.array("d", xvalues), array.array("d", yvalues),
                                          array.array("d", xerrlow), array.array("d", xerrhigh),
                                          array.array("d", yerrlow), array.array("d", yerrhigh))

        ratio.GetYaxis().SetTitle(ytitle)
        ratioErr.GetYaxis().SetTitle(ytitle)
        ratioErr.SetName("BackgroundStatError")
        _plotStyles["Ratio"].apply(ratio)
        _plotStyles[ratioErr.GetName()].apply(ratioErr)

        ret.append(_createHisto(ratio, drawStyle=ratioWrapped.ratioDrawStyle(), legendLabel=None))
        if histograms.uncertaintyMode.showStatOnly():
            ret.append(_createHisto(ratioErr, drawStyle="E2", legendLabel=_legendLabels[ratioErr.GetName()], legendStyle="F"))
            if addAlsoHatchedUncertaintyHisto:
                ratioErr2 = ratioErr.Clone("BackgroundStatError2")
                ratioErr2.SetDirectory(0)
                styles.errorStyle.apply(ratioErr2)
                ratioErr2.SetFillStyle(3344)
                ret.append(_createHisto(ratioErr2, drawStyle="E2", legendLabel=None))
        return ret

    elif isinstance(histo1, dataset.RootHistoWithUncertainties) and isinstance(histo2, dataset.RootHistoWithUncertainties):
        #h1 = histo1.getRootHisto()
        #h2 = histo2.getRootHisto()
        gr1 = histo1.getSystematicUncertaintyGraph(addStatistical=True, addSystematic=False)
        gr2 = histo2.getSystematicUncertaintyGraph(addStatistical=True, addSystematic=False)

        # Add scaled stat uncertainty
        #ret.extend(_createRatioHistosErrorScale(h1, h2, ytitle))
        ret.extend(_createRatioHistosErrorScale(gr1, gr2, ytitle, numeratorOriginatesFromTH1 = isinstance(histo1.getRootHisto(), ROOT.TH1)))
        if histograms.uncertaintyMode.equal(histograms.Uncertainty.StatOnly):
            return ret

        # Then add scaled stat+syst uncertainty

        # Get new TGraphAsymmErrors for stat+syst, then scale it
        ratioSyst1 = histo1.getSystematicUncertaintyGraph(addStatistical=histograms.uncertaintyMode.addStatToSyst())
        ratioSyst2 = histo2.getSystematicUncertaintyGraph(addStatistical=histograms.uncertaintyMode.addStatToSyst())
        removes = []
        for i in xrange(0, ratioSyst2.GetN()):
            yval = ratioSyst2.GetY()[i]
            if yval == 0.0:
                removes.append(i)
                continue
            ratioSyst1.SetPoint(i, ratioSyst1.GetX()[i], ratioSyst1.GetY()[i]/yval)
            ratioSyst1.SetPointEYhigh(i, ratioSyst1.GetErrorYhigh(i)/yval)
            ratioSyst1.SetPointEYlow(i, ratioSyst1.GetErrorYlow(i)/yval)
            ratioSyst1.SetPointEXhigh(i, 0)
            ratioSyst1.SetPointEXlow(i, 0)
            ratioSyst2.SetPoint(i, ratioSyst2.GetX()[i], 1)
            ratioSyst2.SetPointEYhigh(i, ratioSyst2.GetErrorYhigh(i)/yval)
            ratioSyst2.SetPointEYlow(i, ratioSyst2.GetErrorYlow(i)/yval)
#            print i, ratioSyst2.GetX()[i], ratioSyst2.GetErrorXlow(i), ratioSyst2.GetErrorXhigh(i), yval, ratioSyst2.GetY()[i], ratioSyst2.GetErrorYhigh(i), ratioSyst2.GetErrorYlow(i)
        removes.reverse()
        for i in removes:
            ratioSyst1.RemovePoint(i)
            ratioSyst2.RemovePoint(i)

        ratioSyst1.SetName(histo1.GetName()+"_syst")
        ratioSyst2.GetYaxis().SetTitle(ytitle)
        name = "BackgroundStatSystError"
        ratioSyst2.SetName(name)
        if not histograms.uncertaintyMode.addStatToSyst():
            name = "BackgroundSystError"
        _plotStyles[name].apply(ratioSyst2)

        if numeratorStatSyst:
            ret.append(_createHisto(ratioSyst1, drawStyle="[]", legendLabel=None))
        if denominatorStatSyst:
            ret.append(_createHisto(ratioSyst2, drawStyle="2", legendLabel=_legendLabels[name], legendStyle="F"))
        if addAlsoHatchedUncertaintyHisto:
            ratioSyst2_2 = ratioSyst.Clone("BackgroundStatSystError2")
            styles.errorStyle.apply(ratioSyst2_2)
            ratioSyst2_2.SetFillStyle(3354)
            ret.append(_createHisto(ratioSyst2_2, drawStyle="2", legendLabel=None))
        return ret
    else:
        raise Exception("Arguments are of unsupported type, histo1 is %s and histo2 is %s" % (histo1.__class__.__name__, histo2.__class__.__name__))

def _divideOrZero(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator/denominator

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
    _plotStyles["RatioLine"].apply(line)
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
def _createCoverPad(xmin=0.065, ymin=0.285, xmax=0.158, ymax=0.33):
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
    if isinstance(rootObject, ROOT.TH1) or isinstance(rootObject, dataset.RootHistoWithUncertainties):
        return histograms.Histo(rootObject, rootObject.GetName(), **kwargs)
    elif isinstance(rootObject, ROOT.TGraph):
        return histograms.HistoGraph(rootObject, rootObject.GetName(), **kwargs)
    elif isinstance(rootObject, ROOT.TEfficiency):
        return histograms.HistoEfficiency(rootObject, rootObject.GetName(), **kwargs)
    elif not isinstance(rootObject, histograms.Histo):
        raise Exception("rootObject is not TH1, TGraph, histograms.Histo, nor dataset.RootHistoWithUncertainties, it is %s" % rootObject.__class__.__name__)

    return rootObject

## Helper function for partially blinding a plot
#
# \param plot              PlotBase (or derived) object
# \param maxShownValue     If not None, the maximum value to be shown
# \param minShownValue     If not None, the minimum value to be shown
# \param invert            Invert the selection (from [min, max] to [-inf, min], [max, inf])
# \param moveBlinededText  Dictionary for movinge the blinding text (forwarded to histograms.PlotTextBox.move())
def partiallyBlind(plot, maxShownValue=None, minShownValue=None, invert=False, moveBlindedText={}):
    if not plot.histoMgr.hasHisto("Data"):
        return

    dataHisto = plot.histoMgr.getHisto("Data")
    th1 = dataHisto.getRootHisto()

    if minShownValue is None:
        firstShownBin = 1
    else:
        firstShownBin = th1.FindFixBin(minShownValue)

    if maxShownValue is None:
        lastShownBin = th1.GetNbinsX()
    else:
        lastShownBin = th1.FindFixBin(maxShownValue)-1
    
    for i in xrange(1, th1.GetNbinsX()+1):
        if invert:
            if i<= firstShownBin or i >= lastShownBin:
                continue
        else:
            if i >= firstShownBin and i <= lastShownBin:
                continue

        th1.SetBinContent(i, 0)
        th1.SetBinError(i, 0)

    tb = histograms.PlotTextBox(xmin=0.4, ymin=None, xmax=0.6, ymax=0.84, size=17, lineheight=0.035)
    tb.addText("Data blinded in")
    tb.addText("signal region")
    tb.move(**moveBlindedText)
    plot.appendPlotObject(tb)


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
    def __init__(self, datasetRootHistos=[], saveFormats=[".png", ".pdf", ".C"]):
        # Create the histogram manager
        if len(datasetRootHistos) > 0:
            if isinstance(datasetRootHistos[0], dataset.DatasetRootHistoBase):
                for i, drh in enumerate(datasetRootHistos[1:]):
                    if not isinstance(drh, dataset.DatasetRootHistoBase):
                        raise Exception("Input types can't be a mixture of DatasetRootHistoBase and something, datasetRootHistos[%d] is %s" % (i, drh.__class__.__name__))

                self.histoMgr = histograms.HistoManager(datasetRootHistos = datasetRootHistos)
            else:
                histoList = [_createHisto(h) for h in datasetRootHistos]
                # if isinstance(datasetRootHistos[0], ROOT.TH1):
                #     for i, h in enumerate(datasetRootHistos[1:]):
                #         if not isinstance(h, ROOT.TH1):
                #             raise Exception("Input types can't be a mixture of ROOT.TH1 and something, datasetRootHistos[%d] is %s" % (i, type(h).__name__))
                #     histoList = [histograms.Histo(th1, th1.GetName()) for th1 in datasetRootHistos]
                # elif isinstance(datasetRootHistos[0], ROOT.TGraph) or isinstance(datasetRootHistos[0], ROOT.TEfficiency):
                #     for i, h in enumerate(datasetRootHistos[1:]):
                #         if not isinstance(h, ROOT.TGraph) and not isinstance(h, ROOT.TEfficiency):
                #             raise Exception("Input types can't be a mixture of ROOT.TGraph/ROOT.TEfficiency and someting, datasetRootHistos[%d] is %s" % (i, type(h).__name__))
                #         if len(h.GetName()) == 0:
                #             raise Exception("For TGraph/TEfficiency input, the graph name must be set with TGraph.SetName() (name for datasetRootHistos[%d] is empty)" % i)
                #     histoList = [histograms.HistoGraph(gr, gr.GetName()) for gr in datasetRootHistos]

                self.histoMgr = histograms.HistoManager()
                for histo in histoList:
                    self.histoMgr.appendHisto(histo)
                
        else:
            self.histoMgr = histograms.HistoManager()

        # Save the format
        self.saveFormats = saveFormats

        self.plotObjectsBefore = []
        self.plotObjectsAfter = []

        self.drawOptions = {}

    ## Set the default legend styles
    #
    # Default is "F", except for data "PLE" and for signal MC "L"
    # 
    # Intended to be called from the deriving classes
    def _setLegendStyles(self):
        self.histoMgr.setHistoLegendStyleAll("F")
        for h in self.histoMgr.getHistos():
            if h.isData():
                h.setLegendStyle("PE")
            elif isSignal(h.getName()):
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

    ## Get the bin widths (assuming they're the same in all histograms)
    def binWidths(self):
        return self.histoMgr.getHistos()[0].getBinWidths()

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

    ## Set the legend header
    #
    # \param legendHeader String for legend header
    def setLegendHeader(self, legendHeader):
        self.legendHeader = legendHeader        

    ## Add an additional object to be drawn before the plot histograms/graphs
    #
    # \param obj      Object
    # \param option   Drawing option (given to obj.Draw())
    # \param index    Index in the list
    def prependPlotObject(self, obj, option="", index=None):
        t = (obj, option)
        if index is None:
            self.plotObjectsBefore.append(t)
        else:
            self.plotObjectsBefore.insert(index, t)

    ## Add an additional object to be drawn after the plot histograms/graphs
    #
    # \param obj      Object
    # \param option   Drawing option (given to obj.Draw())
    # \param index    Index in the list
    def appendPlotObject(self, obj, option="", index=None):
        t = (obj, option)
        if index is None:
            self.plotObjectsAfter.append(t)
        else:
            self.plotObjectsAfter.insert(index, t)

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
        systKey = "MCSystError"
        if histograms.uncertaintyMode.addStatToSyst():
            systKey = "MCStatSystError"
        self.histoMgr.addMCUncertainty(styles.getErrorStyle(), legendLabel=_legendLabels["MCStatError"], uncertaintyLegendLabel=_legendLabels[systKey])

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
            if hasattr(self, "legendHeader"):
                self.legend.SetHeader(self.legendHeader)
            self.legend.Draw()

        # Redraw the axes in order to get the tick marks on top of the
        # histogram
        self.getPad().RedrawAxis()


    ## Set the integrated luminosity of the data
    #
    # \param lumi   Integrated luminosity (in pb^-1)
    def setLuminosity(self, lumi):
        self.luminosity = lumi

    ## Add text for integrated luminosity
    #
    # \param x   X coordinate (in NDC, None for the default value)
    # \param y   Y coordinate (in NDC, None for the default value)
    #
    # Takes luminosity from self.luminosity member set by
    # setLuminosity() method if it exists. Otherwise forwards the call
    # to self.histoMgr. If setLuminosity() has been called with None,
    # no luminosity text is added.
    def addLuminosityText(self, x=None, y=None):
        histograms._printTextDeprecationWarning("plots.PlotBase.addLuminosityText()", "plots.PlotBase.addStandardTexts()")
        if hasattr(self, "luminosity"):
            if self.luminosity != None:
                histograms.addLuminosityText(x, y, self.luminosity)
        else:
            self.histoMgr.addLuminosityText(x, y)

    ## Set the energy
    #
    # \param energy   String of energy (or list of strings of energies), in TeV
    def setEnergy(self, energy):
        if isinstance(energy, basestring):
            self.energies = [energy]
        else:
            if len(energy) == 1:
                self.energies = energy[:]
            else:
                tmp = {}
                for e in energy:
                    tmp[e] = 1
                self.energies = tmp.keys()
                self.energies.sort()


    ## Add text for centre-of-mass energy
    #
    # \param x   X coordinate (in NDC, None for the default value)
    # \param y   Y coordinate (in NDC, None for the default value)
    #
    # Takes luminosity from self.energies member set by
    # setEnergyText() method if it exists. Otherwise the default
    # specified in histograms is used. If setEnergy() has been called
    # with None, no energy text is added.
    def addEnergyText(self, x=None, y=None):
        histograms._printTextDeprecationWarning("plots.PlotBase.addEnergyText()", "plots.PlotBase.addStandardTexts()")
        s = None
        if hasattr(self, "energies"):
            if self.energies != None:
                s = ", ".join(self.energies)
                s += " TeV"
        histograms.addEnergyText(x, y, s)

    ## Add standard CMS texts
    #
    # \param addLuminosityText  If True, add luminosity text (use stored luminosity)
    # \param kwargs             Keyword arguments, forwarded to histograms.addStandardTexts()
    def addStandardTexts(self, addLuminosityText=False, **kwargs):
        lumi = None
        if hasattr(self, "luminosity"):
            lumi = self.luminosity
        elif self.histoMgr.hasLuminosity():
            lumi = self.histoMgr.getLuminosity()
        elif addLuminosityText:
            raise Exception("addLuminosityText=True, but the Plot object does not have luminosity set, and plot.histoMgr has not been normalized by or to luminosity")

        s = None
        if hasattr(self, "energies"):
            if self.energies is not None:
                s = ", ".join(self.energies)
                s += " TeV"

        histograms.addStandardTexts(lumi=lumi, sqrts=s, **kwargs)

    ## Update drawing options
    #
    # \param kwargs   Keyword arguments (see plots.PlotDrawer())
    def setDrawOptions(self, **kwargs):
        # kwargs may contain dictionaries, we want to take a copy of
        # all of them
        self.drawOptions.update(copy.deepcopy(kwargs))

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
            self.cf.canvas.SaveAs(self.cf.canvas.GetName()+f)

        ROOT.gErrorIgnoreLevel = backup
        
    ## Save the plot to file(s)
    #
    # \param formats   Save to these formats (if not given, the values
    #                  given in the constructor and in
    #                  appendSaveFormat() are used
    # \param saveName  Alternative name for saving
    def saveAs(self, saveName, formats=None):
        if formats == None:
            formats = self.saveFormats

        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

        for f in formats:
            self.cf.canvas.SaveAs(saveName+f)

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
        self.ratioHistoMgr = histograms.HistoManager()

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
        if len(self.ratioHistoMgr) == 0:
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

    def hasFrame2(self):
        return hasattr(self.cf, "frame2")

    ## Get the upper TPad
    def getPad1(self):
        return self.cf.pad1

    ## Get the lower TPad
    def getPad2(self):
        return self.cf.pad2

    def hasPad2(self):
        return hasattr(self.cf, "pad2")

    ## Set the ratio histograms
    #
    # \param ratios  List of TH1/TGraph objects
    def setRatios(self, ratios):
        self.ratioHistoMgr.removeAllHistos()
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
        if isinstance(ratio, histograms.Histo):
            return ratio
        return _createHisto(ratio, drawStyle="EP")

    ## Add TH1/TGraph object to ratio pad
    #
    # \param ratio  TH1/TGraph object
    def appendRatio(self, ratio):
        self.ratioHistoMgr.appendHisto(self._createRatioObject(ratio))

    ## Addend TH1/TGraph objects to ratio pad
    #
    # \param ratios  List of TH1/TGraph objects
    def extendRatios(self, ratios):
        self.ratioHistoMgr.extendHistos([self._createRatioObject(r) for r in ratios])

    def setRatioLegend(self, legend):
        self.ratioLegend = legend
        self.ratioHistoMgr.addToLegend(legend)

    def removeRatioLegend(self):
        delattr(self, "legend")
        del self.ratioLegend

    def setRatioLegendHeader(self, legendHeader):
        self.ratioLegendHeader = legendHeader

    ## Create TCanvas and frame with ratio pad for single ratio
    #
    # \param filename         Name of the frame
    # \param numerator        Numerator TH1/TGraph
    # \param denominator      Denominator TH1/TGraph
    # \param ytitle           Y axis title for the ratio pad
    # \param invertRatio      Invert the roles of numerator and denominator
    # \param ratioIsBinomial  True for binomial ratio (e.g. efficiency) (\b deprecated)
    # \param ratioType        Type of the ratio, forwarded to _createRatioHistos() (None for default)
    # \param ratioErrorOptions Additional options for ratio error treatment
    # \param kwargs           Keyword arguments (forwarded to _createFrame())
    #
    # Intended for internal use only
    def _createFrameRatio(self, filename, numerator, denominator, ytitle, invertRatio=False, ratioIsBinomial=False, ratioType=None, ratioErrorOptions={}, **kwargs):
        (num, denom) = (numerator, denominator)
        if invertRatio:
            (num, denom) = (denom, num)

        if ratioIsBinomial:
            if ratioType is not None:
                raise Exception("You should not set (deprecated) ratioIsBinomial=True, and give ratioType (%s)." % ratioType)
            print "WARNING: ratioIsBinomial is deprepcated, please yse ratioType='binomial' instead"
            ratioType = "binomial"

        ratioHistos = _createRatioHistos(num, denom, ytitle, ratioType=ratioType, ratioErrorOptions=ratioErrorOptions)
        # Remove empty graphs (otherwise ROOT crashes when doing *.C version of graph)
        i = 0
        while i < len(ratioHistos):
	    if hasattr(ratioHistos[0],"getRootGraph"):
		if ratioHistos[i].getRootGraph().GetN() == 0:
		    ratioHistos[i].getRootGraph().Delete()
		    del ratioHistos[i]
		else:
		    i += 1
	    else:
		i += 1

        self.setRatios(ratioHistos)
        reorder = []
        for n in ["BackgroundStatSystError", "BackgroundStatError"]:
            if self.ratioHistoMgr.hasHisto(n):
                reorder.append(n)
        if len(reorder) > 0:
            self.ratioHistoMgr.reverse()
            self.ratioHistoMgr.reorderDraw(reorder)
            reorder.reverse()
            self.ratioHistoMgr.reorderLegend(reorder)
            self.ratioHistoMgr.reverse()

        self._createFrame(filename, **kwargs)

    ## Create TCanvas and frame with ratio pad for many ratios
    #
    # \param filename         Name of the frame
    # \param numerators       List of numerator TH1/TGraph objects
    # \param denominator      Denominator TH1/TGraph object
    # \param invertRatio      Invert the roles of numerator and denominator
    # \param ratioIsBinomial  True for binomial ratio (e.g. efficiency) (\b deprecated)
    # \param ratioType        Type of the ratio, forwarded to _createRatioHistos() (None for default)
    # \param ratioErrorOptions Additional options for ratio error treatment
    # \param kwargs           Keyword arguments (forwarded to _createFrame())
    #
    # Creates one ratio histogram for each numerator, as
    # numerator/denominator. If \a invertRatio is True, the ratios are
    # formed as denominator/numerator.
    #
    # Intended for internal use only
    def _createFrameRatioMany(self, filename, numerators, denominator, invertRatio=False, ratioIsBinomial=False, ratioType=None, ratioErrorOptions={}, **kwargs):
        
        if ratioIsBinomial:
            if ratioType is not None:
                raise Exception("You should not set (deprecated) ratioIsBinomial=True, and give ratioType (%s)." % ratioType)
            print "WARNING: ratioIsBinomial is deprepcated, please yse ratioType='binomial' instead"
            ratioType = "binomial"

        self.ratioHistoMgr.removeAllHistos()
        statSysError = None
        statError = None
        for numer in numerators:
            (num, denom) = (numer, denominator)
            if invertRatio:
                (num, denom) = (denom, num)
            ratioHistos = _createRatioHistos(num, denom, "Ratio", ratioType=ratioType, ratioErrorOptions=ratioErrorOptions)
            tmp = []
            for h in ratioHistos:
                if h.getName() == "BackgroundStatSystError":
                    statSysError = h
                elif h.getName() == "BackgroundStatError":
                    statError = h
                else:
                    if isinstance(numer, histograms.Histo):
                        aux.copyStyle(numer.getRootHisto(), h.getRootHisto())
                    elif isinstance(numer, dataset.RootHistoWithUncertainties):
                        aux.copyStyle(numer.getRootHisto(), h.getRootHisto())
                    else:
                        aux.copyStyle(numer, h.getRootHisto())
                        h = _createHisto(h)
                    tmp.append(h)
            #if len(tmp) > 1:
                #raise Exception("This shouldn't happen")
            self.extendRatios(tmp)

        reorder = []
        if statSysError is not None:
            self.ratioHistoMgr.appendHisto(statSysError)
            reorder.append(statSysError.getName())
        if statError is not None:
            self.ratioHistoMgr.appendHisto(statError)
            reorder.append(statError.getName())
        if len(reorder) > 0:
            self.ratioHistoMgr.reverse()
            self.ratioHistoMgr.reorderDraw(reorder)
            reorder.reverse()
            self.ratioHistoMgr.reorderLegend(reorder)
            self.ratioHistoMgr.reverse()

        self._createFrame(filename, **kwargs)

    ## Create TCanvas with ratio pads and frames
    #
    # \param filename       Name of frame
    # \param coverPadOpts   Options for overriding cover pad placement (see plots._createCoverPad)
    # \param kwargs         Keyword arguments (forwarded to histograms.CanvasFrameTwo.__init__())
    def _createFrame(self, filename, coverPadOpts={}, **kwargs):
        self.cf = histograms.CanvasFrameTwo(self.histoMgr, self.ratioHistoMgr, filename, **kwargs)
        self.frame = self.cf.frame
        self.cf.frame2.GetYaxis().SetNdivisions(505)
        self.coverPadOpts = coverPadOpts

    ## Add label for blinded range
    #
    # \param blindingRangeString   String containing the range for the blinding
    def addBlindingRangeString(self, blindingRangeString):
        self.blindingRangeString = blindingRangeString

    ## Draw the ratio histograms to the ratio pad
    def _draw(self):
        if len(self.ratioHistoMgr) == 0:
            return

        self.cf.canvas.cd(2)

        # Draw first stat+syst errors going to background
        until = None
        for n in ["BackgroundStatSystError", "BackgroundStatError"]:
            if self.ratioHistoMgr.hasHisto(n):
                until = n
        index = self.ratioHistoMgr.draw(untilName=until)

        # Then prepended plot objects
        for obj, option in self.ratioPlotObjectsBefore:
            obj.Draw(option+"same")

        # Then ratio line
        self.ratioLine = _createRatioLine(self.cf.frame.getXmin(), self.cf.frame.getXmax())
        self.ratioLine.Draw("L")

        # Then actual plot content
        if index is not None:
            self.ratioHistoMgr.draw(fromIndex=index+1)

        # And finally the appended plot objects
        for obj, option in self.ratioPlotObjectsAfter:
            obj.Draw(option+"same")

        if hasattr(self, "ratioLegend"):
            if hasattr(self, "ratioLegendHeader"):
                self.ratioLegend.SetHeader(self.ratioLegendHeader)
            self.ratioLegend.Draw()

        # Add label for blinded range
        if hasattr(self, "blindingRangeString"):
            # MK: Why this is not implemented in terms of ratioPlotObjectsAfter?
            histograms.addText(0.55, 0.38, "Data blinded: %s"%self.blindingRangeString, align="center", bold=True)

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

    ## \var ratioHistoManager
    # HistoManager for ratio histograms
    ## \var ratioLine
    # Holds the TGraph for ratio line, if ratio exists
    ## \var ratioCoverPad
    # Holds TPad to cover the larget Y axis value of the ratio TPad,
    # if ratio exists

## Base class for plots with same histogram from many datasets.
class PlotSameBase(PlotBase):
    ## Construct from DatasetManager and a histogram path
    #
    # \param datasetMgr            DatasetManager for datasets
    # \param name                  Path of the histogram in the ROOT files
    # \param normalizeToOne        Should the histograms be normalized to unit area?
    # \param datasetRootHistoArgs  Dictionary for keyword arguments to
    #                              dataset.DatasetManager.getDatasetRootHistos() method
    # \param kwargs                Keyword arguments, forwarded to PlotBase.__init__()
    def __init__(self, datasetMgr, name, normalizeToOne=False, datasetRootHistoArgs={}, **kwargs):
        PlotBase.__init__(self, datasetMgr.getDatasetRootHistos(name, **datasetRootHistoArgs), **kwargs)
        self.datasetMgr = datasetMgr
        self.rootHistoPath = name
        self.normalizeToOne = normalizeToOne

        self.setEnergy(self.datasetMgr.getEnergies())

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
        systKey = "MCSystError"
        if histograms.uncertaintyMode.addStatToSyst():
            systKey = "MCStatSystError"
        self.histoMgr.addMCUncertainty(styles.getErrorStyle(), nameList=["StackedMC"], legendLabel=_legendLabels["MCStatError"], uncertaintyLegendLabel=_legendLabels[systKey])

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

    ## Create TCanvas and frames for the histogram
    #
    # \param filename     Name for TCanvas (becomes the file name)
    # \param createRatio  Create also the ratio pad (ignored, provided to have similar interface with DataMCPlot)
    # \param kwargs       Keyword arguments, forwarded to PlotSameBase.createFrame() or PlotRatioBase._createFrameRatio()
    def createFrame(self, filename, createRatio=False, **kwargs):
        PlotSameBase.createFrame(self, filename, **kwargs)

    ## This is provided to have similar interface with DataMCPlot
    def createFrameFraction(self, filename, **kwargs):
        if "opts2" in kwargs:
            del kwargs["opts2"]
        self.createFrame(filename, **kwargs)


class DataMCPlot(PlotSameBase, PlotRatioBase):
    '''
    Class for data-MC comparison plot.
    
    Several assumptions have been made for this plotting class. If these
    are not met, one should consider either adding the feature to this
    class (if the required change is relatively small), or creating
    another class (if the change is large).
    <ul>
    <li> There can be exactly one histogram with the name "Data" for collision data
    <ul>

    <li> If the "Data" histogram is not there, this class works as
    plots.MCPlot, except normalization by cross section is not
    supported. Also the data/MC ratio is not drawn. </li>

    </ul></li>
    <li> There is always at least one MC histogram </li>

    <li> Only the MC histograms are stacked, and it should be done with the
    stackMCHistograms() method </li>

    <li> Data/MC ratio pad can be added to the same TCanvas, the MC
    considered in the ratio are the stacked ones </li>

    <li> The MC is normalized by the integrated luminosity of the collision
    data by default
    
    <ul>
    <li> Normalization to unit area (normalizeToOne) is also supported
    such that all non-stacked histograms are normalized to unit
    area, and the total area of stacked histograms is normalized to
    unit area while the ratios of the individual datasets is
    determined from the cross sections. The support is in the base class. </li>

    </ul></li>
    </ul>
    '''
    def __init__(self, datasetMgr, name, normalizeToLumi=None, **kwargs):
        '''
        Construct from DatasetManager and a histogram path
        
        \param datasetMgr       DatasetManager for datasets

        \param name             Path of the histogram in the ROOT files

        \param normalizeToLumi  If None, MC is implicitly normalized to
        the luminosity of data. If not None, MC is normalized to the this value of
        integrated luminosity (in pb^-1)

         \param kwargs           Keyword arguments, forwarded to PlotSameBase.__init__()
        '''
        PlotSameBase.__init__(self, datasetMgr, name, **kwargs)
        PlotRatioBase.__init__(self)
        
        # Normalize the MC histograms to the data luminosity
        if normalizeToLumi == None:
            self.histoMgr.normalizeMCByLuminosity()
        else:
            if datasetMgr.hasDataset("Data") and datasetMgr.getDataset("Data").isData():
                raise Exception("Got 'normalizeToLumi' while there is 'Data' dataset. You should use the 'Data' luminosity instead (i.e. do not give 'normalizeToLumi')")
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
        if createRatio and not self.histoMgr.hasHisto("Data"):
            print >> sys.stderr, "Warning: Trying to create data/MC ratio, but there is no 'Data' histogram."
            createRatio = False

        if not createRatio:
            args = {}
            args.update(kwargs)
            for key in kwargs.keys():
                if "ratio" in key:
                    del args[key]
            PlotSameBase.createFrame(self, filename, **args)
        else:
            if not self.histoMgr.hasHisto("StackedMC"):
                raise Exception("Must call stackMCHistograms() before createFrame() with ratio")

            self._normalizeToOne()
            self._createFrameRatio(filename,
                                   self.histoMgr.getHisto("Data").getRootHistoWithUncertainties(),
                                   self.histoMgr.getHisto("StackedMC").getSumRootHistoWithUncertainties(),
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
        systKey = "MCSystError"
        if histograms.uncertaintyMode.addStatToSyst():
            systKey = "MCStatSystError"
        if histograms.uncertaintyMode.equal(histograms.Uncertainty.SystOnly):
            self.histoMgr.addMCUncertainty(styles.getErrorStyle(), nameList=["StackedMC"], legendLabel=_legendLabels[systKey])
        else:
            self.histoMgr.addMCUncertainty(styles.getErrorStyle(), nameList=["StackedMC"], legendLabel=_legendLabels["MCStatError"], uncertaintyLegendLabel=_legendLabels[systKey])

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
                                   self.histoMgr.getHisto("Data").getRootHistoWithUncertainties(),
                                   self.histoMgr.getHisto("StackedMC").getSumRootHistoWithUncertainties(),
                                   "Data/MC", **kwargs)

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
    # \param kwargs             Keyword arguments (forwarded to plots.PlotBase.__init__())
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
            self._createFrameRatio(filename, histos[0].getRootHistoWithUncertainties(), histos[1].getRootHistoWithUncertainties(), "Ratio",
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
    # \param kwargs            Keyword arguments (forwarded to plots.PlotBase.__init__())
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
            self._createFrameRatioMany(filename, [h.getRootHistoWithUncertainties() for h in histos], reference.getRootHistoWithUncertainties(),
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
# \li Is x axis in log or linear scale
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
# The plot classes deriving from plots.PlotBase can also have draw
# options specified. These options override the default values
# (specified in the constructor and/or setDefaults()). The options
# given in __call__() override again the plot-object options.
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
    # \param xlabel              Default X axis title (None for pick from first TH1)
    # \param ylabel              Default Y axis title (None for pick from first TH1)
    # \param zlabel              Default Z axis title (None for not to show)
    # \param xlabelsize          Default Y axis label size (None for default)
    # \param ylabelsize          Default Y axis label size (None for default)
    # \param zhisto              Histo name for the Z information (for updating palette etc) (None for first histogram)
    # \param logx                Should X axis be in log scale by default?
    # \param log                 Should Y axis be in log scale by default?    
    # \param ratio               Should the ratio pad be drawn?
    # \param ratioYlabel         The Y axis title for the ratio pad (None for default)
    # \param ratioInvert         Should the ratio be inverted?
    # \param ratioIsBinomial     Is the ratio binomal (i.e. use Clopper-Pearson?) (deprecated)
    # \param ratioType           Ratio type (None for default)
    # \param ratioErrorOptions   Additional options for ratio error treatment
    # \param ratioCreateLegend   Default legend creation parameters for ratio (None to not to create legend, True to create with default parameters)
    # \param ratioMoveLegend     Default ratio legend movement parameters (after creation)
    # \param opts                Default frame bounds linear scale (see histograms._boundsArgs())
    # \param optsLog             Default frame bounds for log scale (see histograms._boundsArgs())
    # \param opts2               Default bounds for ratio pad (see histograms.CanvasFrameTwo and histograms._boundsArgs())
    # \param canvasOpts          Default canvas modifications (see histograms.CanvasFrame)
    # \param backgroundColor     Default plot background color (None for white)
    # \param rebin               Alias for \a rebinX (for backward compatibility)
    # \param rebinX              Default rebin X value (passed to TH1::Rebin or TH2::Rebin2D)
    # \param rebinY              Default rebin Y value (passed to TH2::Rebin2D)
    # \param rebinToWidthX       Default width of X bins to rebin to
    # \param rebinToWidthY       Default width of Y bins to rebin to (only applicable for TH2)
    # \param divideByBinWidth    Divide bin contents by bin width? (done after rebinning)
    # \param errorBarsX          Add vertical error bars (for all TH1's in the plot)? None for True if divideByBinWidth is True
    # \param createLegend        Default legend creation parameters (None to not to create legend)
    # \param moveLegend          Default legend movement parameters (after creation)
    # \param customizeBeforeFrame Function customize the plot before creating the canvas and frame
    # \param customizeBeforeDraw Function to customize the plot before drawing it
    # \param customizeBeforeSave Function to customize the plot before saving it
    # \param addLuminosityText   Should luminosity text be drawn?
    # \param stackMCHistograms   Should MC histograms be stacked?
    # \param addMCUncertainty    Should MC total (stat) uncertainty be drawn()
    # \param cmsText             If not None, overrides "CMS" text by-plot basis
    # \param cmsExtraText        If not none, overrides the "Preliminary" text by-plot basis
    # \param addCmsText          If False, do not add "CMS" text
    # \param cmsTextPosition     CMS text position (None for default value, see histograms.addStandardTexts() for more)
    # \param cmsExtraTextPosition CMS extra text position (None for default value, see histograms.addStandardTexts() for more)
    def __init__(self,
                 xlabel=None,
                 ylabel="Occurrances / %.0f",
                 zlabel=None,
                 xlabelsize = None,
                 ylabelsize = None,
                 zhisto=None,
                 log=False,
                 logx=False,
                 ratio=False,
                 ratioYlabel=None,
                 ratioInvert=False,
                 ratioIsBinomial=False,
                 ratioType=None,
                 ratioErrorOptions={},
                 ratioCreateLegend=None,
                 ratioMoveLegend={},
                 opts={},
                 optsLog={},
                 optsLogx={},
                 opts2={},
                 canvasOpts=None,
                 backgroundColor=None,
                 rebin=None,
                 rebinX=None,
                 rebinY=None,
                 rebinToWidthX=None,
                 rebinToWidthY=None,
                 divideByBinWidth=None,
                 errorBarsX=None,
                 createLegend={},
                 moveLegend={},
                 customizeBeforeFrame=None,
                 customizeBeforeDraw=None,
                 customizeBeforeSave=None,
                 addLuminosityText=False,
                 stackMCHistograms=False,
                 addMCUncertainty=False,
                 blindingRangeString=None,
                 cmsText=None,
                 cmsExtraText=None,
                 addCmsText=True,
                 cmsTextPosition=None,
                 cmsExtraTextPosition=None,
                 ):
        self.xlabelDefault = xlabel
        self.ylabelDefault = ylabel
        self.zlabelDefault = zlabel
        self.xlabelsizeDefault = xlabelsize;
        self.ylabelsizeDefault = ylabelsize;
        self.zhistoDefault = zhisto
        self.logDefault = log
        self.logxDefault = logx
        self.ratioDefault = ratio
        self.ratioYlabelDefault = ratioYlabel
        self.ratioInvertDefault = ratioInvert
        self.ratioIsBinomialDefault = ratioIsBinomial
        self.ratioTypeDefault = ratioType
        self.ratioErrorOptionsDefault = ratioErrorOptions
        self.ratioCreateLegendDefault = ratioCreateLegend
        self.ratioMoveLegendDefault = ratioMoveLegend
        self.optsDefault = {"ymin": 0, "ymaxfactor": 2.0}
        self.optsDefault.update(opts)
        self.optsLogDefault = {"ymin": 0.01, "ymaxfactor": 2.0}
        self.optsLogDefault.update(optsLog)
        self.optsLogxDefault = {"xmin": 5, "xmax": 10000}
        self.optsLogxDefault.update(optsLogx)
        self.opts2Default = {"ymin": 0.5, "ymax": 1.5}
        self.opts2Default.update(opts2)
        self.canvasOptsDefault = canvasOpts
        self.backgroundColorDefault = backgroundColor
        self.rebinDefault = rebin
        self.rebinXDefault = rebinX
        self.rebinYDefault = rebinY
        self.rebinToWidthXDefault = rebinToWidthX
        self.rebinToWidthYDefault = rebinToWidthY
        self.divideByBinWidthDefault = divideByBinWidth
        self.errorBarsXDefault = errorBarsX
        self.createLegendDefault = createLegend
        self.moveLegendDefault = moveLegend
        self.customizeBeforeFrameDefault = customizeBeforeFrame
        self.customizeBeforeDrawDefault = customizeBeforeDraw
        self.customizeBeforeSaveDefault = customizeBeforeSave
        self.addLuminosityTextDefault = addLuminosityText
        self.stackMCHistogramsDefault = stackMCHistograms
        self.addMCUncertaintyDefault = addMCUncertainty
        self.blindingRangeStringDefault = None
        self.cmsTextDefault = cmsText
        self.cmsExtraTextDefault = cmsExtraText
        self.addCmsTextDefault = addCmsText
        self.cmsTextPositionDefault = cmsTextPosition
        self.cmsExtraTextPositionDefault = cmsExtraTextPosition

    ## Modify the defaults
    #
    # \param kwargs   Keyword arguments (same arguments as for __init__())
    def setDefaults(self, **kwargs):
        for name, value in kwargs.iteritems():
            if not hasattr(self, name+"Default"):
                raise Exception("No default value for '%s'"%name)
            setattr(self, name+"Default", value)

    def _getValue(self, attr, p, args, attrPostfix="", useIfNone="", **kwargs):
        def _update(oldVal, newVal):
            if oldVal is None:
                return copy.deepcopy(newVal)
            if newVal is None:
                return None
            if hasattr(oldVal, "update"):
                oldVal.update(newVal)
                return oldVal
            return newVal

        if "default" in kwargs:
            defaultValue = kwargs["default"]
        else:
            defaultValue = getattr(self, attr+attrPostfix+"Default")
        ret = copy.deepcopy(defaultValue)

        try:
            ret = _update(ret, p.drawOptions[attr+attrPostfix])
        except KeyError:
            pass
        try:
            ret = _update(ret, args[attr])
        except KeyError:
            pass

        if ret is None and useIfNone != "":
            ret = self._getValue(useIfNone, p, args, attrPostfix=attrPostfix, **kwargs)

        return ret

    ## Draw the plot with function call syntax
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param name    Plot file name
    # \param kwargs  Keyword arguments (see below)
    #
    # Keyword arguments are forwarded to the methods doing the actual
    # work. These methods pick the arguments they are interested of.
    # For further documentation, please look the individual methods
    def __call__(self, p, name, *args, **kwargs):
        self.rebin(p, name, **kwargs)
        self.stackMCHistograms(p, **kwargs)
        self.createFrame(p, name, **kwargs)
        self.setLegend(p, **kwargs)
        self.addCutLineBox(p, **kwargs)
        self.customise(p, **kwargs)
        if len(args) > 1:
            raise Exception("At most 1 positional argument allowed (for xlabel), got %d" % len(args))
        elif len(args) == 1:
            if "xlabel" in kwargs:
                raise Exception("May not give positional arguments if xlabel is in kwargs")
            else:
                self.finish(p, xlabel=args[0], **kwargs)
        else:
            self.finish(p, **kwargs)

    ## Rebin all histograms in the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param name    Plot file name (for error message)
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a rebin          Alias for \a rebinX
    # \li\a rebinX         If given and larger than 1, rebin all histograms in
    #                      the plot (X axis for TH2). If list, pass it
    #                      as a double array to TH1::Rebin()
    # \li\a rebinY         If given and larger than 1, rebin all histograms in
    #                      the plot (only applicable for Y axis of
    #                      TH2)
    # \li\a rebinToWidthX  If given, rebin all histograms to this width of X bins.
    # \li\a rebinToWidthY  If given, rebin all histograms to this width of Y bins.
    # \li\a divideByBinWidth Divide bin contents by bin width? (done after rebinning)
    #
    # \b Note: Only one argument above per axis can be given.
    #
    # \b Note: Almost no error checking is done, except what is done in ROOT.
    def rebin(self, p, name, **kwargs):
        rebin = self._getValue("rebin", p, kwargs)
        rebinX = self._getValue("rebinX", p, kwargs)
        rebinY = self._getValue("rebinY", p, kwargs)
        rebinToWidthX = self._getValue("rebinToWidthX", p, kwargs)
        rebinToWidthY = self._getValue("rebinToWidthY", p, kwargs)

        if rebin is not None and rebinX is not None:
            raise Exception("Give either 'rebin' or 'rebinX', not both")
        if rebin is not None:
            rebinX = rebin

        # Use the one given as argument if both are non-None
        if rebinX is not None and rebinToWidthX is not None:
            if "rebin" in kwargs or "rebinX" in kwargs:
                rebinToWidthX = None
            if "rebinToWidthX" in kwargs:
                rebinX = None

            if rebinX is not None and rebinToWidthX is not None:
                raise Exception("Only one of 'rebinX' and 'rebinToWidthX' may be given as an argument.")
            if rebinX is not None:
                print "Plot '%s', argument 'rebinX=%s' overrides the default 'rebinToWidthX=%s'" % (name, str(rebinX), str(self.rebinToWidthXDefault))
            if rebinToWidthX is not None:
                print "Plot '%s', argument 'rebinToWidthX=%s' overrides the default 'rebinX=%s'" % (name, str(rebinToWidthX), str(self.rebinXDefault))
        if rebinY is not None and rebinToWidthY is not None:
            if "rebinY" in kwargs:
                rebinToWidthY = None
            if "rebinToWidthY" in kwargs:
                rebinY = None

            if rebinY is not None and rebinToWidthY is not None:
                raise Exception("Only one of 'rebinY' and 'rebinToWidthY' may be given as an argument.")
            if rebinY is not None:
                print "Plot '%s', argument 'rebinY=%s' overrides the default 'rebinToWidthY=%s'" % (name, str(rebinY), str(self.rebinToWidthYDefault))
            if rebinToWidthY is not None:
                print "Plot '%s', argument 'rebinToWidthY=%s' overrides the default 'rebinY=%s'" % (name, str(rebinToWidthY), str(self.rebinYDefault))


        rebinFunction = None
        if rebinX is not None and isinstance(rebinX, list):
            if len(rebinX) < 2:
                raise Exception("If 'rebinX' is a list, it must have at least two elements")
            n = len(rebinX)-1
            def rebinList(h):
                rhwu = h.getRootHistoWithUncertainties()
                if hasattr(rhwu.getRootHisto(), "Rebin2D"):
                    print >>sys.stderr, "WARNING: Plot '%s', trying to rebin TH2 histogram '%s' with nonequal bin sizes" % (name, h.getName())
                    return
                rhwu.Rebin(n, rhwu.GetName(), array.array("d", rebinX))

            rebinFunction = rebinList
        else:
            # In general (also if the original histogram has variable
            # bin widths) explicitly specifying the bin low edges is
            # the only way which works
            def rebinToWidthTH1(h):
                histo = h.getRootHistoWithUncertainties()
                xmin = histo.getXmin()
                xmax = histo.getXmax()
                nbins = (xmax-xmin)/rebinToWidthX
                intbins = int(nbins+0.5)
                # Check that the number of bins is integer
                diff = abs(intbins - nbins)
                if diff > 1e-3:
                    print >>sys.stderr, "WARNING: Trying to rebin histogram '%s' of plot '%s' for bin width %g, the X axis minimum is %g, maximum %g => number of bins would be %g, which is not integer (diff is %g)" % (h.getName(), name, rebinToWidthX, xmin, xmax, nbins, diff)
                    return

                nbins = intbins
                binLowEdgeList = [xmin + (xmax-xmin)/nbins*i for i in range(0, nbins+1)]
                rebinned = histo.Rebin(nbins, histo.GetName(), array.array("d", binLowEdgeList))
#                h.setRootHisto(rebinned)

            def rebinToWidth(h):
                histo = h.getRootHistoWithUncertainties()
                if not hasattr(histo.getRootHisto(), "Rebin2D"):
                    if rebinX is not None:
                        histo.Rebin(rebinX)
                    if rebinToWidthX is not None:
                        rebinToWidthTH1(h)
                    return
                th = histo.getRootHisto()

                rex = 1
                rey = 1

                if rebinX is not None:
                    rex = rebinX
                if rebinY is not None:
                    rey = rebinY
                if rebinToWidthX is not None:
                    xmin = histo.getXmin()
                    xmax = histo.getXmax()

                    nbinsx = (xmax-xmin)/rebinToWidthX
                    intbinsx = int(nbinsx+0.5)
                    
                    # Check that the requested binning makes sense
                    remainderX = th.GetNbinsX() % intbinsx
                    if remainderX != 0:
                        print >>sys.stderr, "WARNING: Trying to rebin histogram '%s' of plot '%s' for X bin width %g, the X axis minimum is %g, maximum %g => number of bins would be %g, which is not divisor of the number of bins %d, remainder is %d" % (h.getName(), name, rebinToWidthX, xmin, xmax, nbinsx, th.GetNbinsX(), remainderX)
                        return
                    rex = th.GetNbinsX()/intbinsx
                if rebinToWidthY is not None:
                    ymin = histo.getYmin()
                    ymax = histo.getYmax()
                    nbinsy = (ymax-ymin)/rebinToWidthY
                    intbinsy = int(nbinsy+0.5)

                    # Check that the requested binning makes sense
                    remainderY = th.GetNbinsY() % intbinsy
                    if remainderY != 0:
                        print >>sys.stderr, "WARNING: Trying to rebin histogram '%s' of plot '%s' for Y bin width %g, the Y axis minimum is %g, maximum %g => number of bins would be %g, which is not divisor of the number of bins %d, remainder is %d" % (h.getName(), name, rebinToWidthY, ymin, ymax, nbinsy, th.GetNbinsY(), remainderY)
                        return
                    rey = th.GetNbinsY()/intbinsy

                histo.Rebin2D(rex, rey)

            rebinFunction = rebinToWidth

        if rebinFunction is not None:
            p.histoMgr.forEachHisto(rebinFunction)

        if self._getValue("divideByBinWidth", p, kwargs):
            # TH1::Scale() with "width" option divides the histogram by bin width
            p.histoMgr.forEachHisto(lambda h: h.getRootHistoWithUncertainties().Scale(1, "width"))

    ## Stack MC histograms
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a  stackMCHistograms   Should MC histograms be stacked? (default given in __init__()/setDefaults())
    # \li\a  addMCUncertainty    If MC histograms are stacked, should MC total (stat) uncertainty be drawn? (default given in __init__()/setDefaults())
    def stackMCHistograms(self, p, **kwargs):
        stack = self._getValue("stackMCHistograms", p, kwargs)
        if stack:
            p.stackMCHistograms()
            if self._getValue("addMCUncertainty", p, kwargs):
                p.addMCUncertainty()

    ## Create TCanvas and TH1 for the plot frame
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param name    Plot file name
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a log          Should Y axis be in log scale? (default given in __init__()/setDefaults())
    # \li\a opts         Frame bounds (defaults given in __init__()/setDefaults())
    # \li\a opts2        Ratio pad bounds (defaults given in __init__()/setDefaults())
    # \lu\a canvasOpts   Dictionary for canvas modifications
    # \li\a ratio        Should ratio pad be drawn? (default given in __init__()/setDefaults())
    # \li\a ratioYlabel  The Y axis title for the ratio pad (None for default)
    # \li\a ratioInvert  Should the ratio be inverted?
    # \li\a ratioIsBinomial  Is the ratio a binomial?
    # \li\a ratioType    Type of the ratio calculation
    # \li\a ratioErrorOptions   Additional options for ratio error treatment
    # \li\a customizeBeforeFrame Function customize the plot before creating the canvas and frame
    # \li\a backgroundColor  Plot background color (None for white)
    def createFrame(self, p, name, **kwargs):
        customize = self._getValue("customizeBeforeFrame", p, kwargs)
        if customize is not None:
            customize(p)

        log = self._getValue("log", p, kwargs)
        logx = self._getValue("logx", p, kwargs)

        optsPostfix = ""
        if log:
            optsPostfix = "Log"
        if logx:
            optsPostfix = "Logx"

        _opts = self._getValue("opts", p, kwargs, optsPostfix)
        _opts2 = self._getValue("opts2", p, kwargs)

        # Not all plot objects have createRatio keyword argument in their createFrame() method
        args = {
            "opts": _opts,
            "opts2": _opts2,
        }
        ratio = self._getValue("ratio", p, kwargs)
        if ratio:
            args["createRatio"] = True
            args["ratioType"] = self._getValue("ratioType", p, kwargs)
            args["ratioErrorOptions"] = self._getValue("ratioErrorOptions", p, kwargs)
            if self._getValue("ratioInvert", p, kwargs):
                args["invertRatio"] = True
            if self._getValue("ratioIsBinomial", p, kwargs):
                args["ratioIsBinomial"] = True
        canvasOpts = self._getValue("canvasOpts", p, kwargs)
        if canvasOpts is not None:
            args["canvasOpts"] = canvasOpts

        # Set X-style error bars if wanted for possible use of ratioErrorScale and numerator being TH1
        errorBarsX = self._getValue("errorBarsX", p, kwargs, useIfNone="divideByBinWidth")
        if errorBarsX:
            # enable vertical error bar in the global TStyle
            errorXbackup = ROOT.gStyle.GetErrorX()
            ROOT.gStyle.SetErrorX(0.5)

        # Create frame
        p.createFrame(name, **args)
        if log:
            p.getPad().SetLogy(log)
        if logx:
            p.getPad().SetLogx(logx) 
            p.getPad2().SetLogx(logx)               

        if errorBarsX:
            ROOT.gStyle.SetErrorX(errorXbackup)

        # Override ratio ytitletd
        ratioYlabel = self._getValue("ratioYlabel", p, kwargs)
        if ratio and ratioYlabel is not None and p.hasFrame2():
            p.getFrame2().GetYaxis().SetTitle(ratioYlabel)

        # Hack the background color
        bkgColor = self._getValue("backgroundColor", p, kwargs)
        if bkgColor is not None:
            xaxis = p.getFrame().GetXaxis()
            yaxis = p.getFrame().GetYaxis()
            box = ROOT.TBox(xaxis.GetXmin(), yaxis.GetXmin(), xaxis.GetXmax(), yaxis.GetXmax())
            box.SetFillColor(bkgColor)
            p.prependPlotObject(box, index=0)

    ## Add a legend to the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a createLegend  Dictionary forwarded to histograms.creteLegend() (if None, don't create legend)
    # \li\a moveLegend    Dictionary forwarded to histograms.moveLegend() after creating the legend
    # \li\a ratio        Should ratio pad be drawn? (default given in __init__()/setDefaults())
    # \li\a ratioCreateLegend  Dictionary forwarded to histograms.creteLegend() (if None, don't create legend, if True, create with default parameters)
    # \li\a ratioMoveLegend    Dictionary forwarded to histograms.moveLegend() after creating the legend
    # \li\a errorBarsX          Add vertical error bars (for all TH1's in the plot)?  None for True if divideByBinWidth is True
    #
    # The default legend position should be set by modifying histograms.createLegend (see histograms.LegendCreator())
    def setLegend(self, p, **kwargs):
        createLegend = self._getValue("createLegend", p, kwargs)
        moveLegend = self._getValue("moveLegend", p, kwargs)

        # Add X error bar also to legend entries
        if self._getValue("errorBarsX", p, kwargs, useIfNone="divideByBinWidth"):
            # Add L to PE in legend styles
            histos = p.histoMgr.getHistos()
            if hasattr(p, "ratioHistoMgr"):
                histos.extend(p.ratioHistoMgr.getHistos())
            for histo in histos:
                lst = histo.getLegendStyle()
                if lst is None:
                    continue
                lst = lst.lower()
                if "p" in lst and "e" in lst and not "l" in lst:
                    histo.setLegendStyle(lst+"L")

        if createLegend is not None:
            p.setLegend(histograms.moveLegend(histograms.createLegend(**createLegend), **moveLegend))

        if self._getValue("ratio", p, kwargs):
            create = self._getValue("ratioCreateLegend", p, kwargs)
            move = self._getValue("ratioMoveLegend", p, kwargs)
            if create is not None:
                if create == True:
                    create = {}
                p.setRatioLegend(histograms.moveLegend(histograms.createLegendRatio(**create), **move))

    ## Add cut box and/or line to the plot
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a   cutLine   If given (and not None), should be a cut value or a list of cut values. Cut lines are drawn to the value points.
    # \li\a   cutBox    If given (and not None), should be a cut box specification or a list of specifications. For each specification, cut box and/or line is drawn according to the specification. Specification is a dictionary holding the parameters to plots._createCutBoxAndLine
    def addCutLineBox(self, p, **kwargs):
        cutLine = self._getValue("cutLine", p, kwargs, default=None)
        cutBox = self._getValue("cutBox", p, kwargs, default=None)
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
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a xlabel  X axis title (None for pick from first histogram)
    # \li\a ylabel              Y axis title. If contains a '%', it is assumed to be a format string containing one double and the bin width of the plot is given to the format string. (default given in __init__()/setDefaults())
    # \li\a zlabel              Z axis title. Only drawn if not None and TPaletteAxis exists
    # \li\a xlabelsize          X axis label size
    # \li\a ylabelsize          X axis label size
    # \li\a zhisto              Histo name for the Z information (for updating palette etc) (None for first histogram)
    # \li\a errorBarsX          Add vertical error bars (for all TH1's in the plot)?  None for True if divideByBinWidth is True
    # \li\a addLuminosityText   Should luminosity text be drawn? (default given in __init__()/setDefaults())
    # \li\a customizeBeforeDraw Function to customize the plot object before drawing the plot
    # \li\a customizeBeforeSave Function to customize the plot object before saving the plot
    # \li\a cmsText             If not None, overrides "CMS" text by-plot basis
    # \li\a cmsExtraText        If not none, overrides the "Preliminary" text by-plot basis
    # \li\a addCmsText          If False, do not add "CMS" text
    # \param cmsTextPosition     CMS text position (None for default value, see histograms.addStandardTexts() for more)
    # \param cmsExtraTextPosition CMS extra text position (None for default value, see histograms.addStandardTexts() for more)
    #
    # In addition of drawing and saving the plot, handles the X and Y
    # axis titles, and "CMS Preliminary", "sqrt(s)" and luminosity
    # texts.
    def finish(self, p, **kwargs):
        xlab = self._getValue("xlabel", p, kwargs)
        if xlab is None:
            xlab = p.histoMgr.getHistos()[0].getRootHisto().GetXaxis().GetTitle()
        p.frame.GetXaxis().SetTitle(xlab)
        ylabel = self._getValue("ylabel", p, kwargs)
        if ylabel is None:
            ylabel = p.histoMgr.getHistos()[0].getRootHisto().GetYaxis().GetTitle()
        else:
            nformats = ylabel.count("%")
            if nformats == 0:
                pass
            elif nformats == 1:
                ylabel = ylabel % p.binWidth()
            elif nformats == 2:
                binWidths = p.binWidths()
                ylabel = ylabel % (min(binWidths), max(binWidths))
            else:
                raise Exception("Got %d '%%' formats in y label ('%s'), only 0-2 are supported" % (nformats, ylabel))
        p.frame.GetYaxis().SetTitle(ylabel)
        xlabsize = self._getValue("xlabelsize", p, kwargs)
        if xlabsize is None:
            if not isinstance(p.histoMgr.getHistos()[0].getRootHisto(), ROOT.TEfficiency):
                xlabsize = p.histoMgr.getHistos()[0].getRootHisto().GetXaxis().GetLabelSize()
        else:
            p.frame.GetXaxis().SetLabelSize(xlabsize)
        ylabsize = self._getValue("ylabelsize", p, kwargs)
        if ylabsize is None:
            if not isinstance(p.histoMgr.getHistos()[0].getRootHisto(), ROOT.TEfficiency):
                ylabsize = p.histoMgr.getHistos()[0].getRootHisto().GetYaxis().GetLabelSize()
        else:
            p.frame.GetYaxis().SetLabelSize(ylabsize)

        customize = self._getValue("customizeBeforeDraw", p, kwargs)
        if customize != None:
            customize(p)

        # Add string for blinded range into the ratio plot
        blindingRangeString = self._getValue("blindingRangeString", p, kwargs)
        if blindingRangeString != None and isinstance(p, PlotRatioBase):
            p.addBlindingRangeString(blindingRangeString)

        # X error bar
        errorBarsX = self._getValue("errorBarsX", p, kwargs, useIfNone="divideByBinWidth")
        if errorBarsX:
            # enable vertical error bar in the global TStyle
            errorXbackup = ROOT.gStyle.GetErrorX()
            ROOT.gStyle.SetErrorX(0.5)

        p.draw()

        # Updates the possible Z axis label styles
        # Does nothing if the Z axis does not exist
        zlabel = self._getValue("zlabel", p, kwargs)
        zhisto = self._getValue("zhisto", p, kwargs)
        if zhisto is None:
            zrh = p.histoMgr.getHistos()[0].getRootHisto()
        else:
            zrh = p.histoMgr.getHisto(zhisto).getRootHisto()
        paletteAxis = histograms.updatePaletteStyle(zrh)
        if zlabel is not None and paletteAxis != None:
            paletteAxis.GetAxis().SetTitle(zlabel)

        p.addStandardTexts(addLuminosityText = self._getValue("addLuminosityText", p, kwargs),
                           addCmsText = self._getValue("addCmsText", p, kwargs),
                           cmsTextPosition = self._getValue("cmsTextPosition", p, kwargs),
                           cmsExtraTextPosition = self._getValue("cmsExtraTextPosition", p, kwargs),
                           cmsText = self._getValue("cmsText", p, kwargs),
                           cmsExtraText = self._getValue("cmsExtraText", p, kwargs))


        customize2 = self._getValue("customizeBeforeSave", p, kwargs)
        if customize2 is not None:
            customize2(p)

        p.save()

        if errorBarsX:
            ROOT.gStyle.SetErrorX(errorXbackup)


drawPlot = PlotDrawer()
