import NtupleAnalysis.toolssystematics as systematics

DataCardName    = 'Default_8TeV'
#Path = "/home/wendland/data/v533/2014-01-29-noMetSF-withL1ETMfix"#2014-01-29-noMetSF-withL1ETMfix"
#Path = "/home/wendland/data/v533/2014_02_14_v3_etacorrected"
#Path = "/home/wendland/data/v533/2014-03-20"
#Path = "/home/wendland/data/v533/2014-03-20_expCtrlPlots"
#Path = "/home/wendland/data/v533/2014-04-14_nominal_norm5GeVLRB"
#Path = "/home/wendland/data/xnortau"
#Path = "/home/wendland/data/test_nominal_dphi"
#Path = "/home/wendland/data/xnominal"
#Path = "/home/wendland/data/test_2014-09-05"
#Path = "/home/wendland/data/xnominal"
#Path = "/home/wendland/data/test_matti_met60_paramweight"
#Path = "/home/wendland/data/v533/2014-03-20_optTau60Met80_mt20gev"
#Path = "/home/wendland/data/v533/2014-03-20_METprecut30"
#Path = "/home/wendland/data/v533/2014_03_12_metphicorrected"
#Path = "/home/wendland/data/v533/2014_02_14_v3_decaymode1"
#Path            = '/home/wendland/data/v445/met50rtaunprongs'
#Path            = '/mnt/flustre/slehti/hplusAnalysis/QCDInverted/CMSSW_4_4_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/datacardGenerator/TESTDATA/'
Path = "/mnt/flustre/epekkari/FakeTauDatacard"

LightMassPoints      = [80,90,100,120,140,150,155,160]
#LightMassPoints      = [80,120,160]
#LightMassPoints      = [120]
#LightMassPoints      = []

HeavyMassPoints      = [180,190,200,220,250,300,400,500,600] # mass points 400-600 are not available for 2011 branch
#HeavyMassPoints      = [180,220,300,600]
#HeavyMassPoints      = [300]
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
OptionGenuineTauBackgroundSource = "DataDriven"                          # State-of-the-art: embedded data used (use for optimization and results)
#OptionGenuineTauBackgroundSource = "MC_FakeAndGenuineTauNotSeparated" # MC used, fake taus are not separated from genuine taus
#OptionGenuineTauBackgroundSource = "MC_FullSystematics"               # MC used, fake and genuine taus separated (use for embedding closure test)
#OptionGenuineTauBackgroundSource = "MC_RealisticProjection"            # MC used, fake and genuine taus separated (can be used for optimization)

OptionSeparateFakeTtbarFromFakeBackground = False # NOTE: this flag should be put true for light H+ and to false for heavy H+

OptionRealisticEmbeddingWithMC = True # Only relevant for OptionReplaceEmbeddingByMC==True
OptionTreatTriggerUncertaintiesAsAsymmetric = True # Set to true, if you produced multicrabs with doAsymmetricTriggerUncertainties=True
OptionTreatTauIDAndMisIDSystematicsAsShapes = True # Set to true, if you produced multicrabs with doTauIDandMisIDSystematicsAsShapes=True
OptionIncludeSystematics = True # Set to true if you produced multicrabs with doSystematics=True

OptionPurgeReservedLines = True # Makes limit running faster, but cannot combine leptonic datacards
OptionDoControlPlots = True #False 
OptionDoMergeFakeTauColumns = True # Merges the fake tau columns into one
OptionCombineSingleColumnUncertainties = not True # Makes limit running faster
OptionCtrlPlotsAtMt = True # Produce control plots after all selections (all selections for transverse mass)
OptionDisplayEventYieldSummary = True
OptionNumberOfDecimalsInSummaries = 1
OptionRemoveHHDataGroup = True
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

# Separate in the following shape nuisances the shape and normalization components
OptionSeparateShapeAndNormalizationFromSystVariationList = [
                                                            #"ES_taus"
                                                           ]

# For projections
trg_MET_dataeffScaleFactor = None # Default is None, i.e. 1.0

