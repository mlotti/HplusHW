import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics

DataCardName ='Default_13TeV'
#Path='test'
Path='test_1pr'
#Path='test_3pr'
#Path='test_1pr_inclusive'
#Path='test_3pr_inclusive'
#Path="test_1pr_opt_btag_met"
#Path='test_123pr_puppimet'
#Path='testmet140_puppi_vtx'
#Path='testbtagtight'
#Path='testnorm'

LightMassPoints=[80,90,100,120,140,150,155,160]
#LightMassPoints=[80,120,160]
#LightMassPoints=[140]
LightMassPoints=[]

#HeavyMassPoints=[180,200,220,250,300,350,400,500]
#HeavyMassPoints=[180,220,300,600]
HeavyMassPoints=[300]
#HeavyMassPoints=[]

MassPoints=LightMassPoints[:]+HeavyMassPoints[:]

##############################################################################
# Options
BlindAnalysis=True
OptionBlindThreshold=None # If signal exceeds this fraction of expected events, data is blinded; set to None to disable

# Options
OptionMassShape="TransverseMass"
#OptionMassShape="FullMass"
#OptionMassShape="TransverseAndFullMass2D" #FIXME not yet supported!!!

# Choose source of EWK+tt genuine tau background
#OptionGenuineTauBackgroundSource="DataDriven"                        # EWK+tt genuine taus from embedding
OptionGenuineTauBackgroundSource="MC_FakeAndGenuineTauNotSeparated"   # EWK+tt genuine taus from MC

OptionSeparateFakeTtbarFromFakeBackground=False # NOTE: this flag should be put true for light H+ and to false for heavy H+

OptionRealisticEmbeddingWithMC=True # Only relevant for OptionReplaceEmbeddingByMC==True
OptionIncludeSystematics=not True # Set to true if you produced multicrabs with doSystematics=True

OptionDoControlPlots=True
OptionDoMergeFakeTauColumns=True # Merges the fake tau columns into one
OptionCombineSingleColumnUncertainties=False # Makes limit running faster
OptionCtrlPlotsAtMt=True # Produce control plots after all selections (all selections for transverse mass)
OptionDisplayEventYieldSummary=True
OptionNumberOfDecimalsInSummaries=1
OptionLimitOnSigmaBr=False # Is automatically set to true for heavy H+
# Deprecated:
OptionDoTBbarForHeavy=False # NOTE: usable only for 2012
OptionAddSingleTopDependencyForMuParameter=False # Affects only light H+, 2012 only
OptionAddSingleTopSignal=False # Affects only light H+, 2012 only

# Convert the following nuisances from shape to constant
OptionConvertFromShapeToConstantList=["CMS_trg_taumet_tau","CMS_trg_taumet_tau_dataeff","CMS_trg_taumet_tau_MCeff",
                                      "CMS_trg_taumet_L1ETM_dataeff","CMS_trg_taumet_L1ETM_MCeff","CMS_trg_taumet_L1ETM",
                                      "CMS_trg_muon_dataeff", # triggers
                                      #"CMS_eff_t", # tau ID
                                      "CMS_fake_eToTauEndcap", # tau mis-ID
                                      #"CMS_fake_eToTauBarrel", "CMS_fake_muToTau", "CMS_fake_jetToTau", # other tau mis-ID
                                      "CMS_scale_j","CMS_res_j","CMS_scale_met", # jet, MET ES
                                      #"CMS_scale_t", # tau ES
                                      #"CMS_tag_b", "CMS_tag_b_genuinetau", # btag
                                      "CMS_Hptntj_taubkg_ID_mu", "CMS_Hptntj_taubkg_WtauToMu", # embedding-specific
                                      #"CMS_Hptntj_taubkg_reweighting", # other embedding-specific
                                      #"CMS_Hptntj_QCDkbg_metshape", # multijets specific
                                      #"CMS_Hptntj_topPtReweighting", # top pt reweighting
                                      "CMS_pileup", "CMS_pileup_genuinetau", # CMS_pileup
                                      ]
OptionConvertFromShapeToConstantList=[] # FIXME
# Separate in the following shape nuisances the shape and normalization components
OptionSeparateShapeAndNormalizationFromSystVariationList=[#"CMS_scale_t"
                                                          ]

# For projections
CMS_trg_taumet_MET_dataeffScaleFactor=None # Default is None, i.e. 1.0

# Options for reports and article
OptionBr=0.01  # Br(t->bH+)
OptionSqrtS=13 # sqrt(s)

# Tolerance for throwing error on CMS_lumi_13TeVnosity difference (0.01=1 percent agreement is required)
ToleranceForLuminosityDifference=0.05
# Tolerance for almost zero rate (columns with smaller rate are suppressed)
ToleranceForMinimumRate=0.0 # 1.5
# Minimum stat. uncertainty to set to bins with zero events
MinimumStatUncertainty=0.5

##############################################################################
# Counter and histogram path definitions

# Rate counter definitions
SignalRateCounter="Selected events"
FakeRateCounter="EWKfaketaus:SelectedEvents"

# Shape histogram definitions
shapeHistoName=None
histoPathInclusive="ForDataDrivenCtrlPlots"
histoPathGenuineTaus="ForDataDrivenCtrlPlotsEWKGenuineTaus"
histoPathFakeTaus="ForDataDrivenCtrlPlotsEWKFakeTaus"

if OptionMassShape =="TransverseMass":
    shapeHistoName="shapeTransverseMass"
    #shapeHisto="ForDataDrivenCtrlPlotsEWKGenuineTaus/shapeTransverseMass"
elif OptionMassShape =="FullMass":
    raise Exception("Does not work")
    shapeHistoName="shapeInvariantMass"
    #FakeShapeOtherHisto="shapeEWKFakeTausInvariantMass"
    #FakeShapeTTbarHisto=FakeShapeOtherHisto
