#!/usr/bin/env python

######################################################################
# Imports here
######################################################################
import sys
import array
import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

######################################################################
### Define my options and declaration here
######################################################################
bBatchMode = True
ROOT.gROOT.SetBatch(bBatchMode)

bPrintPSet = False
mcOnly = False
bMergeEwk = False
bLogY = True
bNormalizeToOne = True

if bNormalizeToOne:
    yMin = 10E-04
    #yMax = 1E+0
else: 
    yMin = 10E-01
    #yMax = 1E+0

yMinRatio = 0
yMaxRatio = 2
mcOnlyLumi = 2.3*1000 #(pb)
multicrabPath = ["/Volumes/disk/attikis/HIG-12-037/TreeAnalysis_v44_4_130113_105229/"]

######################################################################
### Per-event cuts: HIG-12-037 #HIG-11-019)
######################################################################
### Standalone cuts
MetCut = "met_p4.Pt() > 60" #"met_p4.Pt() > 50"
Mt = "TMath::Sqrt(2*tau_p4.Et()*met_p4.Et()*( 1.0 - ( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() )))"
MtCut = Mt + ">= 80"
BtagCut = "passedBTagging >= 1.0"
#TauIdCut = "passedTauId >= 1.0"
TauIsoCut = "tau_id_byMediumIsolation >= 1.0" #"tau_id_byTightIsolation >= 1.0"
DeltaPhi = "TMath::ACos(( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() ))*(180/TMath::Pi())"
DeltaPhiCut = DeltaPhi + "<= 160"
PlanarityCut = "planarity >= 0.1"
AplanarityCut = "aplanarity >= 0.1"
SphericityCut = "sphericity >= 0.5"
AlphaTCut = "alphaT >= 0.5"
CircularityCut = "circularity >= 0.1"
CircularityAntiCut = "circularity <= 0.1"
JetsEta = "jets_p4.Eta()";
NJets = "Sum$(abs(jets_p4.Eta()) < 3.0)";
NFwdJets = "Sum$(abs(jets_p4.Eta()) >= 1.0)"; #TEC start at eta>=1.0
NFwdJetsCut =  NFwdJets + "< 2";
#NBjetsPass = "Sum$(jets_btag > 1.7) >= 1";
Rtau = "tau_leadPFChargedHadrCand_p4.P() / tau_p4.P()";
RtauCut = Rtau + ">= 0.7";

### Cut combinations
JetSelectionCuts = ""
MetBtagDeltaPhiCuts = And(MetCut, BtagCut, DeltaPhiCut)
MetBtagDeltaPhiSpherCuts = And(MetCut, BtagCut, DeltaPhiCut, SphericityCut)
MetBtagDeltaPhiPlanCuts = And(MetCut, BtagCut, DeltaPhiCut, PlanarityCut)
MetBtagDeltaPhiAplanCuts = And(MetCut, BtagCut, DeltaPhiCut, AplanarityCut)
MetBtagDeltaPhiCircCuts = And(MetCut, BtagCut, DeltaPhiCut, CircularityCut)
MetBtagDeltaPhiAlphaTCuts = And(MetCut, BtagCut, DeltaPhiCut, AlphaTCut)
MetBtagDeltaPhiMtCuts = And(MetCut, BtagCut, DeltaPhiCut, MtCut)

######################################################################
### Define histogram name, expression, and binning here: 
### { hName": "expression >> hNameTmp(nBins, xMin, xMax) }
######################################################################
histoDict = {
    "NFwdJets": "%s >> NFwdJets(11, 0.5, 11.5)" % (NFwdJets),
    "sphericity": "sphericity >> sphericity(10, 0.05, 1.05)",
    "aplanarity": "aplanarity >> aplanarity(10, 0.0, 0.5)",
    "planarity": "planarity >> planarity(10, 0.0, 0.5)",
    "circularity": "circularity >> circularity(10, 0.05, 1.05)",
    "alphaT": "alphaT >> alphaT(10, 0.0, 2.0)", 
    "mT": "%s >> mT(30, 0.0, 600.0)" % (Mt),
    "DeltaPhi": "%s >> mT(18, 0.0, 180.0)" % (DeltaPhi),
    "JetsEta": "%s >> JetsEta(25, -2.5, 2.5)" % (JetsEta),
    "Rtau": "%s >> Rtau(10, 0.05, 1.05)" % (Rtau),
    "JetsArea": "jets_area >> jets_area(10, 0.0, 1.0)",
    "NJets": "%s >> NJets(11, 0.5, 11.5)" % (NJets)
    }

