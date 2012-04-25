DataCardName    = 'myDummyTestName'
#Path            = '/mnt/flustre/slehti/HplusDataForLands'
Path            = '/home/wendland/data/lands/lands_HIG-11-019'
MassPoints      = [80,90,100,120,140,150,155,160]
#MassPoints      = [160]

# Specify name of EDFilter or EDAnalyser process that produced the root files
SignalAnalysis  = "signalAnalysis"
QCDFactorisedAnalysis = "QCDMeasurement"
QCDInvertedAnalysis = "" # FIXME

RootFileName    = "histograms.root" #FIXME

# Rate counter definitions
SignalRateCounter = "deltaPhiTauMET<160"
FakeRateCounter = "nonQCDType2:deltaphi160"

# Shape histogram definitions
SignalShapeHisto = "transverseMassAfterDeltaPhi160"
FakeShapeHisto = "NonQCDTypeIITransverseMassAfterDeltaPhi160"
ShapeHistogramsDimensions = [20, 0.0, 400.0]  # bins, min, max

# Options
OptionReplaceEmbeddingByMC = False


#FIXME move
#import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder
#multicrabPaths = PathFinder.MulticrabPathFinder(Path)
#signalPath = multicrabPaths.getSignalPath()
#signalDataPaths = multicrabPaths.getSubPaths(signalPath,"^Tau_\S+")

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import ObservationInput
Observation = ObservationInput(dirPrefix=SignalAnalysis,
                               rateCounter=SignalRateCounter,
                               datasetDefinitions=["Tau_"],
                               shapeHisto=SignalShapeHisto)
#Observation.setPaths(signalPath,signalDataPaths)

##############################################################################
# DataGroup (i.e. columns in datacard) definitions
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import DataGroup
DataGroups = []

signalTemplate = DataGroup(datasetType="Signal",
                           shapeHisto=SignalShapeHisto,
                           dirPrefix=SignalAnalysis,
                           rateCounter=SignalRateCounter)

for mass in MassPoints:
    myMassList = [mass]
    hhx = signalTemplate.clone()
    hhx.setLabel("HH"+str(mass)+"_a")
    hhx.setLandSProcess(-1)
    hhx.setValidMassPoints(myMassList)
    hhx.setNuisances(["01","03","07","09","10","17","28","33","34"])
    hhx.setDatasetDefinitions(["TTToHplusBHminusB_M"+str(mass)]),
    DataGroups.append(hhx)

    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(["01","03","07","09","10","18","28","33","34"])
    hwx.setDatasetDefinitions(["TTToHplusBWB_M"+str(mass)]),
    DataGroups.append(hwx)

DataGroups.append(DataGroup(
    label        = "QCDfact",
    landsProcess = 3,
    validMassPoints = MassPoints,
    dirPrefix   = QCDFactorisedAnalysis,
    datasetType  = "QCD factorised",
    datasetDefinitions = ["Tau_"],
    MCEWKDatasetDefinitions = ["TTJets","WJets","DY","WW","WZ","ZZ","T_","Tbar_"],
    nuisances    = ["12","13","40b"]
))

DataGroups.append(DataGroup(
    label        = "QCDinv",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD inverted",
    datasetDefinitions   = "^Tau\S+",
    shapeHisto   = "mtSum",
    dirPrefix   = QCDInvertedAnalysis,
    rateCounter  = "deltaPhiTauMET160 limit",
    additionalNormalisation= 0.0066,
    nuisances    = ["41","42","43","44"] # FIXME: add shape stat, i.e. 40x
))

