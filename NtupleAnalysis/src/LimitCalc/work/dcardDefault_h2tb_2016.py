'''
DESCRIPTION:
This is a datacard template for 2016 results. 
It can be used to generate datacards for H+ -> tb analysis, 
in the fully hadronic final state. 


USAGE:
./dcardGenerator.py -x dcardHplus2tb2017Datacard_v2.py -d [directory-containing-multicrab-named-SignalAnalysis_*]


EXAMPLES:
./dcardGenerator_v2.py -x dcardDefault_h2tb_2016.py -d limits2016/ --h2tb


LAST USED:
./dcardGenerator_v2.py -x dcardDefault_h2tb_2016.py -d limits2016/ --h2tb

'''
#================================================================================================  
# Imports
#================================================================================================  
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import sys
import re

#================================================================================================
# Function Definition
#================================================================================================
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def PrintNuisancesTable(Nuisances, DataGroups):
    align   = "{:<3} {:<20} {:<10} {:<20} {:<15} {:<10} {:<40} {:<10}"
    hLine   = "="*140
    header  = align.format("#", "ID", "Distrib.", "Function", "Value (4f)", "Scaling", "Label", "# Datasets")
    table   = []
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # For-loop: All nuisances
    for i, n in enumerate(Nuisances, 1):
        
        datasetList = []
        for j, dg in enumerate(DataGroups, 1):
            if n.getId() in dg.getNuisances():
                datasetList.append(dg.getLabel())
        if isinstance(n.getArg("value"), float):
            value = "%.4f" % n.getArg("value")
        elif n.getId() == "lumi_13TeV":
            value = n.getArg("value").getUncertaintyMax()
        else:
            value = "N/A"

        # Create the row
        #row = align.format(i, n.getId(), n.getDistribution(), n.getFunction(), value, n.getArg("scaling"), n.getLabel(), ", ".join(datasetList) )
        row = align.format(i, n.getId(), n.getDistribution(), n.getFunction(), value, n.getArg("scaling"), n.getLabel(), len(datasetList) )
        table.append(row)
    table.append(hLine)
    table.append("")
    
    # For-loop: All table rows
    for i,row in enumerate(table, 1):
        Print(row, i==1)
    return


#================================================================================================  
# Options
#================================================================================================  
MassPoints                             = [180, 200, 220, 250, 300, 350, 400, 500, 650, 800, 1000, 1500, 2000, 2500, 3000]#, 5000, 7000, 10000]
DataCardName                           = "Hplus2tb_13TeV"
OptionMassShape                        = "LdgTetrajetMass_AfterAllSelections"
OptionBr                               = 1.0   # [default: 1.0]    (The Br(t->bH+) used in figures and tables)
OptionSqrtS                            = 13    # [default: 13]     (The sqrt(s) used in figures and tables)
BlindAnalysis                          = True  # [default: True]   (True, unless you have a green light for unblinding)
OptionBlindThreshold                   = None  # [default: 0.2]    (If signal exceeds this fraction of expected events, data is blinded; set to None to disable)
MinimumStatUncertainty                 = 0.5   # [default: 0.5]    (Minimum stat. uncertainty to set to bins with zero events)
OptionCombineSingleColumnUncertainties = False # [default: False]  (Approxmation that makes limit running faster)
OptionDisplayEventYieldSummary         = False # [default: False]  (Print "Event yield summary", using the TableProducer.py)
OptionDoControlPlots                   = True  # [default: True]   (Produce control plots defined at end of this file)
OptionDoWithoutSignal                  = False # [default: False]  (Also do control plots without any signal present)
OptionFakeBMeasurementSource           = "DataDriven" # [default: "DataDriven"] (options: "DataDriven", "MC")
OptionLimitOnSigmaBr                   = True  # [default: True]   (Set to true for heavy H+)
OptionNumberOfDecimalsInSummaries      = 1     # [defaul: 1]       (Self explanatory)
ToleranceForLuminosityDifference       = 0.05  # [default: 0.05]   (Tolerance for throwing error on luminosity difference; "0.01" means that a 1% is required) 
ToleranceForMinimumRate                = 0.0   # [default: 0.0]    (Tolerance for almost zero rate columns with smaller rate are suppressed) 
labelPrefix                            = ""    # [default: ""]     (Prefix for the labels of datacard columns; e.g. "CMS_Hptntj_", "CMS_H2tb_")

