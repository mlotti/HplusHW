#!/usr/bin/env python

##################################################################################################
# Title          : classificationPlots.py
# Author(s)      : Stefan Richter (based heavily on template test/plotScripts/plotHistoTemplate.py
#                  by Ritva Kinnunen, Matti Kortelainen, Alexandros Attikis)
# Description    : 
##################################################################################################

interactiveMode = False

import sys
from ROOT import *
ROOT.gROOT.SetBatch(not interactiveMode)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configurations
#multicrabDirs = ["multicrab_130722_135352"]
#scenarios = [""]

multicrabDirs = ["multicrab_130725_113751"] # has the top invariant mass in generator histogram!
scenarios = [""]

#multicrabDirs = ["multicrab_130724_113525"]
#scenarios = [
    #"", # default
    #"OptInvMassRecoPzSelectionDeltaEtaMaxTopInvMassCutNone",
    #"OptInvMassRecoPzSelectionDeltaEtaMaxTopInvMassCutLoose",
#    "OptInvMassRecoPzSelectionDeltaEtaMaxTopInvMassCutMedium",
    #"OptInvMassRecoPzSelectionDeltaEtaMaxTopInvMassCutTight",
#    ]


#multicrabDirs = ["multicrab_130529_154518"]

#multicrabDirs = ["multicrab_130522_194442"] # used for most of the plots and info in my MSc thesis
#scenarios = [
#    "", # default
#    "OptInvMassRecoTopInvMassCutNone",
#    "OptInvMassRecoTopInvMassCutLoose",
#    "OptInvMassRecoTopInvMassCutMedium",
#    "OptInvMassRecoTopInvMassCutTight",
#    ]

analysis = "signalAnalysis"
# Data era affects on the set of selected data datasets, and the PU weights (via TDirectory name in histograms.root)
#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

plotSignalOnly = True
#plotSignalOnly = False
#plotAllMassPointsTogether = True
plotAllMassPointsTogether = False
mcOnly = True
#mcOnly = False
mcOnlyLumi = 5000 # 1/pb
#lightHplusMassPoint = 120
lightHplusMassPoints = [80, 90, 100, 120, 140, 150, 155, 160]
#lightHplusMassPoints = [80, 90, 120, 140, 150, 160] # (many plots in Stefan's MSc thesis are shown for these mass points) # TODO change 90 to 100 once there's a working directory
lightHplusTopBR = 0.02
removeQCD = True
#removeQCD = False
massPlotBinWidth = 20 # GeV
discriminantPlotBinWidth = 2000 # GeV^2
#massPlotNormToOne = True
massPlotNormToOne = False

solutionSelectionLabels = {
    "Greater solution closest": "max-|p_{#nu, z}|",
    "Smaller solution closest": "min-|p_{#nu, z}|",
    "TauNuAngleMax solution closest": "max-#xi_{#tau, #nu}",
    "TauNuAngleMin solution closest": "min-#xi_{#tau, #nu}",
    "TauNuDeltaEtaMax solution closest": "max-#Delta#eta_{#tau, #nu}",
    "TauNuDeltaEtaMin solution closest": "min-#Delta#eta_{#tau, #nu}",
    }

eventClassificationLabels = {
    "all passed events": "passed",
    "pure": "pure",
    "#tau genuine": "#tau genuine",
    "b genuine": "b genuine",
    "#tau measurement good": "#tau meas. good",
    "b measurement good": "b meas. good",
    "#tau and b from same top": "#tau and b from same top",
    "MET #approx p_{#nu,T}": "MET #approx p_{#nu,T}"
    }

# Change legend creator defaults
histograms.createLegend.moveDefaults(dx=-0.05)

# main function
def main():
    for multicrabDir in multicrabDirs:
        for scenario in scenarios:
            for lightHplusMassPoint in lightHplusMassPoints:
                doEverything("../"+multicrabDir, scenario, lightHplusMassPoint)

