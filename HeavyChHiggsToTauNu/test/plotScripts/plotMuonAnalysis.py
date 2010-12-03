#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

legendLabels = {
    "Data":                  "Data",
#    "TTbar":                 "t#bar{t}",
#    "TTbarJets":             "t#bar{t}+jets",
    "TTJets":                "t#bar{t}+jets",
    "WJets":                 "W+jets",
#    "ZJets":                 "Z+jets",
    "DYJetsToLL":            "DY+jets",
#    "QCD_Pt15to30_Fall10":   "QCD, 15 < #hat{p}_{T} < 30",
    "QCD_Pt30to50_Fall10":   "QCD, 30 < #hat{p}_{T} < 50",
    "QCD_Pt50to80_Fall10":   "QCD, 50 < #hat{p}_{T} < 80",
    "QCD_Pt80to120_Fall10":  "QCD, 80 < #hat{p}_{T} < 120",
    "QCD_Pt120to170_Fall10": "QCD, 120 < #hat{p}_{T} < 170",
    "QCD_Pt170to300_Fall10": "QCD, 170 < #hat{p}_{T} < 300",
    "QCD_Pt20_MuEnriched": "QCD (#mu enr.), #hat{p}_{T} > 20",
    "QCD_Pt20to30_MuEnriched": "QCD (#mu enr.), 20 < #hat{p}_{T} < 30",
    "QCD_Pt30to50_MuEnriched": "QCD (#mu enr.), 30 < #hat{p}_{T} < 50",
    "QCD_Pt50to80_MuEnriched": "QCD (#mu enr.), 50 < #hat{p}_{T} < 80",
    "QCD_Pt80to120_MuEnriched": "QCD (#mu enr.), 80 < #hat{p}_{T} < 120",
    "QCD_Pt120to150_MuEnriched": "QCD (#mu enr.), 120 < #hat{p}_{T} < 150",
    "QCD_Pt150_MuEnriched": "QCD (#mu enr.), #hat{p}_{T} > 150"
}


QCDdetails = False
#QCDdetails = True

#QCD = "Binned"
QCD = "Mu"
#QCD = "MuBinned"

WdecaySeparate = False
#WdecaySeparate = True

#lastSelection = "h11_JetSelection"
#lastMultip = "h11_Multiplicity"
#lastSelectionOther = "afterOtherCutsAfterJetMultiplicityCut"
#lastSelection = "h12_METCut"
#lastMultip = "h12_Multiplicity"
#lastSelectionOther = "afterOtherCutsAfterMETCut"

multip_beforeJet = "noIsoNoVetoMeth08_Multiplicity"
multip_afterJet = "noIsoNoVetoMeth09_Multiplicity"

lastSelection = "noIsoNoVetoMeth10_METCut"
lastSelectionBeforeMet = "noIsoNoVetoMeth09_JetMultiplicityCut"
lastMultip = "noIsoNoVetoMeth10_Multiplicity"
lastSelectionOther = "noIsoNoVetoMetAoch09_METCutAfterOtherCuts"
lastSelectionBeforeMetOther = "noIsoNoVetoMetAoch08_JetMultiplicityCutAfterOtherCuts"
lastSelectionBeforeMetOtherIso = "noIsoNoVetoMetAoch08_JetMultiplicityCutAfterOtherCutsIso"
lastSelectionOtherIso = "noIsoNoVetoMetAoch09_METCutAfterOtherCutsIso"

QCD_datasets = ["QCD_Pt30to50_Fall10",
                "QCD_Pt50to80_Fall10",
                "QCD_Pt80to120_Fall10",
                "QCD_Pt120to170_Fall10",
                "QCD_Pt170to300_Fall10"]
if QCD == "Mu":
    QCD_datasets = ["QCD_Pt20_MuEnriched"]
elif QCD == "MuBinned":
    QCD_datasets = ["QCD_Pt20to30_MuEnriched",
                    "QCD_Pt30to50_MuEnriched",
                    "QCD_Pt50to80_MuEnriched",
                    "QCD_Pt80to120_MuEnriched",
                    "QCD_Pt120to150_MuEnriched",
                    "QCD_Pt150_MuEnriched"]