OptionIncludeSystematics               = False # [default: True]   (Shape systematics; Requires pseudo-multicrab produced with doSystematics=True) 
OptionConvertFromShapeToConstantList   = []    # [default: []]     (Convert these nuisances from shape to constant; Makes limits run faster & converge more easily)
OptionSeparateShapeAndNormalizationFromSystVariationList=[] # [default: []]  (Separate in the following shape nuisances the shape and normalization components)

#================================================================================================  
# Counter and histogram path definitions
#================================================================================================  
histoPathInclusive        = "ForDataDrivenCtrlPlots"
histoPathGenuineB         = histoPathInclusive + "EWKGenuineB"
histoPathFakeB            = "ForDataDrivenCtrlPlots"
ShapeHistogramsDimensions = systematics.getBinningForPlot(OptionMassShape) # Get the new binning for the shape histogram

if OptionFakeBMeasurementSource == "DataDriven":
    # EWK Datasets should only be Genuibe-b (FakeB = QCD inclusive + EWK GenuineB)
    histoPathEWK = histoPathGenuineB
    dsetTypeEWK  = "GenuineB"
else:
    # EWK Datasets should be inclusive (Bkg = QCD inclusive + EWK inclusive)
    histoPathEWK = histoPathInclusive
    dsetTypeEWK  = "EWKMC"

#================================================================================================  
# Observation definition (how to retrieve number of observed events)
#================================================================================================  
from HiggsAnalysis.LimitCalc.InputClasses import ObservationInput
Observation = ObservationInput(datasetDefinition="Data", shapeHistoName=OptionMassShape, histoPath=histoPathInclusive)


#================================================================================================  
# Nuisance Lists (Just the strings; The objects are defined later below)
#================================================================================================ 
myLumiSystematics       = ["lumi_13TeV"]
myPileupSystematics     = ["CMS_pileup"]
myTopTagSystematics     = ["CMS_topTagging"]
myTrgEffSystematics     = ["CMS_eff_trg_MC"]
myLeptonVetoSystematics = ["CMS_eff_e_veto", "CMS_eff_m_veto", "CMS_eff_tau_veto"]
myJetSystematics        = ["CMS_scale_j", "CMS_res_j"]
myBtagSystematics       = ["CMS_eff_b"]

# Define systematics dictionary (easy access)
mySystematics = {}
mySystematics["MC"]        = myLumiSystematics + myPileupSystematics + myTrgEffSystematics + myLeptonVetoSystematics + myJetSystematics + myBtagSystematics + myTopTagSystematics
mySystematics["Signal"]    = mySystematics["MC"]
mySystematics["FakeB"]     = []
mySystematics["QCD"]       = mySystematics["MC"]
mySystematics["TT"]        = mySystematics["MC"] + ["CMS_scale_ttbar", "CMS_pdf_ttbar", "CMS_mass_ttbar", "CMS_topPtReweight"]
mySystematics["SingleTop"] = mySystematics["MC"] + ["CMS_scale_singleTop", "CMS_pdf_singleTop"]
mySystematics["TTZ"]       = mySystematics["MC"]
mySystematics["TTTT"]      = mySystematics["MC"]
mySystematics["DYJets"]    = mySystematics["MC"] + ["CMS_scale_DY", "CMS_pdf_DY"]
mySystematics["TTW"]       = mySystematics["MC"]
mySystematics["WJets"]     = mySystematics["MC"] + ["CMS_scale_Wjets", "CMS_pdf_Wjets"]
mySystematics["Diboson"]   = mySystematics["MC"] + ["CMS_scale_VV", "CMS_pdf_VV"]

