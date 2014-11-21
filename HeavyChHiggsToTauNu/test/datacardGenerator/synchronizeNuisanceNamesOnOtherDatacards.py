#! /usr/bin/env python

import os
import sys

#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as limitTools
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardReader as DatacardReader

def hplusTauNuToTauMu(myDir, doCorrelation):
    datacardPattern = "datacard_mutau_taunu_m%s_mutau.txt"
    rootFilePattern = "shapes_taunu_m%s_btagmultiplicity_j.root"
    myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, readOnly=False)

    # Replace column names
    myColumnReplaces = {}
    myColumnReplaces["TBH"] = "HpTauNu_tnmt"
    myColumnReplaces["tau_fake"] = "taufake_tnmt"
    myColumnReplaces["tt_ltau"] = "ttltau_tnmt"
    myColumnReplaces["tt_ll"] = "ttll_tnmt"
    myColumnReplaces["singleTop"] = "singleTop_tnmt"
    myColumnReplaces["di_boson"] = "diboson_tnmt"
    myColumnReplaces["Z_tautau"] = "Ztautau_tnmt"
    myColumnReplaces["Z_eemumu"] = "Zeemumu_tnmt"
    
    myMgr.replaceColumnNames(myColumnReplaces)

    # Replace nuisance names
    myNuisanceReplaces = {}
    myNuisanceReplaces["tauId"] = "tau_ID_shape"
    myNuisanceReplaces["jetTauMisId"] = "tau_ID_jetToTau_shape"
    #myNuisanceReplaces["fakesSyst"] = "???"
    myNuisanceReplaces["tes"] = "ES_taus"
    myNuisanceReplaces["topptunc"] = "top_pt"
    myNuisanceReplaces["jes"] = "ES_jets"
    myNuisanceReplaces["jer"] = "JER"
    myNuisanceReplaces["umet"] = "ES_METunclustered"
    #myNuisanceReplaces["btag"] = "b_tag" 
    #myNuisanceReplaces["btag"] = "btag_CSVM"
    #myNuisanceReplaces["unbtag"] = "unbtag_CSVM"
    myNuisanceReplaces["singletopCrossSection"] = "xsect_singleTop"
    myNuisanceReplaces["zllCrossSection"] = "xsect_DYtoll"
    myNuisanceReplaces["dibosonCrossSection"] = "xsect_VV"
    myNuisanceReplaces["ttbarCrossSection"] = "xsect_tt_8TeV"
    myNuisanceReplaces["lumi_8TeV"] = "lumi"
    myNuisanceReplaces["pu"] = "pileup"
    #myNuisanceReplaces[""] = ""
    
    if doCorrelation:
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
    
        myMgr.replaceNuisanceValue("tau_ID_eToTauBarrel_shape", "1.20")
        #myMgr.addNuisance(name="tau_ID_jetToTau_shape", distribution="lnN", columns=["TBH","tt_ltau","singleTop","di_boson","Z_tautau"], value="1.030")
        #myMgr.addNuisance(name="xsect_tt_8TeV", distribution="lnN", columns=["tt_ltau","tt_ll"], value="0.948/1.060")
        myMgr.replaceNuisanceValue("xsect_tt_8TeV", "0.948/1.060")
        myMgr.replaceNuisanceValue("xsect_singleTop", "1.091")
    
        myMgr.convertShapeToNormalizationNuisance(["ES_jets","JER","ES_METunclustered"])

        #myMgr.subtractPedestalFromShapeNuisances("btag")
        #myMgr.subtractPedestalFromShapeNuisances("unbtag")
        myMgr.mergeShapeNuisances(["btag","unbtag"], "b_tag")

    #myMgr.convertShapeToNormalizationNuisance(["btag","unbtag","ES_jets","JER","ES_taus","ES_METunclustered","top_pt"]) # tmp
    #myMgr.convertShapeToNormalizationNuisance(["b_tag"])
    
    #myMgr.addNuisance("btagshapePDF", distribution="lnN", columns=["ttltau_tnmt","ttll_tnmt"], value="1.050")
    
    # Redo stat. uncert. shape histograms
    myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.4, bkgMinimumAbsStatValue=0.4)
    myMgr.recreateShapeStatUncert()
    
    myMgr.close()

