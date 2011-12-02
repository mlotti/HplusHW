#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to normal data
# within the signal analysis. The corresponding python job
# configurations are
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1"
# * signalAnalysis_cfg.py
# for embedding+signal analysis and signal analysis, respectively
#
# Authors: Matti Kortelainen
#
######################################################################

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

# Configuration
#analysis = "signalAnalysis"
analysis = "signalAnalysisTauSelectionHPSTightTauBased"
counters = analysis+"Counters/weighted"
prefix = "TauEmbeddingDataSignalAnalysisData"

embeddingSignalAnalysis = "."
signalAnalysis = "../../multicrab_signalAnalysis_tauIdScan_110411_165833"

useData = True
useData = False

embeddingNormalisation = dataset.Count(0.700, 0.345)
if not useData:
    embeddingNormalisation = dataset.Count(0.369, 0.042) # MC
    prefix = prefix.replace("Data", "MC")

# main function
def main():
    # Read the datasets
    # Take only TT+W from signal analysis, and data from embedding+signal analysis
    datasetsEmbSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=embeddingSignalAnalysis+"/multicrab.cfg", counters=counters)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=signalAnalysis+"/multicrab.cfg", counters=counters)


    # Select only data from embedded
    datasetsEmbSig.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasetsEmbSig)
    if useData:
        datasetsEmbSig.selectAndReorder(datasetsEmbSig.getDataDatasetNames())
    else:
        mcNames = filter(lambda name: "TTToHplus" not in name, datasetsEmbSig.getMCDatasetNames())
        print "Merging MC"
        print "  "+"\n  ".join(mcNames)
        datasetsEmbSig.merge("MC", mcNames)
        datasetsEmbSig.selectAndReorder(["Data", "MC"])

    # Select only data from original
    datasetsSig.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasetsSig)
    sigLumi = datasetsSig.getDataset("Data").getLuminosity()
    if useData:
        datasetsSig.selectAndReorder(datasetsSig.getDataDatasetNames())
    else:
        datasetsSig.remove(["WW_TuneZ2", "WZ_TuneZ2", "ZZ_TuneZ2"])
        mcNames = filter(lambda name: "TTToHplus" not in name, datasetsSig.getMCDatasetNames())
        print "Merging MC"
        print "  "+"\n  ".join(mcNames)
        datasetsSig.merge("MC", mcNames)
        datasetsSig.selectAndReorder(["Data", "MC"])

    print "Embedding luminosity %f" % datasetsEmbSig.getDataset("Data").getLuminosity()
    print "Normal    luminosity %f" % datasetsSig.getDataset("Data").getLuminosity()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    histograms.createLegend.setDefaults(y1=0.7)


    # Wrapper to decrease typing and have the common options
    def createPlot(plot, *args):
        kwargs = {}
        kwargs["saveFormats"] = [".png"]
        return Plot(datasetsEmbSig, datasetsSig, analysis+"/"+plot, *args, **kwargs)

    transverseMass(createPlot("transverseMass"), rebin=20)

    print "============================================================"
    print "Main counter"
    print getMainCounterTable(datasetsEmbSig, datasetsSig).format()

def getMainCounterTable(emb, sig):
    ec = counter.EventCounter(emb)
    ec2 = counter.EventCounter(sig)

    colName = "Data"
    if not useData:
        ec.normalizeMCByLuminosity()
        ec2.normalizeMCByLuminosity()
        colName = "MC"

    table = counter.CounterTable()
    col = ec.getMainCounterTable().getColumn(name=colName)
    col.setName("Embedded")
    table.appendColumn(col)
    col = col.copy()
    col.setName("Embedded (norm)")
    col.multiply(embeddingNormalisation.value(), embeddingNormalisation.uncertainty())
    table.appendColumn(col)

    col = ec2.getMainCounterTable().getColumn(name=colName)
    col.setName("Normal")
    table.appendColumn(col)
        
    return table


class Plot(plots.ComparisonPlot):
    def __init__(self, datasetsEmbSig, datasetsSig, path, normalizeToOne=False, **kwargs):
        dataset = "Data"
        if not useData:
            dataset = "MC"

        self.name = path.split("/")[-1]
        hEmb = datasetsEmbSig.getDataset(dataset).getDatasetRootHisto(path)
        hEmb.setName(self.name+"Embedded")
        hSig = datasetsSig.getDataset(dataset).getDatasetRootHisto(path)
        hSig.setName(self.name+"Normal")
        if not useData:
            hEmb.normalizeToLuminosity(datasetsEmbSig.getDataset("Data").getLuminosity())
            hSig.normalizeToLuminosity(datasetsSig.getDataset("Data").getLuminosity())

        plots.ComparisonPlot.__init__(self, hEmb, hSig, **kwargs)

        self.normalizeToOne = normalizeToOne
        if normalizeToOne:
            self.histoMgr.normalizeToOne()

        sg = styles.generator()
        sg.reset(1)
        self.histoMgr.forHisto(self.name+"Embedded", sg)
        self.histoMgr.forHisto(self.name+"Normal", styles.dataStyle)
        self.histoMgr.setHistoDrawStyleAll("EP")
        self.histoMgr.setHistoLegendStyleAll("p")

        s = "(Data)"
        if not useData:
            s = "(MC)"

        self.histoMgr.setHistoLegendLabelMany({self.name+"Embedded": "Embedded "+s,
                                               self.name+"Normal": "Normal "+s})

        self.histoMgr.forHisto(self.name+"Embedded", lambda h: normaliseEmbedding(h.getRootHisto()))

def normaliseEmbedding(th1):
    for bin in xrange(0, th1.GetNbinsX()+1):
        value = dataset.Count(th1.GetBinContent(bin), th1.GetBinError(bin))
        value.multiply(embeddingNormalisation)

        th1.SetBinContent(bin, value.value())
        th1.SetBinError(bin, value.uncertainty())

def transverseMass(h, rebin=5, ratio=False, particle="#tau"):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(%s, MET) (GeV/c^{2})" % particle
    ylabel = "Events / %.2f GeV/c^{2}" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
    opts["xmax"] = 200

    name = prefix+"_"+h.name
    h.createFrame(name, createRatio=ratio, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()

    name += "_log"
    h.createFrame(name, createRatio=ratio, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()


if __name__ == "__main__":
    main()
