# tau embedding related plotting stuff

import plots
import counter

normalize = True
era = "Run2011A"

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
