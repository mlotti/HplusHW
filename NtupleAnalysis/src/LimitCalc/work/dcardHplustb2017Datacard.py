# This is the first attempt to generate datacards for H+ -> tb analysis
# Run as: ./dcardGenerator.py -x dcardHplustb2017Datacard.py -d [directory-containing-multicrab-named-SignalAnalysis_*]

import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics

DataCardName ='Hplus2tb_13TeV'

LightMassPoints = [] # This is needed to inform the dcard generator that light H+ is not considered
HeavyMassPoints = [180,200,220,250,300,350,400,500,800,1000,2000,3000] # list of mass points to produce datacards
MassPoints=HeavyMassPoints

##############################################################################
# Options
OptionIncludeSystematics=False # Include shape systematics (after multicrab has been produced with doSystematics=True)
OptionDoControlPlots= not True # If you want control plots, switch this to true and define control plots in the end of this file
BlindAnalysis=True # Keep this always as True, unless you have a green light for unblinding and you know what you are doing
OptionMassShape="LdgTetrajetMass" # Set the distribution used in limit extraction
OptionGenuineTauBackgroundSource="MC_FakeAndGenuineTauNotSeparated"   # Choose "MC_FakeAndGenuineTauNotSeparated" or "Embedding"
OptionCombineSingleColumnUncertainties=False # Approxmation that makes limit running faster (normally not needed)
OptionLimitOnSigmaBr = True # Set to true for heavy H+
OptionDisplayEventYieldSummary=True
OptionNumberOfDecimalsInSummaries=1
OptionDoTBbarForHeavy=False # A flag related to combination of different channels in 2012, keep always as False
ToleranceForLuminosityDifference=0.05 # Tolerance for throwing error on luminosity difference (0.01=1 percent agreement is required)
ToleranceForMinimumRate=0.0 # Tolerance for almost zero rate (columns with smaller rate are suppressed)
MinimumStatUncertainty=0.5 # Minimum stat. uncertainty to set to bins with zero events
labelPrefix="" # Prefix for the labels of datacard columns, e.g. "Hplus2tb_"

# Convert the following nuisances from shape to constant (an approximation that makes the limits run faster and converge more easily)
OptionConvertFromShapeToConstantList=[]

# Separate in the following shape nuisances the shape and normalization components
OptionSeparateShapeAndNormalizationFromSystVariationList=[]

# Options for tables, figures etc.
OptionBr=0.01  # Br(t->bH+)
OptionSqrtS=13 # sqrt(s)

##############################################################################
# Counter and histogram path definitions

# Rate counter definitions
SignalRateCounter="Selected events"
FakeRateCounter="EWKfaketaus:SelectedEvents"

# Shape histogram definitions
shapeHistoName=None
if OptionMassShape =="LdgTetrajetMass":
    shapeHistoName="LdgTetrajetMass_AfterAllSelections"
histoPathInclusive="ForDataDrivenCtrlPlots"
ShapeHistogramsDimensions=systematics.getBinningForPlot(shapeHistoName)
DataCardName +="_"+OptionMassShape

##############################################################################
# Observation definition (how to retrieve number of observed events)
#
from HiggsAnalysis.LimitCalc.InputClasses import ObservationInput
Observation=ObservationInput(datasetDefinition="Data", shapeHistoName=shapeHistoName, histoPath=histoPathInclusive)

##############################################################################
# TODO: Define systematics lists commmon to datasets
myTrgSystematics= [] #["CMS_eff_t_trg_data","CMS_eff_t_trg_MC", # Trigger tau part
                     #"CMS_eff_met_trg_data","CMS_eff_met_trg_MC"] # Trigger MET part
myTauIDSystematics=["CMS_eff_t"] #tau ID
#myTauIDSystematics.extend(["CMS_eff_t_highpt"])
#myTauMisIDSystematics=["CMS_fake_eToTau","CMS_fake_muToTau","CMS_fake_jetToTau"] # tau mis-ID
myESSystematics=["CMS_scale_t","CMS_scale_j","CMS_res_j","CMS_scale_met"] # TES, JES, CMS_res_j, UES #FIXME
myBtagSystematics=["CMS_eff_b","CMS_fake_b"] # b tag and mistag
myTopSystematics=["CMS_Hptntj_topPtReweight"] # top pt reweighting
myPileupSystematics=["CMS_pileup"] # CMS_pileup
myLeptonVetoSystematics=[] #["CMS_eff_e_veto","CMS_eff_m_veto"] # CMS_pileup

