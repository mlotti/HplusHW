DataCardName    = 'Default'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_metModeIsolationDependent'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_metModeNeverIsolated'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_vitalonly_correctCtrlPlots'
Path            = '/home/wendland/data/v445/met50_2013-05-13/testInverted'
#Path            = '/home/wendland/data/v445/met50rtaunprongs'
#Path            = '/mnt/flustre/slehti/hplusAnalysis/QCDInverted/CMSSW_4_4_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/datacardGenerator/TESTDATA/'
LightMassPoints      = [80,90,100,120,140,150,155,160]
HeavyMassPoints      = [180,190,200,220,250,300]
HeavyMassPoints      = []
#MassPoints      = [80,90,100,120,140,150,155,160]
#MassPoints      = [80,120,160]
MassPoints      = [120] # The mass points to run

BlindAnalysis   = True

# Rate counter definitions
SignalRateCounter = "Selected events"
FakeRateCounter = "EWKfaketaus:SelectedEvents"

# Options
OptionMassShape = "TransverseMass"
#OptionMassShape = "FullMass"
#OptionMassShape = "TransverseAndFullMass2D" #FIXME not yet supported!!!

OptionReplaceEmbeddingByMC = True
OptionIncludeSystematics = False # Set to true if the JES and PU uncertainties were produced
OptionPurgeReservedLines = True # Makes limit running faster, but cannot combine leptonic datacards
OptionDoControlPlots = True
OptionQCDfactorisedFactorisationSchema = "TauPt" # options: 'full', 'taupt' (recommended), 'taueta, 'nvtx'
OptionDoQCDClosureTests = False

# Options for reports and article
OptionBr = 0.01  # Br(t->bH+)

# Tolerance for throwing error on luminosity difference (0.01 = 1 percent agreement is required)
ToleranceForLuminosityDifference = 0.01

# Shape histogram definitions
SignalShapeHisto = None
FakeShapeHisto = None
ShapeHistogramsDimensions = None

if OptionMassShape == "TransverseMass":
    SignalShapeHisto = "transverseMass"
    FakeShapeHisto = "EWKFakeTausTransverseMass"
    ShapeHistogramsDimensions = { "bins": 10,
                                  "rangeMin": 0.0,
                                  "rangeMax": 400.0,
                                  #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                                  "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200], # if an empty list is given, then uniform bin width is used
                                  "xtitle": "Transverse mass / GeV",
                                  "ytitle": "Events" }
elif OptionMassShape == "FullMass":
    SignalShapeHisto = "fullMass"
    FakeShapeHisto = "EWKFakeTausFullMass"
    ShapeHistogramsDimensions = { "bins": 25,
                                  "rangeMin": 0.0,
                                  "rangeMax": 500.0,
                                  "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                                  #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200], # if an empty list is given, then uniform bin width is used
                                  "xtitle": "Full mass / GeV",
                                  "ytitle": "Events" }
elif OptionMassShape == "TransverseAndFullMass2D": # FIXME: preparing to add support, not yet working
    SignalShapeHisto = "transverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    FakeShapeHisto = "EWKFakeTausTransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    ShapeHistogramsDimensions = [{ "bins": 10,
                                  "rangeMin": 0.0,
                                  "rangeMax": 400.0,
                                  #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                                  "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200], # if an empty list is given, then uniform bin width is used
                                  "xtitle": "Transverse mass / GeV",
                                  "ytitle": "Events" },
                                 { "bins": 25,
                                   "rangeMin": 0.0,
                                   "rangeMax": 500.0,
                                   "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                                   #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200], # if an empty list is given, then uniform bin width is used
                                   "xtitle": "Full mass / GeV",
                                   "ytitle": "Events" }]

DataCardName += "_"+OptionMassShape

##############################################################################
# Specifications for QCD factorised

#QCDFactorisedStdSelVersion = "QCDfactorised_TradReference"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusMET30"
QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusCollinearTailKiller"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusMET30PlusCollinearTailKiller"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusTailKiller"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusMET30PlusTailKiller"

QCDFactorisedValidationMETShapeHistogramsDimensions = {  "bins": 9,
                                                         "rangeMin": 0.0,
                                                         "rangeMax": 500.0,
                                                         #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                                                         "variableBinSizeLowEdges": [0,20,40,60,80,100,150,200,300],
                                                         #"variableBinSizeLowEdges": [],
                                                         "xtitle": "E_{T}^{miss}, GeV/c^{2}",
                                                         "ytitle": "Events"}
QCDFactorisedValidationMtShapeHistogramsDimensions = { "bins": 10,
                                                        "rangeMin": 0.0,
                                                        "rangeMax": 400.0,
                                                        #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                                                        "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,200], # if an empty list is given, then uniform bin width is used
                                                        "xtitle": "Transverse mass / GeV",
                                                        "ytitle": "Events" }

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import ObservationInput
Observation = ObservationInput(#dirPrefix=SignalAnalysis,
                               rateCounter=SignalRateCounter,
                               datasetDefinitions=["Tau_"],
                               shapeHisto=SignalShapeHisto)
