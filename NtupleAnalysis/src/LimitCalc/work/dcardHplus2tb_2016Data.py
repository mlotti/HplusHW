'''
DESCRIPTION:
This is a datacard template for 2016 results. 
It can be used to generate datacards for H+ -> tb analysis, 
in the fully hadronic final state. 


USAGE:
./dcardGenerator.py -x dcardHplus2tb2017Datacard_v2.py -d [directory-containing-multicrab-named-SignalAnalysis_*]


EXAMPLES:
./dcardGenerator_v2.py -x dcardHplus2tb_2016Data.py -d limits2016/ --ht2b


LAST USED:
./dcardGenerator_v2.py -x dcardHplus2tb_2016Data.py -d limits2016/ --ht2b

'''
#================================================================================================  
# Imports
#================================================================================================  
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import sys

#================================================================================================
# Function Definition
#================================================================================================
def Print(msg, printHeader=False):
    if not Verbose:
        return
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

#================================================================================================  
# Options
#================================================================================================  
DataCardName                           = 'Hplus2tb_13TeV'
MassPoints                             = [180, 200, 220, 250, 300, 350, 400, 500, 650, 800, 1000, 1500, 2000, 2500, 3000]#, 5000, 7000, 10000]
BlindAnalysis                          = True  # True, unless you have a green light for unblinding! [default: True]
OptionBlindThreshold                   = 0.2   # [default: 0.2]    (If signal exceeds this fraction of expected events, data is blinded; set to None to disable)
MinimumStatUncertainty                 = 0.5   # [default: 0.5]    (Minimum stat. uncertainty to set to bins with zero events)
UseAutomaticMinimumStatUncertainty     = False # Option to NOT use the MinimumStatUncertainty value above for ~empty bins, but instead determine the value from the lowest non-zero bin for each column
OptionCombineSingleColumnUncertainties = False # [default: False]  (Approxmation that makes limit running faster)
OptionConvertFromShapeToConstantList   = []    # [default: []]     (Convert these nuisances from shape to constant; Approx. that makes limits run faster & converge more easily)
OptionDisplayEventYieldSummary         = False # [default: False]  (Print "Event yield summary", using the TableProducer.py)
OptionDoControlPlots                   = True  # [default: True]   (Produce control plots defined at end of this file)
OptionFakeBMeasurementSource           = "DataDriven" # [default: "DataDriven"] (options: "DataDriven", "MC")
OptionIncludeSystematics               = False # [default: False]  (Shape systematics; Requires pseudo-multicrab produced with doSystematics=True) 
OptionLimitOnSigmaBr                   = True  # [default: True]   (Set to true for heavy H+)
OptionMassShape                        = "LdgTetrajetMass_AfterAllSelections"
OptionNumberOfDecimalsInSummaries      = 1     # [defaul: 1]       (Self explanatory)
OptionSeparateShapeAndNormalizationFromSystVariationList=[] # [default: []]  (Separate in the following shape nuisances the shape and normalization components)
ToleranceForLuminosityDifference       = 0.05  # [default: 0.05]   (Tolerance for throwing error on luminosity difference; "0.01" means that a 1% is required) 
ToleranceForMinimumRate                = 0.0   # [default: 0.0]    (Tolerance for almost zero rate columns with smaller rate are suppressed) 
labelPrefix                            = "CMS_H2tb_" # [default: ""] (Prefix for the labels of datacard columns; e.g. labelPrefix="CMS_Hptntj_" )
# Options for tables, figures etc.
OptionBr   = 0.01  # Br(t->bH+)
OptionSqrtS= 13    # sqrt(s)

#================================================================================================  
# Counter and histogram path definitions
#================================================================================================  
SignalRateCounter  = "Selected events"            # fixme: what is this for?
FakeRateCounter    = "EWKfaketaus:SelectedEvents" # fixme: what is this for?
histoPathInclusive = "ForDataDrivenCtrlPlots"
histoPathFakeB     = "ForDataDrivenCtrlPlots"
histoPathGenuineB  = histoPathInclusive + "EWKGenuineB"
ShapeHistogramsDimensions = systematics.getBinningForPlot(OptionMassShape) # Get the new binning for the shape histogram