myShapeSystematics=[]
myShapeSystematics.extend(myTrgSystematics)
#myShapeSystematics.extend(["CMS_eff_t_highpt"])
#myShapeSystematics.extend(myTauMisIDSystematics)
myShapeSystematics.extend(myESSystematics)
myShapeSystematics.extend(myBtagSystematics)
myShapeSystematics.extend(myTopSystematics)
myShapeSystematics.extend(myPileupSystematics)

if not OptionIncludeSystematics:
    myShapeSystematics=[]

##############################################################################
# DataGroup (i.e. columns in datacard) definitions
from HiggsAnalysis.LimitCalc.InputClasses import DataGroup
DataGroups=[]
EmbeddingIdList=[]
EWKFakeIdList=[]
mergeColumnsByLabel=[]

# Signal datasets
signalTemplate=DataGroup(datasetType="Signal", histoPath=histoPathInclusive, shapeHistoName=shapeHistoName)
for mass in MassPoints:
    myMassList=[mass]
    hx=signalTemplate.clone()
    hx.setLabel("Hp"+str(mass)+"_a")
    hx.setLandSProcess(1)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(#myTrgSystematics[:]+myTauIDSystematics[:] #+myTauMisIDSystematics[:]
                    #+myESSystematics[:]+myBtagSystematics[:]+myPileupSystematics[:]+myLeptonVetoSystematics[:]+
        ["lumi_13TeV"])
    hx.setDatasetDefinition("ChargedHiggs_HplusTB_HplusToTB_M_"+str(mass))
    DataGroups.append(hx)

# FakeB dataset
myFakeB=DataGroup(label=labelPrefix+"FakeBmeasurement", landsProcess=2, validMassPoints=MassPoints,
                datasetType="Embedding", datasetDefinition="FakeBMeasurementTrijetMass",
                nuisances=["lumi_13TeV"],
                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive)
DataGroups.append(myFakeB)


# Option to use a data-driven method ("embedding")
if OptionGenuineTauBackgroundSource =="DataDriven":
    # EWK genuine taus from embedding
    myEmbDataDrivenNuisances=[]
    EmbeddingIdList=[3]
    DataGroups.append(DataGroup(label="CMS_Hptntj_EWK_Tau", landsProcess=3, 
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding", 
                                datasetDefinition="Data", 
                                validMassPoints=MassPoints, 
                                nuisances=myEmbeddingShapeSystematics[:]+myEmbDataDrivenNuisances[:]
                                ))
else:
    # TT
    DataGroups.append(DataGroup(label=labelPrefix+"TT", landsProcess=3,
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding",
                                datasetDefinition="TT",
                                validMassPoints=MassPoints,
                                nuisances=["lumi_13TeV"]))
    # WJetsToQQ
    DataGroups.append(DataGroup(label=labelPrefix+"TTWJetsToQQ", landsProcess=4,
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding", 
                                datasetDefinition="TTWJetsToQQ",
                                validMassPoints=MassPoints,
                                nuisances=["lumi_13TeV"]))
    # TTZToQQ
    DataGroups.append(DataGroup(label=labelPrefix+"TTZToQQ", landsProcess=5,
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding", 
                                datasetDefinition="TTZToQQ",
                                validMassPoints=MassPoints,
                                nuisances=["lumi_13TeV"]))
    # TTTT
    DataGroups.append(DataGroup(label=labelPrefix+"TTTT", landsProcess=6,
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding", 
                                datasetDefinition="TTTT",
                                validMassPoints=MassPoints,
                                nuisances=["lumi_13TeV"]))
    # SingleTop
    DataGroups.append(DataGroup(label=labelPrefix+"SingleTop", landsProcess=7,
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding",
                                datasetDefinition="SingleTop",
                                validMassPoints=MassPoints,
                                nuisances=["lumi_13TeV"]))
    # DYJetsToQQ
    DataGroups.append(DataGroup(label=labelPrefix+"DYJetsToQQ", landsProcess=8,
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive,
                                datasetType="Embedding",
                                datasetDefinition="DYJetsToQQHT",
                                validMassPoints=MassPoints,
                                nuisances=["lumi_13TeV"]))
    # Diboson
    DataGroups.append(DataGroup(label=labelPrefix+"Diboson", landsProcess=9,
                                shapeHistoName=shapeHistoName, histoPath=histoPathInclusive, 
                                datasetType="Embedding", 
                                datasetDefinition="Diboson",
                                validMassPoints=MassPoints,
                                nuisances=["lumi_13TeV"]))


