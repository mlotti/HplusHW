#!/usr/bin/env python

###########################################################################
#
# Author: Stefan Richter
#
###########################################################################


import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles


#------------------------------Configure---------------------------------#
#dirs = ["/afs/cern.ch/user/s/strichte/HeavyChHiggsToTauNu/test/multicrab_130125_153632"]
#dirs = ["/afs/cern.ch/user/s/strichte/HeavyChHiggsToTauNu/test/multicrab_130129_125309"]
dirs = ["/afs/cern.ch/user/s/strichte/HeavyChHiggsToTauNu/test/multicrab_130205_103013"]

analysis = "signalAnalysis"
counters = analysis+"/counters"

mcOnly = False
mcOnlyLumi = 5000 # pb

#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

# Go to batch mode, comment if interactive mode is wanted
ROOT.gROOT.SetBatch(True)
#-------------------------------------------------------------------------#

# Apply TDR style
style = tdrstyle.TDRStyle()

# Construct the datasets
datasets = dataset.getDatasetsFromMulticrabDirs(dirs, counters=counters, dataEra=dataEra, analysisBaseName="signalAnalysis")
if not mcOnly:
    datasets.loadLuminosities()
datasets.updateNAllEventsToPUWeighted()

plots.mergeRenameReorderForDataMC(datasets)

# This can be used to merge datasets:
#datasets.merge("TTJetsPlusWJets", ["TTJets", "WJets"], keepSources=True)

# Override the data luminosity (should not be used except for testing)
#datasets.getDataset("Data").setLuminosity(35)



# Create the plot, the latter argument is the path to the histogram in the ROOT files
if mcOnly:
    h = plots.MCPlot(datasets, analysis+"/FullHiggsMass/HiggsMass", normalizeToLumi=mcOnlyLumi)
else:    
    h = plots.DataMCPlot(datasets, analysis+"/FullHiggsMass/HiggsMass")

# TTJets
drh_reco = datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/FullHiggsMass/HiggsMass")
drh_gen = datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genFullHiggsMass")

drh_reco.normalizeToLuminosity(mcOnlyLumi)
drh_gen.normalizeToLuminosity(mcOnlyLumi)

h_reco = drh_reco.getHistogram() # returns TH1
h_gen = drh_gen.getHistogram()

h_reco.SetName("Reco")
h_gen.SetName("Gen")

h = plots.ComparisonPlot(h_reco, h_gen)
h.histoMgr.forEachHisto(styles.generator())

# Stack MC histograms
#h.stackMCHistograms()
#h.stackMCHistograms(stackSignal=True)

#h.addMCUncertainty()

# # Create canvas and frame for only the distributions
h.createFrame("Full_Higgs_mass")
# h.frame.GetXaxis().SetTitle("m_H (GeV)")
# h.frame.GetYaxis().SetTitle("events / ? GeV")

# # Create legend
h.setLegend(histograms.createLegend())

# # Draw the histograms and the legend
h.draw()

# # Add the necessary pieces of text
# histograms.addCmsPreliminaryText()
# histograms.addEnergyText()
# h.addLuminosityText()

# Save to .png, .eps and .C file
h.save()




# #  counters = "qcdMeasurementMethod2Part1Counters/weighted"
# # Same, but create two pads, one for the distributions and another for
# # the data/MC
# h = plots.DataMCPlot(datasets, "qcdMeasurementMethod2Part1Counters/TauSelection_all_tau_candidates_pt")
# h.stackMCHistograms()
# h.addMCUncertainty()
# h.createFrameFraction("taupt_new2",)
# h.frame.GetXaxis().SetTitle("#tau p_{T} (GeV/c)")
# h.frame.GetYaxis().SetTitle("#tau cands / 1 GeV/c")
# h.setLegend(histograms.createLegend())
# h.draw()
# histograms.addCmsPreliminaryText()
# histograms.addEnergyText()
# h.addLuminosityText()
# h.save()

# # Script execution can be paused like this, it will continue after
# # user has given some input (which must include enter)
# #raw_input("Hit enter to continue")



######################## IMPLEMENT LATER:
# dirs = []
# dirs.append(sys.argv[1])
        