if not OptionIncludeSystematics:
    for i,dset in enumerate(mySystematics, 1):
        #Print("Dataset %s has following systematics: %s" % (dset, ", ".join(mySystematics[dset])), i==1)
        mySystematics[dset] = []
    msg = "Disabled systematics for all datasets (Stat. only datacards)"
    Print(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle(), True)

#================================================================================================  
# DataGroups (= columns in datacard) 
#================================================================================================ 
from HiggsAnalysis.LimitCalc.InputClasses import DataGroup

# Create a signal tempate
signalTemplate   = DataGroup(datasetType="Signal", histoPath=histoPathInclusive, shapeHistoName=OptionMassShape)
signalDataGroups =  []
# For-loop: All mass points
for mass in MassPoints:
    myMassList=[mass]
    hx=signalTemplate.clone()
    hx.setLabel("Hp" + str(mass) )# + "_a")
    hx.setLandSProcess(1)
    hx.setValidMassPoints(myMassList)
    hx.setNuisances(mySystematics["Signal"])
    hx.setDatasetDefinition("ChargedHiggs_HplusTB_HplusToTB_M_%s" % (mass))
    signalDataGroups.append(hx)

# Define all the background datasets
myFakeB = DataGroup(label             = labelPrefix + "FakeBmeasurement",
                    landsProcess      = 2, # must be SAME index as myFakeB (only of them is used!)
                    validMassPoints   = MassPoints,
                    datasetType       = "FakeB",
                    datasetDefinition = "FakeBMeasurementTrijetMass",
                    nuisances         = [], #["lumi_13TeV_forFakeB"],
                    shapeHistoName    = OptionMassShape,
                    histoPath         = histoPathInclusive
                    )

myQCD = DataGroup(label             = labelPrefix + "QCD",
                  landsProcess      = 2, # must be SAME index as myFakeB (only of them is used!)
                  validMassPoints   = MassPoints,
                  datasetType       = "QCDMC",
                  datasetDefinition = "QCD",
                  nuisances         = mySystematics["QCD"],
                  shapeHistoName    = OptionMassShape,
                  histoPath         = histoPathInclusive
                  )

TT = DataGroup(label             = labelPrefix + "TT",
               landsProcess      = 3,
               shapeHistoName    = OptionMassShape, 
               histoPath         = histoPathEWK,
               datasetType       = dsetTypeEWK,                            
               datasetDefinition = "TT", 
               validMassPoints   = MassPoints,
               nuisances         = mySystematics["TT"]
               )

SingleTop = DataGroup(label             = labelPrefix + "SingleTop", 
                      landsProcess      = 4,
                      shapeHistoName    = OptionMassShape,
                      histoPath         = histoPathEWK,
                      datasetType       = dsetTypeEWK,
                      datasetDefinition = "SingleTop",
                      validMassPoints   = MassPoints,
                      nuisances         = mySystematics["SingleTop"]
                      )

TTZ = DataGroup(label             = labelPrefix + "TTZToQQ", 
                landsProcess      = 5,
                shapeHistoName    = OptionMassShape,
                histoPath         = histoPathEWK,
                datasetType       = dsetTypeEWK,
                datasetDefinition = "TTZToQQ",
                validMassPoints   = MassPoints,
                nuisances         = mySystematics["TTZ"]
                )

TTTT = DataGroup(label             = labelPrefix + "TTTT",
                 landsProcess      = 6,
                 shapeHistoName    = OptionMassShape,
                 histoPath         = histoPathEWK,
                 datasetType       = dsetTypeEWK,
                 datasetDefinition = "TTTT",
                 validMassPoints   = MassPoints,
                 nuisances         = mySystematics["TTTT"]
                 )

