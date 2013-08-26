#!/usr/bin/env python
########################################################################
# -*- python -*-
#       File Name:  myPlots.py
# Original Author:  Matti Kortelainen
#          Editor:  Alexandros Attikis
#         Created:  Mon 4 Oct 2010
#     Description:  ROOT plotting macro
#       Institute:  UCY
#         e-mail :  attikis@cern.ch
#        Comments:  
########################################################################

import ROOT
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

############################### LEGENDS ###############################
legendLabels = {
    "Data":                "Data",
    "TTbar_Htaunu_M80":    "H^{#pm} M=80",
    "TTToHpmToTauNu_M90":  "H^{#pm} M=90",
    "TTToHpmToTauNu_M100": "H^{#pm} M=100",
    "TTToHpmToTauNu_M120": "H^{#pm} M=120",
    "TTbar_Htaunu_M140":   "H^{#pm} M=140",
    "TTbar_Htaunu_M160":   "H^{#pm} M=160",
    "TTbar":               "t#bar{t}",
    "TTbarJets":           "t#bar{t}+jets",
    "WJets":               "W+jets",
    "QCD_Pt30to50":        "QCD, 30 < #hat{p}_T < 50",
    "QCD_Pt50to80":        "QCD, 50 < #hat{p}_T < 80",
    "QCD_Pt80to120":       "QCD, 80 < #hat{p}_T < 120",
    "QCD_Pt120to170":      "QCD, 120 < #hat{p}_T < 170",
    "QCD_Pt170to230":      "QCD, 170 < #hat{p}_T < 230",
    "QCD_Pt230to300":      "QCD, 230 < #hat{p}_T < 300"
    }
############################### CUSTOMISATION ###############################
### Go to batch mode, comment if interactive mode is wanted (see on the
### bottom of the script how to make it to wait input from user)
# ROOT.gROOT.SetBatch(True) # Comment out to open canvases

### Apply TDR style
style = TDRStyle()

############################### DATASETS ###############################
### Construct datasets as stated in the multicrab.cfg of the execution
### directory. The returned object is of type DatasetManager.
#datasets = getDatasetsFromMulticrabCfg() ## uncomment me

### Construct datasets from the given list of CRAB task directories
#datasets = getDatasetsFromCrabDirs(["TTToHpmToTauNu_M100"]) ### example: single dataset
#datasets = getDatasetsFromCrabDirs(["TTbar_Htaunu_M80", "TTToHpmToTauNu_M90", "TTToHpmToTauNu_M100","TTToHpmToTauNu_M120","TTbar_Htaunu_M140", "TTbar_Htaunu_M160", "QCD_Pt30to50", "QCD_Pt50to80", "QCD_Pt80to120", "QCD_Pt120to170"]) ### example: list of datasets

### Construct datasets from a given list of (name, pathToRooTFile) pairs
#datasets = getDatasetsFromRootFiles([("QCD_Pt50to80", "QCD_Pt50to80/res/histograms_1_1_zCl.root")])
#datasets = getDatasetsFromRootFiles([("WJets", "WJets/res/histograms_32_1_f4s.root")])
#datasets = getDatasetsFromRootFiles([("TTbar", "TTbar/res/histograms_3_1_oN4.root")])
#datasets = getDatasetsFromRootFiles([("TTToHpmToTauNu_M100", "TTToHpmToTauNu_M100/res/histograms_1_1_6Ac.root")])
datasets = getDatasetsFromRootFiles([("TTToHpmToTauNu_M120", "TTToHpmToTauNu_M120/res/histograms_1_1_nRc.root")]) ## comment me
datasets.updateNAllEventsToPUWeighted()

############################### MERGING ###############################
### Example how to merge histograms of several datasets
# datasets.merge("QCD", ["QCD_Pt30to50", "QCD_Pt50to80", "QCD_Pt80to120", "QCD_Pt120to170", "QCD_Pt170to230", "QCD_Pt230to300"]) #uncomment me