######################################################################
### Function declarations here
######################################################################
def main():

    ### Get the ROOT files for all datasets, merge datasets and reorder them
    print "*** Obtaining ROOT files from:\n    %s" % (multicrabPath)
    datasets = dataset.getDatasetsFromMulticrabDirs(multicrabPath, dataEra="Run2011A")

    printPSet(bPrintPSet, folderName="signalAnalysisRun2011A")

    print "*** Calling datasets.updateNAllEventsToPUWeighted():"
    datasets.updateNAllEventsToPUWeighted()
    print "*** Loading luminosities"
    datasets.loadLuminosities()    
    print "*** Calling plots.mergeRenameReorderForDataMC(datasets):"
    plots.mergeRenameReorderForDataMC(datasets)
    
    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION

    ### Merge desirable datasets
    if bMergeEwk:
        print "*** Merging EWK MC"
        datasets.merge("EWK MC", ["WJets", "TTJets", "DYJetsToLL", "SingleTop", "Diboson"])
        plots._plotStyles["EWK MC"] = styles.ttStyle  #plots._plotStyles["EWK"] = styles.getEWKStyle()
    
    ### Remove signals other than M120
    print "*** Removing all signal except M120"
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    ### Setup style
    print "*** Setting up style"
    styleGenerator = styles.generator(fill=True)
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.05, dy=+0.0)
    
    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    print "*** Setting the signal cross sections to a given BR(t->bH+) and BR(H+ -> tau+ nu)"
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.01, br_Htaunu=1)

    ### Merge signals into one histo
    print "*** Merging WH and HH signals into one histogram"
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    ### Print desirable information here
    print "*** Available datasets:\n    %s" % (datasets.getAllDatasetNames())
    if mcOnly:
        print "*** Integrated Luminosity:\n    %s (pb)" % (mcOnlyLumi)
    else:
        print "*** Integrated Luminosity:\n     %s (pb)" % (datasets.getDataset("Data").getLuminosity())

    ### Do all plots defined in histoDict function
    doPlots(datasets, histoDict, JetSelectionCuts, SaveExtension = "JetSelection_Validation")
    #doPlots(datasets, histoDict, MetBtagDeltaPhiCuts, SaveExtension = "MetBtagDeltaPhi")
    #doPlots(datasets, histoDict, MetBtagDeltaPhiMtCuts, SaveExtension = "MetBtagDeltaPhiMt")
    #doPlots(datasets, histoDict, MtCut, SaveExtension = "Mt")
    #doPlots(datasets, histoDict, MetBtagDeltaPhiCircCuts, SaveExtension = "MetBtagDeltaPhiCirc")
    #doPlots(datasets, histoDict, MetBtagDeltaPhiSpherCuts, SaveExtension = "MetBtagDeltaPhiSpher")
    #doPlots(datasets, histoDict, MetBtagDeltaPhiAplanCuts, SaveExtension = "MetBtagDeltaPhiAplan")
    #doPlots(datasets, histoDict, MetBtagDeltaPhiPlanCuts, SaveExtension = "MetBtagDeltaPhiPlan")
    #doPlots(datasets, histoDict, MetBtagDeltaPhiAlphaTCuts, SaveExtension = "MetBtagDeltaPhiAlphaT")
    
    ### Keep session alive (otherwise canvases close automatically)
    if bBatchMode == False:
        raw_input("*** Press \"any\" key to exit pyROOT: ")