#================================================================================================  
# Observation definition (how to retrieve number of observed events)
#================================================================================================  
from HiggsAnalysis.LimitCalc.InputClasses import ObservationInput
Observation = ObservationInput(datasetDefinition="Data", shapeHistoName=OptionMassShape, histoPath=histoPathInclusive)

#================================================================================================  
# Define systematics lists commmon to datasets
#================================================================================================  
# Luminosity uncertainty
myLumiSystematics = ["lumi_13TeV"]

# Currently (21 Sep 2017) no Trigger SF is used
myTrgSystematics = [] 
# myTrgSystematics = ["CMS_eff_trg_data", "CMS_eff_trg_MC"], # Trigger efficiency

# No tau-ID in Hplus2tb (veto on taus to ensure orthogonality with Hplus2TauNu
myTauIDSystematics = []
# myTauIDSystematics = ["CMS_eff_t"]
# myTauIDSystematics.extend(["CMS_eff_t_highpt"])

# No tau mis-ID in Hplus2tb (veto on taus to ensure orthogonality with Hplus2TauNu
myTauMisIDSystematics = []
# myTauMisIDSystematics = ["CMS_fake_eToTau","CMS_fake_muToTau","CMS_fake_jetToTau"] 

# Tau Energy Scale (TES), Jet Energy Scale (JES), Jet Energy Resolution (JER) i.e. TES, JES, CMS_res_j, UES 
myESSystematics = ["CMS_scale_t","CMS_scale_j","CMS_res_j","CMS_scale_met"] #fixme: is this okay?

# B-tag and mistag
myBtagSystematics = ["CMS_eff_b","CMS_fake_b"] 

# Top pt reweighting
myTopSystematics = ["CMS_Hptntj_topPtReweight"]

# CMS_pileup
myPileupSystematics=["CMS_pileup"] 

# Lepton Veto 
myLeptonVetoSystematics=[] #["CMS_eff_e_veto","CMS_eff_m_veto"]

# All Shape-related systematics
myShapeSystematics=[]
myShapeSystematics.extend(myTrgSystematics)
myShapeSystematics.extend(myESSystematics)
myShapeSystematics.extend(myBtagSystematics)
myShapeSystematics.extend(myTopSystematics)
myShapeSystematics.extend(myPileupSystematics)

if not OptionIncludeSystematics:
    myShapeSystematics=[]

# Inform user of the list of systematics
nSystematics = len(myShapeSystematics)
if nSystematics>0:
    Print("A total of %s shape-related systematics will be considered." % nSystematics, True)

#================================================================================================  
# DataGroup (i.e. columns in datacard) definitions
#================================================================================================ 
from HiggsAnalysis.LimitCalc.InputClasses import DataGroup
DataGroups         = []
EWKFakeIdList      = []
mergeColumnsByLabel= []

# Signal datasets
# ===============
signalTemplate  = DataGroup(datasetType="Signal", histoPath=histoPathInclusive, shapeHistoName=OptionMassShape)
signalNuisances = myLumiSystematics

# signalNuisances = myLumiSystematics[:] + myPileupSystematics[:] + myTrgSystematics[:] + myLeptonVetoSystematics[:] + myESSystematics[:] + myBtagSystematics[:]
# signalNuisances+= myTauIDSystematics[:] + myTauMisIDSystematics[:] 

# For-loop: All mass points
for mass in MassPoints:
    myMassList=[mass]
    hx=signalTemplate.clone()
    hx.setLabel("Hp" + str(mass) + "_a") #fixme: what is the "_a" for?
    hx.setLandSProcess(1)                #fixme: what is it for?
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(signalNuisances)
    hx.setDatasetDefinition("ChargedHiggs_HplusTB_HplusToTB_M_%s" % (mass))
    DataGroups.append(hx)


