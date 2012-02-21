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
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

# These are per-muon cuts
muonKinematics = "(muons_p4.Pt() > 40 && abs(muons_p4.Eta()) < 2.1)"
muondB = "(abs(muons_f_dB) < 0.02)"
muonIsolation = "((muons_f_tauTightIc04ChargedIso + muons_f_tauTightIc04GammaIso) == 0)"
muonSelection = "(%s && %s && %s)" % (muonKinematics, muondB, muonIsolation)
muonSelectionNoIso = "(%s && %s)" % (muonKinematics, muondB)

# Construct muon veto, first the muons accepted as veto muons
muonVeto = "muons_p4.Pt() > 15 && abs(muons_p4.Eta()) < 2.5 && abs(muons_f_dB) < 0.02 && (muons_f_trackIso+muons_f_caloIso)/muons_p4.Pt() <= 0.15"
# then exclude the selected muon (this will work only after the 'one selected muon' requirement)
muonVetoNoIso = muonVeto + " && !"+muonSelectionNoIso
muonVeto += " && !"+muonSelection
# then make it a sum cut
muonVeto = "Sum$(%s) == 0" % muonVeto
muonVetoNoIso = "Sum$(%s) == 0" % muonVetoNoIso

electronVeto = "ElectronVetoPassed"

# Jet selection as per-event cut
#jetSelection = "(jets_p4.Pt() > 30 && abs(jets_p4.Eta()) < 2.4 && jets_looseId)"
# Jet cleaning
#jetSelection += ""
# Construct per-event cut
#jetSelection = "Sum$(%s) >= 3" % jetSelection
jetSelection = "jets_p4@.size() >= (3+Sum$(%s && muons_jetMinDR < 0.1))" % muonSelection
jetSelectionNoIso = "jets_p4@.size() >= (3+Sum$(%s && muons_jetMinDR < 0.1))" % muonSelectionNoIso

metcut = "pfMet_p4.Pt() > 40"

btagging = "Sum$(jets_f_tche > 1.7 && sqrt((jets_p4.Phi()-muons_p4.Phi())^2+(jets_p4.Eta()-muons_p4.Eta())^2) > 0.5) >= 1"

analysis = "muonNtuple"

#era = "EPS"
#era = "Run2011A-EPS"
era = "Run2011A"

weight = {"EPS": "pileupWeightEPS",
          "Run2011A-EPS": "weightPileup_Run2011AnoEPS",
          "Run2011A": "weightPileup_Run2011A",
          }[era]
#weight = ""

treeDraw = dataset.TreeDraw(analysis+"/tree", weight=weight)

def main():
    counters = analysis+"Counters"
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    tauEmbedding.updateAllEventsToWeighted(datasets)

    #datasets.remove(filter(lambda name: name != "SingleMu_Mu_166374-167043_Prompt" and name != "TTJets_TuneZ2_Summer11", datasets.getAllDatasetNames()))
    if era == "EPS":
        datasets.remove([
            "SingleMu_Mu_170722-172619_Aug05",
            "SingleMu_Mu_172620-173198_Prompt",
            "SingleMu_Mu_173236-173692_Prompt",
        ])
    elif era == "Run2011A-EPS":
        datasets.remove([
            "SingleMu_Mu_160431-163261_May10",
            "SingleMu_Mu_163270-163869_May10",
            "SingleMu_Mu_165088-166150_Prompt",
            "SingleMu_Mu_166161-166164_Prompt",
            "SingleMu_Mu_166346-166346_Prompt",
            "SingleMu_Mu_166374-167043_Prompt",
            "SingleMu_Mu_167078-167913_Prompt",

#            "SingleMu_Mu_170722-172619_Aug05",
#            "SingleMu_Mu_172620-173198_Prompt",
#            "SingleMu_Mu_173236-173692_Prompt",
            ])
    elif era == "Run2011A":
        pass

    #datasets.remove(datasets.getMCDatasetNames())
    datasets.loadLuminosities()

    #datasetsMC = datasets.deepCopy()
    #datasetsMC.remove(datasets.getDataDatasetNames())
    
    plots.mergeRenameReorderForDataMC(datasets)
    
    styleGenerator = styles.generator(fill=True)

    style = tdrstyle.TDRStyle()
    #histograms.createLegend.moveDefaults(dx=-0.15)
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dx=-0.02)

    doPlots(datasets)
    printCounters(datasets)
