# tau embedding related plotting stuff

import math
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import dataset
import histograms
import plots
import counter

# Apply embedding normalization (muon efficiency, W->tau->mu factor
normalize = True
# Data era
era = "Run2011A"

# When doing the averaging, take the stat uncertainty as the average
# of the stat uncertanties of the trials
uncertaintyByAverage = False

datasetAllEvents = {
    "TTJets_TuneZ2_Summer11": (3701947, {"Run2011A": 3693782.50}),
    # Not all events were processed for pattuples
    "WJets_TuneZ2_Summer11": (None, {"Run2011A": 82207600.00/81352576}),
    "W3Jets_TuneZ2_Summer11": (7685944, {"Run2011A": 7688457.50}),
    "DYJetsToLL_M50_TuneZ2_Summer11": (33576416, {"Run2011A": 33556404.00}),
    # Not all events were processed for pattuples
    "DYJetsToLL_M50_TuneZ2_Summer11": (None, {"Run2011A": 33556404.00/33576416}),
    "T_t-channel_TuneZ2_Summer11": (3900171, {"Run2011A": 3906455.50}),
    "Tbar_t-channel_TuneZ2_Summer11": (1944826, {"Run2011A": 1949474.6}),
    "T_tW-channel_TuneZ2_Summer11": (814390, {"Run2011A": 807697.38}),
    "Tbar_tW-channel_TuneZ2_Summer11": (809984, {"Run2011A": 797144.94}),
    "T_s-channel_TuneZ2_Summer11": (259971, {"Run2011A": 261646.25}),
    "Tbar_s-channel_TuneZ2_Summer11": (137980, {"Run2011A": 139142.36}),
    "WW_TuneZ2_Summer11": (4225916, {"Run2011A": 4226660.50}),
    "WZ_TuneZ2_Summer11": (4265243, {"Run2011A": 4272549.50}),
    "ZZ_TuneZ2_Summer11": (4187885, {"Run2011A": 4197760.00}),
}

# Signal analysis multicrab directories for embedding trials
dirEmbs_120131 = [
    "multicrab_signalAnalysis_Met50_systematics_v13_3_Run2011A_120131_123142",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest1_Run2011A_120131_133727",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest2_Run2011A_120131_135817",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest3_Run2011A_120131_141821",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest4_Run2011A_120131_143855",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest5_Run2011A_120131_145907",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest6_Run2011A_120131_152041",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest7_Run2011A_120131_154149",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest8_Run2011A_120131_160339",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest9_Run2011A_120131_162422",
]
dirEmbs = dirEmbs_120131

# Signal analysis multicrab directory for normal MC
dirSig = "../multicrab_compareEmbedding_Run2011A_120118_122555" # for 120118, 120126, 120131

########################################
# Update all event counts to the ones taking into account the pileup reweighting
def updateAllEventsToWeighted(datasets):
    # If DatasetsMany or similar
    if hasattr(datasets, "datasetManagers"):
        for ds in datasets.datasetManagers:
            updateAllEventsToWEighted(ds)
        return

    for name, tpl in datasetAllEvents.iteritems():
        if not datasets.hasDataset(name):
            continue
        dataset = datasets.getDataset(name)
        (N, weightedN) = tpl
        nAllEvents = dataset.getNAllEvents()
        if N != None:
            if nAllEvents != N:
                raise Exception("Datasets %s, number of all events is %d, expected %d" % (name, nAllEvents, N))
            dataset.setNAllEvents(weightedN[era])
        else:
            dataset.setNAllEvents(weightedN[era]*nAllEvents) # There is some fluctuation in the exact counts of DYJets and WJets between trials


########################################
# Embedding normalization
def scaleNormalization(obj):
    if not normalize:
        return

    #scaleMCfromWmunu(obj) # data/MC trigger correction
    scaleMuTriggerIdEff(obj)
    scaleWmuFraction(obj)
    return

def scaleMuTriggerIdEff(obj):
    # From 2011A only
    #data = 0.508487
    #mc = 0.541083
    # May10 in 41X
    #data = 0.891379
    #mc = 0.931707
    # 1fb in 42X
    data = None
    if era == "EPS":
        data = 0.884462
    elif era == "Run2011A-EPS":
        data = 0.879
    elif era == "Run2011A":
        data = 0.881705
    mc = 0.919829

    scaleHistosCounters(obj, scaleDataHisto, "scaleData", 1/data)
    scaleHistosCounters(obj, scaleMCHisto, "scaleMC", 1/mc)

