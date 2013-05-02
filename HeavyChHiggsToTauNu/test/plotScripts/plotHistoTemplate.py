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
#dataEra = "Run2011A" #dataEra = "Run2011B" #dataEra = "Run2011AB"
dataEra = "Run2012AB"

mcOnly = False
#mcOnly = True
mcOnlyLumi = 2300 # pb

lightHplusMassPoint = 120
lightHplusTopBR = 0.05

# main function
def main():
    # Read the datasets, see twiki page for more examples
    # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicSoftware#Construct_datasets
    #
    # This one constructs datasets assuming that the multicrab
    # directory is the working directory
    datasets = dataset.getDatasetsFromMulticrabCfg(analysisName=analysis, dataEra=dataEra)

    # This one constructs from some other multicrab directory, the
    # path can be absolute or relative
    #datasets = dataset.getDatasetsFromMulticrabCfg(directory="/path/to/your/multicrab/directory", analysisName=analysis, dataEra=dataEra)

    # Usually you can also omit the analysisName, as it can be detected automatically
    # datasets = dataset.getDatasetsFromMulticrabCfg(dataEra=dataEra)

    # If you have both light and heavy analysis and/or optimization
    # enabled, you have to specify searchMode and/or optimizationMode
    # explicitly
    # datasets = dataset.getDatasetsFromMulticrabCfg(searchMode="Light", dataEra=dataEra, optimizationMode="Opt...")

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
    datasets.remove(filter(lambda name: "Hplus_taunu_" in name, datasets.getAllDatasetNames()))

    # Change legend creator defaults
    histograms.createLegend.moveDefaults(dx=-0.05)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=lightHplusTopBR, br_Htaunu=1)
    # Example how to set cross section to a specific MSSM point
    #xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)
    histograms.createSignalText.set(mass=lightHplusMassPoint)

    # Merge TT->WH+ and TT->H+H- signals into one dataset (per mass point)
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Merge T->H+ signals into one dataset (per mass point)
    #plots.mergeSingleTopHplus(datasets)

    # Merge TT->WH+, TT->H+H-, and T->H+ signals into one dataset (per mass point)
    #plots.mergeLightHplus(datasets)

    # Replace signal dataset with a signal+background dataset, where
    # the BR(t->H+) is taken into account for SM ttbar
    plots.replaceLightHplusWithSignalPlusBackground(datasets)
    
    # You can print a tree of all the merged datasets with this
    #datasets.printDatasetTree()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Create counters
    doCounters(datasets)

    if interactiveMode:
        raw_input("*** Press \"Enter\" to exit pyROOT: ")

# Default plot drawing options, all of these can be overridden in the
# individual drawPlot() calls
drawPlot = plots.PlotDrawer(log=True, addLuminosityText=True, stackMCHistograms=True, addMCUncertainty=True)