datasets = getDatasetsFromMulticrabCfg(counters="noIsoNoVetoMetcountAnalyzer")
datasetsQCD = datasets.shallowCopy()
datasetsQCD.selectAndReorder(QCD_datasets)

#datasets.getDataset("Mu_135821-144114").setLuminosity(3051760.115/1e6) # ub^-1 -> pb^-1
#datasets.getDataset("Mu_146240-147116").setLuminosity(4390660.197/1e6)
#datasets.getDataset("Mu_147196-149442").setLuminosity(27384630.974/1e6)
datasets.getDataset("Mu_135821-144114").setLuminosity(2863224.758/1e6) # ub^-1 -> pb^-1
datasets.getDataset("Mu_146240-147116").setLuminosity(3977060.866/1e6)
datasets.getDataset("Mu_147196-149442").setLuminosity(27907588.871/1e6)
datasets.mergeData()

datasetsMC = datasets.deepCopy()
datasetsMC.remove(["Data"])

for name in [d.getName() for d in datasets.getAllDatasets()]:
    if "QCD" in name and name not in QCD_datasets:
        datasets.remove(name)
        datasetsMC.remove(name)
        del legendLabels[name]
datasets.merge("QCD", QCD_datasets)
if QCD == "Binned":
    legendLabels["QCD"] = " QCD, 30 < #hat{p}_{T} < 300"
elif QCD == "Mu":
    legendLabels["QCD"] = legendLabels["QCD_Pt20_MuEnriched"]
elif QCD == "MuBinned":
    legendLabels["QCD"] = " QCD (#mu enrich.), 20 < #hat{p}_{T} < 300"
for q in QCD_datasets:
    del legendLabels[q]

#singlet = ["SingleTop_sChannel", "SingleTop_tChannel", "SingleTop_tWChannel"] # Summer10
singlet = ["TToBLNu_s-channel", "TToBLNu_t-channel", "TToBLNu_tW-channel"] # Fall10
datasets.merge("Single t", singlet)
legendLabels["Single t"] = "Single t"

styleGenerator = styles.generator(fill=True)
wmunu = ["WJets", "TTJets", "Single t"]
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
        "QCD"
])



#datasets.getDataset("Data").setPrefix("PileupV1")

#textDefaults.setCmsPreliminaryDefaults()
textDefaults.setEnergyDefaults(x=0.17)
textDefaults.setLuminosityDefaults(x=0.4, size=0.04)
createLegend.setDefaults(x1=0.65,y1=0.7)

style = TDRStyle()

class Histo:
    def __init__(self, datasets, name, lumi=None):
        self.histos = HistoSet(datasets, name)
        #print "\n".join(histos.getDatasetNames())

        if lumi == None:
            self.histos.normalizeMCByLuminosity()
        else:
            self.histos.normalizeMCToLuminosity(lumi)

        self.histos.setHistoLegendLabels(legendLabels)

        hasData = self.histos.hasHisto("Data")

        self.histos.setHistoLegendStyleAll("F")
        if hasData:
            self.histos.setHistoLegendStyle("Data", "p")

        styleGenerator.reset()
        self.histos.forEachMCHisto(styleGenerator)
        if hasData:
            styles.getDataStyle()(self.histos.getHisto("Data"))
            self.histos.setHistoDrawStyle("Data", "EP")

    def createFrame(self, plotname, **kwargs):
        (self.canvas, self.frame) = self.histos.createCanvasFrame(plotname, **kwargs)

    def setLegend(self, legend):
        self.legend = legend
        self.histos.addToLegend(legend)

    def draw(self):
        self.histos.draw()
        self.legend.Draw()

    def save(self):
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
        self.canvas.SaveAs(".png")
        self.canvas.SaveAs(".eps")
        #self.canvas.SaveAs(".C")
        ROOT.gErrorIgnoreLevel = backup

dataLumi = datasets.getDataset("Data").getLuminosity()