elif OptionMassShape =="TransverseAndFullMass2D": # FIXME: preparing to add support, not yet working
    raise Exception("Does not work")
    shapeHistoName="shapetransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    #FakeShapeOtherHisto="shapeEWKFakeTausTransverseAndFullMass2D" # FIXME: Not yet implemented to signal analysis, etc.
    #FakeShapeTTbarHisto=FakeShapeOtherHisto
ShapeHistogramsDimensions=systematics.getBinningForPlot(shapeHistoName)

DataCardName +="_"+OptionMassShape.replace("TransverseMass","mT").replace("FullMass","invMass")

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from HiggsAnalysis.LimitCalc.InputClasses import ObservationInput
Observation=ObservationInput(datasetDefinition="Data", shapeHistoName=shapeHistoName, histoPath=histoPathInclusive)

##############################################################################
# Define systematics lists commmon to datasets
myTrgSystematics=["CMS_trg_taumet_tau_dataeff","CMS_trg_taumet_tau_MCeff", # Trigger tau part
                  "CMS_trg_taumet_MET_dataeff","CMS_trg_taumet_MET_MCeff"] # Trigger MET part
myTauIDSystematics=["CMS_eff_t"] #tau ID
myTauMisIDSystematics=["CMS_fake_eToTau","CMS_fake_muToTau","CMS_fake_jetToTau"] # tau mis-ID
myESSystematics=["CMS_scale_t","CMS_scale_j","CMS_res_j","CMS_scale_met"] # TES, JES, CMS_res_j, UES
myBtagSystematics=["CMS_tag_b","CMS_mistag_b"] # b tag and mistag
myTopSystematics=["CMS_Hptntj_topPtReweighting"] # top pt reweighting
myPileupSystematics=["CMS_pileup"] # CMS_pileup
myLeptonVetoSystematics=["CMS_veto_e","CMS_veto_mu"] # CMS_pileup

myShapeSystematics=[]
myShapeSystematics.extend(myTrgSystematics)
#myShapeSystematics.extend(myTauIDSystematics)
myShapeSystematics.extend(myTauMisIDSystematics)
myShapeSystematics.extend(["CMS_scale_t","CMS_scale_j"]) #myESSystematics)
myShapeSystematics.extend(myBtagSystematics)
myShapeSystematics.extend(myTopSystematics)
#myShapeSystematics.extend(myPileupSystematics)

if not OptionIncludeSystematics:
    myShapeSystematics=[]

myEmbeddingShapeSystematics=["CMS_trg_taumet_tau_dataeff","CMS_trg_taumet_L1ETM_dataeff","CMS_trg_muon_dataeff","CMS_scale_t","CMS_Hptntj_taubkg_ID_mu","CMS_Hptntj_taubkg_WtauToMu"]

##############################################################################
# DataGroup (i.e. columns in datacard) definitions
#
from HiggsAnalysis.LimitCalc.InputClasses import DataGroup
DataGroups=[]
EmbeddingIdList=[]
EWKFakeIdList=[]

signalTemplate=DataGroup(datasetType="Signal", histoPath=histoPathInclusive, shapeHistoName=shapeHistoName)
mergeColumnsByLabel=[]

for mass in LightMassPoints:
    myMassList=[mass]
    hwx=signalTemplate.clone()
    hwx.setLabel("CMS_Hptntj_HW"+str(mass)+"_a")
    hwx.setLandSProcess(0)
    hwx.setValidMassPoints(myMassList)
    hwx.setNuisances(myTrgSystematics[:]+myTauIDSystematics[:]+myTauMisIDSystematics[:]
                     +myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]
                     +["xsect_tt","CMS_lumi_13TeV"])
    hwx.setDatasetDefinition("TTToHplusBWB_M"+str(mass))
    DataGroups.append(hwx)
for mass in HeavyMassPoints:
    myMassList=[mass]
    hx=signalTemplate.clone()
    hx.setLabel("CMS_Hptntj_Hp"+str(mass)+"_a")
    hx.setLandSProcess(0)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(myTrgSystematics[:]+myTauIDSystematics[:]+myTauMisIDSystematics[:]
                    +myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]
                    +["CMS_lumi_13TeV"])
    if not OptionDoTBbarForHeavy:    
        hx.setDatasetDefinition("HplusTB_M"+str(mass))
    else:
        raise Exception("This does not work")    
        hx.setDatasetDefinition("HplusToTBbar_M"+str(mass))
    DataGroups.append(hx)

#for i in range(0,len(myQCDShapeSystematics)):#if myQCDShapeSystematics[i].startswith("trg_CaloMET") and not "forQCD" in myQCDShapeSystematics[i]:#    myQCDShapeSystematics[i]=myQCDShapeSystematics[i]+"_forQCD"

#myQCD=DataGroup(#label="QCDinv",#landsProcess=3,#validMassPoints=MassPoints,#datasetType="QCD inverted",#datasetDefinition="QCDinvertedmt",#nuisances=myQCDShapeSystematics[:]+["CMS_tag_b","CMS_Hptntj_topPtReweighting","CMS_Hptntj_QCDkbg_metshape","xsect_tt_forQCD","CMS_Hptntj_QCDbkg_templateFit","CMS_lumi_13TeV_forQCD"],#shapeHistoName=shapeHistoName,
#)
#if OptionMassShape =="TransverseMass":#myQCD.setDatasetDefinition("QCDinvertedmt")
#elif OptionMassShape =="FullMass":#myQCD.setDatasetDefinition("QCDinvertedinvmass")

