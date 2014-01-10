import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics

DataCardName    = 'Default_7TeV'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_metModeIsolationDependent'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_metModeNeverIsolated'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/met50_vitalonly_correctCtrlPlots'
#Path            = '/home/wendland/data/v445/met50_2013-05-13/testInverted'
Path = "/home/wendland/data/v445/2013-12-03"
#Path            = '/home/wendland/data/v445/met50rtaunprongs'
#Path            = '/mnt/flustre/slehti/hplusAnalysis/QCDInverted/CMSSW_4_4_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/datacardGenerator/TESTDATA/'
LightMassPoints      = [80,90,100,120,140,150,155,160]
LightMassPoints      = [80,120,160]
LightMassPoints      = [120]
#LightMassPoints      = []
HeavyMassPoints      = [180,190,200,220,250,300] # points 400, 500, 600 are not available in 2011 branch
HeavyMassPoints      = [180,220,300]
HeavyMassPoints      = []
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
OptionRealisticEmbeddingWithMC = True # Only relevant for OptionReplaceEmbeddingByMC==True
OptionTreatTriggerUncertaintiesAsAsymmetric = False # Set to true, if you produced multicrabs with doAsymmetricTriggerUncertainties=True
OptionTreatTauIDAndMisIDSystematicsAsShapes = False # Set to true, if you produced multicrabs with doTauIDandMisIDSystematicsAsShapes=True
OptionIncludeSystematics = True # Set to true if you produced multicrabs with doSystematics=True

OptionPurgeReservedLines = True # Makes limit running faster, but cannot combine leptonic datacards
OptionDoControlPlots = True
OptionDisplayEventYieldSummary = True
OptionNumberOfDecimalsInSummaries = 1
OptionRemoveHHDataGroup = False
OptionLimitOnSigmaBr = False # Is automatically set to true for heavy H+
#OptionDoTBbarForHeavy = False # NOTE: not usable in 2011

# For projections
trg_MET_dataeffScaleFactor = None # Default is None, i.e. 1.0

# Options for reports and article
OptionBr = 0.01  # Br(t->bH+)
OptionSqrtS = 7 # sqrt(s)

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
myTrgShapeSystematics = []
if OptionTreatTriggerUncertaintiesAsAsymmetric:
    myTrgShapeSystematics = ["trg_tau_dataeff","trg_tau_MCeff","trg_MET_dataeff","trg_MET_MCeff"] # Variation done separately for data and MC efficiencies
else:
    myTrgShapeSystematics = ["trg_tau","trg_MET"] # Variation of trg scale factors

    myTauIDShapeSystematics = []
if OptionTreatTauIDAndMisIDSystematicsAsShapes:
    myTauIDShapeSystematics = ["tau_ID_shape","tau_ID_eToTauBarrel_shape","tau_ID_eToTauEndcap_shape","tau_ID_muToTau_shape","tau_ID_jetToTau_shape"] # tau ID and mis-ID systematics done with shape variation
else:
    myTauIDShapeSystematics = ["tau_ID"] # tau ID and mis-ID systematics done with constants


myShapeSystematics = []
myShapeSystematics.extend(myTrgShapeSystematics)
myShapeSystematics.extend(myTauIDShapeSystematics)
myShapeSystematics.extend(["ES_taus","ES_jets","JER","ES_METunclustered","pileup"]) # btag is not added, because it has the tag and mistag categories

myEmbeddingShapeSystematics = ["trg_tau_dataeff","trg_MET_dataeff","trg_muon_dataeff","ES_taus","Emb_mu_ID","Emb_WtauTomu"]
# Add tau ID uncert. to embedding either as a shape or as a constant
if "tau_ID_shape" in myTauIDShapeSystematics:
    myEmbeddingShapeSystematics.append("tau_ID_constShape")
else:
    myEmbeddingShapeSystematics.append("tau_ID")

myFakeShapeSystematics = []
for item in myShapeSystematics:
    if item == "tau_ID":
        myFakeShapeSystematics.append("tau_misID")
    else:
        myFakeShapeSystematics.append(item)

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
    hhx.setNuisances(myShapeSystematics[:]+["e_mu_veto","b_tag","stat_binByBin","xsect_tt_7TeV","lumi"])
    hhx.setDatasetDefinition("TTToHplusBHminusB_M"+str(mass))
    DataGroups.append(hhx)

    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(myShapeSystematics[:]+["e_mu_veto","b_tag","stat_binByBin","xsect_tt_7TeV","lumi"])
    hwx.setDatasetDefinition("TTToHplusBWB_M"+str(mass))
    DataGroups.append(hwx)

