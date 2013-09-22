import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics

DataCardName    = 'Default_7TeV'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_metModeIsolationDependent'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_metModeNeverIsolated'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_vitalonly_correctCtrlPlots'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/testInverted'
Path = "/home/wendland/data/v445/2013-09-09"
#Path            = '/home/wendland/data/v445/met50rtaunprongs'
#Path            = '/mnt/flustre/slehti/hplusAnalysis/QCDInverted/CMSSW_4_4_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/datacardGenerator/TESTDATA/'
LightMassPoints      = [80,90,100,120,140,150,155,160]
LightMassPoints      = [120]
HeavyMassPoints      = [180,190,200,220,250,300]
HeavyMassPoints      = [180]
MassPoints = LightMassPoints[:]+HeavyMassPoints[:]

BlindAnalysis   = True

# Rate counter definitions
SignalRateCounter = "Selected events"
FakeRateCounter = "EWKfaketaus:SelectedEvents"

# Options
OptionMassShape = "TransverseMass"
#OptionMassShape = "FullMass"
#OptionMassShape = "TransverseAndFullMass2D" #FIXME not yet supported!!!

OptionReplaceEmbeddingByMC = True
OptionIncludeSystematics = True # Set to true if the JES and PU uncertainties were produced
OptionPurgeReservedLines = True # Makes limit running faster, but cannot combine leptonic datacards
OptionDoControlPlots = True
OptionDisplayEventYieldSummary = True
OptionNumberOfDecimalsInSummaries = 1
OptionRemoveHHDataGroup = False
OptionLimitOnSigmaBr = False # Is automatically set to true for heavy H+

# Options for reports and article
OptionBr = 0.01  # Br(t->bH+)

# Tolerance for throwing error on luminosity difference (0.01 = 1 percent agreement is required)
ToleranceForLuminosityDifference = 0.01

# Shape histogram definitions
SignalShapeHisto = None
FakeShapeHisto = None
ShapeHistogramsDimensions = None

if OptionMassShape == "TransverseMass":
    SignalShapeHisto = "shapeTransverseMass"
    FakeShapeHisto = "shapeEWKFakeTausTransverseMass"
elif OptionMassShape == "FullMass":
    SignalShapeHisto = "shapeInvariantMass"
    FakeShapeHisto = "shapeEWKFakeTausInvariantMass"
elif OptionMassShape == "TransverseAndFullMass2D": # FIXME: preparing to add support, not yet working
    SignalShapeHisto = "shapetransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    FakeShapeHisto = "shapeEWKFakeTausTransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
ShapeHistogramsDimensions = systematics.getBinningForPlot(SignalShapeHisto)

DataCardName += "_"+OptionMassShape

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import ObservationInput
Observation = ObservationInput(datasetDefinition="Data",
                               shapeHisto=SignalShapeHisto)
#Observation.setPaths(signalPath,signalDataPaths)

##############################################################################
# Systematics lists

myShapeSystematics = ["trg_tau","trg_MET","ES_taus","ES_jets","JER","ES_METunclustered","pileup"] # btag is not added, because it has the tag and mistag categories
myFakeShapeSystematics = []
for item in myShapeSystematics:
    myFakeShapeSystematics.append("%s_fakes"%item)


##############################################################################
# DataGroup (i.e. columns in datacard) definitions
#
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import DataGroup
DataGroups = []
EmbeddingIdList = []
EWKFakeIdList = []

signalTemplate = DataGroup(datasetType="Signal",
                           shapeHisto=SignalShapeHisto)

for mass in LightMassPoints:
    myMassList = [mass]
    hhx = signalTemplate.clone()
    hhx.setLabel("HH"+str(mass)+"_a")
    hhx.setLandSProcess(-1)
    hhx.setValidMassPoints(myMassList)
    hhx.setNuisances(myShapeSystematics[:]+["tau_ID","e_mu_veto","b_tag","stat_binByBin","xsect_tt_7TeV","lumi"])
    hhx.setDatasetDefinition("TTToHplusBHminusB_M"+str(mass))
    DataGroups.append(hhx)

    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(myShapeSystematics[:]+["tau_ID","e_mu_veto","b_tag","stat_binByBin","xsect_tt_7TeV","lumi"])
    hwx.setDatasetDefinition("TTToHplusBWB_M"+str(mass))
    DataGroups.append(hwx)