DYJets = DataGroup(label             = labelPrefix + "DYJetsToQQ", 
                   landsProcess      = 7,
                   shapeHistoName    = OptionMassShape,
                   histoPath         = histoPathEWK,
                   datasetType       = dsetTypeEWK,
                   datasetDefinition = "DYJetsToQQHT",
                   validMassPoints   = MassPoints,
                   nuisances         = mySystematics["DYJets"]
                   )

TTW = DataGroup(label             = labelPrefix + "TTWJetsToQQ", 
                landsProcess      = 8,
                shapeHistoName    = OptionMassShape, 
                histoPath         = histoPathEWK,
                datasetType       = dsetTypeEWK,
                datasetDefinition = "TTWJetsToQQ",
                validMassPoints   = MassPoints,
                nuisances         = mySystematics["TTW"]
                )

WJets = DataGroup(label             = labelPrefix + "WJetsToQQ_HT_600ToInf",
                  landsProcess      = 9,
                  shapeHistoName    = OptionMassShape,
                  histoPath         = histoPathEWK, 
                  datasetType       = dsetTypeEWK,
                  datasetDefinition = "WJetsToQQ_HT_600ToInf",
                  validMassPoints   = MassPoints,
                  nuisances         = mySystematics["WJets"]
                  )

Diboson = DataGroup(label             = labelPrefix + "Diboson",
                    landsProcess      = 10,
                    shapeHistoName    = OptionMassShape,
                    histoPath         = histoPathEWK, 
                    datasetType       = dsetTypeEWK,
                    datasetDefinition = "Diboson",
                    validMassPoints   = MassPoints,
                    nuisances         = mySystematics["Diboson"]
                    )


# Append datasets in order you want them to appear in the data-driven control plot stack
DataGroups = []
DataGroups.extend(signalDataGroups)
if OptionFakeBMeasurementSource == "DataDriven":
    DataGroups.append(myFakeB)
else:
    DataGroups.append(myQCD)
DataGroups.append(TT)
DataGroups.append(SingleTop)
DataGroups.append(TTZ)
DataGroups.append(TTTT)
DataGroups.append(DYJets)
DataGroups.append(TTW)
DataGroups.append(WJets)
DataGroups.append(Diboson)

#================================================================================================  
# Shape Nuisance Parameters (aka Systematics)  (= rows in datacard) 
#================================================================================================ 
from HiggsAnalysis.LimitCalc.InputClasses import Nuisance

# Define all individual nuisances that can be potentially used (ShapeVariations require running with systematics flag! Defined in AnalysisBuilder.py)
# trgMC_Shape     = Nuisance(id="CMS_eff_trg_MC"   , label="Trigger MC efficiency", distr="shapeQ", function="ShapeVariation", systVariation="TrgEffMC")
# PU_Shape        = Nuisance(id="CMS_pileup"       , label="Pileup", distr="shapeQ", function="ShapeVariation", systVariation="PUWeight")
# bTag_Shape      = Nuisance(id="CMS_eff_b"        , label="b tagging", distr="shapeQ", function="ShapeVariation", systVariation="BTagSF")
# TopPt_Shape     = Nuisance(id="CMS_topPtReweight", label="Top pT reweighting", distr="shapeQ", function="ShapeVariation", systVariation="TopPt")
# JES_Shape       = Nuisance(id="CMS_scale_j"      , label="Jet Energy Scale (JES)"                   , distr="shapeQ", function="ShapeVariation", systVariation="JES")
# JER_Shape       = Nuisance(id="CMS_res_j"        , label="Jet Energy Resolution (JER)"              , distr="shapeQ", function="ShapeVariation", systVariation="JER")

#================================================================================================  
# Constant Nuisance Parameters (aka Systematics)  (= rows in datacard) 
#================================================================================================ 
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

