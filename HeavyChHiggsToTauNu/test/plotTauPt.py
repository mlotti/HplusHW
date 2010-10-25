#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################


import ROOT
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

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
    "QCD_Pt230to300":      "QCD, 230 < #hat{p}_T < 300"}


# Go to batch mode, comment if interactive mode is wanted (see on the
# bottom of the script how to make it to wait input from user)
ROOT.gROOT.SetBatch(True)

# Apply TDR style
style = TDRStyle()

# Construct datasets as stated in the multicrab.cfg of the execution
# directory. The returned object is of type DatasetSet.
datasets = getDatasetsFromMulticrabCfg()

# Construct datasets from the given list of CRAB task directories
#datasets = getDatasetsFromCrabDirs(["QCD_Pt120to170"])
#datasets = getDatasetsFromCrabDirs(["TTbar_Htaunu_M80"])

# Construct datasets from a given list of (name, pathToRooTFile) pairs
#datasets = getDatasetsFromRootFiles([("QCD_Pt120to170", "QCD_Pt120to170/res/histograms-QCD_Pt120to170.root")])

# Get set of histograms with the given path. The returned object is of
# type HistoSet, which contains a histogram from each dataset in
# DatasetSet. The histograms can be e.g. merged/stacked or normalized
# in various ways before drawing.
tauPts = datasets.getHistoSet("signalAnalysis/tau_pt")

# Print the list of datasets in the given HistoSet
#print "\n".join(tauPts.getDatasetNames())

# Example how to remove some datasets
tauPts.removeDatasets([
#    "BTau_146240-146729",
    "TTbar_Htaunu_M80",
    "TTToHpmToTauNu_M90",
    "TTToHpmToTauNu_M100",
    #"TTToHpmToTauNu_M120",
    "TTbar_Htaunu_M140",
    "TTbar_Htaunu_M160",
    "TTbar",
    "QCD_Pt15_pythia6", "QCD_Pt15_pythia8", "QCD_Pt30",
    "QCD_Pt80", "QCD_Pt170", "QCD_Pt80to120_Fall10",
    "QCD_Pt120to170_Fall10", "QCD_Pt127to300_Fall10"])

# Merge all collision data datasets to one, it has name "Data"
# Note: this must be done before normalizeMCByLuminosity()
tauPts.mergeDataDatasets()

# Example how to set the luminosity of a data dataset
#tauPts.getDataset("Data").setLuminosity(5)

# The default normalization is no normalization (i.e. number of MC
# events for MC, and number of events for data)

# Normalize MC histograms to their cross section
#tauPts.normalizeMCByCrossSection()
#ylabel = "Cross section (pb)"

# Normalize MC histograms to the luminosity of the collision data in
# the HistoSet
#tauPts.normalizeMCByLuminosity()
#ylabel = "#tau cands / 1 GeV/c"

# Normalize MC histograms to an explicit luminosity in pb
tauPts.normalizeMCToLuminosity(1.473)
ylabel = "#tau cands / 1 GeV/c"

# Normalize the area of *all* histograms to 1
#tauPts.normalizeToOne()
#ylabel = "A.u."

# Example how to merge histograms of several datasets
tauPts.mergeDatasets("QCD", ["QCD_Pt30to50", "QCD_Pt50to80", "QCD_Pt80to120",
                             "QCD_Pt120to170", "QCD_Pt170to230", "QCD_Pt230to300"])

# Example how to set legend labels from defaults
#tauPts.setHistoLegendLabel("TTbar_Htaunu_M80", "H^{#pm} M=80") # one dataset at a time
tauPts.setHistoLegendLabels(legendLabels) # many datasets, with dict


mcDatasetNames = tauPts.getMCDatasetNames()
stackedMcDatasetNames = mcDatasetNames[:]
del stackedMcDatasetNames[stackedMcDatasetNames.index("TTToHpmToTauNu_M120")]

# Example how to modify legend styles
tauPts.setHistoLegendStyleAll("F")
tauPts.setHistoLegendStyle("Data", "p")
tauPts.setHistoLegendStyle("TTToHpmToTauNu_M120", "l")

# Apply the default styles (for all histograms, for MC histograms, for a single histogram)
tauPts.applyStylesMC(styles.getStylesFill()) # Apply SetFillColor too, needed for histogram stacking
tauPts.applyStyle("Data", styles.getDataStyle())
tauPts.applyStyle("TTToHpmToTauNu_M120", styles.getStyles()[0])
tauPts.setHistoDrawStyle("Data", "EP")


# Example how to stack all MC datasets
# Note: this MUST be done after all legend/style manipulation
#tauPts.stackMCDatasets()
tauPts.stackDatasets("MC", stackedMcDatasetNames)

# Create TCanvas and TH1F such that they cover all histograms
(canvas, frame) = tauPts.createCanvasFrame("taupt")
(canvas, frame) = tauPts.createCanvasFrame("taupt", ymin=1, ymax=80000000) # for logy

# Set the frame options, e.g. axis labels
frame.GetXaxis().SetTitle("Tau p_{T} (GeV/c)")
frame.GetYaxis().SetTitle(ylabel)

# Legend
legend = createLegend(0.7, 0.5, 0.9, 0.8)
tauPts.addToLegend(legend)

# Draw the plots
tauPts.draw()
legend.Draw()

# Set y-axis logarithmic (remember to give ymin for createCanvasFrame()
ROOT.gPad.SetLogy(True)

# The necessary texts, all take the position as arguments
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
tauPts.addLuminosityText()


# Script execution can be paused like this, it will continue after
# user has given some input (which must include enter)
#raw_input("Hit enter to continue")


# Save TCanvas as png
canvas.SaveAs(".png")
#canvas.SaveAs(".eps")
canvas.SaveAs(".C")
