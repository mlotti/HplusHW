## \package tauEmbedding
# Tau embedding (EWK+ttbar tau background measurement) related plotting utilities

import math
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import dataset
import histograms
import plots
import counter
import styles

## Apply embedding normalization (muon efficiency, W->tau->mu factor
normalize = True
## Data era
era = "Run2011A"

## When doing the averaging, take the stat uncertainty as the average of the stat uncertanties of the trials
uncertaintyByAverage = False

## Number of PU-reweighted all events for datasets
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

## Signal analysis multicrab directories for embedding trials
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
## Signal analysis multicrab directories for embedding trials
#
# This variable is used to select from possibly multiple sets of embedding directories
dirEmbs = dirEmbs_120131

## Signal analysis multicrab directory for normal MC
dirSig = "../multicrab_compareEmbedding_Run2011A_120118_122555" # for 120118, 120126, 120131


## Update all event counts to the ones taking into account the pileup reweighting
#
# \param datasets   dataset.DatasetManager object
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


## Apply embedding normalization
#
# \param obj  plots.PlotBase, histograms.Histo, or counter.EventCounter object
#
# The normalization includes the muon trigger and ID efficiency, and W->tau->mu fraction
def scaleNormalization(obj):
    if not normalize:
        return

    #scaleMCfromWmunu(obj) # data/MC trigger correction
    scaleMuTriggerIdEff(obj)
    scaleWmuFraction(obj)

## Apply muon trigger and ID efficiency normalization
#
# \param obj  plots.PlotBase, histograms.Histo, or counter.EventCounter object
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

## Apply W->tau->mu normalization
#
# \param obj  plots.PlotBase, histograms.Histo, or counter.EventCounter object
def scaleWmuFraction(obj):
    Wtaumu = 0.038479

    scaleHistosCounters(obj, scaleHisto, "scale", 1-Wtaumu)

## Helper function to scale histos or counters
#
# \param obj          plots.PlotBase, histograms.Histo, or counter.EventCounter object
# \param plotFunc     Function to apply for plots.PlotBase and histograms.Histo objects
# \param counterFunc  Name of counter.EventCounter function to apply
# \param scale        Multiplication factor
def scaleHistosCounters(obj, plotFunc, counterFunc, scale):
    if isinstance(obj, plots.PlotBase):
        scaleHistos(obj, plotFunc, scale)
    elif isinstance(obj, counter.EventCounter):
        scaleCounters(obj, counterFunc, scale)
    else:
        plotFunc(obj, scale)

## Helper function to scale plots.PlotBase objects
#
# \param plot       plots.PlotBase object
# \param function   Function to apply
# \param scale      Multiplication factor
def scaleHistos(plot, function, scale):
    plot.histoMgr.forEachHisto(lambda histo: function(histo, scale))

## Helper function to scale counter.EventCounter
#
# \param eventCounter  counter.EventCounter object
# \param methodName    Name of the counter.EventCounter method to apply
# \param scale         Multiplication factor
def scaleCounters(eventCounter, methodName, scale):
    getattr(eventCounter, methodName)(scale)

## Helper function to scale only MC histograms.Histo objects
#
# \param histo   histograms.Histo object
# \param scale   Multiplication factor
def scaleMCHisto(histo, scale):
    if histo.isMC():
        scaleHisto(histo, scale)

## Helper function to scale only data histograms.Histo objects
#
# \param histo   histograms.Histo object
# \param scale   Multiplication factor
def scaleDataHisto(histo, scale):
    if histo.isData():
        scaleHisto(histo, scale)

## Helper function to scale histograms.Histo objects
#
# \param histo   histograms.Histo object
# \param scale   Multiplication factor
def scaleHisto(histo, scale):
    th1 = histo.getRootHisto()
    th1.Scale(scale)


## Calculate square sum of TH1 bins
def squareSum(th1):
    s = 0
    for bin in xrange(0, th1.GetNbinsX()+2):
        #print "Bin %d, low edge %.1f, value %f" % (bin, th1.GetBinLowEdge(bin), th1.GetBinContent(bin))
        value = th1.GetBinContent(bin)
        s += value*value
    return s