### Example how to remove some datasets
#datasets.remove(["QCD_Pt15_pythia6", "QCD_Pt15_pythia8", "QCD_Pt30",
#                       "QCD_Pt80", "QCD_Pt170", "QCD_Pt80to120_Fall10",
#                       "QCD_Pt120to170_Fall10", "QCD_Pt127to300_Fall10"])


############################### HISTOS ###############################
### Get set of histograms with the given path. The returned object is of
### type HistoManager, which contains a histogram from each dataset in
### DatasetManager. The histograms can be e.g. merged/stacked or normalized
### in various ways before drawing.
TauIsolTrkPt = HistoManager(datasets, "signalAnalysis/tau_isoltrk_pt")

### Print the list of datasets in the given HistoManager
#print "\n".join(TauIsolTrkPt.getDatasetNames())

############################### DATA ###############################
### Merge all collision data datasets to one, it has name "Data"
### Note: this must be done before normalizeMCByLuminosity()
#TauIsolTrkPt.mergeDataDatasets()

### Example how to set the luminosity of a data dataset
#TauIsolTrkPt.getDataset("Data").setLuminosity(5)

### The default normalization is no normalization (i.e. number of MC
### events for MC, and number of events for data)

############################### NORMALISE ###############################
### Normalize MC histograms to their cross section
#TauIsolTrkPt.normalizeMCByCrossSection()
#ylabel = "Cross section (pb)"

### Normalize MC histograms to the luminosity of the collision data in
# the HistoManager
#TauIsolTrkPt.normalizeMCByLuminosity()
#ylabel = "#tau cands / 1 GeV/c"

### Normalize MC histograms to an explicit luminosity in pb
TauIsolTrkPt.normalizeMCToLuminosity(10)
ylabel = "Events"

### Normalize the area of *all* histograms to 1
#TauIsolTrkPt.normalizeToOne()
#ylabel = "a.u"

############################### STYLES ###############################
### Example how to set legend labels from defaults
TauIsolTrkPt.setHistoLegendLabelMany(legendLabels) # many datasets, with dict

### Example how to modify legend styles
TauIsolTrkPt.setHistoLegendStyleAll("F")
TauIsolTrkPt.setHistoLegendStyle("Data", "p")

### Apply the default styles (for all histograms, for MC histograms, for a single histogram)
TauIsolTrkPt.forEachMCHisto(styles.generator(fill=True)) # Apply SetFillColor too, needed for histogram stacking
TauIsolTrkPt.forHisto("Data", styles.getDataStyle())
#TauIsolTrkPt.setHistoDrawStyle("Data", "EP")

### Example how to stack all MC datasets. NOTE: this MUST be done after all legend/style manipulation
#TauIsolTrkPt.stackMCDatasets()

### Create TCanvas and TH1F such that they cover all histograms
cf = CanvasFrame(TauIsolTrkPt, "TauIsolTrkPt", ymin=0.01, ymax=None, xmin=0.0, xmax=20.0)

### Set the frame options, e.g. axis labels
cf.frame.GetXaxis().SetTitle("#tau-jet, Ldg Trk in Isol Annulus, p_{T} (GeV/c)")
cf.frame.GetYaxis().SetTitle(ylabel)

### Legend
legend = createLegend(0.7, 0.5, 0.9, 0.8)
TauIsolTrkPt.addToLegend(legend)

### Draw the plots
TauIsolTrkPt.draw()
legend.Draw()

### Set y-axis logarithmic (remember to give ymin for createCanvasFrame()
ROOT.gPad.SetLogy(True)

### The necessary texts, all take the position as arguments
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
TauIsolTrkPt.addLuminosityText() ### need to comment out if normalising to unity 

############################### EXECUTION ###############################
### Script execution can be paused like this, it will continue after
### user has given some input (which must include enter)
raw_input("Hit enter to continue") ### keep canvas open until you hit enter

############################### SAVING ###############################
### Save TCanvas as png
cf.canvas.SaveAs(".png")
#cf.canvas.SaveAs(".eps")
#cf.canvas.SaveAs(".C")
