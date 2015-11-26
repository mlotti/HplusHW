import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics

DataCardName    = 'Default_13TeV'
Path            = 'test'
#Path            = 'test_1pr'
#Path            = 'test_3pr'
#Path            = 'test_123pr_puppimet'
#Path            = 'testmet140_puppi_vtx'
#Path            = 'testbtagtight'
#Path            = 'testnorm'

LightMassPoints      = [80,90,100,120,140,150,155,160]
#LightMassPoints      = [80,120,160]
#LightMassPoints      = [140]
LightMassPoints      = []

#HeavyMassPoints      = [180,190,200,220,250,300,400,500,600]
#HeavyMassPoints      = [180,220,300,600]
HeavyMassPoints      = [300]
#HeavyMassPoints      = []

MassPoints = LightMassPoints[:]+HeavyMassPoints[:]

BlindAnalysis   = True
OptionBlindThreshold = None # If signal exceeds this fraction of expected events, data is blinded; set to None to disable

# Uncomment following line to inject signal with certain mass and normalization into the observation
#OptionSignalInjection = {"sample": "TTToHplusBWB_M120", "normalization": 0.0035} # the normalization is relative to the normalization in the multicrab
#OptionSignalInjection = {"sample": "TTToHplusBWB_M160", "normalization": 0.0022} # the normalization is relative to the normalization in the multicrab
#OptionSignalInjection = {"sample": "HplusTB_M250", "normalization": 0.28} # the normalization is relative to the normalization in the multicrabs
#OptionSignalInjection = {"sample": "HplusTB_M500", "normalization": 0.035} # the normalization is relative to the normalization in the multicrabs

# Rate counter definitions
SignalRateCounter = "Selected events"
FakeRateCounter = "EWKfaketaus:SelectedEvents"

# Options
OptionMassShape = "TransverseMass"
#OptionMassShape = "FullMass"
#OptionMassShape = "TransverseAndFullMass2D" #FIXME not yet supported!!!

# Choose source of EWK+tt genuine tau background
#OptionGenuineTauBackgroundSource = "DataDriven"                          # State-of-the-art: embedded data used (use for optimization and results)
OptionGenuineTauBackgroundSource = "MC_FakeAndGenuineTauNotSeparated" # MC used, fake taus are not separated from genuine taus
#OptionGenuineTauBackgroundSource = "MC_FullSystematics"               # MC used, fake and genuine taus separated (use for embedding closure test)
#OptionGenuineTauBackgroundSource = "MC_RealisticProjection"            # MC used, fake and genuine taus separated (can be used for optimization)

OptionSeparateFakeTtbarFromFakeBackground = False # NOTE: this flag should be put true for light H+ and to false for heavy H+

OptionRealisticEmbeddingWithMC = True # Only relevant for OptionReplaceEmbeddingByMC==True
OptionTreatTauIDAndMisIDSystematicsAsShapes = True # Set to true, if you produced multicrabs with doTauIDandMisIDSystematicsAsShapes=True
OptionIncludeSystematics = True # Set to true if you produced multicrabs with doSystematics=True

OptionDoControlPlots = True
OptionDoMergeFakeTauColumns = True # Merges the fake tau columns into one
OptionCombineSingleColumnUncertainties = not True # Makes limit running faster
OptionCtrlPlotsAtMt = True # Produce control plots after all selections (all selections for transverse mass)
OptionDisplayEventYieldSummary = True
OptionNumberOfDecimalsInSummaries = 1
OptionLimitOnSigmaBr = False # Is automatically set to true for heavy H+
OptionDoTBbarForHeavy = False # NOTE: usable only for 2012
OptionAddSingleTopDependencyForMuParameter = False # Affects only light H+
OptionAddSingleTopSignal = False # Affects only light H+

# Convert the following nuisances from shape to constant
OptionConvertFromShapeToConstantList = ["trg_tau","trg_tau_dataeff","trg_tau_MCeff","trg_L1ETM_dataeff","trg_L1ETM_MCeff","trg_L1ETM","trg_muon_dataeff", # triggers
                                        #"tau_ID_shape", # tau ID
                                        "tau_ID_eToTauEndcap_shape", # tau mis-ID
                                        #"tau_ID_eToTauBarrel_shape", "tau_ID_muToTau_shape", "tau_ID_jetToTau_shape", # other tau mis-ID
                                        "ES_jets","JER","ES_METunclustered", # jet, MET
                                        #"ES_taus", # tau ES
                                        #"b_tag", "b_tag_fakes", # btag
                                        "Emb_mu_ID", "Emb_WtauTomu", # embedding-specific
                                        #"Emb_reweighting", # other embedding-specific
                                        #"QCD_metshape", # multijets specific
                                        #"top_pt", # top pt reweighting
                                        "pileup", "pileup_fakes", # pileup
                                        ]
OptionConvertFromShapeToConstantList = [] # FIXME
# Separate in the following shape nuisances the shape and normalization components
OptionSeparateShapeAndNormalizationFromSystVariationList = [
                                                            #"ES_taus"
                                                           ]

# For projections
trg_MET_dataeffScaleFactor = None # Default is None, i.e. 1.0

# Options for reports and article
OptionBr = 0.01  # Br(t->bH+)
OptionSqrtS = 13 # sqrt(s)

# Tolerance for throwing error on luminosity difference (0.01 = 1 percent agreement is required)
ToleranceForLuminosityDifference = 0.05
# Tolerance for almost zero rate (columns with smaller rate are suppressed)
ToleranceForMinimumRate = 0.0 # 1.5
# Minimum stat. uncertainty to set to bins with zero events
MinimumStatUncertainty = 0.5


# Shape histogram definitions
SignalShapeHisto = None
FakeShapeHisto = None
ShapeHistogramsDimensions = None

if OptionMassShape == "TransverseMass":
    SignalShapeHisto = "ForDataDrivenCtrlPlots/shapeTransverseMass"
    FakeShapeTTbarHisto = "ForDataDrivenCtrlPlotsEWKFakeTaus/shapeTransverseMass"
    FakeShapeOtherHisto = "ForDataDrivenCtrlPlotsEWKFakeTaus/shapeTransverseMassProbabilisticBtag"
elif OptionMassShape == "FullMass":
    raise Exception("Does not work")
    SignalShapeHisto = "shapeInvariantMass"
    FakeShapeOtherHisto = "shapeEWKFakeTausInvariantMass"
    FakeShapeTTbarHisto = FakeShapeOtherHisto
elif OptionMassShape == "TransverseAndFullMass2D": # FIXME: preparing to add support, not yet working
    raise Exception("Does not work")
    SignalShapeHisto = "shapetransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    FakeShapeOtherHisto = "shapeEWKFakeTausTransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    FakeShapeTTbarHisto = FakeShapeOtherHisto
ShapeHistogramsDimensions = systematics.getBinningForPlot(SignalShapeHisto)

DataCardName += "_"+OptionMassShape.replace("TransverseMass","mT").replace("FullMass","invMass")

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from HiggsAnalysis.LimitCalc.InputClasses import ObservationInput
Observation = ObservationInput(datasetDefinition="Data",
                               shapeHisto=SignalShapeHisto)
#Observation.setPaths(signalPath,signalDataPaths)

##############################################################################
# Systematics lists
myTrgShapeSystematics = []
myTrgShapeSystematics = ["trg_tau_dataeff","trg_tau_MCeff","trg_L1ETM_dataeff","trg_L1ETM_MCeff"] # Variation done separately for data and MC efficiencies