def hplusTauNuToDilepton(myDir, doCorrelation):
    for suffix in ["ee","emu","mumu"]:
        datacardPattern = "DataCard_"+suffix+"_taunu_m%s.txt"
        rootFilePattern = "CrossSectionShapes_taunu_m%s.root"
        rootFileDirectory = suffix
        myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, rootFileDirectory=rootFileDirectory, readOnly=False)

        # Replace nuisance names
        myNuisanceReplaces = {}
        myNuisanceReplaces["tauId"] = "tau_ID_shape"
        myNuisanceReplaces["jetTauMisId"] = "tau_ID_eToTauBarrel_shape"
        #myNuisanceReplaces["fakesSyst"] = "???"
        myNuisanceReplaces["tes"] = "ES_taus"
        myNuisanceReplaces["topptunc"] = "top_pt"
        myNuisanceReplaces["jes"] = "ES_jets"
        myNuisanceReplaces["jer"] = "JER"
        myNuisanceReplaces["umet"] = "ES_METunclustered"
        myNuisanceReplaces["dy_additional_8TeV"] = "dyAdditional_8TeV"
        #myNuisanceReplaces["btag"] = "b_tag" 
        #myNuisanceReplaces["btag"] = "btag_CSVM"
        #myNuisanceReplaces["unbtag"] = "unbtag_CSVM"
        myNuisanceReplaces["singletopCrossSection"] = "xsect_singleTop"
        myNuisanceReplaces["zllCrossSection"] = "xsect_DYtoll"
        myNuisanceReplaces["dibosonCrossSection"] = "xsect_VV"
        myNuisanceReplaces["ttbarCrossSection"] = "xsect_tt_8TeV"
        myNuisanceReplaces["lumi_8TeV"] = "lumi"
        myNuisanceReplaces["pu"] = "pileup"
        #myNuisanceReplaces[""] = ""
        if doCorrelation:
            myMgr.replaceNuisanceNames(myNuisanceReplaces)
        
            myMgr.replaceNuisanceValue("tau_ID_eToTauBarrel_shape", "1.20")
            #myMgr.addNuisance(name="tau_ID_jetToTau_shape", distribution="lnN", columns=["TBH","tt_ltau","singleTop","di_boson","Z_tautau"], value="1.030")
            #myMgr.addNuisance(name="xsect_tt_8TeV", distribution="lnN", columns=["tt_ltau","tt_ll"], value="0.948/1.060")
        
            # Add xsection uncertainty
            myMgr.addNuisance("xsect_tt_8TeV", distribution="lnN", columns=["ttbar","otherttbar"], value="0.948/1.060")
            myMgr.addNuisance("xsect_wjets", distribution="lnN", columns=["wjets"], value="0.963/1.040")
            myMgr.addNuisance("xsect_singletop", distribution="lnN", columns=["st"], value="1.091")
            myMgr.addNuisance("xsect_DYtoll", distribution="lnN", columns=["dy"], value="1.040")
            myMgr.addNuisance("xsect_VV", distribution="lnN", columns=["vv"], value="1.040")
            myMgr.mergeShapeNuisances(["btag","unbtag"], "b_tag")
            #myMgr.removeNuisance("unbtag")

        #myMgr.addNuisance("btagshapePDF", distribution="lnN", columns=["ttbar","otherttbar"], value="1.050")
        
        # Replace column names
        myColumnReplaces = {}
        myColumnReplaces["TBH"] = "HpTauNu%s"%suffix.upper()
        myColumnReplaces["vv"] = "vv%s"%suffix.upper()
        myColumnReplaces["wjets"] = "wjets%s"%suffix.upper()
        myColumnReplaces["otherttbar"] = "otherttbar%s"%suffix.upper()
        myColumnReplaces["st"] = "st%s"%suffix.upper()
        myColumnReplaces["dy"] = "dy%s"%suffix.upper()
        myColumnReplaces["ttbar"] = "ttbar%s"%suffix.upper()
        myMgr.replaceColumnNames(myColumnReplaces)
        
        myNuisanceReplaces = {}
        myNuisanceReplaces["st%s_%s_st%sat"%(suffix.upper(),suffix,suffix.upper())] = "st_%s_stat"%suffix
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
        
        myMgr.convertShapeToNormalizationNuisance(["JER","ES_jets","leff","pileup","ES_METunclustered"])
        #myMgr.convertShapeToNormalizationNuisance(["btag","unbtag","top_pt","b_tag"]) # TMP
        
        myMgr.removeNuisance("fakes")
        myMgr.removeNuisance("br")
        myMgr.removeNuisance("theoryUncXS_vv")
        myMgr.removeNuisance("theoryUncXS_wjets")
        myMgr.removeNuisance("theoryUncXS_otherttbar")
        myMgr.removeNuisance("theoryUncXS_st")
        myMgr.removeNuisance("theoryUncXS_dy")
        myMgr.removeNuisance("theoryUncXS_ttbar")
        
        # Redo stat. uncert. shape histograms
        myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.4, bkgMinimumAbsStatValue=0.4)
        myMgr.recreateShapeStatUncert()
        
        myMgr.close()

