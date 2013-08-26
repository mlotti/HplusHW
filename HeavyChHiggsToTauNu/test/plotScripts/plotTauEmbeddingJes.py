#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import plotTauEmbeddingSignalAnalysis as tauEmbedding

#postfix = ""
#postfix = "CaloMet60"
postfix = "CaloMet60TEff"

baseline = "signalAnalysis"+postfix
#baseline = "signalAnalysisRtau0MET70"+postfix

plus = baseline + "JESPlus03eta02METPlus00"
#plus = baseline + "JESPlus03eta02METMinus00"
minus = baseline + "JESMinus03eta02METPlus00"
#minus = baseline + "JESMinus03eta02METMinus00"

normalize=True
#normalize=False

#count = "btagging"
count = "deltaPhiTauMET<160"
#count = "deltaPhiTauMET<130"
#count = "deltaPhiTauMET<90"

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=baseline+"Counters", weightedCounters=False)

    datasets.remove([
#            "SingleMu_Mu_160431-163261_May10",
#            "SingleMu_Mu_163270-163869_May10",
#            "SingleMu_Mu_165088-166150_Prompt",
#            "SingleMu_Mu_166161-166164_Prompt",
#            "SingleMu_Mu_166346-166346_Prompt",
#            "SingleMu_Mu_166374-167043_Prompt",
#            "SingleMu_Mu_167078-167913_Prompt",

#            "SingleMu_Mu_170722-172619_Aug05",
#            "SingleMu_Mu_172620-173198_Prompt",
#            "SingleMu_Mu_173236-173692_Prompt",
        ])
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)

    values = {}

    analyses = [
        ("Baseline", baseline),
        ("Plus", plus),
        ("Minus", minus)
        ]

    mainTable = counter.CounterTable()
    tauTable = counter.CounterTable()
    cntr = "Counters"
    if normalize:
        cntr += "/weighted"
    for name, analysis in analyses:
        eventCounter = counter.EventCounter(datasets, counters=analysis+cntr)

        eventCounter.normalizeMCByLuminosity()
        if normalize:
            tauEmbedding.scaleNormalization(eventCounter)
        col = eventCounter.getMainCounterTable().getColumn(name="Data")
        col.setName(name)
        mainTable.appendColumn(col)
        effcol = counter.efficiencyColumn(col.getName()+" eff", col)
        mainTable.appendColumn(effcol)
        values[name+"Main"] = effcol

        value = col.getCount(col.getRowNames().index(count)).value()
        values[name] = value

        col = eventCounter.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight").getColumn(name="Data")
        col.setName(name)
        tauTable.appendColumn(col)
        effcol = counter.efficiencyColumn(col.getName()+" eff", col)
        tauTable.appendColumn(effcol)
        values[name+"Tau"] = effcol
    
    mainTable.appendColumn(counter.divideColumn("Plus eff/Baseline", values["PlusMain"], values["BaselineMain"]))
    mainTable.appendColumn(counter.divideColumn("Minus eff/Baseline", values["MinusMain"], values["BaselineMain"]))
    tauTable.appendColumn(counter.divideColumn("Plus eff/Baseline", values["PlusTau"], values["BaselineTau"]))
    tauTable.appendColumn(counter.divideColumn("Minus eff/Baseline", values["MinusTau"], values["BaselineTau"]))

    print mainTable.format()
    print tauTable.format()

    plusDiff = abs(values["Baseline"] - values["Plus"])
    minusDiff = abs(values["Baseline"] - values["Minus"])
    maxDiff = max(plusDiff, minusDiff)
    rel = maxDiff / values["Baseline"]

    print "Count %s, baseline %.3f, plus %.3f, minus %.3f" % (count, values["Baseline"], values["Plus"], values["Minus"])
    print "Plus diff %.3f, minus diff %.3f" % (plusDiff, minusDiff)
    print "Relative uncertainty from tau energy scale %.6f" % (rel)


    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.32, dh=-0.15)

    metCut = "(met_p4.Et() > 50)"
    bTaggingCut = "passedBTagging"
    tdMt = dataset.TreeDraw("dummy",
                            weight="weightPileup*weightTrigger*weightBTagging",
                            selection=metCut+"&&"+bTaggingCut,
                            varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(40,0,400)"
                            )

    output = ROOT.TFile.Open("mt_variated_ewk.root", "RECREATE")

    #doPlot(datasets, analyses, tdMt, "mt_variated")
    doPlot(datasets, analyses, "transverseMass", "mt_variated_btagging", output, "Dphi180")
    doPlot(datasets, analyses, "transverseMassAfterDeltaPhi160", "mt_variated_deltaPhi160", output, "Dphi160")
    doPlot(datasets, analyses, "transverseMassAfterDeltaPhi130", "mt_variated_deltaPhi130", output, "Dphi130")
    doPlot(datasets, analyses, "transverseMassAfterDeltaPhi90", "mt_variated_deltaPhi90", output, "Dphi90")

    output.Close()

def doPlot(datasets, analyses, path, name, rootFile=None, rootHistoName=None):
    histos = []
    legends = {"Plus": "#tau-jet energy scale variated by +3 %",
               "Minus": "#tau-jet energy scale variated by -3 %"}

    for aname, analysis in analyses:
        p = None
        if isinstance(path, basestring):
            p = plots.DataMCPlot(datasets, analysis+"/"+path)
        else:
            p = plots.DataMCPlot(datasets, path.clone(tree=analysis+"/tree"))

        if normalize:
            tauEmbedding.scaleNormalization(p)
        
        h = p.histoMgr.getHisto("Data")
        h.setName(aname)
        h.setLegendLabel(legends.get(aname, aname))
        histos.append(h)

    p = plots.ComparisonManyPlot(histos[0], histos[1:])
    p.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    if rootFile:
        baseline = histos[0].getRootHisto().Clone("EWKtau_"+rootHistoName)
        baseline.SetDirectory(rootFile)
        baseline.Write()

        plus = histos[1].getRootHisto().Clone("EWKtau_JESUp_"+rootHistoName)
        plus.SetDirectory(rootFile)
        plus.Write()

        minus = histos[2].getRootHisto().Clone("EWKtau_JESDown_"+rootHistoName)
        minus.SetDirectory(rootFile)
        minus.Write()

    styles.mcStyle(p.histoMgr.getHisto("Plus"))
    styles.mcStyle2(p.histoMgr.getHisto("Minus"))
    p.histoMgr.getHisto("Minus").getRootHisto().SetMarkerSize(2)
    p.setLuminosity(datasets.getDataset("Data").getLuminosity())
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