myTauIDShapeSystematics = []
if OptionTreatTauIDAndMisIDSystematicsAsShapes:
    myTauIDShapeSystematics = ["tau_ID_shape","tau_ID_eToTauBarrel_shape","tau_ID_eToTauEndcap_shape","tau_ID_muToTau_shape","tau_ID_jetToTau_shape"] # tau ID and mis-ID systematics done with shape variation
else:
    myTauIDShapeSystematics = ["tau_ID"] # tau ID and mis-ID systematics done with constants

myShapeSystematics = []
myShapeSystematics.extend(myTrgShapeSystematics)
myShapeSystematics.extend(myTauIDShapeSystematics)
myShapeSystematics.extend(["ES_taus","ES_jets","JER","ES_METunclustered","pileup"]) # btag is not added, because it has the tag and mistag categories

myEmbeddingShapeSystematics = ["trg_tau_dataeff","trg_L1ETM_dataeff","trg_muon_dataeff","ES_taus","Emb_mu_ID","Emb_WtauTomu"]
# Add tau ID uncert. to embedding either as a shape or as a constant
if "tau_ID_shape" in myTauIDShapeSystematics:
    myEmbeddingShapeSystematics.append("tau_ID_shape")
else:
    myEmbeddingShapeSystematics.append("tau_ID")

myFakeShapeSystematics = []
for item in myShapeSystematics:
    if item == "tau_ID":
        myFakeShapeSystematics.append("tau_misID")
    else:
        if not item == "tau_ID_shape":
            myFakeShapeSystematics.append(item)

myShapeSystematics = [] # FIXME

##############################################################################
# DataGroup (i.e. columns in datacard) definitions
#
from HiggsAnalysis.LimitCalc.InputClasses import DataGroup
DataGroups = []
EmbeddingIdList = []
EWKFakeIdList = []

signalTemplate = DataGroup(datasetType="Signal",
                           shapeHisto=SignalShapeHisto)

mergeColumnsByLabel = []

for mass in LightMassPoints:
    myMassList = [mass]
    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(myShapeSystematics[:]+["e_veto", "mu_veto","b_tag","xsect_tt","lumi"])
    hwx.setDatasetDefinition("TTToHplusBWB_M"+str(mass))
    DataGroups.append(hwx)
    
for mass in HeavyMassPoints:
    myMassList = [mass]
    hx = signalTemplate.clone()
    hx.setLabel("Hp"+str(mass)+"_a")
    hx.setLandSProcess(0)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(myShapeSystematics[:]+["e_veto", "mu_veto","b_tag","lumi"])
    if not OptionDoTBbarForHeavy:
        hx.setDatasetDefinition("HplusTB_M"+str(mass))
    else:
        raise Exception("This does not work")
        hx.setDatasetDefinition("HplusToTBbar_M"+str(mass))
    DataGroups.append(hx)

myQCDShapeSystematics = myShapeSystematics[:]
#for i in range(0,len(myQCDShapeSystematics)):
    #if myQCDShapeSystematics[i].startswith("trg_CaloMET") and not "forQCD" in myQCDShapeSystematics[i]:
    #    myQCDShapeSystematics[i] = myQCDShapeSystematics[i]+"_forQCD"

#myQCD = DataGroup(
    #label        = "QCDinv",
    #landsProcess = 3,
    #validMassPoints = MassPoints,
    #datasetType  = "QCD inverted",
    #datasetDefinition = "QCDinvertedmt",
    #nuisances    = myQCDShapeSystematics[:]+["b_tag","top_pt","QCD_metshape","xsect_tt_forQCD","QCDinvTemplateFit","lumi_forQCD"],
    #shapeHisto   = SignalShapeHisto,
#)
#if OptionMassShape == "TransverseMass":
    #myQCD.setDatasetDefinition("QCDinvertedmt")
#elif OptionMassShape == "FullMass":
    #myQCD.setDatasetDefinition("QCDinvertedinvmass")

myQCD = DataGroup(
    label        = "QCDinv",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD MC",
    datasetDefinition = "QCD",
    nuisances    = myShapeSystematics[:]+["b_tag","xsect_QCD","lumi"],
    shapeHisto   = SignalShapeHisto,
)

DataGroups.append(myQCD)

if OptionGenuineTauBackgroundSource == "DataDriven":
    myEmbDataDrivenNuisances = ["Emb_QCDcontam","Emb_hybridCaloMET","Emb_reweighting"]
    # EWK + ttbar with genuine taus
    EmbeddingIdList = [3]
    DataGroups.append(DataGroup(
        label        = "EWK_Tau",
        landsProcess = 1,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        #datasetDefinition   = ["SingleMu"],
        datasetDefinition   = "Data",
        validMassPoints = MassPoints,
        #additionalNormalisation = 0.25, # not needed anymore
        nuisances    = myEmbeddingShapeSystematics[:]+myEmbDataDrivenNuisances[:]
        #nuisances    = ["trg_tau_embedding","tau_ID","ES_taus","Emb_QCDcontam","Emb_WtauTomu","Emb_musel_ditau_mutrg","stat_Emb"]
    ))

    # EWK + ttbar with fake taus
    if not OptionSeparateFakeTtbarFromFakeBackground:
        mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    else:
        mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    DataGroups.append(DataGroup(
        label        = "tt_EWK_faketau",
        landsProcess = 4,
        shapeHisto   = FakeShapeTTbarHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","top_pt","xsect_tt","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "W_EWK_faketau",
        landsProcess = 5,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "WJetsHT",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_Wjets","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_EWK_faketau",
        landsProcess = 6,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_EWK_faketau",
        landsProcess = 7,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "DYJetsToLLHT",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_DYtoll","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_EWK_faketau",
        landsProcess = 8,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_VV","lumi","probBtag"],
    ))