myQCD=DataGroup(label="CMS_Hptntj_QCDandFakeTau", landsProcess=1, validMassPoints=MassPoints,
                #datasetType="QCD MC", datasetDefinition="QCD",
                #nuisances=myShapeSystematics[:]+["xsect_QCD","CMS_lumi_13TeV"],
                datasetType="QCD inverted", datasetDefinition="QCDMeasurementMT",
                nuisances=myTrgSystematics[:]
                          +myESSystematics[:]+myBtagSystematics[:]+myTopSystematics[:]
                          +["CMS_Hptntj_QCDbkg_templateFit"], #,"xsect_tt_forQCD","CMS_lumi_13TeV_forQCD"]+myTauIDSystematics[:],
                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive)
DataGroups.append(myQCD)
print "*** Warning *** FIXME: Add QCD uncertainties xsect_tt_forQCD and CMS_lumi_13TeV_forQCD"

if OptionGenuineTauBackgroundSource =="DataDriven":
    # EWK genuine taus from embedding
    myEmbDataDrivenNuisances=["CMS_EmbSingleMu_QCDcontam","CMS_EmbSingleMu_hybridCaloMET","CMS_Hptntj_taubkg_reweighting"] # EWK + ttbar with genuine taus
    EmbeddingIdList=[3]
    DataGroups.append(DataGroup(label="CMS_Hptntj_EWK_Tau", landsProcess=1, 
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding", 
                                #datasetDefinition=["SingleMu"], 
                                datasetDefinition="Data", 
                                validMassPoints=MassPoints, 
                                #additionalNormalisation=0.25, # not needed anymore
                                nuisances=myEmbeddingShapeSystematics[:]+myEmbDataDrivenNuisances[:]
                                ))
else:
    # EWK genuine taus from MC
    DataGroups.append(DataGroup(label="CMS_Hptntj_tt_genuinetau", landsProcess=3,
                                shapeHistoName=shapeHistoName, histoPath=histoPathGenuineTaus,
                                datasetType="Embedding",
                                datasetDefinition="TT",
                                validMassPoints=MassPoints,
                                nuisances=myTrgSystematics[:]+myTauIDSystematics[:]
                                  +myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]
                                  +myTopSystematics+["xsect_tt","CMS_lumi_13TeV"]))
    DataGroups.append(DataGroup(label="CMS_Hptntj_W_genuinetau", landsProcess=4,
                                shapeHistoName=shapeHistoName, histoPath=histoPathGenuineTaus,
                                datasetType="Embedding", 
                                datasetDefinition="WJetsHT",
                                validMassPoints=MassPoints,
                                nuisances=myTrgSystematics[:]+myTauIDSystematics[:]
                                  +myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]
                                  +["xsect_Wjets","CMS_lumi_13TeV"]))
    DataGroups.append(DataGroup(label="CMS_Hptntj_t_genuinetau", landsProcess=5,
                                shapeHistoName=shapeHistoName, histoPath=histoPathGenuineTaus,
                                datasetType="Embedding",
                                datasetDefinition="SingleTop",
                                validMassPoints=MassPoints,
                                nuisances=myTrgSystematics[:]+myTauIDSystematics[:]
                                  +myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]
                                  +["xsect_singleTop","CMS_lumi_13TeV"]))
    DataGroups.append(DataGroup(label="CMS_Hptntj_DY_genuinetau", landsProcess=6,
                                shapeHistoName=shapeHistoName, histoPath=histoPathGenuineTaus,
                                datasetType="Embedding",
                                datasetDefinition="DYJetsToLLHT",
                                validMassPoints=MassPoints,
                                nuisances=myTrgSystematics[:]+myTauIDSystematics[:]
                                  +myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]
                                  +["xsect_DYtoll","CMS_lumi_13TeV"]))
    #DataGroups.append(DataGroup(label="CMS_Hptntj_VV_genuinetau", landsProcess=7,
                                #shapeHistoName=shapeHistoName, histoPath=histoPathGenuineTaus, 
                                #datasetType="Embedding", 
                                #datasetDefinition="Diboson",
                                #validMassPoints=MassPoints,
                                #nuisances=myTrgSystematics[:]+myTauIDSystematics[:]
                                  #+myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]
                                  #+["xsect_VV","CMS_lumi_13TeV"]))
    # Merge EWK as one column or not
    #if not OptionSeparateFakeTtbarFromFakeBackground:
        #mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["tt_EWK_faketau","W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})
    #else:
        #mergeColumnsByLabel.append({"label": "EWKnontt_faketau", "mergeList": ["W_EWK_faketau","t_EWK_faketau","DY_EWK_faketau","VV_EWK_faketau"]})

# Reserve column 2
# This was necessary for LandS; code could be updated to combine for this piece
if not OptionAddSingleTopSignal:DataGroups.append(DataGroup(label="res.", landsProcess=2,
    datasetType="None", validMassPoints=MassPoints))

##############################################################################
# Definition of nuisance parameters
#
# Note: Remember to include 'stat.' into the label of nuistances of statistical nature
#
from HiggsAnalysis.LimitCalc.InputClasses import Nuisance
ReservedNuisances=[]
Nuisances=[]

#=====tau and MET trg
if "CMS_trg_taumet_tau_dataeff" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_tau_dataeff", label="tau+MET trg tau part data eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="TauTrgEffData"))
else:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_tau_dataeff", label="APPROXIMATION for tau+MET trg tau part data eff.",
        distr="lnN", function="Constant", value=0.015))
if "CMS_trg_taumet_tau_MCeff" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_tau_MCeff", label="tau+MET trg tau part MC eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="TauTrgEffMC"))
else:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_tau_MCeff", label="APPROXIMATION for tau+MET trg tau part MC eff.",
        distr="lnN", function="Constant", value=0.010))
if "CMS_trg_taumet_MET_dataeff" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_MET_dataeff", label="tau+MET trg MET data eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="METTrgEffData"))
else:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_MET_dataeff", label="APPROXIMATION for tau+MET trg MET data eff.",
        distr="lnN", function="Constant", value=0.15))
