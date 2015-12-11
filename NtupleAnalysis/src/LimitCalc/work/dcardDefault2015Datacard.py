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
#OptionGenuineTauBackgroundSource = "DataDriven"                        # EWK+tt genuine taus from embedding
OptionGenuineTauBackgroundSource = "MC_FakeAndGenuineTauNotSeparated"   # EWK+tt genuine taus from MC

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
OptionAddSingleTopDependencyForMuParameter = False # Affects only light H+, 2012 only
OptionAddSingleTopSignal = False # Affects only light H+, 2012 only

# Convert the following nuisances from shape to constant
OptionConvertFromShapeToConstantList = ["trg_tau","trg_tau_dataeff","trg_tau_MCeff","trg_L1ETM_dataeff","trg_L1ETM_MCeff","trg_L1ETM","trg_muon_dataeff", # triggers
                                        #"tau_ID_shape", # tau ID
                                        "tau_ID_eToTauEndcap_shape", # tau mis-ID
                                        #"tau_ID_eToTauBarrel_shape", "tau_ID_muToTau_shape", "tau_ID_jetToTau_shape", # other tau mis-ID
                                        "ES_jets","JER","ES_METunclustered", # jet, MET
                                        #"ES_taus", # tau ES
                                        #"b_tag", "b_tag_genuinetau", # btag
                                        "Emb_mu_ID", "Emb_WtauTomu", # embedding-specific
                                        #"Emb_reweighting", # other embedding-specific
                                        #"QCD_metshape", # multijets specific
                                        #"top_pt", # top pt reweighting
                                        "pileup", "pileup_genuinetau", # pileup
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
shapeHistoName = None
histoPathInclusive = "ForDataDrivenCtrlPlots"
histoPathGenuineTaus = "ForDataDrivenCtrlPlotsEWKGenuineTaus"
histoPathFakeTaus = "ForDataDrivenCtrlPlotsEWKFakeTaus"

if OptionMassShape == "TransverseMass":
    shapeHistoName = "shapeTransverseMass"
    #shapeHisto = "ForDataDrivenCtrlPlotsEWKGenuineTaus/shapeTransverseMass"
elif OptionMassShape == "FullMass":
    raise Exception("Does not work")
    shapeHistoName = "shapeInvariantMass"
    #FakeShapeOtherHisto = "shapeEWKFakeTausInvariantMass"
    #FakeShapeTTbarHisto = FakeShapeOtherHisto
elif OptionMassShape == "TransverseAndFullMass2D": # FIXME: preparing to add support, not yet working
    raise Exception("Does not work")
    shapeHistoName = "shapetransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    #FakeShapeOtherHisto = "shapeEWKFakeTausTransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    #FakeShapeTTbarHisto = FakeShapeOtherHisto
ShapeHistogramsDimensions = systematics.getBinningForPlot(shapeHistoName)

DataCardName += "_"+OptionMassShape.replace("TransverseMass","mT").replace("FullMass","invMass")

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from HiggsAnalysis.LimitCalc.InputClasses import ObservationInput
Observation = ObservationInput(datasetDefinition="Data",
                               shapeHistoName=shapeHistoName,
                               histoPath=histoPathInclusive)
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
myFakeShapeSystematics = [] # FIXME

##############################################################################
# DataGroup (i.e. columns in datacard) definitions
#
from HiggsAnalysis.LimitCalc.InputClasses import DataGroup
DataGroups = []
EmbeddingIdList = []
EWKFakeIdList = []

signalTemplate = DataGroup(datasetType="Signal",
                           histoPath=histoPathInclusive,
                           shapeHistoName=shapeHistoName)

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
    #shapeHistoName = shapeHistoName,
#)
#if OptionMassShape == "TransverseMass":
    #myQCD.setDatasetDefinition("QCDinvertedmt")
#elif OptionMassShape == "FullMass":
    #myQCD.setDatasetDefinition("QCDinvertedinvmass")

myQCD = DataGroup(
    label        = "QCDinv",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD inverted",
    datasetDefinition = "QCDMeasurementMT",
    nuisances    = myQCDShapeSystematics[:]+["QCDinvTemplateFit"],#+"xsect_tt_forQCD","QCDinvTemplateFit","lumi_forQCD"
    #datasetType  = "QCD MC",
    #datasetDefinition = "QCD",
    #nuisances    = myShapeSystematics[:]+["b_tag","xsect_QCD","lumi"],
    shapeHistoName = shapeHistoName,
    histoPath = histoPathInclusive,
)

DataGroups.append(myQCD)

if OptionGenuineTauBackgroundSource == "DataDriven":
    # EWK genuine taus from embedding
    myEmbDataDrivenNuisances = ["Emb_QCDcontam","Emb_hybridCaloMET","Emb_reweighting"]
    # EWK + ttbar with genuine taus
    EmbeddingIdList = [3]
    DataGroups.append(DataGroup(
        label        = "EWK_Tau",
        landsProcess = 1,
        shapeHistoName = shapeHistoName,
        histoPath = histoPathInclusive,
        datasetType  = "Embedding",
        #datasetDefinition   = ["SingleMu"],
        datasetDefinition   = "Data",
        validMassPoints = MassPoints,
        #additionalNormalisation = 0.25, # not needed anymore
        nuisances    = myEmbeddingShapeSystematics[:]+myEmbDataDrivenNuisances[:]
        #nuisances    = ["trg_tau_embedding","tau_ID","ES_taus","Emb_QCDcontam","Emb_WtauTomu","Emb_musel_ditau_mutrg","stat_Emb"]
    ))
else:
    # EWK genuine taus from MC
    DataGroups.append(DataGroup(
        label        = "tt_EWK_faketau",
        landsProcess = 4,
        shapeHistoName = shapeHistoName,
        histoPath    = histoPathGenuineTaus,
        datasetType  = "Embedding",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_genuinetau", "mu_veto_genuinetau","b_tag_genuinetau","top_pt","xsect_tt","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "W_EWK_faketau",
        landsProcess = 5,
        shapeHistoName = shapeHistoName,
        histoPath    = histoPathGenuineTaus,
        datasetType  = "Embedding",
        datasetDefinition = "WJetsHT",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_genuinetau", "mu_veto_genuinetau","b_tag_genuinetau","xsect_Wjets","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "t_EWK_faketau",
        landsProcess = 6,
        shapeHistoName = shapeHistoName,
        histoPath    = histoPathGenuineTaus,
        datasetType  = "Embedding",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_genuinetau", "mu_veto_genuinetau","b_tag_genuinetau","xsect_singleTop","lumi","probBtag"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_EWK_faketau",
        landsProcess = 7,
        shapeHistoName = shapeHistoName,
        histoPath    = histoPathGenuineTaus,
        datasetType  = "Embedding",
        datasetDefinition   = "DYJetsToLLHT",
        validMassPoints = MassPoints,
        nuisances    = myFakeShapeSystematics[:]+["e_veto_genuinetau", "mu_veto_genuinetau","b_tag_genuinetau","xsect_DYtoll","lumi","probBtag"],
    ))
    #DataGroups.append(DataGroup(
        #label        = "VV_EWK_faketau",
        #landsProcess = 8,
        #shapeHistoName = shapeHistoName,
        #histoPath    = histoPathGenuineTaus,
        #datasetType  = "Embedding",
        #datasetDefinition   = "Diboson",
        #validMassPoints = MassPoints,
        #nuisances    = myFakeShapeSystematics[:]+["e_veto_genuinetau", "mu_veto_genuinetau","b_tag_genuinetau","xsect_VV","lumi","probBtag"],
    #))
  
    # Merge EWK as one column or not
    #if not OptionSeparateFakeTtbarFromFakeBackground:
        #mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    #else:
        #mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})

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
    id            = "e_veto_genuinetau",
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
    id            = "mu_veto_genuinetau",
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
    id            = "b_tag_genuinetau",
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
    id            = "b_mistag_genuinetau",
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
    id            = "pileup_genuinetau",
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
            #id            = "b_tag_genuinetau",
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
            ##id            = "b_mistag_genuinetau",
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
            #id            = "b_tag_genuinetau",
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
            #id            = "b_tag_genuinetau",
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
        #id            = "e_veto_genuinetau",
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
        #id            = "mu_veto_genuinetau",
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
            #id            = "pileup_genuinetau",
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
            #id            = "pileup_genuinetau",
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
#MergeNuisances.append(["ES_taus","ES_taus_genuinetau","ES_taus_tempForEmbedding"])
#MergeNuisances.append(["ES_jets","ES_jets_genuinetau"])
#MergeNuisances.append(["JER","JER_genuinetau"])
#MergeNuisances.append(["ES_METunclustered","ES_METunclustered_genuinetau"])
MergeNuisances.append(["e_veto", "e_veto_genuinetau"])
MergeNuisances.append(["mu_veto", "mu_veto_genuinetau"])
MergeNuisances.append(["b_tag","b_tag_genuinetau"])
MergeNuisances.append(["b_mistag","b_mistag_genuinetau"])
MergeNuisances.append(["pileup","pileup_genuinetau"])
MergeNuisances.append(["xsect_tt", "xsect_tt_forQCD"])
MergeNuisances.append(["lumi", "lumi_forQCD"])

from HiggsAnalysis.LimitCalc.InputClasses import convertFromSystVariationToConstant
convertFromSystVariationToConstant(Nuisances, OptionConvertFromShapeToConstantList)

from HiggsAnalysis.LimitCalc.InputClasses import separateShapeAndNormalizationFromSystVariation
separateShapeAndNormalizationFromSystVariation(Nuisances, OptionSeparateShapeAndNormalizationFromSystVariationList)

# Control plots
from HiggsAnalysis.LimitCalc.InputClasses import ControlPlotInput
ControlPlots = []
#EWKPath = "ForDataDrivenCtrlPlotsEWKFakeTaus"
EWKPath = "ForDataDrivenCtrlPlotsEWKGenuineTaus"

#ControlPlots.append(ControlPlotInput(
    #title            = "WeightedCounters",
    #histoName        = "counter",
    #details          = { "xlabel": "",
                         #"xlabelsize": 10,
                         #"ylabel": "Events",
                         #"divideByBinWidth": False,
                         #"unit": "",
                         #"log": True,
                         #"opts": {"ymin": 0.0009} },
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "NVertices_AfterStandardSelections",
    #histoName        = "NVertices_AfterStandardSelections",
    #details          = { "xlabel": "N_{vertices}",
                         #"ylabel": "Events",
                         #"divideByBinWidth": False,
                         #"unit": "",
                         #"log": True,
                         #"opts": {"ymin": 0.0009} },
#))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_pT_AfterStandardSelections",
    histoName        = "SelectedTau_pT_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.0009} },
))

