'''
DESCRIPTION:
-This is a datacard template for 2016 results. 
It can be used to generate datacards for H+ -> tb analysis, 
in the fully hadronic final state. 


USAGE:
./dcardGenerator.py -x dcardHplus2tb2017Datacard_v2.py -d [directory-containing-multicrab-named-SignalAnalysis_*]


EXAMPLES:
./dcardGenerator_v2.py -x dcardDefault_h2tb_2016.py -d limits2016/ --h2tb


LAST USED:
./dcardGenerator_v2.py -x dcardDefault_h2tb_2016.py -d limits2016/ --h2tb
OR
./dcardGenerator_v2.py -x dcardDefault_h2tb_2016_new.py -d limits2016/ --h2tb

'''
#================================================================================================  
# Imports
#================================================================================================  
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import sys
import re

#================================================================================================
# Definitions
#================================================================================================
ss = ShellStyles.SuccessStyle()
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
es = ShellStyles.ErrorStyle()

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
    align   = "{:<3} {:<30} {:<10} {:<20} {:<15} {:<10} {:<40} {:<10}"
    hLine   = "="*150
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


def getFakeBSystematics(myTTBarSystematics, OptionShapeSystematics, verbose=False):
    '''
    Return a list of all systematics to be considered for the Fake-b measurement

    Takes as input the TTbar list and ammends/adds to its.

    # Approximation 1: only ttbar xsect uncertainty applied to FakeB, as ttbar dominates the EWK GenuineB (but uncertainty is scaled according to 1-purity)
    # Approximation 2: lepton and tau-veto neglected (negligible contribution)
    '''
    mySystematics = []
    # For-loop: All TT Systematics
    for syst in myTTBarSystematics:
        if "veto" in syst.lower():
            continue 
        # Only append to name if it is NOT a shape uncertainty!
        if syst not in myJetSystematics + myPileupSystematics + myBtagSystematics + ["CMS_topreweight"] + myTopTagSystematics:
            newSyst = syst + "_forFakeB"
        else:
            if OptionShapeSystematics:
                newSyst = syst
            else:
                newSyst = syst + "_forFakeB"
        mySystematics.append(newSyst)

    # Add by hand the systematics related to Transfer Factors
    mySystematics.append("CMS_HPTB_fakeB_transferfactor")

    if verbose:
        for i, s in enumerate(mySystematics, 1):
            Print("Fake-b Systematic %d) %s" % (i, s), i==1)
    return mySystematics


#================================================================================================  
# Options
#================================================================================================  
OptionTest                             = False # [default: False]
OptionPaper                            = True  # [default: True]
OptionMergeRares                       = True  # [default: True]
OptionIncludeSystematics               = True # [default: True]   (Shape systematics; Requires pseudo-multicrab produced with doSystematics=True) 
OptionShapeSystematics                 = True  # [default: True]   (Shape systematics; Requires pseudo-multicrab produced with doSystematics=True) 
OptionDoControlPlots                   = True  # [default: True]   (Produce control plots defined at end of this file)
MassPoints                             = [180, 200, 220, 250, 300, 350, 400, 500, 650, 800, 1000, 1500, 2000, 2500, 3000]#, 5000, 7000, 10000]
DataCardName                           = "Hplus2tb_13TeV"
OptionMassShape                        = "LdgTetrajetMass_AfterAllSelections"
OptionBr                               = 1.0          # [default: 1.0]    (The Br(t->bH+) used in figures and tables)
OptionSqrtS                            = 13           # [default: 13]     (The sqrt(s) used in figures and tables)
BlindAnalysis                          = False        # [default: True]   (Change only if "green light" for unblinding)
OptionBlindThreshold                   = None         # [default: None]   (If signal exceeds this fraction of expected events, data is blinded)
MinimumStatUncertainty                 = 0.5          # [default: 0.5]    (min. stat. uncert. to set to bins with zero events)
UseAutomaticMinimumStatUncertainty     = False        # [default: False]  (Do NOT use the MinimumStatUncertainty; determine value from lowest non-zero rate for each dataset   )
OptionCombineSingleColumnUncertainties = False        # [default: False]  (Approxmation that makes limit running faster)
OptionDisplayEventYieldSummary         = False        # [default: False]  (Print "Event yield summary", using the TableProducer.py)
OptionDoWithoutSignal                  = False        # [default: False]  (Also do control plots without any signal present)
OptionFakeBMeasurementSource           = "DataDriven" # [default: "DataDriven"] (options: "DataDriven", "MC")
OptionLimitOnSigmaBr                   = True         # [default: True]   (Set to true for heavy H+)
OptionNumberOfDecimalsInSummaries      = 1            # [defaul: 1]       (Self explanatory)
ToleranceForLuminosityDifference       = 0.05         # [default: 0.05]   (Tolerance for throwing error on luminosity difference; "0.01" means that a 1% is required) 
ToleranceForMinimumRate                = 0.0          # [default: 0.0]    (Tolerance for almost zero rate columns with smaller rate are suppressed) 
labelPrefix                            = ""           # [default: ""]     (Prefix for the labels of datacard columns; e.g. "CMS_Hptntj_", "CMS_H2tb_")
labelPostfix                           = "_GenuineB"  # [default: "_GenuineB"]
OptionConvertFromShapeToConstantList   = []           # [default: []]     (Convert these nuisances from shape to constant; Makes limits run faster & converge more easily)
OptionSeparateShapeAndNormFromSystList = []           # [default: []]     (Separate in the following shape nuisances the shape and normalization components)

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
myLumiSystematics          = ["lumi_13TeV"]
myPileupSystematics        = ["CMS_pileup"]
myTopTagSystematics        = ["CMS_HPTB_toptagging"]
myTrgEffSystematics        = ["CMS_eff_trg_MC"]
myLeptonVetoSystematics    = ["CMS_eff_e_veto", "CMS_eff_m_veto", "CMS_eff_tau_veto"]
myJetSystematics           = ["CMS_scale_j", "CMS_res_j"]
myBtagSystematics          = ["CMS_eff_b"]

