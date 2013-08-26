#!/usr/bin/env python

######################################################################
# All imported modules here
######################################################################
import sys
import array
import ROOT
from ROOT import gStyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
from TreeHelper import *

######################################################################
### Define options and declarations here
######################################################################
### Global Boolean switches
bBatchMode        = True
bPrintPSet        = False
bLogY             = True
bNormalizeToOne   = False
bAddMCUncertainty = True
bAddLumiText      = True
bCustomRange      = False
#
bDataMinusEwk     = True #True 
bStackHistos      = False
bMcOnly           = True #False
bMergeEwk         = True
#
bRemoveSignal     = True #False 
bRemoveEwk        = True #False 
bRemoveQcd        = False
McTypesPresent    = 3-(int(bRemoveSignal)+int(bRemoveEwk)+int(bRemoveQcd))

if bRemoveSignal==True:
    BR_tH      = 0.00
    BR_Htaunu  = 0.00
else:
    BR_tH      = 0.01
    BR_Htaunu  = 1.0

### Other Global Definitions
ROOT.gROOT.SetBatch(bBatchMode)
signalMass = "160" #250
yMin       = 0.0
yMax       = 0.5
yMinLog    = 0.5E-01
yMaxLog    = 1E+03
yMinRatio  = 0.0
yMaxRatio  = 2.0
if bLogY==True:
    yMaxFactor = 100
else:
    yMaxFactor = 1.5
McOnlyLumi = 2.3*1000 #(pb)
myAnalysis = "signalAnalysisLight"
myDataEra  = "Run2011A"
#multicrabPath = ["/Users/attikis/my_work/cms/lxplus/TreeAnalysis_MHT_130215_123318/"]
multicrabPath = ["/Users/attikis/my_work/cms/lxplus/TreeAnalysis_SelJetsInclTau_130222_155040/"]

######################################################################
### Function declarations here
######################################################################
def main():
    '''
    def main():
    Do all main manipulations here. No helper function should be called here. 
    '''

    ### Get the desired datasets 
    datasets = getDatasets(multicrabPath, myDataEra)

    ### Get the histogram names, tree expressions, xLabels and yLabels. All three are connected with unique histogram name key.
    histoDict, xLabelDict, yLabelDict = GetDictionaries()
    
    ### Standard Cuts
    ## doTH1Plots(datasets, histoDict, xLabelDict, yLabelDict, JetSelectionSanityCuts, SaveExtension="TH1_JetSelSanity")
    doPlots(datasets, histoDict, xLabelDict, yLabelDict, JetSelectionCuts, SaveExtension="JetSel")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, JetSelectionMtCuts, SaveExtension="JetSelMt")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, MetBtagCuts, SaveExtension="MetBtag")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, MetBtagTauIDCuts, SaveExtension="MetBtagTauID")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, MetBtagMtCuts, SaveExtension="MetBtagMt")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, MetBtagDeltaPhiCuts, SaveExtension="MetBtagDeltaPhi")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, AllSelectionCuts, SaveExtension="AllSelectionCuts")

    ### Trial Cuts
    # doPlots(datasets, histoDict, xLabelDict, yLabelDict, AllJetsCuts, SaveExtension="TH1_AllJets_JetSel")
    # doPlots(datasets, histoDict, xLabelDict, yLabelDict, AllJetsMtCuts, SaveExtension="TH1_AllJets_JetSelMt")
    # doPlots(datasets, histoDict, xLabelDict, yLabelDict, AllJetsMetBtagCuts, SaveExtension="TH1_AllJets_MetBtag")
    # doPlots(datasets, histoDict, xLabelDict, yLabelDict, AllJetsMetBtagMtCuts, SaveExtension="TH1_AllJets_MetBtagMt")
    # doPlots(datasets, histoDict, xLabelDict, yLabelDict, And(MetBtagCuts, "DeltaPhiMetLdg_DeltaPhiTauMet_RCut"), SaveExtension="TH1_MetBtagRCut")
    # doPlots(datasets, histoDict, xLabelDict, yLabelDict, And(MetBtagCuts, "DeltaPhiMetLdg_DeltaPhiTauMet_AntiRCut"), SaveExtension="TH1_MetBtagRAntiCut")

    return

