#!/usr/bin/env python

import os

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

embedding = "multicrab_110217_155220"
embeddingData = "multicrab_110221_085312"
signalAnalysis = "../multicrab_110218_092432"

#embedding = "multicrab_110228_091023"
#embedding = "multicrab_110228_143151"
#embedding = "multicrab_signalAnalysis_110405_093754"
embedding = "multicrab_signalAnalysis_TauIdScan_110412_090749"
embeddingData = embedding
#signalAnalysis = "../multicrab_110228_085943"
#signalAnalysis = "../multicrab_110404_134156"
signalAnalysis = "../multicrab_signalAnalysis_tauIdScan_110411_165833"

#analysis = "signalAnalysis"
analysis = "signalAnalysisTauSelectionHPSTightTauBased"
#analysis = "signalAnalysisTauSelectionHPSTightTauNoRtauBased"
#analysis = "signalAnalysisTauSelectionHPSMediumTauBased"
#analysis = "signalAnalysisTauSelectionHPSMediumTauNoRtauBased"
#analysis = "signalAnalysisTauSelectionHPSLooseTauBased"
#analysis = "signalAnalysisTauSelectionHPSLooseTauNoRtauBased"
counters = analysis+"Counters"

# Datasets from embedding
datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(embedding, "multicrab.cfg"), counters=counters)
if embeddingData == embedding:
    datasets.loadLuminosities()
else:
    datasetsData = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(embeddingData, "multicrab.cfg"), counters=counters)
    datasetsData.loadLuminosities()
    datasets.extend(datasetsData)

# Datasets from the original signal analysis
datasetsExpected = dataset.getDatasetsFromMulticrabCfg(cfgfile=os.path.join(signalAnalysis, "multicrab.cfg"), counters=counters)

plots.mergeRenameReorderForDataMC(datasetsExpected)
plots.mergeRenameReorderForDataMC(datasets)

lumi = datasetsExpected.getDataset("Data").getLuminosity()

#datasets.getDataset("Data").setLuminosity(36)
#datasetsExpected.getDataset("Data").setLuminosity(36)

print "Embedded lumi %f" % datasets.getDataset("Data").getLuminosity()
print "Expected lumi %f" % datasetsExpected.getDataset("Data").getLuminosity()

datasets.remove("TToHplusBWB_M120")

#datasets.selectAndReorder(["TTJets", "WJets", "QCD_Pt20_MuEnriched"])
#datasetsExpected.selectAndReorder(["TTJets", "WJets"])


mainCounterMap = {
    "Trigger and HLT_MET cut": "Triggered",
    "primary vertex": "Good primary vertex",
    "taus == 1": r"One identified \taujet",
    "electron veto": r"Electron veto",
    "muon veto": r"Muon veto",
    "MET": r"$\text{MET} > 70\:\GeV$",
    "njets": r"$\ge 3$ hadronic jets",
    "btagging": r"$\ge 1$ b-tagged jets",
    "fake MET veto": r"$\min(\DeltaPhi(\text{MET},\text{jets})) < 10^\circ$"
}
mainCounterMap.update({ # for ConTeXt
        "taus == 1": r"One identified $\tau$-jet",
        "MET": r"$\text{MET} > 70\Giga\EVolt$",
        "fake MET veto": r"$\min(\Delta\phi(\text{MET},\text{jets})) < 10^\circ$"
})

def floatEqualAssert(a, b):
    c = 0
    if b != 0:
        c = abs(a-b)/b
    elif a != 0:
        c = abs(a-b)/a
    else:
        c = abs(a-b)

    if c >= 0.01:
        raise Exception("a %f and b %f differ" % (a, b))
    

def integrate(th, firstBin, lastBin):
    integral = dataset.Count(0, 0)
    for bin in xrange(firstBin, lastBin+1):
        integral.add(dataset.Count(th.GetBinContent(bin), th.GetBinError(bin)))
    return integral

