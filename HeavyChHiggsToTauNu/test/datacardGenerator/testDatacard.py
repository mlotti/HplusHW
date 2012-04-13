DataCardName    = 'myDymmyTestName'
Path            = '/mnt/flustre/slehti/HplusDataForLands'
MassPoints      = [80,100,120,140,150,155,160]

Analysis        = "signalAnalysis"
RootFileName    = "histograms.root"
ShapeHisto      = "transverseMassAfterDeltaPhi160"
CounterDir      = Analysis+"Counters/weighted"
Counter         = "deltaPhiTauMET<160"
ConfigInfoHisto = "configInfo/configinfo"

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder
multicrabPaths = PathFinder.MulticrabPathFinder(Path)
signalPath = multicrabPaths.getSignalPath()
signalDataPaths = multicrabPaths.getSubPaths(signalPath,"^Tau_\S+")

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import ObservationInput
Observation     = ObservationInput(counterDir=CounterDir,counter=Counter,shapeHisto=ShapeHisto)
Observation.setPaths(signalPath,signalDataPaths)

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import DataGroupInput,DataGroup
DataGroups = DataGroupInput()

template = DataGroup(name="signal",shapeHisto=ShapeHisto,rootpath=Analysis)
template.setPath(signalPath)

for mass in MassPoints:
    hhx = template.clone()
    hhx.setLabel("HH"+str(mass))
    hhx.setLandSProcess(-1)
    hhx.setFunction("Counter")
    hhx.setCounter(Counter)
    hhx.setMass(mass)
    hhx.setNuisances(["1","3","7","9","10","17","28","33","34"])
    hhx.setSubPaths(multicrabPaths.getSubPaths(signalPath,"^TTToHplusBHminusB_M"+str(mass)))
    DataGroups.add(hhx)

    hwx = template.clone()
    hwx.setLabel("HW"+str(mass))
    hwx.setLandSProcess(0)
    hwx.setFunction("Counter")
    hwx.setCounter(Counter)
    hwx.setMass(mass)
    hwx.setNuisances(["1","3","7","9","10","18","28","33","34"])
    hwx.setSubPaths(multicrabPaths.getSubPaths(signalPath,"^TTToHplusBWB_M"+str(mass)))
    DataGroups.add(hwx)

DataGroups.add(DataGroup(
    name         = "QCD",
    label        = "QCDfact",
    rootpath     = "QCDMeasurementCounters",
    landsProcess = 3,
    function     = "QCDMeasurement",
    path         = multicrabPaths.getQCDfacPath(),
    subpath      = multicrabPaths.getSubPaths(multicrabPaths.getQCDfacPath(),"^Tau_\S+"),
    ewkmcpaths   = multicrabPaths.getSubPaths(multicrabPaths.getQCDfacPath(),"^Tau_\S+|Hplus",exclude=True),
    nuisances    = ["12","13"]
))

DataGroups.add(DataGroup(
    name         = "QCD",
    label        = "QCDinv",
    rootpath     = Analysis,
    landsProcess = 3,
    function     = "QCDInverted",
    shapeHisto   = "mtSum",
    counter      = "deltaPhiTauMET160 limit",
    normalization= 0.0066,
    path         = multicrabPaths.getQCDinvPath(),
    subpath      = multicrabPaths.getSubPaths(multicrabPaths.getQCDinvPath(),"^Tau_\S+"),
    nuisances    = ["40","41","42","43"]
))

DataGroups.add(DataGroup(
    name         = "EWK",
    label        = "EWK_Tau",
    rootpath     = Analysis,
    landsProcess = 4,
    function     = "Counter",
    shapeHisto   = ShapeHisto,
    counter      = "nonQCDType2:deltaphi160",
    path         = multicrabPaths.getEWKPath(),
    subpath      = multicrabPaths.getSubPaths(multicrabPaths.getEWKPath(),"^Data"),
    nuisances    = ["1b","3","7c","14","15","16","19"]
))

DataGroups.add(DataGroup(
    name         = "EWK",
    label        = "EWK_DY",
    rootpath     = Analysis,
    landsProcess = 5,
    function     = "Counter", 
    shapeHisto   = ShapeHisto,
    counter      = Counter,
    path         = multicrabPaths.getEWKPath(),
    subpath      = multicrabPaths.getSubPaths(multicrabPaths.getEWKPath(),"^DYJetsToLL"),
    nuisances    = ["1c","3","7","9","11b","15b","16b","31","33","34","24"]
))