######################################################################
def doPlots(datasets, histoDict, xLabelDict, yLabelDict, MyCuts, SaveExtension):
    '''
    def doPlots(datasets, histoDict, xLabelDict, yLabelDict, MyCuts, SaveExtension):
    '''

    histograms.createLegend.moveDefaults(dx=-0.06, dy=+0.02)
    doTH1Plots(datasets, histoDict, xLabelDict, yLabelDict, MyCuts, SaveExtension="TH1_+" + SaveExtension)

    histograms.createLegend.moveDefaults(dx=+10.06, dy=+10.02)
    doTH2Plots(datasets, histoDict, xLabelDict, yLabelDict, MyCuts, SaveExtension="TH2+" + SaveExtension)

    ### Set legend position back to default
    histograms.createLegend.setDefaults(x1=0.4, y2=0.5)

    return

######################################################################
def getDatasets(multicrabPath, myDataEra):
    '''
    def getDatasets(multicrabPath):
    '''

    ### Get the ROOT files for all datasets, merge datasets and reorder them
    print "*** Obtaining datasets from: %s" % (multicrabPath)
    datasets = dataset.getDatasetsFromMulticrabDirs(multicrabPath, dataEra=myDataEra)

    ### Print PSets used in ROOT-file generation
    printPSet(bPrintPSet, folderName=myAnalysis+myDataEra)
    
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

    if bMcOnly==True:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()

    print "\n*** Default merging of dataset components:"
    plots.mergeRenameReorderForDataMC(datasets)
                
    print "\n*** Removing all signal samples, except m=%s GeV/cc" % (signalMass)
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M"+signalMass in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    ### Setup style
    styleGenerator = styles.generator(fill=False)
    plots._legendLabels["TTToHplus_M"+signalMass] = "m_{H^{+}} = " + signalMass + " GeV/c^{2}"
    style = tdrstyle.TDRStyle()

    print "*** Setting signal cross sections, using BR(t->bH+)=%s and BR(H+ -> tau+ nu)=%s" % (BR_tH, BR_Htaunu)
    xsect.setHplusCrossSectionsToBR(datasets, BR_tH, BR_Htaunu)
    print "*** Merging WH and HH signals"
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section
    
    ### Now optionally remove datasets
    if bRemoveEwk:
        mergeEwkMc(datasets)
        datasets.remove(filter(lambda name: "EWK MC" in name, datasets.getAllDatasetNames()))
    else:
        if bMergeEwk==True:
            mergeEwkMc(datasets)

    if bRemoveQcd:
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
        
    #if bRemoveSignal: FIXME
    #    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    #    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    print "*** Available datasets: %s" % (datasets.getAllDatasetNames())

    return datasets