for mass in HeavyMassPoints:
    myMassList = [mass]
    hx = signalTemplate.clone()
    hx.setLabel("Hp"+str(mass)+"_a")
    hx.setLandSProcess(0)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(myShapeSystematics[:]+["e_mu_veto","b_tag","stat_binByBin","lumi"])
    hx.setDatasetDefinition("HplusTB_M"+str(mass))
    DataGroups.append(hx)

myQCDFact = DataGroup(
    label        = "QCDfact",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD factorised",
    datasetDefinition = "QCDfactorisedmt",
    nuisances    = myShapeSystematics[:]+["b_tag","top_pt","QCD_metshape","stat_binByBin"],
    shapeHisto   = SignalShapeHisto,
)

myQCDInv = DataGroup(
    label        = "QCDinv",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD inverted",
    datasetDefinition = "QCDinvertedmt",
    nuisances    = myShapeSystematics[:]+["b_tag","top_pt","QCD_metshape","stat_binByBin","QCDinvTemplateFit"],
    shapeHisto   = SignalShapeHisto,
)

if OptionMassShape == "TransverseMass":
    myQCDFact.setDatasetDefinition("QCDfactorisedmt")
    myQCDInv.setDatasetDefinition("QCDinvertedmt")
elif OptionMassShape == "FullMass":
    myQCDFact.setDatasetDefinition("QCDfactorisedinvmass")
    myQCDInv.setDatasetDefinition("QCDinvertedinvmass")

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
        #additionalNormalisation = 0.25, # not needed anymore
        nuisances    = myEmbeddingShapeSystematics[:]+["Emb_QCDcontam","stat_binByBin"]
        #nuisances    = ["trg_tau_embedding","tau_ID","ES_taus","Emb_QCDcontam","Emb_WtauTomu","Emb_musel_ditau_mutrg","stat_Emb","stat_binByBin"]
    ))

    # EWK + ttbar with fake taus
    EWKFakeIdList = [1,5,6,7,8]
    DataGroups.append(DataGroup(
        label        = "tt_EWK_faketau",
        landsProcess = 1,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","top_pt","xsect_tt_7TeV","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "W_EWK_faketau",
        landsProcess = 5,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "WJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_mistag_fakes","xsect_Wjets","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_EWK_faketau",
        landsProcess = 6,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_EWK_faketau",
        landsProcess = 7,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "DYJetsToLL",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_mistag_fakes","xsect_DYtoll","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_EWK_faketau",
        landsProcess = 8,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_mistag_fakes","xsect_VV","lumi","stat_binByBin"],
    ))
elif OptionRealisticEmbeddingWithMC:
    # Mimic embedding with MC analysis (introduces double counting of EWK fakes, but that should be small effect)
    EmbeddingIdList = [4]
    myEmbeddingShapeSystematics = []
    if OptionTreatTriggerUncertaintiesAsAsymmetric:
        myEmbeddingShapeSystematics = ["trg_tau_dataeff","trg_MET_dataeff","ES_taus"]
    else:
        myEmbeddingShapeSystematics = ["trg_tau","trg_MET","ES_taus"]
    myEmbeddingShapeSystematics.append("ES_taus")
    if OptionTreatTauIDAndMisIDSystematicsAsShapes:
        myEmbeddingShapeSystematics.append("tau_ID_shape")
    else:
        myEmbeddingShapeSystematics.append("tau_ID")
    myEmbeddingShapeSystematics.extend(["Emb_QCDcontam","Emb_rest","stat_binByBin"])
    DataGroups.append(DataGroup(
        label        = "pseudo_emb_TTJets_MC",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myEmbeddingShapeSystematics,
    ))
    DataGroups.append(DataGroup(
        label        = "pseudo_emb_Wjets_MC",
        landsProcess = None,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "WJets",
        validMassPoints = MassPoints,
        nuisances    = myEmbeddingShapeSystematics,
    ))
    DataGroups.append(DataGroup(
        label        = "pseudo_emb_t_MC",
        landsProcess = None,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myEmbeddingShapeSystematics,
    ))
    DataGroups.append(DataGroup(
        label        = "pseudo_emb_DY_MC",
        landsProcess = None,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition   = "DYJetsToLL",
        validMassPoints = MassPoints,
        nuisances    = myEmbeddingShapeSystematics,
    ))
    DataGroups.append(DataGroup(
        label        = "pseudo_emb_VV_MC",
        landsProcess = None,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition   = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myEmbeddingShapeSystematics,
    ))
    EWKFakeIdList = [1,5,6,7,8]
    DataGroups.append(DataGroup(
        label        = "tt_EWK_faketau",
        landsProcess = 1,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","top_pt","xsect_tt_7TeV","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "W_EWK_faketau",
        landsProcess = 5,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "WJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_mistag_fakes","xsect_Wjets","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_EWK_faketau",
        landsProcess = 6,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_EWK_faketau",
        landsProcess = 7,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "DYJetsToLL",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_mistag_fakes","xsect_DYtoll","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_EWK_faketau",
        landsProcess = 8,
        shapeHisto   = FakeShapeHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_mistag_fakes","xsect_VV","lumi","stat_binByBin"],
    ))