# Define plots to draw
def doPlots(datasets):
    def createPlot(name, massbr_x=0.42, massbr_y=0.9, normone_x=0.25, normone_y=0.5, **kwargs):
        # For MC-only mode (and only then), we have to set the luminosity to which MC is normalized explicitly
        args = {}
        args.update(kwargs)
        if mcOnly:
            args["normalizeToLumi"] = mcOnlyLumi

        p = plots.DataMCPlot(datasets, name, **args)
        p.appendPlotObject(histograms.createSignalText(xmin=massbr_x, ymax=massbr_y))
        if kwargs.get("normalizeToOne", False):
            p.appendPlotObject(histograms.PlotText(normone_x, normone_y, "Normalized to unit area", size=17))
        return p

    # Create a plot of one TH2 histogram of a given dataset
    def createTH2Plot(name, datasetName, normalizeToOne=False):
        # Obtain the Dataset object for the given dataset
        dset = datasets.getDataset(datasetName)

        # Pick the luminosity of data if not in MC-only mode
        lumi = mcOnlyLumi
        if datasets.hasDataset("Data") and not mcOnly:
            lumi = datasets.getDataset("Data").getLuminosity()

        # Obtain a DatasetRootHisto wrapper object for the TH2
        # histogram, create a plot object, and if the Dataset is MC,
        # normalize it to the luminosity
        drh = dset.getDatasetRootHisto(name)
        p = plots.PlotBase([drh])
        if normalizeToOne:
            p.histoMgr.normalizeToOne()
            p.setDrawOptions(addLuminosityText=False)
        else:
            if dset.isMC():
                p.histoMgr.normalizeMCToLuminosity(lumi)

        p.histoMgr.setHistoDrawStyleAll("COLZ")

        # Example how to set drawing options on the plot object
        # itself. These override the default, and the options given in
        # drawPlot() override these
        p.setDrawOptions(ratio=False, stackMCHistograms=False, addMCUncertainty=False,
                         #canvasOpts={"addWidth": None} # example of how do disable automatic canvas size modification in the presence of COLZ
                         )
        return p

    # drawPlot defaults can be modified also here
    if not mcOnly:
        drawPlot.setDefaults(ratio=True)

    drawPlot(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBJets", xlabel="Number of selected b jets", ylabel="Events", opts={"xmax": 6}, cutLine=1)

    # opts2 is for the ratio pad
    drawPlot(createPlot("Met"), "Met", xlabel="Type-I corrected PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", rebinToWidthX=20, opts={"ymaxfactor": 10}, opts2={"ymin": 0, "ymax": 2}, cutLine=60)

    # Normalizing to unit area
    drawPlot(createPlot("Vertices/verticesTriggeredAfterWeight", normalizeToOne=True, massbr_x=0.65, massbr_y=0.6, normone_x=0.62, normone_y=0.4),
             "verticesAfterWeightTriggered", xlabel="Number of reconstructed vertices", ylabel="Events", log=False, opts={"xmax": 20}, addLuminosityText=False)

    # TH2 and COLZ, disable legend
    drawPlot(createTH2Plot("TauSelection/TauSelection_selected_taus_eta_vs_phi", "TTJets"), "selectedtau_etavsphi_ttjets", xlabel="#tau #eta", ylabel="#tau #phi", zlabel="Events", log=False, createLegend=None)

    # Rebinning of TH2 (also rebinX and rebinY work), also background color and normalization to unit area
    drawPlot(createTH2Plot("TauSelection/TauSelection_selected_taus_eta_vs_phi", "TTJets", normalizeToOne=True), "selectedtau_etavsphi_ttjets_rebin", xlabel="#tau #eta", ylabel="#tau #phi", zlabel="Events", log=False, createLegend=None, rebinToWidthX=0.2, rebinToWidthY=2*3.14159/24, backgroundColor=ROOT.kGray)

    # Examples of couple of palettes available in (recent) ROOT and which might be better than the rainbow
    # http://root.cern.ch/drupal/content/rainbow-color-map
    def drawExample(postfix):
        drawPlot(createTH2Plot("TauSelection/TauSelection_selected_taus_eta_vs_phi", "TTJets"), "selectedtau_etavsphi_ttjets_"+postfix, xlabel="#tau #eta", ylabel="#tau #phi", zlabel="Events", log=False, createLegend=None)
    tdrstyle.setDarkBodyRadiatorPalette()
    drawExample("darkbodyradiator")

    tdrstyle.setDeepSeaPalette()
    drawExample("deepsea")

    tdrstyle.setGreyScalePalette()
    drawExample("greyscale")

    tdrstyle.setTwoColorHuePalette()
    drawExample("twocolorhue")

def doCounters(datasets):
    # Create EventCounter object, holds all counters of all datasets
    eventCounter = counter.EventCounter(datasets)

    # Normalize counters
    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcOnlyLumi)
    else:
        eventCounter.normalizeMCByLuminosity()

    # Get table (counter.CounterTable) of the main counter, format it
    # with default formatting, and print
    #print eventCounter.getMainCounterTable().format()

    # Create LaTeX format, automatically adjust value precision by uncertainty
    latexFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))

    # Get table of a subcounter, format it with a predefined format,
    # and print
    #print eventCounter.getSubCounterTable("TauIDPassedEvt::TauSelection_HPS").format(latexFormat)

    # Create EventCounter from one dataset
    eventCounter = counter.EventCounter(datasets.getAllDatasets()[0])
    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcOnlyLumi)
    else:
        eventCounter.normalizeMCByLuminosity()

    #print eventCounter.getMainCounterTable().format()

   
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
