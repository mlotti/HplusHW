#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
### System modules
import sys
import array
import math
import ROOT
from ROOT import gStyle
### HPlus modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
### Script-specific modules
from TreeHelper import *
from TreeCutHelper import * 
from TreeVarHelper import * 

######################################################################
### Define options and declarations
######################################################################

### Create boolean dictionary
boolDict = {
"bBatchMode"        : True,
"bRatio"            : False,
"bPrintPSet"        : False,
"bLogY"             : True,
"bNormalizeToOne"   : False,
"bAddMCUncertainty" : True,   #Requires: bStackHistos == True
"bAddLumiText"      : True,
"bCustomRange"      : False,
# 
"bBinSignificance"  : False,  #Requires: bStackHistos == False
"bSignificance"     : False,  #Requires: bStackHistos == False
"bEfficiency"       : False,  #Requires: bStackHistos == False
"bQcdPurity"        : True,   #Requires: bStackHistos == False
# 
"bDataMinusEwk"     : False,  #Requires: bRemoveQcd==False
"bStackHistos"      : False, 
"bMergeEwk"         : False,
#
"bRemoveData"       : False,
"bRemoveSignal"     : False,  #Requires : RemoveData==True
"bRemoveEwk"        : False,
"bRemoveQcd"        : False,
}
    
### Other Global Definitions
getBool        = lambda Key: boolDict[Key]
BR_tH          = 0.01
BR_Htaunu      = 1.0
signalMass     = "160"
yMin           = 0.0
yMax           = 200.0
yMinLog        = 1E-01
yMaxLog        = 1E+03
yMinRatio      = 0.0
yMaxRatio      = 2.0
yMaxFactor     = 2
yMaxFactorTH2  = yMaxFactor*0.7
yMaxFactorLog  = 100
xLegMin        = 0.65
xLegMax        = 0.93
yLegMin        = 0.65
yLegMax        = 0.93
yMinPurity     = 0.9 #0.9 #0.5
yMaxPurity     = 1.005 #1.005
MyLumi         = 2.3*1000 #(pb)
pSetToPrint    = "TTToHplusBHminusB_M120_Fall11"
myDataEra      = "Run2011AB" #"Run2011A" "Run2011B" "Run2011AB"
multicrabPath  = "/Users/attikis/my_work/cms/lxplus/TreeAnalysis_JetThrustAndNonIsoLeptons_v44_5_130312_171728/"
ROOT.gROOT.SetBatch( getBool("bBatchMode") )

######################################################################
### Function declarations
######################################################################
def main():
    '''
    def main():
    The main function where auxuliary methods are called. Specifically,
    The datasets are retrieved for a specified data Era. These are then 
    passed to the plotting module where all manipulations are performed.
    The "HistoList" is imported from HistoHelper.py. The 
    "SaveExtension" refers to a string attached to the end of the default
    file name, not to the type of file saved. By default the histograms 
    are saved in the following formats: .eps, *.png *.C
    '''

    ### Get the desired datasets 
    datasets = getDatasets(multicrabPath, myDataEra)

    ### Plot all histograms defined in the HistoList found in the file HistoHelper.py
    ### Standard Cuts
    #doPlots(datasets, HistoList, JetSelectionSanityCuts, SaveExtension="JetSelSanity")
    #doPlots(datasets, HistoList, JetSelectionCuts, SaveExtension="JetSel")
    #doPlots(datasets, HistoList, JetSelectionMtCuts, SaveExtension="JetSelMt")
    #doPlots(datasets, HistoList, MetBtagCuts, SaveExtension="JetSelMetBtag")
    #doPlots(datasets, HistoList, MetBtagTauIDCuts, SaveExtension="JetSelMetBtagTauID")
    #doPlots(datasets, HistoList, MetBtagMtCuts, SaveExtension="JetSelMetBtagMt")
    #doPlots(datasets, HistoList, MetBtagDeltaPhiCuts, SaveExtension="JetSelMet_BtagDeltaPhi")
    #doPlots(datasets, HistoList, TauIDCut, SaveExtension="JetSelTauID")
    #doPlots(datasets, HistoList, AllSelectionCuts, SaveExtension="AllSelectionCuts")

    ### QCD method tesing
    doPlots(datasets, HistoList, And(Met + ">=30"), SaveExtension="JetSelMet30_DeltaPhiLoose")
    #doPlots(datasets, HistoList, And(Met + ">=50"), SaveExtension="JetSelMet50_DeltaPhiLoose")

    ### DeltaPhi Circular Cut: Loose
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiLooseCuts, Met + ">=50"), SaveExtension="JetSelBtagMet50_DeltaPhiLoose")
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiLooseCuts, Met + ">=60"), SaveExtension="JetSelBtagMet60_DeltaPhiLoose")

    ### DeltaPhi Circular Cut: Medium
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiMediumCuts, Met + ">=50"), SaveExtension="JetSelBtagMet50_DeltaPhiMedium")
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiMediumCuts, Met + ">=60"), SaveExtension="JetSelBtagMet60_DeltaPhiMedium")

    ### DeltaPhi Circular Cut: MediumPlus
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiMediumPlusCuts, Met + ">=50"), SaveExtension="JetSelBtagMet50_DeltaPhiMediumPlus")
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiMediumPlusCuts, Met + ">=60"), SaveExtension="JetSelBtagMet60_DeltaPhiMediumPlus")

    ### DeltaPhi Circular Cut: Tight
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiTightCuts, Met + ">=50"), SaveExtension="JetSelBtagMet50_DeltaPhiTight")
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiTightCuts, Met + ">=60"), SaveExtension="JetSelBtagMet60_DeltaPhiTight")

    ### DeltaPhi Circular Cut: TightPlus
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiTightPlusCuts, Met + ">=50"), SaveExtension="JetSelBtagMet50_DeltaPhiTightPlus")
    #doPlots(datasets, HistoList, And(BtagCut, DeltaPhiTightPlusCuts, Met + ">=60"), SaveExtension="JetSelBtagMet60_DeltaPhiTightPlus")


    return

