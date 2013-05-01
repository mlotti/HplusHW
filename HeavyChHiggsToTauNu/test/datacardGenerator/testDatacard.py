DataCardName    = 'myDummyTestName'
Path            = '/home/wendland/data/v445/met50'
#Path            = '/mnt/flustre/slehti/hplusAnalysis/QCDInverted/CMSSW_4_4_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/datacardGenerator/TESTDATA/'
#MassPoints      = [80,90,100,120,140,150,155,160]
#MassPoints      = [80,90,100,120,140,150,155,160]
#MassPoints      = [80,120,160]
MassPoints      = [120]

BlindAnalysis   = True

# Specify name of EDFilter or EDAnalyser process that produced the root files

# FIXME: remove this block
SignalAnalysis  = "signalAnalysis"
EmbeddingAnalysis     = "signalAnalysis"
#EmbeddingAnalysis     = "signalAnalysisCaloMet60TEff"
#EmbeddingAnalysis     = "signalAnalysisCaloMet60"
QCDFactorisedAnalysis = True
QCDInvertedAnalysis = True

RootFileName    = "histograms.root"

# Rate counter definitions
SignalRateCounter = "Selected events"
FakeRateCounter = "EWKfaketaus:SelectedEvents"

# Options
OptionMassShape = "TransverseMass"
#OptionMassShape = "FullMass"
OptionReplaceEmbeddingByMC = True
OptionIncludeSystematics = False # Set to true if the JES and PU uncertainties were produced
OptionPurgeReservedLines = True # Makes limit running faster, but cannot combine leptonic datacards
OptionDoControlPlots = False

# Options for reports and article
OptionBr = 0.01  # Br(t->bH+)

# Tolerance for throwing error on luminosity difference (0.01 = 1 percent agreement is required)
ToleranceForLuminosityDifference = 0.01

# Shape histogram definitions
SignalShapeHisto = ""
FakeShapeHisto = ""
ShapeHistogramsDimensions = {}

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

DataCardName += "_"+OptionMassShape

##############################################################################
# Specifications for QCD factorised

QCDFactorisedStdSelVersion = "QCDfactorised_TradReference"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusMET30"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusCollinearTailKiller"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusMET30PlusCollinearTailKiller"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusTailKiller"
#QCDFactorisedStdSelVersion = "QCDfactorised_TradPlusMET30PlusTailKiller"

QCDFactorisedValidationMETShapeHistogramsDimensions = {  "bins": 7,
                                                         "rangeMin": 0.0,
                                                         "rangeMax": 100.0,
                                                         #"variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160,180,200,250,300], # if an empty list is given, then uniform bin width is used
                                                         "variableBinSizeLowEdges": [0,10,20,30,40,50,60], # if an empty list is given, then uniform bin width is used
                                                         "xtitle": "E_{T}^{miss}, GeV/c^{2}",
                                                         "ytitle": "Events"}
QCDFactorisedValidationMtShapeHistogramsDimensions = { "bins": 9,
                                                        "rangeMin": 0.0,
                                                        "rangeMax": 400.0,
                                                        #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                                                        "variableBinSizeLowEdges": [0,20,40,60,80,100,120,140,160], # if an empty list is given, then uniform bin width is used
                                                        "xtitle": "Transverse mass / GeV",
                                                        "ytitle": "Events" }