##############################################################################
# TODO: Definition of nuisance parameters
from HiggsAnalysis.LimitCalc.InputClasses import Nuisance
ReservedNuisances=[]
Nuisances=[]

#=====tau ID and mis-ID
# tau ID
Nuisances.append(Nuisance(id="CMS_eff_t", label="tau-jet ID (no Rtau) uncertainty for genuine taus",
    distr="lnN", function="Constant", value=0.10))
Nuisances.append(Nuisance(id="CMS_eff_t_forQCD", label="tau-jet ID uncertainty for genuine taus",
    distr="lnN", function="ConstantForQCD", value=0.10))
# tau ID high-pT
if "CMS_eff_t_highpt" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_eff_t_highpt", label="tau-jet ID high-pt uncertainty for genuine taus",
        distr="shapeQ", function="ShapeVariation", systVariation="TauIDSyst"))       
#=====tau and MET trg
if "CMS_eff_t_trg_data" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_eff_t_trg_data", label="tau+MET trg tau part data eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="TauTrgEffData"))
else:
    Nuisances.append(Nuisance(id="CMS_eff_t_trg_data", label="APPROXIMATION for tau+MET trg tau part data eff.",
        distr="lnN", function="Constant", value=0.03))
if "CMS_eff_t_trg_MC" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_eff_t_trg_MC", label="tau+MET trg tau part MC eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="TauTrgEffMC"))
else:
    Nuisances.append(Nuisance(id="CMS_eff_t_trg_MC", label="APPROXIMATION for tau+MET trg tau part MC eff.",
        distr="lnN", function="Constant", value=0.04))
if "CMS_eff_met_trg_data" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_eff_met_trg_data", label="tau+MET trg MET data eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="METTrgEffData"))
else:
    Nuisances.append(Nuisance(id="CMS_eff_met_trg_data", label="APPROXIMATION for tau+MET trg MET data eff.",
        distr="lnN", function="Constant", value=0.2))
if "CMS_eff_met_trg_MC" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_eff_met_trg_MC", label="tau+MET trg MET MC eff.",
        distr="shapeQ", function="ShapeVariation", systVariation="METTrgEffMC"))
else:
    Nuisances.append(Nuisance(id="CMS_eff_met_trg_MC", label="APPROXIMATION for tau+MET trg MET MC eff.",
        distr="lnN", function="Constant", value=0.01))

#=====lepton veto
'''
Nuisances.append(Nuisance(id="CMS_eff_e_veto", label="e veto",
    distr="lnN", function="Ratio",
    numerator="passed e selection (Veto)", # main counter name after electron veto
    denominator="Met trigger SF", # main counter name before electron and muon veto
    scaling=0.02
))
Nuisances.append(Nuisance(id="CMS_eff_m_veto", label="mu veto",
    distr="lnN", function="Ratio",
    numerator="passed mu selection (Veto)", # main counter name after electron and muon veto
    denominator="passed e selection (Veto)", # main counter name before muon veto
    scaling =0.01
)) 
'''
#===== b tag and mistag SF
if "CMS_eff_b" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_eff_b", label="b tagging",
        distr="shapeQ", function="ShapeVariation", systVariation="BTagSF"))
else:
    Nuisances.append(Nuisance(id="CMS_eff_b", label="APPROXIMATION for b tagging",
        distr="lnN", function="Constant",value=0.05))
if "CMS_fake_b" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_fake_b", label="b mistagging",
        distr="shapeQ", function="ShapeVariation", systVariation="BMistagSF"))
else:
    Nuisances.append(Nuisance(id="CMS_fake_b", label="APPROXIMATION for b mistagging",
        distr="lnN", function="Constant",value=0.02))

