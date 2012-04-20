DataCardName    = 'myDymmyTestName'
#Path            = '/mnt/flustre/slehti/HplusDataForLands'
Path            = '/home/wendland/data/lands/lands_HIG-11-019'
MassPoints      = [80,100,120,140,150,155,160]

# Specify name of EDFilter or EDAnalyser process that produced the root files
SignalAnalysis  = "signalAnalysis"
QCDFactorisedAnalysis = "QCDMeasurement"
QCDInvertedAnalysis = "" # FIXME

# Choose QCD measurement method (can be overridden from command line)
# options: 'QCD factorised' or 'QCD inverted'
QCDMeasurementMethod = "QCD factorised"
#QCDMeasurementMethod = "QCD inverted"

RootFileName    = "histograms.root" #FIXME

# Rate counter definitions
SignalRateCounter = "deltaPhiTauMET<160"
FakeRateCounter = "nonQCDType2:deltaphi160"

# Shape histogram definitions
SignalShapeHisto = "transverseMassAfterDeltaPhi160"
FakeShapeHisto = "NonQCDTypeIITransverseMassAfterDeltaPhi160"
ShapeHistogramsDimensions = [20, 0.0, 400.0]  # bins, min, max


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
    hhx.setLabel("HH"+str(mass))
    hhx.setLandSProcess(-1)
    hhx.setValidMassPoints(myMassList)
    hhx.setNuisances(["1","3","7","9","10","17","28","33","34"])
    hhx.setDatasetDefinitions(["TTToHplusBHminusB_M"+str(mass)]),
#   hhx.setSubPaths(multicrabPaths.getSubPaths(signalPath,"^TTToHplusBHminusB_M"+str(mass)))
    DataGroups.append(hhx)

    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass))
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(["1","3","7","9","10","18","28","33","34"])
    hwx.setDatasetDefinitions(["TTToHplusBWB_M"+str(mass)]),
#    hwx.setSubPaths(multicrabPaths.getSubPaths(signalPath,"^TTToHplusBWB_M"+str(mass)))
    DataGroups.append(hwx)

DataGroups.append(DataGroup(
    label        = "QCDfact",
    landsProcess = 3,
    validMassPoints = MassPoints,
    dirPrefix   = QCDFactorisedAnalysis,
    datasetType  = "QCD factorised",
    datasetDefinitions = ["Tau_"],
    MCEWKDatasetDefinitions = ["TTJets","WJets","DY","WW","WZ","ZZ","T_","Tbar_"],
    #mcEWKDatasetsForQCD = multicrabPaths.getSubPaths(multicrabPaths.getQCDfacPath(),"^Tau_\S+|Hplus",exclude=True),
    nuisances    = ["12","13"]
))

if 0 == 1:
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
        #path         = multicrabPaths.getQCDinvPath(),
        #subpath      = multicrabPaths.getSubPaths(multicrabPaths.getQCDinvPath(),"^Tau_\S+"),
        nuisances    = ["40","41","42","43"]
    ))

DataGroups.append(DataGroup(
    label        = "EWK_Tau",
    landsProcess = 4,
    shapeHisto   = SignalShapeHisto,
    datasetType  = "Embedding",
    datasetDefinitions   = ["Data"],
    dirPrefix   = SignalAnalysis,
    rateCounter  = SignalRateCounter,
    validMassPoints = MassPoints,
    #path         = multicrabPaths.getEWKPath(),
    #subpath      = multicrabPaths.getSubPaths(multicrabPaths.getEWKPath(),"^Data"),
    nuisances    = ["1b","3","7c","14","15","16","19"]
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
    #path         = multicrabPaths.getEWKPath(),
    #subpath      = multicrabPaths.getSubPaths(multicrabPaths.getEWKPath(),"^DYJetsToLL"),
    nuisances    = ["1c","3","7","9","11b","15b","16b","31","33","34","24"]
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
    #path         = multicrabPaths.getEWKPath(),
    #subpath      = multicrabPaths.getSubPaths(multicrabPaths.getEWKPath(),"^WW"),
    nuisances    = ["1c","3","7","9","11b","15b","16b","32","33","34","27"]
))

DataGroups.append(DataGroup(
    label        = "EWK_tt_faketau",
    landsProcess = 1,
    shapeHisto   = FakeShapeHisto,
    datasetType  = "Signal",
    datasetDefinitions   = ["TTJets_"],
    dirPrefix   = SignalAnalysis,
    rateCounter  = FakeRateCounter,
    validMassPoints = MassPoints,
    #subpath      = multicrabPaths.getSubPaths(signalPath,"^TTJets_"),
    nuisances    = ["1","4","7b","9","10","28","33","34b","35"]
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
    #subpath      = multicrabPaths.getSubPaths(signalPath,"^WJets_"),
    nuisances    = ["1","4","7b","9","11","29","33","34b","37"]
))