# Options for reports and article
OptionBr = 0.01  # Br(t->bH+)
OptionSqrtS = 8 # sqrt(s)

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
    SignalShapeHisto = "shapeTransverseMass"
    FakeShapeTTbarHisto = "shapeEWKFakeTausTransverseMass"
    FakeShapeOtherHisto = "shapeProbabilisticBtagEWKFakeTausTransverseMass"
elif OptionMassShape == "FullMass":
    SignalShapeHisto = "shapeInvariantMass"
    FakeShapeOtherHisto = "shapeEWKFakeTausInvariantMass"
    FakeShapeTTbarHisto = FakeShapeOtherHisto
elif OptionMassShape == "TransverseAndFullMass2D": # FIXME: preparing to add support, not yet working
    SignalShapeHisto = "shapetransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    FakeShapeOtherHisto = "shapeEWKFakeTausTransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    FakeShapeTTbarHisto = FakeShapeOtherHisto
ShapeHistogramsDimensions = systematics.getBinningForPlot(SignalShapeHisto)

DataCardName += "_"+OptionMassShape.replace("TransverseMass","mT").replace("FullMass","invMass")

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from LimitCalcInputClasses import ObservationInput
Observation = ObservationInput(datasetDefinition="Data",
                               shapeHisto=SignalShapeHisto)
#Observation.setPaths(signalPath,signalDataPaths)

##############################################################################
# Systematics lists
myTrgShapeSystematics = []
if OptionTreatTriggerUncertaintiesAsAsymmetric:
    myTrgShapeSystematics = ["trg_tau_dataeff","trg_tau_MCeff","trg_L1ETM_dataeff","trg_L1ETM_MCeff"] # Variation done separately for data and MC efficiencies
else:
    myTrgShapeSystematics = ["trg_tau","trg_L1ETM"] # Variation of trg scale factors

myTauIDShapeSystematics = []
if OptionTreatTauIDAndMisIDSystematicsAsShapes:
    myTauIDShapeSystematics = ["tau_ID_shape","tau_ID_eToTauBarrel_shape","tau_ID_eToTauEndcap_shape","tau_ID_muToTau_shape","tau_ID_jetToTau_shape"] # tau ID and mis-ID systematics done with shape variation
else:
    myTauIDShapeSystematics = ["tau_ID"] # tau ID and mis-ID systematics done with constants

myShapeSystematics = []
myShapeSystematics.extend(myTrgShapeSystematics)
myShapeSystematics.extend(myTauIDShapeSystematics)
myShapeSystematics.extend(["ES_taus","ES_jets","JER","ES_METunclustered","pileup"]) # btag is not added, because it has the tag and mistag categories

myEmbeddingMETUncert = "trg_L1ETM"
if OptionTreatTriggerUncertaintiesAsAsymmetric:
    myEmbeddingMETUncert += "_dataeff"
    myEmbeddingShapeSystematics = ["trg_tau_dataeff",myEmbeddingMETUncert,"trg_muon_dataeff","ES_taus","Emb_mu_ID","Emb_WtauTomu"]
else:
    myEmbeddingShapeSystematics = ["trg_tau",myEmbeddingMETUncert,"trg_muon","ES_taus","Emb_mu_ID","Emb_WtauTomu"]
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

##############################################################################
# DataGroup (i.e. columns in datacard) definitions
#
from LimitCalcInputClasses import DataGroup
DataGroups = []
EmbeddingIdList = []
EWKFakeIdList = []

signalTemplate = DataGroup(datasetType="Signal",
                           shapeHisto=SignalShapeHisto)

mergeColumnsByLabel = []