def normalizationFactor(embedded, expected):
    mtRange = (30, 70)

    lowBin = embedded.FindBin(mtRange[0])
    upBin = embedded.FindBin(mtRange[1])-1
    #print lowBin, embedded.GetBinLowEdge(lowBin)
    #print upBin, embedded.GetXaxis().GetBinUpEdge(upBin)

    floatEqualAssert(mtRange[0], embedded.GetBinLowEdge(lowBin))
    floatEqualAssert(mtRange[1], embedded.GetXaxis().GetBinUpEdge(upBin))

    embeddedCount = integrate(embedded, lowBin, upBin)
    expectedCount = integrate(expected, lowBin, upBin)
    normfactor = expectedCount.copy()
    normfactor.divide(embeddedCount)

    print "mT normalization range %.1f - %.1f GeV/c^2 (bins %d - %d)" % (mtRange[0], mtRange[1], lowBin, upBin)
    print "Embedded events %.1f +- %.1f" % (embeddedCount.value(), embeddedCount.uncertainty())
    print "Expected events %.1f +- %.1f" % (expectedCount.value(), expectedCount.uncertainty())
    print "Normalization factor %.3f +- %.3f" % (normfactor.value(), normfactor.uncertainty())

    return normfactor

def signalAreaEvents(embedded, expected, normfactor):
    mtMin = 0

    lowBin = embedded.FindBin(mtMin)
    upBin = embedded.GetNbinsX()+1 # include the overflow bin

    #embeddedCount = integrate(embedded, lowBin, upBin)
    #expectedCount = integrate(expected, lowBin, upBin)
    #embeddedCount = dataset.Count(embedded.Integral(lowBin, upBin), 0)
    #expectedCount = dataset.Count(expected.Integral(lowBin, upBin), 0)
    embeddedCount = dataset.Count(embedded.Integral(), 0)
    expectedCount = dataset.Count(expected.Integral(), 0)

    prediction = embeddedCount.copy()
    prediction.multiply(normfactor)

    print "Embedded events %.2f" % embeddedCount.value()
    print "Predicted events %.2f +- %.2f" % (prediction.value(), prediction.uncertainty())
    print "Expected events %.2f" % expectedCount.value()

mtEmbedded = plots.DataMCPlot(datasets, analysis+"/transverseMass")
mtExpected = plots.DataMCPlot(datasetsExpected, analysis+"/transverseMass")

def run(func, getter):
    return func(getter(mtEmbedded.histoMgr), getter(mtExpected.histoMgr))

norms = {}

for d in ["Data", "TTJets", "WJets"]:
    print
    print "From %s" % d
    norms[d] = run(normalizationFactor, lambda h: h.getHisto(d).getRootHisto())

mtEmbedded.stackMCHistograms()
mtExpected.stackMCHistograms()

print
print "From all MC"
norms["MCSum"] = run(normalizationFactor, lambda h: h.getHisto("StackedMC").getSumRootHisto())

# Scale
#mtEmbedded.histoMgr.forEachHisto(lambda histo: histo.getRootHisto().Scale(0.406020))

normFactor = norms["Data"]
#normFactor = dataset.Count(0.429, 0.296)
#normFactor = dataset.Count(0.7, 0.345) # Data
normFactor = dataset.Count(0.369, 0.042) # MC
def signalAreaEventsFactor(x, y):
    signalAreaEvents(x, y, normFactor)

print
print
print "From Data"
run(signalAreaEventsFactor, lambda h: h.getHisto("Data").getRootHisto())

print
print "From all MC"
run(signalAreaEventsFactor, lambda h: h.getHisto("StackedMC").getSumRootHisto())



import sys
sys.exit(0)

# Table formatting
tableFormat = counter.TableFormatText()
for i in xrange(1, 19, 2):
    tableFormat.setColumnFormat(counter.CellFormatText(valueFormat="%.5f"), index=i)
#tableFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueOnly=True))

def addEffs(table):
    eff = counter.counterEfficiency(table)
    colnames = eff.getColumnNames()
    mapping = {}
    for n in colnames:
        mapping[n] = n+"_eff"
    eff.renameColumns(mapping)

    for icol in xrange(0, eff.getNcolumns()):
        table.insertColumn(2*icol+1, eff.getColumn(icol))

