#!/usr/bin/env python

######################################################################
#
# This plot script is for analysing the muon selection part of the EWK
# background measurement. The corresponding python job configuration
# is tauEmbedding/muonAnalysis_cfg.py.
#
# Author: Matti Kortelainen
#
######################################################################

import sys
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

def findSelection(lst, name):
    for n in lst:
        if name in n:
            return n
#    raise Exception("Did not find '%s' from the following list\n%s" % (name, "\n".join(lst)))
    return None

def replaceSelection(name, new):
    return name.split("_")[0]+"_"+new

class Selections:
    def __init__(self, analysisPrefix):
        self.topMuJetRefMet = [analysisPrefix+x for x in [
                "h00_AllMuons",
                "h01_Triggered",
                "h02_PrimaryVertex",
                "h03_GlobalTrackerMuon",
                "h04_MuonKin",
                "h05_MuonJetDR",
                "h06_MuonQuality",
                "h07_MuonIP",
                "h08_MuonIsolation",
                "h09_MuonVertexDiff",
                "h10_MuonVeto",
                "h11_ElectronVeto",
                "h12_JetMultiplicityCut",
                "h13_METCut"]]
        self.topMuJetRefMetAoc = []
        
        self.noIsoNoVetoMet = [analysisPrefix+x for x in [
                "h00_AllMuons",
                "h01_Triggered",
                "h02_PrimaryVertex",
                "h03_GlobalTrackerMuon",
                "h04_MuonKin",
                "h05_MuonJetDR",
                "h06_MuonQuality",
                "h07_MuonIP",
                "h08_MuonVertexDiff",
                "h09_JetMultiplicityCut",
                "h10_METCut"]]
        self.noIsoNoVetoMetAoc = [analysisPrefix+"Aoc"+x+"AfterOtherCuts" for x in [
                "h07_MuonLargestPt",
                "h08_JetMultiplicityCut",
                "h09_METCut"]]
        
        self.muonSelectionPF = [analysisPrefix+x for x in [
                "h00_AllMuons",
                "h01_Triggered",
                "h02_PrimaryVertex",
                "h03_GlobalTrackerMuon",
                "h04_MuonKin",
                "h05_MuonQuality",
                "h06_MuonIP",
                "h07_MuonVertexDiff",
        #        "h07_MuonLargestPt",
        #        "h07_JetSelection",
        #        "h07_JetId",
                "h08_MuonVeto",
                "h09_JetMultiplicityCut",
                "h10_METCut"]]
        self.muonSelectionPFAoc = [analysisPrefix+"Aoc"+x+"AfterOtherCuts" for x in [
                "h07_MuonLargestPt",
                "h08_JetMultiplicityCut",
                "h09_METCut"]]
        
        self.muonSelectionPFIsoTau = [analysisPrefix+x for x in [
                "h00_AllMuons",
                "h01_Triggered",
                "h02_PrimaryVertex",
                "h03_GlobalTrackerMuon",
                "h04_MuonKin",
                "h05_MuonQuality",
                "h06_MuonIP",
                "h07_MuonVertexDiff",
                "h08_MuonIsolationWithTau",
                "h09_MuonVeto",
                "h10_JetMultiplicityCut",
                "h11_METCut"
                ]]
        self.muonSelectionPFIsoTauAoc = [analysisPrefix+"Aoc"+x+"AfterOtherCuts" for x in [
                "h08_MuonLargestPt",
                "h09_JetMultiplicityCut",
                "h10_METCut"]]

        self.selections = self.noIsoNoVetoMet
        self.selectionsAoc = self.noIsoNoVetoMetAoc
        if "muonSelectionPF" in analysisPrefix:
            if "IsoTau" in analysisPrefix:
                self.selections = self.muonSelectionPFIsoTau
                self.selectionsAoc = self.muonSelectionPFIsoTauAoc
            else:
                self.selections = self.muonSelectionPF
                self.selectionsAoc = self.muonSelectionPFAoc
        elif "topMuJetRefMet" in analysisPrefix:
            self.selections = self.topMuJetRefMet
            self.selectionsAoc = self.topMuJetRefMetAoc
        
        self.selectionAll = self.selections[0]
        self.selectionTrigger = self.selections[1]
        self.selectionPrimaryVertex = self.selections[2]
        self.selectionMuon = findSelection(self.selections, "MuonVeto")
        self.selectionMuonIso = findSelection(self.selections, "MuonIsolation")
        self.selectionJetId = findSelection(self.selections, "JetId")
        self.selectionJet = findSelection(self.selections, "JetMultiplicityCut")
        self.selectionMet = findSelection(self.selections, "METCut")
        
        self.multipMuon = replaceSelection(self.selectionMuon, "Multiplicity")
        #multipMuonJetSelection = replaceSelection(selectionMuon, "MultiplicityAfterJetId")
        
        self.lastSelection = self.selections[-1]
        self.lastSelectionBeforeMet = self.selections[-2]
        self.lastSelectionOther = self.selectionsAoc[-1]
        self.lastSelectionOtherIso = self.selectionsAoc[-1]+"Iso"
        self.lastSelectionBeforeMetOther = self.selectionsAoc[-2]
        self.lastSelectionBeforeMetOtherIso = self.selectionsAoc[-2]+"Iso"
        