def scaleWmuFraction(obj):
    Wtaumu = 0.038479

    scaleHistosCounters(obj, scaleHisto, "scale", 1-Wtaumu)

def scaleHistosCounters(obj, plotFunc, counterFunc, scale):
    if isinstance(obj, plots.PlotBase):
        scaleHistos(obj, plotFunc, scale)
    elif isinstance(obj, counter.EventCounter):
        scaleCounters(obj, counterFunc, scale)
    else:
        plotFunc(obj, scale)

def scaleHistos(plot, function, scale):
    plot.histoMgr.forEachHisto(lambda histo: function(histo, scale))

def scaleCounters(eventCounter, methodName, scale):
    getattr(eventCounter, methodName)(scale)

def scaleMCHisto(histo, scale):
    if histo.isMC():
        scaleHisto(histo, scale)

def scaleDataHisto(histo, scale):
    if histo.isData():
        scaleHisto(histo, scale)

def scaleHisto(histo, scale):
    th1 = histo.getRootHisto()
    th1.Scale(scale)


########################################
# helper function
def squareSum(th1):
    s = 0
    for bin in xrange(0, th1.GetNbinsX()+2):
        #print "Bin %d, low edge %.1f, value %f" % (bin, th1.GetBinLowEdge(bin), th1.GetBinContent(bin))
        value = th1.GetBinContent(bin)
        s += value*value
    return s


########################################
# Classes for doing the averaging
class DatasetsMany:
    def __init__(self, dirs, counters, normalizeMCByLuminosity=False):
        self.datasetManagers = []
        for d in dirs:
            datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=d+"/multicrab.cfg", counters=counters)
            datasets.loadLuminosities()
            updateAllEventsToWeighted(datasets)
            self.datasetManagers.append(datasets)

        self.normalizeMCByLuminosity=normalizeMCByLuminosity

    def forEach(self, function):
        for dm in self.datasetManagers:
            function(dm)

    def getFirstDatasetManager(self):
        return self.datasetManagers[0]

    # Compatibility with dataset.DatasetManager
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    def getAllDatasetNames(self):
        return self.datasetManagers[0].getAllDatasetNames()

    def close(self):
        self.forEach(lambda d: d.close())

    # End of compatibility methods
    def getDatasetFromFirst(self, name):
        return self.getFirstDatasetManager().getDataset(name)

    def setLumiFromData(self):
        self.lumi = self.getDatasetFromFirst("Data").getLuminosity()

    def getLuminosity(self):
        return self.lumi

    def getHistogram(self, datasetName, name, rebin=1):
        histos = self.getHistograms(datasetName, name)

        # Averaging is done here
        histo = histos[0]
        histo_low = histo.Clone(histo.GetName()+"_low")
        histo_high = histo.Clone(histo.GetName()+"_high")
        for h in histos[1:]:
            for bin in xrange(0, histo.GetNbinsX()+2):
                histo.SetBinContent(bin, histo.GetBinContent(bin)+h.GetBinContent(bin))
                if uncertaintyByAverage:
                    histo.SetBinError(bin, histo.GetBinError(bin)+h.GetBinError(bin))
                else:
                    histo.SetBinError(bin, math.sqrt(histo.GetBinError(bin)**2+h.GetBinError(bin)**2))

                histo_low.SetBinContent(bin, min(histo_low.GetBinContent(bin), h.GetBinContent(bin)))
                histo_high.SetBinContent(bin, max(histo_high.GetBinContent(bin), h.GetBinContent(bin)))

        for bin in xrange(0, histo.GetNbinsX()+2):
            histo.SetBinContent(bin, histo.GetBinContent(bin)/len(histos))
            if uncertaintyByAverage:
                histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))
            else:
                histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))

        if rebin > 1:
            histo.Rebin(rebin)
            histo_low.Rebin(rebin)
            histo_high.Rebin(rebin)

        binCenters = []
        values = []
        errLow = []
        errHigh = []
        for bin in xrange(1, histo.GetNbinsX()+1):
            binCenters.append(histo.GetXaxis().GetBinCenter(bin))
            values.append(histo.GetBinContent(bin))
            errLow.append(histo.GetBinContent(bin) - histo_low.GetBinContent(bin))
            errHigh.append(histo_high.GetBinContent(bin) - histo.GetBinContent(bin))

        gr = ROOT.TGraphAsymmErrors(len(binCenters),
                                    array.array("d", binCenters), array.array("d", values),
                                    array.array("d", [0]*len(binCenters)), array.array("d", [0]*len(binCenters)),
                                    array.array("d", errLow), array.array("d", errHigh))

        histo.SetName("Average")

        return (histo, gr) # Average histogram, min/max graph

    def getEfficiency(self, datasetName, numerator, denominator):
        effs = []
        for dm in self.datasetManagers:
            ds = dm.getDataset(datasetName)
            num = ds.getDatasetRootHisto(numerator).getHistogram()
            den = ds.getDatasetRootHisto(denominator).getHistogram()

            eff = ROOT.TEfficiency(num, den)
            effs.append(eff)

        # Here we use merging, as the trials are just about extending statistics
        result = effs[0]
        for e in effs[1:]:
            result.Add(e)
        return result

    def hasHistogram(self, datasetName, name):
        has = True
        for dm in self.datasetManagers:
            has = has and dm.getDataset(datasetName).hasRootHisto(name)
        return has

    def getHistograms(self, datasetName, name):
        histos = []
        for i, dm in enumerate(self.datasetManagers):
            ds = dm.getDataset(datasetName)
            h = ds.getDatasetRootHisto(name)
            if h.isMC() and self.normalizeMCByLuminosity:
                h.normalizeToLuminosity(self.lumi)
            h = histograms.HistoWithDataset(ds, h.getHistogram(), "dummy") # only needed for scaleNormalization()
            scaleNormalization(h)
            h = h.getRootHisto()
            h.SetName("Trial %d"%(i+1))
            histos.append(h)

        return histos # list of individual histograms

    def getCounter(self, datasetName, name):
        (embDataHisto, tmp) = self.getHistogram(datasetName, name)
        return counter.HistoCounter(datasetName, embDataHisto)