# Read the expected MC
ecExpected = counter.EventCounter(datasetsExpected)
ecExpected.normalizeMCToLuminosity(lumi)
ecExpectedMain = ecExpected.getMainCounterTable()
addEffs(ecExpectedMain)

print "Expected MC"
print ecExpectedMain.format(tableFormat)

expectedTT = ecExpectedMain.getCount(ecExpectedMain.getNrows()-1, ecExpectedMain.indexColumn("TTJets")).value()

# Read the observed MC for the first time in order to get the
# normalization factor
tmp = counter.EventCounter(datasets)
tmp.normalizeMCToLuminosity(lumi)
tmpMain =tmp.getMainCounterTable()
observedTT = tmpMain.getCount(tmpMain.getNrows()-1, tmpMain.indexColumn("TTJets")).value()

#normFactor = expectedTT/observedTT
normFactor = 1.2/3.2

print "Expected MC %f, observed MC %f, observed normalization factor %f" % (expectedTT, observedTT, normFactor)

# Read the observed MC for the second time in order to apply the
# normalization factor
eventCounter = counter.EventCounter(datasets)
eventCounter.normalizeMCToLuminosity(lumi)
eventCounter.scale(normFactor)
main = eventCounter.getMainCounterTable()
addEffs(main)

print "Observed MC"
print main.format(tableFormat)


print "----"

def addSumColumn(table):
    #dataColumn = table.indexColumn("Data")

    #indices = filter(lambda x: x != dataColumn, xrange(0, table.getNcolumns()))
    #columns = [table.getColumn(i) for i in indices]
    columns = [table.getColumn(i) for i in xrange(0, table.getNcolumns())]
    table.insertColumn(1, counter.sumColumn("MCsum", columns))

def addTtwFractionColumn(table):
    ttColumn = table.indexColumn("TTJets")
    fraction = counter.divideColumn("TTJets/(TTJets+WJets)", table.getColumn(ttColumn), ttwSum(table))
    fraction.multiply(100) # -> %
    table.appendColumn(fraction)

def ttwSum(table):
    ttColumn = table.indexColumn("TTJets")
    wColumn = table.indexColumn("WJets")
    return counter.sumColumn("TTJets+WJets", [table.getColumn(i) for i in [ttColumn, wColumn]])

def addPurityColumn(table):
    mcSumColumn = table.indexColumn("MCsum")
    purity = counter.divideColumn("TT+W purity", ttwSum(table), table.getColumn(mcSumColumn))
    purity.multiply(100) # -> %
    table.appendColumn(purity)

latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.1f", valueOnly=True))
latexFormat.setColumnFormat(counter.CellFormatTeX(valueFormat="%.2f", valueOnly=True), name="TTJets/(TTJets+WJets)")

expectedTable = ecExpected.getMainCounterTable()
observedTable = tmp.getMainCounterTable()

for table in [expectedTable, observedTable]:
    addTtwFractionColumn(table)

    table.renameRows(mainCounterMap)

    print table.format(latexFormat)

observedTable = tmp.getMainCounterTable()
addSumColumn(observedTable)
addPurityColumn(observedTable)
addTtwFractionColumn(table)

#tablettw = counter.CounterTable()
#tablettw.appendColumn(ttwSum(observedTable))
#for c in ["QCD_Pt20_MuEnriched", "TT+W purity"]:
#    tablettw.appendColumn(observedTable.getColumn(name=c))
#tablettw.renameRows(mainCounterMap)
#print tablettw.format(latexFormat)

#print counter.counterEfficiency(main).format(tableFormat)

#mainCounter = eventCounter.getMainCounterTable()
#mainCounter.renameRows(mainCounterMap)
#print mainCounter.format()

# eventCounter = counter.EventCounter(datasets)
# eventCounter.normalizeMCToLuminosity(lumi)
# eventCounter.scale(0.5)

# print eventCounter.getMainCounterTable().format()