# Define systematics dictionary (easier access)
mySystematics = {}
mySystematics["MC"]          = myLumiSystematics + myPileupSystematics + myTrgEffSystematics + myLeptonVetoSystematics + myJetSystematics + myBtagSystematics + myTopTagSystematics
mySystematics["Signal"]      = mySystematics["MC"] + ["CMS_HPTB_mu_RF_HPTB","CMS_HPTB_pdf_HPTB"]
mySystematics["FakeB"]       = []
mySystematics["QCD"]         = mySystematics["MC"]
mySystematics["TT"]          = mySystematics["MC"] + ["QCDscale_ttbar", "pdf_ttbar", "mass_top", "CMS_topreweight"] + ["CMS_HPTB_mu_RF_top","CMS_HPTB_pdf_top"]
mySystematics["SingleTop"]   = mySystematics["MC"] + ["QCDscale_singleTop", "pdf_singleTop"] + ["CMS_HPTB_mu_RF_top","CMS_HPTB_pdf_top"]
mySystematics["TTZToQQ"]     = mySystematics["MC"] + ["QCDscale_ttZ", "pdf_ttZ"] + ["CMS_HPTB_mu_RF_ewk","CMS_HPTB_pdf_ewk"]
mySystematics["TTTT"]        = mySystematics["MC"] + ["CMS_HPTB_mu_RF_top","CMS_HPTB_pdf_top"]
mySystematics["DYJetsToQQHT"]= mySystematics["MC"] + ["QCDscale_DY", "pdf_DY"] + ["CMS_HPTB_mu_RF_ewk","CMS_HPTB_pdf_ewk"]
mySystematics["TTWJetsToQQ"] = mySystematics["MC"] + ["QCDscale_ttW", "pdf_ttW"] + ["CMS_HPTB_mu_RF_top","CMS_HPTB_pdf_top"]
mySystematics["WJetsToQQ_HT_600ToInf"]  = mySystematics["MC"] + ["QCDscale_Wjets", "pdf_Wjets"] + ["CMS_HPTB_mu_RF_ewk","CMS_HPTB_pdf_ewk"]
mySystematics["Diboson"]     = mySystematics["MC"] + ["QCDscale_VV", "pdf_VV"] + ["CMS_HPTB_mu_RF_ewk","CMS_HPTB_pdf_ewk"]
mySystematics["FakeB"]       = getFakeBSystematics(mySystematics["TT"], OptionShapeSystematics, verbose=False)
mySystematics["Rares"]       = mySystematics["MC"] #+ ["QCDscale_ttW", "pdf_ttW"] + ["CMS_HPTB_mu_RF_top","CMS_HPTB_pdf_top"]

