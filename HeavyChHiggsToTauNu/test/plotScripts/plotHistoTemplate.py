#!/usr/bin/env python

######################################################################
# Title          : plotTest.py 
# Authors        : Ritva Kinnunen, Matti Kortelainen, Alexandros Attikis
# Description    : This is an example plotting script. 
######################################################################

# This file is an example. It might not do exactly what you want, and
# it might contain more features than you need. Please do not edit and
# commit this file, unless your intention is to change the example.

interactiveMode = False

import ROOT
ROOT.gROOT.SetBatch(not interactiveMode)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configurations
analysis = "signalAnalysis"
# Data era affects on the set of selected data datasets, and the PU
# weights (via TDirectory name in histograms.root)
dataEra = "Run2011A" #dataEra = "Run2011B" #dataEra = "Run2011AB"

mcOnly = False
#mcOnly = True
mcOnlyLumi = 2300 # pb

lightHplusMassPoint = 120
lightHplusTopBR = 0.05

# main function
def main():
    # Read the datasets
    #datasets = dataset.getDatasetsFromMulticrabCfg(directory="/Volumes/disk/attikis/HIG-12-037/TreeAnalysis_v44_4_130113_105229/", analysisName=analysis, dataEra=dataEra)
    datasets = dataset.getDatasetsFromMulticrabCfg(analysisName=analysis, searchMode="Light", dataEra=dataEra, optimizationMode="OptTaupt40byMediumCombinedIsolationDeltaBetaCorrRtau07JetGEQ3Et20BetaGT02Met100BjetGEQ1Et20discr09and09Dphi160ToprecoNone")

    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()

    datasets.updateNAllEventsToPUWeighted()    
    plots.mergeRenameReorderForDataMC(datasets)

    if mcOnly:
        print "*** Int.Lumi (manually set)", mcOnlyLumi
    else:
        print "*** Int.Lumi",datasets.getDataset("Data").getLuminosity()
    print "*** norm=",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M%d"%lightHplusMassPoint in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    # Change legend creator defaults
    histograms.createLegend.moveDefaults(dx=-0.05)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=lightHplusTopBR, br_Htaunu=1)
    # Example how to set cross section to a specific MSSM point
    #xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    # Merge signals into one dataset (per mass point)
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Replace signal dataset with a signal+background dataset, where
    # the BR(t->H+) is taken into account for SM ttbar
    plots.replaceLightHplusWithSignalPlusBackground(datasets)
    
    # You can print a tree of all the merged datasets with this
    #datasets.printDatasetTree()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    if interactiveMode:
        raw_input("*** Press \"Enter\" to exit pyROOT: ")

# Default plot drawing options, all of these can be overridden in the
# individual drawPlot() calls
drawPlot = plots.PlotDrawer(log=True, addLuminosityText=True, stackMCHistograms=True, addMCUncertainty=True)

# Define plots to draw
def doPlots(datasets):
    def createPlot(name, massbr_x=0.42, massbr_y=0.87, normone_x=0.25, normone_y=0.5, **kwargs):
        args = {}
        args.update(kwargs)
        if mcOnly:
            args["normalizeToLumi"] = mcOnlyLumi

        p = plots.DataMCPlot(datasets, name, **args)
        addMassBRText(p, massbr_x, massbr_y)
        if kwargs.get("normalizeToOne", False):
            p.appendPlotObject(histograms.PlotText(normone_x, normone_y, "Normalized to unit area", size=17))
        return p

    # drawPlot defaults can be modified also here
    if not mcOnly:
        drawPlot.setDefaults(ratio=True)

    drawPlot(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBJets", xlabel="Number of selected b jets", ylabel="Events", opts={"xmax": 6}, cutLine=1)

    # opts2 is for the ratio pad
    drawPlot(createPlot("Met"), "Met", xlabel="Type-I corrected PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", rebinToWidthX=20, opts={"ymaxfactor": 10}, opts2={"ymin": 0, "ymax": 2}, cutLine=60)

    # Normalizing to unit area
    drawPlot(createPlot("Vertices/verticesTriggeredAfterWeight", normalizeToOne=True, massbr_x=0.65, massbr_y=0.5, normone_x=0.62, normone_y=0.4),
             "verticesAfterWeightTriggered", xlabel="Number of reconstructed vertices", ylabel="Events", log=False, opts={"xmax": 20}, addLuminosityText=False)

# Helper function to add mHplus and BR    
def addMassBRText(plot, x, y):
    size = 20
    separation = 0.04

    massText = "m_{H^{+}} = %d GeV/c^{2}" % lightHplusMassPoint
    brText = "#it{B}(t #rightarrow bH^{+})=%.2f" % lightHplusTopBR

    plot.appendPlotObject(histograms.PlotText(x, y, massText, size=size))
    plot.appendPlotObject(histograms.PlotText(x, y-separation, brText, size=size))
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