elif OptionGenuineTauBackgroundSource == "MC_FullSystematics" or OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
    # Mimic embedding with MC analysis (introduces double counting of EWK fakes, but that should be small effect)
    myEmbeddingShapeSystematics = []
    mergeColumnsByLabel.append({"label": "MC_EWKTau", "mergeList": ["pseudo_emb_TTJets_MC","pseudo_emb_Wjets_MC","pseudo_emb_t_MC","pseudo_emb_DY_MC","pseudo_emb_VV_MC"], 
                                "subtractList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    if OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
        # Mimic with uncertainties the outcome of data-driven embedding
        myEmbeddingShapeSystematics.append("trg_tau_dataeff")
        myEmbeddingShapeSystematics.append("trg_L1ETM_dataeff")
        myEmbeddingShapeSystematics.append("ES_taus")
        if OptionTreatTauIDAndMisIDSystematicsAsShapes:
            myEmbeddingShapeSystematics.append("tau_ID_shape")
            myFakeShapeSystematics.append("tau_ID_shape")
        else:
            myEmbeddingShapeSystematics.append("tau_ID")
            myFakeShapeSystematics.append("tau_ID")
        myEmbeddingShapeSystematics.extend(["Emb_QCDcontam","Emb_hybridCaloMET","Emb_rest"])
    elif OptionGenuineTauBackgroundSource == "MC_FullSystematics":
        # Use full MC systematics; approximate xsect uncertainty with ttbar xsect unsertainty
        myEmbeddingShapeSystematics = myShapeSystematics[:]+["top_pt","e_veto", "mu_veto","b_tag","xsect_tt","lumi"]
    DataGroups.append(DataGroup(
        label        = "pseudo_emb_TTJets_MC",
        landsProcess = 1,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myEmbeddingShapeSystematics[:],
    ))
    DataGroups.append(DataGroup(
        label        = "pseudo_emb_Wjets_MC",
        landsProcess = None,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "WJetsHT",
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
        datasetDefinition   = "DYJetsToLLHT",
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
    mergeColumnsByLabel.append({"label": "MC_EWKFakeTau", "mergeList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    DataGroups.append(DataGroup(
        label        = "tt_EWK_faketau",
        landsProcess = 4,
        shapeHisto   = FakeShapeTTbarHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","top_pt","xsect_tt","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "W_EWK_faketau",
        landsProcess = 5,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "WJetsHT",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_Wjets","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_EWK_faketau",
        landsProcess = 6,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_EWK_faketau",
        landsProcess = 7,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "DYJetsToLLHT",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_DYtoll","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_EWK_faketau",
        landsProcess = 8,
        shapeHisto   = FakeShapeOtherHisto,
        datasetType  = "EWKfake",
        datasetDefinition   = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_fakes", "mu_veto_fakes","b_tag_fakes","xsect_VV","lumi","probBtag"],
    ))
elif OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
    # Replace embedding and fakes with MC
    #if OptionDoMergeFakeTauColumns:
        #myList = ["Wjets_MC","DY_MC","VV_MC"]
        #if not OptionAddSingleTopDependencyForMuParameter:
            #myList.append("sngltop_MC")
            #mergeColumnsByLabel.append({"label": "EWKnontop_MC", "mergeList": myList[:]})
        #else:
            #mergeColumnsByLabel.append({"label": "EWKnontt_MC", "mergeList": myList[:]})
    DataGroups.append(DataGroup(
        label        = "ttbar_MC",
        landsProcess = 1,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_veto", "mu_veto","b_tag","top_pt","xsect_tt","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "Wjets_MC",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "WJetsHT",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_veto", "mu_veto","b_tag","xsect_Wjets","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "sngltop_MC",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_veto", "mu_veto","b_tag","xsect_singleTop","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_MC",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "DYJetsToLLHT",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_veto", "mu_veto","b_tag","xsect_DYtoll","lumi"],
    ))
    #DataGroups.append(DataGroup(
        #label        = "VV_MC",
        #landsProcess = 7,
        #shapeHisto   = SignalShapeHisto,
        #datasetType  = "Embedding",
        #datasetDefinition = "Diboson",
        #validMassPoints = MassPoints,
        #nuisances    = myShapeSystematics[:]+["e_veto", "mu_veto","b_tag","xsect_VV","lumi"],
    #))
else:
    raise Exception("Error: unknown value for flag OptionGenuineTauBackgroundSource!")

# Reserve column 2
if not OptionAddSingleTopSignal:
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
from HiggsAnalysis.LimitCalc.InputClasses import Nuisance
ReservedNuisances = []
Nuisances = []

# 2015 definitions
Nuisances.append(Nuisance(
    id            = "trg_tau_dataeff",
    label         = "tau+MET trg tau part data eff.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.015,
))
Nuisances.append(Nuisance(
    id            = "trg_tau_MCeff",
    label         = "tau+MET trg tau part MC eff.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.010,
))
Nuisances.append(Nuisance(
    id            = "trg_L1ETM_dataeff",
    label         = "tau+MET trg L1ETM data eff.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.030,
))
Nuisances.append(Nuisance(
    id            = "trg_L1ETM_MCeff",
    label         = "tau+MET trg L1ETM MC eff.",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.001,
))
Nuisances.append(Nuisance(
    id            = "e_veto",
    label         = "e veto",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "passed e selection (Veto)", # main counter name after electron veto
    denominator   = "Tau trigger SF", # main counter name before electron and muon veto
    scaling       = 0.02
))
Nuisances.append(Nuisance(
    id            = "e_veto_fakes",
    label         = "e veto fakes",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "passed e selection (Veto)", # main counter name after electron veto
    denominator   = "Tau trigger SF", # main counter name before electron and muon veto # the name is misleading, it is actually after tau trg scale factor
    scaling       = 0.02
))
Nuisances.append(Nuisance(
    id            = "mu_veto",
    label         = "mu veto",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "passed mu selection (Veto)", # main counter name after electron and muon veto
    denominator   = "passed e selection (Veto)", # main counter name before muon veto
    scaling       = 0.01
))
Nuisances.append(Nuisance(
    id            = "mu_veto_fakes",
    label         = "mu veto fakes",
    distr         = "lnN",
    function      = "Ratio",
    numerator     = "passed mu selection (Veto)", # main counter name after electron and muon veto
    denominator   = "passed e selection (Veto)", # main counter name before muon veto
    scaling       = 0.01
))
if "tau_ID_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_shape",
        label         = "tau-jet ID (no Rtau) genuine taus",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.06,
    ))
if "tau_ID_eToTauBarrel_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_eToTauBarrel_shape",
        label         = "tau-jet ID (no Rtau) e->tau (barrel)",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.001,
    ))
if "tau_ID_eToTauEndcap_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_eToTauEndcap_shape",
        label         = "tau-jet ID (no Rtau) e->tau (endcap)",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.001,
    ))
if "tau_ID_muToTau_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_muToTau_shape",
        label         = "tau-jet ID (no Rtau) mu->tau",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.001,
    ))
if "tau_ID_jetToTau_shape" in myShapeSystematics:
    Nuisances.append(Nuisance(
        id            = "tau_ID_jetToTau_shape",
        label         = "tau-jet ID (no Rtau) jet->tau",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.01,
    ))
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
    value         = 0.015,
))
Nuisances.append(Nuisance(
    id            = "b_tag",
    label         = "NON-EXACT VALUE for btagging",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04,
))
Nuisances.append(Nuisance(
    id            = "b_tag_fakes",
    label         = "NON-EXACT VALUE for btagging for EWK fake taus",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04,
))
Nuisances.append(Nuisance(
    id            = "b_mistag",
    label         = "NON-EXACT VALUE for mistagging",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04,
))
Nuisances.append(Nuisance(
    id            = "b_mistag_fakes",
    label         = "NON-EXACT VALUE for mistagging EWK fake taus",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.04,
))
Nuisances.append(Nuisance(
    id            = "top_pt",
    label         = "NON-EXACT VALUE for top pT reweighting",
    distr         = "lnN",
    function      = "Constant",
    value         = 0.05,
))
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
    id            = "probBtag",
    label         = "probabilistic btag", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.5
))
Nuisances.append(Nuisance(
    id            = "QCDinvTemplateFit",
    label         = "QCDInv: fit", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.03,
))
Nuisances.append(Nuisance(
    id            = "xsect_tt",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyDown(),
    upperValue    = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyUp(),
))
Nuisances.append(Nuisance(
    id            = "xsect_tt_forQCD",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "ConstantForQCD",
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
    id            = "xsect_QCD",
    label         = "QCD MC cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("QCD").getUncertaintyDown()
))
Nuisances.append(Nuisance(
    id            = "lumi",
    label         = "luminosity",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getLuminosityUncertainty()
))
Nuisances.append(Nuisance(
    id            = "lumi_forQCD",
    label         = "luminosity",
    distr         = "lnN",
    function      = "ConstantForQCD",
    value         = systematics.getLuminosityUncertainty()
))


