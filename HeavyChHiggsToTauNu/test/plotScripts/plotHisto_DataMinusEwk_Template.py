#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
import sys
import math
import ROOT
from ROOT import gStyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from HistoHelperNew import *

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
"bCustomRange"      : True,
# 
"bDataMinusEwk"     : True,  #Requires: bRemoveQcd==False
"bStackHistos"      : True, 
"bMergeEwk"         : True,
#
"bRemoveData"       : False,
"bRemoveSignal"     : False,  #Requires : RemoveData==True (for it to be True)
"bRemoveEwk"        : False,
"bRemoveQcd"        : False,
}
    
### Other Global Definitions
getBool        = lambda Key: boolDict[Key]
BR_tH          = 0.01
BR_Htaunu      = 1.0
signalMass     = "160" #250
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
yMinPurity     = 0.1 #0.9 #0.5
yMaxPurity     = 1.005 #1.005
MyLumi         = 2.3*1000 #(pb)
myAnalysis     = "signalAnalysisLight"
pSetToPrint    = "TTToHplusBHminusB_M120_Fall11"
#myDataEra      = "Run2011A"
#myDataEra      = "Run2011B" 
myDataEra      = "Run2011AB"
multicrabPath  = "/Users/attikis/my_work/cms/lxplus/FullHplusMass_FromStefan_130327_142054/"
ROOT.gROOT.SetBatch( getBool("bBatchMode") )

######################################################################
### Function declarations
######################################################################
def main():

    ### Get the desired datasets 
    datasets = getDatasets(multicrabPath, myDataEra)

    ### Plot all histograms defined in the HistoTemplateList found in the file HistoHelper.py
    doPlots(datasets, HistoTemplateList, SaveExtension="")

    return

######################################################################
def doPlots(datasets, HistoTemplateList, SaveExtension):
    '''
    def doPlots(datasets, HistoTemplateList, SaveExtension):
    '''

    doTH1Plots(datasets, HistoTemplateList, SaveExtension="TH1" + SaveExtension)

    return

######################################################################
def getDatasets(multicrabPath, myDataEra):
    '''
    def getDatasets(multicrabPath, myDataEra):
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
    Merges the EWK MC samples into a single dataset. The style adopted is that of ttbar (default)
    '''
    
    print "*** Merging EWK MC"
    datasets.merge("EWK MC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=False)
    plots._plotStyles["EWK MC"] = styles.ttStyle

    return #datasets

######################################################################
def createTH1Plot(datasets, name, **kwargs):
    ''' 
    def createTH1Plot(name, **kwargs):
    Creates the TH1 plots according to the global booleans options defined at the top.
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
def doTH1Plots(datasets, HistoTemplateList, SaveExtension):
    ''' 
    def doTH1Plots(datasets, HistoTemplateList, SaveExtension):
    Loops over all histograms defined in HistoHelper.py and customises each plot accordingly. 
    The global boolean options are also taken care of including x- and y- min, max, ratio, logY, etc..
    '''
    
    if getBool("bCustomRange"):
        drawPlot = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=getBool("bAddMCUncertainty"), log=getBool("bLogY"), ratio=getBool("bRatio"), addLuminosityText=getBool("bAddLumiText"), ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMinLog, "ymax": yMaxLog})
    else:
        drawPlot = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=getBool("bAddMCUncertainty"), log=getBool("bLogY"), ratio=getBool("bRatio"), addLuminosityText=getBool("bAddLumiText"), opts={"ymaxfactor": yMaxFactor}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymaxfactor": yMaxFactorLog})
    

    ### Go ahead and draw the plot
    histograms.createLegend.setDefaults(x1=xLegMin, x2= xLegMax, y1 = yLegMin, y2=yLegMax)

    ### Loop over all hName and expressions in the histogram list. Create & Draw plot
    counter=0        
    for h in HistoTemplateList:
        hName     = h.name
        hPath     = h.path
        fileName  = "%s_%s" % (hName, SaveExtension)
        xLabel    = h.xlabel
        yLabel    = h.ylabel
        iBinWidth = h.binWidthX
        if "_Vs_" in hName:
            continue

        p = createTH1Plot(datasets, hPath, normalizeToOne = getBool("bNormalizeToOne"))
        if not getBool("bStackHistos"):
            drawPlot(p, fileName, rebinToWidthX=iBinWidth)
        else:
            drawPlot(p, fileName + "_Stacked", xlabel=xLabel, ylabel=yLabel, rebinToWidthX=iBinWidth)

    ### Do Data plots with QCD=Data-EwkMc. Only executed if certain (boolean) conditions are met.
    if getBool("bDataMinusEwk") and not getBool("bRemoveData"):

        if getBool("bCustomRange"):
            drawPlot2 = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=False, log=getBool("bLogY"), ratio=False, addLuminosityText=getBool("bAddLumiText"), ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMinLog, "ymax": yMaxLog})
        else:
            drawPlot2 = plots.PlotDrawer(stackMCHistograms=getBool("bStackHistos"), addMCUncertainty=False, log=getBool("bLogY"), ratio=False, addLuminosityText=getBool("bAddLumiText"), opts={"ymaxfactor": yMaxFactor}, optsLog={"ymaxfactor": yMaxFactorLog})
            
        doDataMinusEwk(p, drawPlot2, datasets, hPath, hName, xLabel, yLabel, iBinWidth, SaveExtension, hType={"TH1": True})

    return

######################################################################
def doDataMinusEwk(p, drawPlot, datasets, hPath, hName, xLabel, yLabel, binWidth, SaveExtension, **kwargs):
    '''
    def doDataMinusEwk(p, drawPlot, datasets, hPath, hName, xLabel, yLabel, SaveExtension):
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
        p2 = createTH1Plot(datasets, hPath, normalizeToOne = False)
    else:
        p2 = createTH2Plot(datasets, hPath, normalizeToOne = False)

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
                if( "TTToHplus" in htmp.GetName() or "sum_errors" in htmp.GetName() ):
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
    # ## For TH2 case remove the "Data" and "EWK MC" histos and setup the temperature style 
    if "TH2" in hType:
        p2.histoMgr.removeHisto("Data") 
        p2.histoMgr.removeHisto("EWK MC") #fixme
        p2.histoMgr.setHistoDrawStyleAll("COLZ")
        setHistoContours(p2, 30)
    
    ### Draw the plot with custom options and save
    if not getBool("bStackHistos"):
        saveName = "%s_%s" % (hName, SaveExtension + "_DataMinusEwk")
    else:
        saveName = "%s_%s" % (hName, SaveExtension + "_DataMinusEwk_Stacked")
    drawPlot(p2, saveName, xlabel=xLabel, ylabel=yLabel, rebinToWidthX=binWidth)

    return

######################################################################
if __name__ == "__main__":

    ### Call the main function
    main()

    ### Keep session alive (otherwise canvases close automatically)
    if not getBool("bBatchMode"):
        raw_input("*** DONE! Press \"ENTER\" key to continue: ")
