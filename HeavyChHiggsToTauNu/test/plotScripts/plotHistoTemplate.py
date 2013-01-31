#!/usr/bin/env python

######################################################################
# Title          : plotTest.py 
# Authors        : Ritva Kinnunen, Matti Kortelainen, Alexandros Attikis
# Description    : This is a test plotting script. 
######################################################################

import ROOT
ROOT.gROOT.SetBatch(False) #True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configurations
analysis = "signalAnalysis"
counters = analysis+"/counters"
treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")
dataEra = "Run2011A" #dataEra = "Run2011B" #dataEra = "Run2011AB"

# main function
def main():

    # Read the datasets
    #datasets = dataset.getDatasetsFromMulticrabDirs(["/home/attikis/scratch0/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/TreeAnalysis_v44_4_130113_105229/"], dataEra="Run2011A")
    datasets = dataset.getDatasetsFromMulticrabDirs(["/Volumes/disk/attikis/HIG-12-037/TreeAnalysis_v44_4_130113_105229/"], dataEra="Run2011A")

    datasets.loadLuminosities()
    datasets.updateNAllEventsToPUWeighted()    
    plots.mergeRenameReorderForDataMC(datasets)
    print "*** Int.Lumi",datasets.getDataset("Data").getLuminosity()
    print "*** norm=",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    # Create Legends
    histograms.createLegend.moveDefaults(dx=-0.02)
    histograms.createLegend.moveDefaults(dh=-0.03)
    datasets_lands = datasets.deepCopy()

    # Set the signal cross sections to the ttbar for datasets for lands
    xsect.setHplusCrossSectionsToTop(datasets_lands)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
    # xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    # Merge signals into one histo
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Print counters
    #doCounters(datasets)
    raw_input("*** Press \"Enter\" to exit pyROOT: ")
    

# Define plots to draw
def doPlots(datasets):
    def createPlot(name, **kwargs):
        return plots.DataMCPlot(datasets, analysis+"/"+name, **kwargs)
    
    drawPlot(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBJets", xlabel="Number of selected b jets", ylabel="Events", opts={"xmax": 6}, textFunction=lambda: addMassBRText(x=0.45, y=0.87), cutLine=1)
    pasJuly = "met_p4.Et() > 70 && Max$(jets_btag) > 1.7"
    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
    
def scaleMC(histo, scale):
    if histo.isMC():
        th1 = histo.getRootHisto()
        th1.Scale(scale)

def scaleMCHistos(h, scale):
    h.histoMgr.forEachHisto(lambda histo: scaleMC(histo, scale))

def scaleMCfromWmunu(h):
    scaleMCHistos(h, 1.0)

# Common drawing function
def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, addMCUncertainty=True, ratio=False, opts={}, opts2={}, moveLegend={}, textFunction=None, cutLine=None, cutBox=None):
    if cutLine != None and cutBox != None:
        raise Exception("Both cutLine and cutBox were given, only either one can exist")

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()

    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    if addMCUncertainty:
        h.addMCUncertainty()

    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts.update(opts)
    _opts2.update(opts2)    
    
    #if log:
    #    name = name + "_log"
    h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    if log:
        h.getPad().SetLogy(log)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    # Add cut line and/or box
    if cutLine != None:
        lst = cutLine
        if not isinstance(lst, list):
            lst = [lst]

        for line in lst:
            h.addCutBoxAndLine(line, box=False, line=True)
    if cutBox != None:
        lst = cutBox
        if not isinstance(lst, list):
            lst = [lst]

        for box in lst:
            h.addCutBoxAndLine(**box)

    common(h, xlabel, ylab, textFunction=textFunction)
    print "*** Saving %s" % (name)

# Common formatting
def common(h, xlabel, ylabel, addLuminosityText=True, textFunction=None):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    if textFunction != None:
        textFunction()
    h.save()

def tauCandPt(h, step="", rebin=2):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylabel = "Events /%.0f GeV/c" % h.binWidth()   
    xlabel = "p_{T}^{#tau candidate} (GeV/c)"
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           

    name = "tauCandidatePt_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()
    
def met(h, rebin=20, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "MET (GeV)"
    ylabel = "Events / %.0f GeV" % h.binWidth()

    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = "MET"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def transverseMass(h, rebin=20):
    name = flipName(h.getRootHistoPath())

    particle = ""
    if "Original" in name:
        particle = "#mu"
        name = name.replace("TransverseMass", "Mt")
    else:
        particle = "#tau jet"
        name = name.replace("TransverseMass", "Mt")

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(%s, MET) (GeV/c^{2})" % particle
    ylabel = "Events / %.2f GeV/c^{2}" % h.binWidth()
    
    scaleMCfromWmunu(h)     
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)#stackSignal=True)
    h.addMCUncertainty()

    opts = {"xmax": 200}

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
           
def numberOfJets(h, name, rebin=1, ratio=False):
    opts = {"ymin": 0.01,"xmax": 10.0, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.05, "ymax": 1.5}

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "BJets" in name:
        particle = "b jet"
        opts["xmax"] = 6
    xlabel = "Number of %ss" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.setLegend(histograms.createLegend(0.65, 0.65, 0.9, 0.92))
    common(h, xlabel, ylabel)

class AddMassBRText:
    def __init__(self):
        self.mass = 120
        self.br = 0.05
        self.size = 20
        self.separation = 0.04

    def setMass(self, mass):
        self.mass = mass

    def setBR(self, br):
        self.br = br

    def __call__(self, x, y):
        mass = "m_{H^{#pm}} = %d GeV/c^{2}" % self.mass
        br = "BR(t #rightarrow bH^{#pm})=%.2f" % self.br

        histograms.addText(x, y, mass, size=self.size)
        histograms.addText(x, y-self.separation, br, size=self.size)

addMassBRText = AddMassBRText()
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