#    doPlotsWTauMu(datasets, "TTJets")
#    doPlotsWTauMu(datasets, "WJets")


def doPlots(datasets):
    def createPlot(name, **kwargs):
        return plots.DataMCPlot(datasets, name, **kwargs)

    selections = [
        ("Full_", And(muonSelection, muonVeto, electronVeto, jetSelection)),
        ("FullNoIso_", And(muonSelectionNoIso, muonVetoNoIso, electronVeto, jetSelectionNoIso)),
#        ("Analysis_", "&&".join([muonSelection, muonVeto, electronVeto, jetSelection, metcut, btagging])),
        ]

    for name, selection in selections:
        tdMuon = treeDraw.clone(selection=selection)


        td = tdMuon.clone(varexp="muons_p4.Pt() >>tmp(40,0,400)")
        muonPt(createPlot(td), prefix=name, ratio=True, cutBox={"cutValue":40, "greaterThan":True})

        td = tdMuon.clone(varexp="pfMet_p4.Pt() >>tmp(40,0,400)")
        met(createPlot(td), prefix=name, ratio=True)

        td = tdMuon.clone(varexp="sqrt(2 * muons_p4.Pt() * pfMet_p4.Et() * (1-cos(muons_p4.Phi()-pfMet_p4.Phi()))) >>tmp(40,0,400)")
        transverseMass(createPlot(td), prefix=name, ratio=True)


def doPlotsWTauMu(datasets, name):
    selection = And(muonSelection, muonVeto, electronVeto, jetSelection)
    td = treeDraw.clone(varexp="muons_p4.Pt() >> tmp(40,0,400)")

    ds = datasets.getDataset(name)
    # Take first unweighted histograms for the fraction plot
    drh_all = ds.getDatasetRootHisto(td.clone(selection=selection, weight=""))
    drh_pure = ds.getDatasetRootHisto(td.clone(selection=And(selection, "abs(muons_mother_pdgid) == 24"), weight=""))
    hallUn = drh_all.getHistogram()
    hpureUn = drh_pure.getHistogram()

    # Then the correctly weighted for the main plot
    drh_all = ds.getDatasetRootHisto(td.clone(selection=selection))
    drh_pure = ds.getDatasetRootHisto(td.clone(selection=And(selection, "abs(muons_mother_pdgid) == 24")))
    lumi = datasets.getDataset("Data").getLuminosity()
    drh_all.normalizeToLuminosity(lumi)
    drh_pure.normalizeToLuminosity(lumi)
    hall = drh_all.getHistogram()
    hpure = drh_pure.getHistogram()

    hall.SetName("All")
    hpure.SetName("Pure")

    p = plots.ComparisonPlot(hall, hpure)
    p.histoMgr.setHistoLegendLabelMany({
            "All": "All muons",
            "Pure": "W#rightarrow#tau#rightarrow#mu"
#            "Pure": "W#rightarrow#mu"
            })
    p.histoMgr.forEachHisto(styles.generator())

    hallErr = hall.Clone("AllError")
    hallErr.SetFillColor(ROOT.kBlue-7)
    hallErr.SetFillStyle(3004)
    hallErr.SetMarkerSize(0)
    p.prependPlotObject(hallErr, "E2")

    hpureErr = hpure.Clone("PureErr")
    hpureErr.SetFillColor(ROOT.kRed-7)
    hpureErr.SetFillStyle(3005)
    hpureErr.SetMarkerSize(0)
    p.prependPlotObject(hpureErr, "E2")

    p.createFrame("muonPt_wtaumu_"+name, createRatio=True, opts={"ymin": 1e-1, "ymaxfactor": 2}, opts2={"ymin": 0.9, "ymax": 1.05}
                  )
    p.setRatios([plots._createRatio(hpureUn, hallUn, "", isBinomial=True)])
    xmin = p.frame.GetXaxis().GetXmin()
    xmax = p.frame.GetXaxis().GetXmax()
    val = 1-0.038479
    l = ROOT.TLine(xmin, val, xmax, val)
    l.SetLineWidth(2)
    l.SetLineColor(ROOT.kBlue)
    l.SetLineStyle(4)
    p.prependPlotObjectToRatio(l)
    #p.appendPlotObjectToRatio(histograms.PlotText(0.18, 0.61, "1-0.038", size=18, color=ROOT.kBlue))
    p.appendPlotObjectToRatio(histograms.PlotText(0.18, 0.61, "0.038", size=18, color=ROOT.kBlue))
    p.getFrame2().GetYaxis().SetTitle("W#rightarrow#mu fraction")

    p.getPad().SetLogy(True)
    p.setLegend(histograms.moveLegend(histograms.createLegend()))
    tmp = hpureErr.Clone("tmp")
    tmp.SetFillColor(ROOT.kBlack)
    tmp.SetFillStyle(3013)
    tmp.SetLineColor(ROOT.kWhite)
    p.legend.AddEntry(tmp, "Stat. unc.", "F")

    p.frame.GetXaxis().SetTitle("Muon p_{T} (GeV/c)")
    p.frame.GetYaxis().SetTitle("Events / %.0f GeV/c" % p.binWidth())
    p.appendPlotObject(histograms.PlotText(0.5, 0.9, plots._legendLabels.get(name, name), size=18))

    p.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    p.save()