DataGroups.add(DataGroup(
    name         = "EWK",
    label        = "EWK_VV",
    rootpath     = Analysis,
    landsProcess = 6,
    function     = "Counter",
    shapeHisto   = ShapeHisto,
    counter      = Counter,
    path         = multicrabPaths.getEWKPath(),
    subpath      = multicrabPaths.getSubPaths(multicrabPaths.getEWKPath(),"^WW"),
    nuisances    = ["1c","3","7","9","11b","15b","16b","32","33","34","27"]
))

DataGroups.add(DataGroup(
    name         = "EWK",
    label        = "EWK_tt_faketau",
    rootpath     = Analysis,
    landsProcess = 1,
    function     = "Counter",
    shapeHisto   = "NonQCDTypeIITransverseMassAfterDeltaPhi160",
    counter      = "nonQCDType2:deltaphi160",
    path         = signalPath,
    subpath      = multicrabPaths.getSubPaths(signalPath,"^TTJets_"),
    nuisances    = ["1","4","7b","9","10","28","33","34b","35"]
))

DataGroups.add(DataGroup(
    name         = "EWK",
    label        = "EWK_W_faketau",
    rootpath     = Analysis,
    landsProcess = 7,
    function     = "Counter",
    shapeHisto   = "NonQCDTypeIITransverseMassAfterDeltaPhi160",
    counter      = "nonQCDType2:deltaphi160",
    path         = signalPath,
    subpath      = multicrabPaths.getSubPaths(signalPath,"^WJets_"),
    nuisances    = ["1","4","7b","9","11","29","33","34b","37"]
))

DataGroups.add(DataGroup(
    name         = "EWK",
    label        = "EWK_t_faketau",
    rootpath     = Analysis,
    landsProcess = 8,
    function     = "Counter",
    shapeHisto   = "NonQCDTypeIITransverseMassAfterDeltaPhi160",
    counter      = "nonQCDType2:deltaphi160",
    path         = signalPath,
    subpath      = multicrabPaths.getSubPaths(signalPath,"^T_tW"),
    nuisances    = ["1","4","7b","9","10","30","33","34b","38"]
))