if "CMS_trg_taumet_MET_MCeff" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_MET_MCeff", label="tau+MET trg MET MC eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="METTrgEffMC"))
else:
    Nuisances.append(Nuisance(id="CMS_trg_taumet_MET_MCeff", label="APPROXIMATION for tau+MET trg MET MC eff.",
        distr="lnN", function="Constant", value=0.01))
#=====lepton veto
Nuisances.append(Nuisance(id="CMS_veto_e", label="e veto",
    distr="lnN", function="Ratio",
    numerator="passed e selection (Veto)", # main counter name after electron veto
    denominator="Tau trigger SF", # main counter name before electron and muon veto
    scaling=0.02
))
Nuisances.append(Nuisance(id="CMS_veto_mu", label="mu veto",
    distr="lnN", function="Ratio",
    numerator="passed mu selection (Veto)", # main counter name after electron and muon veto
    denominator="passed e selection (Veto)", # main counter name before muon veto
    scaling =0.01
))
#=====tau ID and mis-ID
# tau ID
if "CMS_eff_t" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_eff_t", label="tau-jet ID (no Rtau) genuine taus",
        distr="shapeQ", function="ShapeVariation", systVariation="GenuineTau"))
else:
    Nuisances.append(Nuisance(id="CMS_eff_t", label="APPROXIMATION for tau-jet ID (no Rtau) genuine taus",
        distr="lnN", function="Constant", value=0.06))
# e->tau mis-ID
if "CMS_fake_eToTau" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_fake_eToTau", label="tau-jet ID (no Rtau) e->tau",
        distr="shapeQ", function="ShapeVariation", systVariation="FakeTauElectron"))
else:
    Nuisances.append(Nuisance(id="CMS_fake_eToTau", label="APPROXIMATION for tau-jet ID (no Rtau) e->tau",
        distr="lnN", function="Constant", value=0.001))
#if "CMS_fake_eToTauBarrel" in myShapeSystematics:
    #Nuisances.append(Nuisance(id="CMS_fake_eToTauBarrel", label="tau-jet ID (no Rtau) e->tau (barrel)",
        #distr="shapeQ", function="ShapeVariation", systVariation="GenuineTau"))
#else:
    #Nuisances.append(Nuisance(id="CMS_fake_eToTauBarrel", label="APPROXIMATION for tau-jet ID (no Rtau) e->tau (barrel)",
        #distr="lnN", function="Constant", value=0.001))
#if "CMS_fake_eToTauEndcap" in myShapeSystematics:
    #Nuisances.append(Nuisance(id="CMS_fake_eToTauEndcap", label="tau-jet ID (no Rtau) e->tau (endcap)",
        #distr="shapeQ", function="ShapeVariation", systVariation="GenuineTau"))
#else:
    #Nuisances.append(Nuisance(id="CMS_fake_eToTauEndcap", label="APPROXIMATION for tau-jet ID (no Rtau) e->tau (endcap)",
        #distr="lnN", function="Constant", value=0.001))
# mu->tau mis-ID
if "CMS_fake_muToTau" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_fake_muToTau", label="tau-jet ID (no Rtau) mu->tau",
        distr="shapeQ", function="ShapeVariation", systVariation="FakeTauMuon"))
else:
    Nuisances.append(Nuisance(id="CMS_fake_muToTau", label="APPROXIMATION for tau-jet ID (no Rtau) mu->tau",
        distr="lnN", function="Constant", value=0.001))
# jet->tau mis-ID
if "CMS_fake_jetToTau" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_fake_jetToTau", label="tau-jet ID (no Rtau) jet->tau",
        distr="shapeQ", function="ShapeVariation", systVariation="FakeTauJet"))
else:
    Nuisances.append(Nuisance(id="CMS_fake_jetToTau", label="APPROXIMATION for tau-jet ID (no Rtau) jet->tau",
        distr="lnN", function="Constant", value=0.01))
#===== energy scales
# tau ES
if "CMS_scale_t" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_scale_t", label="Tau energy scale",
        distr="shapeQ", function="ShapeVariation", systVariation="tauES"))
else:
    Nuisances.append(Nuisance(id="CMS_scale_t", label="APPROXIMATION for tau ES",
        distr="lnN", function="Constant", value=0.03))
# jet ES
if "CMS_scale_j" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_scale_j", label="Jet energy scale",
        distr="shapeQ", function="ShapeVariation", systVariation="JES"))
else:
    Nuisances.append(Nuisance(id="CMS_scale_j", label="APPROXIMATION for jet ES",
        distr="lnN", function="Constant", value=0.03))
# unclustered MET ES
if "CMS_scale_met" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_scale_met", label="Unclustered MET energy scale",
        distr="shapeQ", function="ShapeVariation", systVariation="CMS_res_j"))
else:
    Nuisances.append(Nuisance(id="CMS_scale_met", label="APPROXIMATION for unclustered MET ES",
        distr="lnN", function="Constant",value=0.03))
# CMS_res_j
if "CMS_res_j" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_res_j", label="Jet energy resolution",
        distr="shapeQ", function="ShapeVariation", systVariation="CMS_res_j"))
else:
    Nuisances.append(Nuisance(id="CMS_res_j", label="APPROXIMATION for CMS_res_j",
        distr="lnN", function="Constant",value=0.03))
#===== b tag and mistag SF
if "CMS_tag_b" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_tag_b", label="b tagging",
        distr="shapeQ", function="ShapeVariation", systVariation="BTagSF"))
else:
    Nuisances.append(Nuisance(id="CMS_tag_b", label="APPROXIMATION for b tagging",
        distr="lnN", function="Constant",value=0.05))
if "CMS_mistag_b" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_mistag_b", label="b mistagging",
        distr="shapeQ", function="ShapeVariation", systVariation="BMistagSF"))
else:
    Nuisances.append(Nuisance(id="CMS_mistag_b", label="APPROXIMATION for b mistagging",
        distr="lnN", function="Constant",value=0.05))