def printCounters(datasets):
    print "============================================================"
    print "Dataset info: "
    datasets.printInfo()

    eventCounter = counter.EventCounter(datasets)
    if True:
        selection = "Sum$(%s) >= 1" % muonKinematics
        eventCounter.getMainCounter().appendRow("Muon kinematics", treeDraw.clone(selection=selection))
        selection = "Sum$(%s && %s) >= 1" % (muonKinematics, muondB)
        eventCounter.getMainCounter().appendRow("Muon IP", treeDraw.clone(selection=selection))
        selection = "Sum$(%s && %s && %s) >= 1" % (muonKinematics, muondB, muonIsolation)
        eventCounter.getMainCounter().appendRow("Muon isolation", treeDraw.clone(selection=selection))
        selection = "Sum$(%s && %s && %s) == 1" % (muonKinematics, muondB, muonIsolation)
        print selection
        eventCounter.getMainCounter().appendRow("One selected muon", treeDraw.clone(selection=selection))
        selection += "&&" +muonVeto
        print selection
        eventCounter.getMainCounter().appendRow("Muon veto", treeDraw.clone(selection=selection))
        selection += "&&" +electronVeto
        print selection
        eventCounter.getMainCounter().appendRow("Electron veto", treeDraw.clone(selection=selection))
        selection += "&&" +jetSelection
        print selection
        eventCounter.getMainCounter().appendRow("Jet selection", treeDraw.clone(selection=selection))

    eventCounter.normalizeMCByLuminosity()

    table = eventCounter.getMainCounterTable()
    addSumColumn(table)

    cellFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%.3f'))
    print table.format(cellFormat)