if not OptionIncludeSystematics:
    msg = "Disabled systematics for all datasets (Stat. only datacards)"
    # For-loop: All dataset-systematics pairs
    for i,dset in enumerate(mySystematics, 1):
        mySystematics[dset] = []
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
myFakeB = DataGroup(label             = labelPrefix + "FakeB", #"FakeBmeasurement",
                    landsProcess      = 2, # must be SAME index as myFakeB (only of them is used!)
                    validMassPoints   = MassPoints,
                    datasetType       = "FakeB",
                    datasetDefinition = "FakeBMeasurementTrijetMass",
                    nuisances         = mySystematics["FakeB"],
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

TT = DataGroup(label             = labelPrefix + "TT" + labelPostfix, #
               landsProcess      = 3,
               shapeHistoName    = OptionMassShape, 
               histoPath         = histoPathEWK,
               datasetType       = dsetTypeEWK,                            
               datasetDefinition = "TT", 
               validMassPoints   = MassPoints,
               nuisances         = mySystematics["TT"]
               )

SingleTop = DataGroup(label             = labelPrefix + "SingleTop" + labelPostfix,
                      landsProcess      = 4,
                      shapeHistoName    = OptionMassShape,
                      histoPath         = histoPathEWK,
                      datasetType       = dsetTypeEWK,
                      datasetDefinition = "SingleTop",
                      validMassPoints   = MassPoints,
                      nuisances         = mySystematics["SingleTop"]
                      )

TTZ = DataGroup(label             = labelPrefix + "TTZToQQ" + labelPostfix, 
                landsProcess      = 5,
                shapeHistoName    = OptionMassShape,
                histoPath         = histoPathEWK,
                datasetType       = dsetTypeEWK,
                datasetDefinition = "TTZToQQ",
                validMassPoints   = MassPoints,
                nuisances         = mySystematics["TTZToQQ"]
                )

TTTT = DataGroup(label             = labelPrefix + "TTTT" + labelPostfix,
                 landsProcess      = 6,
                 shapeHistoName    = OptionMassShape,
                 histoPath         = histoPathEWK,
                 datasetType       = dsetTypeEWK,
                 datasetDefinition = "TTTT",
                 validMassPoints   = MassPoints,
                 nuisances         = mySystematics["TTTT"]
                 )

DYJets = DataGroup(label             = labelPrefix + "DYJetsToQQHT" + labelPostfix, 
                   landsProcess      = 7,
                   shapeHistoName    = OptionMassShape,
                   histoPath         = histoPathEWK,
                   datasetType       = dsetTypeEWK,
                   datasetDefinition = "DYJetsToQQHT",
                   validMassPoints   = MassPoints,
                   nuisances         = mySystematics["DYJetsToQQHT"]
                   )

TTWJets = DataGroup(label             = labelPrefix + "TTWJetsToQQ" + labelPostfix, 
                    landsProcess      = 8,
                    shapeHistoName    = OptionMassShape, 
                    histoPath         = histoPathEWK,
                    datasetType       = dsetTypeEWK,
                    datasetDefinition = "TTWJetsToQQ",
                    validMassPoints   = MassPoints,
                    nuisances         = mySystematics["TTWJetsToQQ"]
                    )

WJets = DataGroup(label             = labelPrefix + "WJetsToQQ_HT_600ToInf" + labelPostfix,
                  landsProcess      = 9,
                  shapeHistoName    = OptionMassShape,
                  histoPath         = histoPathEWK, 
                  datasetType       = dsetTypeEWK,
                  datasetDefinition = "WJetsToQQ_HT_600ToInf",
                  validMassPoints   = MassPoints,
                  nuisances         = mySystematics["WJetsToQQ_HT_600ToInf"]
                  )

Diboson = DataGroup(label             = labelPrefix + "Diboson" + labelPostfix,
                    landsProcess      = 10,
                    shapeHistoName    = OptionMassShape,
                    histoPath         = histoPathEWK, 
                    datasetType       = dsetTypeEWK,
                    datasetDefinition = "Diboson",
                    validMassPoints   = MassPoints,
                    nuisances         = mySystematics["Diboson"]
                    )

Rares = DataGroup(label             = labelPrefix + "Rares" + labelPostfix,
                    landsProcess      = 5,
                    shapeHistoName    = OptionMassShape,
                    histoPath         = histoPathEWK, 
                    datasetType       = dsetTypeEWK,
                    datasetDefinition = "Rares",
                    validMassPoints   = MassPoints,
                    nuisances         = mySystematics["Rares"]
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
if OptionMergeRares:
    rares = aux.GetListOfRareDatasets()
    Print("Replacing rare datasets with single new dataset: [%s] -> %s" % ( ts + ", ".join(rares) + ns, ss + "Rares" + ns), True)
    DataGroups.append(Rares)
else:
    DataGroups.append(TTZ)
    DataGroups.append(TTTT)
    DataGroups.append(DYJets)
    DataGroups.append(TTWJets)
    DataGroups.append(WJets)
    DataGroups.append(Diboson)

#================================================================================================  
# Shape Nuisance Parameters (aka Systematics)  (= rows in datacard) 
#================================================================================================ 
from HiggsAnalysis.LimitCalc.InputClasses import Nuisance

# Define all individual nuisances that can be potentially used (ShapeVariations require running with systematics flag! Defined in AnalysisBuilder.py)
JES_Shape      = Nuisance(id="CMS_scale_j"    , label="Jet Energy Scale (JES)", distr="shapeQ", function="ShapeVariation", systVariation="JES")
JER_Shape      = Nuisance(id="CMS_res_j"      , label="Jet Energy Resolution (JER)", distr="shapeQ", function="ShapeVariation", systVariation="JER")
bTagSF_Shape   = Nuisance(id="CMS_eff_b"      , label="b tagging", distr="shapeQ", function="ShapeVariation", systVariation="BTagSF")
topPt_Shape    = Nuisance(id="CMS_topreweight", label="Top pT reweighting", distr="shapeQ", function="ShapeVariation", systVariation="TopPt")
PU_Shape       = Nuisance(id="CMS_pileup"     , label="Pileup", distr="shapeQ", function="ShapeVariation", systVariation="PUWeight")
tf_FakeB_Shape = Nuisance(id="CMS_HPTB_fakeB_transferfactor", label="Transfer Factor uncertainty",  distr="shapeQ", function="QCDShapeVariation", systVariation="TransferFactor")
topTag_Shape   = Nuisance(id="CMS_HPTB_toptagging", label="TopTag", distr="shapeQ", function="ShapeVariation", systVariation="TopTagSF")
# NOTE: systVariation key is first declared in HiggsAnalysis/NtupleAnalysis/python/AnalysisBuilder.py

#================================================================================================  
# Constant Nuisance Parameters (aka Systematics)  (= rows in datacard) 
#================================================================================================ 
tt_scale_down        = systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyDown()
tt_scale_up          = systematics.getCrossSectionUncertainty("TTJets_scale").getUncertaintyUp()
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
ttW_pdf_down         = systematics.getCrossSectionUncertainty("TTW_pdf").getUncertaintyDown()
ttW_pdf_up           = systematics.getCrossSectionUncertainty("TTW_pdf").getUncertaintyUp()
ttW_scale_up         = systematics.getCrossSectionUncertainty("TTW_scale").getUncertaintyUp()
ttW_scale_down       = systematics.getCrossSectionUncertainty("TTW_scale").getUncertaintyDown()
ttZ_pdf_down         = systematics.getCrossSectionUncertainty("TTZ_pdf").getUncertaintyDown()
ttZ_pdf_up           = systematics.getCrossSectionUncertainty("TTZ_pdf").getUncertaintyUp()
ttZ_scale_down       = systematics.getCrossSectionUncertainty("TTZ_scale").getUncertaintyDown()
ttZ_scale_up         = systematics.getCrossSectionUncertainty("TTZ_scale").getUncertaintyUp()
#tttt_pdf_down        = systematics.getCrossSectionUncertainty("TTTT_pdf").getUncertaintyDown()
#tttt_pdf_up          = systematics.getCrossSectionUncertainty("TTTT_pdf").getUncertaintyUp()
#tttt_scale_down      = systematics.getCrossSectionUncertainty("TTTT_scale").getUncertaintyDown()
#tttt_scale_up        = systematics.getCrossSectionUncertainty("TTTT_scale").getUncertaintyUp()
lumi_2016            = systematics.getLuminosityUncertainty("2016")
# Default nuisances
lumi13TeV_Const = Nuisance(id="lumi_13TeV"         , label="Luminosity 13 TeV uncertainty", distr="lnN", function="Constant", value=lumi_2016)
trgMC_Const     = Nuisance(id="CMS_eff_trg_MC"     , label="Trigger MC efficiency (Approx.)", distr="lnN", function="Constant", value=0.05)
PU_Const        = Nuisance(id="CMS_pileup"         , label="Pileup (Approx.)", distr="lnN", function="Constant", value=0.05)
eVeto_Const     = Nuisance(id="CMS_eff_e_veto"     , label="e veto", distr="lnN", function="Ratio", numerator="passed e selection (Veto)", denominator="passed PV", scaling=0.02)
muVeto_Const    = Nuisance(id="CMS_eff_m_veto"     , label="mu veto", distr="lnN", function="Ratio", numerator="passed mu selection (Veto)", denominator="passed e selection (Veto)", scaling=0.01)
tauVeto_Const   = Nuisance(id="CMS_eff_tau_veto"   , label="tau veto", distr="lnN", function="Ratio", numerator="Passed tau selection (Veto)", denominator="passed mu selection (Veto)", scaling=0.03)
bTagSF_Const    = Nuisance(id="CMS_eff_b"          , label="b tagging (Approx.)", distr="lnN", function="Constant", value=0.05)
JES_Const       = Nuisance(id="CMS_scale_j"        , label="Jet Energy Scale (JES) (Approx.)"     , distr="lnN", function="Constant", value=0.03)
JER_Const       = Nuisance(id="CMS_res_j"          , label="Jet Energy Resolution (JER) (Approx.)", distr="lnN", function="Constant", value=0.04)
topPt_Const     = Nuisance(id="CMS_topreweight"    , label="Top pT reweighting (Approx.)", distr="lnN", function="Constant", value=0.25)
topTag_Const    = Nuisance(id="CMS_HPTB_toptagging", label="Top tagging (Approx.)", distr="lnN", function="Constant", value=0.10)

# Cross section uncertainties
ttbar_scale_Const    = Nuisance(id="QCDscale_ttbar"    , label="QCD XSection uncertainties", distr="lnN", function="Constant", value=tt_scale_down, upperValue=tt_scale_up)
ttbar_pdf_Const      = Nuisance(id="pdf_ttbar"         , label="TTbar XSection pdf uncertainty", distr="lnN", function="Constant", value=tt_pdf_down, upperValue=tt_pdf_up)
ttbar_mass_Const     = Nuisance(id="mass_top"          , label="TTbar XSection top mass uncertainty", distr="lnN", function="Constant", value=tt_mass_down, upperValue=tt_mass_up) 
wjets_scale_Const    = Nuisance(id="QCDscale_Wjets"    , label="QCD XSection uncertainties", distr="lnN", function="Constant", value=wjets_scale_down, upperValue=wjets_scale_up)
wjets_pdf_Const      = Nuisance(id="pdf_Wjets"         , label="W+jets XSection pdf uncertainty", distr="lnN", function="Constant", value=wjets_pdf_down)
singleTop_mass_Const = Nuisance(id="mass_singleTop"    , label="Single top XSection top mass uncertainty", distr="lnN", function="Constant", value=tt_mass_down, upperValue=tt_mass_up)  #FIXME: same as ttbar?
singleTop_scale_Const= Nuisance(id="QCDscale_singleTop", label="QCD XSection uncertainties", distr="lnN", function="Constant", value=singleTop_scale_down)
singleTop_pdf_Const  = Nuisance(id="pdf_singleTop"     , label="Single top XSection pdf ucnertainty", distr="lnN", function="Constant", value=singleTop_pdf_down)
DY_scale_Const       = Nuisance(id="QCDscale_DY"       , label="QCD XSection uncertainties", distr="lnN", function="Constant", value=DY_scale_down, upperValue=DY_scale_up)
DY_pdf_Const         = Nuisance(id="pdf_DY"            , label="DYJets XSection pdf uncertainty", distr="lnN", function="Constant", value=DY_pdf_down)
diboson_scale_Const  = Nuisance(id="QCDscale_VV"       , label="QCD XSection uncertainties", distr="lnN", function="Constant", value=diboson_scale_down)
diboson_pdf_Const    = Nuisance(id="pdf_VV"            , label="Diboson XSection pdf uncertainty", distr="lnN", function="Constant", value=diboson_pdf_down)
ttW_pdf_Const        = Nuisance(id="pdf_ttW"           , label="TTW XSection pdf uncertainty", distr="lnN", function="Constant", value=ttW_pdf_down)
ttW_scale_Const      = Nuisance(id="QCDscale_ttW"      , label="QCD XSection uncertainties", distr="lnN", function="Constant", value=ttW_scale_down, upperValue=ttW_scale_up)
ttZ_pdf_Const        = Nuisance(id="pdf_ttZ"           , label="TTZ XSection pdf uncertainty", distr="lnN", function="Constant", value=ttZ_pdf_down)
ttZ_scale_Const      = Nuisance(id="QCDscale_ttZ"      , label="QCD XSection uncertainties", distr="lnN", function="Constant", value=ttZ_scale_down, upperValue=ttZ_scale_up)
#tttt_pdf_Const       = Nuisance(id="pdf_tttt"          , label="TTTT XSection pdf uncertainty", distr="lnN", function="Constant", value=tttt_pdf_down)
#tttt_scale_Const     = Nuisance(id="QCDscale_tttt"     , label="TTTT XSection scale uncertainty", distr="lnN", function="Constant", value=tttt_scale_down)


#==== Acceptance uncertainties (QCDscale) - new fixme
RF_QCDscale_top_const  = Nuisance(id="CMS_HPTB_mu_RF_top" , label="QCDscale acceptance uncertainty for top backgrounds", distr="lnN", function="Constant",value=0.02)
RF_QCDscale_ewk_const  = Nuisance(id="CMS_HPTB_mu_RF_ewk" , label="QCDscale acceptance uncertainty for EWK backgrounds", distr="lnN", function="Constant",value=0.05)
RF_QCDscale_HPTB_const = Nuisance(id="CMS_HPTB_mu_RF_HPTB", label="QCDscale acceptance uncertainty for signal"         , distr="lnN", function="Constant",value=0.048)
#RF_QCDscale_HPTB_const = Nuisance(id="CMS_HPTB_mu_RF_HPTB_heavy", label="QCDscale acceptance uncertainty for signal", distr="lnN", function="Constant",value=0.012)

#==== Acceptance uncertainties  (PDF) -new fixme
RF_pdf_top_const  = Nuisance(id="CMS_HPTB_pdf_top", label="PDF acceptance uncertainty for top backgrounds", distr="lnN", function="Constant",value=0.02,upperValue=0.0027)
RF_pdf_ewk_const  = Nuisance(id="CMS_HPTB_pdf_ewk", label="PDF acceptance uncertainty for EWK backgrounds", distr="lnN", function="Constant",value=0.033,upperValue=0.046)
RF_pdf_HPTB_const = Nuisance(id="CMS_HPTB_pdf_HPTB", label="PDF acceptance uncertainty for signal", distr="lnN", function="Constant",value=0.004,upperValue=0.017)

# Fake-b nuisances
tf_FakeB_Const          = Nuisance(id="CMS_HPTB_fakeB_transferfactor", label="Transfer Factor uncertainty", distr="lnN", function="Constant", value=0.10)
lumi13TeV_FakeB_Const   = Nuisance(id="lumi_13TeV_forFakeB"      , label="Luminosity 13 TeV uncertainty", distr="lnN", function="ConstantForFakeB", value=lumi_2016)
trgMC_FakeB_Const       = Nuisance(id="CMS_eff_trg_MC_forFakeB"  , label="Trigger MC efficiency (Approx.)", distr="lnN", function="ConstantForFakeB", value=0.05)
PU_FakeB_Const          = Nuisance(id="CMS_pileup_forFakeB"      , label="Pileup (Approx.)", distr="lnN", function="ConstantForFakeB", value=0.05)
eVeto_FakeB_Const       = Nuisance(id="CMS_eff_e_veto_forFakeB"  , label="e veto", distr="lnN", function="Ratio", numerator="passed e selection (Veto)", denominator="passed PV", scaling=0.02) 
muVeto_FakeB_Const      = Nuisance(id="CMS_eff_m_veto_forFakeB"  , label="mu veto", distr="lnN", function="Ratio", numerator="passed mu selection (Veto)", denominator="passed e selection (Veto)", scaling=0.01)
tauVeto_FakeB_Const     = Nuisance(id="CMS_eff_tau_veto_forFakeB", label="tau veto", distr="lnN", function="Ratio", numerator="Passed tau selection (Veto)", denominator="passed mu selection (Veto)", scaling=0.01)
JES_FakeB_Const         = Nuisance(id="CMS_scale_j_forFakeB"     , label="Jet Energy Scale (JES) (Approx.)"     , distr="lnN", function="ConstantForFakeB", value=0.03)
JER_FakeB_Const         = Nuisance(id="CMS_res_j_forFakeB"       , label="Jet Energy Resolution (JER) (Approx.)", distr="lnN", function="ConstantForFakeB", value=0.04)
bTagSF_FakeB_Const      = Nuisance(id="CMS_eff_b_forFakeB"       , label="b tagging (Approx.)", distr="lnN", function="ConstantForFakeB", value=0.05)
topPt_FakeB_Const       = Nuisance(id="CMS_topreweight_forFakeB" , label="Top pT reweighting (Approx.)", distr="lnN", function="ConstantForFakeB", value=0.25)
topTag_FakeB_Const      = Nuisance(id="CMS_HPTB_toptagging_forFakeB", label="Top tagging (Approx.)", distr="lnN", function="ConstantForFakeB", value=0.20)
ttbar_scale_FakeB_Const = Nuisance(id="QCDscale_ttbar_forFakeB"  , label="QCD XSection uncertainties", distr="lnN", function="ConstantForFakeB", value=tt_scale_down, upperValue=tt_scale_up)
ttbar_pdf_FakeB_Const   = Nuisance(id="pdf_ttbar_forFakeB"       , label="TTbar XSection pdf uncertainty", distr="lnN", function="ConstantForFakeB", value=tt_pdf_down, upperValue=tt_pdf_up)
ttbar_mass_FakeB_Const  = Nuisance(id="mass_top_forFakeB"        , label="TTbar XSection top mass uncertainty", distr="lnN", function="ConstantForFakeB", value=tt_mass_down, upperValue=tt_mass_up) 
RF_QCDscale_FakeB_const = Nuisance(id="CMS_HPTB_mu_RF_top_forFakeB", label="QCDscale acceptance uncertainty for FakeB" , distr="lnN", function="ConstantForFakeB",value=0.02)
RF_pdf_FakeB_const      = Nuisance(id="CMS_HPTB_pdf_top_forFakeB"  , label="PDF acceptance uncertainty for FakeB"      , distr="lnN", function="ConstantForFakeB",value=0.02, upperValue=0.0027)


#================================================================================================ 
# Nuisance List (If a given nuisance "name" is used in any of the DataGroups it must be appended)
#================================================================================================ 
ReservedNuisances = []
Nuisances = []
Nuisances.append(lumi13TeV_Const)
if OptionShapeSystematics:
    Nuisances.append(PU_Shape)
    Nuisances.append(JES_Shape)
    Nuisances.append(JER_Shape)
    Nuisances.append(topPt_Shape)
    Nuisances.append(bTagSF_Shape) 
    Nuisances.append(topTag_Shape)
    Nuisances.append(tf_FakeB_Shape)
else:
    Nuisances.append(PU_Const)
    Nuisances.append(PU_FakeB_Const)
    Nuisances.append(JES_Const)
    Nuisances.append(JES_FakeB_Const)
    Nuisances.append(JER_FakeB_Const)
    Nuisances.append(JER_Const)
    Nuisances.append(topPt_Const)
    Nuisances.append(topPt_FakeB_Const)
    Nuisances.append(bTagSF_Const) 
    Nuisances.append(bTagSF_FakeB_Const)
    Nuisances.append(tf_FakeB_Const)
    Nuisances.append(topTag_Const)
    Nuisances.append(topTag_FakeB_Const)

# Common in Shapes/Constants
Nuisances.append(lumi13TeV_FakeB_Const)
Nuisances.append(trgMC_Const)
Nuisances.append(trgMC_FakeB_Const)

# Approximation 2: lepton and tau-veto neglected (negligible contribution)
Nuisances.append(eVeto_Const)
Nuisances.append(muVeto_Const)
Nuisances.append(tauVeto_Const)
# Nuisances.append(eVeto_FakeB_Const)
# Nuisances.append(muVeto_FakeB_Const)
# Nuisances.append(tauVeto_FakeB_Const)

# Approximation 1: only ttbar xsect uncertainty applied to FakeB, as ttbar dominates the EWK GenuineB (but uncertainty is scaled according to 1-purity)
Nuisances.append(ttbar_scale_Const) 
Nuisances.append(ttbar_scale_FakeB_Const) 
Nuisances.append(ttbar_pdf_Const)
Nuisances.append(ttbar_pdf_FakeB_Const)
Nuisances.append(ttbar_mass_Const)
Nuisances.append(ttbar_mass_FakeB_Const)
Nuisances.append(wjets_scale_Const)
Nuisances.append(wjets_pdf_Const)
Nuisances.append(singleTop_scale_Const)
Nuisances.append(singleTop_pdf_Const)
Nuisances.append(DY_scale_Const)
Nuisances.append(DY_pdf_Const)
Nuisances.append(diboson_scale_Const)
Nuisances.append(diboson_pdf_Const)
Nuisances.append(ttW_pdf_Const)
Nuisances.append(ttW_scale_Const)
Nuisances.append(ttZ_pdf_Const)
Nuisances.append(ttZ_scale_Const)
# Nuisances.append(tttt_pdf_Const)
# Nuisances.append(tttt_scale_Const)

# RF/QCD Scale
Nuisances.append(RF_QCDscale_top_const)
Nuisances.append(RF_QCDscale_ewk_const)
Nuisances.append(RF_QCDscale_HPTB_const)
#Nuisances.append(RF_QCDscale_HPTB_const)
Nuisances.append(RF_QCDscale_FakeB_const)
Nuisances.append(RF_pdf_top_const)
Nuisances.append(RF_pdf_ewk_const)
Nuisances.append(RF_pdf_HPTB_const)
Nuisances.append(RF_pdf_FakeB_const)

PrintNuisancesTable(Nuisances, DataGroups)

#================================================================================================ 
# Merge nuisances to same row (first item specifies the name for the row)
# This is for correlated uncertainties. It forces 2 nuisances to be on SAME datacard row
# For example, ttbar xs scale and singleTop pdf should be varied togethed (up or down) but always
# in phase.
# WARNING: This mostly (or solely?) applies for constants. not shape systematics!
# NOTE: When merging nuisances the resultant "merged" name will be the first element of the merging list
# MergeNuisances.append(["QCDscale_ttbar", "QCDscale_singleTop"]) #resultant name will be "QCDscale_ttbar"
#================================================================================================ 
MergeNuisances=[]

# Correlate ttbar and single top cross-section uncertainties
if 0:
    MergeNuisances.append(["QCDscale_ttbar", "QCDscale_singleTop"]) #resultant name will be "QCDscale_ttbar"
    MergeNuisances.append(["pdf_ttbar"  , "pdf_singleTop"])
else:
    #MergeNuisances.append(["QCDscale_ttbar", "QCDscale_singleTop", "QCDscale_ttbar_forFakeB", "QCDscale_ttW", "QCDscale_ttZ"])
    #MergeNuisances.append(["pdf_ttbar"  , "pdf_singleTop"  , "pdf_ttbar_forFakeB"  , "pdf_ttW"  , "pdf_ttZ"])    
    MergeNuisances.append(["QCDscale_ttbar", "QCDscale_ttbar_forFakeB"])
    MergeNuisances.append(["pdf_ttbar"  , "pdf_ttbar_forFakeB"])

# Correlate FakeB and GenuineB uncerainties
MergeNuisances.append(["lumi_13TeV"       , "lumi_13TeV_forFakeB"])
MergeNuisances.append(["CMS_eff_trg_MC"   , "CMS_eff_trg_MC_forFakeB"])
#MergeNuisances.append(["CMS_eff_e_veto"   , "CMS_eff_e_veto_forFakeB"])
#MergeNuisances.append(["CMS_eff_m_veto"   , "CMS_eff_m_veto_forFakeB"])
#MergeNuisances.append(["CMS_eff_tau_veto" , "CMS_eff_tau_veto_forFakeB"])
MergeNuisances.append(["mass_top"   , "mass_top_forFakeB"])
MergeNuisances.append(["CMS_HPTB_mu_RF_top", "CMS_HPTB_mu_RF_top_forFakeB"])
MergeNuisances.append(["CMS_HPTB_pdf_top", "CMS_HPTB_pdf_top_forFakeB"])

if not OptionShapeSystematics:
    MergeNuisances.append(["CMS_pileup"   , "CMS_pileup_forFakeB"])
    MergeNuisances.append(["CMS_eff_b"    , "CMS_eff_b_forFakeB"])
    MergeNuisances.append(["CMS_scale_j"  , "CMS_scale_j_forFakeB"])
    MergeNuisances.append(["CMS_res_j"    , "CMS_res_j_forFakeB"])
    MergeNuisances.append(["CMS_topreweight", "CMS_topreweight_forFakeB"])
    #MergeNuisances.append(["CMS_HPTB_toptagging", "CMS_HPTB_toptagging_forFakeB"]) #iro
    
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
nSysShapeComponents = len(OptionSeparateShapeAndNormFromSystList)
if (nSysShapeComponents>0):
    Print("Separating %s/%s shape and normalization components" % (nSysShapeComponents, nSysTotal), True)
    separateShapeAndNormalizationFromSystVariation(Nuisances, OptionSeparateShapeAndNormFromSystList)

#================================================================================================ 
# Control plots
#================================================================================================ 
# https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines#Figures_and_tables
uPt   = "GeV/c"
uMass = "GeV/c^{2}"
if OptionPaper:
    uPt   = "GeV"
    uMass = "GeV"

from HiggsAnalysis.LimitCalc.InputClasses import ControlPlotInput
ControlPlots= []

hMET = ControlPlotInput(
    title            = "MET_AfterAllSelections",
    histoName        = "MET_AfterAllSelections",
    details          = { "xlabel"             : "E_{T}^{miss}",
                         #"ylabel"             : "Events / #DeltaE_{T}^{miss}",
                         "ylabel"             : "< Events / GeV >",
                         "divideByBinWidth"   : True,
                         "unit"               : "GeV",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmax": 300.0}
                         },
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot      
    )

hHT = ControlPlotInput(
    title            = "HT_AfterAllSelections",
    histoName        = "HT_AfterAllSelections",
    details          = { "xlabel"             : "H_{T}",
                         #"ylabel"             : "Events / #DeltaH_{T}",
                         "ylabel"             : "< Events / GeV >",
                         "divideByBinWidth"   : True,
                         "unit"               : "GeV",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 3000.0} },
                         },
    blindedRange=[800.0, 3000.0], # specify range min,max if blinding applies to this control plot      
    )

