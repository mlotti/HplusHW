#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

WdecaySeparate = False
#WdecaySeparate = True

tuneD6T = False
#tuneD6T = True

def findSelection(lst, name):
    for n in lst:
        if name in n:
            return n
    raise Exception("Did not find '%s' from the following list\n%s" % (name, "\n".join(lst)))

def replaceSelection(name, new):
    return name.split("_")[0]+"_"+new

#prefix = "noIsoNoVetoMetNJets3"
prefix = "noIsoNoVetoMetPFPt30Met20NJets3"
#prefix = "topMuJetRefMet"

topMuJetRefMet = [prefix+x for x in [
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
topMuJetRefMetAoc = []

noIsoNoVetoMet = [prefix+x for x in [
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
noIsoNoVetoMetAoc = [prefix+"Aoc"+x+"AfterOtherCuts" for x in [
        "h07_MuonLargestPt",
        "h08_JetMultiplicityCut",
        "h09_METCut"]]

noIsoNoVetoMetPF = [prefix+x for x in [
        "h00_AllMuons",
        "h01_Triggered",
        "h02_PrimaryVertex",
        "h03_GlobalTrackerMuon",
        "h04_MuonKin",
        "h05_MuonQuality",
        "h06_MuonIP",
        "h07_MuonVertexDiff",
        "h07_MuonLargestPt",
        "h08_JetMultiplicityCut",
        "h09_METCut"]]
noIsoNoVetoMetPFAoc = [prefix+"Aoc"+x+"AfterOtherCuts" for x in [
        "h06_MuonLargestPt",
        "h07_JetMultiplicityCut",
        "h08_METCut"]]

selections = noIsoNoVetoMet
selectionsAoc = noIsoNoVetoMetAoc
index = 8
if "noIsoNoVetoMetPF" in prefix:
    selections = noIsoNoVetoMetPF
    selectionsAoc = noIsoNoVetoMetPFAoc
elif "topMuJetRefMet" in prefix:
    selections = topMuJetRefMet
    selectionsAoc = topMuJetRefMetAoc
    index = 11

multip_beforeJet = prefix+"h%02d_Multiplicity" % index; index += 1
multip_afterJet = prefix+"h%02d_Multiplicity" % index; index += 1
lastMultip = prefix+"h%02d_Multiplicity" % index; index += 1

selectionAll = selections[0]
selectionTrigger = selections[1]
selectionPrimaryVertex = selections[2]
selectionMuon = findSelection(selections, "MuonLargestPt")
selectionJet = findSelection(selections, "JetMultiplicityCut")
selectionMet = findSelection(selections, "METCut")

multipMuon = replaceSelection(selectionMuon, "Multiplicity")
multipMuonJetSelection = replaceSelection(selectionMuon, "MultiplicityAfterJetId")

lastSelection = selections[-1]
lastSelectionBeforeMet = selections[-2]
lastSelectionOther = selectionsAoc[-1]
lastSelectionOtherIso = selectionsAoc[-1]+"Iso"
lastSelectionBeforeMetOther = selectionsAoc[-2]
lastSelectionBeforeMetOtherIso = selectionsAoc[-2]+"Iso"

datasets = dataset.getDatasetsFromMulticrabCfg(counters=prefix+"countAnalyzer")
#datasets.loadLuminosities()

if tuneD6T:
    datasets.remove(["TTJets_TuneZ2_Winter10", "WJets_TuneZ2_Winter10"])
else:
    datasets.remove(["TTJets_TuneD6T_Winter10", "WJets_TuneD6T_Winter10"])

plots.mergeRenameReorderForDataMC(datasets)

datasetsQCD = datasets.shallowCopy()
datasetsQCD.selectAndReorder(["QCD_Pt20_MuEnriched"])

datasetsMC = datasets.deepCopy()
datasetsMC.remove(["Data"])

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

datasets.selectAndReorder(
    ["Data"] + wmunu + [
        "DYJetsToLL",
        "QCD_Pt20_MuEnriched"
])

normalizeToLumi = None
if not datasets.hasDataset("Data"):
    normalizeToLumi = 36

#textDefaults.setCmsPreliminaryDefaults()
#histograms.textDefaults.setEnergyDefaults(x=0.17)
#histograms.textDefaults.setLuminosityDefaults(x=0.4, size=0.04)
#histograms.createLegend.setDefaults(x1=0.65,y1=0.7)
style = tdrstyle.TDRStyle()

class Plot(plots.PlotBase):
    def __init__(self, datasets, name):
        plots.PlotBase.__init__(self, datasets, name,
                                [".png"]
                                )

        if normalizeToLumi == None:
            self.histoMgr.normalizeMCByLuminosity()
        else:
            self.histoMgr.normalizeMCToLuminosity(normalizeToLumi)

        self._setLegendLabels()
        self._setLegendStyles()
        self._setPlotStyles()

def binWidth(plot):
    return plot.histoMgr.getHistos()[0].getBinWidth(1)

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
    h.histoMgr.addLuminosityText(x=0.4)
    h.save()

def jetPt(h, prefix=""):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    xlabel = "Jet p_{T} (GeV/c)"
    ylabel = "Number of jets / %.1f GeV/c" % binWidth(h)

    h.stackMCHistograms()
    h.addMCUncertainty()

    h.createFrame(prefix+"jet_pt_log", ymin=0.1, yfactor=2)
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
    xmax = 350

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))
    ylabel = ylabel % binWidth(h)

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
    ylabel = "Number of muons / %.1f" % binWidth(h)

    h.stackMCHistograms()
    
    if plotAll:
        h.createFrame(prefix+"muon_eta", yfactor=1.4)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText(x=0.2)
        h.save()

    h.createFrame(prefix+"muon_eta_log", yfactor=2, ymin=0.1)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText(x=0.2)
    h.save()

def muonPhi(h, prefix="", plotAll=False):
#    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(5))

    xlabel = "Muon  #phi"
    ylabel = "Number of muons / %.1f" % binWidth(h)
    h.stackMCHistograms()

    if plotAll:
        h.createFrame(prefix+"muon_phi", yfactor=1.4)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        h.histoMgr.addLuminosityText(x=0.2)
        h.save()

    h.createFrame(prefix+"muon_phi_log", yfactor=2, ymin=0.1)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy()
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText(x=0.2)
    h.save()

def muonIso(h, prefix=""):
    xlabel = "Muon rel. isol. (GeV/c)"
    #ylabel = "Number of muons / 0.01"
    #rebin = 2
    ylabel = "Number of muons / 0.025"
    rebin = 5

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    h.stackMCHistograms()
    h.createFrame(prefix+"muon_reliso")
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText()
    h.save()

    h.createFrame(prefix+"muon_reliso_log", ymin=1e-2, ymax=4000)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend(0.72, 0.7, 0.92, 0.92))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.histoMgr.addLuminosityText(x=0.45, y=0.85)
    h.save()

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
    ylabel = "Number of events / %.1f GeV/c" % binWidth(h)

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
    def __init__(self, rebin=2, postfix=""):
        self.rebin = rebin
        self.postfix = postfix
        if len(postfix) > 0:
            self.postfix = "_"+self.postfix
        self.ylabel = "Number of events / %d.0 GeV" % self.rebin
        self.xlabels = {"calomet": "Calo MET",
                        "pfmet": "PF MET",
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
        #h.histoMgr.addLuminosityText()
        h.save()

    def _createPlot(self, met, selection, calcNumEvents=False):
        h = Plot(datasets, selection+"/%s_et" % met)
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(self.rebin))
        if calcNumEvents:
            self._calculateNumEvents(h)
        h.stackMCHistograms()
        return h

    def plot(self, met, selection=lastSelection, calcNumEvents=False):
        h = self._createPlot(met, selection, calcNumEvents)
        self._plotLinear(h, selection, met)
        h.removeLegend()
        self._plotLog(h, selection, met)

    def plotLog(self, met, selection=lastSelection):
        h = self._createPlot(met, selection)
        self._plotLog(h, selection, met)

plotMet = PlotMet()

#for sel in selections:
#for sel in [selectionMuon, selectionJet, selectionMet]:
for sel in [selectionJet, selectionMet]:
    prefix = sel+"_"

    muonPt(Plot(datasets, sel+"/muon_pt"), prefix)
    muonEta(Plot(datasets, sel+"/muon_eta"), prefix)
    muonPhi(Plot(datasets, sel+"/muon_phi"), prefix)

    jetPt(Plot(datasets, sel+"/pfjet_pt"), prefix)

    plotMet.plotLog("pfmet", selection=sel)

    wTransMass(Plot(datasets, sel+"/wmunuPF_tmass"), prefix)

for sel in [multipMuon, multipMuonJetSelection]:
    prefix = sel+"_"

    jetMultiplicity(Plot(datasets, sel+"/jets_multiplicity"), prefix)


# jetMultiplicity()
# muonPt(Plot(datasets, lastSelectionOther+"/pt"), lastSelectionOther+"_")
# muonPt(Plot(datasets, lastSelectionBeforeMetOther+"/pt"), lastSelectionBeforeMetOther+"_")
# muonPt(Plot(datasets, lastSelection+"/muon_pt"), lastSelection+"_")
# muonEta(Plot(datasets, lastSelection+"/muon_eta"), lastSelection+"_")
# muonPhi(Plot(datasets, lastSelection+"/muon_phi"), lastSelection+"_")
# muonD0()
# muonIso(Plot(datasets, lastSelectionBeforeMetOtherIso+"/relIso"), lastSelectionBeforeMetOtherIso+"_")
# muonIso(Plot(datasets, lastSelectionOtherIso+"/relIso"), lastSelectionOtherIso+"_")
# muonIso(Plot(datasets, lastSelection+"/muon_relIso"), lastSelection+"_")
 
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


print "============================================================"
print "Dataset info: "
datasets.printInfo()

eventCounter = makeEventCounter(datasets)
if normalizeToLumi == None:
    eventCounter.normalizeMCByLuminosity()
else:
    eventCounter.normalizeMCToLuminosity(normalizeToLumi)

print "============================================================"
print "Main counter (%s)" % eventCounter.getNormalizationString()
#eventCounter.getMainCounter().printCounter()
print eventCounter.getMainCounterTable().format()
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
print eventCounter.getMainCounterTable().format()