######################################################################
def doPlots(datasets, histoDict, MyCuts, SaveExtension):
    ''' doPlots(datasets, histoDict, MyCuts, SaveExtension):
    This module takes the "histoDict" dictionary (which maps the histogram names and tree expressions)
    and the TCut expression "MyCuts" to first create and then plot the histograms, using the given "datasets". 
    The "SaveExtension" is the string attached to the name all plotted histograms, primarily to distinguish 
    the plot type.
    '''
    
    def createPlot(name, **kwargs):
        ''' createPlot(name, **kwargs):
    This module is used to create the histograms for the given "name". The user can pass 
    arguments including the histogram name, expression, labels, cut boxes etc..    
    '''
        if mcOnly:
            ### If 'normalizeToOne' is given in kwargs, we don't need the normalizeToLumi (or actually the library raises an Exception)
            args = {}
            args.update(kwargs)
            if not ("normalizeToOne" in args and args["normalizeToOne"]):
                args["normalizeToLumi"] = mcOnlyLumi
            p = plots.MCPlot(datasets, name, **args)
            p.histoMgr.setHistoLegendStyleAll("L")
            return p
        else:
            p = plots.DataMCPlot(datasets, name, **kwargs)
            return p
        p.setDefaultStyles()
        return p

    ### Function returns a progress bar object (pBar) and a CallBack(int, int) function
    maxValue = len(histoDict)
    print "\n*** Preparing %s histogram(s) for the cut group:\n    %s" % (maxValue, MyCuts)

    ### Create a progress bar to inform user of progress status
    pBar = StartProgressBar(maxValue)

    ### Customise my plots
    if mcOnly:
        drawPlot = plots.PlotDrawer(stackMCHistograms=False, addMCUncertainty=True, log=bLogY, ratio=False, addLuminosityText= not bNormalizeToOne, ratioYlabel="Ratio", optsLog={"ymin": yMin}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio})
    else:
        drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=bLogY, ratio=True, addLuminosityText=True, ratioYlabel="Ratio", optsLog={"ymin": yMin}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio})


    ### Define the tree to be used with the given cuts
    if "passedBTagging" in MyCuts:
        EvtWeight = "(weightPileup*weightTrigger*weightPrescale*weightBTagging)"
    else:
        EvtWeight = "weightPileup*weightTrigger*weightPrescale"
    print "*** Drawing tree with event weight:\n    %s" % (EvtWeight)
    treeDraw = dataset.TreeDraw("signalAnalysis/tree", weight=EvtWeight)
    MyTreeDraw = treeDraw.clone(selection=MyCuts)
    
    ### Loop over all hName and expressions in the dictionary "histoDict"
    counter=0
    for hName in histoDict:
        #print "*** Plotting \"%s\": %s" % (hName, histoDict[hName])
        histo = MyTreeDraw.clone(varexp=histoDict[hName])
        if mcOnly:
            if bNormalizeToOne:
                drawPlot(createPlot(histo, normalizeToOne = bNormalizeToOne), "%s_%s" % (hName, SaveExtension+"_Normalised"), hName, ylabel="Events / %.2f ")
                #, cutBox={"cutValue":0.0, "greaterThan":True})
            else:
                drawPlot(createPlot(histo, normalizeToOne = bNormalizeToOne), "%s_%s" % (hName, SaveExtension), hName, ylabel="Events / %.2f ")
            #, cutBox={"cutValue":0.0, "greaterThan":True})
        else:
            if bNormalizeToOne:
                drawPlot(createPlot(histo, normalizeToOne = False), "%s_%s" % (hName, SaveExtension+"_Normalised"), hName, ylabel="Events / %.2f ")
            #, cutBox={"cutValue":0.0, "greaterThan":True})
            else:
                drawPlot(createPlot(histo, normalizeToOne = False), "%s_%s" % (hName, SaveExtension), hName, ylabel="Events / %.2f ")
        # Increment counter and pdate progress bar
        counter = counter+1
        pBar.update(counter)
    
    ### Stop pbar once done with the loop
    pBar.finish()
    return

######################################################################
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
def printPSet(bPrintPset, folderName="signalAnalysis"):
    '''
    def printPSet():
    Simple module that prints the parameters set in running the analysis
    '''
    if bPrintPset:
        from ROOT import gROOT
        gDirectory = gROOT.GetGlobal("gDirectory")
        named = gDirectory.Get("%s/parameterSet" % (folderName))
        print named.GetTitle()
        raw_input("*** Press \"any\" key to continue: ")
    else:
        return;

######################################################################
### Main function here
if __name__ == "__main__":
    main()