class SetTH1Directory:
    def __init__(self, value):
        self.value = value

    def __enter__(self):
        self.backup = ROOT.TH1.AddDirectoryStatus()
        ROOT.TH1.AddDirectory(self.value)

    def __exit__(self, type, value, traceback):
        ROOT.TH1.AddDirectory(self.backup)
        

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
        diboson = 0.0
        
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
            elif "Diboson" in histo.getName():
                diboson += content
            else:
                other += content

        cut = self.histoMgr.getHistos()[0].getRootHisto().GetBinCenter(bin)
        #print "Bin cut  TTJets WJets TT+W QCD Other TT+W/all QCD/all QCD/QCD/tt+w"
        #print "%d %f  %f %f %f %f %f %f %f %f" % (bin, cut, ttjets, wjets, (ttjets+wjets), qcd, other, ((ttjets+wjets)/(ttjets+wjets+qcd+other)), (qcd/(ttjets+wjets+qcd+other)), (qcd/(ttjets+wjets+qcd)))
        nall = ttjets+wjets+st+dyjets+qcd+diboson+other
#        print "Bin cut   TT_eff W_eff  TT+W/all  QCD/all"
#        print "%d %f   %f %f  %f %f" % (bin, cut, ttjets/ttjets_all, wjets/wjets_all, (ttjets+wjets)/nall, qcd/nall)
        
        print "Bin cut   TT W QCD  TT+W+ST/all  QCD/all  DY/all"
        print "%d %f   %f %f %f  %f %f %f" % (bin, cut, ttjets, wjets, qcd, (ttjets+wjets+st)/nall, qcd/nall, dyjets/nall)

        print "Bin cut   sum W TT ST QCD DY DiB other"
        print "%d %f    %.0f %.0f %.0f %.0f %.0f %.0f %.0f %f" % (bin, cut, nall, wjets, ttjets, st, qcd, dyjets, diboson, other)
        print "Bin cut   sum W TT ST QCD DY DiB other"
        print "%d %f    \\bTD %.0f \\eTD\\bTD %.0f \\eTD\\bTD %.0f \\eTD\\bTD %.0f \\eTD\\bTD %.0f \\eTD\\bTD %.0f \\eTD\\bTD %.0f \\eTD\\bTD %f \\eTD" % (bin, cut, nall, wjets, ttjets, st, qcd, dyjets, diboson, other)


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
                mcSum = histograms.sumRootHistos([getSumOrRootHisto(histo) for histo in filter(lambda h: h.isMC(), plot.histoMgr.getHistos())])
                qcdHisto = plot.histoMgr.getHisto("QCD_Pt20_MuEnriched")
                qcd = getSumOrRootHisto(qcdHisto).Clone(name+"_QCDfraction")
                qcd.Divide(mcSum) # qcd/mcSum
                h = histograms.Histo(qcdHisto.getDataset(), qcd, name)
                h.setLegendLabel(legends.get(name, ""))
                self.histoMgr.appendHisto(h)

            self.histoMgr.forEachHisto(styles.generator())
            self.histoMgr.setHistoLegendStyleAll("l")

# class PlotIsoBase(plots.PlotBase):
#     def __init__(self, saveFormats, legendLabels={}):
#         plots.PlotBase.__init__(self, [], saveFormats)
#         self.legends = {
#             "sumIsoRel": "Rel iso",
#             "pfSumIsoRel": "PF rel iso",
#         }
#         self.legends.update(legendLabels)

#     def _sumRootHisto(plot, func):
#         return histograms.sumRootHistos([getSumOrRootHisto(histo) for histo in filter(func, plot.histoMgr.getHistos())])

#     def _mcSum(plot):
#         return self._sumRootHisto(plot, lambda h: not h.isMC())

# class PlotIsoSignal(plots.PlotBase):
#     def __init__(self, passedPlots, names, **kwargs):

#         plots.PlotBase(passedPlots[0].saveFormats, **kwargs)
#         with SetTH1Directory(False):
#             for plot, name in zip(passedPlots, names):
#                 mcSum = self._mcSum(plot)

#                 signalDatasets = ["TTJets", "WJets", "SingleTop"]
#                 signalSum = self._sumRootHisto(plot, lambda h: h.getName() in signalDatasets)