######################################################################
def mergeEwkMc(datasets):
    '''
    def mergeEwkMc(datasets):
    '''
    
    print "*** Merging EWK MC for datasets object \"%s\"" % (str(datasets))
    datasets.merge("EWK MC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=False)
    plots._plotStyles["EWK MC"] = styles.ttStyle

    return #datasets

######################################################################
def createTH1Plot(datasets, name, **kwargs):
    ''' 
    def createTH1Plot(name, **kwargs):
    '''
    
    ### Copy arguments to a new dictionary
    args = {}
    args.update(kwargs)
    
    ### Proceed differently for MC-only plots and Data-MC plots
    if bMcOnly==True:
        if not ("normalizeToOne" in args and args["normalizeToOne"]):
            args["normalizeToLumi"] = McOnlyLumi
        p = plots.MCPlot(datasets, name, **args)
        if bStackHistos==True:
            p.setDefaultStyles()
        else:
            p.setDefaultStyles()
            p.histoMgr.setHistoDrawStyleAll("P")
            p.histoMgr.setHistoLegendStyleAll("P")
    else:
        p = plots.DataMCPlot(datasets, name, **kwargs)
        if bStackHistos==True:
            p.setDefaultStyles()
        else:
            p.setDefaultStyles()
            p.histoMgr.setHistoDrawStyleAll("P")
            p.histoMgr.setHistoLegendStyleAll("P")
    
    return p

######################################################################
def createTH2Plot(datasets, name, **kwargs):
    ''' 
    def createTH2Plot(name, **kwargs):
    '''

    ### Copy arguments to a new dictionary
    args = {}
    args.update(kwargs)
        
    ### Proceed differently for MC-only plots and Data-MC plots
    if not ("normalizeToOne" in args and args["normalizeToOne"]):
        args["normalizeToLumi"] = McOnlyLumi
    p = plots.DataMCPlot(datasets, name, **args)
    p.setDefaultStyles()
    p.histoMgr.setHistoDrawStyleAll("COLZ")
    gStyle.SetPalette(1)
  
    return p

######################################################################
def doTH1Plots(datasets, histoDict, xLabelDict, yLabelDict,  MyCuts, SaveExtension):
    ''' 
    def doTH1Plots(datasets, histoDict, xLabelDict, yLabelDict,  MyCuts, SaveExtension):
    '''

    ### Create a progress bar to inform user of progress status. Calculate the number of TH1 histos only
    maxValue = 0
    for key in histoDict:
        if "_Vs_" in key:
            continue
        else:
            maxValue += 1
    if bDataMinusEwk==True and bMcOnly==False:
        maxValue= maxValue*2
    if maxValue==0:
        print "*** NOTE! No TH1 histos to plot. Exiting doTH1Plots() module."
        return
    print "\n*** Preparing %s TH1 histogram(s) for the cut group:\n    \"%s\"" % (maxValue, MyCuts)
    pBar = StartProgressBar(maxValue)
    
    if bCustomRange:
        drawPlot = plots.PlotDrawer(stackMCHistograms=bStackHistos, addMCUncertainty=bAddMCUncertainty, log=bLogY, ratio=not bMcOnly, addLuminosityText=bAddLumiText, ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMinLog, "ymax": yMaxLog})
    else:
        drawPlot = plots.PlotDrawer(stackMCHistograms=bStackHistos, addMCUncertainty=bAddMCUncertainty, log=bLogY, ratio=bStackHistos, addLuminosityText=bAddLumiText, opts={"ymaxfactor": yMaxFactor}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMinLog, "ymaxfactor": yMaxFactor})
    
    ### Define the event "weight" to be used
    if "passedBTagging" in MyCuts:
        #EvtWeight = "(weightPileup*weightTrigger*weightPrescale*weightBTagging)"
        EvtWeight = "(weightPileup*weightTauTrigger*weightPrescale*weightBTagging)"
    else:
        #EvtWeight = "weightPileup*weightTrigger*weightPrescale"
        EvtWeight = "weightPileup*weightTauTrigger*weightPrescale"
        
    print "*** And Event weight:\n    \"%s\"" % (EvtWeight)
    treeDraw = dataset.TreeDraw("tree", weight=EvtWeight)
    MyTreeDraw = treeDraw.clone(selection=MyCuts)
    
    ### Loop over all hName and expressions in the histogram dictionary "histoDict". Create & Draw plot
    counter=0        
    for key in histoDict:
        if "_Vs_" in key:
            continue
        hName = key
        histo = MyTreeDraw.clone(varexp=histoDict[hName])
        fileName = "%s_%s" % (hName, SaveExtension)
        xLabel = xLabelDict[hName]
        yLabel = yLabelDict[hName]
            
        ### Go ahead and draw the plot
        p = createTH1Plot(datasets, histo, normalizeToOne = bNormalizeToOne)
        drawPlot(p, fileName, rebin=1, xlabel=xLabel, ylabel=yLabel)

        ### Increment counter and pdate progress bar
        counter = counter+1
        pBar.update(counter)
    
        ### Do Data plots with QCD= Data-Ewk_MC. Only executed if certain (boolean) conditions are met.
        doDataMinusEWk(p, drawPlot, datasets, counter, histo, hName, xLabel, yLabel, SaveExtension)
        pBar.update(counter)
        
    ### Stop pbar once done with the loop
    pBar.finish()    

    return