QCDFactorisationMETShapeCorrections = {
    "source": "shape_CtrlLeg1METAfterStandardSelections/CtrlLeg1METAfterStandardSelections",
    "name": "QCDfactorised_validation_MET_1D_Full",
    "bins": [8, 1, 1],
    "QCDfactorised_validation_MET_1D_Full_CorrectionBinLeftEdges": [0.00, 10.00, 20.00, 30.00, 40.00, 50.00, 60.00],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_0": [1.036104, 1.048980, 1.104733, 1.271495, 1.120040, 0.869107, 0.266232],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_0": [0.416069, 0.328825, 0.319309, 0.362864, 0.360971, 0.338884, 0.274786],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_1": [1.010068, 1.032821, 0.844114, 0.955167, 1.160494, 1.047382, 1.052456],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_1": [0.432928, 0.346066, 0.283326, 0.315546, 0.395032, 0.434501, 0.589872],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_2": [0.998914, 0.932571, 1.025616, 1.231595, 1.053585, 1.475297, 0.136521],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_2": [0.477292, 0.356867, 0.362464, 0.441395, 0.410757, 0.635094, 0.254122],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_3": [1.031436, 0.959958, 0.928372, 1.234895, 1.199805, 1.291159, 0.185898],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_3": [0.492214, 0.369971, 0.342328, 0.437485, 0.463561, 0.578932, 0.295029],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_4": [0.975548, 0.880998, 1.054509, 1.171911, 1.081376, 1.256730, 0.406191],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_4": [0.422501, 0.312712, 0.343169, 0.383368, 0.394789, 0.510742, 0.414343],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_5": [0.876624, 0.808355, 1.263013, 1.328661, 1.069023, 0.971516, 0.092730],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_5": [0.437259, 0.329263, 0.446820, 0.483494, 0.450331, 0.477194, 0.198666],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_6": [0.754988, 1.255687, 1.159182, 0.861225, 1.187017, 0.900584, 0.408189],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_6": [0.414640, 0.493161, 0.447875, 0.371869, 0.525709, 0.491353, 0.433724],
    "QCDfactorised_validation_MET_1D_Full_Correction_bin_7": [1.251079, 1.227791, 1.070303, 0.952361, 0.948940, 0.945502, 0.597940],
    "QCDfactorised_validation_MET_1D_Full_CorrectionUncertainty_bin_7": [0.745487, 0.510899, 0.448428, 0.420891, 0.501961, 0.605113, 0.476329],
}
QCDFactorisationMtShapeCorrections = {
    "source": "shape_MtShapesAfterStandardSelection/MtShapesAfterStandardSelection",
    "name": "QCDfactorised_validation_mT_1D_Full",
    "bins": [8, 1, 1],
    "QCDfactorised_validation_mT_1D_Full_CorrectionBinLeftEdges": [0.00, 20.00, 40.00, 60.00, 80.00, 100.00, 120.00, 140.00, 160.00],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_0": [0.532105, 0.886371, 1.094611, 1.250627, 1.166074, 0.966448, 0.364552, 1.247514, 3.075688],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_0": [0.313213, 0.370488, 0.379840, 0.379706, 0.363649, 0.425371, 0.422977, 1.379275, 3.634559],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_1": [0.648265, 0.892773, 0.712239, 1.182355, 1.079627, 1.285717, 1.688803, 0.604024, 2.176340],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_1": [0.389642, 0.414163, 0.354686, 0.366951, 0.349099, 0.456941, 0.793534, 0.602436, 2.105546],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_2": [0.638710, 0.170776, 0.864587, 0.980271, 1.290615, 1.364725, 1.358832, 1.799790, 0.738001],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_2": [0.501238, 0.237155, 0.453104, 0.373533, 0.433880, 0.499816, 0.639113, 1.164577, 0.967887],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_3": [0.486865, 0.736137, 0.549256, 1.074207, 1.161940, 1.285372, 1.396731, 1.043410, 0.145336],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_3": [0.376391, 0.508303, 0.377718, 0.413258, 0.423712, 0.464729, 0.631370, 0.639868, 0.268567],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_4": [0.211087, 0.523989, 0.798778, 0.851101, 1.355641, 1.209534, 1.230425, 1.141673, 0.992386],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_4": [0.266977, 0.476130, 0.377749, 0.329276, 0.435799, 0.398475, 0.460436, 0.605035, 0.609689],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_5": [0.333443, 0.723946, 0.820675, 0.766779, 1.006963, 1.200128, 1.389728, 1.299009, 0.838164],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_5": [0.373534, 0.419942, 0.501918, 0.392262, 0.429668, 0.460171, 0.533044, 0.571198, 0.472024],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_6": [0.271905, 0.678116, 0.739706, 1.035079, 1.171607, 1.204750, 1.214119, 1.009838, 1.003941],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_6": [0.377428, 0.518778, 0.502265, 0.509721, 0.525553, 0.511417, 0.516851, 0.471444, 0.456217],
    "QCDfactorised_validation_mT_1D_Full_Correction_bin_7": [1.085690, 1.389372, 0.128390, 1.269037, 0.847800, 0.997187, 1.447119, 0.826870, 0.969181],
    "QCDfactorised_validation_mT_1D_Full_CorrectionUncertainty_bin_7": [0.818243, 0.872531, 0.251288, 0.851395, 0.550802, 0.506219, 0.658021, 0.424001, 0.373741],
}
QCDFactorisedValidationMETShapeSource = [
    "shape_CtrlLeg1METAfterStandardSelections/CtrlLeg1METAfterStandardSelections",
    "shape_CtrlLeg1METAfterStandardSelectionsMET20/CtrlLeg1METAfterStandardSelectionsMET20",
    "shape_CtrlLeg1METAfterStandardSelectionsMET30/CtrlLeg1METAfterStandardSelectionsMET30",
    "shape_CtrlLeg1METAfterTauIDNoRtau/CtrlLeg1METAfterTauIDNoRtau",
    "shape_CtrlLeg1METAfterTauIDNoRtauMET20/CtrlLeg1METAfterTauIDNoRtauMET20",
    "shape_CtrlLeg1METAfterTauIDNoRtauMET30/CtrlLeg1METAfterTauIDNoRtauMET30",
    "shape_CtrlLeg1METAfterFullTauID/CtrlLeg1METAfterFullTauID",
    "shape_CtrlLeg1METAfterFullTauIDMET20/CtrlLeg1METAfterFullTauIDMET20",
    "shape_CtrlLeg1METAfterFullTauIDMET30/CtrlLeg1METAfterFullTauIDMET30",
]
QCDFactorisedValidationMtShapeSource = [
    "shape_MtShapesAfterStandardSelection/MtShapesAfterStandardSelection",
    "shape_MtShapesAfterStandardSelectionMET20/MtShapesAfterStandardSelectionMET20",
    "shape_MtShapesAfterStandardSelectionMET30/MtShapesAfterStandardSelectionMET30",
    "shape_MtShapesAfterTauIDNoRtau/MtShapesAfterTauIDNoRtau",
    "shape_MtShapesAfterTauIDNoRtauMET20/MtShapesAfterTauIDNoRtauMET20",
    "shape_MtShapesAfterTauIDNoRtauMET30/MtShapesAfterTauIDNoRtauMET30",
    "shape_MtShapesAfterTauID/MtShapesAfterTauID",
    "shape_MtShapesAfterTauIDMET20/MtShapesAfterTauIDMET20",
    "shape_MtShapesAfterTauIDMET30/MtShapesAfterTauIDMET30",
]

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