# 2012 definitions
#if False:
    #if "trg_tau" in myShapeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "trg_tau",
            #label         = "tau+MET trg tau part",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "TauTrgSF",
        #))
    #else:
        #Nuisances.append(Nuisance(
            #id            = "trg_tau_dataeff",
            #label         = "tau+MET trg tau part data eff.",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "TauTrgDataEff",
        #))

        #Nuisances.append(Nuisance(
            #id            = "trg_tau_MCeff",
            #label         = "tau+MET trg tau part MC eff.",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "TauTrgMCEff",
        #))

    #if OptionIncludeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "trg_L1ETM_dataeff",
            #label         = "tau+MET trg L1ETM data eff.",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "L1ETMDataEff",
        #))
        #Nuisances.append(Nuisance(
            #id            = "trg_L1ETM_MCeff",
            #label         = "tau+MET trg L1ETM MC eff.",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "L1ETMMCEff",
        #))

    #if OptionGenuineTauBackgroundSource == "DataDriven":
        #Nuisances.append(Nuisance(
            #id            = "trg_muon_dataeff",
            #label         = "SingleMu trg data eff.",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "MuonTrgDataEff",
        #))

    #if not "tau_ID_shape" in myShapeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "tau_ID",
            #label         = "tau-jet ID (no Rtau)",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = systematics.getTauIDUncertainty(isGenuineTau=True)
        #))

        #Nuisances.append(Nuisance(
            #id            = "tau_misID",
            #label         = "tau-jet mis ID (no Rtau)",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.15, # FIXME
        #))

    ##Nuisances.append(Nuisance(
        ##id            = "tau_ID_constShape",
        ##label         = "tau-jet ID (no Rtau)",
        ##distr         = "shapeQ",
        ##function      = "ConstantToShape",
        ##value         = systematics.getTauIDUncertainty(isGenuineTau=True)
    ##))

    #if "tau_ID_shape" in myShapeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "tau_ID_shape",
            #label         = "tau-jet ID (no Rtau) genuine taus",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "GenuineTau",
        #))

    #if "tau_ID_eToTauBarrel_shape" in myShapeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "tau_ID_eToTauBarrel_shape",
            #label         = "tau-jet ID (no Rtau) e->tau (barrel)",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "FakeTauBarrelElectron",
        #))

    #if "tau_ID_eToTauEndcap_shape" in myShapeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "tau_ID_eToTauEndcap_shape",
            #label         = "tau-jet ID (no Rtau) e->tau (endcap)",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "FakeTauEndcapElectron",
        #))

    #if "tau_ID_muToTau_shape" in myShapeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "tau_ID_muToTau_shape",
            #label         = "tau-jet ID (no Rtau) mu->tau",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "FakeTauMuon",
        #))

    #if "tau_ID_jetToTau_shape" in myShapeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "tau_ID_jetToTau_shape",
            #label         = "tau-jet ID (no Rtau) jet->tau",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "FakeTauJet",
        #))

    #if OptionIncludeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "ES_taus",
            #label         = "TES bin-by-bin uncertainty",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "TES",
        #))
        #Nuisances.append(Nuisance(
            #id            = "ES_jets",
            #label         = "JES bin-by-bin uncertainty",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "JES",
        #))
        #Nuisances.append(Nuisance(
            #id            = "JER",
            #label         = "Jet energy resolution",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "JER",
        #))
        #Nuisances.append(Nuisance(
            #id            = "ES_METunclustered",
            #label         = "MET unclustered scale bin-by-bin uncertainty",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "MET",
        #))
        #Nuisances.append(Nuisance(
            #id            = "b_tag",
            #label         = "btagging",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "BTagSF",
        #))
        #Nuisances.append(Nuisance(
            #id            = "b_tag_fakes",
            #label         = "btagging for EWK fake taus",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "BTagSF",
        #))
        ##Nuisances.append(Nuisance(
            ##id            = "b_mistag",
            ##label         = "mistagging",
            ##distr         = "shapeQ",
            ##function      = "ShapeVariation",
            ##systVariation = "BTagSF",
        ##))
        ##Nuisances.append(Nuisance(
            ##id            = "b_mistag_fakes",
            ##label         = "mistagging EWK fake taus",
            ##distr         = "shapeQ",
            ##function      = "ShapeVariation",
            ##systVariation = "BTagSF",
        ##))
        #Nuisances.append(Nuisance(
            #id            = "top_pt",
            #label         = "top pT reweighting",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "TopPtWeight",
        #))
    #else:
        #Nuisances.append(Nuisance(
            #id            = "ES_taus",
            #label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.03,
        #))
        #Nuisances.append(Nuisance(
            #id            = "ES_jets",
            #label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.03,
        #))
        #Nuisances.append(Nuisance(
            #id            = "ES_METunclustered",
            #label         = "NON-EXACT VALUE for JES/JER/MET/Rtau effect on mT shape",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.01,
        #))
        #Nuisances.append(Nuisance(
            #id            = "JER",
            #label         = "NON-EXACT VALUE for Jet energy resolution",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.02,
        #))
        #Nuisances.append(Nuisance(
            #id            = "b_tag",
            #label         = "NON-EXACT VALUE for btagging",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.05,
        #))
        #Nuisances.append(Nuisance(
            #id            = "b_tag_fakes",
            #label         = "NON-EXACT VALUE for btagging for EWK fake taus",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.05,
        #))
        #Nuisances.append(Nuisance(
            #id            = "b_tag",
            #label         = "NON-EXACT VALUE for mistagging",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.05,
        #))
        #Nuisances.append(Nuisance(
            #id            = "b_tag_fakes",
            #label         = "NON-EXACT VALUE for mistagging EWK fake taus",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.05,
        #))
        #Nuisances.append(Nuisance(
            #id            = "top_pt",
            #label         = "NON-EXACT VALUE for top pT reweighting",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.15,
        #))

    #if OptionGenuineTauBackgroundSource == "DataDriven":
        #Nuisances.append(Nuisance(
            #id            = "Emb_mu_ID",
            #label         = "Muon ID for embedding",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "MuonIdDataEff",
        #))

    #Nuisances.append(Nuisance(
        #id            = "e_veto",
        #label         = "e veto",
        #distr         = "lnN",
        #function      = "Ratio",
        #numerator     = "electron veto", # main counter name after electron and muon veto
        #denominator   = "tau trigger scale factor", # main counter name before electron and muon veto
        #scaling       = 0.02
    #))

    #Nuisances.append(Nuisance(
        #id            = "e_veto_fakes",
        #label         = "e veto",
        #distr         = "lnN",
        #function      = "Ratio",
        #numerator     = "EWKfaketaus:electron veto", # main counter name after electron and muon veto
        #denominator   = "EWKfaketaus:taus == 1", # main counter name before electron and muon veto # the name is misleading, it is actually after tau trg scale factor
        #scaling       = 0.02
    #))

    #Nuisances.append(Nuisance(
        #id            = "mu_veto",
        #label         = "mu veto",
        #distr         = "lnN",
        #function      = "Ratio",
        #numerator     = "muon veto", # main counter name after electron and muon veto
        #denominator   = "electron veto", # main counter name before electron and muon veto
        #scaling       = 0.01
    #))

    #Nuisances.append(Nuisance(
        #id            = "mu_veto_fakes",
        #label         = "mu veto",
        #distr         = "lnN",
        #function      = "Ratio",
        #numerator     = "EWKfaketaus:muon veto", # main counter name after electron and muon veto
        #denominator   = "EWKfaketaus:electron veto", # main counter name before electron and muon veto # the name is misleading, it is actually after tau trg scale factor
        #scaling       = 0.01
    #))

    #Nuisances.append(Nuisance(
        #id            = "QCD_metshape",
        #label         = "QCD met shape syst.",
        #distr         = "shapeQ",
        #function      = "QCDShapeVariation",
        #systVariation = "QCDNormSource",
    #))

    #if OptionGenuineTauBackgroundSource == "DataDriven" or OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
        #Nuisances.append(Nuisance(
            #id            = "Emb_QCDcontam",
            #label         = "EWK with taus QCD contamination",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.020 #FIXME
        #))
        #Nuisances.append(Nuisance(
            #id            = "Emb_hybridCaloMET",
            #label         = "EWK with taus hybrid calo MET and L1ETM",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.12 #FIXME
        #))


    #if OptionGenuineTauBackgroundSource == "DataDriven":
        #if "Emb_WtauTomu" in myEmbeddingShapeSystematics:
            #Nuisances.append(Nuisance(
                #id            = "Emb_WtauTomu",
                #label         = "EWK with taus W->tau->mu",
                #distr         = "shapeQ",
                #function      = "ShapeVariation",
                #systVariation = "WTauMu",
            #))
        #else:
            #Nuisances.append(Nuisance(
                #id            = "Emb_WtauTomu",
                #label         = "EWK with taus W->tau->mu",
                #distr         = "lnN",
                #function      = "Constant",
                #value         = 0.007
            #))
        #Nuisances.append(Nuisance(
            #id            = "Emb_reweighting",
            #label         = "Embedding reweighting",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "EmbMTWeight",
        #))

    #if OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
        #Nuisances.append(Nuisance(
            #id            = "Emb_rest",
            #label         = "EWK with taus W->tau->mu",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.03
        #))

    ##Nuisances.append(Nuisance(
        ##id            = "Emb_musel_ditau_mutrg",
        ##label         = "EWK with taus muon selection+ditau+mu trg",
        ##distr         = "lnN",
        ##function      = "Constant",
        ##value         = 0.031 #FIXME
    ##))

    #Nuisances.append(Nuisance(
        #id            = "xsect_tt",
        #label         = "ttbar cross section",
        #distr         = "lnN",
        #function      = "Constant",
        #value         = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyDown(),
        #upperValue    = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyUp(),
    #))

    #Nuisances.append(Nuisance(
        #id            = "xsect_tt_forQCD",
        #label         = "ttbar cross section",
        #distr         = "lnN",
        #function      = "ConstantForQCD",
        #value         = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyDown(),
        #upperValue    = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyUp(),
    #))

    #Nuisances.append(Nuisance(
        #id            = "xsect_Wjets",
        #label         = "W+jets cross section",
        #distr         = "lnN",
        #function      = "Constant",
        #value         = systematics.getCrossSectionUncertainty("WJets").getUncertaintyDown()
    #))

    #Nuisances.append(Nuisance(
        #id            = "xsect_singleTop",
        #label         = "single top cross section",
        #distr         = "lnN",
        #function      = "Constant",
        #value         = systematics.getCrossSectionUncertainty("SingleTop").getUncertaintyDown()
    #))

    #Nuisances.append(Nuisance(
        #id            = "xsect_DYtoll",
        #label         = "Z->ll cross section",
        #distr         = "lnN",
        #function      = "Constant",
        #value         = systematics.getCrossSectionUncertainty("DYJetsToLL").getUncertaintyDown()
    #))

    #Nuisances.append(Nuisance(
        #id            = "xsect_VV",
        #label         = "diboson cross section",
        #distr         = "lnN",
        #function      = "Constant",
        #value         = systematics.getCrossSectionUncertainty("Diboson").getUncertaintyDown()
    #))

    #Nuisances.append(Nuisance(
        #id            = "lumi",
        #label         = "luminosity",
        #distr         = "lnN",
        #function      = "Constant",
        #value         = systematics.getLuminosityUncertainty()
    #))

    #Nuisances.append(Nuisance(
        #id            = "lumi_forQCD",
        #label         = "luminosity",
        #distr         = "lnN",
        #function      = "ConstantForQCD",
        #value         = systematics.getLuminosityUncertainty()
    #))

    #if OptionIncludeSystematics:
        #Nuisances.append(Nuisance(
            #id            = "pileup",
            #label         = "pileup",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "PUWeight",
        #))

        #Nuisances.append(Nuisance(
            #id            = "pileup_fakes",
            #label         = "pileup",
            #distr         = "shapeQ",
            #function      = "ShapeVariation",
            #systVariation = "PUWeight",
        #))
    #else:
        #Nuisances.append(Nuisance(
            #id            = "pileup",
            #label         = "FAKE pileup",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.05
        #))
        #Nuisances.append(Nuisance(
            #id            = "pileup_fakes",
            #label         = "FAKE pileup",
            #distr         = "lnN",
            #function      = "Constant",
            #value         = 0.05
        #))

    #Nuisances.append(Nuisance(
        #id            = "probBtag",
        #label         = "probabilistic btag", 
        #distr         = "lnN",
        #function      = "Constant", 
        #value         = 0.5
    #))

    #Nuisances.append(Nuisance(
        #id            = "QCDinvTemplateFit",
        #label         = "QCDInv: fit", 
        #distr         = "lnN",
        #function      = "Constant", 
        #value         = 0.03,
    #))