def jetMultiplicity():
    # After muon selection (h10_ElectronVeto)
    h = Histo(datasets, multip_beforeJet+"/jets_multiplicity")
    h.histos.stackMCHistograms()
    h.createFrame(multip_beforeJet+"_njets", ymin=0.1, ymax=1e6)
    h.frame.GetXaxis().SetTitle("Jet multiplicity")
    h.frame.GetYaxis().SetTitle("Number of events")
    h.setLegend(createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText(x=0.4)
    h.save()
    
    # After muon selection + jet multip. cut (h11_JetSelection)
    for x in [multip_afterJet, lastMultip]:
        h = Histo(datasets, x+"/jets_multiplicity")
        h.histos.stackMCHistograms()
        h.createFrame(x+"_njets", xmin=3)
        h.frame.GetXaxis().SetTitle("Jet multiplicity")
        h.frame.GetYaxis().SetTitle("Number of events")
        h.setLegend(createLegend())
        h.draw()
        addCmsPreliminaryText()
        addEnergyText()
        h.histos.addLuminosityText()
        h.save()

# Muon pt after all other cuts
def muonPt(h, prefix=""):
    xlabel = "Muon p_{T} (GeV/c)"
    #ylabel = "Number of muons / 5.0 GeV/c"
    ylabel = "Number of events / 5.0 GeV/c"
    ptcut = 40
    xmax = 350

    h.histos.forEachHisto(lambda h: h.Rebin(5))
    h.histos.stackMCHistograms()
    h.createFrame(prefix+"muon_pt", xmax=xmax)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend())
    #ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()

    h.createFrame(prefix+"muon_pt_log", ymin=0.01, yfactor=2, xmax=xmax)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()

    h.createFrame(prefix+"muon_pt_cut%d"%ptcut, xmin=ptcut, xmax=xmax, ymax=200)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()

    h.createFrame(prefix+"muon_pt_cut%d_log"%ptcut, xmin=ptcut, xmax=xmax, ymin=0.1, yfactor=2)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()
    
# Muon eta after all other cuts
def muonEta(h, prefix=""):
    h.histos.forEachHisto(lambda h: h.Rebin(5))
    h.histos.stackMCHistograms()
    h.createFrame(prefix+"muon_eta", yfactor=1.4)
    h.frame.GetXaxis().SetTitle("Muon  #eta")
    h.frame.GetYaxis().SetTitle("Number of muons / 0.5")
    h.setLegend(createLegend())
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText(x=0.2)
    h.save()

# Muon isolation after all other cuts
def muonIso(h, prefix=""):
    xlabel = "Muon rel. isol. (GeV/c)"
    #ylabel = "Number of muons / 0.01"
    #rebin = 2
    ylabel = "Number of muons / 0.025"
    rebin = 5

    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.histos.stackMCHistograms()
    h.createFrame(prefix+"muon_reliso")
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend())
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()

    h.createFrame(prefix+"muon_reliso_log", ymin=1e-2, ymax=4000)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend(0.72, 0.7, 0.92, 0.92))
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText(x=0.45, y=0.85)
    h.save()

def muonD0():
    # Muon track ip w.r.t. beam spot
    h = Histo(datasets, lastSelection+"/muon_trackDB")
    h.histos.stackMCHistograms()
    h.createFrame(lastSelection+"_muon_trackdb", xmin=0, xmax=0.2, ymin=0.1)
    h.frame.GetXaxis().SetTitle("Muon track d_{0}(Bsp) (cm)")
    h.frame.GetYaxis().SetTitle("Number of muons")
    h.setLegend(createLegend(0.7, 0.5, 0.9, 0.8))
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()