## Class for doing the averaging over many dataset.DatasetManager objects
class DatasetsMany:
    ## Constructor
    #
    # \param dirs                      List of paths multicrab directories, either absolute or relative to working directory
    # \param counters                  Directory in dataset TFiles containing the event counters
    # \param normalizeMCByLuminosity   Normalize MC to data luminosity?
    #
    # Construct a dataset.DatasetManager object from each multicrab directory
    def __init__(self, dirs, counters, normalizeMCByLuminosity=False):
        self.datasetManagers = []
        for d in dirs:
            datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=d+"/multicrab.cfg", counters=counters)
            datasets.loadLuminosities()
            updateAllEventsToWeighted(datasets)
            self.datasetManagers.append(datasets)

        self.normalizeMCByLuminosity=normalizeMCByLuminosity

    ## Apply a function for each dataset.DatasetManager object
    def forEach(self, function):
        for dm in self.datasetManagers:
            function(dm)

    ## Get dataset.DatasetManager object from the first multicrab directory
    def getFirstDatasetManager(self):
        return self.datasetManagers[0]

    ## Remove dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \param args    Positional arguments (forwarded to dataset.Dataset.remove())
    # \param kwargs  Keyword arguments (forwarded to dataset.Dataset.remove())
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    ## Get a list of names of all dataset.Dataset objects (compatibility with dataset.DatasetManager)
    def getAllDatasetNames(self):
        return self.datasetManagers[0].getAllDatasetNames()

    ## Close all TFiles of the contained dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \see dataset.DatasetManager.close()
    def close(self):
        self.forEach(lambda d: d.close())

    
    ## Get dataset.Dataset object from the first dataset.DatasetManager
    #
    # \param name   Name of the dataset
    def getDatasetFromFirst(self, name):
        return self.getFirstDatasetManager().getDataset(name)

    ## Set the integrated luminosity from data dataset
    def setLumiFromData(self):
        self.lumi = self.getDatasetFromFirst("Data").getLuminosity()

    ## Get the integrated luminosity
    def getLuminosity(self):
        return self.lumi

    ## Get a ROOT histogram for a given dataset, averaged over the multiple dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram (or dataset.TreeDraw object)
    # \param rebin         Rebin
    #
    # \return tuple of (histogram, min_max_graph)
    #
    # The min/max graph has the average as the value, and for each bin
    # the minimum and maximum in the asymmetric errors.
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

    ## Create TEfficiency for a given dataset, merged over the multiple dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param numerator     Name of the numerator histogram
    # \param denominator   Name of the denominator histogram
    #
    # \return TEfficiency object 
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

    ## Check if a histogram exists for all dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram to check
    def hasHistogram(self, datasetName, name):
        has = True
        for dm in self.datasetManagers:
            has = has and dm.getDataset(datasetName).hasRootHisto(name)
        return has

    ## Get the ROOT histograms of a given name from all dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the ROOT histogram
    #
    # \return list of ROOT histograms
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

    ## Get a counter.HistoCounter for a given dataset and counter
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the counter ROOT histogram
    #
    # \return counter.HistoCounter object
    def getCounter(self, datasetName, name):
        (embDataHisto, tmp) = self.getHistogram(datasetName, name)
        return counter.HistoCounter(datasetName, embDataHisto)