MergeNuisances = []
if "tau_ID_constShape" in myEmbeddingShapeSystematics:
    MergeNuisances.append(["tau_ID_shape", "tau_ID_constShape"])
#MergeNuisances.append(["ES_taus","ES_taus_fakes","ES_taus_tempForEmbedding"])
#MergeNuisances.append(["ES_jets","ES_jets_fakes"])
#MergeNuisances.append(["JER","JER_fakes"])
#MergeNuisances.append(["ES_METunclustered","ES_METunclustered_fakes"])
MergeNuisances.append(["e_veto", "e_veto_fakes"])
MergeNuisances.append(["mu_veto", "mu_veto_fakes"])
MergeNuisances.append(["b_tag","b_tag_fakes"])
MergeNuisances.append(["b_mistag","b_mistag_fakes"])
MergeNuisances.append(["pileup","pileup_fakes"])
MergeNuisances.append(["xsect_tt", "xsect_tt_forQCD"])
MergeNuisances.append(["lumi", "lumi_forQCD"])

from HiggsAnalysis.LimitCalc.InputClasses import convertFromSystVariationToConstant
convertFromSystVariationToConstant(Nuisances, OptionConvertFromShapeToConstantList)

from HiggsAnalysis.LimitCalc.InputClasses import separateShapeAndNormalizationFromSystVariation
separateShapeAndNormalizationFromSystVariation(Nuisances, OptionSeparateShapeAndNormalizationFromSystVariationList)

# Control plots
from HiggsAnalysis.LimitCalc.InputClasses import ControlPlotInput
ControlPlots = []