def hplusTbToTauMu(myDir, doCorrelation):
    datacardPattern = "datacard_mutau_tb_m%s_mutau.txt"
    rootFilePattern = "shapes_tb_m%s_btagmultiplicity_j.root"
    myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, readOnly=False)

    # Replace column names
    myColumnReplaces = {}
    myColumnReplaces["HTB"] = "HpTB_tbmt"
    myColumnReplaces["tau_fake"] = "taufake_tbmt"
    myColumnReplaces["tt_ltau"] = "ttltau_tbmt"
    myColumnReplaces["tt_ll"] = "ttll_tbmt"
    myColumnReplaces["singleTop"] = "singleTop_tbmt"
    myColumnReplaces["di_boson"] = "diboson_tbmt"
    myColumnReplaces["Z_tautau"] = "Ztautau_tbmt"
    myColumnReplaces["Z_eemumu"] = "Zeemumu_tbmt"
    
    myMgr.replaceColumnNames(myColumnReplaces)

    # Replace nuisance names
    myNuisanceReplaces = {}
    myNuisanceReplaces["tauId"] = "tau_ID_shape"
    #myNuisanceReplaces["fakesSyst"] = "???"
    myNuisanceReplaces["tes"] = "ES_taus"
    myNuisanceReplaces["topptunc"] = "top_pt"
    myNuisanceReplaces["jes"] = "ES_jets"
    myNuisanceReplaces["jer"] = "JER"
    myNuisanceReplaces["umet"] = "ES_METunclustered"
    #myNuisanceReplaces["btag"] = "b_tag" 
    #myNuisanceReplaces["btag"] = "btag_CSVM"
    #myNuisanceReplaces["unbtag"] = "unbtag_CSVM"
    myNuisanceReplaces["singletopCrossSection"] = "xsect_singleTop"
    myNuisanceReplaces["zllCrossSection"] = "xsect_DYtoll"
    myNuisanceReplaces["dibosonCrossSection"] = "xsect_VV"
    myNuisanceReplaces["ttbarCrossSection"] = "xsect_tt_8TeV"
    myNuisanceReplaces["lumi_8TeV"] = "lumi"
    myNuisanceReplaces["pu"] = "pileup"
    #myNuisanceReplaces[""] = ""
    
    if doCorrelation:
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
    
        myMgr.replaceNuisanceValue("tau_ID_eToTauBarrel_shape", "1.20")
        #myMgr.addNuisance(name="tau_ID_jetToTau_shape", distribution="lnN", columns=["TBH","tt_ltau","singleTop","di_boson","Z_tautau"], value="1.030")
        #myMgr.addNuisance(name="xsect_tt_8TeV", distribution="lnN", columns=["tt_ltau","tt_ll"], value="0.948/1.060")
        myMgr.replaceNuisanceValue("xsect_tt_8TeV", "0.948/1.060")
        myMgr.replaceNuisanceValue("xsect_singleTop", "1.091")
    
        #myMgr.subtractPedestalFromShapeNuisances("btag")
        #myMgr.subtractPedestalFromShapeNuisances("unbtag")
        myMgr.mergeShapeNuisances(["btag","unbtag"], "b_tag")


    #myMgr.addNuisance("btagshapePDF", distribution="lnN", columns=["tt_ltau_tbmt","tt_ll_tbmt"], value="1.050")

    myMgr.convertShapeToNormalizationNuisance(["JER","ES_METunclustered","ES_jets"])
    
    #myMgr.convertShapeToNormalizationNuisance(["btag","unbtag"])
    #myMgr.convertShapeToNormalizationNuisance(["b_tag"])
    
    # Redo stat. uncert. shape histograms
    myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.4, bkgMinimumAbsStatValue=0.4)
    myMgr.recreateShapeStatUncert()
    
    myMgr.close()