for mass in HeavyMassPoints:
    myMassList = [mass]
    hx = signalTemplate.clone()
    hx.setLabel("Hp"+str(mass)+"_a")
    hx.setLandSProcess(0)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(myShapeSystematics[:]+["tau_ID","e_mu_veto","b_tag","stat_binByBin","xsect_heavyHplus_7TeV","lumi"])
    hx.setDatasetDefinition("HplusTB_M"+str(mass))
    DataGroups.append(hx)

myQCDFact = DataGroup(
    label        = "QCDfact",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD factorised",
    datasetDefinition = "QCDfactorisedmt",
    nuisances    = myShapeSystematics[:]+["QCD_metshape","stat_binByBin"],
    shapeHisto   = SignalShapeHisto,
)

myQCDInv = DataGroup(
    label        = "QCDinv",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD inverted",
    datasetDefinition = "QCDfactorisedmt",
    nuisances    = myShapeSystematics[:]+["QCD_metshape","stat_binByBin","QCDinvTemplateFit"],
    shapeHisto   = SignalShapeHisto,
)

if OptionMassShape == "TransverseMass":
    myQCDFact.setDatasetDefinition("QCDfactorisedmt")
    myQCDInv.setDatasetDefinition("QCDfactorisedmt")
elif OptionMassShape == "FullMass":
    myQCDFact.setDatasetDefinition("QCDfactorisedinvmass")
    myQCDInv.setDatasetDefinition("QCDfactorisedinvmass")

DataGroups.append(myQCDFact)
DataGroups.append(myQCDInv)

if not OptionReplaceEmbeddingByMC:
    # EWK + ttbar with genuine taus
    EmbeddingIdList = [4]
    DataGroups.append(DataGroup(
        label        = "EWK_Tau",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        #datasetDefinition   = ["SingleMu"],
        datasetDefinition   = "Data",
        validMassPoints = MassPoints,
        additionalNormalisation = 1.0907, #FIXME
        nuisances    = ["trg_tau_embedding","tau_ID","Emb_QCDcontam","Emb_WtauTomu","Emb_musel_ditau_mutrg","stat_Emb","stat_binByBin","ES_taus_tempForEmbedding"]#FIXME
        #nuisances    = ["trg_tau_embedding","tau_ID","ES_taus","Emb_QCDcontam","Emb_WtauTomu","Emb_musel_ditau_mutrg","stat_Emb","stat_binByBin"]
    ))

    # EWK + ttbar with fake taus
    EWKFakeIdList = [1,5,6]
    DataGroups.append(DataGroup(
        label        = "tt_EWK_faketau",
        landsProcess = 1,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_misID","e_mu_veto_fakes","b_tag_fakes","xsect_tt_7TeV","lumi","stat_binByBin_fakes"],
    ))
    DataGroups.append(DataGroup(
        label        = "W_EWK_faketau",
        landsProcess = 5,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "WJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_misID","e_mu_veto_fakes","b_mistag_fakes","xsect_Wjets","lumi","stat_binByBin_fakes"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_EWK_faketau",
        landsProcess = 6,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_misID","e_mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","stat_binByBin_fakes"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_EWK_faketau",
        landsProcess = 7,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "DYJetsToLL",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_misID","e_mu_veto_fakes","b_mistag_fakes","xsect_DYtoll","lumi","stat_binByBin_fakes"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_EWK_faketau",
        landsProcess = 8,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_misID","e_mu_veto_fakes","b_mistag_fakes","xsect_VV","lumi","stat_binByBin_fakes"],
    ))
