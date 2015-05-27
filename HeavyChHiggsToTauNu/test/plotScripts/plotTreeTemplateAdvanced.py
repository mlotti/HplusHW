#!/usr/bin/env python

######################################################################
#
# Author : Matti Kortelainen, Alexandros Attikis
# Note   : This is a tree test plotting script
#
######################################################################
import sys
import array

import ROOT
ROOT.gROOT.SetBatch(False) #True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
######################################################################
# Per-event cuts: HIG-11-019
######################################################################
JetSelection = "jets_p4@.size() >= 3"
MetCut = "met_p4.Pt() > 50"
Mt = "TMath::Sqrt(2*tau_p4.Et()*met_p4.Et()*( 1.0 - ( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() )))"
MtCut = Mt + ">= 200"
BtagCut = "passedBTagging >= 1.0"
TauIsoCut = "tau_id_byTightIsolation >= 1.0"
DeltaPhi = "TMath::ACos(( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() ))*(180/TMath::Pi())"
DeltaPhiCut = DeltaPhi + "<= 160"
SphericityCut = "sphericity >= 0.5"
AlphaTCut = "alphaT >= 0.5"
CircularityCut = "circularity >= 0.1"
CircularityAntiCut = "circularity <= 0.1"

######################################################################
# Define my cuts
######################################################################
MetBtagDeltaPhiCuts = And(MetCut, BtagCut, DeltaPhiCut)
MetBtagDeltaPhiCircularityCuts = And(MetCut, BtagCut, DeltaPhiCut, CircularityCut)
TestCuts = CircularityAntiCut

######################################################################
# Declarations
######################################################################
EvtWeight = "weightPileup*weightTrigger*weightPrescale"
treeDraw = dataset.TreeDraw("tree", weight=EvtWeight)

######################################################################
# Define the main function here:
def main():
    
    # Get the ROOT files for all datasets, merge datasets and reorder them
    datasets = dataset.getDatasetsFromMulticrabCfg(directory="/Volumes/disk/attikis/HIG-12-037/TreeAnalysis_v44_4_130113_105229/", dataEra="Run2011A")
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()    
    plots.mergeRenameReorderForDataMC(datasets)

    # Merge desirable datasets
    datasets.merge("EWK MC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"])
    plots._plotStyles["EWK MC"] = styles.ttStyle  #plots._plotStyles["EWK"] = styles.getEWKStyle()
    
    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    # Setup style
    styleGenerator = styles.generator(fill=True)
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.0, dy=+0.0)
    
    # Merge signals into one histo
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Print desirable information here
    print "*** Event weight applied: %s" % (EvtWeight)
    print "*** Available datasets: %s" % (datasets.getAllDatasetNames())
    print "*** WARNING! What about btag scale factor?"
    print "*** Integrated Luminosity: %s (pb)" % (datasets.getDataset("Data").getLuminosity())

    # Define histogram name, expression, and binning here: 
    # { hName": "expression >> hNameTmp(nBins, xMin, xMax) }
    histoDict1 = {
        "sphericity": "sphericity >> sphericity(20, 0.0, 1.0)", 
        "aplanarity": "aplanarity >> aplanarity(20, 0.0, 0.5)", 
        "planarity": "planarity >> planarity(20, 0.0, 0.5)", 
        "circularity": "circularity >> circularity(20, 0.0, 1.0)", 
        "alphaT": "alphaT >> alphaT(20, 0.0, 1.0)", 
        "mT": "%s >> mT(30, 0.0, 600.0)" % (Mt)
        }

    # Do all plots defined in doPlots(datasets) function
#    doPlots(datasets, histoDict1, "", SaveExtension = "JetSelection")
#    doPlots(datasets, histoDict1, MetBtagDeltaPhiCuts, SaveExtension = "Met_Btag_DeltaPhi")
#    doPlots(datasets, histoDict1, MetBtagDeltaPhiCircularityCuts, SaveExtension = "Met_Btag_DeltaPhi_Circularity")
#    doPlots(datasets, histoDict1, TestCuts, SaveExtension = "Test")


    # Do just mT plots
    histoDict2 = {
        "mT": "%s >> mT(30, 0.0, 600.0)" % (Mt)
        }

    for i in range(1, 8):
        cutValue = (i+0.0)/(10.0)
        doPlots(datasets, histoDict2, "circularity <= %f" % (cutValue), SaveExtension = "Circularity%s" % (i))
        
    # Keep session alive (otherwise canvases close automatically)
    # raw_input("*** Press \"Enter\" to exit pyROOT: ")


######################################################################
# Function to make the plots:
def doPlots(datasets, histoDict, MyCuts, SaveExtension):
    ''' doPlots(datasets, histoDict, MyCuts, SaveExtension):
    This module takes the "histoDict" dictionary (which maps the histogram names and tree expressions)
    and the TCut expression "MyCuts" to first create and then plot the histograms, using the given "datasets". 
    The "SaveExtension" is the string attached to the name all plotted histograms, primarily to distinguish 
    the plot type.
    '''
    
    # Function to create the plots
    def createPlot(name, **kwargs):
        ''' createPlot(name, **kwargs):
    This module is used to create the histograms for the given "name". The user can pass 
    arguments including the histogram name, expression, labels, cut boxes etc..    
    '''
        p = plots.DataMCPlot(datasets, name, **kwargs)
        p.setDefaultStyles()
        return p

    print "\n*** Cuts to be applied: %s" % (MyCuts)
    
    # Function returns a progress bar object (pBar) and a CallBack(int, int) function
    maxValue = len(histoDict)
    print "*** Preparing %s histogram(s) for the given cut group" % (maxValue)

    # Create a progress bar to inform user of progress status
    pBar = StartProgressBar(maxValue)

    # Customise my plots
    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=True, ratio=False, addLuminosityText=True, ratioYlabel="Ratio", optsLog={"ymin": 1e-1}, opts2={"ymin": 0, "ymax": 2})

    # Define the tree to be used with the standard cuts
    MyTreeDraw = treeDraw.clone(selection=MyCuts)
    
    # Loop over all hName and expressions in the dictionary "histoDict"
    counter=0
    for hName in histoDict:
        #print "*** Plotted \"%s\": %s" % (hName, histoDict[hName])
        histo = MyTreeDraw.clone(varexp=histoDict[hName])
        drawPlot(createPlot(histo), "%s_%s" % (hName, SaveExtension), hName, ylabel="Events / %.1f ", cutBox={"cutValue":0.0, "greaterThan":True})

        # Increment counter and pdate progress bar
        counter = counter+1
        pBar.update(counter)
    
    # Stop pbar once done with the loop
    pBar.finish()


######################################################################
# This module creates a progress bar. Call it before executing a potentially long function/module.
def StartProgressBar(maxValue):
    ''' StartProgressBar(maxValue):
    Simple module to create and initialise a progress bar. The argument "maxvalue" refers to the 
    total number of tasks to be completed. This must be defined at the start of the progress bar.
    '''
    import progressbar
    widgets = [progressbar.FormatLabel(''), ' ', progressbar.Percentage(), ' ', progressbar.Bar('/'), ' ', progressbar.RotatingMarker()]
    pBar = progressbar.ProgressBar(widgets=widgets, maxval=maxValue)
    if pBar.start_time is None:
        pBar.start()
    return pBar

######################################################################
# Main function here
if __name__ == "__main__":
    main()