#ControlPlots.append(ControlPlotInput(
    #title            = "SelectedTau_p_AfterStandardSelections",
    #histoName        = "SelectedTau_p_AfterStandardSelections",
    #details          = { "xlabel": "Selected #tau p",
                         #"ylabel": "Events/#Deltap",
                         #"divideByBinWidth": True,
                         #"unit": "GeV/c",
                         #"log": True,
                         #"opts": {"ymin": 0.009} },
#))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_eta_AfterStandardSelections",
    histoName        = "SelectedTau_eta_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau #eta",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.009} },
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_phi_AfterStandardSelections",
    histoName        = "SelectedTau_phi_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau #phi",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.009} },
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_ldgTrkPt_AfterStandardSelections",
    histoName        = "SelectedTau_ldgTrkPt_AfterStandardSelections",
    details          = { "xlabel": "#tau leading track ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.0009} },
))

#ControlPlots.append(ControlPlotInput(
    #title            = "SelectedTau_LeadingTrackP_AfterStandardSelections",
    #histoName        = "SelectedTau_LeadingTrackP_AfterStandardSelections",
    #details          = { "xlabel": "#tau leading track p",
                         #"ylabel": "Events/#Deltap",
                         #"divideByBinWidth": True,
                         #"unit": "GeV/c",
                         #"log": True,
                         #"ratioLegendPosition": "right",
                         #"opts": {"ymin": 0.0009} },