myFakeB = DataGroup(label             = labelPrefix + "FakeBmeasurement",
                    landsProcess      = 2, #fixme: what is it for?
                    validMassPoints   = MassPoints,
                    datasetType       = "FakeB", #FakeB
                    datasetDefinition = "FakeBMeasurementTrijetMass",
                    nuisances         = myLumiSystematics,
                    shapeHistoName    = OptionMassShape,
                    histoPath         = histoPathInclusive)

myQCD = DataGroup(label             = labelPrefix + "QCD",
                  landsProcess      = 2, #fixme: what is it for?
                  validMassPoints   = MassPoints,
                  datasetType       = "QCDMC", #QCDMC
                  datasetDefinition = "QCD",
                  nuisances         = myLumiSystematics,
                  shapeHistoName    = OptionMassShape,
                  histoPath         = histoPathInclusive)

if OptionFakeBMeasurementSource == "DataDriven":
    DataGroups.append(myFakeB)

    # EWK Datasets should only be Genuibe-b (FakeB = QCD inclusive + EWK GenuineB)
    histoPathEWK = histoPathGenuineB
    dsetTypeEWK  = "GenuineB"

else:
    DataGroups.append(myQCD)

    # EWK Datasets should be inclusive (Bkg = QCD inclusive + EWK inclusive)
    histoPathEWK = histoPathInclusive
    dsetTypeEWK  = "EWKMC"