else:
    # Mimic embedding with MC analysis (introduces double counting of EWK fakes, but that should be small effect)
    EmbeddingIdList = [1,4,5,6,7]
    DataGroups.append(DataGroup(
        label        = "ttbar_MC",
        landsProcess = 1,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_ID","e_mu_veto","b_tag","xsect_tt_7TeV","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "Wjets_MC",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "WJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_ID","e_mu_veto","b_mistag","xsect_Wjets","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_MC",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_ID","e_mu_veto","b_tag","xsect_singleTop","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_MC",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition   = "DYJetsToLL",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_ID","e_mu_veto","b_mistag","xsect_DYtoll","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_MC",
        landsProcess = 7,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition   = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["tau_ID","e_mu_veto","b_mistag","xsect_VV","lumi","stat_binByBin"],
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

#Nuisances.append(Nuisance(
    #id            = "trg_tau",
    #label         = "tau+MET trg tau part",
    #distr         = "lnN",
    #function      = "ScaleFactor",
    #histoDir      = ["ScaleFactorUncertainties"],
    #histograms    = ["TauTriggerScaleFactorAbsUncert_AfterSelection"],
    #normalisation = ["TauTriggerScaleFactorAbsUncertCounts_AfterSelection"],
#))

Nuisances.append(Nuisance(
    id            = "trg_tau",
    label         = "tau+MET trg tau part",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "TauTrgSF",
))

Nuisances.append(Nuisance(
    id            = "trg_tau_embedding",
    label         = "tau+MET trg tau part for EWKtau (temp)",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.066 #FIXME
))

Nuisances.append(Nuisance(
    id            = "trg_tau_fakes",
    label         = "tau+MET trg tau part for EWK fake taus",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "TauTrgSF",
))

#Nuisances.append(Nuisance(
    #id            = "trg_tau_fakes",
    #label         = "tau+MET trg tau part for EWK fake taus",
    #distr         = "lnN",
    #function      = "ScaleFactor",
    #histoDir      = ["ScaleFactorUncertainties"],
    #histograms    = ["TriggerScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    #normalisation = ["TriggerScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"],
#))

#Nuisances.append(Nuisance(
    #id            = "trg_MET",
    #label         = "tau+MET trg MET part",
    #distr         = "shapeQ",
    #function      = "ShapeVariation",
    #systVariation = "METTrgSF",
#))

#Nuisances.append(Nuisance(
    #id            = "trg_MET_fakes",
    #label         = "tau+MET trg MET part",
    #distr         = "shapeQ",
    #function      = "ShapeVariation",
    #systVariation = "METTrgSF"
#))

Nuisances.append(Nuisance(
    id            = "trg_MET",
    label         = "tau+MET trg MET part",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.10
))

Nuisances.append(Nuisance(
    id            = "trg_MET_fakes",
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
    value         = systematics.getTauIDUncertainty(isGenuineTau=True)
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
        function      = "ShapeVariation",
        systVariation = "TES",
    ))
    Nuisances.append(Nuisance(
        id            = "ES_taus_fakes",
        label         = "TES bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "TES",
    ))
    Nuisances.append(Nuisance(
        id            = "ES_jets",
        label         = "JES bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "JES",
    ))
    Nuisances.append(Nuisance(
        id            = "ES_jets_fakes",
        label         = "JES bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "JES",
    ))
    Nuisances.append(Nuisance(
        id            = "JER",
        label         = "Jet energy resolution",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "JER",
    ))
    Nuisances.append(Nuisance(
        id            = "JER_fakes",
        label         = "Jet energy resolution",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "JES",
    ))
    Nuisances.append(Nuisance(
        id            = "ES_METunclustered",
        label         = "MET unclustered scale bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "MET",
    ))
    Nuisances.append(Nuisance(
        id            = "ES_METunclustered_fakes",
        label         = "MET unclustered scale bin-by-bin uncertainty",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "MET",
    ))
    Nuisances.append(Nuisance(
        id            = "b_tag",
        label         = "btagging",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "BTagSF",
    ))
    Nuisances.append(Nuisance(
        id            = "b_tag_fakes",
        label         = "btagging for EWK fake taus",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "BTagSF",
    ))
    Nuisances.append(Nuisance(
        id            = "b_mistag",
        label         = "mistagging",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "BTagSF",
    ))
    Nuisances.append(Nuisance(
        id            = "b_mistag_fakes",
        label         = "mistagging EWK fake taus",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "BTagSF",
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
        id            = "JER",
        label         = "NON-EXACT VALUE for Jet energy resolution",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.02,
    ))
    Nuisances.append(Nuisance(
        id            = "JER_fakes",
        label         = "NON-EXACT VALUE for Jet energy resolution",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.02,
    ))
    Nuisances.append(Nuisance(
        id            = "b_tag",
        label         = "NON-EXACT VALUE for btagging",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05,
    ))
    Nuisances.append(Nuisance(
        id            = "b_tag_fakes",
        label         = "NON-EXACT VALUE for btagging for EWK fake taus",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05,
    ))
    Nuisances.append(Nuisance(
        id            = "b_mistag",
        label         = "NON-EXACT VALUE for mistagging",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05,
    ))
    Nuisances.append(Nuisance(
        id            = "b_mistag_fakes",
        label         = "NON-EXACT VALUE for mistagging EWK fake taus",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05,
    ))

Nuisances.append(Nuisance(
    id            = "ES_taus_tempForEmbedding",
    label         = "Temporary TES for EWKtau",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.020, #FIXME
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

#Nuisances.append(Nuisance(
    #id            = "b_tag",
    #label         = "btagging",
    #distr         = "lnN",
    #function      = "ScaleFactor",
    #histoDir      = ["ScaleFactorUncertainties"],
    #histograms    = ["BtagScaleFactorAbsUncert_AfterSelection"],
    #normalisation = ["BtagScaleFactorAbsUncertCounts_AfterSelection"]
#))

#Nuisances.append(Nuisance(
    #id            = "b_tag_fakes",
    #label         = "btagging for EWK fake taus",
    #distr         = "lnN",
    #function      = "ScaleFactor",
    #histoDir      = ["ScaleFactorUncertainties"],
    #histograms    = ["BtagScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    #normalisation = ["BtagScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"]
#))

#Nuisances.append(Nuisance(
    #id            = "b_mistag",
    #label         = "mistagging",
    #distr         = "lnN",
    #function      = "ScaleFactor",
    #histoDir      = ["ScaleFactorUncertainties"],
    #histograms    = ["BtagScaleFactorAbsUncert_AfterSelection"],
    #normalisation = ["BtagScaleFactorAbsUncertCounts_AfterSelection"]
#))

#Nuisances.append(Nuisance(
    #id            = "b_mistag_fakes",
    #label         = "mistagging EWK fake taus",
    #distr         = "lnN",
    #function      = "ScaleFactor",
    #histoDir      = ["ScaleFactorUncertainties"],
    #histograms    = ["BtagScaleFactorAbsUncert_EWKFakeTausAfterSelection"],
    #normalisation = ["BtagScaleFactorAbsUncertCounts_EWKFakeTausAfterSelection"]
#))

Nuisances.append(Nuisance(
    id            = "QCD_metshape",
    label         = "QCD met shape syst.",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "QCDNorm",
))

Nuisances.append(Nuisance(
    id            = "Emb_QCDcontam",
    label         = "EWK with taus QCD contamination",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.012 #FIXME
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
    value         = 0.031 #FIXME
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
    function      = "Counter",
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
    function      = "Counter",
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
    function      = "Counter",
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
    id            = "xsect_heavyHplus_7TeV",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("HplusTB").getUncertaintyDown(),
    upperValue    = systematics.getCrossSectionUncertainty("HplusTB").getUncertaintyUp(),
))

Nuisances.append(Nuisance(
    id            = "xsect_tt_7TeV",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyDown(),
    upperValue    = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyUp(),
))

Nuisances.append(Nuisance(
    id            = "xsect_Wjets",
    label         = "W+jets cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("WJets").getUncertaintyDown()
))

Nuisances.append(Nuisance(
    id            = "xsect_singleTop",
    label         = "single top cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("SingleTop").getUncertaintyDown()
))

Nuisances.append(Nuisance(
    id            = "xsect_DYtoll",
    label         = "Z->ll cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("DYJetsToLL").getUncertaintyDown()
))

Nuisances.append(Nuisance(
    id            = "xsect_VV",
    label         = "diboson cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("Diboson").getUncertaintyDown()
))

Nuisances.append(Nuisance(
    id            = "lumi",
    label         = "luminosity",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getLuminosityUncertainty()
))

if OptionIncludeSystematics:
    Nuisances.append(Nuisance(
        id            = "pileup",
        label         = "pileup",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "PUWeight",
    ))

    Nuisances.append(Nuisance(
        id            = "pileup_fakes",
        label         = "pileup",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "PUWeight",
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
    histograms    = SignalShapeHisto,
))

Nuisances.append(Nuisance(
    id            = "stat_binByBin_fakes",
    label         = "Bin-by-bin stat. uncertainty on the shape",
    distr         = "shapeStat",
    function      = "Shape",
    histograms    = FakeShapeHisto,
))

Nuisances.append(Nuisance(
    id            = "QCDinvTemplateFit",
    label         = "QCDInv: fit", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.0043
))

MergeNuisances = []
MergeNuisances.append(["trg_tau","trg_tau_embedding","trg_tau_fakes"])
MergeNuisances.append(["ES_taus","ES_taus_fakes","ES_taus_tempForEmbedding"])
MergeNuisances.append(["ES_jets","ES_jets_fakes"])
MergeNuisances.append(["JER","JER_fakes"])
MergeNuisances.append(["ES_METunclustered","ES_METunclustered_fakes"])
MergeNuisances.append(["e_mu_veto","e_mu_veto_fakes"])
MergeNuisances.append(["b_tag","b_tag_fakes"])
MergeNuisances.append(["b_mistag","b_mistag_fakes"])
MergeNuisances.append(["pileup","pileup_fakes"])
#MergeNuisances.append(["stat_binByBin","stat_binByBin_QCDfact","stat_binByBin_fakes"])

# Control plots
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import ControlPlotInput
ControlPlots = []


# FIXME: fix how QCD background is taken here
ControlPlots.append(ControlPlotInput(
    title            = "Njets",
    signalHHid       = [-1],
    signalHWid       = [0],
    QCDid            = [3],
    embeddingId      = EmbeddingIdList,
    EWKfakeId        = EWKFakeIdList,
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "NjetsAfterJetSelectionAndMETSF",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "NjetsAfterJetSelectionAndMETSF",
    QCDFactNormalisation = "/CtrlNjets",
    QCDFactHistoName = "/CtrlNjets",
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
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "ImprovedDeltaPhiCutsJet%dCollinear"%(i+1),
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "ImprovedDeltaPhiCutsJet%dCollinear"%(i+1),
        QCDFactNormalisation = "/QCDTailKillerJet%dCollinear"%i,
        QCDFactHistoName = "/QCDTailKillerJet%dCollinear"%i,
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
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "MET",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "MET",
    QCDFactNormalisation = "/CtrlMET",
    QCDFactHistoName = "/CtrlMET",
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
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "NBjets",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "NBjets",
    QCDFactNormalisation = "/CtrlNbjets",
    QCDFactHistoName = "/CtrlNbjets",
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
    #QCDFactNormalisation = "/factorisation/Leg1AfterBTagging",
    #QCDFactHistoName = "/CtrlLeg1AfterDeltaPhiTauMET", #FIXME
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
    #QCDFactNormalisation = "/factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoName = "/CtrlLeg1AfterMaxDeltaPhiJetMET", #FIXME
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
    #QCDFactNormalisation = "/factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoName = "/CtrlLeg1AfterTopMass", #FIXME
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
    #QCDFactNormalisation = "/factorisation/Leg1AfterDeltaPhiTauMET",
    #QCDFactHistoName = "/CtrlLeg1AfterTopMass", #FIXME
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
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "ImprovedDeltaPhiCutsJet%dBackToBack"%(i+1),
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "ImprovedDeltaPhiCutsJet%dBackToBack"%(i+1),
        QCDFactNormalisation = "/QCDTailKillerJet%dBackToBack"%i,
        QCDFactHistoName = "/QCDTailKillerJet%dBackToBack"%i,
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
    signalHistoName  = "shapeTransverseMass",
    EWKfakeHistoPath  = "",
    EWKfakeHistoName  = "shapeEWKFakeTausTransverseMass",
    QCDFactNormalisation = "/NevtAfterLeg1",
    QCDFactHistoName = "/MtAfterLeg1",
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

if False:
    ControlPlots.append(ControlPlotInput(
        title            = "FullMass",
        signalHHid       = [-1],
        signalHWid       = [0],
        QCDid            = [3],
        embeddingId      = EmbeddingIdList,
        EWKfakeId        = EWKFakeIdList,
        signalHistoPath  = "",
        signalHistoName  = "shapeInvariantMass",
        EWKfakeHistoPath  = "",
        EWKfakeHistoName  = "shapeEWKFakeTausInvariantMass",
        QCDFactNormalisation = "/NevtAfterLeg1",
        QCDFactHistoName = "/MassAfterLeg1",
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
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "NjetsAfterMET",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
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