def doEverything(multicrabDir, scenario, lightHplusMassPoint):
    print "MultiCRAB directory is", multicrabDir
    module = analysis+dataEra+scenario
    print "Module is", module
    print "Mass point is", lightHplusMassPoint
    #return

    # Customizations for specific MultiCRAB directories
    if multicrabDir == "../multicrab_130522_194442" and lightHplusMassPoint == 100: #TODO DELETE WHEN CRAB HAS RUN AGAIN!
        return # the M100 sample was accidentally not processed in this MultiCRAB directory
    
    # Read the datasets, see twiki page for more examples
    # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicSoftware#Construct_datasets
    # Usually you can also omit the analysisName, as it can be detected automatically
    # If you have optimization enabled, you have to specify optimizationMode explicitly (optimizationMode="Opt...") 
    if plotSignalOnly:
        datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabDir, analysisName=analysis, dataEra=dataEra,
                                                       optimizationMode=scenario, includeOnlyTasks="TTToHplus")
    else:
        datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabDir, analysisName=analysis, dataEra=dataEra,
                                                       optimizationMode=scenario)
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
    ### TO PLOT SEVERAL MASS POINTS TOGETHER, ACTIVATE THIS:
#     if not plotAllMassPointsTogether:
#         datasets.remove(filter(lambda name: "TTToHplus" in name and not ("M%d"%lightHplusMassPoint in name or "M80" in name),
#                                datasets.getAllDatasetNames()))
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

    # FOR PLOTTING MULTIPLE MASS POINTS IN THE SAME GRAPH
    #plots._plotStyles["TTToHplus_M80"].append(styles.StyleLine(lineColor=ROOT.kBlue))
    #plots._legendLabels["TTToHplus_M80"] += "M=80"
    
    # You can print a tree of all the merged datasets with this
    #datasets.printDatasetTree()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets, scenario, lightHplusMassPoint)

    # Print a counter table for use in LaTeX documents
    doCounters(datasets)

    # Do plots with a fit
    if plotSignalOnly and (scenario == "OptInvMassRecoTopInvMassCutMedium" or scenario == "OptInvMassRecoPzSelectionDeltaEtaMaxTopInvMassCutMedium"):
        doFit(datasets, "HiggsMass", scenario, lightHplusMassPoint, "Gauss")
        doFit(datasets, "HiggsMass", scenario, lightHplusMassPoint, "BW")
        #doFit(datasets, "HiggsMass_smaller", scenario, lightHplusMassPoint, "Gauss")
        #doFit(datasets, "HiggsMass_smaller", scenario, lightHplusMassPoint, "BW")

    if interactiveMode:
        raw_input("*** Press \"Enter\" to exit pyROOT: ")



# Default plot drawing options, all of these can be overridden in the
# individual drawPlot() calls
drawPlot = plots.PlotDrawer(log=True, addLuminosityText=True, stackMCHistograms=True, addMCUncertainty=True)
if plotSignalOnly:
    drawPlot = plots.PlotDrawer(log=True, addLuminosityText=True, stackMCHistograms=False, addMCUncertainty=False)
    

# Define plots to draw
def doPlots(datasets, scenario, lightHplusMassPoint):
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
        #p.histoMgr.setHistoDrawStyleAll("SCAT")
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
    scenarioSuffix = ""
    if not scenario == "":
        scenarioSuffix = "_"+scenario
    nameSuffix = ""
    if plotSignalOnly:
        nameSuffix = nameSuffix + "_signalOnly"
    if not plotAllMassPointsTogether:
        nameSuffix = "_M%d"%lightHplusMassPoint