hMHT = ControlPlotInput(
    title            = "MHT_AfterAllSelections",
    histoName        = "MHT_AfterAllSelections",
    details          = { "xlabel"             : "MHT",
                         #"ylabel"             : "Events / #DeltaMHT",
                         "ylabel"             : "< Events / GeV >",
                          "divideByBinWidth"   : True,
                         "unit"               : "GeV",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 400.0} }
                         },
    )

hLdgTopPt = ControlPlotInput(
    title            = "LdgTrijetPt_AfterAllSelections",
    histoName        = "LdgTrijetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 900.0} }
                         },
    )

hLdgTopMass = ControlPlotInput(
    title            = "LdgTrijetMass_AfterAllSelections",
    histoName        = "LdgTrijetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jjb}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "%s" % (uMass),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 350.0} 
                         },
    )

hLdgTopBjetPt = ControlPlotInput(
    title            = "LdgTrijetBjetPt_AfterAllSelections",
    histoName        = "LdgTrijetBjetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 700.0} }
                         },
    )

hLdgTopBjetEta = ControlPlotInput(
    title            = "LdgTrijetBjetEta_AfterAllSelections",
    histoName        = "LdgTrijetBjetEta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} 
                         },
    )

hLdgTopBjetBdisc = ControlPlotInput(
    title            = "LdgTrijetBjetBdisc_AfterAllSelections",
    histoName        = "LdgTrijetBjetBdisc_AfterAllSelections",
    details          = { "xlabel"             : "CSVv2 discriminator",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NW",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 0.78, "xmax": 1.0} 
                         },
    )


