#!/usr/bin/env python

import os
import re
from array import array

import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

ROOT.gROOT.SetBatch(True)

legends = {
    "signalAnalysisTauSelectionHPSTightTauBased": "HPS tight",
    "signalAnalysisTauSelectionHPSMediumTauBased": "HPS medium",
    "signalAnalysisTauSelectionHPSLooseTauBased": "HPS loose",
    "signalAnalysisTauSelectionShrinkingConeCutBased": "Shr. cone",
    "signalAnalysisTauSelectionHPSTightTauNoRtauBased": "HPS tight no R_{#tau}",
    "signalAnalysisTauSelectionHPSMediumTauNoRtauBased": "HPS medium no R_{#tau}",
    "signalAnalysisTauSelectionHPSLooseTauNoRtauBased": "HPS loose no R_{#tau}",
    "signalAnalysisTauSelectionShrinkingConeCutNoRtauBased": "Shr. cone no R_{#tau}"
}

def dashed(style):
    return styles.StyleCompound([style, styles.StyleLine(lineStyle=3)])

plotStyles = {
    "signalAnalysisTauSelectionHPSTightTauBased": styles.styles[0],
    "signalAnalysisTauSelectionHPSMediumTauBased": styles.styles[1],
    "signalAnalysisTauSelectionHPSLooseTauBased": styles.styles[2],
    "signalAnalysisTauSelectionShrinkingConeCutBased": styles.styles[3],
    "signalAnalysisTauSelectionHPSTightTauNoRtauBased": dashed(styles.styles[0]),
    "signalAnalysisTauSelectionHPSMediumTauNoRtauBased": dashed(styles.styles[1]),
    "signalAnalysisTauSelectionHPSLooseTauNoRtauBased": dashed(styles.styles[2]),
    "signalAnalysisTauSelectionShrinkingConeCutNoRtauBased": dashed(styles.styles[3]),
}

def main():
    analyses = [
        "signalAnalysisTauSelectionHPSTightTauNoRtauBased",
        "signalAnalysisTauSelectionHPSMediumTauNoRtauBased",
        "signalAnalysisTauSelectionHPSLooseTauNoRtauBased",
        "signalAnalysisTauSelectionShrinkingConeCutNoRtauBased",
        "signalAnalysisTauSelectionHPSTightTauBased",
        "signalAnalysisTauSelectionHPSMediumTauBased",
        "signalAnalysisTauSelectionHPSLooseTauBased",
        "signalAnalysisTauSelectionShrinkingConeCutBased",
        ]
    datasetManagers = DatasetManagers(analyses, mergeAllMC=True)

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    #transverseMass(Plot(datasetManagers, "TTJets", "transverseMass"), name="TTJets_transverseMass", rebin=10)
    transverseMass(Plot(datasetManagers, "MC", "transverseMass"), name="MCSum_transverseMass", rebin=10)
    transverseMass(Plot(datasetManagers, "Data", "transverseMass"), name="Data_transverseMass", rebin=10, log=False)

    print datasetManagers.getMainCounterTable("Data").format()

class DatasetManagers:
    def __init__(self, analyses, mergeAllMC=False):
        self.analyses = analyses
        self.datasetManagers = []
        for an in analyses:
            dm = dataset.getDatasetsFromMulticrabCfg(counters=an+"Counters/weighted")
            dm.loadLuminosities()
            plots.mergeRenameReorderForDataMC(dm)
            if mergeAllMC:
                dm.mergeMC()
            self.datasetManagers.append(dm)

    def getAnalyses(self):
        return self.analyses

    def getDatasetRootHistos(self, datasetName, histoName):
        ret = []
        for an, dm in zip(self.analyses, self.datasetManagers):
            ret.append(dm.getDataset(datasetName).getDatasetRootHisto(an+"/"+histoName))
        return ret

    def getMainCounterTable(self, dataset):
        table = counter.CounterTable()
        for an, dm in zip(self.analyses, self.datasetManagers):
            eventCounter = counter.EventCounter(dm)
            eventCounter.normalizeMCByLuminosity()

            tmpTable = eventCounter.getMainCounterTable()
            col = tmpTable.getColumn(name=dataset)
            col.setName(legends[an])
            table.appendColumn(col)
        return table


class Plot(plots.PlotBase):
    def __init__(self, datasetManagers, datasetName, histoName, **kwargs):
        self.datasetManagers = datasetManagers
        datasetRootHistos = self.datasetManagers.getDatasetRootHistos(datasetName, histoName)
        for an, drh in zip(self.datasetManagers.getAnalyses(), datasetRootHistos):
            drh.setName(an)
        plots.PlotBase.__init__(self, datasetRootHistos, **kwargs)

        #self.histoMgr.normalizeToOne()
        self.histoMgr.normalizeMCByCrossSection()
        self.histoMgr.forEachHisto(plots.SetPlotStyle(plotStyles))
        self.histoMgr.setHistoLegendLabelMany(legends)


def transverseMass(h, name="transverseMass", rebin=2, log=True):
#    name = h.getRootHistoPath()
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    xlabel = "m_{T}(#tau jet, MET) (GeV/c^{2})" 
    ylabel = "A.u."

  
#    h.stackMCHistograms()
#    h.addMCUncertainty()
    opts = {"xmax": 200}
#    opts = {"ymin": 0.0001,"xmax": 200, "ymaxfactor": 1.3}
#    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    opts = {"xmax": 200}

    if log:
        name += "_log"
        opts["ymin"] = 1e-4
        opts["ymaxfactor"] = 2

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    legend = histograms.createLegend()
    if log:
        h.getPad().SetLogy(True)
        histograms.moveLegend(legend, dx=-0.5, dy=-0.3)
    h.setLegend(legend)
        
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
#    h.addLuminosityText()
    h.save()



if __name__ == "__main__":
    main()