#     if removeQCD:
#         nameSuffix = nameSuffix + "_noQCD"
#     if massPlotNormToOne:
#         nameSuffix = nameSuffix + "_normToOne"

    # Plot: top invariant masses
    drawPlot(createPlot("FullHiggsMass/TopInvariantMassInGenerator", normalizeToOne=massPlotNormToOne), "TopInvariantMassInGenerator"+nameSuffix,
             xlabel="m_{t}", ylabel="Events / 5 GeV", log=False, opts={"xmin": 100, "xmax": 300})
    drawPlot(createPlot("FullHiggsMass/TopMassSolution", normalizeToOne=massPlotNormToOne), "TopMass"+nameSuffix,
             xlabel="m_{t}", ylabel="Events / %d GeV"%massPlotBinWidth, log=True, rebinToWidthX=massPlotBinWidth)
        
    #drawPlot(createPlot("FullHiggsMass/TopInvariantMassInGenerator", normalizeToOne=massPlotNormToOne),
    #         "TopInvariantMassInGenerator"+nameSuffix, xlabel="m_{t}", ylabel="Events / %d GeV"%massPlotBinWidth,
    #         log=False, rebinToWidthX=massPlotBinWidth)

    # PLOT: Higgs invariant mass using the chosen selection method (RECO, GEN, GEN_NuToMET)
    drawPlot(createPlot("FullHiggsMass/HiggsMass", normalizeToOne=massPlotNormToOne), "HiggsMass"+scenario+nameSuffix,
             xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
             cutLine=lightHplusMassPoint)
    if scenario == "":
        drawPlot(createPlot("FullHiggsMass/HiggsMass_greater", normalizeToOne=massPlotNormToOne), "HiggsMass_GREATER"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)
        drawPlot(createPlot("FullHiggsMass/HiggsMass_smaller", normalizeToOne=massPlotNormToOne), "HiggsMass_SMALLER"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)
        drawPlot(createPlot("FullHiggsMass/HiggsMass_tauNuAngleMax", normalizeToOne=massPlotNormToOne), "HiggsMass_ANGLEMAX"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)
        drawPlot(createPlot("FullHiggsMass/HiggsMass_tauNuAngleMin", normalizeToOne=massPlotNormToOne), "HiggsMass_ANGLEMIN"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)
        drawPlot(createPlot("FullHiggsMass/HiggsMass_tauNuDeltaEtaMax", normalizeToOne=massPlotNormToOne), "HiggsMass_DELTAETAMAX"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)
        drawPlot(createPlot("FullHiggsMass/HiggsMass_tauNuDeltaEtaMin", normalizeToOne=massPlotNormToOne), "HiggsMass_DELTAETAMIN"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)
#     if plotSignalOnly:
#         drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN", normalizeToOne=massPlotNormToOne),
#                  "HiggsMass_GEN"+nameSuffix+"_TauNuAngleMax",
#                  xlabel="m(#tau, #nu_{#tau}) (MC truth)",
#                  ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
#         drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN_NeutrinosReplacedWithMET", normalizeToOne=massPlotNormToOne),
#                  "HiggsMass_GEN_NuToMET"+nameSuffix+"_TauNuAngleMax",
#                  xlabel="m(#tau, #nu_{#tau}) (MC truth, #nu_{#tau} #leftrightarrow  #slash{E}_{T})",
#                  ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
    # PLOT: Higgs invariant mass using the better and the worse solution, respectively
    if scenario == "":
        drawPlot(createPlot("FullHiggsMass/HiggsMass_betterSolution", normalizeToOne=massPlotNormToOne),
                 "HiggsMass_betterSolution"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)
        drawPlot(createPlot("FullHiggsMass/HiggsMass_worseSolution", normalizeToOne=massPlotNormToOne),
                 "HiggsMass_worseSolution"+scenarioSuffix+nameSuffix,
                 xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
                 cutLine=lightHplusMassPoint)



#     # PLOT: Higgs invariant mass using the chosen selection method, positive discriminant only
#     drawPlot(createPlot("FullHiggsMass/HiggsMassPositiveDiscriminant", normalizeToOne=massPlotNormToOne),
#              "HiggsMassPosDisc"+nameSuffix,
#              xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
#              cutLine=lightHplusMassPoint)