else:
    # Replace embedding and fakes with MC
    EmbeddingIdList = [1,4,5,6,7]
    DataGroups.append(DataGroup(
        label        = "ttbar_MC",
        landsProcess = 1,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_tag","top_pt","xsect_tt_7TeV","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "Wjets_MC",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "WJets",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_mistag","xsect_Wjets","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_MC",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_singleTop","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_MC",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "DYJetsToLL",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_mistag","xsect_DYtoll","lumi","stat_binByBin"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_MC",
        landsProcess = 7,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_mistag","xsect_VV","lumi","stat_binByBin"],
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

if "trg_tau" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "trg_tau",
        label         = "tau+MET trg tau part",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "TauTrgSF",
    ))
else:
    Nuisances.append(Nuisance(
        id            = "trg_tau_dataeff",
        label         = "tau+MET trg tau part data eff.",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "TauTrgDataEff",
    ))

    Nuisances.append(Nuisance(
        id            = "trg_tau_MCeff",
        label         = "tau+MET trg tau part MC eff.",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "TauTrgMCEff",
    ))

if "trg_MET" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "trg_MET",
        label         = "tau+MET trg MET part",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "METTrgSF",
    ))
else:
    Nuisances.append(Nuisance(
        id            = "trg_MET_dataeff",
        label         = "tau+MET trg MET part data eff.",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "MetTrgDataEff",
        scaleFactor   = trg_MET_dataeffScaleFactor,
    ))

    Nuisances.append(Nuisance(
        id            = "trg_MET_MCeff",
        label         = "tau+MET trg MET part MC eff.",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "MetTrgMCEff",
    ))

if not OptionReplaceEmbeddingByMC:
    Nuisances.append(Nuisance(
        id            = "trg_muon_dataeff",
        label         = "SingleMu trg data eff.",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "MuonTrgDataEff",
    ))

if not "tau_ID_shape" in myShapeSystematics:
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
        function      = "Constant",
        value         = 0.15, # FIXME
    ))

Nuisances.append(Nuisance(
    id            = "tau_ID_constShape",
    label         = "tau-jet ID (no Rtau)",
    distr         = "shapeQ",
    function      = "ConstantToShape",
    value         = systematics.getTauIDUncertainty(isGenuineTau=True)
))

if "tau_ID_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_shape",
        label         = "tau-jet ID (no Rtau) genuine taus",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "GenuineTau",
    ))

if "tau_ID_eToTauBarrel_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_eToTauBarrel_shape",
        label         = "tau-jet ID (no Rtau) e->tau (barrel)",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "FakeTauBarrelElectron",
    ))

if "tau_ID_eToTauEndcap_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_eToTauEndcap_shape",
        label         = "tau-jet ID (no Rtau) e->tau (endcap)",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "FakeTauEndcapElectron",
    ))

if "tau_ID_muToTau_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_muToTau_shape",
        label         = "tau-jet ID (no Rtau) mu->tau",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "FakeTauMuon",
    ))

if "tau_ID_jetToTau_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_jetToTau_shape",
        label         = "tau-jet ID (no Rtau) jet->tau",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "FakeTauJet",
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
        id            = "ES_jets",
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
        id            = "ES_METunclustered",
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
    Nuisances.append(Nuisance(
        id            = "top_pt",
        label         = "top pT reweighting",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "TopPtWeight",
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
        id            = "ES_jets",
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
        id            = "JER",
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
        id            = "top_pt",
        label         = "NON-EXACT VALUE for top pT reweighting",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.15,
    ))

if not OptionReplaceEmbeddingByMC:
    Nuisances.append(Nuisance(
        id            = "Emb_mu_ID",
        label         = "Muon ID for embedding",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "MuonIdDataEff",
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
    denominator   = "EWKfaketaus:taus == 1", # main counter name before electron and muon veto # the name is misleading, it is actually after tau trg scale factor
    scaling       = 0.02
))

Nuisances.append(Nuisance(
    id            = "QCD_metshape",
    label         = "QCD met shape syst.",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "QCDNorm",
))