#Observation.setPaths(signalPath,signalDataPaths)

##############################################################################
# DataGroup (i.e. columns in datacard) definitions
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import DataGroup
DataGroups = []
EmbeddingIdList = []
EWKFakeIdList = []

signalTemplate = DataGroup(datasetType="Signal",
                           shapeHisto=SignalShapeHisto,
                           #dirPrefix=SignalAnalysis,
                           rateCounter=SignalRateCounter)

for mass in LightMassPoints:
    myMassList = [mass]
    hhx = signalTemplate.clone()
    hhx.setLabel("HH"+str(mass)+"_a")
    hhx.setLandSProcess(-1)
    hhx.setValidMassPoints(myMassList)
    hhx.setNuisances(["trg_tau","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_tag","stat_binByBin","xsect_tt_7TeV","lumi","pileup"])
    hhx.setDatasetDefinitions(["TTToHplusBHminusB_M"+str(mass)]),
    DataGroups.append(hhx)

    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(["trg_tau","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_tag","stat_binByBin","xsect_tt_7TeV","lumi","pileup"])
    hwx.setDatasetDefinitions(["TTToHplusBWB_M"+str(mass)]),
    DataGroups.append(hwx)

for mass in HeavyMassPoints:
    myMassList = [mass]
    hx = signalTemplate.clone()
    hx.setLabel("Hp"+str(mass)+"_a")
    hx.setLandSProcess(0)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(["trg_tau","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_tag","stat_binByBin","lumi","pileup"])
    hx.setDatasetDefinitions(["HplusTB_M"+str(mass)]),
    DataGroups.append(hx)

if OptionMassShape == "TransverseMass":
    DataGroups.append(DataGroup(
        label        = "QCDfact",
        landsProcess = 3,
        validMassPoints = MassPoints,
        #dirPrefix   = QCDFactorisedAnalysis,
        datasetType  = "QCD factorised",
        datasetDefinitions = ["Tau_"],
        MCEWKDatasetDefinitions = ["TTJets","WJets","W1Jets","W2Jets","W3Jets","W4Jets","DY","WW","WZ","ZZ","T_","Tbar_"],
        #MCEWKDatasetDefinitions = ["TTJets","W2Jets","DY","WW","WZ","ZZ","T_","Tbar_"],
        nuisances    = ["QCDfact_syst","stat_binByBin_QCDfact"],
        QCDfactorisedInfo = { "afterStdSelSource": QCDFactorisedStdSelVersion+"/NevtAfterStandardSelections",
                              "afterMETLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg1",
                              "afterTauLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg2",
                              "afterMETandTauLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg1AndLeg2", # for checking only
                              "closureMETShapeSource": [QCDFactorisedStdSelVersion+"/CtrlMET",
                                                        QCDFactorisedStdSelVersion+"/CtrlMETAfterLeg1",
                                                        QCDFactorisedStdSelVersion+"/CtrlMETAfterLeg2"],
                              "closureMETShapeDetails": QCDFactorisedValidationMETShapeHistogramsDimensions,
                              "finalShapeHisto": QCDFactorisedStdSelVersion+"/MtAfterLeg1", # prefix for shape histograms in MET leg (will be weighted by tau leg efficiency)
                              "closureShapeSource": [QCDFactorisedStdSelVersion+"/MtAfterStandardSelections",
                                                     QCDFactorisedStdSelVersion+"/MtAfterLeg1",
                                                     QCDFactorisedStdSelVersion+"/MtAfterLeg2"],
                              "closureShapeDetails": QCDFactorisedValidationMtShapeHistogramsDimensions,
                              "factorisationSchema" : OptionQCDfactorisedFactorisationSchema,
                              #"assumedMCEWKSystUncertainty": 0.20, # has no effect anymore ... # not needed
                              #"factorisationMapAxisLabels": ["#tau p_{T}, GeV", "#tau #eta", "N_{vertices}"], # not needed
                              #"METShapeCorrections": QCDFactorisationMETShapeCorrections,
                              #"MTShapeCorrections": QCDFactorisationMtShapeCorrections,
                              #FIXME: add systematics definition (tau trg uncer as function of tau bins, trg MET leg, tauID, energy scales, btagging, xsection)
        }
    ))