#     # PLOT: Higgs invariant mass using the chosen selection method, negative discriminant only
#     drawPlot(createPlot("FullHiggsMass/HiggsMassNegativeDiscriminant", normalizeToOne=massPlotNormToOne),
#              "HiggsMassNegDisc"+scenarioSuffix+nameSuffix,
#              xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth,
#              cutLine=lightHplusMassPoint)


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
#                  xlabel="m(#tau, #nu_{#tau}) ["+selectionMethod+"]", ylabel="Events / %d GeV"%massPlotBinWidth, log=False,
#                  rebinToWidthX=massPlotBinWidth)
#         if plotSignalOnly:
#             drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN_"+selectionMethod, normalizeToOne=massPlotNormToOne),
#                      "HiggsMass_GEN_"+selectionMethod+nameSuffix,
#                      xlabel="m(#tau, #nu_{#tau}) (MC truth) ["+selectionMethod+"]",
#                      ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
#             drawPlot(createPlot("FullHiggsMass/HiggsMass_GEN_NuToMET_"+selectionMethod, normalizeToOne=massPlotNormToOne),
#                      "HiggsMass_GEN_NuToMET_"+selectionMethod+nameSuffix,
#                      xlabel="m(#tau, #nu_{#tau}) (MC truth, #nu_{#tau} #leftrightarrow  #slash{E}_{T}) ["+selectionMethod+"]",
#                      ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
    

#     # PLOT: HiggsMassPure
#     drawPlot(createPlot("FullHiggsMass/HiggsMassPure", normalizeToOne=massPlotNormToOne), "HiggsMassPure"+nameSuffix, xlabel="m(#tau, #nu_{#tau}) of pure events", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
#     # PLOT: HiggsMassImpure
#     drawPlot(createPlot("FullHiggsMass/HiggsMassImpure", normalizeToOne=massPlotNormToOne), "HiggsMassImpure"+nameSuffix, xlabel="m(#tau, #nu_{#tau}) of events with mis-ID", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)

    # PLOT: Transverse mass
    if scenario == "":
        drawPlot(createPlot("CommonPlots/AtEveryStep/Selected/transverseMass", normalizeToOne=massPlotNormToOne),
                 "TransverseMass"+nameSuffix,
                 xlabel="m_{T}(#tau, #nu_{#tau})", ylabel="Events / %d GeV"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)

    # Set colour scheme for 2D plots
    tdrstyle.setDeepSeaPalette()

    # PLOT: Transverse mass versus invariant mass
    if plotSignalOnly:
        drawPlot(createTH2Plot("FullHiggsMass/TransMassVsInvMass", "TTToHplus_M%d"%lightHplusMassPoint),
                 "TransMassVsInvMass"+scenarioSuffix+nameSuffix,
                 xlabel="(M_{H^{+}}=%d GeV sig. only)          m_{T}(#tau, #nu_{#tau})"%lightHplusMassPoint, ylabel="m(#tau, #nu_{#tau})",
                 zlabel="Events", log=False, createLegend=None,
                 opts={"xmax": 200, "ymax": 200}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)
    else:
        drawPlot(createTH2Plot("FullHiggsMass/TransMassVsInvMass", "TTToHplus_M%d"%lightHplusMassPoint),
                 "TransMassVsInvMass"+scenarioSuffix+nameSuffix,
                 xlabel="(M_{H^{+}}=%d GeV sig. + bkg)          m_{T}(#tau, #nu_{#tau})"%lightHplusMassPoint, ylabel="m(#tau, #nu_{#tau})",
                 zlabel="Events", log=False, createLegend=None,
                 opts={"xmax": 200, "ymax": 200}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)
        drawPlot(createTH2Plot("FullHiggsMass/TransMassVsInvMass", "TTJets"),
                 "TransMassVsInvMass_ttbarOnly"+scenarioSuffix,
                 xlabel="(t#bar{t} only)          m_{T}(#tau, #nu_{#tau})", ylabel="m(#tau, #nu_{#tau})", zlabel="Events",
                 log=False, createLegend=None,
                 opts={"xmax": 200, "ymax": 200}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)
    # PLOT: Top mass versus invariant mass
#     drawPlot(createTH2Plot("FullHiggsMass/TopMassVsInvMass", "TTToHplus_M%d"%lightHplusMassPoint),
#              "TopMassVsInvMass"+scenarioSuffix+nameSuffix,
#              xlabel="(M_{H^{+}} = %d GeV)          m_{top}"%lightHplusMassPoint, ylabel="m(#tau, #nu_{#tau})",
#              zlabel="Events", log=False, createLegend=None,
#              opts={"xmax": 500, "ymax": 200}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)
#     if not plotSignalOnly:
#         drawPlot(createTH2Plot("FullHiggsMass/TopMassVsInvMass", "TTJets"),
#                  "TopMassVsInvMass_ttbarOnly"+scenarioSuffix,
#                  xlabel="(t#bar{t} only)          m_{top}", ylabel="m(#tau, #nu_{#tau})",
#                  zlabel="Events", log=False, createLegend=None,
#                  opts={"xmax": 500, "ymax": 200}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)
    # PLOT: Top mass versus neutrino number