for mass in LightMassPoints:
    myMassList = [mass]
    hhx = signalTemplate.clone()
    hhx.setLabel("HH"+str(mass)+"_a")
    hhx.setLandSProcess(-1)
    hhx.setValidMassPoints(myMassList)
    hhx.setNuisances(myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_tt_8TeV","lumi"])
    hhx.setDatasetDefinition("TTToHplusBHminusB_M"+str(mass))
    DataGroups.append(hhx)

    hwx = signalTemplate.clone()
    hwx.setLabel("HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_tt_8TeV","lumi"])
    hwx.setDatasetDefinition("TTToHplusBWB_M"+str(mass))
    DataGroups.append(hwx)
    
    if OptionAddSingleTopSignal:
        mySuffix = ["s","t","tW"]
        myLabelList = []
        for i in range(0,len(mySuffix)):
            hst = signalTemplate.clone()
            label = "HST%d_%s"%(mass, mySuffix[i])
            myLabelList.append(label)
            hst.setLabel(label)
            hst.setLandSProcess(-2)
            hst.setValidMassPoints(myMassList)
            hst.setNuisances(myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_singleTop","lumi"])
            hst.setDatasetDefinition("Hplus_taunu_%s-channel_M%d"%(mySuffix[i],mass))
            DataGroups.append(hst)
        mergeColumnsByLabel.append({"label": label.replace("_%s"%mySuffix[i],""), "mergeList": myLabelList[:]})

for mass in HeavyMassPoints:
    myMassList = [mass]
    hx = signalTemplate.clone()
    hx.setLabel("Hp"+str(mass)+"_a")
    hx.setLandSProcess(0)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(myShapeSystematics[:]+["e_mu_veto","b_tag","lumi"])
    if not OptionDoTBbarForHeavy:
        hx.setDatasetDefinition("HplusTB_M"+str(mass))
    else:
        hx.setDatasetDefinition("HplusToTBbar_M"+str(mass))
    DataGroups.append(hx)

myQCDShapeSystematics = myShapeSystematics[:]
#for i in range(0,len(myQCDShapeSystematics)):
    #if myQCDShapeSystematics[i].startswith("trg_CaloMET") and not "forQCD" in myQCDShapeSystematics[i]:
    #    myQCDShapeSystematics[i] = myQCDShapeSystematics[i]+"_forQCD"

myQCDFact = DataGroup(
    label        = "QCDfact",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD factorised",
    datasetDefinition = "QCDfactorisedmt",
    nuisances    = myQCDShapeSystematics[:]+["b_tag","top_pt","QCD_metshape","xsect_tt_8TeV_forQCD","lumi_forQCD"],
    shapeHisto   = SignalShapeHisto,
)

myQCDInv = DataGroup(
    label        = "QCDinv",
    landsProcess = 3,
    validMassPoints = MassPoints,
    datasetType  = "QCD inverted",
    datasetDefinition = "QCDinvertedmt",
    nuisances    = myQCDShapeSystematics[:]+["b_tag","top_pt","QCD_metshape","xsect_tt_8TeV_forQCD","QCDinvTemplateFit","lumi_forQCD","fakerateprob_weighting","probabilistic_Btag","lepton_veto_forFakeTau", "normalizationAfterCollinearCuts"],
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
    # if not OptionSeparateFakeTtbarFromFakeBackground:
    #     mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    # else:
    #     mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    # DataGroups.append(DataGroup(
    #     label        = "tt_EWK_faketau",
    #     landsProcess = 4,
    #     shapeHisto   = FakeShapeTTbarHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition = "TTJets",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","top_pt","xsect_tt_8TeV","lumi"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "W_EWK_faketau",
    #     landsProcess = 5,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition = "WJets",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_Wjets","lumi","probBtag"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "t_EWK_faketau",
    #     landsProcess = 6,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition = "SingleTop",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","probBtag"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "DY_EWK_faketau",
    #     landsProcess = 7,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition   = "DYJetsToLL",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_DYtoll","lumi","probBtag"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "VV_EWK_faketau",
    #     landsProcess = 8,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition   = "Diboson",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_VV","lumi","probBtag"],
    # ))
elif OptionGenuineTauBackgroundSource == "MC_FullSystematics" or OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
    # Mimic embedding with MC analysis (introduces double counting of EWK fakes, but that should be small effect)
    myEmbeddingShapeSystematics = []
    mergeColumnsByLabel.append({"label": "MC_EWKTau", "mergeList": ["pseudo_emb_TTJets_MC","pseudo_emb_Wjets_MC","pseudo_emb_t_MC","pseudo_emb_DY_MC","pseudo_emb_VV_MC"], 
                                "subtractList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    if OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
        # Mimic with uncertainties the outcome of data-driven embedding
        if OptionTreatTriggerUncertaintiesAsAsymmetric:
            myEmbeddingShapeSystematics.append("trg_tau_dataeff")
            myEmbeddingShapeSystematics.append("trg_L1ETM_dataeff")
        else:
            myEmbeddingShapeSystematics.append("trg_tau")
            myEmbeddingShapeSystematics.append("trg_L1ETM")
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
        myEmbeddingShapeSystematics = myShapeSystematics[:]+["top_pt","e_mu_veto","b_tag","xsect_tt_8TeV","lumi"]
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
    # mergeColumnsByLabel.append({"label": "MC_EWKFakeTau", "mergeList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    # DataGroups.append(DataGroup(
    #     label        = "tt_EWK_faketau",
    #     landsProcess = 4,
    #     shapeHisto   = FakeShapeTTbarHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition = "TTJets",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","top_pt","xsect_tt_8TeV","lumi"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "W_EWK_faketau",
    #     landsProcess = 5,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition = "WJets",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_Wjets","lumi","probBtag"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "t_EWK_faketau",
    #     landsProcess = 6,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition = "SingleTop",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_singleTop","lumi","probBtag"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "DY_EWK_faketau",
    #     landsProcess = 7,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition   = "DYJetsToLL",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_DYtoll","lumi","probBtag"],
    # ))
    # DataGroups.append(DataGroup(
    #     label        = "VV_EWK_faketau",
    #     landsProcess = 8,
    #     shapeHisto   = FakeShapeOtherHisto,
    #     datasetType  = "EWKfake",
    #     datasetDefinition   = "Diboson",
    #     validMassPoints = MassPoints,
    #     nuisances    = myFakeShapeSystematics[:]+["e_mu_veto_fakes","b_tag_fakes","xsect_VV","lumi","probBtag"],
    # ))
elif OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
    # Replace embedding and fakes with MC
    myList = ["Wjets_MC","DY_MC","VV_MC"]
    if OptionDoMergeFakeTauColumns:
        if not OptionAddSingleTopDependencyForMuParameter:
            myList.append("sngltop_MC")
            mergeColumnsByLabel.append({"label": "EWKnontop_MC", "mergeList": myList[:]})
        else:
            mergeColumnsByLabel.append({"label": "EWKnontt_MC", "mergeList": myList[:]})
    DataGroups.append(DataGroup(
        label        = "ttbar_MC",
        landsProcess = 1,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "TTJets",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_tag","top_pt","xsect_tt_8TeV","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "Wjets_MC",
        landsProcess = 4,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "WJets",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_Wjets","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "sngltop_MC",
        landsProcess = 5,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "SingleTop",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_singleTop","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "DY_MC",
        landsProcess = 6,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "DYJetsToLL",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_DYtoll","lumi"],
    ))
    DataGroups.append(DataGroup(
        label        = "VV_MC",
        landsProcess = 7,
        shapeHisto   = SignalShapeHisto,
        datasetType  = "Embedding",
        datasetDefinition = "Diboson",
        validMassPoints = MassPoints,
        nuisances    = myShapeSystematics[:]+["e_mu_veto","b_tag","xsect_VV","lumi"],
    ))
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
from LimitCalcInputClasses import Nuisance
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

if OptionIncludeSystematics:
    if OptionTreatTriggerUncertaintiesAsAsymmetric:
        Nuisances.append(Nuisance(
            id            = "trg_L1ETM_dataeff",
            label         = "tau+MET trg L1ETM data eff.",
            distr         = "shapeQ",
            function      = "ShapeVariation",
            systVariation = "L1ETMDataEff",
        ))
        Nuisances.append(Nuisance(
            id            = "trg_L1ETM_MCeff",
            label         = "tau+MET trg L1ETM MC eff.",
            distr         = "shapeQ",
            function      = "ShapeVariation",
            systVariation = "L1ETMMCEff",
        ))
    else:
        Nuisances.append(Nuisance(
            id            = "trg_L1ETM",
            label         = "tau+MET trg L1ETM",
            distr         = "shapeQ",
            function      = "ShapeVariation",
            systVariation = "L1ETMSF",
        ))

if OptionGenuineTauBackgroundSource == "DataDriven":
    if OptionTreatTriggerUncertaintiesAsAsymmetric:
        Nuisances.append(Nuisance(
            id            = "trg_muon_dataeff",
            label         = "SingleMu trg data eff.",
            distr         = "shapeQ",
            function      = "ShapeVariation",
            systVariation = "MuonTrgDataEff",
        ))
    else:
        Nuisances.append(Nuisance(
            id            = "trg_muon",
            label         = "SingleMu trg data eff.",
            distr         = "lnN",
            function      = "Constant",
            value         = 0.02,
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

#Nuisances.append(Nuisance(
    #id            = "tau_ID_constShape",
    #label         = "tau-jet ID (no Rtau)",
    #distr         = "shapeQ",
    #function      = "ConstantToShape",
    #value         = systematics.getTauIDUncertainty(isGenuineTau=True)
#))

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
    #Nuisances.append(Nuisance(
        #id            = "b_mistag",
        #label         = "mistagging",
        #distr         = "shapeQ",
        #function      = "ShapeVariation",
        #systVariation = "BTagSF",
    #))
    #Nuisances.append(Nuisance(
        #id            = "b_mistag_fakes",
        #label         = "mistagging EWK fake taus",
        #distr         = "shapeQ",
        #function      = "ShapeVariation",
        #systVariation = "BTagSF",
    #))
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
        id            = "b_tag",
        label         = "NON-EXACT VALUE for mistagging",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.05,
    ))
    Nuisances.append(Nuisance(
        id            = "b_tag_fakes",
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

if OptionGenuineTauBackgroundSource == "DataDriven":
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
    function      = "QCDShapeVariation",
    systVariation = "QCDNormSource",
))

Nuisances.append(Nuisance(
    id            = "fakerateprob_weighting",
    label         = "Fake rate probability weighting syst.",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "FakeWeighting",
))

Nuisances.append(Nuisance(
    id            = "probabilistic_Btag",
    label         = "B tag applied as weight of fake taus not from tt",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "probBtag",
))

Nuisances.append(Nuisance(
    id            = "lepton_veto_forFakeTau",
    label         = "Lepton veto",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "lepton_veto",
))

if OptionGenuineTauBackgroundSource == "DataDriven" or OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
    Nuisances.append(Nuisance(
        id            = "Emb_QCDcontam",
        label         = "EWK with taus QCD contamination",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.020 #FIXME
    ))
    Nuisances.append(Nuisance(
        id            = "Emb_hybridCaloMET",
        label         = "EWK with taus hybrid calo MET and L1ETM",
        distr         = "lnN",
        function      = "Constant",
        value         = 0.12 #FIXME
    ))


if OptionGenuineTauBackgroundSource == "DataDriven":
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
    Nuisances.append(Nuisance(
        id            = "Emb_reweighting",
        label         = "Embedding reweighting",
        distr         = "shapeQ",
        function      = "ShapeVariation",
        systVariation = "EmbMTWeight",
    ))

if OptionGenuineTauBackgroundSource == "MC_RealisticProjection":
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
    id            = "xsect_tt_8TeV",
    label         = "ttbar cross section",
    distr         = "lnN",
    function      = "Constant",
    value         = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyDown(),
    upperValue    = systematics.getCrossSectionUncertainty("TTJets").getUncertaintyUp(),
))

Nuisances.append(Nuisance(
    id            = "xsect_tt_8TeV_forQCD",
    label         = "ttbar cross section",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "xsect_tt_8TeV_forQCD",
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

Nuisances.append(Nuisance(
    id            = "lumi_forQCD",
    label         = "luminosity",
    distr         = "shapeQ",
    function      = "ShapeVariation",
    systVariation = "lumi_forQCD",
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
    id            = "normalizationAfterCollinearCuts",
    label         = "normalization done after collinear cuts", 
    distr         = "lnN",
    function      = "Constant", 
    value         = 0.045,
))

MergeNuisances = []
if "tau_ID_constShape" in myEmbeddingShapeSystematics:
    MergeNuisances.append(["tau_ID_shape", "tau_ID_constShape"])
#if OptionTreatTriggerUncertaintiesAsAsymmetric:
#    MergeNuisances.append(["trg_CaloMET_dataeff", "trg_CaloMET_dataeff_forQCD"])
#    MergeNuisances.append(["trg_CaloMET_MCeff", "trg_CaloMET_MCeff_forQCD"])
#else:
#    MergeNuisances.append(["trg_CaloMET", "trg_CaloMET_forQCD"])
#MergeNuisances.append(["ES_taus","ES_taus_fakes","ES_taus_tempForEmbedding"])
#MergeNuisances.append(["ES_jets","ES_jets_fakes"])
#MergeNuisances.append(["JER","JER_fakes"])
#MergeNuisances.append(["ES_METunclustered","ES_METunclustered_fakes"])
MergeNuisances.append(["e_mu_veto","e_mu_veto_fakes"])
MergeNuisances.append(["b_tag","b_tag_fakes"])
#MergeNuisances.append(["b_tag","b_tag_fakes"])
MergeNuisances.append(["pileup","pileup_fakes"])
MergeNuisances.append(["xsect_tt_8TeV", "xsect_tt_8TeV_forQCD"])
MergeNuisances.append(["lumi", "lumi_forQCD"])

from LimitCalcInputClasses import convertFromSystVariationToConstant
convertFromSystVariationToConstant(Nuisances, OptionConvertFromShapeToConstantList)

from LimitCalcInputClasses import separateShapeAndNormalizationFromSystVariation
separateShapeAndNormalizationFromSystVariation(Nuisances, OptionSeparateShapeAndNormalizationFromSystVariationList)

# Control plots
from LimitCalcInputClasses import ControlPlotInput
ControlPlots = []


if OptionMassShape == "TransverseMass":
    ControlPlots.append(ControlPlotInput(
        title            = "TransverseMass",
        signalHistoPath  = "",
        signalHistoName  = "shapeTransverseMass",
        EWKfakeHistoPath  = "",
        EWKfakeHistoName  = "shapeEWKFakeTausTransverseMass",
        details          = {#"cmsTextPosition": "right",
                            #"xlabel": "m_{T}(^{}#tau_{h},^{}E_{T}^{miss})",
                            #"ylabel": "Events/^{}#Deltam_{T}",
                            #"unit": "GeV",
                            #"xlabel": "m_{T} (GeV)",
                            "xlabel": "m_{T}(tau,MET), GeV",
                            "ylabel": "< Events / bin >", "ylabelBinInfo": False,
                            "moveLegend": {"dx": -0.15, "dy": -0.03, "dh":0.1},
                            "ratioMoveLegend": {"dx": -0.06, "dy": 0.0},
                            "divideByBinWidth": True,
                            "log": False,
                            "opts": {"ymin": 0.0},
                            "opts2": {"ymin": 0.0, "ymax": 2.0}
                            },
        blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [60, 180], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    ControlPlots.append(ControlPlotInput(
        title            = "TransverseMassLog",
        signalHistoPath  = "",
        signalHistoName  = "shapeTransverseMass",
        EWKfakeHistoPath  = "",
        EWKfakeHistoName  = "shapeEWKFakeTausTransverseMass",
        details          = {#"cmsTextPosition": "right",
                            #"xlabel": "m_{T}(^{}#tau_{h},^{}E_{T}^{miss})",
                            #"ylabel": "Events/^{}#Deltam_{T}",
                            #"unit": "GeV",
                            #"xlabel": "m_{T} (GeV)",
                            "xlabel": "m_{T}(tau,MET), GeV",
                            "ylabel": "< Events / bin >", "ylabelBinInfo": False,
                            "moveLegend": {"dx": -0.10, "dy": -0.03, "dh":0.1},
                            "ratioMoveLegend": {"dx": -0.06, "dy": 0.0},
                            "divideByBinWidth": True,
                            "log": True,
                            "opts": {"ymin": 1e-3},
                            "opts2": {"ymin": 0.0, "ymax": 2.0}
                           },
        blindedRange     = [-1, 1000], # specify range min,max if blinding applies to this control plot
        evaluationRange  = [], # specify range to be evaluated and saved into a file
        flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot
    ))