######################################################################
def doPlots(datasets, HistoList, MyCuts, SaveExtension):
    '''
    def doPlots(datasets, HistoList, MyCuts, SaveExtension):
    This module does all necessary manipulations for plotting the TH1
    and TH2 histograms. Currently on TH1 plots are supported but 
    in the future the method doTH2Plots(datasets, HistoList, SaveExtension)
    will also be called here.
    '''

    doTH1Plots(datasets, HistoList, MyCuts, SaveExtension)

    return

######################################################################
def getDatasets(multicrabPath, myDataEra):
    '''
    def getDatasets(multicrabPath, myDataEra):
    This module used the user-defined path to a multicrab directory to 
    get the available datasets for a given Data-Era. 
    According to the boolean dictionary in the beginning of this file
    the datasets are merged and reordered. Optionally the PSet parameters
    are also printed for a specified dataset, also selected at the beginning 
    of this file with the "pSetToPrint" string.
    '''

    ### Get the ROOT files for all datasets, merge datasets and reorder them
    print "*** Obtaining datasets from: %s" % (multicrabPath)
    datasets = dataset.getDatasetsFromMulticrabCfg(directory=multicrabPath, dataEra=myDataEra)
    # print "*** Available datasets: %s" % (datasets.getAllDatasetNames())

    ### Print PSets used in ROOT-file generation
    if getBool("bPrintPSet"):
        print datasets.getDataset(pSetToPrint).getParameterSet()
        
    ### Take care of PU weighting, luminosity, signal merging etc... of the datatasets
    manageDatasets(datasets)

    return datasets

