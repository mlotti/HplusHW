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
### directory. The returned object is of type DatasetSet.
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

############################### HISTOS ###############################
### Get set of histograms with the given path. The returned object is of
### type HistoSet, which contains a histogram from each dataset in
### DatasetSet. The histograms can be e.g. merged/stacked or normalized
### in various ways before drawing.
Rtau = datasets.getHistoSet("signalAnalysis/tau_Rtau")

### Print the list of datasets in the given HistoSet
#print "\n".join(Rtau.getDatasetNames())

### Example how to remove some datasets
#Rtau.removeDatasets(["QCD_Pt15_pythia6", "QCD_Pt15_pythia8", "QCD_Pt30",
#                       "QCD_Pt80", "QCD_Pt170", "QCD_Pt80to120_Fall10",
#                       "QCD_Pt120to170_Fall10", "QCD_Pt127to300_Fall10"])

############################### DATA ###############################
### Merge all collision data datasets to one, it has name "Data"
### Note: this must be done before normalizeMCByLuminosity()
#Rtau.mergeDataDatasets()

### Example how to set the luminosity of a data dataset
#Rtau.getDataset("Data").setLuminosity(5)

### The default normalization is no normalization (i.e. number of MC
### events for MC, and number of events for data)

############################### NORMALISE ###############################
### Normalize MC histograms to their cross section
#Rtau.normalizeMCByCrossSection()
#ylabel = "Cross section (pb)"

### Normalize MC histograms to the luminosity of the collision data in
# the HistoSet
#Rtau.normalizeMCByLuminosity()
#ylabel = "#tau cands / 1 GeV/c"

### Normalize MC histograms to an explicit luminosity in pb
Rtau.normalizeMCToLuminosity(10)
ylabel = "Events"

### Normalize the area of *all* histograms to 1
#Rtau.normalizeToOne()
#ylabel = "a.u"

############################### MERGING ###############################
### Example how to merge histograms of several datasets
# Rtau.mergeDatasets("QCD", ["QCD_Pt30to50", "QCD_Pt50to80", "QCD_Pt80to120", "QCD_Pt120to170", "QCD_Pt170to230", "QCD_Pt230to300"]) #uncomment me

### Example how to remove given datasets
#Rtau.removeDatasets(["QCD", "TTbar"])
#Rtau.removeDatasets(["TTToHpmToTauNu_M90", "QCD"])

############################### STYLES ###############################
### Example how to set legend labels from defaults
Rtau.setHistoLegendLabels(legendLabels) # many datasets, with dict

### Example how to modify legend styles
Rtau.setHistoLegendStyleAll("F")
Rtau.setHistoLegendStyle("Data", "p")

### Apply the default styles (for all histograms, for MC histograms, for a single histogram)
Rtau.applyStylesMC(styles.getStylesFill()) # Apply SetFillColor too, needed for histogram stacking
Rtau.applyStyle("Data", styles.getDataStyle())
#Rtau.setHistoDrawStyle("Data", "EP")

### Example how to stack all MC datasets. NOTE: this MUST be done after all legend/style manipulation
#Rtau.stackMCDatasets()

### Create TCanvas and TH1F such that they cover all histograms
(canvas, frame) = Rtau.createCanvasFrame("Rtau", ymin=0.01, ymax=None, xmin=0.0, xmax=1.05)

### Set the frame options, e.g. axis labels
frame.GetXaxis().SetTitle("R_{#tau}")
frame.GetYaxis().SetTitle(ylabel)

### Legend
legend = createLegend(0.7, 0.5, 0.9, 0.8)
Rtau.addToLegend(legend)

### Draw the plots
Rtau.draw()
legend.Draw()

### Set y-axis logarithmic (remember to give ymin for createCanvasFrame()
ROOT.gPad.SetLogy(True)

### The necessary texts, all take the position as arguments
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
Rtau.addLuminosityText() ### need to comment out if normalising to unity 

############################### EXECUTION ###############################
### Script execution can be paused like this, it will continue after
### user has given some input (which must include enter)
raw_input("Hit enter to continue") ### keep canvas open until you hit enter

############################### SAVING ###############################
### Save TCanvas as png
canvas.SaveAs(".png")
#canvas.SaveAs(".eps")
#canvas.SaveAs(".C")
