#!/usr/bin/env python

##################################################################################################
# Title          : fullMassMCPlot.py
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

multicrabDir = "../multicrab_130226_161611" # Higgs mass calculated using the old algorithm ("OldSchool")
#multicrabDir = "../multicrab_130226_170317" # Higgs mass calculated using the new algorithm ("Stefan's")
#multicrabDir = "../multicrab_130220_105309"
#multicrabDir = "../multicrab_130219_143046"
#multicrabDir = "../multicrab_130213_201254"
analysis = "signalAnalysis"
# Data era affects on the set of selected data datasets, and the PU
# weights (via TDirectory name in histograms.root)
dataEra = "Run2011A" #dataEra = "Run2011B" #dataEra = "Run2011AB"

#mcOnly = False
mcOnly = True
mcOnlyLumi = 5000 # 1/pb

lightHplusMassPoint = 120
lightHplusTopBR = 0.02

#removeQCD = False
removeQCD = True

massPlotBinWidth = 25 # GeV

massPlotNormToOne = False
#massPlotNormToOne = True


# main function
def main():
    # Read the datasets, see twiki page for more examples
    # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicSoftware#Construct_datasets
    # Usually you can also omit the analysisName, as it can be detected automatically
    # If you have optimization enabled, you have to specify optimizationMode explicitly (optimizationMode="Opt...")
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

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M%d"%lightHplusMassPoint in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    # Remove QCD datasets (because the simulated QCD background is negligible but has huge artefacts)
    if removeQCD:
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))

    # Change legend creator defaults
    histograms.createLegend.moveDefaults(dx=-0.05)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=lightHplusTopBR, br_Htaunu=1)
    # Example how to set cross section to a specific MSSM point
    #xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    myXSect = datasets.getDataset("TTToHplusBWB_M120").getCrossSection()
    myNormFactor = datasets.getDataset("TTToHplusBWB_M120").getNormFactor()
    myNAll = datasets.getDataset("TTToHplusBWB_M120").getNAllEvents()
    print "### HW cross section =", myXSect

    # Merge signals into one dataset (per mass point)
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Replace signal dataset with a signal+background dataset, where
    # the BR(t->H+) is taken into account for SM ttbar
    plots.replaceLightHplusWithSignalPlusBackground(datasets)
    
    # You can print a tree of all the merged datasets with this
    #datasets.printDatasetTree()

    # Apply TDR style
    style = tdrstyle.TDRStyle()



    # Calculate N_signal/N_background and Poisson significance of signal
    #numberOfSignalEvents = datasets.getDataset("TTToHplus_M120").getCrossSection() * myIntegratedLuminosity
    numberOfSignalEvents = myXSect * myIntegratedLuminosity
    print "###", datasets.getDataset("TTToHplus_M120").getCrossSection()
    print "###", myIntegratedLuminosity
    print "*** Number of signal events:", numberOfSignalEvents
    print "*** ...or:", myNormFactor * myNAll * myIntegratedLuminosity
    
    # names = datasetMgr.getAllDatasetNames()
    #d_ttjets = datasets.getDataset("TTJets")
    #print d_ttjets.getNAllEvents()




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
            p.appendPlotObject(histograms.PlotText(2*normone_x, normone_y+0.03, "Normalized to unit area", size=17))
        if removeQCD:
            p.appendPlotObject(histograms.PlotText(2*normone_x, normone_y, "QCD background not shown", size=17, color=2))
        return p

    # drawPlot defaults can be modified also here
    if not mcOnly:
        drawPlot.setDefaults(ratio=True)


    # PLOT: full mass of (tau, nu) system
    if removeQCD:
        massPlotName = "FullTauNuMass_M%d_noQCD"%lightHplusMassPoint
    else:
        massPlotName = "FullTauNuMass_M%d"%lightHplusMassPoint
    if massPlotNormToOne:
        massPlotName = massPlotName + "_normToOne"
        
    drawPlot(createPlot("FullHiggsMass/HiggsMass", normalizeToOne=massPlotNormToOne), massPlotName, xlabel="m(#tau, #nu_{#tau})", ylabel="Events / %d Gev"%massPlotBinWidth, log=False, rebinToWidthX=massPlotBinWidth)
                

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


#     # PLOT: b tagging
#     drawPlot(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBJets", xlabel="Number of selected b jets", ylabel="Events", opts={"xmax": 6}, cutLine=1)

#     # PLOT: MET
#     # opts2 is for the ratio pad
#     drawPlot(createPlot("Met"), "Met", xlabel="Type-I corrected PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", rebinToWidthX=20, opts={"ymaxfactor": 10}, opts2={"ymin": 0, "ymax": 2}, cutLine=60)

#     # PLOT: vertices
#     # Normalizing to unit area
#     drawPlot(createPlot("Vertices/verticesTriggeredAfterWeight", normalizeToOne=True, massbr_x=0.65, massbr_y=0.5, normone_x=0.62, normone_y=0.4),
#              "verticesAfterWeightTriggered", xlabel="Number of reconstructed vertices", ylabel="Events", log=False, opts={"xmax": 20}, addLuminosityText=False)