DataGroups.append(DataGroup(
    label        = "EWK_t_faketau",
    landsProcess = 8,
    shapeHisto   = FakeShapeHisto,
    datasetType  = "Signal",
    datasetDefinitions   = ["T_", "Tbar_"], #FIXME and s and t channels
    dirPrefix   = SignalAnalysis,
    rateCounter  = FakeRateCounter,
    validMassPoints = MassPoints,
    #subpath      = multicrabPaths.getSubPaths(signalPath,"^T_tW"),
    nuisances    = ["1","4","7b","9","10","30","33","34b","38"]
))

##############################################################################
# Definition of nuisance parameters
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import Nuisance
Nuisances = []
ReservedNuisances = []
ReservedNuisances.append([["2","5","6","8","20","21","23"],"reserved for leptonic"])

Nuisances.append(Nuisance(
    id            = "1",
    label         = "tau+MET trg scale factor",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["/ScaleFactorUncertainties/"],
    histograms    = ["TriggerScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.append(Nuisance(  
    id            = "1b", 
    label         = "tau+MET trg efficiency",
    distr         = "lnN", 
    function      = "Constant",
    value         = 0.113
))

Nuisances.append(Nuisance(
    id            = "1c",
    label         = "tau+MET trg scale factor",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["signalAnalysisNormal/ScaleFactorUncertainties/",
                     "signalAnalysisEmbedded/ScaleFactorUncertainties/"],
    histograms    = ["TriggerScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["signalAnalysisNormal/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160",
                     "signalAnalysisEmbedded/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.append(Nuisance(
    id            = "3",
    label         = "tau-jet ID (no Rtau)",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.06
))

Nuisances.append(Nuisance(
    id            = "4", 
    label         = "tau-jet mis ID (no Rtau)",  
    distr         = "lnN",
    function      = "Constant",
    value         = 0.15
))

Nuisances.append(Nuisance(
    id            = "7",
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    histoDir      = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus10",
                     "signalAnalysisJESMinus03eta02METPlus10"],
    histograms    = [SignalShapeHisto]
))

Nuisances.append(Nuisance(
    id            = "7b",  
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    histoDir      = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus10",
                     "signalAnalysisJESMinus03eta02METPlus10"],
    histograms    = [FakeShapeHisto]
))

Nuisances.append(Nuisance(
    id            = "7c",  
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    histoDir      = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus00",
                     "signalAnalysisJESMinus03eta02METPlus00"],
    histograms    = [SignalShapeHisto]
))

Nuisances.append(Nuisance(
    id            = "9",  
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
    counter       = FakeRateCounter,
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
    counter       = FakeRateCounter,
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
    function      = "maxCounter",
    histoDir      = ["signalAnalysis/weighted/",
                     "signalAnalysisPUWeightMinusCounters/weighted/",
                     "signalAnalysisPUWeightPlusCounters/weighted/"],
    counter       = SignalRateCounter
))

Nuisances.append(Nuisance(
    id            = "34b",
    label         = "pileup",
    distr         = "lnN",
    function      = "maxCounter",
    histoDir      = ["signalAnalysis/weighted/",
                     "signalAnalysisPUWeightMinusCounters/weighted/",       
                     "signalAnalysisPUWeightPlusCounters/weighted/"],
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
    label         = "QCDInv: stat.",
    distr         = "lnN",
    function      = "QCDInverted",
    counter       = "deltaPhiTauMET160 limit"
))

Nuisances.append(Nuisance(
    id            = "41",
    label         = "QCDInv: JES/JER/MET/Rtau effect on normalisation",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.057
))

Nuisances.append(Nuisance(
    id            = "42",
    label         = "QCDInv: MET shape", 
    distr         = "lnN",
    function      = "Constant",
    value         = 0.055
))

Nuisances.append(Nuisance(
    id            = "43",
    label         = "QCDInv: fit", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.0043
))

MergeNuisances = []
MergeNuisances.append(["1","1b","1c"])
MergeNuisances.append(["7","7b","7c"])
MergeNuisances.append(["11","11b"])
MergeNuisances.append(["15","15b"])
MergeNuisances.append(["16","16b"])
MergeNuisances.append(["34","34b"])