## Class for obtaining the residual MC results
class DatasetsResidual:
    ## Constructor
    #
    # \param datasetsEmb    tauEmbedding.DatasetsMany object for embedding datasets
    # \param datasetsSig    dataset.DatasetManager obejct for normal MC
    # \param analysisEmb    Analysis directory for embeddded datasets (directory containing the ROOT histograms in the TFile)
    # \param analysisSig    Analysis directory for normal MC datasets (directory containing the ROOT histograms in the TFile)
    # \param residualNames  List of names of the datasets for which to derive the residuals (e.g. DYJetsToLL and WW)
    # \param totalNames     List of names of "total" datasets, for which to add the residual MC on top of the original contribution (e.g. emb.data+res.MC and emb.MC+res.MC)
    def __init__(self, datasetsEmb, datasetsSig, analysisEmb, analysisSig, residualNames, totalNames=[]):
        self.datasetsEmb = datasetsEmb
        self.datasetsSig = datasetsSig

        # For an ugly hack
        self.analysisEmb = analysisEmb
        self.analysisSig = analysisSig

        self.residualNames = residualNames
        self.totalNames = totalNames
        for name in totalNames:
            if name in residualNames:
                raise Exception("residualNames and totalNames must be disjoint (dataset '%s' was given in both)")

    ## Replace embedding analysis directory name with a normal MC analysis directory
    #
    # \param name  Histogram name, or dataset.TreeDraw object
    def _replaceSigName(self, name):
        if isinstance(name, basestring):
            return name.replace(self.analysisEmb, self.analysisSig)
        else:
            return name.clone(tree=lambda name: name.replace(self.analysisEmb, self.analysisSig))

    ## Apply a function for each dataset.DatasetManager object
    def forEach(self, function):
        self.datasetsEmb.forEach(function)
        function(self.datasetsSig)

    ## Remove dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \param args    Positional arguments (forwarded to dataset.Dataset.remove())
    # \param kwargs  Keyword arguments (forwarded to dataset.Dataset.remove())
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    ## Get a list of names of all dataset.Dataset objects (compatibility with dataset.DatasetManager)
    def getAllDatasetNames(self):
        return self.datasetsEmb.getAllDatasetNames()

    ## Close all TFiles of the contained dataset.Dataset objects (compatibility with dataset.DatasetManager)
    #
    # \see dataset.DatasetManager.close()
    def close(self):
        self.forEach(self, lambda d: d.close())


    ## Ask if the residual MC is added to a given dataset
    #
    # \param datasetName   Dataset name
    #
    # \return  True, if residual MC has been added for this dataset
    def isResidualAdded(self, datasetName):
        return datasetName in self.totalNames or datasetName in self.residualNames

    ## Get the integrated luminosity
    def getLuminosity(self):
        return self.datasetsEmb.getLuminosity()

    ## Check if a histogram exists for all dataset.DatasetManager objects
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram to check
    def hasHistogram(self, datasetName, name):
        return self.datasetsEmb.hasHistogram(datasetName, name) and self.datasetsSig.getDataset(datasetName).hasHistogram(name)

    ## Get a ROOT histogram for a given dataset
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the histogram (or dataset.TreeDraw object)
    # \param rebin         Rebin
    #
    # If dataset is not in \a totalNames nor \a residual names, return
    # the embedded result (averaged over multiple dataset.DatasetManager object).
    #
    # If dataset is in \a residualNames, calculate the residual result
    # as normal-embedded.
    #
    # If dataset is in \a totalNames, calculate sum of total_emb + sum(res_mc)
    def getHistogram(self, datasetName, name, rebin=1):
        if datasetName in self.totalNames:
            #print "Creating sum for "+datasetName
            (histo, tmp) = self.datasetsEmb.getHistogram(datasetName, name, rebin)
            for res in self.residualNames:
                #print "From residual of "+res
                (h, tmp) = self.getHistogram(res, name, rebin)
                histo.Add(h)
            return (histo, None)
        elif not datasetName in self.residualNames:
            return self.datasetsEmb.getHistogram(datasetName, name)

        #print "Calculating residual of "+datasetName

        # Ugly hack
        sigName = self._replaceSigName(name)

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        sigHisto = self.datasetsSig.getDataset(datasetName).getDatasetRootHisto(sigName) # DatasetRootHisto
        sigHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigHisto = sigHisto.getHistogram() # ROOT.TH1

        # residual = normal-embedded
        sigHisto.Add(embHisto, -1)

        sigHisto.SetName(embHisto.GetName()+"Residual")
        if rebin > 1:
            sigHisto.Rebin(rebin)

        return (sigHisto, None)

    ## Get a counter.HistoCounter for a given dataset and counter
    #
    # \param datasetName   Name of the dataset
    # \param name          Name of the counter ROOT histogram
    #
    # \return counter.HistoCounter object
    #
    # For datasets not in \a residualNames, return the embedded result
    #
    # For datasets in \a residualNames, calculate the result as normal-embedded
    def getCounter(self, datasetName, name):
        if not datasetName in self.residualNames:
            return self.datasetsEmb.getCounter(datasetName, name)

        # Ugly hack
        sigName = name
        if isinstance(sigName, basestring):
            sigName = sigName.replace(self.analysisEmb, self.analysisSig)
        else:
            sigName = sigName.clone(tree=sigName.tree.replace(self.analysisEmb, self.analysisSig))

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        sigHisto = self.datasetsSig.getDataset(datasetName).getDatasetRootHisto(sigName) # DatasetRootHisto
        sigHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigHisto = sigHisto.getHistogram() # ROOT.TH1

        table = counter.CounterTable()
        table.appendColumn(counter.HistoCounter("Embedded", embHisto))
        table.appendColumn(counter.HistoCounter("Normal", sigHisto))
        table.removeNonFullRows()

        embColumn = table.getColumn(name="Embedded")
        sigColumn = table.getColumn(name="Normal")
        residual = counter.subtractColumn(datasetName+" residual", sigColumn, embColumn)
        return residual

