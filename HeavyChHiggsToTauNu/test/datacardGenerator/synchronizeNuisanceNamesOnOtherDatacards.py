#! /usr/bin/env python

import os
import sys

#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as limitTools
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardReader as DatacardReader

# Common naming, see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsCombinationConventions
_CommonNuisanceReplaces = {}
_CommonNuisanceReplaces["lumi"] = "lumi_8TeV"
_CommonNuisanceReplaces["ES_taus"] = "CMS_scale_t"
_CommonNuisanceReplaces["ES_jets"] = "CMS_scale_j"
_CommonNuisanceReplaces["ES_METunclustered"] = "CMS_scale_met"
_CommonNuisanceReplaces["JER"] = "CMS_res_j"
_CommonNuisanceReplaces["tau_ID_shape"] = "CMS_eff_t"
_CommonNuisanceReplaces["tau_ID_eToTauBarrel_shape"] = "CMS_fake_eToTauBarrel"
_CommonNuisanceReplaces["tau_ID_eToTauEndcap_shape"] = "CMS_fake_eToTauEndcap"
_CommonNuisanceReplaces["tau_ID_muToTau_shape"] = "CMS_fake_muToTau"
_CommonNuisanceReplaces["tau_ID_jetToTau_shape"] = "CMS_fake_jetToTau"
_CommonNuisanceReplaces["trg_tau_dataeff"] = "CMS_trg_taumet_tauDataEff"
_CommonNuisanceReplaces["trg_tau_MCeff"] = "CMS_trg_taumet_tauMCEff"
_CommonNuisanceReplaces["trg_L1ETM_dataeff"] = "CMS_trg_taumet_L1ETMDataEff"
_CommonNuisanceReplaces["trg_L1ETM_MCeff"] = "CMS_trg_taumet_L1ETMMCEff"
_CommonNuisanceReplaces["trg_muon_dataeff"] = "CMS_trg_mu_dataEff"

_MinimumStatUncertByBkg = {}
_MinimumStatUncertByBkg["st"] = 0.45
_MinimumStatUncertByBkg["wjets"] = 10 # 40 would be the proper number
_MinimumStatUncertByBkg["dy"] = 2.3
_MinimumStatUncertByBkg["Ztt"] = 2.3
_MinimumStatUncertByBkg["Zeemm"] = 2.3
_MinimumStatUncertByBkg["ttbar"] = 0.09
_MinimumStatUncertByBkg["vv"] = 0.11

_removeUncertainties = None
_keepUncertainties = ["*"]

#_removeUncertainties = ["xsect*"]
#_removeUncertainties = ["CMS_btag_CSVM","]
#_keepUncertainties = ["xsect*","lumi*"]
#_keepUncertainties = ["lumi*"]