#))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_Rtau_AfterStandardSelections",
    histoName        = "SelectedTau_Rtau_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau ^{}R_{#tau}",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SE",
                         "opts": {"ymin": 0.009} },
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_DecayMode_AfterStandardSelections",
    histoName        = "SelectedTau_DecayMode_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau Decay mode",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.9} },
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_Nprongs_AfterStandardSelections",
    histoName        = "SelectedTau_Nprongs_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau N_{prongs}",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.9} },
))

ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_source_AfterStandardSelections",
    histoName        = "SelectedTau_source_AfterStandardSelections",
    details          = { "xlabel": "",
                         "ylabel": "Events",
                         "xlabelsize": 10,
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.9} },
))

ControlPlots.append(ControlPlotInput(
    title            = "NjetsAfterJetSelectionAndMETSF",
    histoName        = "NjetsAfterJetSelectionAndMETSF",
    details          = { "xlabel": "Number of selected jets",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "opts": {"ymin": 0.9} },
    flowPlotCaption  = "^{}#tau_{h}+#geq3j", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "JetPt_AfterStandardSelections",
    histoName        = "JetPt_AfterStandardSelections",
    details          = { "xlabel": "jet ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.009} },
))

ControlPlots.append(ControlPlotInput(
    title            = "JetEta_AfterStandardSelections",
    histoName        = "JetEta_AfterStandardSelections",
    details          = { "xlabel": "jet #eta",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.09} },
))