hLdgTopDijetPt = ControlPlotInput(
    title            = "LdgTrijetDijetPt_AfterAllSelections",
    histoName        = "LdgTrijetDijetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 700.0} 
                         },
    )

hLdgTopDijetMass = ControlPlotInput(
    title            = "LdgTrijetDijetMass_AfterAllSelections",
    histoName        = "LdgTrijetDijetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jj}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "%s" % (uMass),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40.0, "xmax": 200.0} 
                         },
    )

hSubldgTopPt = ControlPlotInput(
    title            = "SubldgTrijetPt_AfterAllSelections",
    histoName        = "SubldgTrijetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 900.0} }
                         },
    )

hSubldgTopMass = ControlPlotInput(
    title            = "SubldgTrijetMass_AfterAllSelections",
    histoName        = "SubldgTrijetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jjb}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "%s" % (uMass),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 360.0} }
                         },
    )

hSubldgTopBjetPt = ControlPlotInput(
    title            = "SubldgTrijetBjetPt_AfterAllSelections",
    histoName        = "SubldgTrijetBjetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 700.0} }
                         },
    )

hSubldgTopBjetEta = ControlPlotInput(
    title            = "SubldgTrijetBjetEta_AfterAllSelections",
    histoName        = "SubldgTrijetBjetEta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} 
                         },
    )