elif OptionMassShape == "FullMass":
    DataGroups.append(DataGroup(
        label        = "QCDfact",
        landsProcess = 3,
        validMassPoints = MassPoints,
        #dirPrefix   = QCDFactorisedAnalysis,
        datasetType  = "QCD factorised",
        datasetDefinitions = ["Tau_"],
        MCEWKDatasetDefinitions = ["TTJets","WJets","W1Jets","W2Jets","W3Jets","W4Jets","DY","WW","WZ","ZZ","T_","Tbar_"],
        #MCEWKDatasetDefinitions = ["TTJets","W2Jets","W3Jets","W4Jets","DY","WW","WZ","ZZ","T_","Tbar_"],
        nuisances    = ["QCDfact_syst","stat_binByBin_QCDfact"],
        QCDfactorisedInfo = { "afterStdSelSource": QCDFactorisedStdSelVersion+"/NevtAfterStandardSelections",
                              "afterMETLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg1",
                              "afterTauLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg2",
                              "afterMETandTauLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg1AndLeg2", # for checking only
                              "closureMETShapeSource": [QCDFactorisedStdSelVersion+"/CtrlMET",
                                                        QCDFactorisedStdSelVersion+"/CtrlMETAfterLeg1",
                                                        QCDFactorisedStdSelVersion+"/CtrlMETAfterLeg2"],
                              "closureMETShapeDetails": QCDFactorisedValidationMETShapeHistogramsDimensions,
                              "finalShapeHisto": QCDFactorisedStdSelVersion+"/MassAfterLeg1", # prefix for shape histograms in MET leg (will be weighted by tau leg efficiency)
                              "closureShapeSource": [QCDFactorisedStdSelVersion+"/MassAfterStandardSelections",
                                                     QCDFactorisedStdSelVersion+"/MassAfterLeg1",
                                                     QCDFactorisedStdSelVersion+"/MassAfterLeg2"],
                              "closureShapeDetails": QCDFactorisedValidationMtShapeHistogramsDimensions,
                              #"assumedMCEWKSystUncertainty": 0.20, # has no effect anymore ... # not needed
                              #"factorisationMapAxisLabels": ["#tau p_{T}, GeV", "#tau #eta", "N_{vertices}"], # not needed
                              #"METShapeCorrections": QCDFactorisationMETShapeCorrections,
                              #"MTShapeCorrections": QCDFactorisationMtShapeCorrections,
                              #FIXME: add systematics definition (tau trg uncer as function of tau bins, trg MET leg, tauID, energy scales, btagging, xsection)
        }
    ))

DataGroups.append(DataGroup(
    label        = "QCDinv",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD inverted",
    datasetDefinitions   = "Data",
    shapeHisto   = "mtSum",
    #dirPrefix   = QCDInvertedAnalysis,
    rateCounter  = "integral",
#    additionalNormalisation = 1.0,
    nuisances    = ["stat_QCDinv","42","43","44"] # FIXME: add shape stat, i.e. 40x,
))

if not OptionReplaceEmbeddingByMC:
    # EWK + ttbar with genuine taus
    EmbeddingIdList = [4]
    DataGroups.append(DataGroup(
        label        = "EWK_Tau",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        #datasetDefinitions   = ["SingleMu"],
        datasetDefinitions   = ["Data"],
        #dirPrefix   = EmbeddingAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        additionalNormalisation = 1.0907,
        nuisances    = ["trg_tau_embedding","tau_ID","Emb_QCDcontam","Emb_WtauTomu","Emb_musel_ditau_mutrg","stat_Emb","stat_binByBin","ES_taus_tempForEmbedding"]
        #nuisances    = ["trg_tau_embedding","tau_ID","ES_taus","Emb_QCDcontam","Emb_WtauTomu","Emb_musel_ditau_mutrg","stat_Emb","stat_binByBin"]
    ))

    # EWK + ttbar with fake taus
    EWKFakeIdList = [1,5,6]
    DataGroups.append(DataGroup(
        label        = "EWK_tt_faketau",
        landsProcess = 1,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["TTJets_"],
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_fakes","trg_MET","tau_misID","ES_taus_fakes","ES_jets_fakes","ES_METunclustered_fakes","e_mu_veto_fakes","b_tag_fakes","xsect_tt_7TeV","lumi","pileup_fakes","stat_binByBin_fakes"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_W_faketau",
        landsProcess = 5,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["WJets","W1Jets","W2Jets","W3Jets","W4Jets"],
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_fakes","trg_MET","ES_taus_fakes","ES_jets_fakes","ES_METunclustered_fakes","e_mu_veto_fakes","b_mistag_fakes","xsect_Wjets","lumi","pileup_fakes","stat_binByBin_fakes"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_t_faketau",
        landsProcess = 6,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["T_", "Tbar_"],
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_fakes","trg_MET","ES_taus_fakes","ES_jets_fakes","ES_METunclustered_fakes","e_mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","pileup_fakes","stat_binByBin_fakes"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_DY_faketau",
        landsProcess = 7,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["DYJetsToLL"],
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_fakes","trg_MET","tau_misID","ES_taus_fakes","ES_jets_fakes","ES_METunclustered_fakes","e_mu_veto_fakes","b_mistag","xsect_DYtoll","lumi","pileup_fakes","stat_binByBin_fakes"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_VV_faketau",
        landsProcess = 8,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["WW","WZ","ZZ"],
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_fakes","trg_MET","tau_misID","ES_taus_fakes","ES_jets_fakes","ES_METunclustered_fakes","e_mu_veto_fakes","b_mistag","xsect_VV","lumi","pileup_fakes","stat_binByBin_fakes"]
    ))