ControlPlots.append(ControlPlotInput(
    title            = "CollinearAngularCutsMinimum",
    histoName        = "CollinearAngularCutsMinimum",
    details          = { "xlabel": "R_{coll}^{min}",
        #"xlabel": "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1..3},MET))^{2}})",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SE",
                         "opts": {"ymin": 0.09} },
    flowPlotCaption  = "R_{coll}^{min}", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "BJetSelection",
    histoName        = "NBjets",
    details          = { "xlabel": "Number of selected b jets",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "opts": {"ymin": 0.09} },
    flowPlotCaption  = "#geq1 b tag", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "BtagDiscriminator",
    histoName        = "BtagDiscriminator",
    details          = { "xlabel": "b tag discriminator",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "NE",
                         "opts": {"ymin": 0.9} },
))

ControlPlots.append(ControlPlotInput(
    title            = "BJetPt",
    histoName        = "BJetPt",
    details          = { "xlabel": "b jet ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.0009} },
))

ControlPlots.append(ControlPlotInput(
    title            = "BJetEta",
    histoName        = "BJetEta",
    details          = { "xlabel": "b jet #eta",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.09} },
))


ControlPlots.append(ControlPlotInput(
    title            = "MET",
    histoName        = "MET",
    details          = { "xlabel": "E_{T}^{miss}",
                         "ylabel": "Events/^{}#DeltaE_{T}^{miss}",
                         "divideByBinWidth": True,
                         "unit": "GeV",
                         "log": True,
                         "opts": {"ymin": 0.00009} },
    flowPlotCaption  = "^{}E_{T}^{miss}", # Leave blank if you don't want to include the item to the selection flow plot
))

ControlPlots.append(ControlPlotInput(
    title            = "METPhi",
    histoName        = "METPhi",
    details          = { "xlabel": "E_{T}^{miss} #phi",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.09} },
))

#ControlPlots.append(ControlPlotInput(
    #title            = "TauPlusMETPt",
    #histoName        = "TauPlusMETPt",
    #details          = { "xlabel": "p_{T}(#tau + ^{}E_{T}^{miss})",
                         #"ylabel": "Events/^{}#Deltap_{T}",
                         #"divideByBinWidth": True,
                         #"unit": "GeV",
                         #"log": True,
                         #"opts": {"ymin": 0.0009} },
#))

#for i in range(1,5):
    #ControlPlots.append(ControlPlotInput(
        #title            = "CollinearAngularCuts2DJet%d"%i,
        #histoName        = "ImprovedDeltaPhiCuts2DJet%dCollinear"%i,
        #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                             #"ylabel": "#Delta#phi(jet_{%d},E_{T}^{miss})"%i,
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": False,
                            #"legendPosition": "NW",
                            #"opts": {"zmin": 0.0} },
    #))
    #ControlPlots.append(ControlPlotInput(
        #title            = "BackToBackAngularCuts2DJet%d"%i,
        #histoName        = "ImprovedDeltaPhiCuts2DJet%dBackToBack"%i,
        #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                             #"ylabel": "#Delta#phi(jet_{%d},E_{T}^{miss})"%i,
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": False,
                            #"legendPosition": "NW",
                            #"opts": {"zmin": 0.0} },
    #))