hSubldgTopBjetBdisc = ControlPlotInput(
    title            = "SubldgTrijetBjetBdisc_AfterAllSelections",
    histoName        = "SubldgTrijetBjetBdisc_AfterAllSelections",
    details          = { "xlabel"             : "CSVv2 discriminator",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NW",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 0.78, "xmax": 1.0} 
                         },
    )


hSubldgTopDijetPt = ControlPlotInput(
    title            = "SubldgTrijetDijetPt_AfterAllSelections",
    histoName        = "SubldgTrijetDijetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 700.0} }
                         },
    )

hSubldgTopDijetMass = ControlPlotInput(
    title            = "SubldgTrijetDijetMass_AfterAllSelections",
    histoName        = "SubldgTrijetDijetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jj}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "%s" % (uMass),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40.0, "xmax": 200.0} }
    )

hLdgTopR32  = ControlPlotInput(
    title            = "LdgTrijetTopMassWMassRatioAfterAllSelections",
    histoName        = "LdgTrijetTopMassWMassRatioAfterAllSelections",
    details          = { "xlabel"             : "R_{32}^{ldg}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 0.5, "xmax": 4.0} }
    )

hSubldgTopR32  = ControlPlotInput(
    title            = "SubldgTrijetTopMassWMassRatioAfterAllSelections",
    histoName        = "SubldgTrijetTopMassWMassRatioAfterAllSelections",
    details          = { "xlabel"             : "R_{32}^{sub-ldg}",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 0.5, "xmax": 4.0} }
    )