if not OptionReplaceEmbeddingByMC:
     # EWK + ttbar with genuine taus
    DataGroups.append(DataGroup(
        label        = "EWK_Tau",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinitions   = ["Data"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01b","03","07c","14","15","16","19","40"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_DY",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinitions   = ["DYJetsToLL"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01c","03","07","09","11b","15b","16b","31","33","34","24"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_VV",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinitions   = ["WW"], #,"WZ","ZZ"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01c","03","07","09","11b","15b","16b","32","33","34","27"]
    ))

    # EWK + ttbar with fake taus
    DataGroups.append(DataGroup(
        label        = "EWK_tt_faketau",
        landsProcess = 1,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["TTJets_"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01","04","07b","09","10","28","33","34b","35"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_W_faketau",
        landsProcess = 7,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["WJets"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01","04","07b","09","11","29","33","34b","37"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_t_faketau",
        landsProcess = 8,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["T_", "Tbar_"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01","04","07b","09","10","30","33","34b","38"]
    ))
else:
    # Mimic embedding with MC analysis (introduces double counting of EWK fakes, but that should be small effect)
    DataGroups.append(DataGroup(
        label        = "MC_EWK_Tau",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["TTJets", "WJets_", "Tbar_", "T_"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01b","03","07","14","15","16","19","40"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_EWK_DY",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinitions   = ["DYJetsToLL"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01","03","07","09","11","15b","16b","31","33","34","24"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_EWK_VV",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinitions   = ["WW","WZ","ZZ"],
        dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01","03","07","09","11","15b","16b","32","33","34","27"]
    ))
    DataGroups.append(DataGroup(
        label        = "empty",
        landsProcess = 1,
        datasetType  = "None",
        validMassPoints = MassPoints,
    ))


# Reserve column 2
DataGroups.append(DataGroup(
    label        = "res.",
    landsProcess = 2,
    datasetType  = "None",
    validMassPoints = MassPoints,
))


##############################################################################
# Definition of nuisance parameters
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import Nuisance
ReservedNuisances = []
ReservedNuisances.append(["02", "reserved for leptonic"])
ReservedNuisances.append(["05", "reserved for leptonic"])
ReservedNuisances.append(["06", "reserved for leptonic"])
ReservedNuisances.append(["08", "reserved for leptonic"])
ReservedNuisances.append(["20", "reserved for leptonic"])
ReservedNuisances.append(["21", "reserved for leptonic"])
ReservedNuisances.append(["23", "reserved for leptonic"])

Nuisances = []

Nuisances.append(Nuisance(
    id            = "01",
    label         = "tau+MET trg scale factor",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["signalAnalysis/ScaleFactorUncertainties/"],
    histograms    = ["TriggerScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["signalAnalysis/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160"],
    addUncertaintyInQuadrature = 0.10 # MET leg uncertainty
))

Nuisances.append(Nuisance(
    id            = "01b", 
    label         = "tau+MET trg efficiency",
    distr         = "lnN", 
    function      = "Constant",
    value         = 0.113
))

Nuisances.append(Nuisance(
    id            = "01c",
    label         = "tau+MET trg scale factor",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["signalAnalysisNormal/ScaleFactorUncertainties/",
                     "signalAnalysisEmbedded/ScaleFactorUncertainties/"],
    histograms    = ["TriggerScaleFactorAbsUncert_AfterDeltaPhi160",
                     "TriggerScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["signalAnalysisNormal/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160",
                     "signalAnalysisEmbedded/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160"],
    addUncertaintyInQuadrature = 0.10 # MET leg uncertainty
))

Nuisances.append(Nuisance(
    id            = "03",
    label         = "tau-jet ID (no Rtau)",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.06
))

Nuisances.append(Nuisance(
    id            = "04", 
    label         = "tau-jet mis ID (no Rtau)",  
    distr         = "lnN",
    function      = "Constant",
    value         = 0.15
))

Nuisances.append(Nuisance(
    id            = "07",
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    histoDir      = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus10",
                     "signalAnalysisJESMinus03eta02METPlus10"],
    histograms    = [SignalShapeHisto]
))

Nuisances.append(Nuisance(
    id            = "07b",
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    histoDir      = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus10",
                     "signalAnalysisJESMinus03eta02METPlus10"],
    histograms    = [FakeShapeHisto]
))

Nuisances.append(Nuisance(
    id            = "07c",
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    histoDir      = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus00",
                     "signalAnalysisJESMinus03eta02METPlus00"],
    histograms    = [SignalShapeHisto]
))

Nuisances.append(Nuisance(
    id            = "09",
    label         = "lepton veto",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "muon veto",
    denominator   = "trigger scale factor",
    scaling       = 0.02
))

Nuisances.append(Nuisance(
    id            = "10",
    label         = "btagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["signalAnalysis/ScaleFactorUncertainties/"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["signalAnalysis/ScaleFactorUncertainties/BtagScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.append(Nuisance(
    id            = "11",
    label         = "mistagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["signalAnalysis/ScaleFactorUncertainties/"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["signalAnalysis/ScaleFactorUncertainties/BtagScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.append(Nuisance(
    id            = "11b",
    label         = "mistagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["signalAnalysisNormal/ScaleFactorUncertainties/"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["signalAnalysisNormal/ScaleFactorUncertainties/BtagScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.append(Nuisance(
    id            = "12",
    label         = "QCD stat.",
    distr         = "lnN",
    function      = "QCDFactorised",
    QCDmode       = "statistics",
    histoDir      = ["QCDMeasurement/"],
    histograms    = ["KESKEN"]
))

Nuisances.append(Nuisance(
    id            = "13",
    label         = "QCD syst.",
    distr         = "lnN",
    function      = "QCDFactorised",
    QCDmode       = "systematics",
))

Nuisances.append(Nuisance(
    id            = "14",
    label         = "EWK with taus QCD contamination",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.012
))

Nuisances.append(Nuisance(
    id            = "15",
    label         = "EWK with taus W->tau->mu",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.007
))

Nuisances.append(Nuisance(
    id            = "15b",
    label         = "EWK with taus W->tau->mu",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.001
))

Nuisances.append(Nuisance(
    id            = "16",
    label         = "EWK with taus muon selection",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.005
))

Nuisances.append(Nuisance(
    id            = "16b",
    label         = "EWK with taus muon selection",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.001
))

Nuisances.append(Nuisance(
    id            = "17",
    label         = "MC signal statistics, HH",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "18",
    label         = "MC signal statistics, HW",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "19",
    label         = "EWK with taus stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "22",
    label         = "tt->jjtau MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0
))

Nuisances.append(Nuisance(
    id            = "24",
    label         = "Z->tautau MC stat",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "25",
    label         = "W+jets MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0
))

Nuisances.append(Nuisance(
    id            = "26",
    label         = "Single top MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0
))

Nuisances.append(Nuisance(
    id            = "27",
    label         = "diboson MC stat",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "28",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.096,
    upperValue    = 0.070,
))

Nuisances.append(Nuisance(
    id            = "29",
    label         = "W+jets cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.05
))

Nuisances.append(Nuisance(
    id            = "30",
    label         = "single top cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.08
))

Nuisances.append(Nuisance(
    id            = "31",
    label         = "Z->ll cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04
))

Nuisances.append(Nuisance(
    id            = "32",
    label         = "diboson cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04
))

Nuisances.append(Nuisance(
    id            = "33",
    label         = "luminosity",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.022
))

Nuisances.append(Nuisance(
    id            = "34",
    label         = "pileup",
    distr         = "lnN",
    function      = "pileupUncertainty",
    histoDir      = ["signalAnalysisCounters", # nominal
                     "signalAnalysisPUWeightMinusCounters", # minus
                     "signalAnalysisPUWeightPlusCounters"], # up
    counter       = SignalRateCounter
))

Nuisances.append(Nuisance(
    id            = "34b",
    label         = "pileup",
    distr         = "lnN",
    function      = "pileupUncertainty",
    histoDir      = ["signalAnalysisCounters", # nominal
                     "signalAnalysisPUWeightMinusCounters", # minus
                     "signalAnalysisPUWeightPlusCounters"], # up
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "35",
    label         = "ttbar fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "36", 
    label         = "Z->tautau fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "37",  
    label         = "W+jets fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "38",
    label         = "single top fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "39", 
    label         = "diboson fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "40",
    label         = "Stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "Shape",
    counter       = SignalRateCounter
))

Nuisances.append(Nuisance(
    id            = "40b",
    label         = "Stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "Shape",
    QCDmode       = "shapestat"
))

Nuisances.append(Nuisance(
    id            = "40c",
    label         = "Stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "Shape",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "41",
    label         = "QCDInv: stat.",
    distr         = "lnN",
    function      = "QCDInverted",
    counter       = "deltaPhiTauMET160 limit"
))

Nuisances.append(Nuisance(
    id            = "42",
    label         = "QCDInv: JES/JER/MET/Rtau effect on normalisation",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.057
))

Nuisances.append(Nuisance(
    id            = "43",
    label         = "QCDInv: MET shape", 
    distr         = "lnN",
    function      = "Constant",
    value         = 0.055
))

Nuisances.append(Nuisance(
    id            = "44",
    label         = "QCDInv: fit", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.0043
))

MergeNuisances = []
MergeNuisances.append(["01","01b","01c"])
MergeNuisances.append(["07","07b","07c"])
MergeNuisances.append(["11","11b"])
MergeNuisances.append(["15","15b"])
MergeNuisances.append(["16","16b"])
MergeNuisances.append(["34","34b"])
MergeNuisances.append(["40","40b","40c"])