else:
    # Mimic embedding with MC analysis (introduces double counting of EWK fakes, but that should be small effect)
    EmbeddingIdList = [1,4,5,6,7]
    DataGroups.append(DataGroup(
        label        = "MC_ttbar",
        landsProcess = 1,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["TTJets"],
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_embedding","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_tag","xsect_tt_7TeV","lumi","pileup","stat_binByBin"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_Wjets",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["WJets", "W1Jets", "W2Jets", "W3Jets", "W4Jets"],
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_embedding","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_mistag","xsect_Wjets","lumi","pileup","stat_binByBin"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_1top",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["Tbar_", "T_"],
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau_embedding","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_tag","xsect_singleTop","lumi","pileup","stat_binByBin"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_DY",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["DYJetsToLL"],
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_mistag","xsect_DYtoll","lumi","pileup","stat_binByBin"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_VV",
        landsProcess = 7,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["WW","WZ","ZZ"],
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["trg_tau","trg_MET","tau_ID","ES_taus","ES_jets","ES_METunclustered","e_mu_veto","b_mistag","xsect_VV","lumi","pileup","stat_binByBin"]
    ))
    #DataGroups.append(DataGroup(
        #label        = "empty",
        #landsProcess = 1,
        #datasetType  = "None",
        #validMassPoints = MassPoints,
    #))


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
# Note: Remember to include 'stat.' into the label of nuistances of statistical nature
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import Nuisance
ReservedNuisances = []
ReservedNuisances.append(["05", "reserved for leptonic"])
ReservedNuisances.append(["06", "reserved for leptonic"])
ReservedNuisances.append(["08", "reserved for leptonic"])
ReservedNuisances.append(["20", "reserved for leptonic"])
ReservedNuisances.append(["21", "reserved for leptonic"])
ReservedNuisances.append(["23", "reserved for leptonic"])
if OptionPurgeReservedLines:
    ReservedNuisances = []

Nuisances = []

Nuisances.append(Nuisance(
    id            = "trg_tau",
    label         = "tau+MET trg tau part",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["TauTriggerScaleFactorAbsUncert_AfterSelection"],
    normalisation = ["TauTriggerScaleFactorAbsUncertCounts_AfterSelection"],
))

Nuisances.append(Nuisance(
    id            = "trg_tau_embedding",
    label         = "tau+MET trg tau part for EWKtau (temp)",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.066
))