from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import NuisanceTable,Nuisance
Nuisances = NuisanceTable()
Nuisances.reserve(["2","5","6","8","20","21","23"],comment="reserved for leptonic")
Nuisances.add(Nuisance(
    id            = "1",
    label         = "tau+MET trg scale factor",
    distr         = "lnN",
    function      = "ScaleFactor",
    paths         = [Analysis+"/ScaleFactorUncertainties/"],
    histograms    = ["TriggerScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalization = [Analysis+"/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.add(Nuisance(  
    id            = "1b", 
    label         = "tau+MET trg efficiency",
    distr         = "lnN", 
    function      = "Constant",
    value         = 0.113
))

Nuisances.add(Nuisance(
    id            = "1c",
    label         = "tau+MET trg scale factor",
    distr         = "lnN",
    function      = "ScaleFactor",
    paths         = ["signalAnalysisNormal/ScaleFactorUncertainties/",
                     "signalAnalysisEmbedded/ScaleFactorUncertainties/"],
    histograms    = ["TriggerScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalization = ["signalAnalysisNormal/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160",
                     "signalAnalysisEmbedded/ScaleFactorUncertainties/TriggerScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.add(Nuisance(
    id            = "3",
    label         = "tau-jet ID (no Rtau)",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.06
))

Nuisances.add(Nuisance(
    id            = "4", 
    label         = "tau-jet mis ID (no Rtau)",  
    distr         = "lnN",
    function      = "Constant",
    value         = 0.15
))

Nuisances.add(Nuisance(
    id            = "7",
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    paths         = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus10",
                     "signalAnalysisJESMinus03eta02METPlus10"],
    histograms    = [ShapeHisto]
))

Nuisances.add(Nuisance(
    id            = "7b",  
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    paths         = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus10",
                     "signalAnalysisJESMinus03eta02METPlus10"],
    histograms    = ["NonQCDTypeIITransverseMassAfterDeltaPhi160"]
))

Nuisances.add(Nuisance(
    id            = "7c",  
    label         = "JES/JER/MET/Rtau effect on mT shape",
    distr         = "shapeQ",
    function      = "Shape",
    paths         = ["signalAnalysis",
                     "signalAnalysisJESPlus03eta02METMinus00",
                     "signalAnalysisJESMinus03eta02METPlus00"],
    histograms    = [ShapeHisto]
))

Nuisances.add(Nuisance(
    id            = "9",  
    label         = "lepton veto",
    distr         = "lnN",
    function      = "Ratio",
    counterHisto  = CounterDir+"/counter",
    numerator     = "muon veto",
    denominator   = "trigger scale factor",
    extranorm     = 0.02
))

Nuisances.add(Nuisance(
    id            = "10",   
    label         = "btagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    paths         = ["signalAnalysis/ScaleFactorUncertainties/"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalization = ["signalAnalysis/ScaleFactorUncertainties/BtagScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.add(Nuisance(
    id            = "11",
    label         = "mistagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    paths         = ["signalAnalysis/ScaleFactorUncertainties/"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalization = ["signalAnalysis/ScaleFactorUncertainties/BtagScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.add(Nuisance(
    id            = "11b",
    label         = "mistagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    paths         = ["signalAnalysisNormal/ScaleFactorUncertainties/"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalization = ["signalAnalysisNormal/ScaleFactorUncertainties/BtagScaleFactorAbsUncertCounts_AfterDeltaPhi160"]
))

Nuisances.add(Nuisance(
    id            = "12",
    label         = "QCD stat.",
    distr         = "lnN",
    function      = "QCDMeasurement",
#    QCDMode       = "statistics",
    counterHisto  = "QCDMeasurementCounters/weighted/counter",
    paths         = ["QCDMeasurement/"],
    histograms    = ["KESKEN"]
))

Nuisances.add(Nuisance(   
    id            = "13",
    label         = "QCD syst.",
    distr         = "lnN",
    function      = "QCDMeasurement",
#    QCDMode       = "systematics",
    counterHisto  = "QCDMeasurementCounters/weighted/counter",
    paths         = ["QCDMeasurement/"],
    histograms    = ["KESKEN"]                                                                       
))

Nuisances.add(Nuisance(
    id            = "14", 
    label         = "EWK with taus QCD contamination",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.012
))

Nuisances.add(Nuisance(
    id            = "15",
    label         = "EWK with taus W->tau->mu",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.007
))

Nuisances.add(Nuisance(
    id            = "15b", 
    label         = "EWK with taus W->tau->mu",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.001
))

Nuisances.add(Nuisance(
    id            = "16",
    label         = "EWK with taus muon selection",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.005  
))

Nuisances.add(Nuisance(
    id            = "16b",
    label         = "EWK with taus muon selection",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.001
))

Nuisances.add(Nuisance(
    id            = "17",
    label         = "MC signal statistics, HH",
    distr         = "lnN",
    function      = "Counter",
    counterHisto  = CounterDir+"/counter",
    counter       = Counter
))

Nuisances.add(Nuisance(
    id            = "18",
    label         = "MC signal statistics, HW",
    distr         = "lnN",
    function      = "Counter",
    counterHisto  = CounterDir+"/counter",
    counter       = Counter
))

Nuisances.add(Nuisance(  
    id            = "19", 
    label         = "EWK with taus stat.",
    distr         = "lnN",
    function      = "Counter",
    counterHisto  = CounterDir+"/counter",
    counter       = Counter
))

Nuisances.add(Nuisance(  
    id            = "22",
    label         = "tt->jjtau MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0
))

Nuisances.add(Nuisance(   
    id            = "24",
    label         = "Z->tautau MC stat",
    distr         = "lnN",
    function      = "Counter",
    counterHisto  = CounterDir+"/counter",
    counter       = Counter
))

Nuisances.add(Nuisance(
    id            = "25",
    label         = "W+jets MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0
))

Nuisances.add(Nuisance(
    id            = "26",
    label         = "Single top MC stat.",   
    distr         = "lnN",
    function      = "Constant",
    value         = 0
))

Nuisances.add(Nuisance(                                                                                                  
    id            = "27",                                                                                                
    label         = "diboson MC stat",
    distr         = "lnN",                                                                                               
    function      = "Counter",                                                                                           
    counterHisto  = CounterDir+"/counter",                                                                               
    counter       = Counter                                                                                              
))

Nuisances.add(Nuisance(                                                                                                  
    id            = "28",
    label         = "ttbar cross section",
    distr         = "lnN",                                                                                               
    function      = "Constant",
#    range         = [0.096,0.070] #??FIXME
))

Nuisances.add(Nuisance(                                                                                                  
    id            = "29",
    label         = "W+jets cross section",
    distr         = "lnN",                 
    function      = "Constant",                                                                                          
    value         = 0.05
))

Nuisances.add(Nuisance(                                                                                                  
    id            = "30",                                                                                                
    label         = "single top cross section",
    distr         = "lnN",                     
    function      = "Constant",                
    value         = 0.08
))

Nuisances.add(Nuisance(                                                                                                  
    id            = "31",
    label         = "Z->ll cross section",
    distr         = "lnN",                
    function      = "Constant",           
    value         = 0.04
))

Nuisances.add(Nuisance(                                                                                                  
    id            = "32",
    label         = "diboson cross section",
    distr         = "lnN",                                                                                               
    function      = "Constant",                                                                                          
    value         = 0.04                                                                                                 
))

Nuisances.add(Nuisance(
    id            = "33",
    label         = "luminosity",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.22
))

Nuisances.add(Nuisance(
    id            = "34",
    label         = "pileup",
    distr         = "lnN",
    function      = "maxCounter",
    paths         = ["signalAnalysis/weighted/",
                     "signalAnalysisPUWeightMinusCounters/weighted/",
                     "signalAnalysisPUWeightPlusCounters/weighted/"],
    counterHisto  = "counter",
    counter       = Counter
))

Nuisances.add(Nuisance(
    id            = "34b",
    label         = "pileup",
    distr         = "lnN",
    function      = "maxCounter",
    paths         = ["signalAnalysis/weighted/",
                     "signalAnalysisPUWeightMinusCounters/weighted/",       
                     "signalAnalysisPUWeightPlusCounters/weighted/"],
    counterHisto  = "counter",           
    counter       = "nonQCDType2:deltaphi160"
))

Nuisances.add(Nuisance(  
    id            = "35",
    label         = "ttbar fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counterHisto  = Analysis+"/counter",
    counter       = "nonQCDType2:deltaphi160"
))

Nuisances.add(Nuisance(
    id            = "36", 
    label         = "Z->tautau fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",   
    counterHisto  = Analysis+"/counter",
    counter       = "nonQCDType2:deltaphi160"
))

Nuisances.add(Nuisance(
    id            = "37",  
    label         = "W+jets fake tau MC stat.",
    function      = "Counter",
    counterHisto  = Analysis+"/counter",
    counter       = "nonQCDType2:deltaphi160"
))

Nuisances.add(Nuisance(
    id            = "38",
    label         = "single top fake tau MC stat.",
    distr         = "lnN",   
    function      = "Counter",
    counterHisto  = Analysis+"/counter",
    counter       = "nonQCDType2:deltaphi160"
))

Nuisances.add(Nuisance(
    id            = "39", 
    label         = "diboson fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counterHisto  = Analysis+"/counter",
    counter       = "nonQCDType2:deltaphi160"
))

Nuisances.add(Nuisance(
    id            = "40",
    label         = "QCDInv: stat.",
    distr         = "lnN",
    function      = "QCDInverted",
    counterHisto  = Analysis+"/counter",
    counter       = "deltaPhiTauMET160 limit"
))

Nuisances.add(Nuisance(
    id            = "41",
    label         = "QCDInv: JES/JER/MET/Rtau effect on normalization",
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.057
))

Nuisances.add(Nuisance(
    id            = "42",
    label         = "QCDInv: MET shape", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.055
))

Nuisances.add(Nuisance(
    id            = "43",
    label         = "QCDInv: fit", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.0043
))

Nuisances.merge("1","1b")
Nuisances.merge("1","1c")
Nuisances.merge("7","7b")
Nuisances.merge("7","7c")   
Nuisances.merge("11","11b")   
Nuisances.merge("15","15b")   
Nuisances.merge("16","16b")   
Nuisances.merge("34","34b")   