def main():
    #analysisPrefix = "noIsoNoVetoMetNJets3"
    #analysisPrefix = "noIsoNoVetoMetPFPt30Met20NJets3"
    #analysisPrefix = "topMuJetRefMet"
    analysisPrefix = "muonSelectionPFPt40Met20NJets3"
    #analysisPrefix = "muonSelectionPFPt40Met20NJets3IsoTau"
    sel = Selections(analysisPrefix)

    WdecaySeparate = False
    #WdecaySeparate = True

    datasets = dataset.getDatasetsFromMulticrabCfg(counters=analysisPrefix+"countAnalyzer")
    datasets.loadLuminosities()
    
    datasetsMC = datasets.deepCopy()
    datasetsMC.remove(datasets.getDataDatasetNames())
    
    plots.mergeRenameReorderForDataMC(datasets)
    
    styleGenerator = styles.generator(fill=True)
    wmunu = ["WJets", "TTJets", "SingleTop"]
    if WdecaySeparate:
        for i, name in enumerate(wmunu):
            d = datasets.getDataset(name)
            dc = d.deepCopy()
    
            d.setPrefix("WMuNu")
            dc.setPrefix("WOther")
            datasets.rename(name, name+"WMuNu")
            dc.setName(name+"WOther")
            datasets.append(dc)
            legendLabels[name+"WMuNu"] = legendLabels[name]+" (W#rightarrow#mu#nu)"
            legendLabels[name+"WOther"] = legendLabels[name]+" (W#rightarrow X)"
            del legendLabels[name]
            
        inds = range(0,len(wmunu)) + range(len(wmunu)+2, 2*len(wmunu)+2) + range(len(wmunu), len(wmunu)+2)
        styleGenerator.reorder(inds)
    
        wmunu = [x+"WMuNu" for x in wmunu] + [x+"WOther" for x in wmunu]
    
    #datasets.selectAndReorder(
    #    ["Data"] + wmunu + [
    #        "DYJetsToLL",
    #        "QCD_Pt20_MuEnriched"
    #])
    #datasets.selectAndReorder(["Data", "TTJets", "WJets", "QCD_Pt20_MuEnriched"])

    style = tdrstyle.TDRStyle()

    normalizeToLumi = None
    if not datasets.hasDataset("Data"):
        normalizeToLumi = 36

    def createPlot(name, **kwargs):
        return Plot(datasets, name, normalizeToLumi=normalizeToLumi, **kwargs)

    plotMet = PlotMet(datasets, rebin=5, normalizeToLumi=normalizeToLumi)
    
    #for sel in selections:
    #for sel in [selectionMuon, selectionJet, selectionMet]:
    #for isel, sel in enumerate([selectionMuon, selectionJetId, selectionJet, selectionMet]):
    for isel, sel in enumerate([sel.selectionJet]):
        if sel == None:
            continue
    
        prefix = sel+"_"
    
        printFraction = isel in [0, 2, 3]
    
        muonPt(createPlot(sel+"/muon_pt"), prefix)
        muonEta(createPlot(sel+"/muon_eta"), prefix)
        muonPhi(createPlot(sel+"/muon_phi"), prefix)
    
        isoPassed = []
        isoNames = ["sumIsoRel", "pfSumIsoRel"]
        for iso in isoNames:
            isoPassed.append(muonIso(createPlot(sel+"/muon_"+iso), prefix, iso, printFraction=printFraction))
        muonIsoQcd(PlotIso(isoPassed, isoNames), prefix)
    
        jetPt(createPlot(sel+"/jet_pt"), prefix)
    
        plotMet.plotLog("met", selection=sel)
    
        if isel > 0:
            wTransMass(createPlot(sel+"/wmumetPF_tmass"), prefix)
    
    #for sel in [multipMuon, multipMuonJetSelection]:
    #    prefix = sel+"_"
    #
    #    jetMultiplicity(createPlot(datasets, sel+"/jets_multiplicity"), prefix)
    
    
    # jetMultiplicity()
    # muonPt(createPlot(datasets, lastSelectionOther+"/pt"), lastSelectionOther+"_")
    # muonPt(createPlot(datasets, lastSelectionBeforeMetOther+"/pt"), lastSelectionBeforeMetOther+"_")
    # muonPt(createPlot(datasets, lastSelection+"/muon_pt"), lastSelection+"_")
    # muonEta(createPlot(datasets, lastSelection+"/muon_eta"), lastSelection+"_")
    # muonPhi(createPlot(datasets, lastSelection+"/muon_phi"), lastSelection+"_")
    # muonD0()
    # muonIso(createPlot(datasets, lastSelectionBeforeMetOtherIso+"/relIso"), lastSelectionBeforeMetOtherIso+"_")
    # muonIso(createPlot(datasets, lastSelectionOtherIso+"/relIso"), lastSelectionOtherIso+"_")
    # muonIso(createPlot(datasets, lastSelection+"/muon_relIso"), lastSelection+"_")
     
    # plotMet.plot("calomet")
    # plotMet.plot("pfmet")
    # plotMet.plot("tcmet")
    # plotMet.plot("pfmet", selection=lastSelectionBeforeMet, calcNumEvents=True)
    
    #for x in selections[:-1]:
    #for x in selections:
    #    plotMet.plotLog("pfmet", selection=x)
    #    #for met in ["calomet", "pfmet", "tcmet"]:
    #    #    plotMet.plotLog(met, selection=x)
    
    #for rebin in [1, 2, 4, 5, 8, 10, 15, 16, 20]:
    #    pm = PlotMet(rebin, postfix="%d"%rebin)
    #    for sel in [noIsoNoVetoMet[-3], lastSelectionBeforeMet]:
    #        pm.plotLog("pfmet", selection=sel)
    

    printCounters(datasets, datasetsMC, analysisPrefix, normalizeToLumi)