class EventCounterMany:
    def __init__(self, datasetsMany, normalize=True, *args, **kwargs):
        self.eventCounters = []
        for dsMgr in datasetsMany.datasetManagers:
            ec = counter.EventCounter(dsMgr, *args, **kwargs)
            ec.normalizeMCToLuminosity(datasetsMany.getLuminosity())
            if normalize:
                scaleNormalization(ec)
            self.eventCounters.append(ec)

    def removeColumns(self, datasetNames):
        for ec in self.eventCounters:
            ec.removeColumns(datasetNames)

    def mainCounterAppendRow(self, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getMainCounter().appendRow(*args, **kwargs)

    def subCounterAppendRow(self, name, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getSubCounter(name).appendRow(*args, **kwargs)

    def getMainCounterTable(self):
        return counter.meanTable([ec.getMainCounterTable() for ec in self.eventCounters], uncertaintyByAverage)

    def getSubCounterTable(self, name):
        return counter.meanTable([ec.getSubCounterTable(name) for ec in self.eventCounters], uncertaintyByAverage)

    def getMainCounterTableFit(self):
        return counter.meanTableFit([ec.getMainCounterTable() for ec in self.eventCounters])

    def getSubCounterTableFit(self, name):
        return counter.meanTableFit([ec.getSubCounterTable(name) for ec in self.eventCounters])

    def getNormalizationString(self):
        return self.eventCounters[0].getNormalizationString()

########################################
# Common plot drawer
class PlotDrawerTauEmbedding(plots.PlotDrawer):
    def __init__(self, **kwargs):
        plots.PlotDrawer.__init__(self, normalize=True, **kwargs)
        self.normalizeDefault = normalize

    def __call__(self, p, name, xlabel, **kwargs):
        self.rebin(p, **kwargs)

        if kwargs.get("normalize", self.normalizeDefault):
            scaleNormalization(p)

        self.stackMCHistograms(p, **kwargs)
        self.createFrame(p, name, **kwargs)
        self.setLegend(p, **kwargs)
        self.addCutLineBox(p, **kwargs)
        self.finish(p, xlabel, **kwargs)

drawPlot = PlotDrawerTauEmbedding(ylabel="Events / %.0f GeV/c", log=True, stackMCHistograms=True, addMCUncertainty=True)