######################################################################
def doTH2Plots(datasets, histoDict, xLabelDict, yLabelDict,  MyCuts, SaveExtension):
    ''' 
    def doTH2Plots(datasets, histoDict, xLabelDict, yLabelDict,  MyCuts, SaveExtension):
    '''
    if McTypesPresent>1:
        print "*** WARNING: More than one MC-type histo found present (McTypesPresent=%s). This is not allowed for a TH2. Aboring plotting of TH2." %(McTypesPresent)
        return

    if bMcOnly==False:
        print "*** NOTE: bMcOnly is set to %s. Disabling all MC samples for the TH2 plots. Only \"Data\" is available." % (bMcOnly)
        bMergeEwk     = True
        bRemoveSignal = True
        bRemoveEwk    = True
        bRemoveQcd    = True

    ### Create a progress bar to inform user of progress status. Calculate the number of TH1 histos only
    maxValue = 0
    for key in histoDict:
        if not "_Vs_" in key:
            continue
        else:
            maxValue += 1
    if maxValue==0:
        print "*** NOTE! No TH2 histos to plot. Exiting doTH2Plots() module."
        return
    print "\n*** Preparing %s TH2 histogram(s) for the cut group:\n    \"%s\"" % (maxValue, MyCuts)
    pBar = StartProgressBar(maxValue)

    if bCustomRange:
        drawPlot = plots.PlotDrawer(stackMCHistograms=False, addMCUncertainty=bAddMCUncertainty, log=false, ratio=False, addLuminosityText=bAddLumiText, ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMinLog, "ymax": yMaxLog})
    else:
        drawPlot = plots.PlotDrawer(stackMCHistograms=False, addMCUncertainty=bAddMCUncertainty, log=False, ratio=False, addLuminosityText=bAddLumiText, ratioYlabel="Ratio")

    ### Define the event "weight" to be used
    if "passedBTagging" in MyCuts:
        #EvtWeight = "(weightPileup*weightTrigger*weightPrescale*weightBTagging)"
        EvtWeight = "(weightPileup*weightTauTrigger*weightPrescale*weightBTagging)"
    else:
        #EvtWeight = "weightPileup*weightTrigger*weightPrescale"
        EvtWeight = "weightPileup*weightTauTrigger*weightPrescale"
        
    print "*** And Event weight:\n    \"%s\"" % (EvtWeight)
    treeDraw = dataset.TreeDraw("tree", weight=EvtWeight)
    MyTreeDraw = treeDraw.clone(selection=MyCuts)
    
    ### Loop over all hName and expressions in the histogram dictionary "histoDict". Create & Draw plot
    counter=0        
    for key in histoDict:
        if not "_Vs_" in key:
            continue
        else:
            hName = key
            histo = MyTreeDraw.clone(varexp=histoDict[hName])
            fileName = "%s_%s" % (hName, SaveExtension)
            xLabel = xLabelDict[hName]
            yLabel = yLabelDict[hName]
            
        ### Go ahead and draw the plot
        p = createTH2Plot(datasets, histo, normalizeToOne = bNormalizeToOne)
        drawPlot(p, fileName, rebin=1, xlabel=xLabel, ylabel=yLabel)
        
        ### Increment counter and pdate progress bar
        counter = counter+1
        pBar.update(counter)
        
    ### Stop pbar once done with the loop
    pBar.finish()    

    return

