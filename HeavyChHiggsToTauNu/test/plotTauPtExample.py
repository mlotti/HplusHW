#!/usr/bin/env python

import ROOT
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

legendLabels = {
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


# Go to batch mode
ROOT.gROOT.SetBatch(True)

# Apply TDR style
style = TDRStyle()

# Construct datasets as stated in the multicrab.cfg of the execution
# directory. The returned object is of type DatasetSet.
datasets = getDatasetsFromMulticrabCfg()

# Construct datasets from the given list of CRAB task directories
#datasets = getDatasetsFromCrabDirs(["QCD_Pt120to170"])

# Construct datasets from a given list of (name, pathToRooTFile) pairs
#datasets = getDatasetsFromRootFiles([("QCD_Pt120to170", "QCD_Pt120to170/res/histograms-QCD_Pt120to170.root")])

# Get set of histograms with the given path. The returned object is of
# type HistoSet, which contains a histogram from each dataset in
# DatasetSet. The histograms can be e.g. merged/stacked or normalized
# in various ways before drawing.
tauPts = datasets.getHistoSet("signalAnalysis/tau_pt")

# Print the list of datasets in the given HistoSet
#print "\n".join(tauPts.getDatasetNames())


# The default normalization is no normalization (i.e. number of MC
# events for MC, and number of events for data)

# Normalize MC histograms to their cross section
#tauPts.normalizeMCByCrossSection()
#ylabel = "Cross section (pb)"

# Normalize MC histograms to the luminosity of the collision data in
# the HistoSet
#tauPts.normalizeMCByLuminosity()
#ylabel = "Events / 1 GeV/c"

# Normalize MC histograms to an explicit luminosity in pb
tauPts.normalizeMCToLuminosity(4)
ylabel = "#tau cands / 1 GeV/c"

# Normalize the area of *all* histograms to 1
#tauPts.normalizeToOne()
#ylabel = "A.u."

# Example how to merge histograms of several datasets
tauPts.mergeDatasets("QCD", ["QCD_Pt30to50", "QCD_Pt50to80", "QCD_Pt80to120",
                             "QCD_Pt120to170", "QCD_Pt170to230", "QCD_Pt230to300"])

# Example how to remove given datasets
#tauPts.removeDatasets(["QCD", "TTbar"])

# Example how to set legend labels from defaults
#tauPts.setHistoLegendLabel("TTbar_Htaunu_M80", "H^{#pm} M=80") # one dataset at a time
tauPts.setHistoLegendLabels(legendLabels) # many datasets, with dict

# Example how to modify legend styles
tauPts.setHistoLegendStyleAll("F")
tauPts.setHistoLegendStyle("Data", "p")

# Apply the default styles
#tauPts.applyStyles(styles.getStyles())
tauPts.applyStyles(styles.getStylesFill()) # Apply SetFillColor too, needed for histogram stacking
tauPts.applyStyle("Data", styles.getDataStyle())


# Example how to stack all MC datasets
# Note: this MUST be done after all legend/style manipulation
tauPts.stackMCDatasets()

# Create TCanvas and TH1F such that they cover all histograms
(canvas, frame) = tauPts.createCanvasFrame("taupt")
#(canvas, frame) = tauPts.createCanvasFrame("taupt", ymin=10, ymax=1e9) # for logy

# Set the frame options, e.g. axis labels
frame.GetXaxis().SetTitle("Tau p_{T} (GeV/c)")
frame.GetYaxis().SetTitle(ylabel)

# Legend
legend = createLegend(0.7, 0.5, 0.9, 0.8)
tauPts.addToLegend(legend)

# Draw the plots
tauPts.draw() # Normal draw, 
#tauPts.drawMCStacked() # Draw MC datasets as stacked
legend.Draw()

# Set y-axis logarithmic (remember to give ymin for createCanvasFrame()
#ROOT.gPad.SetLogy(True)

# The necessary texts, all take the position as arguments
addCmsPreliminaryText()
addEnergyText(x=0.3, y=0.85)
tauPts.addLuminosityText()

# Save TCanvas as png
canvas.SaveAs(".png")
