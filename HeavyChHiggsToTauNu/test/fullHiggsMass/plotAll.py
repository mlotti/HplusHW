#!/usr/bin/env python

##################################################################################################
# Title          : classificationPlots.py
# Author(s)      : Stefan Richter (based heavily on template test/plotScripts/plotHistoTemplate.py
#                  by Ritva Kinnunen, Matti Kortelainen, Alexandros Attikis)
# Description    : 
##################################################################################################

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
#multicrabDir = "../multicrab_130418_114926"
multicrabDir = "../multicrab_130417_135419"

cutInfoSuffix = ""
if multicrabDir == "../multicrab_130418_114926":
    cutInfoSuffix = "_noTopMassCut"

analysis = "signalAnalysis"
# Data era affects on the set of selected data datasets, and the PU
# weights (via TDirectory name in histograms.root)
#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

#plotSignalOnly = True
plotSignalOnly = False
#plotAllMassPointsTogether = True
plotAllMassPointsTogether = False
mcOnly = True
#mcOnly = False
mcOnlyLumi = 5000 # 1/pb
# Set lightHplusMassPoint to a value < 0 if you want to plot all the masses:
#lightHplusMassPoint = 120
#lightHplusMassPoints = [80, 90, 100, 120, 140, 150, 155, 160]
lightHplusMassPoints = [80, 100, 120, 140, 160]
lightHplusTopBR = 0.02
removeQCD = True
#removeQCD = False
massPlotBinWidth = 20 # GeV
discriminantPlotBinWidth = 5000 # GeV^2
#massPlotNormToOne = True
massPlotNormToOne = False

counterLabels = {
    "Greater solution closest": "max-|p_{#nu, z}|",
    "Smaller solution closest": "min-|p_{#nu, z}|",
    "TauNuAngleMax solution closest": "max-#alpha_{#tau, #nu}",
    "TauNuAngleMin solution closest": "min-#alpha_{#tau, #nu}",
    "TauNuDeltaEtaMax solution closest": "max-#Delta#eta_{#tau, #nu}",
    "TauNuDeltaEtaMin solution closest": "min-#Delta#eta_{#tau, #nu}",
    }

# Change legend creator defaults
histograms.createLegend.moveDefaults(dx=-0.05)

# main function
def main():
    for lightHplusMassPoint in lightHplusMassPoints:
        doEverything(lightHplusMassPoint)

def doEverything(lightHplusMassPoint):
    print "MultiCRAB directory is", multicrabDir
    
    # Read the datasets, see twiki page for more examples
    # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicSoftware#Construct_datasets
    # Usually you can also omit the analysisName, as it can be detected automatically
    # If you have optimization enabled, you have to specify optimizationMode explicitly (optimizationMode="Opt...") 
    if plotSignalOnly:
        datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabDir, analysisName=analysis, dataEra=dataEra,
                                                       includeOnlyTasks="TTToHplus")
    else:
        datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabDir, analysisName=analysis, dataEra=dataEra)

    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()

    datasets.updateNAllEventsToPUWeighted()
    plots.mergeRenameReorderForDataMC(datasets)

    if mcOnly:
        myIntegratedLuminosity = mcOnlyLumi
    else:
        myIntegratedLuminosity = datasets.getDataset("Data").getLuminosity()
    print "*** Integrated luminosity", myIntegratedLuminosity, "/pb"
    # print "*** Norm =",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()    

    # Remove signal datasets except for the desired mass (if specified)
    if not plotAllMassPointsTogether:
        datasets.remove(filter(lambda name: "TTToHplus" in name and not "M%d"%lightHplusMassPoint in name,
                               datasets.getAllDatasetNames()))
    # Remove heavy charged Higgs signal datasets
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    # Remove QCD datasets (because the simulated QCD background is negligible but has huge artefacts)
    if removeQCD:
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=lightHplusTopBR, br_Htaunu=1)
    # Example how to set cross section to a specific MSSM point
    #xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    myXSect = datasets.getDataset("TTToHplusBWB_M%d"%lightHplusMassPoint).getCrossSection()
    myNormFactor = datasets.getDataset("TTToHplusBWB_M%d"%lightHplusMassPoint).getNormFactor()
    myNAll = datasets.getDataset("TTToHplusBWB_M%d"%lightHplusMassPoint).getNAllEvents()
    print "### HW cross section =", myXSect

    # Merge signals into one dataset (per mass point)
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    
    
    # Replace signal dataset with a signal+background dataset, where
    # the BR(t->H+) is taken into account for SM ttbar
    if not plotSignalOnly:
        plots.replaceLightHplusWithSignalPlusBackground(datasets)
    
    # You can print a tree of all the merged datasets with this
    #datasets.printDatasetTree()

    # Apply TDR style
    style = tdrstyle.TDRStyle()



    # Calculate N_signal/N_background and Poisson significance of signal
    #numberOfSignalEvents = datasets.getDataset("TTToHplus_M120").getCrossSection() * myIntegratedLuminosity
    numberOfSignalEvents = myXSect * myIntegratedLuminosity
    print "###", datasets.getDataset("TTToHplus_M%d"%lightHplusMassPoint).getCrossSection()
    print "###", myIntegratedLuminosity
    print "*** Number of signal events:", numberOfSignalEvents
    print "*** ...or:", myNormFactor * myNAll * myIntegratedLuminosity
    
    # names = datasetMgr.getAllDatasetNames()
    #d_ttjets = datasets.getDataset("TTJets")
    #print d_ttjets.getNAllEvents()




    # Create plots
    doPlots(datasets, lightHplusMassPoint)

    doCounters(datasets)

    if interactiveMode:
        raw_input("*** Press \"Enter\" to exit pyROOT: ")