# Default nuisances
lumi13TeV_Const = Nuisance(id="lumi_13TeV"       , label="Luminosity 13 TeV uncertainty", distr="lnN", function="Constant", value=lumi_2016)
trgMC_Const     = Nuisance(id="CMS_eff_trg_MC"   , label="Trigger MC efficiency (Approx.)", distr="lnN", function="Constant", value=0.05)
PU_Const        = Nuisance(id="CMS_pileup"       , label="Pileup (Approx.)", distr="lnN", function="Constant", value=0.05)
eVeto_Const     = Nuisance(id="CMS_eff_e_veto"   , label="e veto", distr="lnN", function="Ratio", numerator="passed e selection (Veto)", denominator="passed PV", scaling=0.02) #sigma-eID= 2%, fixme
muVeto_Const    = Nuisance(id="CMS_eff_m_veto"   , label="mu veto", distr="lnN", function="Ratio", numerator="passed mu selection (Veto)", denominator="passed e selection (Veto)", scaling=0.01) #sigma-muID= 1%, fixme
tauVeto_Const   = Nuisance(id="CMS_eff_tau_veto" , label="tau veto", distr="lnN", function="Ratio", numerator="Passed tau selection (Veto)", denominator="passed mu selection (Veto)", scaling=0.01) #sigma-tauID= 1%, fixme
bTag_Const      = Nuisance(id="CMS_eff_b"        , label="b tagging (Approx.)", distr="lnN", function="Constant", value=0.05)
JES_Const       = Nuisance(id="CMS_scale_j"      , label="Jet Energy Scale (JES) (Approx.)"     , distr="lnN", function="Constant", value=0.03)
JER_Const       = Nuisance(id="CMS_res_j"        , label="Jet Energy Resolution (JER) (Approx.)", distr="lnN", function="Constant", value=0.04)
topPt_Const     = Nuisance(id="CMS_topPtReweight", label="Top pT reweighting (Approx.)", distr="lnN", function="Constant", value=0.25)
topTag_Const    = Nuisance(id="CMS_topTagging"   , label="Top tagging (Approx.)", distr="lnN", function="Constant", value=0.20)

# Fake-b nuisances
lumi13TeV_FakeB_Const = Nuisance(id="lumi_13TeV_forFakeB" , label="Luminosity 13 TeV uncertainty (for QCD)", distr="lnN", function="ConstantForFakeB", value=lumi_2016)

# Cross section uncertainties
ttbar_scale_Const    = Nuisance(id="CMS_scale_ttbar"    , label="TTbar XSection scale uncertainty", distr="lnN", function="Constant", value=tt_xs_down, upperValue=tt_xs_up)
ttbar_pdf_Const      = Nuisance(id="CMS_pdf_ttbar"      , label="TTbar XSection pdf uncertainty", distr="lnN", function="Constant", value=tt_pdf_down, upperValue=tt_pdf_up)
ttbar_mass_Const     = Nuisance(id="CMS_mass_ttbar"     , label="ttbar XSection top mass uncertainty", distr="lnN", function="Constant", value=tt_mass_down, upperValue=tt_mass_up) 
wjets_scale_Const    = Nuisance(id="CMS_scale_Wjets"    , label="W+jets XSection scale uncertainty", distr="lnN", function="Constant", value=wjets_scale_down, upperValue=wjets_scale_up)
wjets_pdf_Const      = Nuisance(id="CMS_pdf_Wjets"      , label="W+jets XSection pdf uncertainty", distr="lnN", function="Constant", value=wjets_pdf_down)
singleTop_scale_Const= Nuisance(id="CMS_scale_singleTop", label="Single top XSection sale uncertainty", distr="lnN", function="Constant", value=singleTop_scale_down)
singleTop_pdf_Const  = Nuisance(id="CMS_pdf_singleTop"  , label="Single top XSection pdf ucnertainty", distr="lnN", function="Constant", value=singleTop_pdf_down)
DY_scale_Const       = Nuisance(id="CMS_scale_DY"       , label="Z->ll XSection scale uncertainty", distr="lnN", function="Constant", value=DY_scale_down, upperValue=DY_scale_up)
DY_pdf_Const         = Nuisance(id="CMS_pdf_DY"         , label="Z->ll XSection pdf uncertainty", distr="lnN" , function="Constant", value=DY_pdf_down)
diboson_scale_Const  = Nuisance(id="CMS_scale_VV"       , label="Diboson XSection scale uncertainty", distr="lnN", function="Constant", value=diboson_scale_down)
diboson_pdf_Const    = Nuisance(id="CMS_pdf_VV"         , label="Diboson XSection pdf uncertainty", distr="lnN", function="Constant", value=diboson_pdf_down)