######################################################################
def manageDatasets(datasets):
    '''
    def manageDatasets(datasets):
    Handles the PU weighting, luminosity loading and signal merging of the datatasets.
    '''
    
    ### Since (by default) we use weighted counters, and the analysis job inputs are 
    ### normally skims (as are "v44_4" and "v53_1"), need to update events to PU weighted
    print "\n*** Updating events to PU weighted:"
    datasets.updateNAllEventsToPUWeighted()

    if getBool("bRemoveData"):
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()

    print "\n*** Default merging of dataset components:"
    plots.mergeRenameReorderForDataMC(datasets)
                
    if getBool("bRemoveSignal"): 
        print "\n*** Removing all signal samples"
        datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    else:
        print "\n*** Removing all signal samples, except m=%s GeV/cc" % (signalMass)
        datasets.remove(filter(lambda name: "TTToHplus" in name and not "M"+signalMass in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
        plots._legendLabels["TTToHplus_M"+signalMass] = "m_{H^{#pm}} = " + signalMass + " GeV/c^{2}"

    ### Setup style
    styleGenerator = styles.generator(fill=False)
    style = tdrstyle.TDRStyle()

    print "*** Setting signal cross sections, using BR(t->bH+)=%s and BR(H+ -> tau+ nu)=%s" % (BR_tH, BR_Htaunu)
    xsect.setHplusCrossSectionsToBR(datasets, BR_tH, BR_Htaunu)
    print "*** Merging WH and HH signals"
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section
    
    ### Now optionally remove datasets
    if getBool("bRemoveEwk"):
        mergeEwkMc(datasets)
        datasets.remove(filter(lambda name: "EWK MC" in name, datasets.getAllDatasetNames()))
    else:
        if getBool("bMergeEwk"):
            mergeEwkMc(datasets)
    if getBool("bRemoveQcd"):
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
        
    print "*** Available datasets: %s" % (datasets.getAllDatasetNames())

    return datasets

######################################################################
def mergeEwkMc(datasets):
    '''
    def mergeEwkMc(datasets):
    Merges the EWK MC samples into a single dataset. The style adopted is that of ttbar (default).
    The merging is controlled by the use of the "bMergeEwk" boolean.
    '''
    
    print "*** Merging EWK MC"
    datasets.merge("EWK MC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=False)
    plots._plotStyles["EWK MC"] = styles.ttStyle

    return #datasets

######################################################################
def createTH1Plot(datasets, name, **kwargs):
    ''' 
    def createTH1Plot(name, **kwargs):
    Creates the TH1 plots according to the global booleans and other 
    options, as defined at the top of this file.
    '''
    
    ### Copy arguments to a new dictionary
    args = {}
    args.update(kwargs)
    
    ### Proceed differently for Stacking and No-Stacking of plots
    if getBool("bRemoveData"):
        args["normalizeToLumi"] = MyLumi
    p = plots.DataMCPlot(datasets, name, **args)
    p.setDefaultStyles()

    if not getBool("bStackHistos"):
        p.histoMgr.setHistoDrawStyleAll("P")
        p.histoMgr.setHistoLegendStyleAll("P")
    
    return p

######################################################################
def doTH1Plots(datasets, HistoList, MyCuts, SaveExtension):
    ''' 
    def doTH1Plots(datasets, HistoList, MyCuts, SaveExtension):
    Loops over all histograms defined in HistoHelper.py and customises 
    each plot accordingly. Global booleans and other options are also
    taken care of (including x- and y- min, max, ratio, logY, etc..). See
    the beginning of the file for all available options.
    '''
    
    if getBool("bCustomRange"):
        drawPlot = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=getBool("bAddMCUncertainty"), log=getBool("bLogY"), ratio=getBool("bRatio"), addLuminosityText=getBool("bAddLumiText"), ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMinLog, "ymax": yMaxLog})
    else:
        drawPlot = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=getBool("bAddMCUncertainty"), log=getBool("bLogY"), ratio=getBool("bRatio"), addLuminosityText=getBool("bAddLumiText"), opts={"ymaxfactor": yMaxFactor}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymaxfactor": yMaxFactorLog})

    ### Define the event "weight" to be used
    if "passedBTagging" in MyCuts:
        EvtWeight = "(weightPileup*weightTauTrigger*weightPrescale*weightBTagging)"
    else:
        EvtWeight = "weightPileup*weightTauTrigger*weightPrescale"
        
    print "*** Cuts applied: \"%s\"" % (MyCuts)
    print "*** Weight applied: \"%s\"" % (EvtWeight)
    treeDraw = dataset.TreeDraw("tree", weight=EvtWeight)
    MyTreeDraw = treeDraw.clone(selection=MyCuts)    

    ### Go ahead and draw the plot
    histograms.createLegend.setDefaults(x1=xLegMin, x2= xLegMax, y1 = yLegMin, y2=yLegMax)

    ### Loop over all hName and expressions in the histogram list. Create & Draw plot
    counter=0        
    for h in HistoList:
        hName     = h.name
        hExpr     = MyTreeDraw.clone(varexp=h.expr)
        saveName  = "TH1_%s" % (hName)
        xLabel    = h.xlabel
        yLabel    = h.ylabel
        iBinWidth = h.binWidthX
        ### Consider hName with "_Vs_" in the name as a TH2 histogram 
        if "_Vs_" in hName:
            continue

        p = createTH1Plot(datasets, hExpr, normalizeToOne = getBool("bNormalizeToOne"))
        if not getBool("bStackHistos"):
            drawPlot(p, saveName + SaveExtension, xlabel=xLabel, ylabel=yLabel, rebinToWidthX=iBinWidth)
        else:
            drawPlot(p, saveName + "_Stacked" + SaveExtension, xlabel=xLabel, ylabel=yLabel, rebinToWidthX=iBinWidth)

        ### Do Data plots with QCD=Data-EwkMc. Only executed if certain (boolean) conditions are met.
        if getBool("bDataMinusEwk") and not getBool("bRemoveData"):

            if getBool("bCustomRange"):
                drawPlot2 = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=False, log=getBool("bLogY"), ratio=False, addLuminosityText=getBool("bAddLumiText"), ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMinLog, "ymax": yMaxLog})
            else:
                drawPlot2 = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=False, log=getBool("bLogY"), ratio=False, addLuminosityText=getBool("bAddLumiText"), opts={"ymaxfactor": yMaxFactor}, optsLog={"ymaxfactor": yMaxFactorLog})
            
            doDataMinusEwk(p, drawPlot2, datasets, hExpr, hName, xLabel, yLabel, iBinWidth, SaveExtension, hType={"TH1": True})

        ### Do QCD Purity plots
        if getBool("bQcdPurity"):
            doQcdPurPlots(p, drawPlot, datasets, hExpr, hName, xLabel, "Purity", SaveExtension)

    return