for mass in MassPoints:
    myMassList = [mass]
    hhx = signalTemplate.clone()
    hhx.setLabel("HH"+str(mass)+"_a")
    hhx.setLandSProcess(-1)
    hhx.setValidMassPoints(myMassList)
    hhx.setNuisances(["01","02","03","45","46","47","09","10","17","28","33","34"])
    hhx.setDatasetDefinitions(["TTToHplusBHminusB_M"+str(mass)]),
    DataGroups.append(hhx)

    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(["01","02","03","45","46","47","09","10","18","28","33","34"])
    hwx.setDatasetDefinitions(["TTToHplusBWB_M"+str(mass)]),
    DataGroups.append(hwx)


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
        nuisances    = ["12","13","40b"],
        QCDfactorisedInfo = { "afterStdSelSource": QCDFactorisedStdSelVersion+"/NevtAfterStandardSelections",
                              "afterMETLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg1",
                              "afterTauLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg2",
                              "afterMETandTauLegSource": QCDFactorisedStdSelVersion+"/NevtAfterLeg1AndLeg2", # for checking only
                              "validationMETShapeSource": QCDFactorisedValidationMETShapeSource, # FIXME check
                              "validationMETShapeDetails": QCDFactorisedValidationMETShapeHistogramsDimensions, # FIXME check
                              "basicMtHisto": QCDFactorisedStdSelVersion+"/MtAfterLeg1", # prefix for shape histograms in MET leg (will be weighted by tau leg efficiency)
                              "validationMtShapeSource": QCDFactorisedValidationMtShapeSource, # FIXME check
                              "validationMtShapeDetails": QCDFactorisedValidationMtShapeHistogramsDimensions, # FIXME check
                              "assumedMCEWKSystUncertainty": 0.20, # has no effect anymore ... # FIXME check
                              "factorisationMapAxisLabels": ["#tau p_{T}, GeV", "#tau #eta", "N_{vertices}"], # FIXME check
                              #"METShapeCorrections": QCDFactorisationMETShapeCorrections,
                              #"MTShapeCorrections": QCDFactorisationMtShapeCorrections,
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
        nuisances    = ["12","13","40b"],
        QCDfactorisedInfo = { "afterStdSelSource": "factorisation/AfterJetSelection",
                              "afterMETLegSource": "factorisation/Leg1AfterTopSelection",
                              "afterTauLegSource": "factorisation/Leg2AfterTauID",
                              "validationMETShapeSource": QCDFactorisedValidationMETShapeSource,
                              "validationMETShapeDetails": [],
                              "basicMtHisto": "shape_FullMassShapesAfterFullMETLeg/FullMassShapesAfterFullMETLeg", # prefix for shape histograms in MET leg (will be weighted by tau leg efficiency)
                              "validationMtShapeSource": QCDFactorisedValidationMtShapeSource,
                              "validationMtShapeDetails": [],
                              "validationMtShapeSource": [],
                              "assumedMCEWKSystUncertainty": 0.20,
                              "factorisationMapAxisLabels": ["#tau p_{T}, GeV", "#tau #eta", "N_{vertices}"],
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
    nuisances    = ["41","42","43","44"] # FIXME: add shape stat, i.e. 40x
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
        nuisances    = ["01b","03","14","15","16","19","40","48"]
        #nuisances    = ["01b","03","45","14","15","16","19","40"]
    ))
    
    #DataGroups.append(DataGroup(
        #label        = "res_DY.",
        #landsProcess = 5,
        #datasetType  = "None",
        #validMassPoints = MassPoints,
    #))
    #DataGroups.append(DataGroup(
        #label        = "res_WW.",
        #landsProcess = 6,
        #datasetType  = "None",
        #validMassPoints = MassPoints,
    #))
    #DataGroups.append(DataGroup(
        #label        = "EWK_DY",
        #landsProcess = 5,
        #shapeHisto   = SignalShapeHisto,
        #datasetType  = "Embedding",
        #datasetDefinitions   = ["DYJetsToLL"],
        #dirPrefix   = SignalAnalysis,
        #rateCounter  = SignalRateCounter,
        #validMassPoints = MassPoints,
        #nuisances    = ["01c","03","45","46","47","09","11b","15b","16b","31","33","34","24"]
    #))
    #DataGroups.append(DataGroup(
        #label        = "EWK_VV",
        #landsProcess = 6,
        #shapeHisto   = SignalShapeHisto,
        #datasetType  = "Embedding",
        #datasetDefinitions   = ["WW"], #,"WZ","ZZ"],
        #dirPrefix   = SignalAnalysis,
        #rateCounter  = SignalRateCounter,
        #validMassPoints = MassPoints,
        #nuisances    = ["01c","03","45","46","47","09","11b","15b","16b","32","33","34","27"]
    #))

    # EWK + ttbar with fake taus
    EWKFakeIdList = [1,5,6]
    DataGroups.append(DataGroup(
        label        = "EWK_tt_faketau",
        landsProcess = 1,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["TTJets_"],
        #dirPrefix   = SignalAnalysis,
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01d","02","04","45","46","47","09","10b","28","33","34b","35"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_W_faketau",
        landsProcess = 5,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["WJets","W1Jets","W2Jets","W3Jets","W4Jets"],
        #dirPrefix   = SignalAnalysis,
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01d","02","04","45","46","47","09","11b","29","33","34b","37"]
    ))
    DataGroups.append(DataGroup(
        label        = "EWK_t_faketau",
        landsProcess = 6,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions = ["T_", "Tbar_"],
        #dirPrefix   = SignalAnalysis,
        rateCounter  = FakeRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01d","02","04","45","46","47","09","10b","30","33","34b","38"]
    ))