ControlPlots.append(ControlPlotInput(
    title            = "WeightedCounters",
    signalHistoPath  = "counters/weighted",
    signalHistoName  = "counter",
    EWKfakeHistoPath  = "counters/weighted",
    EWKfakeHistoName  = "counter",
    details          = { "xlabel": "",
                         "xlabelsize": 10,
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "opts": {"ymin": 0.0009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

#ControlPlots.append(ControlPlotInput(
    #title            = "NVertices_AfterStandardSelections",
    #signalHistoPath  = "ForDataDrivenCtrlPlots",
    #signalHistoName  = "NVertices_AfterStandardSelections",
    #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    #EWKfakeHistoName  = "NVertices_AfterStandardSelections",
    #details          = { "xlabel": "N_{vertices}",
                         #"ylabel": "Events",
                         #"divideByBinWidth": False,
                         #"unit": "",
                         #"log": True,
                         #"opts": {"ymin": 0.0009} },
    #blindedRange     = [], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_pT_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_pT_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_pT_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.0009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_p_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_p_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_p_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau p",
                         "ylabel": "Events/#Deltap",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_eta_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_eta_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_eta_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau #eta",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_phi_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_phi_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_phi_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau #phi",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_ldgTrkPt_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_ldgTrkPt_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_ldgTrkPt_AfterStandardSelections",
    details          = { "xlabel": "#tau leading track ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.0009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_LeadingTrackP_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_LeadingTrackP_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_LeadingTrackP_AfterStandardSelections",
    details          = { "xlabel": "#tau leading track p",
                         "ylabel": "Events/#Deltap",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.0009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_Rtau_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_Rtau_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_Rtau_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau ^{}R_{#tau}",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SE",
                         "opts": {"ymin": 0.009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_DecayMode_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_DecayMode_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_DecayMode_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau Decay mode",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.9} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_Nprongs_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_Nprongs_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_Nprongs_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau N_{prongs}",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.9} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_source_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "SelectedTau_source_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "SelectedTau_source_AfterStandardSelections",
    details          = { "xlabel": "",
                         "ylabel": "Events",
                         "xlabelsize": 10,
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.9} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "NjetsAfterJetSelectionAndMETSF",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "NjetsAfterJetSelectionAndMETSF",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "NjetsAfterJetSelectionAndMETSF",
    details          = { "xlabel": "Number of selected jets",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "opts": {"ymin": 0.9} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "^{}#tau_{h}+#geq3j", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "JetPt_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "JetPt_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "JetPt_AfterStandardSelections",
    details          = { "xlabel": "jet ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "JetEta_AfterStandardSelections",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "JetEta_AfterStandardSelections",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "JetEta_AfterStandardSelections",
    details          = { "xlabel": "jet #eta",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.09} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "CollinearAngularCutsMinimum",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "CollinearAngularCutsMinimum",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "CollinearAngularCutsMinimum",
    details          = { "xlabel": "R_{coll}^{min}",
        #"xlabel": "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1..3},MET))^{2}})",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SE",
                         "opts": {"ymin": 0.09} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "R_{coll}^{min}", # Leave blank if you don't want to include the item to the selection flow plot
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
                         "opts": {"ymin": 0.09} },
    blindedRange=[],
    #blindedRange     = [1.5,10], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "#geq1 b tag", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "BtagDiscriminator",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "BtagDiscriminator",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "BtagDiscriminator",
    details          = { "xlabel": "b tag discriminator",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "NE",
                         "opts": {"ymin": 0.9} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "BJetPt",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "BJetPt",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "BJetPt",
    details          = { "xlabel": "b jet ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.0009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "BJetEta",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "BJetEta",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "BJetEta",
    details          = { "xlabel": "b jet #eta",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.09} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))


ControlPlots.append(ControlPlotInput(
    title            = "MET",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "MET",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "MET",
    details          = { "xlabel": "E_{T}^{miss}",
                         "ylabel": "Events/^{}#DeltaE_{T}^{miss}",
                         "divideByBinWidth": True,
                         "unit": "GeV",
                         "log": True,
                         "opts": {"ymin": 0.00009} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "^{}E_{T}^{miss}", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "METPhi",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "METPhi",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "METPhi",
    details          = { "xlabel": "E_{T}^{miss} #phi",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.09} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
))

#ControlPlots.append(ControlPlotInput(
    #title            = "TauPlusMETPt",
    #signalHistoPath  = "ForDataDrivenCtrlPlots",
    #signalHistoName  = "TauPlusMETPt",
    #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    #EWKfakeHistoName  = "TauPlusMETPt",
    #details          = { "xlabel": "p_{T}(#tau + ^{}E_{T}^{miss})",
                         #"ylabel": "Events/^{}#Deltap_{T}",
                         #"divideByBinWidth": True,
                         #"unit": "GeV",
                         #"log": True,
                         #"opts": {"ymin": 0.0009} },
    #blindedRange     = [], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#for i in range(1,5):
    #ControlPlots.append(ControlPlotInput(
        #title            = "CollinearAngularCuts2DJet%d"%i,
        #signalHistoPath  = "ForDataDrivenCtrlPlots",
        #signalHistoName  = "ImprovedDeltaPhiCuts2DJet%dCollinear"%i,
        #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        #EWKfakeHistoName  = "ImprovedDeltaPhiCuts2DJet%dCollinear"%i,
        #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                             #"ylabel": "#Delta#phi(jet_{%d},E_{T}^{miss})"%i,
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": False,
                            #"legendPosition": "NW",
                            #"opts": {"zmin": 0.0} },
        #blindedRange     = [], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))
    #ControlPlots.append(ControlPlotInput(
        #title            = "BackToBackAngularCuts2DJet%d"%i,
        #signalHistoPath  = "ForDataDrivenCtrlPlots",
        #signalHistoName  = "ImprovedDeltaPhiCuts2DJet%dBackToBack"%i,
        #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        #EWKfakeHistoName  = "ImprovedDeltaPhiCuts2DJet%dBackToBack"%i,
        #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                             #"ylabel": "#Delta#phi(jet_{%d},E_{T}^{miss})"%i,
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": False,
                            #"legendPosition": "NW",
                            #"opts": {"zmin": 0.0} },
        #blindedRange     = [], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))

#ControlPlots.append(ControlPlotInput(
    #title            = "CollinearAngularCuts2DMinimum",
    #signalHistoPath  = "ForDataDrivenCtrlPlots",
    #signalHistoName  = "ImprovedDeltaPhiCuts2DCollinearMinimum",
    #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    #EWKfakeHistoName  = "ImprovedDeltaPhiCuts2DCollinearMinimum",
    #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                          #"ylabel": "#Delta#phi(jet_{1..3},E_{T}^{miss})",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": False,
                        #"legendPosition": "NW",
                        #"opts": {"zmin": 0.0} },
    #blindedRange     = [], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "BackToBackAngularCuts2DMinimum",
    #signalHistoPath  = "ForDataDrivenCtrlPlots",
    #signalHistoName  = "ImprovedDeltaPhiCuts2DBackToBackMinimum",
    #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    #EWKfakeHistoName  = "ImprovedDeltaPhiCuts2DBackToBackMinimum",
    #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                          #"ylabel": "#Delta#phi(jet_{1..3},E_{T}^{miss})",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": False,
                        #"legendPosition": "NW",
                        #"opts": {"zmin": 0.0} },
    #blindedRange     = [], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "DeltaPhiTauMet",
    #signalHistoPath  = "ForDataDrivenCtrlPlots",
    #signalHistoName  = "DeltaPhiTauMet",
    #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    #EWKfakeHistoName  = "DeltaPhiTauMet",
    #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                          #"ylabel": "Events",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": True,
                        #"legendPosition": "NW",
                        #"opts": {"ymin": 0.9} },
    #blindedRange     = [], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "MinDeltaPhiTauJet",
    #signalHistoPath  = "ForDataDrivenCtrlPlots",
    #signalHistoName  = "MinDeltaPhiTauJet",
    #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    #EWKfakeHistoName  = "MinDeltaPhiTauJet",
    #details          = { "xlabel": "min (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                          #"ylabel": "Events",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": True,
                        #"legendPosition": "NW",
                        #"opts": {"ymin": 0.9} },
    #blindedRange     = [], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "MaxDeltaPhiTauJet",
    #signalHistoPath  = "ForDataDrivenCtrlPlots",
    #signalHistoName  = "MaxDeltaPhiTauJet",
    #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    #EWKfakeHistoName  = "MaxDeltaPhiTauJet",
    #details          = { "xlabel": "max (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                          #"ylabel": "Events",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": True,
                        #"legendPosition": "NW",
                        #"opts": {"ymin": 0.9} },
    #blindedRange     = [], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))


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
                         #"xlabel": "#Delta#phi(^{}#tau_{h},^{}E_{T}^{miss})",
                         #"ylabel": "Events",
                         #"unit": "^{o}",
                         #"log": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "^{}N_{b jets}", # Leave blank if you don't want to include the item to the selection flow plot
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
                         #"xlabel": "max(#Delta#phi(jet,^{}E_{T}^{miss})",
                         #"ylabel": "Events",
                         #"unit": "^{o}",
                         #"log": True,
                         #"DeltaRatio": 0.5,
                         #"ymin": 0.9,
                         #"ymax": -1},
    #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
    #evaluationRange  = [], # specify range to be evaluated and saved into a file
    #flowPlotCaption  = "#Delta#phi(^{}#tau_{h},^{}E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
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


ControlPlots.append(ControlPlotInput(
    title            = "BackToBackAngularCutsMinimum",
    signalHistoPath  = "ForDataDrivenCtrlPlots",
    signalHistoName  = "BackToBackAngularCutsMinimum",
    EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
    EWKfakeHistoName  = "BackToBackAngularCutsMinimum",
    details          = { "xlabel": "^{}R_{bb}^{min}",
    #"xlabel": "min(#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..3},MET)^{2}})",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SE",
                         "opts": {"ymin": 0.09} },
    blindedRange     = [], # specify range min,max if blinding applies to this control plot
    evaluationRange  = [], # specify range to be evaluated and saved into a file
    flowPlotCaption  = "^{}R_{bb}^{min}", # Leave blank if you don't want to include the item to the selection flow plot
))

if OptionMassShape == "TransverseMass":
    ControlPlots.append(ControlPlotInput(
        title            = "TransverseMass",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "shapeTransverseMass",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "shapeEWKFakeTausTransverseMass",
        details          = {"cmsTextPosition": "right",
                            #"xlabel": "m_{T}(^{}#tau_{h},^{}E_{T}^{miss})",
                            #"ylabel": "Events/^{}#Deltam_{T}",
                            #"unit": "GeV",
                            "xlabel": "m_{T} (GeV)",
                            "ylabel": "< Events / bin >", "ylabelBinInfo": False,
                            "moveLegend": {"dx": -0.10, "dy": -0.12, "dh":0.1},
                            "ratioMoveLegend": {"dx": -0.06, "dy": -0.33},
                            "divideByBinWidth": True,
                            "log": False,
                            "opts": {"ymin": 0.0},
                            "opts2": {"ymin": 0.0, "ymax": 2.0}
                            },
        blindedRange     = [81, 1000], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [60, 180], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "final", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    ControlPlots.append(ControlPlotInput(
        title            = "TransverseMassLog",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "shapeTransverseMass",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "shapeEWKFakeTausTransverseMass",
        details          = {"cmsTextPosition": "right",
                            #"xlabel": "m_{T}(^{}#tau_{h},^{}E_{T}^{miss})",
                            #"ylabel": "Events/^{}#Deltam_{T}",
                            #"unit": "GeV",
                            "xlabel": "m_{T} (GeV)",
                            "ylabel": "< Events / bin >", "ylabelBinInfo": False,
                            "moveLegend": {"dx": -0.10, "dy": -0.12, "dh":0.1},
                            "ratioMoveLegend": {"dx": -0.06, "dy": -0.33},
                            "divideByBinWidth": True,
                            "log": True,
                            "opts": {"ymin": 1e-4},
                            "opts2": {"ymin": 0.0, "ymax": 2.0}
                           },
        blindedRange     = [81, 1000], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
elif OptionMassShape == "FullMass":
    ControlPlots.append(ControlPlotInput(
        title            = "FullMass",
        signalHistoPath  = "",
        signalHistoName  = "shapeInvariantMass",
        EWKfakeHistoPath  = "",
        EWKfakeHistoName  = "shapeEWKFakeTausInvariantMass",
        details          = { "xlabel": "m(^{}#tau_{h},^{}E_{T}^{miss})",
                             "ylabel": "Events/#Deltam",
                             "divideByBinWidth": True,
                             "unit": "GeV",
                             "log": False,
                             "opts": {"ymin": 0.0},
                             "opts2": {"ymin": 0.0, "ymax": 2.0},
                           },
        blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [80, 180], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "final", # Leave blank if you don't want to include the item to the selection flow plot
    ))

if OptionCtrlPlotsAtMt:
    ControlPlots.append(ControlPlotInput(
        title            = "NVertices_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "NVertices_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "NVertices_AfterAllSelections",
        details          = { "xlabel": "N_{vertices}",
                            "ylabel": "Events",
                            "divideByBinWidth": False,
                            "unit": "",
                            "log": True,
                            "opts": {"ymin": 0.0009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
      flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
  
    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_pT_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_pT_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_pT_AfterAllSelections",
        details          = { "xlabel": "Selected #tau ^{}p_{T}",
                             "ylabel": "Events/^{}#Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "opts": {"ymin": 0.0009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_p_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_p_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_p_AfterAllSelections",
        details          = { "xlabel": "Selected #tau p",
                             "ylabel": "Events/#Deltap",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "opts": {"ymin": 0.009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_eta_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_eta_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_eta_AfterAllSelections",
        details          = { "xlabel": "Selected #tau #eta",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_phi_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_phi_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_phi_AfterAllSelections",
        details          = { "xlabel": "Selected #tau #phi",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "{}^{o}",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.09} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_ldgTrkPt_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_ldgTrkPt_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_ldgTrkPt_AfterAllSelections",
        details          = { "xlabel": "#tau leading track p{}_{T}",
                             "ylabel": "Events/^{}#Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "ratioLegendPosition": "right",
                             "opts": {"ymin": 0.0009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_LeadingTrackP_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_LeadingTrackP_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_LeadingTrackP_AfterAllSelections",
        details          = { "xlabel": "#tau leading track p",
                             "ylabel": "Events/#Deltap",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "ratioLegendPosition": "right",
                             "opts": {"ymin": 0.0009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_Rtau_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_Rtau_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_Rtau_AfterAllSelections",
        details          = { "xlabel": "Selected #tau R_{#tau}",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SE",
                             "opts": {"ymin": 0.009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_Rtau_FullRange_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_Rtau_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_Rtau_AfterAllSelections",
        details          = { "xlabel": "Selected #tau R_{#tau}",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts2": {"ymin": 0.2, "ymax": 1.8},
                             "opts": {"ymin": 0.009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_DecayMode_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_DecayMode_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_DecayMode_AfterAllSelections",
        details          = { "xlabel": "Selected #tau Decay mode",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "ratioLegendPosition": "right",
                             "opts": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_Nprongs_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_Nprongs_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_Nprongs_AfterAllSelections",
        details          = { "xlabel": "Selected #tau N_{prongs}",
                            "ylabel": "Events",
                            "divideByBinWidth": False,
                            "unit": "",
                            "log": True,
                            "ratioLegendPosition": "right",
                            "opts": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_source_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "SelectedTau_source_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "SelectedTau_source_AfterAllSelections",
        details          = { "xlabel": "",
                            "ylabel": "Events",
                            "xlabelsize": 10,
                            "divideByBinWidth": False,
                            "unit": "",
                            "log": True,
                            "ratioLegendPosition": "right",
                            "opts": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "Njets_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "Njets_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "Njets_AfterAllSelections",
        details          = { "xlabel": "Number of selected jets",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "opts": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "JetPt_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "JetPt_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "JetPt_AfterAllSelections",
        details          = { "xlabel": "jet ^{}p_{T}",
                             "ylabel": "Events/^{}Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "opts": {"ymin": 0.009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "JetEta_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "JetEta_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "JetEta_AfterAllSelections",
        details          = { "xlabel": "jet #eta",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.09} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "CollinearAngularCutsMinimum_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "CollinearAngularCutsMinimum_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "CollinearAngularCutsMinimum_AfterAllSelections",
        details          = { "xlabel": "R_{coll}^{min}",
        #"xlabel": "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1..3},MET))^{2}})",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "{}^{o}",
                             "log": True,
                             "legendPosition": "NW",
                             "opts": {"ymin": 0.09} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BJetSelection_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "NBjets_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "NBjets_AfterAllSelections",
        details          = { "xlabel": "Number of selected b jets",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "opts": {"ymin": 0.09} },
        blindedRange=[],
        #blindedRange     = [1.5,10], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BtagDiscriminator_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "BtagDiscriminator_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "BtagDiscriminator_AfterAllSelections",
        details          = { "xlabel": "b tag discriminator",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "NE",
                             "opts": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BJetPt_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "BJetPt_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "BJetPt_AfterAllSelections",
        details          = { "xlabel": "b jet ^{}p_{T}",
                             "ylabel": "Events/^{}#Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "opts": {"ymin": 0.0009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BJetEta_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "BJetEta_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "BJetEta_AfterAllSelections",
        details          = { "xlabel": "b jet #eta",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.09} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "MET_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "MET_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "MET_AfterAllSelections",
        details          = { "xlabel": "E_{T}^{miss}",
                             "ylabel": "Events/^{}#DeltaE_{T}^{miss}",
                             "divideByBinWidth": True,
                             "unit": "GeV",
                             "log": True,
                             "opts": {"ymin": 0.0009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "METPhi_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "METPhi_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "METPhi_AfterAllSelections",
        details          = { "xlabel": "E_{T}^{miss} #phi",
                             "ylabel": "Events/^{}#DeltaE_{T}^{miss}#phi",
                             "divideByBinWidth": True,
                             "unit": "{}^{o}",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.009} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    #ControlPlots.append(ControlPlotInput(
        #title            = "TauPlusMETPt_AfterAllSelections",
        #signalHistoPath  = "ForDataDrivenCtrlPlots",
        #signalHistoName  = "TauPlusMETPt_AfterAllSelections",
        #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        #EWKfakeHistoName  = "TauPlusMETPt_AfterAllSelections",
        #details          = { "xlabel": "p_{T}(#tau + ^{}E_{T}^{miss})",
                             #"ylabel": "Events/^{}#Deltap_{T}",
                             #"divideByBinWidth": True,
                             #"unit": "GeV",
                             #"log": True,
                             #"opts": {"ymin": 0.0009} },
        #blindedRange     = [], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    #for i in range(1,5):
        #ControlPlots.append(ControlPlotInput(
            #title            = "AngularCuts2DJet%d_AfterAllSelections"%i,
            #signalHistoPath  = "ForDataDrivenCtrlPlots",
            #signalHistoName  = "ImprovedDeltaPhiCuts2DJet%dBackToBack"%i,
            #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
            #EWKfakeHistoName  = "ImprovedDeltaPhiCuts2DJet%dBackToBack"%i,
            #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                                #"ylabel": "#Delta#phi(jet_{%d},E_{T}^{miss})"%i,
                                #"divideByBinWidth": False,
                                #"unit": "{}^{o}",
                                #"log": False,
                                #"legendPosition": "NW",
                                #"opts": {"zmin": 0.0} },
            #blindedRange     = [], # specify range min,max if blinding applies to this control plot
            #evaluationRange  = [], # specify range to be evaluated and saved into a file
            #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
        #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "AngularCuts2DMinimum_AfterAllSelections",
        #signalHistoPath  = "ForDataDrivenCtrlPlots",
        #signalHistoName  = "ImprovedDeltaPhiCuts2DMinimum",
        #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        #EWKfakeHistoName  = "ImprovedDeltaPhiCuts2DMinimum",
        #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                              #"ylabel": "#Delta#phi(jet_{1..3},E_{T}^{miss})",
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": False,
                            #"legendPosition": "NW",
                            #"opts": {"zmin": 0.0} },
        #blindedRange     = [], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    ControlPlots.append(ControlPlotInput(
        title            = "DeltaPhiTauMet_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "DeltaPhiTauMet_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "DeltaPhiTauMet_AfterAllSelections",
        details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                              "ylabel": "Events",
                            "divideByBinWidth": False,
                            "unit": "{}^{o}",
                            "log": True,
                            "legendPosition": "NW",
                            "opts": {"ymin": 0.9} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))

    #ControlPlots.append(ControlPlotInput(
        #title            = "MinDeltaPhiTauJet_AfterAllSelections",
        #signalHistoPath  = "ForDataDrivenCtrlPlots",
        #signalHistoName  = "MinDeltaPhiTauJet_AfterAllSelections",
        #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        #EWKfakeHistoName  = "MinDeltaPhiTauJet_AfterAllSelections",
        #details          = { "xlabel": "min (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                              #"ylabel": "Events",
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": True,
                            #"legendPosition": "NW",
                            #"opts": {"ymin": 0.9} },
        #blindedRange     = [], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "MaxDeltaPhiTauJet_AfterAllSelections",
        #signalHistoPath  = "ForDataDrivenCtrlPlots",
        #signalHistoName  = "MaxDeltaPhiTauJet_AfterAllSelections",
        #EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        #EWKfakeHistoName  = "MaxDeltaPhiTauJet_AfterAllSelections",
        #details          = { "xlabel": "max (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                              #"ylabel": "Events",
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": True,
                            #"legendPosition": "NW",
                            #"opts": {"ymin": 0.9} },
        #blindedRange     = [], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "DeltaPhi_AfterAllSelections",
        #signalHistoPath  = "",
        #signalHistoName  = "deltaPhi_AfterAllSelections",
        #EWKfakeHistoPath  = "",
        #EWKfakeHistoName  = "EWKFakeTausDeltaPhi_AfterAllSelections",
        #details          = { "bins": 11,
                             #"rangeMin": 0.0,
                             #"rangeMax": 180.0,
                             #"variableBinSizeLowEdges": [0., 10., 20., 30., 40., 60., 80., 100., 120., 140., 160.], # if an empty list is given, then uniform bin width is used
                             #"binLabels": [], # leave empty to disable bin labels
                             #"xlabel": "#Delta#phi(#tau_{h},^{}E_{T}^{miss})",
                             #"ylabel": "Events",
                             #"unit": "^{o}",
                             #"log": True,
                             #"DeltaRatio": 0.5,
                             #"ymin": 0.9,
                             #"ymax": -1},
        #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "^{}N_{b jets}", # Leave blank if you don't want to include the item to the selection flow plot
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
                             #"xlabel": "max(#Delta#phi(jet,^{}E_{T}^{miss})",
                             #"ylabel": "Events",
                             #"unit": "^{o}",
                             #"log": True,
                             #"DeltaRatio": 0.5,
                             #"ymin": 0.9,
                             #"ymax": -1},
        #blindedRange     = [-1, 300], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "#Delta#phi(^{}#tau_{h},^{}E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
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

    ControlPlots.append(ControlPlotInput(
        title            = "BackToBackAngularCutsMinimum_AfterAllSelections",
        signalHistoPath  = "ForDataDrivenCtrlPlots",
        signalHistoName  = "BackToBackAngularCutsMinimum_AfterAllSelections",
        EWKfakeHistoPath  = "ForDataDrivenCtrlPlotsEWKFakeTaus",
        EWKfakeHistoName  = "BackToBackAngularCutsMinimum_AfterAllSelections",
        details          = { #"xlabel": "min(#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..3},MET)^{2}})",
                             "xlabel": "R_{bb}^{min}",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "^{o}",
                             "log": True,
                             "legendPosition": "NE",
                             "opts": {"ymin": 0.09} },
        blindedRange     = [], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
