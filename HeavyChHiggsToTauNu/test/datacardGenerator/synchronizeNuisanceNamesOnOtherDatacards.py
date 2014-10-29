#! /usr/bin/env python

import os
import sys

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as limitTools
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardReader as DatacardReader

if __name__ == "__main__":
    # Read datacards
    myDir = "."
    mySettings = limitTools.GeneralSettings(myDir,[])
    #datacardPattern = mySettings.getDatacardPattern(limitTools.LimitProcessType.TAUJETS)    
    #rootFilePattern = mySettings.getRootfilePattern(limitTools.LimitProcessType.TAUJETS)
    datacardPattern = "datacard_mutau_taunu_m%s_mutau.txt"
    rootFilePattern = "shapes_taunu_m%s_btagmultiplicity_j.root"
    myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern)

    # Replace column names
    myColumnReplaces = {}
    myColumnReplaces["QCDinv"] = "QCDinverted"
    #myMgr.replaceColumnNames(myColumnReplaces)

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
    myNuisanceReplaces["lumi_8TeV"] = "lumi"
    myNuisanceReplaces["pu"] = "pileup"
    #myNuisanceReplaces[""] = ""
    myMgr.replaceNuisanceNames(myNuisanceReplaces)

    myMgr.mergeShapeNuisances(["btag","unbtag"], "b_tag")
    
    myMgr.addNuisance(name="xsect_tt_8TeV", distribution="lnN", columns=["tt_ltau","tt_ll"], value="0.948/1.045")
    myMgr.replaceNuisanceValue("tau_ID_jetToTau_shape", "1.200")

    myMgr.convertShapeToNormalizationNuisance(["ES_jets"])

    # Redo stat. uncert. shape histograms
    myMgr.recreateShapeStatUncert()
    
    myMgr.close()
    