#     drawPlot(createTH2Plot("FullHiggsMass/TopMassVsNeutrinoNumber", "TTToHplus_M%d"%lightHplusMassPoint),
#              "TopMassVsNeutrinoNumber"+scenarioSuffix+nameSuffix,
#              xlabel="(M_{H^{+}} = %d GeV)          m_{top}"%lightHplusMassPoint, ylabel="Number of neutrinos",
#              zlabel="Events", log=False, createLegend=None,
#              opts={"xmax": 500, "ymax": 8}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=1.0)
#     if not plotSignalOnly:
#         drawPlot(createTH2Plot("FullHiggsMass/TopMassVsInvMass", "TTJets"),
#                  "TopMassVsInvMass_ttbarOnly"+scenarioSuffix,
#                  xlabel="(t#bar{t} only)          m_{top}", ylabel="Number of neutrinos",
#                  zlabel="Events", log=False, createLegend=None,
#                  opts={"xmax": 500, "ymax": 8}, rebinToWidthX=massPlotBinWidth, rebinToWidthY=massPlotBinWidth)
    
        

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
    def formatDiscriminantPlotLabels(p):
        axis = p.getFrame().GetXaxis()
        #axis.LabelsOption("d")
        axis.SetLabelSize(14)

    drawPlot(createPlot("FullHiggsMass/Discriminant", normalizeToOne=massPlotNormToOne), "Discriminant"+nameSuffix,
             xlabel = "Discriminant", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0, customizeBeforeDraw=formatDiscriminantPlotLabels)
    drawPlot(createPlot("FullHiggsMass/Discriminant_GEN", normalizeToOne=massPlotNormToOne), "Discriminant_GEN"+nameSuffix,
             xlabel = "Discriminant (MC truth)", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0, customizeBeforeDraw=formatDiscriminantPlotLabels)
    drawPlot(createPlot("FullHiggsMass/Discriminant_GEN_NeutrinosReplacedWithMET", normalizeToOne=massPlotNormToOne),
             "Discriminant_GEN_NuToMET"+nameSuffix,
             xlabel = "Discriminant (MC truth, #vec{p}^{#nu}_{T} #rightarrow #vec{E}^{miss}_{T})",
             ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
             rebinToWidthX=discriminantPlotBinWidth, cutLine=0, customizeBeforeDraw=formatDiscriminantPlotLabels)
    # PLOT: Discriminant (RECO_pure, RECO_with_misidentification)
#     drawPlot(createPlot("FullHiggsMass/DiscriminantPure", normalizeToOne=massPlotNormToOne), "Discriminant_pure"+nameSuffix,
#              xlabel = "Discriminant", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
#              rebinToWidthX=discriminantPlotBinWidth, cutLine=0)
#     drawPlot(createPlot("FullHiggsMass/DiscriminantImpure", normalizeToOne=massPlotNormToOne), "Discriminant_misID"+nameSuffix,
#              xlabel = "Discriminant", ylabel = "Events / %d GeV^{2}"%discriminantPlotBinWidth, log=False,
#              rebinToWidthX=discriminantPlotBinWidth, cutLine=0)

    # PLOT: Counters
    def renameLabels(p):
        axis = p.getFrame().GetXaxis()
        axis.LabelsOption("d")
        axis.CenterLabels(True)
        for i in range(1, 7):
            axis.SetBinLabel(i, counterLabels[str(axis.GetBinLabel(i))])