# TT
DataGroups.append(DataGroup(label             = labelPrefix + "TT",
                            landsProcess      = 3,
                            shapeHistoName    = OptionMassShape, 
                            histoPath         = histoPathEWK,
                            datasetType       = dsetTypeEWK,                            
                            datasetDefinition = "TT", 
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
                  )


# SingleTop
DataGroups.append(DataGroup(label             = labelPrefix + "SingleTop", 
                            landsProcess      = 4,
                            shapeHistoName    = OptionMassShape,
                            histoPath         = histoPathEWK,
                            datasetType       = dsetTypeEWK,
                            datasetDefinition = "SingleTop",
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
                  )

# TTZToQQ
DataGroups.append(DataGroup(label             = labelPrefix + "TTZToQQ", 
                            landsProcess      = 5,
                            shapeHistoName    = OptionMassShape,
                            histoPath         = histoPathEWK,
                            datasetType       = dsetTypeEWK,
                            datasetDefinition = "TTZToQQ",
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
                  )

# TTTT
DataGroups.append(DataGroup(label             = labelPrefix + "TTTT",
                            landsProcess      = 6,
                            shapeHistoName    = OptionMassShape,
                            histoPath         = histoPathEWK,
                            datasetType       = dsetTypeEWK,
                            datasetDefinition = "TTTT",
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
                  )

# DYJetsToQQ
DataGroups.append(DataGroup(label             = labelPrefix + "DYJetsToQQ", 
                            landsProcess      = 7,
                            shapeHistoName    = OptionMassShape,
                            histoPath         = histoPathEWK,
                            datasetType       = dsetTypeEWK,
                            datasetDefinition = "DYJetsToQQHT",
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
                  )

# tt+W
DataGroups.append(DataGroup(label             = labelPrefix + "TTWJetsToQQ", 
                            landsProcess      = 8,
                            shapeHistoName    = OptionMassShape, 
                            histoPath         = histoPathEWK,
                            datasetType       = dsetTypeEWK,
                            datasetDefinition = "TTWJetsToQQ",
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
                  )

# W+jets
DataGroups.append(DataGroup(label             = labelPrefix + "WJetsToQQ_HT_600ToInf",
                            landsProcess      = 9,
                            shapeHistoName    = OptionMassShape,
                            histoPath         = histoPathEWK, 
                            datasetType       = dsetTypeEWK,
                            datasetDefinition = "WJetsToQQ_HT_600ToInf",
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
)

# Diboson
DataGroups.append(DataGroup(label             = labelPrefix + "Diboson",
                            landsProcess      = 10,
                            shapeHistoName    = OptionMassShape,
                            histoPath         = histoPathEWK, 
                            datasetType       = dsetTypeEWK,
                            datasetDefinition = "Diboson",
                            validMassPoints   = MassPoints,
                            nuisances         = myLumiSystematics
                            )
                  )


#================================================================================================ 
# Definition of nuisance parameters
#================================================================================================ 
from HiggsAnalysis.LimitCalc.InputClasses import Nuisance

# Some definitions first
ReservedNuisances    = []
Nuisances            = []
tt_xs_down           = systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyDown()
tt_xs_up             = systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyUp()
tt_pdf_down          = systematics.getCrossSectionUncertainty("TTJets_pdf").getUncertaintyDown()
tt_pdf_up            = systematics.getCrossSectionUncertainty("TTJets_pdf").getUncertaintyUp()
tt_mass_down         = systematics.getCrossSectionUncertainty("TTJets_mass").getUncertaintyDown()
tt_mass_up           = systematics.getCrossSectionUncertainty("TTJets_mass").getUncertaintyUp()
wjets_scale_down     = systematics.getCrossSectionUncertainty("WJets_scale").getUncertaintyDown()
wjets_scale_up       = systematics.getCrossSectionUncertainty("WJets_scale").getUncertaintyUp()
wjets_pdf_down       = systematics.getCrossSectionUncertainty("WJets_pdf").getUncertaintyDown()
singleTop_scale_down = systematics.getCrossSectionUncertainty("SingleTop_scale").getUncertaintyDown()
singleTop_pdf_down   = systematics.getCrossSectionUncertainty("SingleTop_pdf").getUncertaintyDown()
DY_scale_down        = systematics.getCrossSectionUncertainty("DYJetsToLL_scale").getUncertaintyDown()
DY_scale_up          = systematics.getCrossSectionUncertainty("DYJetsToLL_scale").getUncertaintyUp()
DY_pdf_down          = systematics.getCrossSectionUncertainty("DYJetsToLL_pdf").getUncertaintyDown()
DY_pdf_up            = systematics.getCrossSectionUncertainty("DYJetsToLL_pdf").getUncertaintyUp()
diboson_scale_down   = systematics.getCrossSectionUncertainty("Diboson_scale").getUncertaintyDown()
diboson_scale_up     = systematics.getCrossSectionUncertainty("Diboson_scale").getUncertaintyUp()
diboson_pdf_down     = systematics.getCrossSectionUncertainty("Diboson_pdf").getUncertaintyDown()
diboson_pdf_up       = systematics.getCrossSectionUncertainty("Diboson_pdf").getUncertaintyUp()
lumi_2016            = systematics.getLuminosityUncertainty("2016")

# Define all individual nuisances that can be potentially used
tauID_N         = Nuisance(id="CMS_eff_t"       , label="tau-jet ID (no Rtau) uncer, genuine taus" , distr="lnN"   , function="Constant"      , value=0.10)
tauIDQCD_N      = Nuisance(id="CMS_eff_t_forQCD", label="tau-jet ID uncert, genuine taus"          , distr="lnN"   , function="ConstantForQCD", value=0.10)
tauIDPt_N       = Nuisance(id="CMS_eff_t_highpt", label="tau-jet ID uncert, genuine taus (high-pt)", distr="shapeQ", function="ShapeVariation", systVariation="TauIDSyst")
trg_N           = Nuisance(id="CMS_eff_trg_data", label="Trigger data efficiency"                  , distr="shapeQ", function="ShapeVariation", systVariation="TrgEffData")
trgApprox_N     = Nuisance(id="CMS_eff_trg_data", label="Trigger data efficiency (Approximation)"  , distr="lnN"   , function="Constant"      , value=0.03)
trgMC_N         = Nuisance(id="CMS_eff_trg_MC"  , label="Trigger MC efficiency"                    , distr="shapeQ", function="ShapeVariation", systVariation="TrgEffMC")
trgMCApprox_N   = Nuisance(id="CMS_eff_trg_MC"  , label="Trigger MC efficiency (Approximation)"    , distr="lnN"   , function="Constant"      , value=0.04)
bTag_N          = Nuisance(id="CMS_eff_b"       , label="b tagging"                                , distr="shapeQ", function="ShapeVariation", systVariation="BTagSF")
bTagApprox_N    = Nuisance(id="CMS_eff_b"       , label="b tagging (Approximation)"                , distr="lnN"   , function="Constant"      , value=0.05)
bMistag_N       = Nuisance(id="CMS_fake_b"      , label="b mis-tagging"                            , distr="shapeQ", function="ShapeVariation", systVariation="BMistagSF")
bMistagApprox_N = Nuisance(id="CMS_fake_b"      , label="b mis-tagging (Approximation)"            , distr="lnN"   , function="Constant"      , value=0.02)
TES_N           = Nuisance(id="CMS_scale_t"     , label="Tau Energy Scale (TES)"                   , distr="shapeQ", function="ShapeVariation", systVariation="TauES")
TESapprox_N     = Nuisance(id="CMS_scale_t"     , label="Tau Energy Scale (TES) (Approximation)"   , distr="lnN"   , function="Constant"      , value=0.06)
JES_N           = Nuisance(id="CMS_scale_j"     , label="Jet Energy Scale (JES)"                   , distr="shapeQ", function="ShapeVariation", systVariation="JES")
JESapprox_N     = Nuisance(id="CMS_scale_j"     , label="Jet Energy Scale (JES) (Approximation)"   , distr="lnN"   , function="Constant"      , value=0.03)
UES_N           = Nuisance(id="CMS_scale_met"   , label="Unclustered MET Energy Scale (UES)"       , distr="shapeQ", function="ShapeVariation", systVariation="UES")
UESapprox_N     = Nuisance(id="CMS_scale_met"   , label="Unclustered MET Energy Scale (UES) (App.)", distr="lnN"   , function="Constant"      , value=0.03)
JER_N           = Nuisance(id="CMS_res_j"       , label="Jet Energy Resolution (JER)"              , distr="shapeQ", function="ShapeVariation", systVariation="JER")
JERapprox_N     = Nuisance(id="CMS_res_j"       , label="Jet Energy Resolution (JER) (Approx.)"    , distr="lnN"   , function="Constant"      , value=0.04)
PU_N            = Nuisance(id="CMS_pileup"      , label="Pileup"                                   , distr="shapeQ", function="ShapeVariation", systVariation="PUWeight")
PUapprox_N      = Nuisance(id="CMS_pileup"      , label="Pileup (Approximation)"                   , distr="lnN"   , function="Constant"      , value=0.05)
TopPt_N         = Nuisance(id="CMS_Hptntj_topPtReweight", label="Top pT reweighting"               , distr="shapeQ", function="ShapeVariation", systVariation="TopPt")
TopPtApprox_N   = Nuisance(id="CMS_Hptntj_topPtReweight", label="Top pT reweighting (Approx.)"     , distr="lnN"   , function="Constant"      , value=0.25)
ttbar_scale_N   = Nuisance(id="CMS_scale_ttbar", label="ttbar cross-section scale uncertainty"     , distr="lnN", function="Constant", value=tt_xs_down  , upperValue=tt_xs_up)
ttbar_pdf_N     = Nuisance(id="CMS_pdf_ttbar"  , label="ttbar cross-section pdf uncertainty"       , distr="lnN", function="Constant", value=tt_pdf_down , upperValue=tt_pdf_up)
ttbar_mass_N    = Nuisance(id="CMS_mass_ttbar" , label="ttbar cross-section top mass uncertainty"  , distr="lnN", function="Constant", value=tt_mass_down, upperValue=tt_mass_up) 
ttbar_scaleQCD_N= Nuisance(id="CMS_scale_ttbar_forQCD", label="ttbar cross-section scale uncert."  , distr="lnN", function="ConstantForQCD",value=tt_xs_down  ,upperValue=tt_xs_up)
ttbar_pdfQCD_N  = Nuisance(id="CMS_pdf_ttbar_forQCD"  , label="ttbar cross-section pdf uncertainty", distr="lnN", function="ConstantForQCD",value=tt_pdf_down ,upperValue=tt_pdf_up)
ttbar_massQCD_N = Nuisance(id="CMS_mass_ttbar_forQCD" , label="ttbar cross-section top mass uncer.", distr="lnN", function="ConstantForQCD",value=tt_mass_down,upperValue=tt_mass_up)
wjets_scale_N   = Nuisance(id="CMS_scale_Wjets", label="W+jets cross-section scale uncertainty", distr="lnN", function="Constant", value=wjets_scale_down, upperValue=wjets_scale_up)
wjets_pdf_N      = Nuisance(id="CMS_pdf_Wjets"      , label="W+jets cross-section pdf uncertainty"     , distr="lnN", function="Constant", value=wjets_pdf_down)
singleTop_scale_N= Nuisance(id="CMS_scale_singleTop", label="single top cross-section sale uncertainty", distr="lnN", function="Constant", value=singleTop_scale_down)
singleTop_pdf_N  = Nuisance(id="CMS_pdf_singleTop"  , label="single top cross-section pdf ucnertainty" , distr="lnN", function="Constant", value=singleTop_pdf_down)
DY_scale_N       = Nuisance(id="CMS_scale_DY"       , label="Z->ll cross-section scale uncertainty"    , distr="lnN", function="Constant", value=DY_scale_down, upperValue=DY_scale_up)
DY_pdf_N         = Nuisance(id="CMS_pdf_DY"         , label="Z->ll cross-section pdf uncertainty"      , distr="lnN" , function="Constant"     , value=DY_pdf_down)
diboson_scale_N  = Nuisance(id="CMS_scale_VV"       , label="diboson cross-section scale uncertainty"  , distr="lnN", function="Constant"      , value=diboson_scale_down)
diboson_pdf_N    = Nuisance(id="CMS_pdf_VV"         , label="diboson cross-section pdf uncertainty"    , distr="lnN", function="Constant"      , value=diboson_pdf_down)
lumi_13TeV_N     = Nuisance(id="lumi_13TeV"         , label="Luminosity 13 TeV uncertainty"            , distr="lnN", function="Constant"      , value=lumi_2016)
lumi_13TeVQCD_N  = Nuisance(id="lumi_13TeV_forQCD"  , label="Luminosity 13 TeV uncertainty"            , distr="lnN", function="ConstantForQCD", value=lumi_2016)

qcd_templateFit_N= Nuisance(id="CMS_Hptntj_FakeTauBG_templateFit", label="Data-driven QCD fit"  , distr="lnN"   , function="Constant"         , value=0.03)
qcd_metShape_N   = Nuisance(id="CMS_Hptntj_QCDkbg_metshape"      , label="Data-driven QCD shape", distr="shapeQ", function="QCDShapeVariation", systVariation="QCDNormSource")


#================================================================================================ 
# Construct list of nuisance parameters
#================================================================================================ 
Nuisances.append(tauID_N)
Nuisances.append(tauIDQCD_N)
if "CMS_eff_t_highpt" in myShapeSystematics:
    Nuisances.append(tauIDPt_N)

if "CMS_eff_trg_data" in myShapeSystematics:
    Nuisances.append(trg_N)
else:
    Nuisances.append(trgApprox_N)

if "CMS_eff_trg_MC" in myShapeSystematics:
    Nuisances.append(trgMC_N)
else:
    Nuisances.append(trgMCApprox_N)

# Lepton veto
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

if "CMS_eff_b" in myShapeSystematics:
    Nuisances.append(bTag_N)
else:
    Nuisances.append(bTagApprox_N) 

if "CMS_fake_b" in myShapeSystematics:
    Nuisances.append(bMistag_N)
else:
    Nuisances.append(bMistagApprox_N)

if "CMS_scale_t" in myShapeSystematics:
    Nuisances.append(TES_N)
else:
    Nuisances.append(TESapprox_N)

if "CMS_scale_j" in myShapeSystematics:
    Nuisances.append(JES_N)
else:
    Nuisances.append(JESapprox_N)

if "CMS_scale_met" in myShapeSystematics:
    Nuisances.append(UES_N)
else:
    Nuisances.append(UESapprox_N)

if "CMS_res_j" in myShapeSystematics:
    Nuisances.append(JER_N)
else:
    Nuisances.append(JERapprox_N)

if "CMS_Hptntj_topPtReweight" in myShapeSystematics:
    Nuisances.append(TopPt_N)
else:
    Nuisances.append(TopPtApprox_N)

if "CMS_pileup" in myShapeSystematics:
    Nuisances.append(PU_N) 
else:
    Nuisances.append(PUapprox_N)

# Cross section uncertainties
Nuisances.append(ttbar_scale_N) 
Nuisances.append(ttbar_pdf_N)
Nuisances.append(ttbar_mass_N)
Nuisances.append(ttbar_scaleQCD_N)
Nuisances.append(ttbar_pdfQCD_N)
Nuisances.append(ttbar_massQCD_N)
Nuisances.append(wjets_scale_N)
Nuisances.append(wjets_pdf_N)
Nuisances.append(singleTop_scale_N)
Nuisances.append(singleTop_pdf_N)
Nuisances.append(DY_scale_N)
Nuisances.append(DY_pdf_N)
Nuisances.append(diboson_scale_N)
Nuisances.append(diboson_pdf_N)
Nuisances.append(lumi_13TeV_N)
Nuisances.append(lumi_13TeVQCD_N)
if OptionIncludeSystematics:
    Nuisances.append(qcd_templateFit_N)
    Nuisances.append(qcd_metShape_N)


#================================================================================================ 
# Merge nuisances to same row (first item specifies the name for the row)
#================================================================================================ 
MergeNuisances=[]

# Correlate ttbar and single top cross-section uncertainties
MergeNuisances.append(["CMS_scale_ttbar", "CMS_scale_singleTop"])
MergeNuisances.append(["CMS_pdf_ttbar"  , "CMS_pdf_singleTop"])

# Merge QCDandFakeTau nuisances to corresponding t_genuine nuisances
MergeNuisances.append(["CMS_eff_t"      , "CMS_eff_t_forQCD"])
MergeNuisances.append(["CMS_scale_ttbar", "CMS_scale_ttbar_forQCD"])
MergeNuisances.append(["CMS_pdf_ttbar"  , "CMS_pdf_ttbar_forQCD"])
MergeNuisances.append(["CMS_mass_ttbar" , "CMS_mass_ttbar_forQCD"])
MergeNuisances.append(["lumi_13TeV"     , "lumi_13TeV_forQCD"])

# Convert shape systematics to constants if asked
from HiggsAnalysis.LimitCalc.InputClasses import convertFromSystVariationToConstant
nSysTotal     = len(Nuisances)
nSysToConvert = len(OptionConvertFromShapeToConstantList)
if nSysToConvert > 0:
    Print("Converting %s/%s shape systematics to constants if asked." % (nSysToConvert, nSysTotal), True)
convertFromSystVariationToConstant(Nuisances, OptionConvertFromShapeToConstantList)

# Separate the shape nuisances and the shape and normalization components if asked
from HiggsAnalysis.LimitCalc.InputClasses import separateShapeAndNormalizationFromSystVariation
nSysShapeComponents = len(OptionSeparateShapeAndNormalizationFromSystVariationList)
if (nSysShapeComponents>0):
    Print("Separating %s/%s shape and normalization components" % (nSysShapeComponents, nSysTotal), True)
    separateShapeAndNormalizationFromSystVariation(Nuisances, OptionSeparateShapeAndNormalizationFromSystVariationList)

#================================================================================================ 
# Control plots
#================================================================================================ 
from HiggsAnalysis.LimitCalc.InputClasses import ControlPlotInput
ControlPlots= []

hMET = ControlPlotInput(
    title            = "MET_AfterAllSelections",
    histoName        = "MET_AfterAllSelections",
    details          = { "xlabel"             : "E_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 400.0} }
    )

hHT = ControlPlotInput(
    title            = "HT_AfterAllSelections",
    histoName        = "HT_AfterAllSelections",
    details          = { "xlabel"             : "H_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 3000.0} }
    )

hTopPt = ControlPlotInput(
    title            = "LdgTrijetPt_AfterAllSelections",
    histoName        = "LdgTrijetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 900.0} }
    )

hTopMass = ControlPlotInput(
    title            = "LdgTrijetMass_AfterAllSelections",
    histoName        = "LdgTrijetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jjb}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c^{2}",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 350.0} }
    )

hTopBjetPt = ControlPlotInput(
    title            = "LdgTrijetBjetPt_AfterAllSelections",
    histoName        = "LdgTrijetBjetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 700.0} }
    )

hTopDijetPt = ControlPlotInput(
    title            = "LdgTrijetDijetPt_AfterAllSelections",
    histoName        = "LdgTrijetDijetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 700.0} }
    )

hTopDijetMass = ControlPlotInput(
    title            = "LdgTrijetDijetMass_AfterAllSelections",
    histoName        = "LdgTrijetDijetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jj}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c^{2}",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmin": 40.0, "xmax": 160.0} }
    )

hTopR32  = ControlPlotInput(
    title            = "LdgTrijetTopMassWMassRatioAfterAllSelections",
    histoName        = "LdgTrijetTopMassWMassRatioAfterAllSelections",
    details          = { "xlabel"             : "R_{32}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmin": 0.5, "xmax": 4.0} }
    )

hTetrajetBjetPt = ControlPlotInput(
    title            = "TetrajetBjetPt_AfterAllSelections",
    histoName        = "TetrajetBjetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 900.0} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hTetrajetBjetEta = ControlPlotInput(
    title            = "TetrajetBjetEta_AfterAllSelections",
    histoName        = "TetrajetBjetEta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    # flowPlotCaption  = "m_{jjbb}", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hHiggsPt = ControlPlotInput(
    title            = "LdgTetrajetPt_AfterAllSelections",
    histoName        = "LdgTetrajetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 900.0} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hHiggsMass = ControlPlotInput(
    title            = "LdgTetrajetMass_AfterAllSelections",
    histoName        = "LdgTetrajetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jjbb}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "GeV/c^{2}",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 3000.0} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    # flowPlotCaption  = "m_{jjbb}", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hVertices = ControlPlotInput(
    title            = "NVertices_AfterAllSelections",
    histoName        = "NVertices_AfterAllSelections",
    details          = { "xlabel"             : "vertex multiplicity",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-1, "ymaxfactor": 10, "xmax": 80.0} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    )

# Create ControlPlot list (NOTE: Remember to set OptionDoControlPlots to True)
ControlPlots.append(hMET)
ControlPlots.append(hHT)
#ControlPlots.append(hTopPt)
#ControlPlots.append(hTopMass)
#ControlPlots.append(hTopBjetPt)
#ControlPlots.append(hTopDijetPt)
#ControlPlots.append(hTopDijetMass)
#ControlPlots.append(hTopR32)
#ControlPlots.append(hTetrajetBjetPt)
#ControlPlots.append(hTetrajetBjetEta)
#ControlPlots.append(hHiggsPt)
#ControlPlots.append(hHiggsMass)
#ControlPlots.append(hVertices)