# Default plot drawing options, all of these can be overridden in the
# individual drawPlot() calls
drawPlot = plots.PlotDrawer(log=True, addLuminosityText=True, stackMCHistograms=True, addMCUncertainty=True)
if plotSignalOnly:
    drawPlot = plots.PlotDrawer(log=True, addLuminosityText=True, stackMCHistograms=False, addMCUncertainty=False)
    

# Define plots to draw
def doPlots(datasets, lightHplusMassPoint):
    def createPlot(name, massbr_x=0.67, massbr_y=0.58, normone_x=0.67, normone_y=0.58, **kwargs):
        args = {}
        args.update(kwargs)
        if mcOnly:
            args["normalizeToLumi"] = mcOnlyLumi

        p = plots.DataMCPlot(datasets, name, **args)
        addMassBRText(p, massbr_x, massbr_y, lightHplusMassPoint)
        #p.addCutBoxAndLine(cutValue=0)
        if kwargs.get("normalizeToOne", False):
            p.appendPlotObject(histograms.PlotText(normone_x, normone_y+0.03, "Normalized to unit area", size=17))
        if removeQCD and not plotSignalOnly:
            #p.appendPlotObject(histograms.PlotText(2.7*normone_x, normone_y, "#splitline{QCD background}{not shown}",
            p.appendPlotObject(histograms.PlotText(normone_x,  normone_y-0.10, "#splitline{QCD background}{not shown}",
                                                   size=17, color=2))
        return p

    # Create a plot of one TH2 histogram of a given dataset
    def createTH2Plot(name, datasetName):
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
        if dset.isMC():
            p.histoMgr.normalizeMCToLuminosity(lumi)
                
        p.histoMgr.setHistoDrawStyleAll("COLZ")
        
        # Example how to set drawing options on the plot object
        # itself. These override the default, and the options given in
        # drawPlot() override these
        p.setDrawOptions(ratio=False, stackMCHistograms=False, addMCUncertainty=False,
                         #canvasOpts={"addWidth": None}
                         # example of how do disable automatic canvas size modification in the presence of COLZ
                         )
        return p
        
        
    # drawPlot defaults can be modified also here
    if not mcOnly:
        drawPlot.setDefaults(ratio=True)
    #drawPlot.setDefaults(opts={"xmin":0, "xmax": 300})
    #drawPlot.setDefaults(opts={"ymin":0, "ymax": 70})


    # specify common parts of the plots' names
    nameSuffix = ""
    if not plotAllMassPointsTogether:
        nameSuffix = "_M%d"%lightHplusMassPoint
    if plotSignalOnly:
        nameSuffix = nameSuffix + "_signalOnly"
#     if removeQCD:
#         nameSuffix = nameSuffix + "_noQCD"
#     if massPlotNormToOne:
#         nameSuffix = nameSuffix + "_normToOne"




    # PLOT: top invariant mass in generator
#     drawPlot(createPlot("FullHiggsMass/TopInvariantMassInGenerator", normalizeToOne=massPlotNormToOne),
#              "TopInvariantMassInGenerator"+nameSuffix, xlabel="m(b, #tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth,
#              log=False, rebinToWidthX=massPlotBinWidth)

    # PLOT: Higgs invariant mass using the chosen selection method (RECO, GEN, GEN_NuToMET)
    drawPlot(createPlot("FullHiggsMass/HiggsMass", normalizeToOne=massPlotNormToOne), "HiggsMass"+cutInfoSuffix+nameSuffix,
             xlabel="m_{#tau, #nu_{#tau}}", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
             cutLine=lightHplusMassPoint)