#===== Top pt SF
if "CMS_Hptntj_topPtReweighting" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_Hptntj_topPtReweighting", label="top pT reweighting",
        distr="shapeQ", function="ShapeVariation", systVariation="TopPt"))
else:
    Nuisances.append(Nuisance(id="CMS_Hptntj_topPtReweighting", label="APPROXIMATION for top pT reweighting",
        distr="lnN", function="Constant",value=0.20))
#===== Pileup
if "CMS_pileup" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_pileup", label="CMS_pileup",
        distr="shapeQ", function="ShapeVariation", systVariation="Pileup"))
else:
    Nuisances.append(Nuisance(id="CMS_pileup", label="APPROXIMATION for CMS_pileup",
        distr="lnN", function="Constant",value=0.05))
#===== Cross section
Nuisances.append(Nuisance(id="xsect_tt", label="ttbar cross section",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("TTJets").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("TTJets").getUncertaintyUp()))
Nuisances.append(Nuisance(id="xsect_tt_forQCD", label="ttbar cross section",
    distr="lnN", function="ConstantForQCD",
    value=systematics.getCrossSectionUncertainty("TTJets").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("TTJets").getUncertaintyUp()))
Nuisances.append(Nuisance(id="xsect_Wjets", label="W+jets cross section",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("WJets").getUncertaintyDown()))
Nuisances.append(Nuisance(id="xsect_singleTop", label="single top cross section",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("SingleTop").getUncertaintyDown()))
Nuisances.append(Nuisance(id="xsect_DYtoll", label="Z->ll cross section",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("DYJetsToLL").getUncertaintyDown()))
Nuisances.append(Nuisance(id="xsect_VV", label="diboson cross section",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("Diboson").getUncertaintyDown()))
Nuisances.append(Nuisance(id="xsect_QCD", label="QCD MC cross section",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("QCD").getUncertaintyDown()))
#===== Luminosity
Nuisances.append(Nuisance(id="CMS_lumi_13TeV", label="CMS_lumi_13TeVnosity",
    distr="lnN", function="Constant",
    value=systematics.getLuminosityUncertainty()))
Nuisances.append(Nuisance(id="CMS_lumi_13TeV_forQCD", label="CMS_lumi_13TeVnosity",
    distr="lnN", function="ConstantForQCD",
    value=systematics.getLuminosityUncertainty()))
#===== QCD measurement
Nuisances.append(Nuisance(id="CMS_Hptntj_QCDbkg_templateFit", label="QCDInv: fit", 
    distr="lnN", function="Constant", value=0.03))
Nuisances.append(Nuisance(id="CMS_Hptntj_QCDkbg_metshape", label="QCD met shape syst.",
    distr="shapeQ", function="QCDShapeVariation", systVariation="QCDNormSource"))
#===== Embedding
if OptionGenuineTauBackgroundSource == "DataDriven":
    Nuisances.append(Nuisance(id="CMS_EmbSingleMu_QCDcontam", label="EWK with taus QCD contamination",
        distr="lnN", function="Constant", value=0.020 #FIXME
    ))
    Nuisances.append(Nuisance(id="CMS_EmbSingleMu_hybridCaloMET", label="EWK with taus hybrid calo MET and L1ETM",
        distr="lnN", function="Constant", value=0.12 #FIXME
    ))
    if "CMS_Hptntj_taubkg_WtauToMu" in myEmbeddingShapeSystematics:
        Nuisances.append(Nuisance(id="CMS_Hptntj_taubkg_WtauToMu", label="EWK with taus W->tau->mu",
            distr="shapeQ", function="ShapeVariation", systVariation="WTauMu", ))
    else:
        Nuisances.append(Nuisance(id="CMS_Hptntj_taubkg_WtauToMu", label="EWK with taus W->tau->mu",
            distr="lnN", function="Constant", value=0.007 ))
    Nuisances.append(Nuisance(id="CMS_Hptntj_taubkg_reweighting", label="Embedding reweighting",
        distr="shapeQ", function="ShapeVariation", systVariation="EmbMTWeight",
    ))
#===== Merge nuisances to same row (first item specifies the name for the row)
MergeNuisances=[]
if "CMS_eff_t_constShape" in myEmbeddingShapeSystematics:
    MergeNuisances.append(["CMS_eff_t", "CMS_eff_t_constShape"])
#MergeNuisances.append(["CMS_scale_t","CMS_scale_t_genuinetau","CMS_scale_t_tempForEmbedding"])
#MergeNuisances.append(["CMS_scale_j","CMS_scale_j_genuinetau"])
#MergeNuisances.append(["CMS_res_j","CMS_res_j_genuinetau"])
#MergeNuisances.append(["CMS_scale_met","CMS_scale_met_genuinetau"])
#MergeNuisances.append(["CMS_veto_e", "CMS_veto_e_genuinetau"])
#MergeNuisances.append(["CMS_veto_mu", "CMS_veto_mu_genuinetau"])
#MergeNuisances.append(["CMS_tag_b","CMS_tag_b_genuinetau"])
#MergeNuisances.append(["CMS_mistag_b","CMS_mistag_b_genuinetau"])
#MergeNuisances.append(["CMS_pileup","CMS_pileup_genuinetau"])
MergeNuisances.append(["xsect_tt", "xsect_tt_forQCD"])
MergeNuisances.append(["CMS_lumi_13TeV", "CMS_lumi_13TeV_forQCD"])

from HiggsAnalysis.LimitCalc.InputClasses import convertFromSystVariationToConstant
convertFromSystVariationToConstant(Nuisances, OptionConvertFromShapeToConstantList)

from HiggsAnalysis.LimitCalc.InputClasses import separateShapeAndNormalizationFromSystVariation
separateShapeAndNormalizationFromSystVariation(Nuisances, OptionSeparateShapeAndNormalizationFromSystVariationList)