class PrintNumEvents:
    def __init__(self, minMet):
        self.minMet = minMet
        self.results = {}
        #print "MET cut %d" % self.minMet

    def __call__(self, name, histo):
        bin = histo.FindBin(self.minMet)
        n = histo.Integral(bin, histo.GetNbinsX()+1)
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
def plotMet(met, selection=lastSelection, prefix="met", calcNumEvents=False):
    rebin = 5
    ylabel = "Number of events / 5.0 GeV"
    xlabel = {"calomet": "Calo MET",
              "pfmet": "PF MET",
              "tcmet": "TC MET"}[met] + " (GeV)"

    h = Histo(datasets, selection+"/%s_et" % met)
    if calcNumEvents:
        for pn in [0, 15, 20, 30, 40]:
            pn = PrintNumEvents(pn)
            for name in [d.getName() for d in datasets.getAllDatasets()]:
                h.histos.forHisto(name, lambda h: pn(name, h))
            pn.printQcdFraction()
            print

    h.histos.forEachHisto(lambda h: h.Rebin(rebin))
    h.histos.stackMCHistograms()
    h.createFrame(selection+"_"+prefix+"_"+met, ymax=200, xmax=300)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend())
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()

    h.createFrame(selection+"_"+prefix+"_"+met+"_log", ymin=0.01, ymax=200, xmax=300)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    addCmsPreliminaryText()
    addEnergyText()
    h.histos.addLuminosityText()
    h.save()


jetMultiplicity()
muonPt(Histo(datasets, lastSelectionOther+"/pt"), lastSelectionOther+"_")
muonPt(Histo(datasets, lastSelectionBeforeMetOther+"/pt"), lastSelectionBeforeMetOther+"_")
muonPt(Histo(datasets, lastSelection+"/muon_pt"), lastSelection+"_")
muonEta(Histo(datasets, lastSelection+"/muon_eta"), lastSelection+"_")
muonD0()
muonIso(Histo(datasets, lastSelectionBeforeMetOtherIso+"/relIso"), lastSelectionBeforeMetOtherIso+"_")
muonIso(Histo(datasets, lastSelectionOtherIso+"/relIso"), lastSelectionOtherIso+"_")
muonIso(Histo(datasets, lastSelection+"/muon_relIso"), lastSelection+"_")
#muonIso(Histo(datasets, lastSelectionOther+"/relIso"), lastSelectionOther+"_")
#muonIso(Histo(datasets, lastSelection+"/muon_relIso"), lastSelection+"_")

plotMet("calomet")
plotMet("pfmet")
plotMet("tcmet")

plotMet("pfmet", selection=lastSelectionBeforeMet, calcNumEvents=True)

if QCDdetails:
    muonPt(Histo(datasetsQCD, lastSelectionOther+"/pt", dataLumi), lastSelectionOther+"_qcd_")
    muonPt(Histo(datasetsQCD, lastSelection+"/pt", dataLumi), lastSelection+"_qcd_")
    muonEta(Histo(datasetsQCD, lastSelection+"/muon_eta", dataLumi), lastSelection+"_qcd_")
    muonIso(Histo(datasetsQCD, lastSelectionOther+"/relIso", dataLumi), lastSelectionOther+"_")
    muonIso(Histo(datasetsQCD, lastSelection+"/muon_relIso", dataLumi), lastSelection+"_")

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
    return EventCounter(ds, modifyCountNames)


print "============================================================"
print "Dataset info: "
datasets.printInfo()

eventCounter = makeEventCounter(datasets)
eventCounter.normalizeMCByLuminosity()

print "============================================================"
print "Main counter (%s)" % eventCounter.getNormalizationString()
#eventCounter.getMainCounter().printCounter()
print eventCounter.getMainCounterTable().format(FloatDecimalFormat(1))
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
print eventCounter.getMainCounterTable().format(FloatDecimalFormat(0))

if QCDdetails:
    print "============================================================"
    print "QCD dataset info: "
    datasetsQCD.printInfo()


    eventCounter = makeEventCounter(datasetsQCD)
    eventCounter.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    print "============================================================"
    print "Main counter (%s)" % eventCounter.getNormalizationString()
    eventCounter.getMainCounter().printCounter(FloatDecimalFormat(1))


    eventCounter = makeEventCounter(datasetsQCD)
    print "============================================================"
    print "Main counter (%s)" % eventCounter.getNormalizationString()
    eventCounter.getMainCounter().printCounter(FloatDecimalFormat(0))