#ControlPlots.append(ControlPlotInput(
    #title            = "CollinearAngularCuts2DMinimum",
    #histoName        = "ImprovedDeltaPhiCuts2DCollinearMinimum",
    #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                          #"ylabel": "#Delta#phi(jet_{1..3},E_{T}^{miss})",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": False,
                        #"legendPosition": "NW",
                        #"opts": {"zmin": 0.0} },
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "BackToBackAngularCuts2DMinimum",
    #histoName        = "ImprovedDeltaPhiCuts2DBackToBackMinimum",
    #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                          #"ylabel": "#Delta#phi(jet_{1..3},E_{T}^{miss})",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": False,
                        #"legendPosition": "NW",
                        #"opts": {"zmin": 0.0} },
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "DeltaPhiTauMet",
    #histoName        = "DeltaPhiTauMet",
    #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                          #"ylabel": "Events",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": True,
                        #"legendPosition": "NW",
                        #"opts": {"ymin": 0.9} },
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "MinDeltaPhiTauJet",
    #histoName        = "MinDeltaPhiTauJet",
    #details          = { "xlabel": "min (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                          #"ylabel": "Events",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": True,
                        #"legendPosition": "NW",
                        #"opts": {"ymin": 0.9} },
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "MaxDeltaPhiTauJet",
    #histoName        = "MaxDeltaPhiTauJet",
    #details          = { "xlabel": "max (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                          #"ylabel": "Events",
                        #"divideByBinWidth": False,
                        #"unit": "{}^{o}",
                        #"log": True,
                        #"legendPosition": "NW",
                        #"opts": {"ymin": 0.9} },
#))


#ControlPlots.append(ControlPlotInput(
    #title            = "DeltaPhi",
    #histoName        = "deltaPhi",
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
    #flowPlotCaption  = "^{}N_{b jets}", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "MaxDeltaPhi",
    #histoName        = "maxDeltaPhiJetMet",
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
    #flowPlotCaption  = "#Delta#phi(^{}#tau_{h},^{}E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "WMass",
    #histoName        = "WMass",
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
    #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
#))

#ControlPlots.append(ControlPlotInput(
    #title            = "TopMass",
    #histoName        = "TopMass",
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
#))


ControlPlots.append(ControlPlotInput(
    title            = "BackToBackAngularCutsMinimum",
    histoName        = "BackToBackAngularCutsMinimum",
    details          = { "xlabel": "^{}R_{bb}^{min}",
    #"xlabel": "min(#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..3},MET)^{2}})",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SE",
                         "opts": {"ymin": 0.09} },
    flowPlotCaption  = "^{}R_{bb}^{min}", # Leave blank if you don't want to include the item to the selection flow plot
))

if OptionMassShape == "TransverseMass":
    ControlPlots.append(ControlPlotInput(
        title            = "TransverseMass",
        histoName        = "shapeTransverseMass",
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
        flowPlotCaption  = "final", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    #ControlPlots.append(ControlPlotInput(
        #title            = "TransverseMassLog",
        #signalhistoPath  = "ForDataDrivenCtrlPlots",
        #histoName        = "shapeTransverseMass",
        #EWKfakehistoPath  = EWKPath,
        #EWKfakeHistoName  = "shapeEWKFakeTausTransverseMass",
        #details          = {"cmsTextPosition": "right",
                            ##"xlabel": "m_{T}(^{}#tau_{h},^{}E_{T}^{miss})",
                            ##"ylabel": "Events/^{}#Deltam_{T}",
                            ##"unit": "GeV",
                            #"xlabel": "m_{T} (GeV)",
                            #"ylabel": "< Events / bin >", "ylabelBinInfo": False,
                            #"moveLegend": {"dx": -0.10, "dy": -0.12, "dh":0.1},
                            #"ratioMoveLegend": {"dx": -0.06, "dy": -0.33},
                            #"divideByBinWidth": True,
                            #"log": True,
                            #"opts": {"ymin": 1e-4},
                            #"opts2": {"ymin": 0.0, "ymax": 2.0}
                           #},
        #blindedRange     = [81, 1000], # specify range min,max if blinding applies to this control plot
        #evaluationRange  = [], # specify range to be evaluated and saved into a file
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))
elif OptionMassShape == "FullMass":
    ControlPlots.append(ControlPlotInput(
        title            = "FullMass",
        histoName        = "shapeInvariantMass",
        details          = { "xlabel": "m(^{}#tau_{h},^{}E_{T}^{miss})",
                             "ylabel": "Events/#Deltam",
                             "divideByBinWidth": True,
                             "unit": "GeV",
                             "log": False,
                             "opts": {"ymin": 0.0},
                             "opts2": {"ymin": 0.0, "ymax": 2.0},
                           },
        blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
        flowPlotCaption  = "final", # Leave blank if you don't want to include the item to the selection flow plot
    ))