if not OptionReplaceEmbeddingByMC or OptionRealisticEmbeddingWithMC:
    Nuisances.append(Nuisance(
        id            = "Emb_QCDcontam",
        label         = "EWK with taus QCD contamination",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.012 #FIXME
    ))

if not OptionReplaceEmbeddingByMC:
    if "Emb_WtauTomu" in myEmbeddingShapeSystematics:
        Nuisances.append(Nuisance(
            id            = "Emb_WtauTomu",
            label         = "EWK with taus W->tau->mu",
            distr         = "shapeQ",
            function      = "ShapeVariation",
            systVariation = "WTauMu",
        ))
    else:
        Nuisances.append(Nuisance(
            id            = "Emb_WtauTomu",
            label         = "EWK with taus W->tau->mu",
            distr         = "lnN",
            function      = "Constant",
            value         = 0.007
        ))

if OptionRealisticEmbeddingWithMC and OptionReplaceEmbeddingByMC:
    Nuisances.append(Nuisance(
        id            = "Emb_rest",
        label         = "EWK with taus W->tau->mu",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.03
    ))

#Nuisances.append(Nuisance(
    #id            = "Emb_musel_ditau_mutrg",
    #label         = "EWK with taus muon selection+ditau+mu trg",
    #distr         = "lnN",
    #function      = "Constant",
    #value         = 0.031 #FIXME
#))

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

#Nuisances.append(Nuisance(
    #id            = "stat_binByBin_fakes",
    #label         = "Bin-by-bin stat. uncertainty on the shape",
    #distr         = "shapeStat",
    #function      = "Shape",
    #histograms    = FakeShapeHisto,
#))

Nuisances.append(Nuisance(
    id            = "QCDinvTemplateFit",
    label         = "QCDInv: fit", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.0043
))

MergeNuisances = []
if not OptionReplaceEmbeddingByMC and "tau_ID_shape" in myTauIDShapeSystematics:
    MergeNuisances.append(["tau_ID_shape", "tau_ID_constShape"])
#MergeNuisances.append(["ES_taus","ES_taus_fakes","ES_taus_tempForEmbedding"])
#MergeNuisances.append(["ES_jets","ES_jets_fakes"])
#MergeNuisances.append(["JER","JER_fakes"])
#MergeNuisances.append(["ES_METunclustered","ES_METunclustered_fakes"])
MergeNuisances.append(["e_mu_veto","e_mu_veto_fakes"])
MergeNuisances.append(["b_tag","b_tag_fakes"])
MergeNuisances.append(["b_mistag","b_mistag_fakes"])
MergeNuisances.append(["pileup","pileup_fakes"])
#MergeNuisances.append(["stat_binByBin","stat_binByBin_QCDfact","stat_binByBin_fakes"])

# Control plots
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.InputClasses import ControlPlotInput
ControlPlots = []

