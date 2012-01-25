#!/usr/bin/env python

import os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import plotTauEmbeddingSignalAnalysis as tauEmbedding
import produceTauEmbeddingResult as result

#postfix = ""
#postfix = "CaloMet60"
postfix = "CaloMet60TEff"

baseline = "signalAnalysis"+postfix
#baseline = "signalAnalysisRtau0MET70"+postfix

plus = baseline + "JESPlus03eta02METPlus00"
#plus = baseline + "JESPlus03eta02METMinus00"
minus = baseline + "JESMinus03eta02METPlus00"
#minus = baseline + "JESMinus03eta02METMinus00"

#count = "btagging"
count = "deltaPhiTauMET<160"
#count = "deltaPhiTauMET<130"
#count = "deltaPhiTauMET<90"


def main():
    dirEmbs = ["."] + [os.path.join("..", d) for d in result.dirEmbs[1:]]
    #dirSig = "../"+result.dirSig
    
    datasetsEmb = result.DatasetsMany(dirEmbs, baseline+"Counters")
    #datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")

    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    #plots.mergeRenameReorderForDataMC(datasetsSig)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    values = {}

    analyses = [
        ("Baseline", baseline),
        ("Plus", plus),
        ("Minus", minus)
        ]

    cntr = "Counters/weighted"

    mainTable = counter.CounterTable()
    tauTable = counter.CounterTable()

    for name, analysis in analyses:
        c = datasetsEmb.getCounter("Data", analysis+cntr+"/counter")
        c.setName(name)
        mainTable.appendColumn(c)
        col = mainTable.getColumn(name=name)
        
        value = col.getCount(col.getRowNames().index(count)).value()
        values[name] = value
    
    plusDiff = abs(values["Baseline"] - values["Plus"])
    minusDiff = abs(values["Baseline"] - values["Minus"])
    maxDiff = max(plusDiff, minusDiff)
    rel = maxDiff / values["Baseline"]

    print "Count %s, baseline %.3f, plus %.3f, minus %.3f" % (count, values["Baseline"], values["Plus"], values["Minus"])
    print "Plus diff %.3f, minus diff %.3f" % (plusDiff, minusDiff)
    print "Relative uncertainty from tau energy scale %.6f" % (rel)

    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.32, dh=-0.15)

    doPlot(datasetsEmb, analyses, "transverseMassAfterDeltaPhi160", "mt_variated_deltaPhi160")


def doPlot(datasetsEmb, analyses, path, name):
    histos = []
    legends = {"Plus": "#tau-jet energy scale variated by +3 %",
               "Minus": "#tau-jet energy scale variated by -3 %"}

    for aname, analysis in analyses:
        (rootHisto, tmp) = datasetsEmb.getHistogram("Data", analysis+"/"+path)
        h = histograms.Histo(rootHisto, aname)
        h.setLegendLabel(legends.get(aname, aname))
        h.setDrawStyle("EP")
        h.setLegendStyle("p")
        histos.append(h)

    p = plots.ComparisonManyPlot(histos[0], histos[1:])
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))

    styles.dataStyle(p.histoMgr.getHisto("Baseline"))
    styles.mcStyle(p.histoMgr.getHisto("Plus"))
    styles.mcStyle2(p.histoMgr.getHisto("Minus"))
    p.histoMgr.getHisto("Minus").getRootHisto().SetMarkerSize(2)
    p.setLuminosity(datasetsEmb.getLuminosity())
    p.createFrame(name, createRatio=True, opts2={"ymax": 2}, opts={"ymax": 40})
    yaxis = p.getFrame2().GetYaxis()
    yaxis.SetTitle("Ratio")
    #yaxis.SetTitleSize(yaxis.GetTitleSize()*0.8)
    p.setLegend(histograms.moveLegend(histograms.createLegend()))
    
    p.frame.GetXaxis().SetTitle("m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})")
    p.frame.GetYaxis().SetTitle("Events / 20 GeV/c^{2}")
    p.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    p.addLuminosityText()
    p.save()


if __name__ == "__main__":
    main()