# e->tau mis-ID
#if "CMS_fake_eToTau" in myShapeSystematics:
#    Nuisances.append(Nuisance(id="CMS_fake_eToTau", label="tau-jet ID (no Rtau) e->tau",
#        distr="shapeQ", function="ShapeVariation", systVariation="FakeTauElectron"))
#else:
#    Nuisances.append(Nuisance(id="CMS_fake_eToTau", label="APPROXIMATION for tau-jet ID (no Rtau) e->tau",
#        distr="lnN", function="Constant", value=0.001))
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
#if "CMS_fake_muToTau" in myShapeSystematics:
#    Nuisances.append(Nuisance(id="CMS_fake_muToTau", label="tau-jet ID (no Rtau) mu->tau",
#        distr="shapeQ", function="ShapeVariation", systVariation="FakeTauMuon"))
#else:
#    Nuisances.append(Nuisance(id="CMS_fake_muToTau", label="APPROXIMATION for tau-jet ID (no Rtau) mu->tau",
#        distr="lnN", function="Constant", value=0.001))
# jet->tau mis-ID
#if "CMS_fake_jetToTau" in myShapeSystematics:
#    Nuisances.append(Nuisance(id="CMS_fake_jetToTau", label="tau-jet ID (no Rtau) jet->tau",
#        distr="shapeQ", function="ShapeVariation", systVariation="FakeTauJet"))
#else:
#    Nuisances.append(Nuisance(id="CMS_fake_jetToTau", label="APPROXIMATION for tau-jet ID (no Rtau) jet->tau",
#        distr="lnN", function="Constant", value=0.01))

#===== energy scales
# tau ES
if "CMS_scale_t" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_scale_t", label="Tau energy scale",
        distr="shapeQ", function="ShapeVariation", systVariation="TauES"))
else:
    Nuisances.append(Nuisance(id="CMS_scale_t", label="APPROXIMATION for tau ES",
        distr="lnN", function="Constant", value=0.06))
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
        distr="shapeQ", function="ShapeVariation", systVariation="UES"))
else:
    Nuisances.append(Nuisance(id="CMS_scale_met", label="APPROXIMATION for unclustered MET ES",
        distr="lnN", function="Constant",value=0.03))
# CMS_res_j
if "CMS_res_j" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_res_j", label="Jet energy resolution",
        distr="shapeQ", function="ShapeVariation", systVariation="JER"))
else:
    Nuisances.append(Nuisance(id="CMS_res_j", label="APPROXIMATION for CMS_res_j",
        distr="lnN", function="Constant",value=0.04))

#===== Top pt SF
if "CMS_Hptntj_topPtReweight" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_Hptntj_topPtReweight", label="top pT reweighting",
        distr="shapeQ", function="ShapeVariation", systVariation="TopPt"))
else:
    Nuisances.append(Nuisance(id="CMS_Hptntj_topPtReweight", label="APPROXIMATION for top pT reweighting",
        distr="lnN", function="Constant",value=0.25))

#===== Pileup
if "CMS_pileup" in myShapeSystematics:
    Nuisances.append(Nuisance(id="CMS_pileup", label="CMS_pileup",
        distr="shapeQ", function="ShapeVariation", systVariation="PUWeight"))
else:
    Nuisances.append(Nuisance(id="CMS_pileup", label="APPROXIMATION for CMS_pileup",
        distr="lnN", function="Constant",value=0.05))

#===== Cross section uncertainties