Nuisances.append(Nuisance(
    id            = "trg_tau_fakes",
    label         = "tau+MET trg tau part for EWK fake taus",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["TriggerScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["TriggerScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"],
))

Nuisances.append(Nuisance(
    id            = "trg_MET",
    label         = "tau+MET trg MET part",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.10
))

Nuisances.append(Nuisance(
    id            = "tau_ID",
    label         = "tau-jet ID (no Rtau)",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.06
))

Nuisances.append(Nuisance(
    id            = "tau_misID", 
    label         = "tau-jet mis ID (no Rtau)",  
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["FakeTauAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["FakeTauAbsUncertCounts_EWKFakeTausAfterSelection"],
))

if OptionIncludeSystematics:
    Nuisances.append(Nuisance(
        id            = "ES_taus",
        label         = "TES bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = SignalRateCounter,
        histoDir      = ["TESPlus",
                        "TESMinus"],
        histograms    = [SignalShapeHisto,
                        SignalShapeHisto]
    ))
    Nuisances.append(Nuisance(
        id            = "ES_taus_fakes",
        label         = "TES bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = FakeRateCounter,
        histoDir      = ["TESPlus",
                        "TESMinus"],
        histograms    = [FakeShapeHisto,
                        FakeShapeHisto]
    ))
    Nuisances.append(Nuisance(
        id            = "ES_jets",
        label         = "JES bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = SignalRateCounter,
        histoDir      = ["JESPlus",
                        "JESMinus"],
        histograms    = [SignalShapeHisto,
                        SignalShapeHisto]
    ))
    Nuisances.append(Nuisance(
        id            = "ES_jets_fakes",
        label         = "JES bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = FakeRateCounter,
        histoDir      = ["JESPlus",
                        "JESMinus"],
        histograms    = [FakeShapeHisto,
                        FakeShapeHisto]
    ))
    Nuisances.append(Nuisance(
        id            = "ES_METunclustered",
        label         = "MET unclustered scale bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = SignalRateCounter,
        histoDir      = ["METPlus",
                        "METMinus"],
        histograms    = [SignalShapeHisto,
                        SignalShapeHisto]
    ))
    Nuisances.append(Nuisance(
        id            = "ES_METunclustered_fakes",
        label         = "MET unclustered scale bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = FakeRateCounter,
        histoDir      = ["METPlus",
                        "METMinus"],
        histograms    = [FakeShapeHisto,
                        FakeShapeHisto]
    ))
else:
    Nuisances.append(Nuisance(
        id            = "ES_taus",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.03,
    ))
    Nuisances.append(Nuisance(
        id            = "ES_taus_fakes",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.03,
    ))
    Nuisances.append(Nuisance(
        id            = "ES_jets",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.03,
    ))
    Nuisances.append(Nuisance(
        id            = "ES_jets_fakes",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.03,
    ))
    Nuisances.append(Nuisance(
        id            = "ES_METunclustered",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.01,
    ))
    Nuisances.append(Nuisance(
        id            = "ES_METunclustered_fakes",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.01,
    ))

Nuisances.append(Nuisance(
    id            = "ES_taus_tempForEmbedding",
    label         = "Temporary TES for EWKtau",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.020,
))

Nuisances.append(Nuisance(
    id            = "e_mu_veto",
    label         = "lepton veto",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "muon veto", # main counter name after electron and muon veto
    denominator   = "tau trigger scale factor", # main counter name before electron and muon veto
    scaling       = 0.02
))

Nuisances.append(Nuisance(
    id            = "e_mu_veto_fakes",
    label         = "lepton veto",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "EWKfaketaus:muon veto", # main counter name after electron and muon veto
    denominator   = "EWKfaketaus:taus==1", # main counter name before electron and muon veto # the name is misleading, it is actually after tau trg scale factor
    scaling       = 0.02
))

Nuisances.append(Nuisance(
    id            = "b_tag",
    label         = "btagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_AfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "b_tag_fakes",
    label         = "btagging for EWK fake taus",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "b_mistag",
    label         = "mistagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_AfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "b_mistag_fakes",
    label         = "mistagging EWK fake taus",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "QCDfact_stat",
    label         = "QCD stat.",
    distr         = "lnN",
    function      = "QCDFactorised",
    QCDmode       = "statistics",
))

Nuisances.append(Nuisance(
    id            = "QCDfact_syst",
    label         = "QCD syst.",
    distr         = "lnN",
    function      = "QCDFactorised",
    QCDmode       = "systematics",
))

Nuisances.append(Nuisance(
    id            = "Emb_QCDcontam",
    label         = "EWK with taus QCD contamination",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.012
))

Nuisances.append(Nuisance(
    id            = "Emb_WtauTomu",
    label         = "EWK with taus W->tau->mu",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.007
))

Nuisances.append(Nuisance(
    id            = "Emb_musel_ditau_mutrg",
    label         = "EWK with taus muon selection+ditau+mu trg",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.031
))

Nuisances.append(Nuisance(
    id            = "stat_HH",
    label         = "MC signal stat., HH",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "stat_HW",
    label         = "MC signal stat., HW",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "stat_Hp",
    label         = "MC signal stat., H+",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "stat_Emb",
    label         = "EWK with taus stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "stat_tt_jjtau",
    label         = "tt->jjtau MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "stat_tt_jjtau_fakes",
    label         = "ttbar fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "stat_DYtautau",
    label         = "Z->tautau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "stat_DYtautau_fakes", 
    label         = "Z->tautau fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "stat_Wjets",
    label         = "W+jets MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = SignalRateCounter
))

Nuisances.append(Nuisance(
    id            = "stat_Wjets_fakes",  
    label         = "W+jets fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "stat_singleTop",
    label         = "Single top MC stat.",
    distr         = "lnN",
    function      = "Constant",
    value         = SignalRateCounter
))

Nuisances.append(Nuisance(
    id            = "stat_singleTop_fakes",
    label         = "single top fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "stat_VV",
    label         = "diboson MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter
))

Nuisances.append(Nuisance(
    id            = "stat_VV_fakes", 
    label         = "diboson fake tau MC stat.",
    distr         = "lnN",
    function      = "Counter",
    counter       = FakeRateCounter
))

Nuisances.append(Nuisance(
    id            = "xsect_tt_7TeV",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.062,
    upperValue    = 0.053,
))

Nuisances.append(Nuisance(
    id            = "xsect_tt_8TeV",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.060,
    upperValue    = 0.053,
))

Nuisances.append(Nuisance(
    id            = "xsect_Wjets",
    label         = "W+jets cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.05
))

Nuisances.append(Nuisance(
    id            = "xsect_singleTop",
    label         = "single top cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.08
))

Nuisances.append(Nuisance(
    id            = "xsect_DYtoll",
    label         = "Z->ll cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04
))

Nuisances.append(Nuisance(
    id            = "xsect_VV",
    label         = "diboson cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04
))

Nuisances.append(Nuisance(
    id            = "lumi",
    label         = "luminosity",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.022
))

if OptionIncludeSystematics:
    Nuisances.append(Nuisance(
        id            = "pileup",
        label         = "pileup",
        distr         = "lnN",
        function      = "pileupUncertainty",
        histoDir      = ["", # nominal
                        "PUWeightMinus", # minus
                        "PUWeightPlus"], # up
        counter       = SignalRateCounter
    ))

    Nuisances.append(Nuisance(
        id            = "pileup_fakes",
        label         = "pileup",
        distr         = "lnN",
        function      = "pileupUncertainty",
        histoDir      = ["", # nominal
                        "PUWeightMinus", # minus
                        "PUWeightPlus"], # up
        counter       = FakeRateCounter
    ))
else:
    Nuisances.append(Nuisance(
        id            = "pileup",
        label         = "FAKE pileup",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05
    ))

    Nuisances.append(Nuisance(
        id            = "pileup_fakes",
        label         = "FAKE pileup",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05
    ))


Nuisances.append(Nuisance(
    id            = "stat_binByBin",
    label         = "Bin-by-bin stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "Shape",
    counter       = SignalRateCounter,
    histoDir      = [""],
    histograms    = [SignalShapeHisto],
))

Nuisances.append(Nuisance(
    id            = "stat_binByBin_QCDfact",
    label         = "Bin-by-bin stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "QCDFactorised",
    QCDmode       = "shapestat"
))

Nuisances.append(Nuisance(
    id            = "stat_binByBin_fakes",
    label         = "Bin-by-bin stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "Shape",
    counter       = FakeRateCounter,
    histoDir      = [""],
    histograms    = [FakeShapeHisto],
))

Nuisances.append(Nuisance(
    id            = "stat_QCDinv",
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
MergeNuisances.append(["trg_tau","trg_tau_embedding","trg_tau_fakes"])
MergeNuisances.append(["ES_taus","ES_taus_fakes","ES_taus_tempForEmbedding"])
MergeNuisances.append(["ES_jets","ES_jets_fakes"])
MergeNuisances.append(["ES_METunclustered","ES_METunclustered_fakes"])
MergeNuisances.append(["e_mu_veto","e_mu_veto_fakes"])
MergeNuisances.append(["b_tag","b_tag_fakes"])
MergeNuisances.append(["b_mistag","b_mistag_fakes"])
MergeNuisances.append(["pileup","pileup_fakes"])
MergeNuisances.append(["stat_binByBin","stat_binByBin_QCDfact","stat_binByBin_fakes"])

# Control plots
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import ControlPlotInput
ControlPlots = []
ControlPlots.append(ControlPlotInput(
    title            = "Njets",
    signalHHid       = [-1],
    signalHWid       = [0],
    QCDid            = [3],
    embeddingId      = EmbeddingIdList,
    EWKfakeId        = EWKFakeIdList,
    signalHistoPath  = "ControlPlots",
    signalHistoName  = "Njets_AfterStandardSelections",
    EWKfakeHistoPath  = "ControlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "Njets_AfterStandardSelections",
    QCDFactNormalisation = QCDFactorisedStdSelVersion+"/CtrlNjets",
    QCDFactHistoName = QCDFactorisedStdSelVersion+"/CtrlNjets",
    details          = { "bins": 5,
                         "rangeMin": 3.0,
                         "rangeMax": 8.0,
                         "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         "binLabels": ["3","4","5","6","7"], # leave empty to disable bin labels
                         "xtitle": "Number of selected jets",
                         "ytitle": "Events",
                         "unit": "",
                         "logy": True,
                         "DeltaRatio": 0.5,
                         "ymin": 0.9,
                         "ymax": -1},
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

for i in range(0,4):
    ControlPlots.append(ControlPlotInput(
        title            = "CollinearTailKillerJet%d"%(i+1),
        signalHHid       = [-1],
        signalHWid       = [0],
        QCDid            = [3],
        embeddingId      = EmbeddingIdList,
        EWKfakeId        = EWKFakeIdList,
        signalHistoPath  = "ControlPlots",
        signalHistoName  = "QCDTailKillerJet%dCollinear"%i,
        EWKfakeHistoPath  = "ControlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "QCDTailKillerJet%dCollinear"%i,
        QCDFactNormalisation = QCDFactorisedStdSelVersion+"/QCDTailKillerJet%dCollinear"%i,
        QCDFactHistoName = QCDFactorisedStdSelVersion+"/QCDTailKillerJet%dCollinear"%i,
        details          = { "bins": 26,
                             "rangeMin": 0.0,
                             "rangeMax": 260.0,
                             "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                             "binLabels": [], # leave empty to disable bin labels
                             "xtitle": "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{%d},MET))^{2}}"%(i+1),
                             "ytitle": "Events",
                             "unit": "^{o}",
                             "logy": True,
                             "DeltaRatio": 0.5,
                             "ymin": 0.9,
                             "ymax": -1},
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    if i == 0:
        ControlPlots[len(ControlPlots)-1].flowPlotCaption = "#tau_{h}+#geq3j"
    else:
        ControlPlots[len(ControlPlots)-1].flowPlotCaption = "#Delta#phi_{#uparrow#uparrow,%d}"%(i)

ControlPlots.append(ControlPlotInput(
    title            = "MET",
    signalHHid       = [-1],
    signalHWid       = [0],
    QCDid            = [3],
    embeddingId      = EmbeddingIdList,
    EWKfakeId        = EWKFakeIdList,
    signalHistoPath  = "ControlPlots",
    signalHistoName  = "MET",
    EWKfakeHistoPath  = "ControlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "MET",
    QCDFactNormalisation = QCDFactorisedStdSelVersion+"/CtrlMET",
    QCDFactHistoName = QCDFactorisedStdSelVersion+"/CtrlMET",
    details          = { "bins": 13,
                         "rangeMin": 0.0,
                         "rangeMax": 500.0,
                         #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                         "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                         "binLabels": [], # leave empty to disable bin labels
                         "xtitle": "E_{T}^{miss}",
                         "ytitle": "Events",
                         "unit": "GeV",
                         "logy": True,
                         "DeltaRatio": 0.5,
                         "ymin": 0.9,
                         "ymax": -1},
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "#Delta#phi_{#uparrow#uparrow,4}", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "BJetSelection",
    signalHHid       = [-1],
    signalHWid       = [0],
    QCDid            = [3],
    embeddingId      = EmbeddingIdList,
    EWKfakeId        = EWKFakeIdList,
    signalHistoPath  = "ControlPlots",
    signalHistoName  = "NBjets",
    EWKfakeHistoPath  = "ControlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "NBjets",
    QCDFactNormalisation = QCDFactorisedStdSelVersion+"/CtrlNbjets",
    QCDFactHistoName = QCDFactorisedStdSelVersion+"/CtrlNbjets",
    details          = { "bins": 5,
                         "rangeMin": 0.0,
                         "rangeMax": 5.0,
                         "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         "binLabels": ["0","1","2","3","4"], # leave empty to disable bin labels
                         "xtitle": "Number of selected b jets",
                         "ytitle": "Events",
                         "unit": "",
                         "logy": True,
                         "DeltaRatio": 0.5,
                         "ymin": 0.9,
                         "ymax": -1},
    blindedRange=[],
    #blindedRange     = [1.5,10], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "E_{T}^{miss}", # Leave blank if you don't want to include the item to the selection flow plot
))

#TODO: add as preselection for all ctrl plots in signal analysis MET30 and/or collinear tail killer and/or full tail killer
#TODO: Add to signal analysis ctrl plots tail killer plots

#ControlPlots.append(ControlPlotInput(
    #title            = "DeltaPhi",
    #signalHHid       = [-1],
    #signalHWid       = [0],
    #QCDid            = [3],
    #embeddingId      = EmbeddingIdList,
    #EWKfakeId        = EWKFakeIdList,
    #signalHistoPath  = "",
    #signalHistoName  = "deltaPhi",
    #EWKfakeHistoPath  = "",
    #EWKfakeHistoName  = "EWKFakeTausDeltaPhi",
    #QCDFactNormalisation = QCDFactorisedStdSelVersion+"/factorisation/Leg1AfterBTagging",
    #QCDFactHistoName = QCDFactorisedStdSelVersion+"/CtrlLeg1AfterDeltaPhiTauMET", #FIXME
    #details          = { "bins": 11,
                         #"rangeMin": 0.0,
                         #"rangeMax": 180.0,
                         #"variableBinSizeLowEdges": [0., 10., 20., 30., 40., 60., 80., 100., 120., 140., 160.], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xtitle": "#Delta#phi(#tau_{h},E_{T}^{miss})",
                         #"ytitle": "Events",
                         #"unit": "^{o}",
                         #"logy": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "N_{b jets}", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "MaxDeltaPhi",
    #signalHHid       = [-1],
    #signalHWid       = [0],
    #QCDid            = [3],
    #embeddingId      = EmbeddingIdList,
    #EWKfakeId        = EWKFakeIdList,
    #signalHistoPath  = "",
    #signalHistoName  = "maxDeltaPhiJetMet",
    #QCDFactNormalisation = QCDFactorisedStdSelVersion+"/factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoName = QCDFactorisedStdSelVersion+"/CtrlLeg1AfterMaxDeltaPhiJetMET", #FIXME
    #details          = { "bins": 18,
                         #"rangeMin": 0.0,
                         #"rangeMax": 180.0,
                         #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xtitle": "max(#Delta#phi(jet,E_{T}^{miss})",
                         #"ytitle": "Events",
                         #"unit": "^{o}",
                         #"logy": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "#Delta#phi(#tau_{h},E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "WMass",
    #signalHHid       = [-1],
    #signalHWid       = [0],
    #QCDid            = [3],
    #embeddingId      = EmbeddingIdList,
    #EWKfakeId        = EWKFakeIdList,
    #signalHistoPath  = "TopChiSelection",
    #signalHistoName  = "WMass",
    #QCDFactNormalisation = QCDFactorisedStdSelVersion+"/factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoName = QCDFactorisedStdSelVersion+"/CtrlLeg1AfterTopMass", #FIXME
    #details          = { "bins": 20,
                         #"rangeMin": 0.0,
                         #"rangeMax": 200.0,
                         #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xtitle": "m_{jj}",
                         #"ytitle": "Events",
                         #"unit": "GeV/c^{2}",
                         #"logy": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 400], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "TopMass",
    #signalHHid       = [-1],
    #signalHWid       = [0],
    #QCDid            = [3],
    #embeddingId      = EmbeddingIdList,
    #EWKfakeId        = EWKFakeIdList,
    #signalHistoPath  = "TopChiSelection",
    #signalHistoName  = "TopMass",
    #QCDFactNormalisation = QCDFactorisedStdSelVersion+"/factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoName = QCDFactorisedStdSelVersion+"/CtrlLeg1AfterTopMass", #FIXME
    #details          = { "bins": 20,
                         #"rangeMin": 0.0,
                         #"rangeMax": 400.0,
                         #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xtitle": "m_{bjj}",
                         #"ytitle": "Events",
                         #"unit": "GeV/c^{2}",
                         #"logy": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 400], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

for i in range(0,4):
    ControlPlots.append(ControlPlotInput(
        title            = "BackToBackTailKillerJet%d"%(i+1),
        signalHHid       = [-1],
        signalHWid       = [0],
        QCDid            = [3],
        embeddingId      = EmbeddingIdList,
        EWKfakeId        = EWKFakeIdList,
        signalHistoPath  = "ControlPlots",
        signalHistoName  = "QCDTailKillerJet%dBackToBack"%i,
        EWKfakeHistoPath  = "ControlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "QCDTailKillerJet%dBackToBack"%i,
        QCDFactNormalisation = QCDFactorisedStdSelVersion+"/QCDTailKillerJet%dBackToBack"%i,
        QCDFactHistoName = QCDFactorisedStdSelVersion+"/QCDTailKillerJet%dBackToBack"%i,
        details          = { "bins": 13,
                             "rangeMin": 0.0,
                             "rangeMax": 260.0,
                             "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                             "binLabels": [], # leave empty to disable bin labels
                             "xtitle": "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{%d},MET))^{2}}"%(i+1),
                             "ytitle": "Events",
                             "unit": "^{o}",
                             "logy": True,
                             "DeltaRatio": 0.5,
                             "ymin": 0.9,
                             "ymax": -1},
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    if i == 0:
        ControlPlots[len(ControlPlots)-1].flowPlotCaption = "#geq1 b tag"
    else:
        ControlPlots[len(ControlPlots)-1].flowPlotCaption = "#Delta#phi_{#uparrow#downarrow,%d}"%(i)
ControlPlots.append(ControlPlotInput(
    title            = "TransverseMass",
    signalHHid       = [-1],
    signalHWid       = [0],
    QCDid            = [3],
    embeddingId      = EmbeddingIdList,
    EWKfakeId        = EWKFakeIdList,
    signalHistoPath  = "",
    signalHistoName  = "transverseMass",
    EWKfakeHistoPath  = "",
    EWKfakeHistoName  = "EWKFakeTausTransverseMass",
    QCDFactNormalisation = QCDFactorisedStdSelVersion+"/NevtAfterLeg1",
    QCDFactHistoName = QCDFactorisedStdSelVersion+"/MtAfterLeg1",
    details          = { "bins": 13,
                         "rangeMin": 0.0,
                         "rangeMax": 400.0,
                         "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                         "binLabels": [], # leave empty to disable bin labels
                         "xtitle": "mT(#tau_{h},E_{T}^{miss})",
                         "ytitle": "Events",
                         "unit": "GeV/c^{2}",
                         "logy": False,
                         "DeltaRatio": 0.5,
                         "ymin": 0.9,
                         "ymax": -1},
    blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [60, 180], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "#Delta#phi_{#uparrow#downarrow,4}", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "FullMass",
    signalHHid       = [-1],
    signalHWid       = [0],
    QCDid            = [3],
    embeddingId      = EmbeddingIdList,
    EWKfakeId        = EWKFakeIdList,
    signalHistoPath  = "FullHiggsMass",
    signalHistoName  = "HiggsMass",
    EWKfakeHistoPath  = "",
    EWKfakeHistoName  = "EWKFakeTausFullMass",
    QCDFactNormalisation = QCDFactorisedStdSelVersion+"/NevtAfterLeg1",
    QCDFactHistoName = QCDFactorisedStdSelVersion+"/MassAfterLeg1",
    details          = { "bins": 13,
                         "rangeMin": 0.0,
                         "rangeMax": 500.0,
                         "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                         "binLabels": [], # leave empty to disable bin labels
                         "xtitle": "m(#tau_{h},E^{miss})",
                         "ytitle": "Events",
                         "unit": "GeV/c^{2}",
                         "logy": False,
                         "DeltaRatio": 0.5,
                         "ymin": 0.9,
                         "ymax": -1},
    blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [80, 180], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

if False:
    ControlPlots.append(ControlPlotInput(
        title            = "NjetsAfterMET",
        signalHHid       = [-1],
        signalHWid       = [0],
        QCDid            = [3],
        embeddingId      = EmbeddingIdList,
        EWKfakeId        = EWKFakeIdList,
        signalHistoPath  = "ControlPlots",
        signalHistoName  = "NjetsAfterMET",
        EWKfakeHistoPath  = "ControlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "NjetsAfterMET",
        QCDFactNormalisation = "Njets",
        QCDFactHistoPath = QCDFactorisedStdSelVersion,
        QCDFactHistoName = "", # FIXME
        details          = { "bins": 5,
                             "rangeMin": 3.0,
                             "rangeMax": 8.0,
                             "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                             "binLabels": ["3","4","5","6","7"], # leave empty to disable bin labels
                             "xtitle": "Number of selected jets",
                             "ytitle": "Events",
                             "unit": "",
                             "logy": True,
                             "DeltaRatio": 0.5,
                             "ymin": 0.9,
                             "ymax": -1},
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

