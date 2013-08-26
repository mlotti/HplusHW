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
### Boolean switches
bBatchMode        = True
bPrintPSet        = False
bStackHistos      = False
bLogY             = True
bRatioPlot        = False
bNormalizeToOne   = False #Not supported yet
bAddMCUncertainty = False
bAddLumiText      = True
bMcOnly           = False
bRemoveSignal     = False
bRemoveEwk        = False
bRemoveQcd        = False

### Other Definitions
ROOT.gROOT.SetBatch(bBatchMode)
signalMass = "160" #250
BR_tH      = 0.01
BR_Htaunu  = 1.0
yMin       = 0.0
yMax       = 0.5
yMinLog    = 1E-01
yMaxLog    = 1E+05
McOnlyLumi = 2.3*1000 #(pb)
myAnalysis = "signalAnalysisLight"
myDataEra  = "Run2011A"
multicrabPath = ["/Users/attikis/my_work/cms/lxplus/TreeAnalysis_MHT_130215_123318/"]

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
    datasets = editDatasets(datasets)

    ### Get the histogram names, tree expressions, xLabels and yLabels. All three are connected with unique histogram name key.
    histoDict, xLabelDict, yLabelDict = GetDictionaries()
    
    ### Standard Cuts
    doPlots(datasets, histoDict, xLabelDict, yLabelDict, JetSelectionCuts, SaveExtension="JetSelections")
    doPlots(datasets, histoDict, xLabelDict, yLabelDict, JetSelectionSanityCuts, SaveExtension="JetSelectionsSanity")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, MetBtagCuts, SaveExtension="MetBtag")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, TauIDMetBtagCuts, SaveExtension="TauIDMetBtag")
    #doPlots(datasets, histoDict, xLabelDict, yLabelDict, MetBtagDeltaPhiCuts, SaveExtension="MetBtagDeltaPhi")

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

    if bMcOnly:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()

    print "\n*** Default merging of dataset components:"
    plots.mergeRenameReorderForDataMC(datasets)
                
    print "\n*** Removing all signal samples, except m=%s" % (signalMass)
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M"+signalMass in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    ### Setup style
    styleGenerator = styles.generator(fill=False)
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.02, dy=+0.00)

    print "*** Setting signal cross sections, using BR(t->bH+)=%s and BR(H+ -> tau+ nu)=%s" % (BR_tH, BR_Htaunu)
    xsect.setHplusCrossSectionsToBR(datasets, BR_tH, BR_Htaunu)
    print "*** Merging WH and HH signals"
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section
    
    return datasets

######################################################################
def editDatasets(datasets):
    
    if bRemoveEwk:
        mergeEwkMc(datasets)
        datasets.remove(filter(lambda name: "EWK MC" in name, datasets.getAllDatasetNames()))
    else:
        mergeEwkMc(datasets)

    if bRemoveQcd:
        datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
        
    if bRemoveSignal:
        datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

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
def createPlot(datasets, name, **kwargs):
    ''' 
    def createPlot(name, **kwargs):
    '''
        
    args = {}
    args.update(kwargs)
    if not ("normalizeToOne" in args and args["normalizeToOne"]):
        args["normalizeToLumi"] = McOnlyLumi 
    p = plots.MCPlot(datasets, name, **args)
    p.setDefaultStyles()
    p.histoMgr.setHistoDrawStyleAll("COLZ") #COLZ, LEGO2, SURF2, SCAT
    p.histoMgr.setHistoLegendStyleAll("P") # "L", "P"
    gStyle.SetPalette(1)
  
    return p

######################################################################
def doPlots(datasets, histoDict, xLabelDict, yLabelDict,  MyCuts, SaveExtension):
    ''' 
    def doPlots(datasets, histoDict, xLabelDict, yLabelDict,  MyCuts, SaveExtension):
    '''

    ### Create a progress bar to inform user of progress status
    maxValue = len(histoDict)
    print "\n*** Preparing %s histogram(s) for the cut group:\n    \"%s\"" % (maxValue, MyCuts)
    pBar = StartProgressBar(maxValue)
    

    drawPlot = plots.PlotDrawer(bStackHistos, addMCUncertainty=bAddMCUncertainty, log=bLogY, ratio=bRatioPlot, addLuminosityText=bAddLumiText, ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, optsLog={"ymin": yMinLog, "ymax": yMaxLog})

    ### Define the event "weight" to be used
    if "passedBTagging" in MyCuts:
        EvtWeight = "(weightPileup*weightTrigger*weightPrescale*weightBTagging)"
    else:
        EvtWeight = "weightPileup*weightTrigger*weightPrescale"
        
    print "*** And Event weight:\n    \"%s\"" % (EvtWeight)
    treeDraw = dataset.TreeDraw("tree", weight=EvtWeight)
    MyTreeDraw = treeDraw.clone(selection=MyCuts)
    
    ### Loop over all hName and expressions in the histogram dictionary "histoDict". Create & Draw plot
    counter=0        
    for key in histoDict:
        hName = key
        histo = MyTreeDraw.clone(varexp=histoDict[hName])
        fileName = "%s_%s" % (hName, SaveExtension)
        xLabel = xLabelDict[hName]
        yLabel = yLabelDict[hName]
            
        ### Go ahead and draw the plot
        p = createPlot(datasets, histo, normalizeToOne = bNormalizeToOne)
        drawPlot(p, fileName, rebin=1, xlabel=xLabel, ylabel=yLabel)
        
        ### Increment counter and pdate progress bar
        counter = counter+1
        pBar.update(counter)
        
    ### Stop pbar once done with the loop
    pBar.finish()    

    return

######################################################################
if __name__ == "__main__":

    ### Call the main function here
    main()

    ### Keep session alive (otherwise canvases close automatically)
    if bBatchMode == False:
        raw_input("*** DONE! Press \"ENTER\" key to continue: ")