######################################################################
def doDataMinusEwk(p, drawPlot, datasets, hExpr, hName, xLabel, yLabel, binWidth, SaveExtension, **kwargs):
    '''
    def doDataMinusEwk(p, drawPlot, datasets, hExpr, hName, xLabel, yLabel, SaveExtension):
    For each histogram plotted with doPlots() an identical one with QCD=Data-Ewk MC is also plotted using this method.
    Loops over all histograms defined in HistoHelper.py and customises each plot accordingly. 
    The global boolean options are also taken care of including x- and y- min, max, ratio, logY, etc..
    '''

    args = kwargs.get("hType", None)
    if len(args) < 1:
        raise Exception("*** Should pass at least one keyword argument; Either \"TH1\" or \"TH2\".")

    if "TH1" not in args.keys() and "TH2" not in args.keys():
        raise Exception("*** Should pass at least one keyword argument; Either \"TH1\" or \"TH2\".")
    hType = args.keys()

    if not getBool("bDataMinusEwk") or getBool("bRemoveData"):
        print "*** Skipping replacement of QCD with Data-Ewk. bRemoveData==", getBool("bRemoveData")
        return

    if "TH1" in hType:
        p2 = createTH1Plot(datasets, hExpr, normalizeToOne = False)
    else:
        p2 = createTH2Plot(datasets, hExpr, normalizeToOne = False)

    hDataClone = p.histoMgr.getHisto("Data").getRootHisto().Clone("hData_Clone")
    if (p.histoMgr.getHisto("Data").getRootHisto()) == None:
        raise Exception("*** Cannot replace QCD with Data-Ewk since \"Data\" histogram is empty.")

    ### Copy Data histo to a new histo which will be the QCD=Data-EwkMc histo
    hDataMinusEwk = hDataClone.Clone("hDataMinusEwkMc_Clone")

    ### Loop over all histograms
    for h in p.histoMgr.getHistos():
        htmp = h.getRootHisto()
        if("StackedMC" in htmp.GetName()):
            hStackedMC = htmp.Clone("hStackedMC_Clone")
            for htmp in hStackedMC.GetHists():
                #print "***1) histo = ", (htmp.GetName())
                if (htmp.GetName() in ["Data", "TTToHplus", "sum_errors"]):
                    continue
                elif( "QCD" in htmp.GetName() ):
                    qcd = htmp
                    continue
                else:
                    #print "*** Subtracting %s from Data histo to get QCD=Data-EwkMc" % (htmp.GetName())
                    hDataMinusEwk.Add(htmp, -1)
        else:
            #print "***2) histo = ", (htmp.GetName())
            if(h.isData()):
                continue
            else:
                if (htmp.GetName() in ["TTToHplus", "sum_errors"]):
                    continue
                elif( "QCD" in htmp.GetName() ):
                    qcd = htmp
                    continue
                else:
                    #print "*** Subtracting %s from Data histo to get QCD=Data-EwkMc" % (htmp.GetName())
                    hDataMinusEwk.Add(htmp, -1)

    ### Customise QCD=Data-EwkMc histo
    aux.copyStyle(qcd, hDataMinusEwk)

    if "TH1" in hType:
        if getBool("bStackHistos"):
            DataMinusEwk = histograms.Histo(hDataMinusEwk, "hDataMinusEwkMc", "f", "HIST")
        else:
            DataMinusEwk = histograms.Histo(hDataMinusEwk, "hDataMinusEwkMc", "P", "P")        
    else:
        DataMinusEwk = histograms.Histo(hDataMinusEwk, "hDataMinusEwkMc", "", "P")

    DataMinusEwk.setIsDataMC(False, True)
    DataMinusEwk.setLegendLabel("Data - EWK_{MC}")

    ### Add QCD=Data-EwkMc histo to histograms list, remove QCD-MC histo from histograms list and customise plot 
    p2.histoMgr.insertHisto(2, DataMinusEwk) #insert QCD=Data-EwkMc histo at position 2 (correct order)
    p2.histoMgr.removeHisto("QCD") 
    ### For TH2 case remove the "Data" and "EWK MC" histos and setup the temperature style 
    if "TH2" in hType:
        p2.histoMgr.removeHisto("Data") 
        p2.histoMgr.removeHisto("EWK MC") #fixme
        p2.histoMgr.setHistoDrawStyleAll("COLZ")
        setHistoContours(p2, 30)
    
    ### Draw the plot with custom options and save
    if not getBool("bStackHistos"):
        saveName = "TH1_%s_%s" % (hName, "_DataMinusEwk" + SaveExtension)
    else:
        saveName = "TH1_%s_%s" % (hName, "DataMinusEwk_Stacked" + SaveExtension)
    drawPlot(p2, saveName, xlabel=xLabel, ylabel=yLabel, rebinToWidthX=binWidth)

    return