#                 signal = signalSum.Clone(name+"_signal_fraction")
#                 signal.Divide(mcSum) # signal/mcSum
#                 h = histograms.Histo(theHisto.getDataset(), th1, name)
#                 h.setLegendLabel(self.legends.get(name, ""))
#                 self.histoMgr.appendHisto(h)

#                 self.histoMgr.forEachHisto(styles.generator())
#                 self.histoMgr.setHistoLegendStyleAll("l")

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

def dist2eff(hdist):
    hpass = dist2pass(hdist)
    total = hdist.Integral(0, hdist.GetNbinsX()+1)
    for bin in xrange(0, hdist.GetNbinsX()+2):
        hpass.SetBinContent(bin, hpass.GetBinContent(bin)/total)
    return hpass

def dist2rej(hdist):
    hpass = dist2pass(hdist)
    total = hdist.Integral(0, hdist.GetNbinsX()+1)
    for bin in xrange(0, hdist.GetNbinsX()+2):
        hpass.SetBinContent(bin, 1-hpass.GetBinContent(bin)/total)
    return hpass

def jetMultiplicity(h, prefix=""):
    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"njets_log", xmin=3, xmax=10, ymin=0.1, yfactor=2)
    h.frame.GetXaxis().SetTitle("Jet multiplicity")
    h.frame.GetYaxis().SetTitle("Number of events")
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

def jetPt(h, prefix="", rebin=10):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Jet p_{T} (GeV/c)"
    ylabel = "Number of jets / %.0f GeV/c" % h.binWidth()

    ptcut = 30
    ymin = 1e-1
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
    

def vertexCount(h, prefix="", postfix=""):
    xlabel = "Number of vertices"
    ylabel = "Number of events"

    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"vertices"+postfix)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

    h.createFrame(prefix+"vertices"+postfix+"_log", ymin=0.1, factor=2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()
    


def muonPt(h, prefix="", rebin=1, ratio=False, cutBox=None):
    xlabel = "Muon p_{T} (GeV/c)"
    ylabel = "Events / %.0f GeV/c"
    #ylabel = "Number of events / 5.0 GeV/c"

    _optsLin  = {}
    _optsLog  = {"ymin": 0.1, "ymaxfactor": 2}
    _opts2 = {"ymin": 0, "ymax": 2}

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylabel = ylabel % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

#    tmp = h.histoMgr.getHisto("Data").getRootHisto()
#    dataEvents = tmp.Integral(0, tmp.GetNbinsX()+1)
#    tmp = h.histoMgr.getHisto("StackedMC").getSumRootHisto()
#    mcEvents = tmp.Integral(0, tmp.GetNbinsX()+1)
#    print "Muon pt Data/MC = %f/%f = %f" % (dataEvents, mcEvents, dataEvents/mcEvents)

    h.createFrame(prefix+"muon_pt", opts=_optsLin)
    if cutBox != None:
        h.addCutBoxAndLine(**cutBox)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

    h.createFrame(prefix+"muon_pt_log", createRatio=ratio, opts=_optsLog, opts2=_opts2)
    if cutBox != None:
        h.addCutBoxAndLine(**cutBox)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.moveLegend(histograms.createLegend()))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()
    