######################################################################
def doDataMinusEWk(p, drawPlot, datasets, counter, histo, hName, xLabel, yLabel, SaveExtension):

    if bDataMinusEwk==False or bMcOnly==True:
        return

    ### Create QCD=Data-EwkMc by copying data histo and then subtracting EwkMc
    if bStackHistos==True:
        ### Copy Data histo to a new histo which will be the QCD=Data-EwkMc histo
        hDataMinusEwk = p.histoMgr.getHisto("Data").getRootHisto().Clone("hDataMinusEwkMc_Clone")
        hDataMinusEwk.Reset()
        hDataMinusEwk.Add(p.histoMgr.getHisto("Data").getRootHisto())
        hStackedMC = p.histoMgr.getHisto("StackedMC").getRootHisto().Clone("hStackedMC_Clone")

        for htmp in hStackedMC.GetHists():
            if("TTToHplus" in htmp.GetName()):
                #print "Skipping: ", htmp.GetName()
                continue
            if("QCD" in htmp.GetName()):
                #print "Skipping: ", htmp.GetName()
                continue
            #print "Subtracting: ", htmp.GetName()
            hDataMinusEwk.Add(htmp, -1)
                
        p2 = createTH1Plot(datasets, histo, normalizeToOne = False)
        qcd = histograms.Histo(hDataMinusEwk, "hDataMinusEwkMc", "f", "HIST")
        qcd.setIsDataMC(False, True)
        qcd.setLegendLabel("Data - EWK_{MC}")
        #p2.histoMgr.insertHisto(1, qcd) #insert QCD histo at position 1 (correct order)
        #p2.histoMgr.appendHisto(qcd) 
        p2.histoMgr.insertHisto(2, qcd) #insert QCD histo at position 2 (correct order)

        p2.histoMgr.removeHisto("QCD")

        plots._plotStyles["hDataMinusEwkMc"] = styles.qcdStyle

        saveName = "%s_%s" % (hName, SaveExtension + "_DataMinusEwk")
        drawPlot(p2, saveName, rebin=1, xlabel=xLabel, ylabel=yLabel)
        counter = counter+1
        return
    else:
        ### Copy Data histo to a new histo which will be the QCD=Data-EwkMc histo
        hDataMinusEwk = p.histoMgr.getHisto("QCD").getRootHisto().Clone("hDataMinusEwkMc_Clone")
        hDataMinusEwk.Reset()

        ### Loop over histograms
        for h in p.histoMgr.getHistos():
            htmp = h.getRootHisto()
            #print "*** htmp.GetName() = ", htmp.GetName()

            if(h.isData()):
                #print "*** Adding: ", htmp.GetName()
                hDataMinusEwk.Add(htmp, +1)
            else:
                if("TTToHplus" in htmp.GetName() or "QCD" in htmp.GetName()):
                    #print "*** Skipping: ", htmp.GetName()
                    continue
                else:
                    #print "*** Subtracting: ", htmp.GetName()
                    hDataMinusEwk.Add(htmp, -1)
                
        p2 = createTH1Plot(datasets, histo, normalizeToOne = False)
        qcd = histograms.Histo(hDataMinusEwk, "hDataMinusEwkMc", "P", "P")
        qcd.setIsDataMC(False, True)
        qcd.setLegendLabel("Data - EWK_{MC}")
        p2.histoMgr.insertHisto(2, qcd) #insert QCD histo at position 1 (correct order)
        p2.histoMgr.removeHisto("QCD")

        plots._plotStyles["hDataMinusEwkMc"] = styles.qcdStyle

        saveName = "%s_%s" % (hName, SaveExtension + "_DataMinusEwk")
        drawPlot(p2, saveName, rebin=1, xlabel=xLabel, ylabel=yLabel)
        counter = counter+1
        return


######################################################################
if __name__ == "__main__":

    ### Call the main function here
    main()

    ### Keep session alive (otherwise canvases close automatically)
    if bBatchMode == False:
        raw_input("*** DONE! Press \"ENTER\" key to continue: ")