#            axis.SetBinLabel(i, counterLabels[i])
    #drawPlot(createPlot("counters/weighted/FullHiggsMassCalculator", normalizeToOne=massPlotNormToOne),
    drawPlot(createPlot("counters/weighted/FullHiggsMassCalculator", normalizeToOne=massPlotNormToOne),
             "Counters"+scenarioSuffix+nameSuffix,
             xlabel = "", ylabel = "Event count", log=False, opts={"xmin": 0, "xmax": 4})
             #customizeBeforeDraw=renameLabels)
             
    def renameLabelsSolutionSelection(p):
        axis = p.getFrame().GetXaxis()
        axis.LabelsOption("d")
        axis.CenterLabels(True)
        for i in range(1, 7):
            axis.SetBinLabel(i, solutionSelectionLabels[str(axis.GetBinLabel(i))])
    drawPlot(createPlot("counters/weighted/SolutionSelection", normalizeToOne=massPlotNormToOne),
             "SolutionSelectionCounters"+scenarioSuffix+nameSuffix,
             xlabel = "", ylabel = "Event count", log=False, customizeBeforeDraw=renameLabelsSolutionSelection)

    def renameLabelsEventClassification(p):
        axis = p.getFrame().GetXaxis()
        axis.LabelsOption("u")
        axis.CenterLabels(True)
        for i in range(1, 9):
            axis.SetBinLabel(i, eventClassificationLabels[str(axis.GetBinLabel(i))])
    drawPlot(createPlot("counters/weighted/FullMassEventClassification", normalizeToOne=massPlotNormToOne),
             "EventClassificationCounters"+scenarioSuffix+nameSuffix,
             xlabel = "", ylabel = "Event count", log=False, customizeBeforeDraw=renameLabelsEventClassification)


# Helper function to add mHplus and BR text  
def addMassBRText(plot, x, y, lightHplusMassPoint):
    size = 20
    separation = 0.04

    if not plotAllMassPointsTogether:
        massText = "m_{H^{#pm}} = %d GeV/c^{2}" % lightHplusMassPoint
        plot.appendPlotObject(histograms.PlotText(x, y, massText, size=size))

    brText = "#it{B}(t#rightarrowbH^{+}) = %.2f" % lightHplusTopBR
    plot.appendPlotObject(histograms.PlotText(x, y-separation, brText, size=size))

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
    plainFormat = counter.TableFormatText(counter.CellFormatText(valueOnly=True))

    #table = eventCounter.getMainCounterTable()
    #print table.format()
    
    table  = eventCounter.getSubCounterTable("FullHiggsMassCalculator")
    #table.renameRows(counterLabels)
    print table.format(latexFormat)
    
#     table2 = eventCounter.getSubCounterTable("SolutionSelection")
#     table2.renameRows(solutionSelectionLabels)
#     table2.transpose()
#     print table2.format(plainFormat)
    
    #table3 = eventCounter.getSubCounterTable("FullMassEventClassification")
    #table3.renameRows(eventClassificationLabels)
    #table3.transpose()
    #print table3.format(latexFormat)

def Gaussian(x,par):
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1)

def BW(x,par):
    return par[0]*TMath.BreitWigner(x[0],par[1],par[2])