else:
    # Mimic embedding with MC analysis (introduces double counting of EWK fakes, but that should be small effect)
    EmbeddingIdList = [4,5,6]
    DataGroups.append(DataGroup(
        label        = "MC_EWK_Tau",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        #datasetDefinitions = ["TTJets", "W2Jets","W3Jets","W4Jets", "Tbar_", "T_"],
        datasetDefinitions = ["TTJets", "WJets", "W1Jets", "W2Jets", "W3Jets", "W4Jets", "Tbar_", "T_"],
        #dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01b","03","45","46","47","14","15","16","19","40"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_EWK_DY",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["DYJetsToLL"],
        #dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01","03","45","46","47","09","11","15b","16b","31","33","34","24"]
    ))
    DataGroups.append(DataGroup(
        label        = "MC_EWK_VV",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Signal",
        datasetDefinitions   = ["WW","WZ","ZZ"],
        #dirPrefix   = SignalAnalysis,
        rateCounter  = SignalRateCounter,
        validMassPoints = MassPoints,
        nuisances    = ["01","03","45","46","47","09","11","15b","16b","32","33","34","27"]
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
    id            = "01",
    label         = "tau+MET trg tau part",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["TauTriggerScaleFactorAbsUncert_AfterSelection"],
    normalisation = ["TauTriggerScaleFactorAbsUncertCounts_AfterSelection"],
))