#     if plotSignalOnly:
#         drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN", normalizeToOne=massPlotNormToOne),
#                  "HiggsMass_GEN"+nameSuffix+"_TauNuAngleMax",
#                  xlabel="m_{#tau, #nu_{#tau}} (MC truth)",
#                  ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
#         drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN_NeutrinosReplacedWithMET", normalizeToOne=massPlotNormToOne),
#                  "HiggsMass_GEN_NuToMET"+nameSuffix+"_TauNuAngleMax",
#                  xlabel="m_{#tau, #nu_{#tau}} (MC truth, #nu_{#tau} #leftrightarrow  #slash{E}_{T})",
#                  ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)

    # PLOT: Higgs invariant mass using the chosen selection method, positive discriminant only
    drawPlot(createPlot("FullHiggsMass/HiggsMassPositiveDiscriminant", normalizeToOne=massPlotNormToOne),
             "HiggsMassPosDisc"+nameSuffix,
             xlabel="m_{#tau, #nu_{#tau}}", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
             cutLine=lightHplusMassPoint)

    # PLOT: Higgs invariant mass using the chosen selection method, negative discriminant only
    drawPlot(createPlot("FullHiggsMass/HiggsMassNegativeDiscriminant", normalizeToOne=massPlotNormToOne),
             "HiggsMassNegDisc"+cutInfoSuffix+nameSuffix,
             xlabel="m_{#tau, #nu_{#tau}}", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
             cutLine=lightHplusMassPoint)


    # PLOT: Higgs invariant mass for each different selection method
#     selectionMethods = [
#         "greater",
#         "smaller",
#         "tauNuAngleMax",
#         "tauNuAngleMin",
#         "tauNuDeltaEtaMax",
#         "tauNuDeltaEtaMin"
#         ]
#     for selectionMethod in selectionMethods:
#         drawPlot(createPlot("FullHiggsMass/HiggsMass_"+selectionMethod, normalizeToOne=massPlotNormToOne),
#                  "HiggsMass_"+selectionMethod+nameSuffix,
#                  xlabel="m_{#tau, #nu_{#tau}} ["+selectionMethod+"]", ylabel="Events / %d GeV"%massPlotBinWidth, log=False,
#                  rebinToWidthX=massPlotBinWidth)
#         if plotSignalOnly:
#             drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN_"+selectionMethod, normalizeToOne=massPlotNormToOne),
#                      "HiggsMass_GEN_"+selectionMethod+nameSuffix,
#                      xlabel="m_{#tau, #nu_{#tau}} (MC truth) ["+selectionMethod+"]",
#                      ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
#             drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN_NuToMET_"+selectionMethod, normalizeToOne=massPlotNormToOne),
#                      "HiggsMass_GEN_NuToMET_"+selectionMethod+nameSuffix,
#                      xlabel="m_{#tau, #nu_{#tau}} (MC truth, #nu_{#tau} #leftrightarrow  #slash{E}_{T}) ["+selectionMethod+"]",
#                      ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
    

#     # PLOT: HiggsMassPure
#     drawPlot(createPlot("FullHiggsMass/HiggsMassPure", normalizeToOne=massPlotNormToOne), "HiggsMassPure"+nameSuffix, xlabel="m(#tau, #nu_{#tau}) of pure events", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
#     # PLOT: HiggsMassImpure
#     drawPlot(createPlot("FullHiggsMass/HiggsMassImpure", normalizeToOne=massPlotNormToOne), "HiggsMassImpure"+nameSuffix, xlabel="m(#tau, #nu_{#tau}) of events with mis-ID", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)

    # PLOT: Transverse mass
    drawPlot(createPlot("transverseMass", normalizeToOne=massPlotNormToOne),
             "TransverseMass"+nameSuffix,
             xlabel="m_{T}", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)

    # PLOT: Transverse mass versus invariant mass
    # TH2 and COLZ, disable legend
    tdrstyle.setDeepSeaPalette()
    drawPlot(createTH2Plot("FullHiggsMass/TransMassVsInvMass", "TTToHplus_M%d"%lightHplusMassPoint),
             "TransMassVsInvMass"+cutInfoSuffix+nameSuffix,
             xlabel="(M_{H^{+}} = %d GeV)          m_{T}"%lightHplusMassPoint, ylabel="m_{#tau, #nu_{#tau}}",
             zlabel="Events", log=False, createLegend=None,
             opts={"xmax": 200, "ymax": 200}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)
    if not plotSignalOnly:
        drawPlot(createTH2Plot("FullHiggsMass/TransMassVsInvMass", "TTJets"),
                 "TransMassVsInvMass_ttbarOnly"+cutInfoSuffix,
                 xlabel="(t#bar{t} only)          m_{T}", ylabel="m_{#tau, #nu_{#tau}}", zlabel="Events",
                 log=False, createLegend=None,
                 opts={"xmax": 200, "ymax": 200}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)