def doFit(datasets, histoName, scenarioSuffix, lightHplusMassPoint, fitFunction):
    print "Doing invariant mass fits. (Fit function =", fitFunction + ")"
    
    invmass = plots.PlotBase(
        [datasets.getDataset("TTToHplus_M%d"%lightHplusMassPoint).getDatasetRootHisto("FullHiggsMass/"+histoName)])
    invmass.histoMgr.normalizeMCToLuminosity(mcOnlyLumi) # Could implement possibility to normalize to data lumi (as for plots)
    invmass._setLegendStyles()
    invmass._setLegendLabels()
    invmass.histoMgr.setHistoDrawStyleAll("P")
    #invmass.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1)) # SET REBINNING HERE!
    hinvmass = invmass.histoMgr.getHisto("TTToHplus_M%d"%lightHplusMassPoint).getRootHisto().Clone("FullHiggsMass/"+histoName)
    
    canvas = TCanvas("canvas","",500,500)
    hinvmass.GetYaxis().SetTitle("Events")
    hinvmass.GetXaxis().SetTitle("m(#tau, #nu_{#tau}) (GeV)")
    #    hinvmass.GetYaxis().SetTitleSize(10.0)
    #    hinvmass.GetXaxis().SetTitleSize(20.0)
    hinvmass.Draw()
    histo = hinvmass.Clone("histo")
    #    rangeMin = hinvmass.GetXaxis().GetXmin()
    #    rangeMax = hinvmass.GetXaxis().GetXmax()
    rangeMin = 80
    rangeMax = 160
    if lightHplusMassPoint == 80:
        rangeMin = 80
        rangeMax = 160
    if lightHplusMassPoint == 90:
        rangeMin = 70
        rangeMax = 160
    if lightHplusMassPoint == 100:
        rangeMin = 90
        rangeMax = 165
    if lightHplusMassPoint == 120:
        rangeMin = 80
        rangeMax = 165
    if lightHplusMassPoint == 140:
        rangeMin = 110
        rangeMax = 165
    if lightHplusMassPoint == 150:
        rangeMin = 130
        rangeMax = 170
    if lightHplusMassPoint == 155:
        rangeMin = 140
        rangeMax = 170
    if lightHplusMassPoint == 160:
        rangeMin = 140
        rangeMax = 175
 
    if scenarioSuffix == "_noTopMassCut":
        rangeMax = 190
    #rangeMax = lightHplusMassPoint + 50
    
    numberOfParameters = 3
    
    #    print "Fit range ",rangeMin, " - ",rangeMax
    
    if fitFunction == "Gauss":
        class FitFunction:
            def __call__( self, x, par ):
                return Gaussian(x, par)
    elif fitFunction == "BW":
        class FitFunction:
            def __call__( self, x, par ):
                return BW(x, par)
    else:
        print "ERROR: invalid fit function option given ("+fitFunction+"). Valid options are \"Gauss\", \"BW\"."
        sys.exit(1)
        
    theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,numberOfParameters)
    theFit.SetParName(0,"norm.");
    theFit.SetParName(1,"mean");
    theFit.SetParName(2,"width");
    theFit.SetParLimits(0,1,10000)
    theFit.SetParLimits(1,0,500)
    theFit.SetParLimits(2,0.1,200)
    #    gStyle.SetOptFit(0)
    
    hinvmass.Fit(theFit,"WLR")
    theFit.SetRange(rangeMin,rangeMax)
    theFit.SetLineStyle(1)
    theFit.SetLineWidth(2)
    theFit.Draw("same")
    tex4 = TLatex(0.2,0.96,"CMS Simulation")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    if fitFunction == "Gauss":
        tex2 = TLatex(0.5,0.7,"Gaussian fit")
    if fitFunction == "BW":
        tex2 = TLatex(0.5,0.7,"Breit-Wigner fit")
    tex2.SetNDC()
    tex2.SetTextSize(18)
    tex2.Draw()
    tex3 = TLatex(0.5,0.65,"m_{H^{#pm}} = %d GeV"%lightHplusMassPoint)
    tex3.SetNDC()
    tex3.SetTextSize(18)
    tex3.Draw()
    tex5 = TLatex(0.5,0.6,"#color[2]{Background not shown}")
    tex5.SetNDC()
    tex5.SetTextSize(18)
    tex5.Draw()
    #tex5 = ROOT.TLatex(0.6,0.5,"Matched jets")
    #tex5.SetNDC()
    #tex5.SetTextSize(20)
    #tex5.Draw()
    print "Fit range ",rangeMin, " - ",rangeMax
    canvas.Print("Fit_"+fitFunction+"_"+histoName+scenarioSuffix+"_M%d.png"%lightHplusMassPoint)
    canvas.Print("Fit_"+fitFunction+"_"+histoName+scenarioSuffix+"_M%d.eps"%lightHplusMassPoint)

    print "******************************", fitFunction ,"***********************************"
    if fitFunction == "Gauss":
        print  "$", round(theFit.GetParameter(1), 0), "\\pm", round(theFit.GetParError(1), 0), "$ & $", round(theFit.GetChisquare(), 0), "/", theFit.GetNDF(), "$ &"
    elif fitFunction == "BW":
        print  "$", round(theFit.GetParameter(1), 0), "\\pm", round(theFit.GetParError(1), 0), "$ & $", round(theFit.GetChisquare(), 0), "/", theFit.GetNDF(), "$ \\\\"

        
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
