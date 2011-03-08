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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

# Go to batch mode, comment if interactive mode is wanted (see on the
# bottom of the script how to make it to wait input from user)
ROOT.gROOT.SetBatch(True)

# Apply TDR style
style = tdrstyle.TDRStyle()


# Construct datasets as stated in the multicrab.cfg of the execution
# directory. The returned object is of type DatasetManager.
counters = "signalAnalysisTauSelectionHPSTightTauBasedCounters"
# Embedded+signal analysis
datasetsEmbSig = dataset.getDatasetsFromMulticrabCfg(counters = counters)
# signal analysis
datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile="../../multicrab_110307_141642/multicrab.cfg", counters=counters)

# Construct datasets from the given list of CRAB task directories
#datasets = dataset.getDatasetsFromCrabDirs(["QCD_Pt120to170"])
#datasets = dataset.getDatasetsFromCrabDirs(["TTbar_Htaunu_M80"])

# Construct datasets from a given list of (name, pathToRooTFile) pairs
#datasets = dataset.getDatasetsFromRootFiles([("QCD_Pt120to170", "QCD_Pt120to170/res/histograms-QCD_Pt120to170.root")])

#datasets.remove(["WJets_TuneD6T_Winter10", "TTJets_TuneD6T_Winter10", "Mu_136035-144114_Dec22", "Mu_146428-147116_Dec22", "Mu_147196-149294_Dec22", "TTToHplusBWB_M120_Winter10"])
#datasets.remove(["WJets_TuneD6T_Winter10", "TTJets_TuneD6T_Winter10","TTToHplusBWB_M120_Winter10", "DYJetsToLL_M50_TuneZ2_Winter10", "TToBLNu_s-channel_TuneZ2_Winter10", "TToBLNu_t-channel_TuneZ2_Winter10","TToBLNu_tW-channel_TuneZ2_Winter10","QCD_Pt20_MuEnriched_TuneZ2_Winter10"])
# Load dataset luminosities from a 'lumi.json' file
datasetsEmbSig.loadLuminosities()

# Merge:
#  - all data datasets to 'Data'
#  - all QCD datasets to 'QCD'
#  - all single top datasets to 'SingleTop'
# Rename the physical dataset names to logical (essentially drop the Tune and Winter10)
# Reorder to the 'standard' order, all 'nonstandard' are left to the end
datasetsSig.selectAndReorder(["TTJets_TuneZ2_Winter10", "WJets_TuneZ2_Winter10"]) # pick only TT and W
plots.mergeRenameReorderForDataMC(datasetsEmbSig)
plots.mergeRenameReorderForDataMC(datasetsSig)
datasetsEmbSig.selectAndReorder(["Data"]) # pick only Data

# datasets has the embedded+signal analysis data, and signal analysis TT+W
datasets = datasetsEmbSig
datasets.extend(datasetsSig) 

# Create the plot, latter argument is the path to the histogram in the ROOT files
h = plots.DataMCPlot(datasets, "signalAnalysisTauSelectionHPSTightTauBased/TauEmbeddingAnalysis_begin_embeddingMet")

h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))

# Stack MC histograms
h.stackMCHistograms()
#tauPt.stackMCHistograms(stackSignal=True) # Stack also the signal datasets?

h.addMCUncertainty()

# Create canvas and frame for only the distributions
#h.createFrame("taupt_new", ymin=0.1, ymax=1e4)
h.createFrame("MetSimulateEmbedded_begin", ymin=0.001, ymaxfactor=2)
h.frame.GetXaxis().SetTitle("MET (GeV)")
h.frame.GetYaxis().SetTitle("Events / 1 GeV")

# Create legend
h.setLegend(histograms.createLegend())

ROOT.gPad.SetLogy(True)

# Draw the histograms and the legend
h.draw()

# Add the necessary pieces of text
histograms.addCmsPreliminaryText()
histograms.addEnergyText()
h.addLuminosityText()

# Save to .png, .eps and .C file
h.save()

#  counters = "qcdMeasurementMethod2Part1Counters/weighted"
# Same, but create two pads, one for the distributions and another for
# the data/MC
h = plots.DataMCPlot(datasets, "signalAnalysisTauSelectionHPSTightTauBased/TauEmbeddingAnalysis_begin_embeddingMet")
h.stackMCHistograms()
#h.addMCUncertainty()
h.createFrameFraction("MetSimulateEmbedded_begin2", opts={"ymin": 0.001, "ymaxfactor": 2})
ROOT.gPad.SetLogy(True)

h.frame.GetXaxis().SetTitle("MET (GeV)")
h.frame.GetYaxis().SetTitle("Events / 1 GeV")
h.setLegend(histograms.createLegend())
h.draw()
histograms.addCmsPreliminaryText()
histograms.addEnergyText()
h.addLuminosityText()
h.save()

# Script execution can be paused like this, it will continue after
# user has given some input (which must include enter)
#raw_input("Hit enter to continue")