def muonEta(h, prefix="", plotAll=False, rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
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

def muonPhi(h, prefix="", plotAll=False, rebin=1):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

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

def muonIso(h, prefix="", q="reliso", plotAll=False, ratio=False, printFraction=False, rebin=5, opts={}, opts2={}):
    #dist2pass(h.histoMgr.getHisto("QCD_Pt20_MuEnriched").getRootHisto())

    passed = PlotPassed(h)
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = {"sumIsoRel": "Muon rel. iso",
              "sumIsoRelFull": "Muon rel. iso",
              "pfSumIsoRel": "Muon PF rel. iso",
              "pfSumIsoRelFull": "Muon PF rel. iso",
              "tauTightIso": "N(PFCand) in iso annulus",
              "tauTightSc015Iso": "N(PFCand) in iso annulus",
              "tauTightSc02Iso": "N(PFCand) in iso annulus",
              "tauTightIc04Iso": "N(PFCand) in iso annulus",
              "tauTightIc04ChargedIso": "N(PFChargedCand) in iso annulus",
              "tauTightIc04GammaIso": "N(PFGammaCand) in iso annulus",
              "tauTightIc04SumPtIso": "#Sigma p_{T} in iso annulus (GeV/c)",
              "tauTightIc04MaxPtIso": "max(p_{T}) in iso annulus (GeV/c)",
              "tauTightSc015Ic04Iso": "N(PFCand) in iso annulus",
              "tauTightSc02Ic04Iso": "N(PFCand) in iso annulus",
              "tauMediumIso": "Tau-like medium occupancy",
              "tauLooseIso": "Tau-like loose occupancy",
              "tauVLooseIso": "Tau-like vloose occupancy",
              }[q]
    bw = h.binWidth()
    if bw < 1:
        ylabel = "Number of muons / %.3f" % bw
#    elif int(bw) == 1:
#        ylabel = "Number of muons"
    else:
        ylabel = "Number of muons / %.0f" % bw
    
    h.stackMCHistograms()

    if plotAll:
        h.createFrame(prefix+"muon_"+q, createRatio=ratio)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    _opts = {"ymin": 1e-2, "ymaxfactor": 10}
    _opts.update(opts)
    _opts2 = {"ymin": 0, "ymax": 2}
    _opts2.update(opts2)

    h.createFrame(prefix+"muon_%s_log" % q, createRatio=ratio, opts=_opts, opts2=_opts2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
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
        passed.printFractions(101)
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
    plot.setLegend(histograms.createLegend())
    plot.draw()
    plot.save()

    plot.createFrame(prefix+"muon_qcdfraction_zoom", xmax=0.2, ymax=0.1)
    plot.frame.GetXaxis().SetTitle("Cut on isolation")
    plot.frame.GetYaxis().SetTitle("Fraction of QCD")
    plot.setLegend(histograms.createLegend())
    plot.draw()
    plot.save()

    

def muonD0():
    # Muon track ip w.r.t. beam spot
    h = Plot(datasets, lastSelection+"/muon_trackDB")
    h.stackMCHistograms()
    h.createFrame(lastSelection+"_muon_trackdb", xmin=0, xmax=0.2, ymin=0.1)
    h.frame.GetXaxis().SetTitle("Muon track d_{0}(Bsp) (cm)")
    h.frame.GetYaxis().SetTitle("Number of muons")
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

def wTransMass(h, prefix="", rebin=10):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    xlabel = "m_{T}(#mu, MET) (GeV/c)"
    ylabel = "Number of events / %.0f GeV/c^{2}" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"wtmass_log", ymin=0.1, xmax=350, yfactor=2)
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

def met(h, prefix="", rebin=1, ratio=False):
    xlabel = "E_{T}^{miss} (GeV)"
    ylabel = "Events / %.0f GeV"

    _optsLin  = {}
    _optsLog  = {"ymin": 0.1, "ymaxfactor": 2}
    _opts2 = {"ymin": 0, "ymax": 2}

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylabel = ylabel % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"met", opts=_optsLin)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

    h.createFrame(prefix+"met_log", createRatio=ratio, opts=_optsLog, opts2=_opts2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.moveLegend(histograms.createLegend()))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

def transverseMass(h, prefix="", rebin=1, ratio=False):
    xlabel = "m_{T}(#mu, E_{T}^{miss}) (GeV)"
    ylabel = "Events / %.0f GeV"

    _optsLin  = {}
    _optsLog  = {"ymin": 0.1, "ymaxfactor": 2}
    _opts2 = {"ymin": 0, "ymax": 2}

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylabel = ylabel % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"mt", opts=_optsLin)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

    h.createFrame(prefix+"mt_log", createRatio=ratio, opts=_optsLog, opts2=_opts2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.moveLegend(histograms.createLegend()))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()