def hplusTbToDilepton(myDir, doCorrelation):
    for suffix in ["ee","emu","mumu"]:
        datacardPattern = "DataCard_"+suffix+"_tb_m%s.txt"
        rootFilePattern = "CrossSectionShapes_tb_m%s.root"
        rootFileDirectory = suffix
        myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, rootFileDirectory=rootFileDirectory, readOnly=False)

        # Replace nuisance names
        myNuisanceReplaces = {}
        myNuisanceReplaces["tauId"] = "tau_ID_shape"
        myNuisanceReplaces["jetTauMisId"] = "tau_ID_eToTauBarrel_shape"
        #myNuisanceReplaces["fakesSyst"] = "???"
        myNuisanceReplaces["tes"] = "ES_taus"
        myNuisanceReplaces["topptunc"] = "top_pt"
        myNuisanceReplaces["jes"] = "ES_jets"
        myNuisanceReplaces["jer"] = "JER"
        myNuisanceReplaces["umet"] = "ES_METunclustered"
        myNuisanceReplaces["dy_additional_8TeV"] = "dyAdditional_8TeV"
        #myNuisanceReplaces["btag"] = "b_tag" 
        #myNuisanceReplaces["btag"] = "btag_CSVM"
        #myNuisanceReplaces["unbtag"] = "unbtag_CSVM"
        myNuisanceReplaces["singletopCrossSection"] = "xsect_singleTop"
        myNuisanceReplaces["zllCrossSection"] = "xsect_DYtoll"
        myNuisanceReplaces["dibosonCrossSection"] = "xsect_VV"
        myNuisanceReplaces["ttbarCrossSection"] = "xsect_tt_8TeV"
        myNuisanceReplaces["lumi_8TeV"] = "lumi"
        myNuisanceReplaces["pu"] = "pileup"
        #myNuisanceReplaces[""] = ""
        if doCorrelation:
            myMgr.replaceNuisanceNames(myNuisanceReplaces)
        
            myMgr.replaceNuisanceValue("tau_ID_eToTauBarrel_shape", "1.20")
            #myMgr.addNuisance(name="tau_ID_jetToTau_shape", distribution="lnN", columns=["TBH","tt_ltau","singleTop","di_boson","Z_tautau"], value="1.030")
            #myMgr.addNuisance(name="xsect_tt_8TeV", distribution="lnN", columns=["tt_ltau","tt_ll"], value="0.948/1.060")
        
            # Add xsection uncertainty
            myMgr.addNuisance("xsect_tt_8TeV", distribution="lnN", columns=["ttbar","otherttbar"], value="0.948/1.060")
            myMgr.addNuisance("xsect_wjets", distribution="lnN", columns=["wjets"], value="0.963/1.040")
            myMgr.addNuisance("xsect_singletop", distribution="lnN", columns=["st"], value="1.091")
            myMgr.addNuisance("xsect_DYtoll", distribution="lnN", columns=["dy"], value="1.040")
            myMgr.addNuisance("xsect_VV", distribution="lnN", columns=["vv"], value="1.040")
            
            myMgr.mergeShapeNuisances(["btag","unbtag"], "b_tag")
        
        #myMgr.addNuisance("btagshapePDF", distribution="lnN", columns=["ttbar","otherttbar"], value="1.050")
        
        # Replace column names
        myColumnReplaces = {}
        myColumnReplaces["HTB"] = "HpTB_tb%s"%suffix.upper()
        myColumnReplaces["vv"] = "vv_tb%s"%suffix.upper()
        myColumnReplaces["wjets"] = "wjets_tb%s"%suffix.upper()
        myColumnReplaces["otherttbar"] = "otherttbar_tb%s"%suffix.upper()
        myColumnReplaces["st"] = "st_tb%s"%suffix.upper()
        myColumnReplaces["dy"] = "dy_tb%s"%suffix.upper()
        myColumnReplaces["ttbar"] = "ttbar_tb%s"%suffix.upper()
        myMgr.replaceColumnNames(myColumnReplaces)
        
        myNuisanceReplaces = {}
        myNuisanceReplaces["st%s_%s_st%sat"%(suffix.upper(),suffix,suffix.upper())] = "st_%s_stat"%suffix
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
        
        myMgr.convertShapeToNormalizationNuisance(["JER","ES_jets","leff","pileup","ES_METunclustered"])
        
        myMgr.removeNuisance("fakes")
        #myMgr.removeNuisance("unbtag")
        myMgr.removeNuisance("br")
        myMgr.removeNuisance("theoryUncXS_vv")
        myMgr.removeNuisance("theoryUncXS_wjets")
        myMgr.removeNuisance("theoryUncXS_otherttbar")
        myMgr.removeNuisance("theoryUncXS_st")
        myMgr.removeNuisance("theoryUncXS_dy")
        myMgr.removeNuisance("theoryUncXS_ttbar")
        
        # Redo stat. uncert. shape histograms
        myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.4, bkgMinimumAbsStatValue=0.4)
        myMgr.recreateShapeStatUncert()
        
        myMgr.close()


if __name__ == "__main__":
    # Read datacards
    myDir = "."
    
    doCorrelation = True
    
    
    # tau nu decay mode
    hplusTauNuToTauMu(myDir, doCorrelation=doCorrelation)
    hplusTauNuToDilepton(myDir, doCorrelation=doCorrelation)
    
    # tb decay mode
    hplusTbToTauMu(myDir, doCorrelation=doCorrelation)
    hplusTbToDilepton(myDir, doCorrelation=doCorrelation)