hTetrajetBjetPt = ControlPlotInput(
    title            = "TetrajetBjetPt_AfterAllSelections",
    histoName        = "TetrajetBjetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 900.0} 
                         },
    # blindedRange=[420.0, 900.0], # specify range min,max if blinding applies to this control plot
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
                         #"legendPosition"     : "NE",
                         "legendPosition"     : "RM", #remove
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    # flowPlotCaption  = "m_{jjbb}", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hTetrajetBjetBdisc = ControlPlotInput(
    title            = "TetrajetBjetBdisc_AfterAllSelections",
    histoName        = "TetrajetBjetBdisc_AfterAllSelections",
    details          = { "xlabel"             : "CSVv2 discriminator",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NW",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 0.78, "xmax": 1.0} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    # flowPlotCaption  = "m_{jjbb}", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hLdgHiggsPt = ControlPlotInput(
    title            = "LdgTetrajetPt_AfterAllSelections",
    histoName        = "LdgTetrajetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 900.0} },
                         },
    blindedRange=[205.0, 900.0], # specify range min,max if blinding applies to this control plot      
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hLdgHiggsMass = ControlPlotInput(
    title            = "LdgTetrajetMass_AfterAllSelections",
    histoName        = "LdgTetrajetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jjbb}",
                         #"ylabel"             : "Events / #Deltam_{jjbb}",
                         "ylabel"             : "< Events / %s >" % (uMass),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uMass),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 3000.0} 
                         },
    blindedRange=[0.0, 2500.0], # specify range min,max if blinding applies to this control plot
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    # flowPlotCaption  = "m_{jjbb}", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hVertices = ControlPlotInput(
    title            = "NVertices_AfterAllSelections",
    histoName        = "NVertices_AfterAllSelections",
    details          = { "xlabel"             : "vertex multiplicity",
                         #"ylabel"             : "Events / #Deltabin",
                         "ylabel"             : "< Events >",
                         "divideByBinWidth"   : True,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmax": 80.0} 
                         },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hQGLR  = ControlPlotInput(
    title            = "QGLR_AfterAllSelections",
    histoName        = "QGLR_AfterAllSelections",
    details          = { "xlabel"             : "QGLR",
                         #"ylabel"             : "Events",
                         "ylabel"             : "< Events >",
                         "divideByBinWidth"   : True,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmax": 1.0} },
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hNjets = ControlPlotInput(
    title            = "Njets_AfterAllSelections",
    histoName        = "Njets_AfterAllSelections",
    details          = { "xlabel"             : "jets multiplicity",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 7.0, "xmax": 20.0} 
                         },
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot      
    )


hNBjets = ControlPlotInput(
    title            = "NBjets_AfterAllSelections",
    histoName        = "NBjets_AfterAllSelections",
    details          = { "xlabel"             : "b-jets multiplicity",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 3.0,"xmax": 10.0} 
                         },
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot      
    )

hJetPt = ControlPlotInput(
    title            = "JetPt_AfterAllSelections",
    histoName        = "JetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"xmin": 40.0, "ymin": 1e-2, "ymaxfactor": 10}
                         },
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot
    )

hJetEta = ControlPlotInput(
    title            = "JetEta_AfterAllSelections",
    histoName        = "JetEta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "SE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}}#,
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot      
    )

hBJetPt = ControlPlotInput(
    title            = "BJetPt_AfterAllSelections",
    histoName        = "BJetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"xmin": 40.0, "ymin": 1e-2, "ymaxfactor": 10}}#,
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot      
    )

hBJetEta = ControlPlotInput(
    title            = "BJetEta_AfterAllSelections",
    histoName        = "BJetEta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}}#,
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot      
    )

hBtagDiscriminator = ControlPlotInput(
    title            = "BtagDiscriminator_AfterAllSelections",
    histoName        = "BtagDiscriminator_AfterAllSelections",
    details          = { "xlabel"             : "CSVv2 discriminator",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}}#,
    #blindedRange=[100.0, 400.0], # specify range min,max if blinding applies to this control plot      
    )

hSubldgHiggsPt = ControlPlotInput(
    title            = "SubldgTetrajetPt_AfterAllSelections",
    histoName        = "SubldgTetrajetPt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmax": 900.0} },
    blindedRange=[0.0, 900.0], # specify range min,max if blinding applies to this control plot      
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hSubldgHiggsMass = ControlPlotInput(
    title            = "SubldgTetrajetMass_AfterAllSelections",
    histoName        = "SubldgTetrajetMass_AfterAllSelections",
    details          = { "xlabel"             : "m_{jjbb}",
                         #"ylabel"             : "Events / #Deltam_{jjbb}",
                         "ylabel"             : "< Events / %s >" % (uMass),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uMass),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10}#, "xmax": 3000.0}
                         },
    blindedRange=[0.0, 3000.0], # specify range min,max if blinding applies to this control plot
    flowPlotCaption  = "", # Leave blank if you don't want to include the item to the selection flow plot    
    # flowPlotCaption  = "m_{jjbb}", # Leave blank if you don't want to include the item to the selection flow plot    
    )

hJet1Pt = ControlPlotInput(
    title            = "Jet1Pt_AfterAllSelections",
    histoName        = "Jet1Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 1000.0} }
                         },
    )

hJet2Pt = ControlPlotInput(
    title            = "Jet2Pt_AfterAllSelections",
    histoName        = "Jet2Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 1000.0} }
                         },
    )

hJet3Pt = ControlPlotInput(
    title            = "Jet3Pt_AfterAllSelections",
    histoName        = "Jet3Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 700.0} }
                         },
    )

hJet4Pt = ControlPlotInput(
    title            = "Jet4Pt_AfterAllSelections",
    histoName        = "Jet4Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 600.0} }
                         },
    )