# MET
class PlotMet:
    def __init__(self, datasets, normalizeToLumi=None, rebin=2, postfix=""):
        self.datasets = datasets
        self.normalizeToLumi = normalizeToLumi
        self.rebin = rebin
        self.postfix = postfix
        if len(postfix) > 0:
            self.postfix = "_"+self.postfix
        self.ylabel = "Number of events / %d GeV" % self.rebin
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
        h.setLegend((histograms.createLegend()))
        ROOT.gPad.SetLogy(True)
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText()
        h.save()

    def _createPlot(self, met, selection, calcNumEvents=False):
        h = plots.DataMCPlot(self.datasets, selection+"/%s_et" % met, normalizeToLumi=self.normalizeToLumi)
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(self.rebin))
        if calcNumEvents:
            self._calculateNumEvents(h)
        h.stackMCHistograms()
        h.addMCUncertainty()
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

def printMuonOrigin(datasetsMC, selection):
    datasets = datasetsMC.deepCopy()
    plots.mergeRenameReorderForDataMC(datasets)
    
    printMuonOriginHelper(datasets, selection)

    datasets.merge("Ws", ["TTJets", "WJets", "SingleTop"])
    datasets.selectAndReorder(["Ws"])
    printMuonOriginHelper(datasets, selection)

def printMuonOriginHelper(datasets, selection):
    mother = histograms.HistoManager(datasets, selection+"/muon_genMother")
    mother.normalizeMCByCrossSection()
    grandMother = histograms.HistoManager(datasets, selection+"/muon_genGrandMother")
    grandMother.normalizeMCByCrossSection()

    for datasetName in datasets.getMCDatasetNames():
        m = mother.getHisto(datasetName).getRootHisto()
        gm = grandMother.getHisto(datasetName).getRootHisto()

        allMus = m.Integral(0, m.GetNbinsX()+1)
        muFromW = m.GetBinContent(25)
        muFromZ = m.GetBinContent(24)
        muFromTau = m.GetBinContent(16)
        muFromTauW = gm.GetBinContent(25)
        muFromTauZ = gm.GetBinContent(24)
        otherMus = allMus - muFromW - muFromZ - muFromTauW - muFromTauZ

        print "Dataset %s" % datasetName
#        print "  All mus           %f" % allMus
        print "  Mus from W        %f" % (muFromW/allMus)
        print "  Mus from Z        %f" % (muFromZ/allMus)
        print "  Mus from tau      %f" % (muFromTau/allMus)
        print "    Mus from W->tau %f" % (muFromTauW/allMus)
        print "    Mus from Z->tau %f" % (muFromTauZ/allMus)
        print "  Other mus         %f" % (otherMus/allMus)

 
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

def reorderCounterTable(table):
    # Move QCD
    tmp = table.getColumn(2)
    table.removeColumn(2)
    table.insertColumn(4, tmp)

    # Move Single top
    tmp = table.getColumn(6)
    table.removeColumn(6)
    table.insertColumn(4, tmp)

def printCountersOld(datasets, datasetsMC, analysisPrefix, normalizeToLumi=None):
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
    latexFormat2 = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.1f"))
    #latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.0f", valueOnly=True))
    
    print "============================================================"
    print "Main counter (%s)" % eventCounter.getNormalizationString()
    #eventCounter.getMainCounter().printCounter()
    table = eventCounter.getMainCounterTable()

#    addSumColumn(table)
#    addTtwFractionColumn(table)
#    addPurityColumn(table)
#    addDyFractionColumn(table)
#    addQcdFractionColumn(table)

#    reorderCounterTable(table)

#    print table.format()
    print table.format(latexFormat)
#    print table.format(latexFormat2)
    return
    
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