######################################################################
def doQcdPurPlots(p, drawPlot, datasets, hExpr, hName, xLabel, yLabel, SaveExtension):

    if getBool("bRemoveEwk"):
        print "*** WARNING: No Ewk samples found. Skipping QCD Purity plots."
        return

    histograms.createLegend.setDefaults(x1=xLegMin*(0.90), x2= xLegMax*(0.95), y1 = yLegMin, y2=yLegMax*1.2)
    saveName = "%s_%s" % (hName, SaveExtension + "_QcdPurity")

    ### Setup the histogram text mode and create plot
    p2 = createTH1Plot(datasets, hExpr, normalizeToOne = False)
    
    ### Define the purity histogram binning
    Bins = [40.0, 50.0, 60.0, 70.0, 80.0, 100.0, 120.0, 150.0, 200.0]
    myBins = array.array('d', Bins)

    ### Loop over all histograms to determine the number of signal and bkg events to calculate qcdPurity
    for htmp in p.histoMgr.getHistos():
        name = htmp.getName()
        h = htmp.getRootHisto().Rebin(len(myBins)-1, name, myBins)
        htmp.setRootHisto(h)

        if(name in "Data"):
            hQcdPur =  p.histoMgr.getHisto("Data").getRootHisto().Clone("hQcdPur")
            p2.histoMgr.removeHisto(name)
        elif(name in ["TTToHplus", "QCD"]):
            p2.histoMgr.removeHisto(name)
        else:
            hQcdPur.Add(h, -1)
            p2.histoMgr.removeHisto(name)

    hQcdPur.Divide(p.histoMgr.getHisto("Data").getRootHisto())
    Purity = histograms.Histo(setQcdPurityHistoStyle(hQcdPur), "Purity = #frac{Data-Ewk MC}{Data}", "", "")
    p2.histoMgr.appendHisto(Purity)
    
    ### Draw the plot with custom options and save
    drawPlot = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=getBool("bAddMCUncertainty"), log=False, ratio=getBool("bStackHistos"), addLuminosityText=getBool("bAddLumiText"), opts={"ymin": yMinPurity, "ymax": yMaxPurity})
    drawPlot(p2, saveName, rebin=1, xlabel=xLabel, ylabel=yLabel)

    return
######################################################################    
def setQcdPurityHistoStyle(histo):
    '''
    def setSignifHistoStyle(hSignif):
    '''
    colour = ROOT.kRed
    histo.SetMarkerColor(colour)
    histo.SetLineWidth(2)
    histo.SetLineColor(colour)
    histo.SetMarkerColor(colour)
    histo.SetMarkerStyle(ROOT.kFullCircle)
    histo.SetMarkerSize(1.2)
    histo.SetFillColor(0)

    return histo

######################################################################
if __name__ == "__main__":

    ### Call the main function
    main()

    ### Keep session alive (otherwise canvases close automatically)
    if not getBool("bBatchMode"):
        raw_input("*** DONE! Press \"ENTER\" key exit session: ")