#     # Examples of couple of palettes available in (recent) ROOT and which might be better than the rainbow
#     # http://root.cern.ch/drupal/content/rainbow-color-map
#     def drawExample(postfix):
#         drawPlot(createTH2Plot("TauSelection/TauSelection_selected_taus_eta_vs_phi", "TTJets"),
#                  "selectedtau_etavsphi_ttjets_"+postfix, xlabel="#tau #eta", ylabel="#tau #phi",
#                  zlabel="Events", log=False, createLegend=None)
#     tdrstyle.setDarkBodyRadiatorPalette()
#     drawExample("darkbodyradiator")

    #tdrstyle.setDarkBodyRadiatorPalette()
    
#     drawExample("deepsea")
    
#     tdrstyle.setGreyScalePalette()
#     drawExample("greyscale")
    
#     tdrstyle.setTwoColorHuePalette()
#     drawExample("twocolorhue")


    # PLOT: Discriminant (RECO, GEN, GEN_NuToMET)
    drawPlot(createPlot("FullHiggsMass/Discriminant", normalizeToOne=massPlotNormToOne), "Discriminant"+nameSuffix,
             xlabel = "Discriminant", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0)
    drawPlot(createPlot("FullHiggsMass/Discriminant_GEN", normalizeToOne=massPlotNormToOne), "Discriminant_GEN"+nameSuffix,
             xlabel = "Discriminant (MC truth)", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0)
    drawPlot(createPlot("FullHiggsMass/Discriminant_GEN_NeutrinosReplacedWithMET", normalizeToOne=massPlotNormToOne),
             "Discriminant_GEN_NuToMET"+nameSuffix,
             xlabel = "Discriminant (MC truth, #nu_{#tau} #leftrightarrow  #slash{E}_{T})",
             ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0)
    # PLOT: Discriminant (RECO_pure, RECO_with_misidentification)
    drawPlot(createPlot("FullHiggsMass/DiscriminantPure", normalizeToOne=massPlotNormToOne), "Discriminant_pure"+nameSuffix,
             xlabel = "Discriminant", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0)
    drawPlot(createPlot("FullHiggsMass/DiscriminantImpure", normalizeToOne=massPlotNormToOne), "Discriminant_misID"+nameSuffix,
             xlabel = "Discriminant", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0)

    # PLOT: Counters
    def renameLabels(p):
        axis = p.getFrame().GetXaxis()
        axis.LabelsOption("d")
        axis.CenterLabels(True)
        for i in range(1, 7):
            axis.SetBinLabel(i, counterLabels[str(axis.GetBinLabel(i))])
#            axis.SetBinLabel(i, counterLabels[i])
    drawPlot(createPlot("counters/weighted/FullHiggsMassCalculator", normalizeToOne=massPlotNormToOne), "Counters"+nameSuffix,
             xlabel = "", ylabel = "Event count", log=False, opts={"xmin": 4, "xmax": 10},
             customizeBeforeDraw=renameLabels)


def doCounters(datasets):
    # Create EventCounter object, holds all counters of all datasets
    eventCounter = counter.EventCounter(datasets)

    # Normalize counters
    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcOnlyLumi)
    else:
        eventCounter.normalizeMCByLuminosity()

    # Create LaTeX format, automatically adjust value precision by uncertainty
    latexFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.4f", withPrecision=2))

    table = eventCounter.getSubCounterTable("FullHiggsMassCalculator")
    table.renameRows(counterLabels)
    print table.format(latexFormat)


# Helper function to add mHplus and BR text  
def addMassBRText(plot, x, y, lightHplusMassPoint):
    size = 20
    separation = 0.04

    if not plotAllMassPointsTogether:
        massText = "m_{H^{+}} = %d GeV/c^{2}" % lightHplusMassPoint
        plot.appendPlotObject(histograms.PlotText(x, y, massText, size=size))

    brText = "#it{B}(t #rightarrow bH^{+})=%.2f" % lightHplusTopBR
    plot.appendPlotObject(histograms.PlotText(x, y-separation, brText, size=size))

    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()





# For inspiration:


#     # PLOT: b tagging
#     drawPlot(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBJets", xlabel="Number of selected b jets", ylabel="Events", opts={"xmax": 6}, cutLine=1)

#     # PLOT: MET
#     # opts2 is for the ratio pad
#     drawPlot(createPlot("Met"), "Met", xlabel="Type-I corrected PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", rebinToWidthX=20, opts={"ymaxfactor": 10}, opts2={"ymin": 0, "ymax": 2}, cutLine=60)

#     # PLOT: vertices
#     # Normalizing to unit area
#     drawPlot(createPlot("Vertices/verticesTriggeredAfterWeight", normalizeToOne=True, massbr_x=0.65, massbr_y=0.5, normone_x=0.62, normone_y=0.4),
#              "verticesAfterWeightTriggered", xlabel="Number of reconstructed vertices", ylabel="Events", log=False, opts={"xmax": 20}, addLuminosityText=False)