hJet5Pt = ControlPlotInput(
    title            = "Jet5Pt_AfterAllSelections",
    histoName        = "Jet5Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 500.0}
                         },
    )

hJet6Pt = ControlPlotInput(
    title            = "Jet6Pt_AfterAllSelections",
    histoName        = "Jet6Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 300.0} }
                         },
    )

hJet7Pt = ControlPlotInput(
    title            = "Jet7Pt_AfterAllSelections",
    histoName        = "Jet7Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 30}#, "xmax": 300.0} }
                         },
    )

hJet1Eta = ControlPlotInput(
    title            = "Jet1Eta_AfterAllSelections",
    histoName        = "Jet1Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hJet2Eta = ControlPlotInput(
    title            = "Jet2Eta_AfterAllSelections",
    histoName        = "Jet2Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hJet3Eta = ControlPlotInput(
    title            = "Jet3Eta_AfterAllSelections",
    histoName        = "Jet3Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hJet4Eta = ControlPlotInput(
    title            = "Jet4Eta_AfterAllSelections",
    histoName        = "Jet4Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hJet5Eta = ControlPlotInput(
    title            = "Jet5Eta_AfterAllSelections",
    histoName        = "Jet5Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hJet6Eta = ControlPlotInput(
    title            = "Jet6Eta_AfterAllSelections",
    histoName        = "Jet6Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hJet7Eta = ControlPlotInput(
    title            = "Jet7Eta_AfterAllSelections",
    histoName        = "Jet7Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hBJet1Pt = ControlPlotInput(
    title            = "BJet1Pt_AfterAllSelections",
    histoName        = "BJet1Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 700.0} }
                         },
    )

hBJet2Pt = ControlPlotInput(
    title            = "BJet2Pt_AfterAllSelections",
    histoName        = "BJet2Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T} / #Deltap_{T}",
                         #"ylabel"             : "Events",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40}#, "xmax": 700.0} }
                         },
    )

hBJet3Pt = ControlPlotInput(
    title            = "BJet3Pt_AfterAllSelections",
    histoName        = "BJet3Pt_AfterAllSelections",
    details          = { "xlabel"             : "p_{T}",
                         #"ylabel"             : "Events / #Deltap_{T}",
                         "ylabel"             : "< Events / %s >" % (uPt),
                         "divideByBinWidth"   : True,
                         "unit"               : "%s" % (uPt),
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": 40, "xmax": 700.0} }
    )

hBJet1Eta = ControlPlotInput(
    title            = "BJet1Eta_AfterAllSelections",
    histoName        = "BJet1Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "NE",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hBJet2Eta = ControlPlotInput(
    title            = "BJet2Eta_AfterAllSelections",
    histoName        = "BJet2Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )

hBJet3Eta = ControlPlotInput(
    title            = "BJet3Eta_AfterAllSelections",
    histoName        = "BJet3Eta_AfterAllSelections",
    details          = { "xlabel"             : "#eta",
                         "ylabel"             : "Events",
                         "divideByBinWidth"   : False,
                         "unit"               : "",
                         "log"                : True,
                         "legendPosition"     : "RM",
                         "ratioLegendPosition": "right",
                         "opts"               : {"ymin": 1e-2, "ymaxfactor": 10, "xmin": -2.5, "xmax": 2.5} },
    )


#================================================================================================ 
# Create ControlPlot list (NOTE: Remember to set OptionDoControlPlots to True)
#================================================================================================ 
ControlPlots.append(hMET)
ControlPlots.append(hHT)
ControlPlots.append(hMHT)
### ControlPlots.append(hQGLR) # to speed-up code
ControlPlots.append(hLdgTopPt)
ControlPlots.append(hLdgTopMass)
ControlPlots.append(hLdgTopBjetPt)  # No agreement expected
ControlPlots.append(hLdgTopBjetEta) # No agreement expected
ControlPlots.append(hLdgTopBjetBdisc) # No agreement expected
ControlPlots.append(hLdgTopDijetPt)
ControlPlots.append(hLdgTopDijetMass)
### ControlPlots.append(hLdgTopR32)
ControlPlots.append(hTetrajetBjetPt)
ControlPlots.append(hTetrajetBjetEta)
# ControlPlots.append(hTetrajetBjetBdisc) #no agreement expected
ControlPlots.append(hLdgHiggsPt)
ControlPlots.append(hLdgHiggsMass)
ControlPlots.append(hVertices)
ControlPlots.append(hNjets)
### ControlPlots.append(hNBjets) #No agreement expected
# ControlPlots.append(hJetPt)
# ControlPlots.append(hJetEta)
# ControlPlots.append(hBJetPt)
# ControlPlots.append(hBJetEta)
### ControlPlots.append(hBtagDiscriminator) #No agreement expected
ControlPlots.append(hSubldgTopPt)
ControlPlots.append(hSubldgTopMass)
#ControlPlots.append(hSubldgTopBjetPt)  # No agreement expected
#ControlPlots.append(hSubldgTopBjetEta) # No agreement expected
#ControlPlots.append(hSubldgTopBjetBdisc) # No agreement expected
ControlPlots.append(hSubldgTopDijetPt)
ControlPlots.append(hSubldgTopDijetMass)
### ControlPlots.append(hSubldgTopR32)
ControlPlots.append(hSubldgHiggsPt)
ControlPlots.append(hSubldgHiggsMass)
ControlPlots.append(hJet1Pt)
ControlPlots.append(hJet2Pt)
ControlPlots.append(hJet3Pt)
ControlPlots.append(hJet4Pt)
ControlPlots.append(hJet5Pt)
ControlPlots.append(hJet6Pt)
ControlPlots.append(hJet7Pt)
if 0:
    ControlPlots.append(hJet1Eta)
    ControlPlots.append(hJet2Eta)
    ControlPlots.append(hJet3Eta)
    ControlPlots.append(hJet4Eta)
    ControlPlots.append(hJet5Eta)
    ControlPlots.append(hJet6Eta)
    ControlPlots.append(hJet7Eta)
# No agreement expected
if 0:
    ControlPlots.append(hBJet1Pt)
    ControlPlots.append(hBJet2Pt)
    ControlPlots.append(hBJet3Pt)
    ControlPlots.append(hBJet1Eta)
    ControlPlots.append(hBJet2Eta)
    ControlPlots.append(hBJet3Eta)

if OptionTest:
    ControlPlots = []
    ControlPlots.append(hLdgHiggsMass)
    ControlPlots.append(hTetrajetBjetPt)
    ControlPlots.append(hTetrajetBjetEta)
    ControlPlots.append(hLdgTopPt)
    ControlPlots.append(hLdgTopMass)
    ControlPlots.append(hMET)
    ControlPlots.append(hHT)
    MassPoints = [500]#, 650]