#================================================================================================ 
# Nuisance List (If a given nuisance "name" is used in any of the DataGroups it must be appended)
#================================================================================================ 
ReservedNuisances = []
Nuisances = []
Nuisances.append(lumi13TeV_FakeB_Const)
Nuisances.append(lumi13TeV_Const)
Nuisances.append(PU_Const)     #fixme: constant -> shape
Nuisances.append(topPt_Const)
Nuisances.append(trgMC_Const)  #fixme: constant -> shape
Nuisances.append(eVeto_Const)
Nuisances.append(muVeto_Const)
Nuisances.append(tauVeto_Const)
Nuisances.append(bTag_Const) 
Nuisances.append(JES_Const)    # fixme: constant -> shape
Nuisances.append(JER_Const)    # fixme: constant -> shape
Nuisances.append(topTag_Const) # fixme: constant -> shape

# Cross section uncertainties
Nuisances.append(ttbar_scale_Const) 
Nuisances.append(ttbar_pdf_Const)
Nuisances.append(ttbar_mass_Const)
Nuisances.append(wjets_scale_Const)
Nuisances.append(wjets_pdf_Const)
Nuisances.append(singleTop_scale_Const)
Nuisances.append(singleTop_pdf_Const)
Nuisances.append(DY_scale_Const)
Nuisances.append(DY_pdf_Const)
Nuisances.append(diboson_scale_Const)
Nuisances.append(diboson_pdf_Const)

# Print summary table of all defined nuisances!
PrintNuisancesTable(Nuisances, DataGroups)

#================================================================================================ 
# Merge nuisances to same row (first item specifies the name for the row)
# This is for correlated uncertainties. It forces 2 nuisances to be on SAME datacard row
# For examle, ttbar xs scale and singleTop pdf should be varied togethed (up or down) but alwasy in phase
#================================================================================================ 
MergeNuisances=[]

# Correlate ttbar and single top cross-section uncertainties
MergeNuisances.append(["CMS_scale_ttbar", "CMS_scale_singleTop"]) #resultant name will be "CMS_scale_ttbar"
MergeNuisances.append(["CMS_pdf_ttbar"  , "CMS_pdf_singleTop"])

# Merge Fake-b nuisances to corresponding Genuine-b nuisances (anti-correlated)
# MergeNuisances.append(["CMS_eff_t"      , "CMS_eff_t_forQCD"])
# MergeNuisances.append(["CMS_scale_ttbar", "CMS_scale_ttbar_forQCD"])
# MergeNuisances.append(["CMS_pdf_ttbar"  , "CMS_pdf_ttbar_forQCD"])
# MergeNuisances.append(["CMS_mass_ttbar" , "CMS_mass_ttbar_forQCD"])
MergeNuisances.append(["lumi_13TeV"     , "lumi_13TeV_forFakeB"])

#================================================================================================ 
# Convert shape systematics to constants if asked
#================================================================================================ 
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
    # blindedRange=[200.0, 3000.0], # specify range min,max if blinding applies to this control plot      
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
ControlPlots.append(hTopMass)
#ControlPlots.append(hTopBjetPt)
#ControlPlots.append(hTopDijetPt)
#ControlPlots.append(hTopDijetMass)
#ControlPlots.append(hTopR32)
ControlPlots.append(hTetrajetBjetPt)
#ControlPlots.append(hTetrajetBjetEta)
#ControlPlots.append(hHiggsPt)
ControlPlots.append(hHiggsMass)
#ControlPlots.append(hVertices)