Nuisances.append(Nuisance(
    id            = "01b",
    label         = "tau+MET trg tau part for EWKtau (temp)",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.066
))

Nuisances.append(Nuisance(
    id            = "01c",
    label         = "tau+MET trg tau scale factor for EWK tau",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties",
                     "ScaleFactorUncertainties"],
    histograms    = ["TriggerScaleFactorAbsUncert_AfterDeltaPhi160",
                     "TriggerScaleFactorAbsUncert_AfterDeltaPhi160"],
    normalisation = ["TriggerScaleFactorAbsUncertCounts_AfterSelection",
                     "TriggerScaleFactorAbsUncertCounts_AfterSelection"],
    #addUncertaintyInQuadrature = 0.10 # MET leg uncertainty
))

Nuisances.append(Nuisance(
    id            = "01d",
    label         = "tau+MET trg tau part for EWK fake taus",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["TriggerScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["TriggerScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"],
))

Nuisances.append(Nuisance(
    id            = "02",
    label         = "tau+MET trg MET part",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.10
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
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["FakeTauAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["FakeTauAbsUncertCounts_EWKFakeTausAfterSelection"],
))

if OptionIncludeSystematics:
    Nuisances.append(Nuisance(
        id            = "45",
        label         = "TES effect on shape",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = SignalRateCounter,
        histoDir      = ["TESPlus",
                        "TESMinus"],
        histograms    = [SignalShapeHisto,
                        SignalShapeHisto]
    ))
    #Nuisances.append(Nuisance(
        #id            = "45b",
        #label         = "TES effect on shape",
        #distr         = "shapeQ",
        #function      = "Shape",
        #counter       = SignalRateCounter,
        #histoDir      = ["TESPlus",
                        #"TESMinus"],
        #histograms    = [SignalShapeHisto,
                        #SignalShapeHisto]
    #))
    Nuisances.append(Nuisance(
        id            = "46",
        label         = "JES effect on shape",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = SignalRateCounter,
        histoDir      = ["JESPlus",
                        "JESMinus"],
        histograms    = [SignalShapeHisto,
                        SignalShapeHisto]
    ))

    Nuisances.append(Nuisance(
        id            = "47",
        label         = "MET unclustered scale effect on shape",
        distr         = "shapeQ",
        function      = "Shape",
        counter       = SignalRateCounter,
        histoDir      = ["METPlus",
                        "METMinus"],
        histograms    = [SignalShapeHisto,
                        SignalShapeHisto]
    ))
else:
    Nuisances.append(Nuisance(
        id            = "45",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.03,
    ))

    Nuisances.append(Nuisance(
        id            = "46",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.03,
    ))

    Nuisances.append(Nuisance(
        id            = "47",
        label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.01,
    ))

Nuisances.append(Nuisance(
    id            = "48",
    label         = "Temporary TES for EWKtau",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.020,
))

Nuisances.append(Nuisance(
    id            = "09",
    label         = "lepton veto",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "muon veto", # main counter name after electron and muon veto
    denominator   = "tau trigger scale factor", # main counter name before electron and muon veto
    scaling       = 0.02
))

Nuisances.append(Nuisance(
    id            = "10",
    label         = "btagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_AfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "10b",
    label         = "btagging for EWK fake taus",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "11",
    label         = "mistagging",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_AfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_AfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "11b",
    label         = "mistagging EWK fake taus",
    distr         = "lnN",
    function      = "ScaleFactor",
    histoDir      = ["ScaleFactorUncertainties"],
    histograms    = ["BtagScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    normalisation = ["BtagScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"]
))

Nuisances.append(Nuisance(
    id            = "12",
    label         = "QCD stat.",
    distr         = "lnN",
    function      = "QCDFactorised",
    QCDmode       = "statistics",
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
    label         = "EWK with taus muon selection+ditau+mu trg",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.031
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
    label         = "MC signal stat., HH",
    distr         = "lnN",
    function      = "Counter",
    counter       = SignalRateCounter,
))

Nuisances.append(Nuisance(
    id            = "18",
    label         = "MC signal stat., HW",
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
    label         = "Z->tautau MC stat.",
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
    label         = "diboson MC stat.",
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

if OptionIncludeSystematics:
    Nuisances.append(Nuisance(
        id            = "34",
        label         = "pileup",
        distr         = "lnN",
        function      = "pileupUncertainty",
        histoDir      = ["", # nominal
                        "PUWeightMinus", # minus
                        "PUWeightPlus"], # up
        counter       = SignalRateCounter
    ))

    Nuisances.append(Nuisance(
        id            = "34b",
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
        id            = "34",
        label         = "FAKE pileup",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05
    ))

    Nuisances.append(Nuisance(
        id            = "34b",
        label         = "FAKE pileup",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05
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
    counter       = SignalRateCounter,
    histoDir      = [""],
    histograms    = [SignalShapeHisto],
))

Nuisances.append(Nuisance(
    id            = "40b",
    label         = "Stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "QCDFactorised",
    QCDmode       = "shapestat"
))

Nuisances.append(Nuisance(
    id            = "40c",
    label         = "Stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "Shape",
    counter       = FakeRateCounter,
    histoDir      = [""],
    histograms    = [FakeShapeHisto],
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
MergeNuisances.append(["01","01b","01c","01d"])
#MergeNuisances.append(["07","07b","07c"])
MergeNuisances.append(["10","10b"])
MergeNuisances.append(["11","11b"])
MergeNuisances.append(["15","15b"])
MergeNuisances.append(["16","16b"])
MergeNuisances.append(["34","34b"])
MergeNuisances.append(["40","40b","40c"])

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
    QCDFactNormalisation = "factorisation/AfterJetSelection",
    QCDFactHistoPath = "shape_CtrlLeg1AfterNjets",
    QCDFactHistoName = "CtrlLeg1AfterNjets",
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
    QCDFactNormalisation = "factorisation/AfterJetSelection",
    QCDFactHistoPath = "shape_CtrlLeg1AfterMET",
    QCDFactHistoName = "CtrlLeg1AfterMET",
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
    flowPlotCaption  = "#tau_{h}+#geq3j", # Leave blank if you don't want to include the item to the selection flow plot
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
    QCDFactNormalisation = "factorisation/Leg1AfterMET",
    QCDFactHistoPath = "shape_CtrlLeg1AfterNbjets",
    QCDFactHistoName = "CtrlLeg1AfterNbjets",
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
    blindedRange     = [1.5,10], # specify range min,max if blinding applies to this control plot
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
    #QCDFactNormalisation = "factorisation/Leg1AfterBTagging",
    #QCDFactHistoPath = "shape_CtrlLeg1AfterDeltaPhiTauMET",
    #QCDFactHistoName = "CtrlLeg1AfterDeltaPhiTauMET",
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
    #QCDFactNormalisation = "factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoPath = "shape_CtrlLeg1AfterMaxDeltaPhiJetMET",
    #QCDFactHistoName = "CtrlLeg1AfterMaxDeltaPhiJetMET",
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
    #QCDFactNormalisation = "factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoPath = "shape_CtrlLeg1AfterTopMass",
    #QCDFactHistoName = "CtrlLeg1AfterTopMass",
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
    #QCDFactNormalisation = "factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoPath = "shape_CtrlLeg1AfterTopMass",
    #QCDFactHistoName = "CtrlLeg1AfterTopMass",
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
    QCDFactNormalisation = "factorisation/Leg1AfterTopSelection",
    QCDFactHistoPath = "shape_MtShapesAfterFullMETLeg",
    QCDFactHistoName = "MtShapesAfterFullMETLeg",
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
    flowPlotCaption  = "#Delta#phi(#tau_{h},E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
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
    QCDFactNormalisation = "factorisation/Leg1AfterTopSelection",
    QCDFactHistoPath = "shape_FullMassShapesAfterFullMETLeg",
    QCDFactHistoName = "FullMassShapesAfterFullMETLeg",
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
    QCDFactNormalisation = "factorisation/Leg1AfterMET",
    QCDFactHistoPath = "shape_CtrlLeg1NJetsAfterMET",
    QCDFactHistoName = "CtrlLeg1NJetsAfterMET",
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