class SetTH1Directory:
    def __init__(self, value):
        self.value = value

    def __enter__(self):
        self.backup = ROOT.TH1.AddDirectoryStatus()
        ROOT.TH1.AddDirectory(self.value)

    def __exit__(self, type, value, traceback):
        ROOT.TH1.AddDirectory(self.backup)
        

class Plot(plots.PlotSameBase):
    def __init__(self, datasets, name, normalizeToLumi=None):
        plots.PlotSameBase.__init__(self, datasets, name,
#                                [".png"]
                                )

        if normalizeToLumi == None:
            self.histoMgr.normalizeMCByLuminosity()
        else:
            self.histoMgr.normalizeMCToLuminosity(normalizeToLumi)

        self._setLegendLabels()
        self._setLegendStyles()
        self._setPlotStyles()

class PlotPassed(plots.PlotBase):
    def __init__(self, plot):
        plots.PlotBase.__init__(self, [], plot.saveFormats)

        with SetTH1Directory(False):
            for histo in plot.histoMgr.getHistos():
                hpass = dist2pass(histo.getRootHisto())
                h = histograms.Histo(histo.getDataset(), hpass, histo.getName())
                self.histoMgr.appendHisto(h)
            self.histoMgr.setHistoDrawStyleAll("P")
            self.histoMgr.setHistoLegendStyleAll("P")
            self._setLegendLabels()
            self._setPlotStyles()

    def binWidth(self):
        return self.histoMgr.getHistos()[0].getBinWidth(1)

    def printFractions(self, bin):
        qcd = 0.0
        wjets = 0.0
        wjets_all = 0.0
        ttjets = 0.0
        ttjets_all = 0.0
        st = 0.0
        st_all = 0.0
        dyjets = 0.0
        dyjets_all = 0.0
        other = 0.0
        for histo in self.histoMgr.getHistos():
            if not histo.isMC():
                continue
            th1 = histo.getRootHisto()
            content = th1.GetBinContent(bin)
            nall = th1.GetBinContent(th1.GetNbinsX()+1) # number of all events is in the overflow bin
            if "QCD" in histo.getName():
                qcd += content
            elif "TTJets" in histo.getName():
                ttjets += content
                ttjets_all += nall
            elif "WJets" in histo.getName():
                wjets += content
                wjets_all += nall
            elif "SingleTop" in histo.getName():
                st += content
                st_all += nall
            elif "DYJets" in histo.getName():
                dyjets += content
                dyjets_all += content
            else:
                other += content

        cut = self.histoMgr.getHistos()[0].getRootHisto().GetBinCenter(bin)
        #print "Bin cut  TTJets WJets TT+W QCD Other TT+W/all QCD/all QCD/QCD/tt+w"
        #print "%d %f  %f %f %f %f %f %f %f %f" % (bin, cut, ttjets, wjets, (ttjets+wjets), qcd, other, ((ttjets+wjets)/(ttjets+wjets+qcd+other)), (qcd/(ttjets+wjets+qcd+other)), (qcd/(ttjets+wjets+qcd)))
        nall = ttjets+wjets+st+dyjets+qcd+other