## Event counter for doing the averaging over many datasets.DatasetManager objects
class EventCounterMany:
    ## Constructor
    #
    # \param datasetsMany   tauEmbedding.DatasetsMany object
    # \param normalize      Apply embedding normalization?
    # \param args           Positional arguments (forwarded to counter.EventCounter.__init__())
    # \param kwargs         Keyword arguments (forwarded to counter.EventCounter.__init__())
    def __init__(self, datasetsMany, normalize=True, *args, **kwargs):
        self.eventCounters = []
        for dsMgr in datasetsMany.datasetManagers:
            ec = counter.EventCounter(dsMgr, *args, **kwargs)
            ec.normalizeMCToLuminosity(datasetsMany.getLuminosity())
            if normalize:
                scaleNormalization(ec)
            self.eventCounters.append(ec)

    ## Remove columns
    #
    # \param datasetNames   List of dataset names to remove
    def removeColumns(self, datasetNames):
        for ec in self.eventCounters:
            ec.removeColumns(datasetNames)

    ## Append row from TTree to main counter
    #
    # \param args   Positional arguments (forwarded to counter.Counter.appendRow())
    # \param kwargs Keyword arguments (forwarded to counter.Counter.appendRow())
    def mainCounterAppendRow(self, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getMainCounter().appendRow(*args, **kwargs)

    ## Append row from TTree to a sub counter
    #
    # \param name   Name of the subcounter
    # \param args   Positional arguments (forwarded to counter.Counter.appendRow())
    # \param kwargs Keyword arguments (forwarded to counter.Counter.appendRow())
    def subCounterAppendRow(self, name, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getSubCounter(name).appendRow(*args, **kwargs)

    ## Get main counter table
    #
    # \return counter.CounterTable object
    #
    # Calculated as the mean of the counter.CounterTable objects from
    # the individual trials
    def getMainCounterTable(self):
        return counter.meanTable([ec.getMainCounterTable() for ec in self.eventCounters], uncertaintyByAverage)

    ## Get subcounter table
    #
    # \param name  Name of the subcounter
    #
    # \return counter.CounterTable object
    #
    # Calculated as the mean of the counter.CounterTable objects from
    # the individual trials
    def getSubCounterTable(self, name):
        return counter.meanTable([ec.getSubCounterTable(name) for ec in self.eventCounters], uncertaintyByAverage)

    ## Get main counter table from fit
    #
    # \return counter.CounterTable object
    #
    # Calculated with a least-square fit of a zero-order polynomial to
    # counter.CounterTable objects from the individual trials
    def getMainCounterTableFit(self):
        return counter.meanTableFit([ec.getMainCounterTable() for ec in self.eventCounters])

    ## Get subcounter table from fit
    #
    # \param name  Name of the subcounter
    #
    # \return counter.CounterTable object
    #
    # Calculated with a least-square fit of a zero-order polynomial to
    # counter.CounterTable objects from the individual trials
    def getSubCounterTableFit(self, name):
        return counter.meanTableFit([ec.getSubCounterTable(name) for ec in self.eventCounters])

    ## Get current normalization scheme string
    def getNormalizationString(self):
        return self.eventCounters[0].getNormalizationString()

## Event counter for adding the residual MC
class EventCounterResidual:
    ## Constructor
    #
    # \param datasetsResidual  tauEmbedding.DatasetsResidual object
    # \param counters          Name of the counter histogram in the embedded analysis
    # \param kwargs            Keyword arguments (forwarded to counter.EventCounter.__init__())
    def __init__(self, datasetsResidual, counters=None, **kwargs):
        self.datasetsResidual = datasetsResidual
        self.residualNames = datasetsResidual.residualNames

        countersSig = counters
        if countersSig != None:
            countersSig = datasetsResidual._replaceSigName(countersSig)

        self.eventCounterEmb = EventCounterMany(datasetsResidual.datasetsEmb, counters=counters, **kwargs)
        self.eventCounterSig = counter.EventCounter(datasetsResidual.datasetsSig, counters=countersSig, **kwargs)
        self.eventCounterSig.normalizeMCToLuminosity(datasetsResidual.datasetsEmb.getLuminosity())

    ## Append row from TTree to main counter
    #
    # \param rowName   Name of the row
    # \param treeDraw  dataset.TreeDraw object
    #
    # The TTree name should be the one in embedded analysis
    def mainCounterAppendRow(self, rowName, treeDraw):
        treeDrawSig = self.datasetsResidual._replaceSigName(treeDraw)
        self.eventCounterEmb.mainCounterAppendRow(rowName, treeDraw)
        self.eventCounterSig.getMainCounter().appendRow(rowName, treeDrawSig)

    ## Append row from TTree to subcounter
    #
    # \param name      Name of the subcounter
    # \param rowName   Name of the row
    # \param treeDraw  dataset.TreeDraw object
    #
    # The TTree name should be the one in embedded analysis
    def subCounterAppendRow(self, name, rowName, treeDraw):
        treeDrawSig = self.datasetsResidual._replaceSigName(treeDraw)
        self.eventCounterEmb.subCounterAppendRow(name, rowName, treeDraw)
        self.eventCounterSig.getSubCounter(name).appendRow(rowName, treeDrawSig)

    ## Helper function for adding columns for residual datasets
    #
    # \param table     counter.CounterTable for embedding
    # \param sigTable  counter.CounterTable for normal MC
    #
    # \return counter.CounterTable with residual columns added (same object as \a table argument)
    def _calculateResidual(self, table, sigTable):
        columnNames = table.getColumnNames()
        for name in columnNames:
            if name in self.residualNames:
                i = columnNames.index(name)
                col = table.getColumn(index=i)
                table.removeColumn(i)
                col = counter.subtractColumn(name+" residual", sigTable.getColumn(name=name), col)
                table.insertColumn(i, col)
        return table

    ## Get main counter table with residual columns
    #
    # \return counter.CounterTable object
    def getMainCounterTable(self):
        table = self.eventCounterEmb.getMainCounterTable()
        sigTable = self.eventCounterSig.getMainCounterTable()
        
        table = self._calculateResidual(table, sigTable)
        return table

    ## Get subcounter table with residual columns
    #
    # \param name  Name of the subcounter
    #
    # \return counter.CounterTable object
    def getSubCounterTable(self, name):
        table = self.eventCounterEmb.getSubCounterTable(name)
        sigTable = self.eventCounterSig.getSubCounterTable(name)
        
        table = self._calculateResidual(table, sigTable)
        return table


## Plot drawer for embedding plots
#
# Adds the normalization step to the workflow if plots.PlotDrawer
class PlotDrawerTauEmbedding(plots.PlotDrawer):
    ## Constructor
    #
    # \param normalize   Apply embedding normalization
    # \param kwargs      Keyword arguments (forwarded to plots.PlotDrawer.__init__())
    def __init__(self, normalize=True, **kwargs):
        plots.PlotDrawer.__init__(self, **kwargs)
        self.normalizeDefault = normalize

    ## Apply the tau embedding normalization
    #
    # \param p       plots.PlotBase (or deriving) object
    # \param kwargs  Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a normalize   Should embedding normalization be applied? (default given in __init__()/setDefaults())
    def tauEmbeddingNormalization(self, p, **kwargs):
        if kwargs.get("normalize", self.normalizeDefault):
            scaleNormalization(p)

    def __call__(self, p, name, xlabel, **kwargs):
        self.rebin(p, **kwargs)

        self.tauEmbeddingNormalization(p, **kwargs)

        self.stackMCHistograms(p, **kwargs)
        self.createFrame(p, name, **kwargs)
        self.setLegend(p, **kwargs)
        self.addCutLineBox(p, **kwargs)
        self.finish(p, xlabel, **kwargs)

## Default plot drawer object for tau embedding (embedded data vs. embedded MC) plots
drawPlot = PlotDrawerTauEmbedding(ylabel="Events / %.0f GeV/c", log=True, stackMCHistograms=True, addMCUncertainty=True)


## Plot drawer for embedding vs. normal MC plots
#
# More customization is needed for the uncertainties
class PlotDrawerTauEmbeddingEmbeddedNormal(PlotDrawerTauEmbedding):
    ## Constructor
    #
    # \param kwargs      Keyword arguments (forwarded to tauEmbedding.PlotDrawerTauEmbedding.__init__())
    def __init__(self, **kwargs):
        PlotDrawerTauEmbedding.__init__(self, normalize=False, **kwargs)

    def __call__(self, p, name, xlabel, **kwargs):
        self.rebin(p, **kwargs)

        self.tauEmbeddingNormalization(p, **kwargs)

        sigErr = p.histoMgr.getHisto("Normal").getRootHisto().Clone("Normal_err")
        sigErr.SetFillColor(ROOT.kRed-7)
        sigErr.SetMarkerSize(0)
        sigErr.SetFillStyle(3005)
        p.prependPlotObject(sigErr, "E2")
        if p.histoMgr.hasHisto("Embedded"):
            embErr = p.histoMgr.getHisto("Embedded").getRootHisto().Clone("Embedded_err")
            embErr.SetFillColor(ROOT.kBlue-7)
            embErr.SetFillStyle(3004)
            embErr.SetMarkerSize(0)
            p.prependPlotObject(embErr, "E2")

        if hasattr(p, "embeddingVariation"):
            p.prependPlotObject(h.embeddingVariation, "[]")
        if hasattr(p, "embeddingDataVariation"):
            p.prependPlotObject(p.embeddingDataVariation, "[]")

        if kwargs.get("log", self.logDefault):
            name = name+"_log"

        self.createFrame(p, name, **kwargs)
        if kwargs.get("ratio", self.ratioDefault):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            # Very, very ugly hack
            if p.histoMgr.hasHisto("EmbeddedData"):
                if p.ratios[1].getName() != "Embedded":
                    raise Exception("Assumption that [1] is from embedded MC failed")
                p.ratios[1].setDrawStyle("PE2")
                rh = p.ratios[1].getRootHisto()
                rh.SetFillColor(ROOT.kBlue-7)
                rh.SetFillStyle(3004)

        self.setLegend(p, **kwargs)
        # Add the legend box for stat uncertainty band
        tmp = sigErr.Clone("tmp")
        tmp.SetFillColor(ROOT.kBlack)
        tmp.SetFillStyle(3013)
        tmp.SetLineColor(ROOT.kWhite)
        if not p.histoMgr.hasHisto("Embedded"):
            tmp.SetFillStyle(sigErr.GetFillStyle())
            tmp.SetFillColor(sigErr.GetFillColor())
        p.legend.AddEntry(tmp, "Stat. unc.", "F")

        # Add "legend" entries manually for brackets in embedded variations
        x = p.legend.GetX1()
        y = p.legend.GetY1()
        x += 0.05; y -= 0.03
        if hasattr(p, "embeddingDataVariation"):
            p.appendPlotObject(histograms.PlotText(x, y, "[  ]", size=17, color=p.embeddingDataVariation.GetMarkerColor())); x += 0.05
            p.appendPlotObject(histograms.PlotText(x, y, "Embedded data min/max", size=17)); y-= 0.03
        if hasattr(p, "embeddingVariation"):
            p.appendPlotObject(histograms.PlotText(x, y, "[  ]", size=17, color=p.embeddingVariation.GetMarkerColor())); x += 0.05
            p.appendPlotObject(histograms.PlotText(x, y, "Embedded MC min/max", size=17)); y-= 0.03

        self.addCutLineBox(p, **kwargs)
        self.finish(p, xlabel, **kwargs)

## Plot creator for embedded vs. normal plots
class PlotCreatorMany:
    ## Constructor
    #
    # \param analysisEmb    Name of the embedding analysis TDirectory
    # \param analysisSig    Name of the normal MC analysis TDirectory
    # \param datasetsEmb    tauEmbedding.DatasetsMany object for embedded datasets
    # \param datasetsSig    dataset.DatasetManager object for normal MC datasets
    # \param datasetName    Name of the dataset
    # \param styles         List of plot styles
    # \param addData        Add embedded data?
    # \param addVariation   Add min/max values from embedding trials?
    def __init__(self, analysisEmb, analysisSig, datasetsEmb, datasetsSig, datasetName, styles, addData=False, addVariation=False):
        self.analysisEmb = analysisEmb
        self.analysisSig = analysisSig
        self.datasetsEmb = datasetsEmb # DatasetsMany
        self.datasetsSig = datasetsSig # DatasetManager
        self.datasetName = datasetName
        self.styles = styles # list of styles
        self.addData = addData
        self.addVariation = addVariation
        try:
            self.isResidual = self.datasetsEmb.isResidualAdded(datasetName)
        except:
            self.isResidual = False

    ## Function call syntax for creating the plot
    #
    # \param name   Name of the histogram (with embedding analysis path)
    # \param rebin  Rebin
    #
    # \return plots.PlotBase derived object
    def __call__(self, name, rebin=1):
        lumi = self.datasetsEmb.getLuminosity()

        name2Emb = name
        name2Sig = name
        if isinstance(name, basestring):
            name2Emb = self.analysisEmb+"/"+name
            name2Sig = self.analysisSig+"/"+name
        else: # assume TreeDraw
            name2Emb = name.clone(tree=self.analysisEmb+"/tree")
            name2Sig = name.clone(tree=self.analysisSig+"/tree")
        
        (emb, embVar) = self.datasetsEmb.getHistogram(self.datasetName, name2Emb, rebin)
        sig = self.datasetsSig.getDataset(self.datasetName).getDatasetRootHisto(name2Sig)
        sig.normalizeToLuminosity(lumi)
        sig = sig.getHistogram()
        if rebin > 1:
            sig.Rebin(rebin)

        emb.SetName("Embedded")
        sig.SetName("Normal")
        p = None
        sty = self.styles[:]
        if self.addData:
            (embData, embDataVar) = self.datasetsEmb.getHistogram("Data", name2Emb, rebin=rebin)
            embData.SetName("EmbeddedData")
            p = plots.ComparisonManyPlot(sig, [embData, emb])
            p.histoMgr.reorderDraw(["EmbeddedData", "Embedded", "Normal"])
            p.histoMgr.reorderLegend(["EmbeddedData", "Embedded", "Normal"])
            p.histoMgr.setHistoDrawStyle("EmbeddedData", "EP")
            p.histoMgr.setHistoLegendStyle("EmbeddedData", "P")
            p.histoMgr.setHistoLegendStyle("Embedded", "PL")
            p.setLuminosity(lumi)
            sty = [styles.dataStyle]+sty
        else:
            p = plots.ComparisonPlot(emb, sig)

        embedded = "Embedded "
        legLabel = plots._legendLabels.get(self.datasetName, self.datasetName)
        legLabelEmb = legLabel
        if legLabel != "Data":
            legLabel += " MC"
        residual = ""
        if self.isResidual:
            embedded = "Emb. "
            residual = " + res. MC"
        legLabelEmb += " MC"

        p.histoMgr.setHistoLegendLabelMany({
                "Embedded":     embedded + legLabelEmb + residual,
                "Normal":       "Normal " + legLabel,
                "EmbeddedData": embedded+"data"+residual,
                })
        p.histoMgr.forEachHisto(styles.Generator(sty))
        if self.addVariation:
            if self.addData:
                if embDataVar != None:
                    plots.copyStyle(p.histoMgr.getHisto("EmbeddedData").getRootHisto(), embDataVar)
                    embDataVar.SetMarkerStyle(2)
                    p.embeddingDataVariation = embDataVar
            if embVar != None:
                plots.copyStyle(p.histoMgr.getHisto("Embedded").getRootHisto(), embVar)
                embVar.SetMarkerStyle(2)
                p.embeddingVariation = embVar
    
        return p