if OptionCtrlPlotsAtMt:
    ControlPlots.append(ControlPlotInput(
        title            = "NVertices_AfterAllSelections",
        histoName        = "NVertices_AfterAllSelections",
        details          = { "xlabel": "N_{vertices}",
                            "ylabel": "Events",
                            "divideByBinWidth": False,
                            "unit": "",
                            "log": True,
                            "opts": {"ymin": 0.0009} },
    ))
  
    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_pT_AfterAllSelections",
        histoName        = "SelectedTau_pT_AfterAllSelections",
        details          = { "xlabel": "Selected #tau ^{}p_{T}",
                             "ylabel": "Events/^{}#Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "opts": {"ymin": 0.0009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_eta_AfterAllSelections",
        histoName        = "SelectedTau_eta_AfterAllSelections",
        details          = { "xlabel": "Selected #tau #eta",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_phi_AfterAllSelections",
        histoName        = "SelectedTau_phi_AfterAllSelections",
        details          = { "xlabel": "Selected #tau #phi",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "{}^{o}",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.09} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_ldgTrkPt_AfterAllSelections",
        histoName        = "SelectedTau_ldgTrkPt_AfterAllSelections",
        details          = { "xlabel": "#tau leading track p{}_{T}",
                             "ylabel": "Events/^{}#Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "ratioLegendPosition": "right",
                             "opts": {"ymin": 0.0009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_Rtau_AfterAllSelections",
        histoName        = "SelectedTau_Rtau_AfterAllSelections",
        details          = { "xlabel": "Selected #tau R_{#tau}",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SE",
                             "opts": {"ymin": 0.009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_Rtau_FullRange_AfterAllSelections",
        histoName        = "SelectedTau_Rtau_AfterAllSelections",
        details          = { "xlabel": "Selected #tau R_{#tau}",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts2": {"ymin": 0.2, "ymax": 1.8},
                             "opts": {"ymin": 0.009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_DecayMode_AfterAllSelections",
        histoName        = "SelectedTau_DecayMode_AfterAllSelections",
        details          = { "xlabel": "Selected #tau Decay mode",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "ratioLegendPosition": "right",
                             "opts": {"ymin": 0.9} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_Nprongs_AfterAllSelections",
        histoName        = "SelectedTau_Nprongs_AfterAllSelections",
        details          = { "xlabel": "Selected #tau N_{prongs}",
                            "ylabel": "Events",
                            "divideByBinWidth": False,
                            "unit": "",
                            "log": True,
                            "ratioLegendPosition": "right",
                            "opts": {"ymin": 0.9} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "SelectedTau_source_AfterAllSelections",
        histoName        = "SelectedTau_source_AfterAllSelections",
        details          = { "xlabel": "",
                            "ylabel": "Events",
                            "xlabelsize": 10,
                            "divideByBinWidth": False,
                            "unit": "",
                            "log": True,
                            "ratioLegendPosition": "right",
                            "opts": {"ymin": 0.9} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "Njets_AfterAllSelections",
        histoName        = "Njets_AfterAllSelections",
        details          = { "xlabel": "Number of selected jets",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "opts": {"ymin": 0.9} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "JetPt_AfterAllSelections",
        histoName        = "JetPt_AfterAllSelections",
        details          = { "xlabel": "jet ^{}p_{T}",
                             "ylabel": "Events/^{}Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "opts": {"ymin": 0.009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "JetEta_AfterAllSelections",
        histoName        = "JetEta_AfterAllSelections",
        details          = { "xlabel": "jet #eta",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.09} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "CollinearAngularCutsMinimum_AfterAllSelections",
        histoName        = "CollinearAngularCutsMinimum_AfterAllSelections",
        details          = { "xlabel": "R_{coll}^{min}",
        #"xlabel": "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1..3},MET))^{2}})",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "{}^{o}",
                             "log": True,
                             "legendPosition": "NW",
                             "opts": {"ymin": 0.09} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BJetSelection_AfterAllSelections",
        histoName        = "NBjets_AfterAllSelections",
        details          = { "xlabel": "Number of selected b jets",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "opts": {"ymin": 0.09} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BtagDiscriminator_AfterAllSelections",
        histoName        = "BtagDiscriminator_AfterAllSelections",
        details          = { "xlabel": "b tag discriminator",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "NE",
                             "opts": {"ymin": 0.9} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BJetPt_AfterAllSelections",
        histoName        = "BJetPt_AfterAllSelections",
        details          = { "xlabel": "b jet ^{}p_{T}",
                             "ylabel": "Events/^{}#Deltap_{T}",
                             "divideByBinWidth": True,
                             "unit": "GeV/c",
                             "log": True,
                             "opts": {"ymin": 0.0009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "BJetEta_AfterAllSelections",
        histoName        = "BJetEta_AfterAllSelections",
        details          = { "xlabel": "b jet #eta",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.09} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "MET_AfterAllSelections",
        histoName        = "MET_AfterAllSelections",
        details          = { "xlabel": "E_{T}^{miss}",
                             "ylabel": "Events/^{}#DeltaE_{T}^{miss}",
                             "divideByBinWidth": True,
                             "unit": "GeV",
                             "log": True,
                             "opts": {"ymin": 0.0009} },
    ))

    ControlPlots.append(ControlPlotInput(
        title            = "METPhi_AfterAllSelections",
        histoName        = "METPhi_AfterAllSelections",
        details          = { "xlabel": "E_{T}^{miss} #phi",
                             "ylabel": "Events/^{}#DeltaE_{T}^{miss}#phi",
                             "divideByBinWidth": True,
                             "unit": "{}^{o}",
                             "log": True,
                             "legendPosition": "SW",
                             "opts": {"ymin": 0.009} },
    ))

    #for i in range(1,5):
        #ControlPlots.append(ControlPlotInput(
            #title            = "AngularCuts2DJet%d_AfterAllSelections"%i,
            #histoName        = "ImprovedDeltaPhiCuts2DJet%dBackToBack"%i,
            #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                                #"ylabel": "#Delta#phi(jet_{%d},E_{T}^{miss})"%i,
                                #"divideByBinWidth": False,
                                #"unit": "{}^{o}",
                                #"log": False,
                                #"legendPosition": "NW",
        #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "AngularCuts2DMinimum_AfterAllSelections",
        #histoName        = "ImprovedDeltaPhiCuts2DMinimum",
        #details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                              #"ylabel": "#Delta#phi(jet_{1..3},E_{T}^{miss})",
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": False,
                            #"legendPosition": "NW",
                            #"opts": {"zmin": 0.0} },
    #))

    ControlPlots.append(ControlPlotInput(
        title            = "DeltaPhiTauMet_AfterAllSelections",
        histoName        = "DeltaPhiTauMet_AfterAllSelections",
        details          = { "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                              "ylabel": "Events",
                            "divideByBinWidth": False,
                            "unit": "{}^{o}",
                            "log": True,
                            "legendPosition": "NW",
                            "opts": {"ymin": 0.9} },
    ))

    #ControlPlots.append(ControlPlotInput(
        #title            = "MinDeltaPhiTauJet_AfterAllSelections",
        #histoName        = "MinDeltaPhiTauJet_AfterAllSelections",
        #details          = { "xlabel": "min (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                              #"ylabel": "Events",
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": True,
                            #"legendPosition": "NW",
                            #"opts": {"ymin": 0.9} },
    #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "MaxDeltaPhiTauJet_AfterAllSelections",
        #histoName        = "MaxDeltaPhiTauJet_AfterAllSelections",
        #details          = { "xlabel": "max (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
                              #"ylabel": "Events",
                            #"divideByBinWidth": False,
                            #"unit": "{}^{o}",
                            #"log": True,
                            #"legendPosition": "NW",
                            #"opts": {"ymin": 0.9} },
    #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "DeltaPhi_AfterAllSelections",
        #histoName        = "deltaPhi_AfterAllSelections",
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
        #flowPlotCaption  = "^{}N_{b jets}", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "MaxDeltaPhi",
        #histoName        = "maxDeltaPhiJetMet",
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
        #flowPlotCaption  = "#Delta#phi(^{}#tau_{h},^{}E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "WMass",
        #histoName        = "WMass",
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
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    #ControlPlots.append(ControlPlotInput(
        #title            = "TopMass",
        #histoName        = "TopMass",
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
        #flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    #))

    ControlPlots.append(ControlPlotInput(
        title            = "BackToBackAngularCutsMinimum_AfterAllSelections",
        histoName        = "BackToBackAngularCutsMinimum_AfterAllSelections",
        details          = { #"xlabel": "min(#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..3},MET)^{2}})",
                             "xlabel": "R_{bb}^{min}",
                             "ylabel": "Events",
                             "divideByBinWidth": False,
                             "unit": "^{o}",
                             "log": True,
                             "legendPosition": "NE",
                             "opts": {"ymin": 0.09} },
    ))