#        print "Bin cut   TT_eff W_eff  TT+W/all  QCD/all"
#        print "%d %f   %f %f  %f %f" % (bin, cut, ttjets/ttjets_all, wjets/wjets_all, (ttjets+wjets)/nall, qcd/nall)
        
        print "Bin cut   TT W QCD  TT+W+ST/all  QCD/all  DY/all"
        print "%d %f   %f %f %f  %f %f %f" % (bin, cut, ttjets, wjets, qcd, (ttjets+wjets+st)/nall, qcd/nall, dyjets/nall)


def getSumOrRootHisto(histo):
    if hasattr(histo, "getSumRootHisto"):
        return histo.getSumRootHisto()
    else:
        return histo.getRootHisto()

class PlotIso(plots.PlotBase):
    def __init__(self, passedPlots, names, legendLabels={}):
        plots.PlotBase.__init__(self, [], passedPlots[0].saveFormats)

        legends = {
            "sumIsoRel": "Rel iso",
            "pfSumIsoRel": "PF rel iso",
        }
        legends.update(legendLabels)

        with SetTH1Directory(False):
            rootHistos = []
            for plot, name in zip(passedPlots, names):
                mcSum = histograms.sumRootHistos([getSumOrRootHisto(histo) for histo in filter(lambda h: not h.isMC(), plot.histoMgr.getHistos())])
                qcdHisto = plot.histoMgr.getHisto("QCD_Pt20_MuEnriched")
                qcd = getSumOrRootHisto(qcdHisto).Clone(name+"_QCDfraction")
                qcd.Divide(mcSum) # qcd/mcSum
                h = histograms.Histo(qcdHisto.getDataset(), qcd, name)
                h.setLegendLabel(legends.get(name, ""))
                self.histoMgr.appendHisto(h)

            self.histoMgr.forEachHisto(styles.generator())
            self.histoMgr.setHistoLegendStyleAll("l")
                
                                          


# dist = TH1
def dist2pass(hdist):
    # bin 0             underflow bin
    # bin 1             first bin
    # bin GetNbinsX()   last bin
    # bin GetNbinsX()+1 overflow bin

    # Construct the passed histogram such that the bin low edges in
    # the distribution histogram become the bin centers
    binLowEdges = []
    for bin in xrange(1, hdist.GetNbinsX()+3):
        prevBin = bin-1
        prevLowEdge = hdist.GetBinLowEdge(prevBin)
        thisLowEdge = hdist.GetBinLowEdge(bin)
        binLowEdges.append( (prevLowEdge+thisLowEdge)/2 )

    name = "passed_"+hdist.GetName()
    hpass = ROOT.TH1F(name, name, len(binLowEdges)-1, array.array("d", binLowEdges))

    #print "dist bins %d, pass bins %d" % (hdist.GetNbinsX(), hpass.GetNbinsX())

    #print ["%.4f" % i for i in binLowEdges]
    #print ["%.3f" % hdist.GetBinLowEdge(bin) for bin in xrange(1, hdist.GetNbinsX()+2)]
    #print ["%.3f" % hpass.GetBinCenter(bin) for bin in xrange(1, hpass.GetNbinsX()+1)]
    #for bin in xrange(1, hpass.GetNbinsX()):
    total = hdist.Integral(0, hdist.GetNbinsX()+1)
    #print "total %f" % total
    for bin in xrange(0, hdist.GetNbinsX()+2):
        passed = hdist.Integral(0, bin)
        #print "bin %d content %f, passed/total = %f/%f = %f" % (bin, hdist.GetBinContent(bin), passed, total, passed/total)
        hpass.SetBinContent(bin+1, passed)
    #print "bin N, N+1 %f, %f" % (hpass.GetBinContent(hpass.GetNbinsX()), hpass.GetBinContent(hpass.GetNbinsX()+1))
    return hpass