# Control plots
from HiggsAnalysis.LimitCalc.InputClasses import ControlPlotInput
ControlPlots=[]
#EWKPath="ForDataDrivenCtrlPlotsEWKFakeTaus"
EWKPath="ForDataDrivenCtrlPlotsEWKGenuineTaus"

#ControlPlots.append(ControlPlotInput(
    #title            = "NVertices_AfterStandardSelections",
    #histoName        = "NVertices_AfterStandardSelections",
    #details          = { "xlabel": "N_{vertices}",
                         #"ylabel": "Events",
                         #"divideByBinWidth": False,
                         #"unit": "",
                         #"log": True,
                         #"opts": {"ymin": 0.0009} }))
ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_pT_AfterStandardSelections",
    histoName        = "SelectedTau_pT_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "opts": {"ymin": 0.0009} }))
#ControlPlots.append(ControlPlotInput(
    #title            = "SelectedTau_p_AfterStandardSelections",
    #histoName        = "SelectedTau_p_AfterStandardSelections",
    #details          = { "xlabel": "Selected #tau p",
                         #"ylabel": "Events/#Deltap",
                         #"divideByBinWidth": True,
                         #"unit": "GeV/c",
                         #"log": True,
                         #"opts": {"ymin": 0.009} }))
ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_eta_AfterStandardSelections",
    histoName        = "SelectedTau_eta_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau #eta",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.009} }))
ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_phi_AfterStandardSelections",
    histoName        = "SelectedTau_phi_AfterStandardSelections",
    details          = { "xlabel": "Selected #tau #phi",
                         "ylabel": "Events",
                         "divideByBinWidth": False,
                         "unit": "{}^{o}",
                         "log": True,
                         "legendPosition": "SW",
                         "opts": {"ymin": 0.009} }))
ControlPlots.append(ControlPlotInput(
    title            = "SelectedTau_ldgTrkPt_AfterStandardSelections",
    histoName        = "SelectedTau_ldgTrkPt_AfterStandardSelections",
    details          = { "xlabel": "#tau leading track ^{}p_{T}",
                         "ylabel": "Events/^{}#Deltap_{T}",
                         "divideByBinWidth": True,
                         "unit": "GeV/c",
                         "log": True,
                         "ratioLegendPosition": "right",
                         "opts": {"ymin": 0.0009} }))
#ControlPlots.append(ControlPlotInput(
    #title            = "SelectedTau_LeadingTrackP_AfterStandardSelections",
    #histoName        = "SelectedTau_LeadingTrackP_AfterStandardSelections",
    #details          = { "xlabel": "#tau leading track p",
                         #"ylabel": "Events/#Deltap",
                         #"divideByBinWidth": True,
                         #"unit": "GeV/c",
                         #"log": True,
                         #"ratioLegendPosition": "right",
                         #"opts": {"ymin": 0.0009} },))
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
    title            = "Njets_AfterStandardSelections",
    histoName        = "Njets_AfterStandardSelections",
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
                         "opts": {"ymin": 0.09} }))
#ControlPlots.append(ControlPlotInput(
    #title            = "TauPlusMETPt",
    #histoName        = "TauPlusMETPt",
    #details          = { "xlabel": "p_{T}(#tau + ^{}E_{T}^{miss})",
                         #"ylabel": "Events/^{}#Deltap_{T}",
                         #"divideByBinWidth": True,
                         #"unit": "GeV",
                         #"log": True,
                         #"opts": {"ymin": 0.0009} }))
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

if OptionMassShape =="TransverseMass":
    ControlPlots.append(ControlPlotInput(title="TransverseMass",
        histoName="shapeTransverseMass",
        details={"cmsTextPosition": "right",
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
        }, blindedRange=[81, 1000], # specify range min,max if blinding applies to this control plot
        flowPlotCaption="final", # Leave blank if you don't want to include the item to the selection flow plot
    ))
    ControlPlots.append(ControlPlotInput(title="TransverseMassLog",
        histoName="shapeTransverseMass",
        details={"cmsTextPosition": "right",
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
        }, blindedRange=[81, 1000], # specify range min,max if blinding applies to this control plot
    ))
elif OptionMassShape =="FullMass":
    ControlPlots.append(ControlPlotInput(title="FullMass",
        histoName="shapeInvariantMass",
        details={ "xlabel": "m(^{}#tau_{h},^{}E_{T}^{miss})",
          "ylabel": "Events/#Deltam",
          "divideByBinWidth": True,
          "unit": "GeV",
          "log": False,
          "opts": {"ymin": 0.0},
          "opts2": {"ymin": 0.0, "ymax": 2.0},
        }, blindedRange=[-1, 1000], # specify range min,max if blinding applies to this control plot
        flowPlotCaption="final", # Leave blank if you don't want to include the item to the selection flow plot
    ))