if False: # there's a bug in data for this plot (the underflow was not empty, under investigation)
    ControlPlots.append(ControlPlotInput(
        title            = "Njets",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "Njets",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "Njets",
        details          = { "xlabel": "Number of selected jets",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "optsLog": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
ControlPlots.append(ControlPlotInput(
    title            = "NjetsAfterMETSF",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "NjetsAfterJetSelectionAndMETSF",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "NjetsAfterJetSelectionAndMETSF",
    details          = { "xlabel": "Number of selected jets",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "optsLog": {"ymin": 0.9} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "#tau_{h}+#geq3j", # Leave blank if you don't want to include the item to the selection flow plot
))

for i in range(0,3):
    ControlPlots.append(ControlPlotInput(
        title            = "CollinearTailKillerJet%d"%(i+1),
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "ImprovedDeltaPhiCutsJet%dCollinear"%(i+1),
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "ImprovedDeltaPhiCutsJet%dCollinear"%(i+1),
        details          = { "xlabel": "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{%d},MET))^{2}}"%(i+1),
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "^{o}",
                             "log": True,
                             "optsLog": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    if i == 2:
        ControlPlots[len(ControlPlots)-1].flowPlotCaption = "#Delta#phi_{#uparrow#uparrow}"


ControlPlots.append(ControlPlotInput(
    title            = "MET",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "MET",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "MET",
    details          = { "xlabel": "E_{T}^{miss}",
                         "ylabel": "Events/#DeltaE_{T}^{miss}",
                         "divideByBinWidth": True,
                         "unit": "GeV",
                         "log": True,
                         "optsLog": {"ymin": 0.0008} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "E_{T}^{miss}", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "BJetSelection",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "NBjets",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "NBjets",
    details          = { "xlabel": "Number of selected b jets",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "optsLog": {"ymin": 0.09} },
    blindedRange=[1.5,10],
    #blindedRange     = [1.5,10], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "#geq1 b tag", # Leave blank if you don't want to include the item to the selection flow plot
))

#TODO: add as preselection for all ctrl plots in signal analysis MET30 and/or collinear tail killer and/or full tail killer
#TODO: Add to signal analysis ctrl plots tail killer plots

#ControlPlots.append(ControlPlotInput(
    #title            = "DeltaPhi",
    #signalHistoPath  = "",
    #signalHistoName  = "deltaPhi",
    #EWKfakeHistoPath  = "",
    #EWKfakeHistoName  = "EWKFakeTausDeltaPhi",
    #details          = { "bins": 11,
                         #"rangeMin": 0.0,
                         #"rangeMax": 180.0,
                         #"variableBinSizeLowEdges": [0., 10., 20., 30., 40., 60., 80., 100., 120., 140., 160.], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xlabel": "#Delta#phi(#tau_{h},E_{T}^{miss})",
                         #"ylabel": "Events",
                         #"unit": "^{o}",
                         #"log": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "N_{b jets}", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "MaxDeltaPhi",
    #signalHistoPath  = "",
    #signalHistoName  = "maxDeltaPhiJetMet",
    #details          = { "bins": 18,
                         #"rangeMin": 0.0,
                         #"rangeMax": 180.0,
                         #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xlabel": "max(#Delta#phi(jet,E_{T}^{miss})",
                         #"ylabel": "Events",
                         #"unit": "^{o}",
                         #"log": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "#Delta#phi(#tau_{h},E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "WMass",
    #signalHistoPath  = "TopChiSelection",
    #signalHistoName  = "WMass",
    #details          = { "bins": 20,
                         #"rangeMin": 0.0,
                         #"rangeMax": 200.0,
                         #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xlabel": "m_{jj}",
                         #"ylabel": "Events",
                         #"unit": "GeV/c^{2}",
                         #"log": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 400], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "TopMass",
    #signalHistoPath  = "TopChiSelection",
    #signalHistoName  = "TopMass",
    #details          = { "bins": 20,
                         #"rangeMin": 0.0,
                         #"rangeMax": 400.0,
                         #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                         #"binLabels": [], # leave empty to disable bin labels
                         #"xlabel": "m_{bjj}",
                         #"ylabel": "Events",
                         #"unit": "GeV/c^{2}",
                         #"log": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 400], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

for i in range(0,3):
    ControlPlots.append(ControlPlotInput(
        title            = "BackToBackTailKillerJet%d"%(i+1),
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "ImprovedDeltaPhiCutsJet%dBackToBack"%(i+1),
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "ImprovedDeltaPhiCutsJet%dBackToBack"%(i+1),
        details          = { "xlabel": "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{%d},MET)^{2}}"%(i+1),
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "^{o}",
                             "log": True,
                             "optsLog": {"ymin": 0.9} },
        blindedRange     = [0,300], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    if i == 2:
        ControlPlots[len(ControlPlots)-1].flowPlotCaption = "#Delta#phi_{#uparrow#downarrow}"

if OptionMassShape == "TransverseMass":
    ControlPlots.append(ControlPlotInput(
        title            = "TransverseMass",
        signalHistoPath  = "",
        signalHistoName  = "shapeTransverseMass",
        EWKfakeHistoPath  = "",
        EWKfakeHistoName  = "shapeEWKFakeTausTransverseMass",
        details          = { "xlabel": "m_{T}(#tau_{h},E_{T}^{miss})",
                         "ylabel": "Events/#Deltam_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV",
                         "log": False,
                         "opts": {"ymin": 0.0},
                         "opts2": {"ymin": 0.0, "ymax":2.0},
                         "optsLog": {"ymin": 1e-5} },
        blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [60, 180], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "final", # Leave blank if you don't want to include the item to the selection flow plot
    ))
elif OptionMassShape == "FullMass":
    ControlPlots.append(ControlPlotInput(
        title            = "FullMass",
        signalHistoPath  = "",
        signalHistoName  = "shapeInvariantMass",
        EWKfakeHistoPath  = "",
        EWKfakeHistoName  = "shapeEWKFakeTausInvariantMass",
        details          = { "xlabel": "m(#tau_{h},E_{T}^{miss})",
                             "ylabel": "Events/#Deltam",
                             "divideByBinWidth": True,
                             "unit": "GeV",
                             "log": False,
                             "opts": {"ymin": 0.0},
                             "optsLog": {"ymin": 1e-5} },
        blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [80, 180], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "final", # Leave blank if you don't want to include the item to the selection flow plot
    ))