# ttbar
Nuisances.append(Nuisance(id="CMS_scale_ttbar", label="ttbar cross section scale uncertainty ",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyUp()))
Nuisances.append(Nuisance(id="CMS_pdf_ttbar", label="ttbar pdf uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("TTJets_pdf").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("TTJets_pdf").getUncertaintyUp()))
Nuisances.append(Nuisance(id="CMS_mass_ttbar", label="ttbar top mass uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("TTJets_mass").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("TTJets_mass").getUncertaintyUp()))

# ttbar for QCD
Nuisances.append(Nuisance(id="CMS_scale_ttbar_forQCD", label="ttbar cross section scale uncertainty ",
    distr="lnN", function="ConstantForQCD",
    value=systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyUp()))
Nuisances.append(Nuisance(id="CMS_pdf_ttbar_forQCD", label="ttbar pdf uncertainty",
    distr="lnN", function="ConstantForQCD",
    value=systematics.getCrossSectionUncertainty("TTJets_pdf").getUncertaintyDown()))
Nuisances.append(Nuisance(id="CMS_mass_ttbar_forQCD", label="ttbar top mass uncertainty",
    distr="lnN", function="ConstantForQCD",
    value=systematics.getCrossSectionUncertainty("TTJets_mass").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("TTJets_mass").getUncertaintyUp()))
    
# WJets
Nuisances.append(Nuisance(id="CMS_scale_Wjets", label="W+jets cross section scale uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("WJets_scale").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("WJets_scale").getUncertaintyUp()))
Nuisances.append(Nuisance(id="CMS_pdf_Wjets", label="W+jets pdf uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("WJets_pdf").getUncertaintyDown()))


# Single top
Nuisances.append(Nuisance(id="CMS_scale_singleTop", label="single top cross section sale uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("SingleTop_scale").getUncertaintyDown()))
Nuisances.append(Nuisance(id="CMS_pdf_singleTop", label="single top pdf ucnertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("SingleTop_pdf").getUncertaintyDown()))

# DY
Nuisances.append(Nuisance(id="CMS_scale_DY", label="Z->ll cross section scale uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("DYJetsToLL_scale").getUncertaintyDown(),
    upperValue=systematics.getCrossSectionUncertainty("DYJetsToLL_scale").getUncertaintyUp()))
Nuisances.append(Nuisance(id="CMS_pdf_DY", label="Z->ll pdf uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("DYJetsToLL_pdf").getUncertaintyDown()))

# Diboson
Nuisances.append(Nuisance(id="CMS_scale_VV", label="diboson cross section scale uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("Diboson_scale").getUncertaintyDown()))
Nuisances.append(Nuisance(id="CMS_pdf_VV", label="diboson pdf uncertainty",
    distr="lnN", function="Constant",
    value=systematics.getCrossSectionUncertainty("Diboson_pdf").getUncertaintyDown()))

#===== Luminosity
Nuisances.append(Nuisance(id="lumi_13TeV", label="lumi_13TeVnosity",
    distr="lnN", function="Constant",
    value=systematics.getLuminosityUncertainty("2016")))
Nuisances.append(Nuisance(id="lumi_13TeV_forQCD", label="lumi_13TeVnosity",
    distr="lnN", function="ConstantForQCD",
    value=systematics.getLuminosityUncertainty("2016")))

#===== QCD measurement
if OptionIncludeSystematics:
    Nuisances.append(Nuisance(id="CMS_Hptntj_FakeTauBG_templateFit", label="QCDInv: fit", 
        distr="lnN", function="Constant", value=0.03))
    Nuisances.append(Nuisance(id="CMS_Hptntj_QCDkbg_metshape", label="QCD met shape syst.",
        distr="shapeQ", function="QCDShapeVariation", systVariation="QCDNormSource"))

#===== Merge nuisances to same row (first item specifies the name for the row)
MergeNuisances=[]

# Correlate ttbar and single top xsect uncertainties
MergeNuisances.append(["CMS_scale_ttbar","CMS_scale_singleTop"])
MergeNuisances.append(["CMS_pdf_ttbar","CMS_pdf_singleTop"])

# Merge QCDandFakeTau nuisances to corresponding t_genuine nuisances
MergeNuisances.append(["CMS_eff_t","CMS_eff_t_forQCD"])
MergeNuisances.append(["CMS_scale_ttbar", "CMS_scale_ttbar_forQCD"])
MergeNuisances.append(["CMS_pdf_ttbar", "CMS_pdf_ttbar_forQCD"])
MergeNuisances.append(["CMS_mass_ttbar", "CMS_mass_ttbar_forQCD"])
MergeNuisances.append(["lumi_13TeV", "lumi_13TeV_forQCD"])

# Convert shape systematics to constants if asked
from HiggsAnalysis.LimitCalc.InputClasses import convertFromSystVariationToConstant
convertFromSystVariationToConstant(Nuisances, OptionConvertFromShapeToConstantList)

# Separate the shape nuisances and the shape and normalization components if asked
from HiggsAnalysis.LimitCalc.InputClasses import separateShapeAndNormalizationFromSystVariation
separateShapeAndNormalizationFromSystVariation(Nuisances, OptionSeparateShapeAndNormalizationFromSystVariationList)

# Control plots
from HiggsAnalysis.LimitCalc.InputClasses import ControlPlotInput
ControlPlots=[]
EWKPath="ForDataDrivenCtrlPlotsEWKGenuineTaus"
# If you want to create control plots, add them to the list like this:
#ControlPlots.append(ControlPlotInput(
#    title            = "SelectedTau_pT_AfterStandardSelections",
#    histoName        = "SelectedTau_pT_AfterStandardSelections",
#    details          = { "xlabel": "Selected #tau ^{}p_{T}",
#                         "ylabel": "Events/^{}#Deltap_{T}",
#                         "divideByBinWidth": True,
#                         "unit": "GeV/c",
#                         "log": True,
#                         "legendPosition": "NE",
#                         "opts": {"ymin": 0.0009, "ymaxfactor": 25, "xmax": 500} }))