if OptionCtrlPlotsAtMt:
    ControlPlots.append(ControlPlotInput(title="NVertices_AfterAllSelections",
        histoName="NVertices_AfterAllSelections",
        details={ "xlabel": "N_{vertices}",
          "ylabel": "Events",
          "divideByBinWidth": False,
          "unit": "",
          "log": True,
          "opts": {"ymin": 0.0009} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_pT_AfterAllSelections",
        histoName="SelectedTau_pT_AfterAllSelections",
        details={ "xlabel": "Selected #tau ^{}p_{T}",
          "ylabel": "Events/^{}#Deltap_{T}",
          "divideByBinWidth": True,
          "unit": "GeV/c",
          "log": True,
          "opts": {"ymin": 0.0009} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_eta_AfterAllSelections",
        histoName="SelectedTau_eta_AfterAllSelections",
        details={ "xlabel": "Selected #tau #eta",
          "ylabel": "Events",
          "divideByBinWidth": False,
          "unit": "",
          "log": True,
          "legendPosition": "SW",
          "opts": {"ymin": 0.009} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_phi_AfterAllSelections",
        histoName="SelectedTau_phi_AfterAllSelections",
        details={ "xlabel": "Selected #tau #phi",
          "ylabel": "Events",
          "divideByBinWidth": False,
          "unit": "{}^{o}",
          "log": True,
          "legendPosition": "SW",
          "opts": {"ymin": 0.09} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_ldgTrkPt_AfterAllSelections",
        histoName="SelectedTau_ldgTrkPt_AfterAllSelections",
        details={ "xlabel": "#tau leading track p{}_{T}",
          "ylabel": "Events/^{}#Deltap_{T}",
          "divideByBinWidth": True,
          "unit": "GeV/c",
          "log": True,
          "ratioLegendPosition": "right",
          "opts": {"ymin": 0.0009} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_Rtau_AfterAllSelections",
        histoName="SelectedTau_Rtau_AfterAllSelections",
        details={ "xlabel": "Selected #tau R_{#tau}",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "legendPosition": "SE",
        "opts": {"ymin": 0.009} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_Rtau_FullRange_AfterAllSelections",
        histoName="SelectedTau_Rtau_AfterAllSelections",
        details={ "xlabel": "Selected #tau R_{#tau}",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "legendPosition": "SW",
        "opts2": {"ymin": 0.2, "ymax": 1.8},
        "opts": {"ymin": 0.009} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_DecayMode_AfterAllSelections",
        histoName="SelectedTau_DecayMode_AfterAllSelections",
        details={ "xlabel": "Selected #tau Decay mode",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "ratioLegendPosition": "right",
        "opts": {"ymin": 0.9} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_Nprongs_AfterAllSelections",
        histoName="SelectedTau_Nprongs_AfterAllSelections",
        details={ "xlabel": "Selected #tau N_{prongs}",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "ratioLegendPosition": "right",
        "opts": {"ymin": 0.9} }))
    ControlPlots.append(ControlPlotInput(title="SelectedTau_source_AfterAllSelections",
        histoName="SelectedTau_source_AfterAllSelections",
        details={ "xlabel": "",
        "ylabel": "Events",
        "xlabelsize": 10,
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "ratioLegendPosition": "right",
        "opts": {"ymin": 0.9} }))
    ControlPlots.append(ControlPlotInput(title="Njets_AfterAllSelections",
        histoName="Njets_AfterAllSelections",
        details={ "xlabel": "Number of selected jets",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "opts": {"ymin": 0.9} }))
    ControlPlots.append(ControlPlotInput(title="JetPt_AfterAllSelections",
    histoName="JetPt_AfterAllSelections",
        details={ "xlabel": "jet ^{}p_{T}",
        "ylabel": "Events/^{}Deltap_{T}",
        "divideByBinWidth": True,
        "unit": "GeV/c",
        "log": True,
        "opts": {"ymin": 0.009} }))
    ControlPlots.append(ControlPlotInput(title="JetEta_AfterAllSelections",
    histoName="JetEta_AfterAllSelections",
        details={ "xlabel": "jet #eta",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "legendPosition": "SW",
        "opts": {"ymin": 0.09} }))
    ControlPlots.append(ControlPlotInput(title="CollinearAngularCutsMinimum_AfterAllSelections",
        histoName="CollinearAngularCutsMinimum_AfterAllSelections",
        details={ "xlabel": "R_{coll}^{min}", #"xlabel": "min(#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1..3},MET))^{2}})",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "{}^{o}",
        "log": True,
        "legendPosition": "NW",
        "opts": {"ymin": 0.09} }))
    ControlPlots.append(ControlPlotInput(title="BJetSelection_AfterAllSelections",
        histoName="NBjets_AfterAllSelections",
        details={ "xlabel": "Number of selected b jets",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "opts": {"ymin": 0.09} }))
    ControlPlots.append(ControlPlotInput(title="BtagDiscriminator_AfterAllSelections",
        histoName="BtagDiscriminator_AfterAllSelections",
        details={ "xlabel": "b tag discriminator",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "legendPosition": "NE",
        "opts": {"ymin": 0.9} }))
    ControlPlots.append(ControlPlotInput(title="BJetPt_AfterAllSelections",
        histoName="BJetPt_AfterAllSelections",
        details={ "xlabel": "b jet ^{}p_{T}",
        "ylabel": "Events/^{}#Deltap_{T}",
        "divideByBinWidth": True,
        "unit": "GeV/c",
        "log": True,
        "opts": {"ymin": 0.0009} }))
    ControlPlots.append(ControlPlotInput(title="BJetEta_AfterAllSelections",
        histoName="BJetEta_AfterAllSelections",
        details={ "xlabel": "b jet #eta",
        "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "",
        "log": True,
        "legendPosition": "SW",
        "opts": {"ymin": 0.09} }))
    ControlPlots.append(ControlPlotInput(title="MET_AfterAllSelections",
        histoName="MET_AfterAllSelections",
        details={ "xlabel": "E_{T}^{miss}",
        "ylabel": "Events/^{}#DeltaE_{T}^{miss}",
        "divideByBinWidth": True,
        "unit": "GeV",
        "log": True,
        "opts": {"ymin": 0.0009} }))
    ControlPlots.append(ControlPlotInput(title="METPhi_AfterAllSelections",
        histoName="METPhi_AfterAllSelections",
        details={ "xlabel": "E_{T}^{miss} #phi",
        "ylabel": "Events/^{}#DeltaE_{T}^{miss}#phi",
        "divideByBinWidth": True,
        "unit": "{}^{o}",
        "log": True,
        "legendPosition": "SW",
        "opts": {"ymin": 0.009} }))
    #for i in range(1,5):    
        #ControlPlots.append(ControlPlotInput(title="AngularCuts2DJet%d_AfterAllSelections"%i,
            #histoName="ImprovedDeltaPhiCuts2DJet%dBackToBack"%i,
            #details={"xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
                #"ylabel": "#Delta#phi(jet_{%d},E_{T}^{miss})"%i,
                #"divideByBinWidth": False,
                #"unit": "{}^{o}",
                #"log": False,
                #"legendPosition": "NW"))
    #ControlPlots.append(ControlPlotInput(title="AngularCuts2DMinimum_AfterAllSelections",
        #histoName="ImprovedDeltaPhiCuts2DMinimum",
        #details={ "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
            #"ylabel": "#Delta#phi(jet_{1..3},E_{T}^{miss})",
            #"divideByBinWidth": False,
            #"unit": "{}^{o}",
            #"log": False,
            #"legendPosition": "NW",
            #"opts": {"zmin": 0.0} }))
    ControlPlots.append(ControlPlotInput(title="DeltaPhiTauMet_AfterAllSelections",
        histoName="DeltaPhiTauMet_AfterAllSelections",
        details={ "xlabel": "#Delta#phi(#tau,E_{T}^{miss})",
          "ylabel": "Events",
        "divideByBinWidth": False,
        "unit": "{}^{o}",
        "log": True,
        "legendPosition": "NW",
        "opts": {"ymin": 0.9} }))
    #ControlPlots.append(ControlPlotInput(title="MinDeltaPhiTauJet_AfterAllSelections",
        #histoName="MinDeltaPhiTauJet_AfterAllSelections",
        #details={ "xlabel": "min (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
            #"ylabel": "Events",
            #"divideByBinWidth": False,
            #"unit": "{}^{o}",
            #"log": True,
            #"legendPosition": "NW",
            #"opts": {"ymin": 0.9} }))
    #ControlPlots.append(ControlPlotInput(title="MaxDeltaPhiTauJet_AfterAllSelections",
        #histoName="MaxDeltaPhiTauJet_AfterAllSelections",
        #details={ "xlabel": "max (#Delta#phi(jet_{1..3},E_{T}^{miss}))",
            #"ylabel": "Events",
            #"divideByBinWidth": False,
            #"unit": "{}^{o}",
            #"log": True,
            #"legendPosition": "NW",
            #"opts": {"ymin": 0.9} }))
    #ControlPlots.append(ControlPlotInput(title="DeltaPhi_AfterAllSelections",
        #histoName="deltaPhi_AfterAllSelections",
        #details={ "bins": 11,
            #"rangeMin": 0.0,
            #"rangeMax": 180.0,
            #"variableBinSizeLowEdges": [0., 10., 20., 30., 40., 60., 80., 100., 120., 140., 160.], # if an empty list is given, then uniform bin width is used                         #"binLabels": [], # leave empty to disable bin labels                         #"xlabel": "#Delta#phi(#tau_{h},^{}E_{T}^{miss})",
            #"ylabel": "Events",
            #"unit": "^{o}",
            #"log": True,
            #"DeltaRatio": 0.5,
            #"ymin": 0.9,
            #"ymax": -1},
        #blindedRange=[-1, 300], # specify range min,max if blinding applies to this control plot
        #flowPlotCaption="^{}N_{b jets}", # Leave blank if you don't want to include the item to the selection flow plot
        #))
    #ControlPlots.append(ControlPlotInput(title="MaxDeltaPhi",
        #histoName="maxDeltaPhiJetMet",
        #details={ "bins": 18,
            #"rangeMin": 0.0,
            #"rangeMax": 180.0,
            #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used                         #"binLabels": [], # leave empty to disable bin labels                         #"xlabel": "max(#Delta#phi(jet,^{}E_{T}^{miss})",
            #"ylabel": "Events",
            #"unit": "^{o}",
            #"log": True,
            #"DeltaRatio": 0.5,
            #"ymin": 0.9,
            #"ymax": -1},
        #blindedRange=[-1, 300], # specify range min,max if blinding applies to this control plot
        #flowPlotCaption="#Delta#phi(^{}#tau_{h},^{}E_{T}^{miss})", # Leave blank if you don't want to include the item to the selection flow plot
        #))
    #ControlPlots.append(ControlPlotInput(title="WMass",
        #histoName="WMass",
        #details={ "bins": 20,
            #"rangeMin": 0.0,
            #"rangeMax": 200.0,
            #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used                         #"binLabels": [], # leave empty to disable bin labels                         #"xlabel": "m_{jj}",
            #"ylabel": "Events",
            #"unit": "GeV/c^{2}",
            #"log": True,
            #"DeltaRatio": 0.5,
            #"ymin": 0.9,
            #"ymax": -1},
        #blindedRange=[-1, 400], # specify range min,max if blinding applies to this control plot
        #flowPlotCaption="", # Leave blank if you don't want to include the item to the selection flow plot
        #))
    #ControlPlots.append(ControlPlotInput(title="TopMass",
        #histoName="TopMass",
        #details={ "bins": 20,
            #"rangeMin": 0.0,
            #"rangeMax": 400.0,
            #"variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used                         #"binLabels": [], # leave empty to disable bin labels                         #"xlabel": "m_{bjj}",
            #"ylabel": "Events",
            #"unit": "GeV/c^{2}",
            #"log": True,
            #"DeltaRatio": 0.5,
            #"ymin": 0.9,
            #"ymax": -1},
        #blindedRange=[-1, 400], # specify range min,max if blinding applies to this control plot
        #flowPlotCaption="", # Leave blank if you don't want to include the item to the selection flow plot
        #))
    ControlPlots.append(ControlPlotInput(title="BackToBackAngularCutsMinimum_AfterAllSelections",
        histoName="BackToBackAngularCutsMinimum_AfterAllSelections",
        details={ #"xlabel": "min(#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1..3},MET)^{2}})",
          "xlabel": "R_{bb}^{min}",
          "ylabel": "Events",
          "divideByBinWidth": False,
          "unit": "^{o}",
          "log": True,
          "legendPosition": "NE",
          "opts": {"ymin": 0.09} }))