def hplusTauNuToTauJets(myDir, doCorrelation, nobtagcorr):
    print "*** H+ -> taunu, tau+jets final state ***"
    datacardPattern = "combine_datacard_hplushadronic_m%s.txt"
    rootFilePattern = "combine_histograms_hplushadronic_m%s.root"
    myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, readOnly=False)
    myNuisanceReplaces = {}
    myNuisanceReplaces["QCD_metshape"] = "CMS_Hptntj_QCDbkg_metshape"
    myNuisanceReplaces["QCDinvTemplateFit"] = "CMS_Hptntj_QCDbkg_templateFit"
    myNuisanceReplaces["Emb_QCDcontam"] = "CMS_Hptntj_taubkg_QCDcontam"
    myNuisanceReplaces["Emb_hybridCaloMET"] = "CMS_Hptntj_taubkg_HybridCaloMETApprox"
    myNuisanceReplaces["Emb_WtauTomu"] = "CMS_Hptntj_taubkg_WTauToMu"
    myNuisanceReplaces["Emb_reweighting"] = "CMS_Hptntj_taubkg_Reweighting"
    myNuisanceReplaces["probBtag"] = "CMS_Hptntj_fakebkg_probabilisticBTag"
    myNuisanceReplaces["higherOrderCorr"] = "ttbar_higherOrderCorrections"
    myNuisanceReplaces["e_mu_veto"] = "CMS_Hptntj_leptonVeto"
    myNuisanceReplaces["Emb_mu_ID"] = "CMS_id_m"
    myNuisanceReplaces["EWKnontt_faketau_TailFit_par0"] = "CMS_Hptntj_fakebkg_tailFitPar0"
    myNuisanceReplaces["EWKnontt_faketau_TailFit_par1"] = "CMS_Hptntj_fakebkg_tailFitPar1"
    myNuisanceReplaces["QCDinv_TailFit_par0"] = "CMS_Hptntj_QCDbkg_tailFitPar0"
    myNuisanceReplaces["QCDinv_TailFit_par1"] = "CMS_Hptntj_QCDbkg_tailFitPar1"
    myNuisanceReplaces["EWK_Tau_TailFit_par0"] = "CMS_Hptntj_taubkg_tailFitPar0"
    myNuisanceReplaces["EWK_Tau_TailFit_par1"] = "CMS_Hptntj_taubkg_tailFitPar1"
    myNuisanceReplaces["b_tag"] = "CMS_btag_CSVT"
    myNuisanceReplaces["top_pt"] = "CMS_Hptntj_topPtReweighting"
    myMgr.replaceNuisanceNames(myNuisanceReplaces)
    
    # Replace column names
    myColumnReplaces = {}
    myColumnReplaces["EWKnontt_faketau"] = "CMS_Hptntj_fakebkg"
    myColumnReplaces["EWK_Tau"] = "CMS_Hptntj_taubkg"
    myColumnReplaces["QCDinv"] = "CMS_Hptntj_QCDbkg"
    for m in myMgr._massPoints:
        myColumnReplaces["Hp%s_a"%m] = "CMS_Hptntj_Hptn"
        myColumnReplaces["HW%s_a"%m] = "CMS_ttHpW_signal"
        myColumnReplaces["HH%s_a"%m] = "CMS_ttHpHp_signal"
    myMgr.replaceColumnNames(myColumnReplaces)
    myMgr.replaceNuisanceNames(_CommonNuisanceReplaces)
    
    # Convert not affected items to hyphens
    myMgr.replaceNuisanceValue("CMS_trg_taumet_tauMCEff", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("CMS_trg_taumet_L1ETMMCEff", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("CMS_trg_mu_dataEff", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_fakebkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("CMS_fake_eToTauEndcap", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("CMS_scale_j", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("CMS_res_j", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("CMS_scale_met", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("CMS_id_m", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_fakebkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("CMS_Hptntj_leptonVeto", "-", ["CMS_Hptntj_taubkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("CMS_Hptntj_taubkg_QCDcontam", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_fakebkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("CMS_Hptntj_taubkg_HybridCaloMETApprox", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_fakebkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("CMS_Hptntj_taubkg_WTauToMu", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_fakebkg","CMS_Hptntj_QCDbkg"])
    #myMgr.replaceNuisanceValue("CMS_Hptntj_taubkg_Reweighting", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_fakebkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("xsect_tt_8TeV", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg"])
    myMgr.replaceNuisanceValue("xsect_Wjets", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("xsect_singleTop", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("xsect_DYtoll", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("xsect_VV", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("lumi_8TeV", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("pileup", "-", "CMS_Hptntj_taubkg")
    myMgr.replaceNuisanceValue("CMS_Hptntj_fakebkg_probabilisticBTag", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("CMS_Hptntj_QCDbkg_templateFit", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg","CMS_Hptntj_fakebkg"])
    myMgr.addNuisance("ttbar_higherOrderCorrections", distribution="lnN", columns=["CMS_Hptntj_fakebkg"], value="1.026")
    #myMgr.replaceNuisanceValue("ttbar_higherOrderCorrections", "-", ["CMS_Hptntj_Hptn","CMS_Hptntj_taubkg","CMS_Hptntj_QCDbkg"])
    myMgr.replaceNuisanceValue("ttbar_higherOrderCorrections", "0.992", "CMS_Hptntj_QCDbkg")
    myMgr.removeManyNuisances(_removeUncertainties)
    myMgr.keepManyNuisances(_keepUncertainties)
    myMgr.close()

def hplusTauNuToTauMu(myDir, doCorrelation, nobtagcorr):
    print "*** H+ -> taunu, tau+mu final state ***"
    datacardPattern = "datacard_mutau_taunu_m%s_mutau.txt"
    rootFilePattern = "shapes_taunu_m%s_btagmultiplicity_j.root"
    
    myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, readOnly=False)

    myMgr.removeNuisance("theoryUncXS_vv")
    myMgr.removeNuisance("theoryUncXS_diboson")
    myMgr.removeNuisance("theoryUncXS_wjets")
    myMgr.removeNuisance("theoryUncXS_zll")
    myMgr.removeNuisance("theoryUncXS_ztautau")
    myMgr.removeNuisance("theoryUncXS_otherttbar")
    myMgr.removeNuisance("theoryUncXS_st")
    myMgr.removeNuisance("theoryUncXS_singletop")
    myMgr.removeNuisance("theoryUncXS_dy")
    myMgr.removeNuisance("theoryUncXS_ttbar")

    # Replace nuisance names
    myNuisanceReplaces = {}
    myNuisanceReplaces["tauId"] = "tau_ID_shape"
    myNuisanceReplaces["jetTauMisId"] = "tau_ID_jetToTau_shape"
    #myNuisanceReplaces["fakesSyst"] = "???"
    myNuisanceReplaces["tes"] = "ES_taus"
    myNuisanceReplaces["topptunc"] = "CMS_Hptnmt_topPtReweighting"
    #myNuisanceReplaces["topptunc"] = "top_pt_mutau"
    myNuisanceReplaces["jes"] = "ES_jets"
    myNuisanceReplaces["jer"] = "JER"
    myNuisanceReplaces["umet"] = "ES_METunclustered"
    if nobtagcorr:
        myNuisanceReplaces["btagMed"] = "CMS_btag_CSVM"
        myNuisanceReplaces["unbtagMed"] = "CMS_unbtag_CSVM"
    myNuisanceReplaces["Z_tautau_embedded"] = "CMS_Hptnmt_DYtautau_embedding"
    myNuisanceReplaces["lumi_8TeV"] = "lumi"
    myNuisanceReplaces["pu"] = "pileup"
    myNuisanceReplaces["pdf"] = "ttbarPDFVariation"
    myNuisanceReplaces["matching"] = "ttbarMatchingVariation"
    myNuisanceReplaces["fakesSyst"] = "CMS_Hptnmt_fakebkg_syst"
    myNuisanceReplaces["q2scale"] = "ttbarQ2Scale"
    myNuisanceReplaces["leptEff"] = "CMS_eff_m"
    myMgr.replaceNuisanceNames(myNuisanceReplaces)
    myMgr.replaceNuisanceNames(_CommonNuisanceReplaces)
    # Replace column names
    myColumnReplaces = {}
    myColumnReplaces["TBH"] = "CMS_Hptnmt_Hptn"
    myColumnReplaces["tau_fake"] = "CMS_Hptnmt_taufake"
    myColumnReplaces["tt_ltau"] = "CMS_Hptnmt_ttltau"
    myColumnReplaces["tt_ll"] = "CMS_Hptnmt_ttll"
    myColumnReplaces["singleTop"] = "CMS_Hptnmt_singleTop"
    myColumnReplaces["di_boson"] = "CMS_Hptnmt_vv"
    myColumnReplaces["Z_tautau"] = "CMS_Hptnmt_Ztt"
    myColumnReplaces["Z_eemumu"] = "CMS_Hptnmt_Zeemm"
    myMgr.replaceColumnNames(myColumnReplaces)
    
    myMgr.addNuisance("xsect_tt_8TeV", distribution="lnN", columns=["CMS_Hptnmt_ttltau","CMS_Hptnmt_ttll"], value="0.940/1.052")
    myMgr.addNuisance("xsect_singleTop", distribution="lnN", columns=["CMS_Hptnmt_singleTop"], value="1.091")
    myMgr.addNuisance("xsect_DYtoll", distribution="lnN", columns=["CMS_Hptnmt_Ztt","CMS_Hptnmt_Zeemm"], value="1.040")
    myMgr.addNuisance("xsect_VV", distribution="lnN", columns=["CMS_Hptnmt_vv"], value="1.040")
    
    if doCorrelation:
        #myMgr.replaceNuisanceValue("CMS_eff_t", "1.060", "CMS_Hptnmt_Ztt")
        myMgr.replaceNuisanceValue("CMS_eff_t", "-", ["CMS_Hptnmt_taufake","CMS_Hptnmt_Zeemm","CMS_Hptnmt_ttll"])
        myMgr.replaceNuisanceValue("CMS_fake_jetToTau", "-", ["CMS_Hptnmt_Hptn","CMS_Hptnmt_taufake","CMS_Hptnmt_ttltau","CMS_Hptnmt_singleTop","CMS_Hptnmt_vv","CMS_Hptnmt_Ztt"])
        myMgr.replaceNuisanceValue("CMS_Hptnmt_fakebkg_syst", "-", ["CMS_Hptnmt_Hptn","CMS_Hptnmt_ttltau","CMS_Hptnmt_ttll","CMS_Hptnmt_singleTop","CMS_Hptnmt_vv","CMS_Hptnmt_Ztt","CMS_Hptnmt_Zeemm"])
        myMgr.replaceNuisanceValue("CMS_eff_m", "-", "CMS_Hptnmt_taufake")
        myMgr.replaceNuisanceValue("lumi_8TeV", "-", "CMS_Hptnmt_taufake")
        myMgr.replaceNuisanceValue("pileup", "-", "CMS_Hptnmt_taufake")
    
        myMgr.convertShapeToNormalizationNuisance(["CMS_scale_j","CMS_res_j","CMS_scale_met"]) #,"CMS_Hptnmt_topPtReweighting"])
        #myMgr.replaceNuisanceValue("CMS_scale_j", "1.040", ["CMS_Hptnmt_Ztt","CMS_Hptnmt_Zeemm"])
        #myMgr.replaceNuisanceValue("CMS_res_j", "1.010", ["CMS_Hptnmt_Ztt","CMS_Hptnmt_Zeemm"])
        #myMgr.replaceNuisanceValue("CMS_scale_met", "1.020", ["CMS_Hptnmt_Ztt","CMS_Hptnmt_Zeemm"])
    
    # Redo stat. uncert. shape histograms
    myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.2, bkgMinimumAbsStatValue=_MinimumStatUncertByBkg)
    myMgr.recreateShapeStatUncert()

    #myMgr.removeStatUncert()
    
    myMgr.removeManyNuisances(_removeUncertainties)
    myMgr.keepManyNuisances(_keepUncertainties)
    #myMgr.convertShapeToNormalizationNuisance(["ttbarPDFVariation","CMS_scale_t","CMS_topPtReweighting","CMS_btag_CSVM","CMS_unbtag_CSVM"])
    #myMgr.convertShapeToNormalizationNuisance(["CMS_scale_t"])
    #myMgr.convertShapeToNormalizationNuisance(["CMS_btag_CSVM","CMS_unbtag_CSVM"])
    myMgr.close()

def hplusTauNuToDilepton(myDir, doCorrelation, nobtagcorr):
    for suffix in ["ee","emu","mumu"]:
        print "*** H+ -> taunu, %s final state ***"%suffix
        datacardPattern = "DataCard_"+suffix+"_taunu_m%s.txt"
        rootFilePattern = "CrossSectionShapes_taunu_m%s.root"
        rootFileDirectory = suffix
        myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, rootFileDirectory=rootFileDirectory, readOnly=False)

        myMgr.removeNuisance("theoryUncXS_vv")
        myMgr.removeNuisance("theoryUncXS_wjets")
        myMgr.removeNuisance("theoryUncXS_otherttbar")
        myMgr.removeNuisance("theoryUncXS_st")
        myMgr.removeNuisance("theoryUncXS_dy")
        myMgr.removeNuisance("theoryUncXS_ttbar")

        myMgr.addNuisance("xsect_tt_8TeV", distribution="lnN", columns=["ttbar","otherttbar"], value="0.940/1.052")
        myMgr.addNuisance("xsect_singleTop", distribution="lnN", columns=["st"], value="1.091")
        myMgr.addNuisance("xsect_DYtoll", distribution="lnN", columns=["dy"], value="1.040")
        myMgr.addNuisance("xsect_VV", distribution="lnN", columns=["vv"], value="1.040")
        if suffix in ["ee","emu"]:
            myMgr.addNuisance("xsect_Wjets", distribution="lnN", columns=["wjets"], value="0.963/1.040")
        #myMgr.removeColumn("wjets")
        #myMgr.removeColumn("vv")
        #myMgr.removeColumn("otherttbar")

        # Replace column names
        myColumnReplaces = {}
        myColumnReplaces["TBH"] = "CMS_Hptn%s_Hp%s"%(suffix,suffix)
        myColumnReplaces["vv"] = "CMS_Hptn%s_vv"%suffix
        myColumnReplaces["wjets"] = "CMS_Hptn%s_wjets"%suffix
        myColumnReplaces["otherttbar"] = "CMS_Hptn%s_otherttbar"%suffix
        myColumnReplaces["st"] = "CMS_Hptn%s_st"%suffix
        myColumnReplaces["dy"] = "CMS_Hptn%s_dy"%suffix
        myColumnReplaces["ttbar"] = "CMS_Hptn%s_ttbar"%suffix
        myMgr.replaceColumnNames(myColumnReplaces)
        myNonTTColumns = ["CMS_Hptn%s_Hp%s"%(suffix,suffix), "CMS_Hptn%s_vv"%suffix, "CMS_Hptn%s_wjets"%suffix, "CMS_Hptn%s_otherttbar"%suffix, "CMS_Hptn%s_st"%suffix, "CMS_Hptn%s_dy"%suffix]
        
        # Replace nuisance names
        myNuisanceReplaces = {}
        myNuisanceReplaces["tauId"] = "tau_ID_shape"
        myNuisanceReplaces["jetTauMisId"] = "tau_ID_eToTauBarrel_shape"
        myNuisanceReplaces["tes"] = "ES_taus"
        myNuisanceReplaces["topptunc"] = "CMS_Hptn%s_topPtReweighting"%suffix
        myNuisanceReplaces["jes"] = "ES_jets"
        myNuisanceReplaces["jer"] = "JER"
        myNuisanceReplaces["umet"] = "ES_METunclustered"
        myNuisanceReplaces["dy_additional_8TeV"] = "dyAdditional_8TeV"
        myNuisanceReplaces["btag"] = "CMS_btag_CSVL"
        myNuisanceReplaces["unbtag"] = "CMS_unbtag_CSVL"
        myNuisanceReplaces["lumi_8TeV"] = "lumi"
        myNuisanceReplaces["pu"] = "pileup"
        myNuisanceReplaces["pdf"] = "ttbarPDFVariation"
        myNuisanceReplaces["q2scale"] = "ttbarQ2Scale"
        myNuisanceReplaces["matching"] = "ttbarMatchingVariation"
        myNuisanceReplaces["seleff_8TeV"] = "CMS_eff_dilepton"
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
        myMgr.replaceNuisanceNames(_CommonNuisanceReplaces)
        
        myMgr.replaceNuisanceValue("ttbarQ2Scale","-","CMS_Hptn%s_Hp%s"%(suffix,suffix))
        myMgr.replaceNuisanceValue("ttbarMatchingVariation","-","CMS_Hptn%s_Hp%s"%(suffix,suffix))
        myMgr.replaceNuisanceValue("ttbarQ2Scale","1.030","CMS_Hptn%s_otherttbar"%(suffix))
        myMgr.replaceNuisanceValue("ttbarMatchingVariation","1.010","CMS_Hptn%s_otherttbar"%(suffix))

        #myMgr.addNuisance("btagshapePDF", distribution="lnN", columns=["ttbar","otherttbar"], value="1.050")

        myColumnReplaces = {}
        for c in myMgr.getColumnNames():
            myColumnReplaces["%s_%s"%(c,c)] = c
        myMgr.replaceColumnNames(myColumnReplaces)
        
        myNuisanceReplaces = {}
        myNuisanceReplaces["st%s_%s_st%sat"%(suffix,suffix,suffix)] = "st_%s_stat"%suffix
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
        
        myMgr.convertShapeToNormalizationNuisance(["CMS_scale_j","CMS_res_j","CMS_scale_met","pileup"])
        #myMgr.convertShapeToNormalizationNuisance(["CMS_btag_CSVL","CMS_unbtag_CSVL"])
        #myMgr.convertShapeToNormalizationNuisance(["CMS_btag_CSVL","CMS_unbtag_CSVL"],columnList=myNonTTColumns)
        #myMgr.convertShapeToNormalizationNuisance(["CMS_Hptn%s_topPtReweighting"%suffix],columnList=myNonTTColumns)
        #myMgr.convertShapeToNormalizationNuisance(["btag","unbtag","top_pt","b_tag"]) # TMP
        
        myMgr.replaceNuisanceValue("lumi_8TeV", "1.026")
                
        # Redo stat. uncert. shape histograms
        myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.2, bkgMinimumAbsStatValue=_MinimumStatUncertByBkg)
        myMgr.recreateShapeStatUncert()
        

        myMgr.removeManyNuisances(_removeUncertainties)
        myMgr.keepManyNuisances(_keepUncertainties)
        myMgr.close()

def hplusTbToTauMu(myDir, doCorrelation, nobtagcorr):
    print "*** H+ -> tb, tau+mu final state ***"
    datacardPattern = "datacard_mutau_tb_m%s_mutau.txt"
    rootFilePattern = "shapes_tb_m%s_btagmultiplicity_j.root"
    
    myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, readOnly=False)

    myMgr.removeNuisance("theoryUncXS_vv")
    myMgr.removeNuisance("theoryUncXS_diboson")
    myMgr.removeNuisance("theoryUncXS_wjets")
    myMgr.removeNuisance("theoryUncXS_zll")
    myMgr.removeNuisance("theoryUncXS_ztautau")
    myMgr.removeNuisance("theoryUncXS_otherttbar")
    myMgr.removeNuisance("theoryUncXS_st")
    myMgr.removeNuisance("theoryUncXS_singletop")
    myMgr.removeNuisance("theoryUncXS_dy")
    myMgr.removeNuisance("theoryUncXS_ttbar")

    # Replace nuisance names
    myNuisanceReplaces = {}
    myNuisanceReplaces["tauId"] = "tau_ID_shape"
    myNuisanceReplaces["jetTauMisId"] = "tau_ID_jetToTau_shape"
    #myNuisanceReplaces["fakesSyst"] = "???"
    myNuisanceReplaces["tes"] = "ES_taus"
    myNuisanceReplaces["topptunc"] = "CMS_Hptbmt_topPtReweighting"
    #myNuisanceReplaces["topptunc"] = "top_pt_mutau"
    myNuisanceReplaces["jes"] = "ES_jets"
    myNuisanceReplaces["jer"] = "JER"
    myNuisanceReplaces["umet"] = "ES_METunclustered"
    if nobtagcorr:
        myNuisanceReplaces["btagMed"] = "CMS_btag_CSVM"
        myNuisanceReplaces["unbtagMed"] = "CMS_unbtag_CSVM"
    myNuisanceReplaces["Z_tautau_embedded"] = "CMS_Hptbmt_DYtautau_embedding"
    myNuisanceReplaces["lumi_8TeV"] = "lumi"
    myNuisanceReplaces["pu"] = "pileup"
    myNuisanceReplaces["pdf"] = "ttbarPDFVariation"
    myNuisanceReplaces["matching"] = "ttbarMatchingVariation"
    myNuisanceReplaces["fakesSyst"] = "CMS_Hptbmt_fakebkg_syst"
    myNuisanceReplaces["q2scale"] = "ttbarQ2Scale"
    myNuisanceReplaces["leptEff"] = "CMS_eff_m"
    myMgr.replaceNuisanceNames(myNuisanceReplaces)
    myMgr.replaceNuisanceNames(_CommonNuisanceReplaces)
    # Replace column names
    myColumnReplaces = {}
    myColumnReplaces["HTB"] = "CMS_Hptbmt_Hptb"
    myColumnReplaces["tau_fake"] = "CMS_Hptbmt_taufake"
    myColumnReplaces["tt_ltau"] = "CMS_Hptbmt_ttltau"
    myColumnReplaces["tt_ll"] = "CMS_Hptbmt_ttll"
    myColumnReplaces["singleTop"] = "CMS_Hptbmt_singleTop"
    myColumnReplaces["di_boson"] = "CMS_Hptbmt_vv"
    myColumnReplaces["Z_tautau"] = "CMS_Hptbmt_Ztt"
    myColumnReplaces["Z_eemumu"] = "CMS_Hptbmt_Zeemm"
    myMgr.replaceColumnNames(myColumnReplaces)
    
    myMgr.addNuisance("xsect_tt_8TeV", distribution="lnN", columns=["CMS_Hptbmt_ttltau","CMS_Hptbmt_ttll"], value="0.940/1.052")
    myMgr.addNuisance("xsect_singleTop", distribution="lnN", columns=["CMS_Hptbmt_singleTop"], value="1.091")
    myMgr.addNuisance("xsect_DYtoll", distribution="lnN", columns=["CMS_Hptbmt_Ztt","CMS_Hptbmt_Zeemm"], value="1.040")
    myMgr.addNuisance("xsect_VV", distribution="lnN", columns=["CMS_Hptbmt_vv"], value="1.040")
    
    if doCorrelation:
        #myMgr.replaceNuisanceValue("CMS_eff_t", "1.060", "CMS_Hptbmt_Ztt")
        myMgr.replaceNuisanceValue("CMS_eff_t", "-", ["CMS_Hptbmt_taufake","CMS_Hptbmt_Zeemm","CMS_Hptbmt_ttll"])
        myMgr.replaceNuisanceValue("CMS_fake_jetToTau", "-", ["CMS_Hptbmt_Hptn","CMS_Hptbmt_taufake","CMS_Hptbmt_ttltau","CMS_Hptbmt_singleTop","CMS_Hptbmt_vv","CMS_Hptbmt_Ztt"])
        myMgr.replaceNuisanceValue("CMS_Hptbmt_fakebkg_syst", "-", ["CMS_Hptbmt_Hptn","CMS_Hptbmt_ttltau","CMS_Hptbmt_ttll","CMS_Hptbmt_singleTop","CMS_Hptbmt_vv","CMS_Hptbmt_Ztt","CMS_Hptbmt_Zeemm"])
        myMgr.replaceNuisanceValue("CMS_eff_m", "-", "CMS_Hptbmt_taufake")
        myMgr.replaceNuisanceValue("lumi_8TeV", "-", "CMS_Hptbmt_taufake")
        myMgr.replaceNuisanceValue("pileup", "-", "CMS_Hptbmt_taufake")
    
        myMgr.convertShapeToNormalizationNuisance(["CMS_scale_j","CMS_res_j","CMS_scale_met"]) #,"CMS_Hptbmt_topPtReweighting"])
        #myMgr.replaceNuisanceValue("CMS_scale_j", "1.040", ["CMS_Hptbmt_Ztt","CMS_Hptbmt_Zeemm"])
        #myMgr.replaceNuisanceValue("CMS_res_j", "1.010", ["CMS_Hptbmt_Ztt","CMS_Hptbmt_Zeemm"])
        #myMgr.replaceNuisanceValue("CMS_scale_met", "1.020", ["CMS_Hptbmt_Ztt","CMS_Hptbmt_Zeemm"])
    
    # Redo stat. uncert. shape histograms
    myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.2, bkgMinimumAbsStatValue=_MinimumStatUncertByBkg)
    myMgr.recreateShapeStatUncert()

    #myMgr.removeStatUncert()
    
    myMgr.removeManyNuisances(_removeUncertainties)
    myMgr.keepManyNuisances(_keepUncertainties)
    #myMgr.convertShapeToNormalizationNuisance(["ttbarPDFVariation","CMS_scale_t","CMS_topPtReweighting","CMS_btag_CSVM","CMS_unbtag_CSVM"])
    #myMgr.convertShapeToNormalizationNuisance(["CMS_scale_t"])
    #myMgr.convertShapeToNormalizationNuisance(["CMS_btag_CSVM","CMS_unbtag_CSVM"])
    myMgr.close()

def hplusTbToDilepton(myDir, doCorrelation, nobtagcorr):
    for suffix in ["ee","emu","mumu"]:
        print "*** H+ -> tb, %s final state ***"%suffix
        datacardPattern = "DataCard_"+suffix+"_tb_m%s.txt"
        rootFilePattern = "CrossSectionShapes_tb_m%s.root"
        rootFileDirectory = suffix
        myMgr = DatacardReader.DataCardDirectoryManager(myDir, datacardPattern, rootFilePattern, rootFileDirectory=rootFileDirectory, readOnly=False)

        myMgr.removeNuisance("theoryUncXS_vv")
        myMgr.removeNuisance("theoryUncXS_wjets")
        myMgr.removeNuisance("theoryUncXS_otherttbar")
        myMgr.removeNuisance("theoryUncXS_st")
        myMgr.removeNuisance("theoryUncXS_dy")
        myMgr.removeNuisance("theoryUncXS_ttbar")

        myMgr.addNuisance("xsect_tt_8TeV", distribution="lnN", columns=["ttbar","otherttbar"], value="0.940/1.052")
        myMgr.addNuisance("xsect_singleTop", distribution="lnN", columns=["st"], value="1.091")
        myMgr.addNuisance("xsect_DYtoll", distribution="lnN", columns=["dy"], value="1.040")
        myMgr.addNuisance("xsect_VV", distribution="lnN", columns=["vv"], value="1.040")
        if suffix in ["ee","emu"]:
            myMgr.addNuisance("xsect_Wjets", distribution="lnN", columns=["wjets"], value="0.963/1.040")
        #myMgr.removeColumn("wjets")
        #myMgr.removeColumn("vv")
        #myMgr.removeColumn("otherttbar")

        # Replace column names
        myColumnReplaces = {}
        myColumnReplaces["HTB"] = "CMS_Hptb%s_Hp%s"%(suffix,suffix)
        myColumnReplaces["vv"] = "CMS_Hptb%s_vv"%suffix
        myColumnReplaces["wjets"] = "CMS_Hptb%s_wjets"%suffix
        myColumnReplaces["otherttbar"] = "CMS_Hptb%s_otherttbar"%suffix
        myColumnReplaces["st"] = "CMS_Hptb%s_st"%suffix
        myColumnReplaces["dy"] = "CMS_Hptb%s_dy"%suffix
        myColumnReplaces["ttbar"] = "CMS_Hptb%s_ttbar"%suffix
        myMgr.replaceColumnNames(myColumnReplaces)
        myNonTTColumns = ["CMS_Hptb%s_Hp%s"%(suffix,suffix), "CMS_Hptb%s_vv"%suffix, "CMS_Hptb%s_wjets"%suffix, "CMS_Hptb%s_otherttbar"%suffix, "CMS_Hptb%s_st"%suffix, "CMS_Hptb%s_dy"%suffix]
        
        # Replace nuisance names
        myNuisanceReplaces = {}
        myNuisanceReplaces["tauId"] = "tau_ID_shape"
        myNuisanceReplaces["jetTauMisId"] = "tau_ID_eToTauBarrel_shape"
        myNuisanceReplaces["tes"] = "ES_taus"
        myNuisanceReplaces["topptunc"] = "CMS_Hptb%s_topPtReweighting"%suffix
        myNuisanceReplaces["jes"] = "ES_jets"
        myNuisanceReplaces["jer"] = "JER"
        myNuisanceReplaces["umet"] = "ES_METunclustered"
        myNuisanceReplaces["dy_additional_8TeV"] = "dyAdditional_8TeV"
        myNuisanceReplaces["btag"] = "CMS_btag_CSVL"
        myNuisanceReplaces["unbtag"] = "CMS_unbtag_CSVL"
        myNuisanceReplaces["lumi_8TeV"] = "lumi"
        myNuisanceReplaces["pu"] = "pileup"
        myNuisanceReplaces["pdf"] = "ttbarPDFVariation"
        myNuisanceReplaces["q2scale"] = "ttbarQ2Scale"
        myNuisanceReplaces["matching"] = "ttbarMatchingVariation"
        myNuisanceReplaces["seleff_8TeV"] = "CMS_eff_dilepton"
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
        myMgr.replaceNuisanceNames(_CommonNuisanceReplaces)
        
        myMgr.replaceNuisanceValue("ttbarQ2Scale","-","CMS_Hptb%s_Hp%s"%(suffix,suffix))
        myMgr.replaceNuisanceValue("ttbarMatchingVariation","-","CMS_Hptb%s_Hp%s"%(suffix,suffix))
        myMgr.replaceNuisanceValue("ttbarQ2Scale","1.030","CMS_Hptb%s_otherttbar"%(suffix))
        myMgr.replaceNuisanceValue("ttbarMatchingVariation","1.010","CMS_Hptb%s_otherttbar"%(suffix))

        #myMgr.addNuisance("btagshapePDF", distribution="lnN", columns=["ttbar","otherttbar"], value="1.050")

        myColumnReplaces = {}
        for c in myMgr.getColumnNames():
            myColumnReplaces["%s_%s"%(c,c)] = c
        myMgr.replaceColumnNames(myColumnReplaces)
        
        myNuisanceReplaces = {}
        myNuisanceReplaces["st%s_%s_st%sat"%(suffix,suffix,suffix)] = "st_%s_stat"%suffix
        myMgr.replaceNuisanceNames(myNuisanceReplaces)
        
        myMgr.convertShapeToNormalizationNuisance(["CMS_scale_j","CMS_res_j","CMS_scale_met","pileup"])
        #myMgr.convertShapeToNormalizationNuisance(["CMS_btag_CSVL","CMS_unbtag_CSVL"])
        #myMgr.convertShapeToNormalizationNuisance(["CMS_btag_CSVL","CMS_unbtag_CSVL"],columnList=myNonTTColumns)
        #myMgr.convertShapeToNormalizationNuisance(["CMS_Hptb%s_topPtReweighting"%suffix],columnList=myNonTTColumns)
        #myMgr.convertShapeToNormalizationNuisance(["btag","unbtag","top_pt","b_tag"]) # TMP
        
        myMgr.replaceNuisanceValue("lumi_8TeV", "1.026")
                
        # Redo stat. uncert. shape histograms
        myMgr.fixTooSmalltatUncertProblem(signalMinimumAbsStatValue=0.2, bkgMinimumAbsStatValue=_MinimumStatUncertByBkg)
        myMgr.recreateShapeStatUncert()
        

        myMgr.removeManyNuisances(_removeUncertainties)
        myMgr.keepManyNuisances(_keepUncertainties)
        myMgr.close()

if __name__ == "__main__":
    # Read datacards
    myDir = "."
    
    doCorrelation = True
    nobtagcorr = True
    
    # tau jets
    hplusTauNuToTauJets(myDir, doCorrelation=doCorrelation, nobtagcorr=nobtagcorr)
    sys.exit()
    # tau nu decay mode
    hplusTauNuToTauMu(myDir, doCorrelation=doCorrelation, nobtagcorr=nobtagcorr)
    
    hplusTauNuToDilepton(myDir, doCorrelation=doCorrelation, nobtagcorr=nobtagcorr)
    #sys.exit()
   
    # tb decay mode
    hplusTbToTauMu(myDir, doCorrelation=doCorrelation, nobtagcorr=nobtagcorr)
    hplusTbToDilepton(myDir, doCorrelation=doCorrelation, nobtagcorr=nobtagcorr)