def jetMultiplicity(h, prefix=""):
    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"njets_log", ymin=0.1, yfactor=2)
    h.frame.GetXaxis().SetTitle("Jet multiplicity")
    h.frame.GetYaxis().SetTitle("Number of events")
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

def jetPt(h, prefix=""):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    xlabel = "Jet p_{T} (GeV/c)"
    ylabel = "Number of jets / %.1f GeV/c" % h.binWidth()

    ptcut = 30
    ymin = 4
    xmax = 400

    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"jet_pt_log", xmax=xmax, ymin=ymin, yfactor=2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

    h.createFrame(prefix+"jet_pt_log_cut%d"%ptcut, xmin=ptcut, xmax=xmax, ymin=ymin, yfactor=2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()
    


def muonPt(h, prefix="", plotAll=False):
    xlabel = "Muon p_{T} (GeV/c)"
    ylabel = "Number of muons / %.1f GeV/c"
    #ylabel = "Number of events / 5.0 GeV/c"
    ptcut = 30
    xmax = 400

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    ylabel = ylabel % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    if plotAll:
        h.createFrame(prefix+"muon_pt", xmax=xmax)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

        h.createFrame(prefix+"muon_pt_log", ymin=0.01, yfactor=2, xmax=xmax)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        ROOT.gPad.SetLogy(True)
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

        h.createFrame(prefix+"muon_pt_cut%d"%ptcut, xmin=ptcut, xmax=xmax, ymax=200)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    h.createFrame(prefix+"muon_pt_cut%d_log"%ptcut, xmin=ptcut, xmax=xmax, ymin=0.1, yfactor=2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()
    
def muonEta(h, prefix="", plotAll=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    xlabel = "Muon  #eta"
    ylabel = "Number of muons / %.1f" % h.binWidth()

    h.stackMCHistograms()
    
    if plotAll:
        h.createFrame(prefix+"muon_eta", yfactor=1.4)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    h.createFrame(prefix+"muon_eta_log", yfactor=2, ymin=0.1)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

def muonPhi(h, prefix="", plotAll=False):
#    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))

    xlabel = "Muon  #phi"
    ylabel = "Number of muons / %.1f" % h.binWidth()
    h.stackMCHistograms()

    if plotAll:
        h.createFrame(prefix+"muon_phi", yfactor=1.4)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    h.createFrame(prefix+"muon_phi_log", yfactor=2, ymin=0.1)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy()
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

def muonIso(h, prefix="", q="reliso", plotAll=False, printFraction=False):
    #rebin = 2
    rebin = 5

    #dist2pass(h.histoMgr.getHisto("QCD_Pt20_MuEnriched").getRootHisto())

    passed = PlotPassed(h)
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Muon rel. isol."
    ylabel = "Number of muons / %.3f" % h.binWidth()
    h.stackMCHistograms()

    if plotAll:
        h.createFrame(prefix+"muon_"+q)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    h.createFrame(prefix+"muon_%s_log" % q, ymin=1e-2, ymaxfactor=10)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    #h.setLegend(histograms.createLegend(0.72, 0.7, 0.92, 0.92))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

    passed.createFrame(prefix+"muon_%s_log_passed" % q, ymin=10, ymaxfactor=10)
    passed.frame.GetXaxis().SetTitle("Cut on "+xlabel)
    passed.frame.GetYaxis().SetTitle("Passed events")
    ROOT.gPad.SetLogy(True)
    passed.draw()
    passed.save()

    if printFraction:
        print "----------------------------------------"
        print "quantity %s" % q
        passed.printFractions(21)
        passed.printFractions(31)
        print "----------------------------------------"

    qcdFraction = PlotIso([passed], q)
    qcdFraction.createFrame(prefix+"muon_%s_qcdfraction" % q)
    qcdFraction.frame.GetXaxis().SetTitle("Cut on "+xlabel)
    qcdFraction.frame.GetYaxis().SetTitle("Fraction of QCD")
    qcdFraction.draw()
    qcdFraction.save()

    return passed

def muonIsoQcd(plot, prefix=""):
    plot.createFrame(prefix+"muon_qcdfraction")
    plot.frame.GetXaxis().SetTitle("Cut on isolation")
    plot.frame.GetYaxis().SetTitle("Fraction of QCD")
    plot.setLegend(histograms.createLegend(0.2, 0.8, 0.4, 0.9))
    plot.draw()
    plot.save()

def muonD0():
    # Muon track ip w.r.t. beam spot
    h = Plot(datasets, lastSelection+"/muon_trackDB")
    h.stackMCHistograms()
    h.createFrame(lastSelection+"_muon_trackdb", xmin=0, xmax=0.2, ymin=0.1)
    h.frame.GetXaxis().SetTitle("Muon track d_{0}(Bsp) (cm)")
    h.frame.GetYaxis().SetTitle("Number of muons")
    h.setLegend(histograms.createLegend(0.7, 0.5, 0.9, 0.8))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

def wTransMass(h, prefix=""):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    xlabel = "m_{T}(#mu, MET) (GeV/c)"
    ylabel = "Number of events / %.1f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"wtmass_log", ymin=0.1, yfactor=2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

class PrintNumEvents:
    def __init__(self, minMet):
        self.minMet = minMet
        self.results = {}
        #print "MET cut %d" % self.minMet

    def __call__(self, name, histo):
        th1 = histo.getRootHisto()

        bin = th1.FindBin(self.minMet)
        n = th1.Integral(bin, th1.GetNbinsX()+1)
        #print "Dataset %s: %.1f passes MET cut" % (name, n)
        self.results[name] = n

    def printQcdFraction(self):
        if not "QCD" in self.results:
            return

        s = 0.0
        for name, value in self.results.iteritems():
            if name != "Data":
                s += value

        print "MET cut %d" % self.minMet
        for name, value in self.results.iteritems():
            if name == "Data":
                print "Dataset %s: %.1f passes" % (name, value)
            else:
                print "Dataset %s: %.1f passes, %.1f %%" % (name, value, value/s*100)
                #print "Fraction of name of all MC %.1f %%" % (value/s*100)
        
# MET
class PlotMet:
    def __init__(self, datasets, normalizeToLumi=None, rebin=2, postfix=""):
        self.datasets = datasets
        self.normalizeToLumi = normalizeToLumi
        self.rebin = rebin
        self.postfix = postfix
        if len(postfix) > 0:
            self.postfix = "_"+self.postfix
        self.ylabel = "Number of events / %d.0 GeV" % self.rebin
        self.xlabels = {"calomet": "Calo MET",
                        "pfmet": "PF MET",
                        "met": "PF MET",
                        "tcmet": "TC MET"}

        self.ymax = 200
        self.xmax = 300
#        self.xmax = 100

    def xlabel(self, met):
        return self.xlabels[met]+" (GeV)"

    def _calculateNumEvents(self, h):
        for pn in [0, 15, 20, 30, 40]:
            pn = PrintNumEvents(pn)
            for name in [d.getName() for d in datasets.getAllDatasets()]:
                h.histoMgr.forHisto(name, lambda h: pn(name, h))
            pn.printQcdFraction()
            print

    def _plotLinear(self, h, selection, met):
        h.createFrame(selection+"_"+met+self.postfix, ymax=self.ymax, xmax=self.xmax)
        h.frame.GetXaxis().SetTitle(self.xlabel(met))
        h.frame.GetYaxis().SetTitle(self.ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    def _plotLog(self, h, selection, met):
        h.createFrame(selection+"_"+met+"_log"+self.postfix, ymin=0.1, yfactor=2, xmax=self.xmax)
        h.frame.GetXaxis().SetTitle(self.xlabel(met))
        h.frame.GetYaxis().SetTitle(self.ylabel)
        h.setLegend(histograms.createLegend())
        ROOT.gPad.SetLogy(True)
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    def _createPlot(self, met, selection, calcNumEvents=False):
        h = Plot(self.datasets, selection+"/%s_et" % met, normalizeToLumi=self.normalizeToLumi)
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(self.rebin))
        if calcNumEvents:
            self._calculateNumEvents(h)
        h.stackMCHistograms()
        return h

    def plot(self, met, selection, calcNumEvents=False):
        h = self._createPlot(met, selection, calcNumEvents)
        self._plotLinear(h, selection, met)
        h.removeLegend()
        self._plotLog(h, selection, met)

    def plotLog(self, met, selection):
        h = self._createPlot(met, selection)
        self._plotLog(h, selection, met)

############################################################

class PrefixModify:
    def __init__(self):
        self.remove = []
    def addPrefix(self, prefix):
        self.remove.append(prefix)

    def __call__(self, name):
        for r in self.remove:
            name = name.replace(r, "")
        return name

def makeEventCounter(ds):
    modifyCountNames = PrefixModify()
    for d in ds.getAllDatasets():
        prefix = d.getPrefix()
        if prefix != "":
            modifyCountNames.addPrefix(prefix)
    return counter.EventCounter(ds, modifyCountNames)

def addSumColumn(table):
    dataColumn = table.indexColumn("Data")

    indices = filter(lambda x: x != dataColumn, xrange(0, table.getNcolumns()))
    columns = [table.getColumn(i) for i in indices]
    table.insertColumn(1, counter.sumColumn("MCsum", columns))

def ttwSum(table):
    ttColumn = table.indexColumn("TTJets")
    wColumn = table.indexColumn("WJets")
    return counter.sumColumn("TTJets+WJets", [table.getColumn(i) for i in [ttColumn, wColumn]])

def signalSum(table):
    ttColumn = table.indexColumn("TTJets")
    wColumn = table.indexColumn("WJets")
    stColumn = table.indexColumn("SingleTop")
    return counter.sumColumn("TTJets+WJets+SingleTop", [table.getColumn(i) for i in [ttColumn, wColumn]])

def addTtwFractionColumn(table):
    ttColumn = table.indexColumn("TTJets")
    fraction = counter.divideColumn("TTJets/(TTJets+WJets)", table.getColumn(ttColumn), ttwSum(table))
    fraction.multiply(100) # -> %
    table.appendColumn(fraction)

def addQcdFractionColumn(table):
    qcdColumn = table.indexColumn("QCD_Pt20_MuEnriched")
    mcSumColumn = table.indexColumn("MCsum")
    fraction = counter.divideColumn("QCD/MCsum", table.getColumn(qcdColumn), table.getColumn(mcSumColumn))
    fraction.multiply(100) # -> %
    table.appendColumn(fraction)

def addDyFractionColumn(table):
    dyColumn = table.indexColumn("DYJetsToLL")
    mcSumColumn = table.indexColumn("MCsum")
    fraction = counter.divideColumn("DY/MCsum", table.getColumn(dyColumn), table.getColumn(mcSumColumn))
    fraction.multiply(100) # -> %
    table.appendColumn(fraction)

def addPurityColumn(table):
    mcSumColumn = table.indexColumn("MCsum")
    #purity = counter.divideColumn("TT+W purity", ttwSum(table), table.getColumn(mcSumColumn))
    purity = counter.divideColumn("Purity", signalSum(table), table.getColumn(mcSumColumn))
    purity.multiply(100) # -> %
    table.appendColumn(purity)

def addDataMcRatioColumn(table):
    dataColumn = table.indexColumn("Data")
    mcSumColumn = table.indexColumn("MCsum")
    ratio = counter.divideColumn("Data/MCsum", table.getColumn(dataColumn), table.getColumn(mcSumColumn))
    table.appendColumn(ratio)

def printCounters(datasets, datasetsMC, analysisPrefix, normalizeToLumi=None):
    print "============================================================"
    print "Dataset info: "
    datasets.printInfo()

    eventCounter = makeEventCounter(datasets)
    if normalizeToLumi == None:
        eventCounter.normalizeMCByLuminosity()
    else:
        eventCounter.normalizeMCToLuminosity(normalizeToLumi)
    
    mainCounterMap = {
        "allEvents": "All events",
        "passedTrigger": "Triggered",
        "passedScrapingVeto": "Scaping veto",
        "passedHBHENoiseFilter": "HBHE noise filter",
        "passedPrimaryVertexFilter": "PV filter",
        analysisPrefix+"countAll": "All events",
        analysisPrefix+"countTrigger": "Triggered",
        analysisPrefix+"countPrimaryVertex": "Good primary vertex",
        analysisPrefix+"countGlobalTrackerMuon": "Global \& tracker muon",
        analysisPrefix+"countMuonKin": "Muon \pT, $\eta$ cuts",
        analysisPrefix+"countMuonQuality": "Muon quality cuts",
        analysisPrefix+"countMuonIP": "Muon transverse IP",
        analysisPrefix+"countMuonVertexDiff": "Muon dz",
        analysisPrefix+"countJetMultiplicityCut": "Njets",
        analysisPrefix+"countMETCut": "MET cut"
        }
    
    latexFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.0f"))
    #latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.0f", valueOnly=True))
    
    print "============================================================"
    print "Main counter (%s)" % eventCounter.getNormalizationString()
    #eventCounter.getMainCounter().printCounter()
    table = eventCounter.getMainCounterTable()
    addSumColumn(table)
    addTtwFractionColumn(table)
    addPurityColumn(table)
    addDyFractionColumn(table)
    addQcdFractionColumn(table)
    print table.format()
    
    #print "------------------------------------------------------------"
    #print counterEfficiency(eventCounter.getMainCounterTable()).format(FloatDecimalFormat(4))
    
    # mainTable = eventCounter.getMainCounterTable()
    # effTable = counterEfficiency(mainTable)
    # for icol in xrange(0, effTable.getNcolumns()):
    #     column = effTable.getColumn(icol)
    #     column.setName(column.getName()+" eff")
    #     mainTable.insertColumn(icol*2+1, column)
    
    # print "------------------------------------------------------------"
    # printCounter(mainTable, FloatDecimalFormat(4))
    
    
    eventCounter = makeEventCounter(datasetsMC)
    print "============================================================"
    print "Main counter (%s)" % eventCounter.getNormalizationString()
    print eventCounter.getMainCounterTable().format(counter.TableFormatText(counter.CellFormatText(valueOnly=True, valueFormat="%.0f")))
    
    
    # Make the Data column entries comparable to the MC
    table.renameRows(mainCounterMap)
    dataCol = table.getColumn(0)
    table.removeColumn(0)
    dataCol.removeRow(2) # scraping
    dataCol.removeRow(2) # HBHE
    dataCol.removeRow(2) # pv filter
    dataCol.removeRow(2) # all events
    dataCol.removeRow(2) # triggered
    table.insertColumn(0, dataCol)
    addDataMcRatioColumn(table)
    
    # LaTeX tables for note
    latexFormat.setColumnFormat(counter.CellFormatTeX(valueFormat="%.3f"), name="Data/MCsum")
    latexFormat.setColumnFormat(counter.CellFormatTeX(valueFormat="%.1f"), name="SingleTop")
    
    tableDataMc = counter.CounterTable()
    tableDataMc.appendColumn(table.getColumn(name="Data"))
    tableDataMc.appendColumn(table.getColumn(name="MCsum"))
    tableDataMc.appendColumn(table.getColumn(name="Data/MCsum"))
    print tableDataMc.format(latexFormat)
    
    tableMc = counter.CounterTable()
    #tableMc.appendColumn(table.getColumn(name="MCsum"))
    for mcName in datasets.getMCDatasetNames():
        tableMc.appendColumn(table.getColumn(name=mcName))
    print tableMc.format(latexFormat)
    
    tableRatio = counter.CounterTable()
    for cname in ["TTJets/(TTJets+WJets)", "Purity", "QCD/MCsum", "DY/MCsum"]:
        tableRatio.appendColumn(table.getColumn(name=cname))
        latexFormat.setColumnFormat(counter.CellFormatTeX(valueFormat="%.2f", valueOnly=True), name=cname)
    print tableRatio.format(latexFormat)
    
    #tablettw = counter.CounterTable()
    #tablettw.appendColumn(ttwSum(table))
    #print tablettw.format(latexFormat)

if __name__ == "__main__":
    main()
