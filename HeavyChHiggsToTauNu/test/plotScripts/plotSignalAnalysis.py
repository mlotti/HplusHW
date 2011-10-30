#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen
#
######################################################################

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

# Configuration
analysis = "signalAnalysis"
#analysis = "signalOptimisation"
#analysis = "signalAnalysisJESMinus03eta02METMinus10"
#analysis = "EWKFakeTauAnalysisJESMinus03eta02METMinus10"
#analysis = "signalOptimisation/QCDAnalysisVariation_tauPt40_rtau0_btag2_METcut60_FakeMETCut0"
#analysis = "signalAnalysisTauSelectionHPSTightTauBased2"
#analysis = "signalAnalysisBtaggingTest2"
counters = analysis+"Counters/weighted"

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    datasets.loadLuminosities()

    # Take signals from 42X
#    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_4_patch1/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110621_150040/multicrab.cfg", counters=counters)
#Rtau =0
#    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110804_104313/multicrab.cfg", counters=counters)

#    datasetsSignal.selectAndReorder(["HplusTB_M200_Summer11"])
#    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_4_patch1/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110622_112321/multicrab.cfg", counters=counters)
    #datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_1_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/Signal_v11f_scaledb_424/multicrab.cfg", counters=counters)

    #datasetsSignal.selectAndReorder(["TTToHplusBWB_M120_Summer11", "TTToHplusBHminusB_M120_Summer11"])
    #datasetsSignal.renameMany({"TTToHplusBWB_M120_Summer11" :"TTToHplusBWB_M120_Spring11",
    #                           "TTToHplusBHminusB_M120_Summer11": "TTToHplusBHminusB_M120_Spring11"})
    #datasets.extend(datasetsSignal)

    plots.mergeRenameReorderForDataMC(datasets)

    # Set the signal cross sections to the ttbar
#    xsect.setHplusCrossSectionsToTop(datasets)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Apply TDR style
    style = tdrstyle.TDRStyle()


    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files
    vertexCount(plots.DataMCPlot(datasets, analysis+"/verticesBeforeWeight", normalizeToOne=True), postfix="BeforeWeight")
    vertexCount(plots.DataMCPlot(datasets, analysis+"/verticesAfterWeight", normalizeToOne=True), postfix="AfterWeight")
    vertexCount(plots.DataMCPlot(datasets, analysis+"/verticesTriggeredBeforeWeight", normalizeToOne=True), postfix="BeforeWeightTriggered")
    vertexCount(plots.DataMCPlot(datasets, analysis+"/verticesTriggeredAfterWeight", normalizeToOne=True), postfix="AfterWeightTriggered")
    vertexCount(plots.DataMCPlot(datasets, analysis+"/verticesTriggeredBeforeWeight", normalizeToOne=False), postfix="BeforeWeightTriggeredNorm")
    vertexCount(plots.DataMCPlot(datasets, analysis+"/verticesTriggeredAfterWeight", normalizeToOne=False), postfix="AfterWeightTriggeredNorm")
#    tauPt(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_selectedTauPt"), ratio=False)
#    tauEta(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_selectedTauEta"), ratio=False)
#    tauPhi(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_selectedTauPhi"), ratio=True)
#    leadingTrack(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_leadPFChargedHadrPt"), ratio=True)
#    met2(plots.DataMCPlot(datasets, analysis+"/MET"), "met1", rebin=50)
    
    tauPt(plots.DataMCPlot(datasets, analysis+"/SelectedTau_pT_AfterTauID"), "SelectedTau_pT_AfterTauID", rebin=10)
    tauEta(plots.DataMCPlot(datasets, analysis+"/SelectedTau_eta_AfterTauID"),"SelectedTau_eta_AfterTauID", rebin=10)
#    tauPt(plots.DataMCPlot(datasets, analysis+"/SelectedTau_pT_AfterCuts"), "SelectedTau_pT_AfterCuts", rebin=10)
#    tauEta(plots.DataMCPlot(datasets, analysis+"/SelectedTau_eta_AfterCuts"),"SelectedTau_eta_AfterCuts", rebin=10)
    tauPhi(plots.DataMCPlot(datasets, analysis+"/SelectedTau_phi_AfterTauID"), "SelectedTau_phi_AfterTauID")
    rtau(plots.DataMCPlot(datasets, analysis+"/SelectedTau_Rtau_AfterTauID"), "SelectedTau_Rtau_AfterTauID")
    tauPt(plots.DataMCPlot(datasets, analysis+"/SelectedTau_pT_AfterMetCut"), "SelectedTau_pT_AfterMetCut")
    tauEta(plots.DataMCPlot(datasets, analysis+"/SelectedTau_eta_AfterMetCut"), "SelectedTau_eta_AfterMetCut")
    tauPhi(plots.DataMCPlot(datasets, analysis+"/SelectedTau_phi_AfterMetCut"), "SelectedTau_phi_AfterMetCut")
    rtau(plots.DataMCPlot(datasets, analysis+"/SelectedTau_Rtau_AfterMetCut"), "SelectedTau_Rtau_AfterMetCut")
    rtau(plots.DataMCPlot(datasets, analysis+"/SelectedTau_Rtau_AfterCuts"), "SelectedTau_Rtau_AfterCuts")
#    leadingTrack(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_leadPFChargedHadrPt"), ratio=True)
    
    selectionFlow(plots.DataMCPlot(datasets, analysis+"/SignalSelectionFlow"), "SignalSelectionFlow")
    
#    rtau(plots.DataMCPlot(datasets, analysis+"/genRtau1ProngHp"), "genRtau1ProngHp")
#    rtau(plots.DataMCPlot(datasets, analysis+"/genRtau1ProngW"), "genRtau1ProngW")
   
#    tauCandPt(plots.DataMCPlot(datasets, analysis+"/TauSelection_all_tau_candidates_pt"), step="begin")
#    tauCandEta(plots.DataMCPlot(datasets, analysis+"/TauSelection_all_tau_candidates_eta"), step="begin" )
#    tauCandPhi(plots.DataMCPlot(datasets, analysis+"/TauSelection_all_tau_candidates_phi"), step="begin" )
    
   
#   met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_embeddingMet"), ratio=True)
#   met(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_begin_embeddingMet"), ratio=True)

#    met2(plots.DataMCPlot(datasets, analysis+"/Met_BeforeTauId"), "MetBeforeTauId", rebin=40)

    met2(plots.DataMCPlot(datasets, analysis+"/MET_BeforeMETCut"), "met", rebin=20)
#    met2(plots.DataMCPlot(datasets, analysis+"/Met_BeforeTauId"), "met_beforeTauId", rebin=20)
     
#    deltaPhi(plots.DataMCPlot(datasets, analysis+"/TauEmbeddingAnalysis_afterTauId_DeltaPhi"))
    deltaPhi2(plots.DataMCPlot(datasets, analysis+"/deltaPhi"), "DeltaPhiTauMet", rebin=10)
    deltaPhi2(plots.DataMCPlot(datasets, analysis+"/FakeMETVeto/Closest_DeltaPhi_of_MET_and_selected_jets"), "DeltaPhiJetMet")


    # Set temporarily the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSections(datasets, tanbeta=20, mu=200)
#    datasets.getDataset("TTToHplusBHminusB_M120").setCrossSection(0.2*165)
#    datasets.getDataset("TTToHplusBWB_M120").setCrossSection(0.2*165)

####################
    datasets_tm = datasets
#    datasets_tm = datasets.deepCopy()
#    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.2, br_Htaunu=1)
#    xsect.setHplusCrossSectionsToBR(datasets_tm, br_tH=0.2, br_Htaunu=1)
#    datasets_tm.merge("TTToHplus_M120", ["TTToHplusBWB_M120", "TTToHplusBHminusB_M120"])

#    transverseMass(plots.DataMCPlot(datasets_tm, analysis+"/TauEmbeddingAnalysis_afterTauId_TransverseMass"))
#    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/transverseMass"), "transverseMass")
#    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/transverseMassBeforeFakeMet"), "transverseMassBeforeFakeMet", rebin=20)
#    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/transverseMassBeforeVeto"), "transverseMassBeforeVeto")
#    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/transverseMassAfterVeto"), "transverseMassAfterVeto")
#    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/transverseMassWithTopCut"), "transverseMassWithTopCut")

    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMass"), "transverseMass")
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMassBeforeFakeMet"), "transverseMassBeforeFakeMet", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMassBeforeVeto"), "transverseMassBeforeVeto")
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMassAfterVeto"), "transverseMassAfterVeto")
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMassWithTopCut"), "transverseMassWithTopCut")
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMassWithRtau"), "transverseMassWithRtau")
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMassWithRtauFakeMet"), "transverseMassWithRtauFakeMet")
    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMassDeltaPhiUpperCut"), "transverseMassDeltaPhiUpperCut", rebin=20)
    
#    xsect.setHplusCrossSections(datasets, toTop=True)


    jetPt(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_pt"), "jetPt", rebin=20)
    jetEta(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_eta"), "jetEta", rebin=10)
    jetPhi(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_phi"), "jetPhi", rebin=10)
    numberOfJets(plots.DataMCPlot(datasets, analysis+"/JetSelection/NumberOfSelectedJets"), "NumberOfJets")
    jetEMFraction(plots.DataMCPlot(datasets, analysis+"/JetSelection/jetMaxEMFraction"), "jetMaxEMFraction", rebin=10)
    
    jetPt(plots.DataMCPlot(datasets, analysis+"/Btagging/bjet_pt"), "bjetPt", rebin=30)
    jetEta(plots.DataMCPlot(datasets, analysis+"/Btagging/bjet_eta"), "bjetEta", rebin=30)
    numberOfJets(plots.DataMCPlot(datasets, analysis+"/Btagging/NumberOfBtaggedJets"), "NumberOfBJets")
    
    jetPt(plots.DataMCPlot(datasets, analysis+"/GlobalElectronVeto/GlobalElectronPt"), "electronPt")
    jetEta(plots.DataMCPlot(datasets, analysis+"/GlobalElectronVeto/GlobalElectronEta"), "electronEta")
    
    jetPt(plots.DataMCPlot(datasets, analysis+"/GlobalMuonVeto/GlobalMuonPt"), "muonPt")
    jetEta(plots.DataMCPlot(datasets, analysis+"/GlobalMuonVeto/GlobalMuonEta"), "muonEta")
    
    jetPt(plots.DataMCPlot(datasets, analysis+"/ForwardJetVeto/MaxForwJetEt"), "maxForwJetPt")

    etSumRatio(plots.DataMCPlot(datasets, analysis+"/ForwardJetVeto/EtSumRatio"), "etSumRatio")
    tauJetMass(plots.DataMCPlot(datasets, analysis+"/TauJetMass"), "TauJetMass")
    topMass(plots.DataMCPlot(datasets, analysis+"/TopSelection/Mass_jjbMax"), "topMass_old")
    topMass(plots.DataMCPlot(datasets, analysis+"/TopSelection/Mass_Top"), "topMass_realTop")
    topMass(plots.DataMCPlot(datasets, analysis+"/TopSelection/Mass_bFromTop"), "topMass_bFromTop") 
    ptTop(plots.DataMCPlot(datasets, analysis+"/TopSelection/Pt_jjb"), "pt_jjb")
    ptTop(plots.DataMCPlot(datasets, analysis+"/TopSelection/Pt_jjbmax"), "ptTop")
    ptTop(plots.DataMCPlot(datasets, analysis+"/TopSelection/Pt_top"), "ptTop_realTop") 
    
    
    td = dataset.TreeDraw("signalAnalysis/tree", weight="weightPileup*weightTrigger*weightPrescale")
    pasJuly = "met_p4.Et() > 70 && Max$(jets_btag) > 1.7"
    topMass(plots.DataMCPlot(datasets, td.clone(varexp="topreco_p4.M()>>dist(20,0,800)", selection=pasJuly)), "topMass", rebin=1)

    met2(plots.DataMCPlot(datasets, td.clone(varexp="met_p4.Et()>>dist(40,0,400)")), "metRaw", rebin=1)
    met2(plots.DataMCPlot(datasets, td.clone(varexp="metType1_p4.Et()>>dist(40,0,400)")), "metType1", rebin=1)

    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
    transverseMass2(plots.DataMCPlot(datasets, td.clone(varexp=mt+">>dist(40,0,400)", selection=pasJuly)), "transverseMass_metRaw", rebin=1)
    transverseMass2(plots.DataMCPlot(datasets, td.clone(varexp=mt.replace("met", "metType1")+">>dist(40,0,400)", selection=pasJuly.replace("met", "metType1"))), "transverseMass_metType1", rebin=1)

#    genComparison(datasets)
#    zMassComparison(datasets)
#    topMassComparison(datasets)
#    topPtComparison(datasets) 
#    vertexComparison(datasets)


    eventCounter = counter.EventCounter(datasets)

    # append row from the tree to the main counter
    eventCounter.getMainCounter().appendRow("MET > 70", td.clone(selection="met_p4.Et() > 70"))

    eventCounter.normalizeMCByLuminosity()
#    eventCounter.normalizeMCToLuminosity(73)
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

#    print eventCounter.getSubCounterTable("GlobalMuon_ID").format()

    print eventCounter.getSubCounterTable("tauIDTauSelection").format()
    print eventCounter.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight").format()
#    print eventCounter.getSubCounterTable("TauIDPassedJets::tauID_HPSTight").format()
    print eventCounter.getSubCounterTable("b-tagging").format()
    print eventCounter.getSubCounterTable("Jet selection").format()
    print eventCounter.getSubCounterTable("Jet main").format()    

    
#    latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f"))
#    print eventCounter.getMainCounterTable().format(latexFormat)


#def vertexComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTToHplusBWB_M120"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/verticesBeforeWeight"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/verticesAfterWeight")),
#            "vertices_H120")

#def genComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTJets_TuneZ2"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/genRtau1ProngHp"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/genRtau1ProngW")),
#          "RtauGen_Hp_vs_tt")
    
    
#def zMassComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "DYJetsToLL"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/TauJetMass"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/TauJetMass")),
#            "TauJetMass_Hp_vs_Zll")
    
#def topMassComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTToHplusBWB_M120"
#    rtauGen(plots.PlotBase([datasets.getDataset(signal).getDatasetRootHisto(analysis+"/TopSelection/Mass_jjbMax"),
#                            datasets.getDataset(background).getDatasetRootHisto(analysis+"/Mass_Top"),
#                            datasets.getDataset(background).getDatasetRootHisto(analysis+"/TopSelection/MassMax_Top")]),
#             "topMass_all_vs_real")

#def topPtComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTToHplusBWB_M120"
#    rtauGen(plots.PlotBase([datasets.getDataset(signal).getDatasetRootHisto(analysis+"/TopSelection/Pt_jjb"),
#                            datasets.getDataset(background).getDatasetRootHisto(analysis+"/TopSelection/Pt_jjbmax"),
#                            datasets.getDataset(background).getDatasetRootHisto(analysis+"/TopSelection/Pt_top")]),
#             "topPt_all_vs_real")

def scaleMC(histo, scale):
    if histo.isMC():
        th1 = histo.getRootHisto()
        th1.Scale(scale)

def scaleMCHistos(h, scale):
    h.histoMgr.forEachHisto(lambda histo: scaleMC(histo, scale))

def scaleMCfromWmunu(h):
    # Data/MC scale factor from AN 2011/053
#    scaleMCHistos(h, 1.736)
    scaleMCHistos(h, 1.0)



    
# Helper function to flip the last two parts of the histogram name
# e.g. ..._afterTauId_DeltaPhi -> DeltaPhi_afterTauId
def flipName(name):
    tmp = name.split("_")
    return tmp[-1] + "_" + tmp[-2]

# Common formatting
def common(h, xlabel, ylabel, addLuminosityText=True):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    h.save()

# Functions below are for plot-specific formattings. They all take the
# plot object as an argument, then apply some formatting to it, draw
# it and finally save it to files.

def vertexCount(h, prefix="", postfix=""):
        xlabel = "Number of vertices"
        ylabel = "A.u."

        h.stackMCHistograms()

        stack = h.histoMgr.getHisto("StackedMC")
        #hsum = stack.getSumRootHisto()
        #total = hsum.Integral(0, hsum.GetNbinsX()+1)
        #for rh in stack.getAllRootHistos():
        #    dataset._normalizeToFactor(rh, 1/total)
        #dataset._normalizeToOne(h.histoMgr.getHisto("Data").getRootHisto())

        h.addMCUncertainty()

        opts = {}
        opts_log = {"ymin": 1e-10, "ymaxfactor": 10}
        opts_log.update(opts)
        
        h.createFrame(prefix+"vertices"+postfix, opts=opts)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        h.histoMgr.addLuminosityText()
        h.save()

        h.createFrame(prefix+"vertices"+postfix+"_log", opts=opts_log)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        ROOT.gPad.SetLogy(True)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        h.histoMgr.addLuminosityText()
        h.save()

def rtauGen(h, name, rebin=5, ratio=False):
    #h.setDefaultStyles()
    h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "R_{#tau}"
    if "Mass" in name:
        xlabel = "m (GeV/c^{2})"
    elif "Pt" in name:
        xlabel = "p_{T}(GeV/c)"
    elif "vertices" in name:
        xlabel = "N_{vertices}"
    ylabel = "Events / %.2f" % h.binWidth()

    if "gen" in name:
        kwargs = {"ymin": 0.1, "xmax": 1.1}        
    elif "Pt" in name:
        kwargs = {"ymin": 0.1, "xmax": 400}
    elif "Mass" in name:
        kwargs = {"ymin": 0.1, "xmax": 500}
        
    kwargs = {"ymin": 0.1, "xmax": 500}
#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
#    name = name+"_log"

    h.createFrame(name, **kwargs)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.75, 0.4, 0.9))
    common(h, xlabel, ylabel, addLuminosityText=False)

def selectionFlow(h, name, rebin=1, ratio=False):

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Cut"
    ylabel = "Events"

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"xmax": 7, "ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()    

def tauCandPt(h, step="", rebin=2):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylabel = "Events /%.0f GeV/c" % h.binWidth()   
    xlabel = "p_{T}^{#tau candidate} (GeV/c)"
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           

    name = "tauCandidatePt_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()
    
def tauCandEta(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#tau candidate}"
    ylabel = "Events / %.1f" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.001
           
#    opts = {"xmax": 2.5,"xmin":-2.5}
#    opts["xmin"] = -2.7
#    opts["xmax"] =  2.7    
    name = "tauCandidateEta_%s_log" % step
#    h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend(0.5, 0.2, 0.7, 0.5))
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()

def tauCandPhi(h, step="", rebin=5):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#phi^{#tau candidate}"
    ylabel = "Events / %.1f" % h.binWidth()
    opts = {"ymaxfactor": 2}
    
    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    if h.normalizeToOne:
        ylabel = "A.u."
        opts["yminfactor"] = 1e-5
    else:
        opts["ymin"] = 0.01
           

    name = "tauCandidatePhi_%s_log" % step
    h.createFrameFraction(name, opts=opts)
    #h.createFrame(name, opts=opts)
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    #h.addLuminosityText()
    h.save()
    


def tauPt(h, name, rebin=5, ratio=False):
#    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{#tau jet} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.0001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = "selectedTauPt"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    common(h, xlabel, ylabel)
    
def tauEta(h, name, rebin=5, ratio=False):
#    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#tau jet}"
    ylabel = "Events"

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    
    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = "selectedTauEta"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
    common(h, xlabel, ylabel)
    
def tauPhi(h, name, rebin=10, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#phi^{#tau jet}"
    ylabel = "Events"

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = "selectedTauPhi"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.3, 0.9, 0.6))
    common(h, xlabel, ylabel)
    
def leadingTrack(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{leading track} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.001,"xmin": 10.0, "ymaxfactor": 5}
    name = "leadingTrackPt"
#    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def rtau(h, name, rebin=15, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "R_{#tau}"
    ylabel = "Events / %.2f" % h.binWidth()

    h.stackMCHistograms()
    h.addMCUncertainty()
    scaleMCfromWmunu(h)
    
    opts = {"ymin": 0.001,"xmax": 1.1, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.68, 0.4, 0.93))
    common(h, xlabel, ylabel)


def met(h, rebin=20, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "MET (GeV)"
#    if "embedding" in name:
#        xlabel = "Embedded "+xlabel
#    elif "original" in name:
#        xlabel = "Original "+xlabel
    
    ylabel = "Events / %.0f GeV" % h.binWidth()

    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = "MET"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)


    
def met2(h, name, rebin=30, ratio=True):
#    name = h.getRootHistoPath()
#    name = "met"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    xlabel = "MET (GeV)"
#    if "embedding" in name:
#        xlabel = "Embedded "+xlabel
#    elif "original" in name:
#        xlabel = "Original "+xlabel
    ylabel = "Events / %.0f GeV" % h.binWidth()
    xlabel = "E_{T}^{miss} (GeV)"
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.0, "ymax": 2.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.65, 0.55, 0.9, 0.9))
    common(h, xlabel, ylabel)



def deltaPhi(h, rebin=40, ratio=False):
    name = flipName(h.getRootHistoPath())

    particle = "#tau jet"
    if "Original" in name:
        particle = "#mu"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#Delta#phi(%s, MET) (rad)" % particle
    ylabel = "Events / %.2f rad" % h.binWidth()
    
    scaleMCfromWmunu(h)    
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    #h.createFrameFraction(name)
    h.createFrame(name)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.6, 0.4, 0.9))
    common(h, xlabel, ylabel)
    
def deltaPhi2(h, name, rebin=2):
#    name = flipName(h.getRootHistoPath())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

#    particle = "jet"
#    if "taus" in name:
#        particle = "jet,#tau"
    xlabel = "#Delta#phi(#tau jet, MET)^{0}"
    ylabel = "Events / %.2f deg" % h.binWidth()
    
    scaleMCfromWmunu(h)      
    h.stackMCHistograms()
    h.addMCUncertainty()
    
#    name = "deltaPhiMetJet"
    #h.createFrameFraction(name)
#    h.createFrame(name)
    opts = {"ymin": 0.001, "ymaxfactor": 2}
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.3, 0.4, 0.5))
    common(h, xlabel, ylabel)


    
    
def transverseMass(h, rebin=20):
    name = flipName(h.getRootHistoPath())

    particle = ""
    if "Original" in name:
        particle = "#mu"
        name = name.replace("TransverseMass", "Mt")
    else:
        particle = "#tau jet"
        name = name.replace("TransverseMass", "Mt")

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(%s, MET) (GeV/c^{2})" % particle
    ylabel = "Events / %.2f GeV/c^{2}" % h.binWidth()
    
    scaleMCfromWmunu(h)     
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)#stackSignal=True)
    h.addMCUncertainty()

    opts = {"xmax": 200}

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def transverseMass2(h,name, rebin=10):
#    name = flipName(h.getRootHistoPath())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(#tau jet, MET) (GeV/c^{2})" 
    ylabel = "Events / %.2f GeV/c^{2}" % h.binWidth()
    
    scaleMCfromWmunu(h)    
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)#stackSignal=True)
    h.addMCUncertainty()
    
#    name = name+"_log"
    opts = {"ymin": 0.001, "ymaxfactor": 2.0,"xmax": 350 }
#    opts = {"xmax": 200 }
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.68, 0.9, 0.93))
    common(h, xlabel, ylabel)
       
def jetPt(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "b jet"
    if "electron" in name:
        particle = "electron"
    if "muon" in name:
        particle = "muon"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{%s} (GeV/c)" % particle
#    xlabel = "p_{T}^{muon} (GeV/c)" 
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)
    h.addMCUncertainty()

    opts = {"ymin": 0.001,"xmax": 400.0, "ymaxfactor": 2}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.65, 0.9, 0.9))
    common(h, xlabel, ylabel)

    
def jetEta(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "b jet"
    if "electron" in name:
        particle = "electron"
    if "muon" in name:
        particle = "muon"
    xlabel = "#eta^{%s}" % particle
#    xlabel = "#eta^{muon}"
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01,"xmin": -3.5,"xmax": 3.5, "ymaxfactor": 10}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.7, 0.9, 0.95))
#    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def jetPhi(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
    xlabel = "#phi^{%s}" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.7, 0.2, 0.9, 0.5))
    common(h, xlabel, ylabel)
    
def jetEMFraction(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    xlabel = "max(EMfraction) in jets" 
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.2, 0.4, 0.5))
    common(h, xlabel, ylabel)

def numberOfJets(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "Btagged" in name:
        particle = "b jet"
    xlabel = "Number of %ss" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01,"xmax": 7.0, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def etSumRatio(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "#Sigma E_{T}^{Forward} / #Sigma E_{T}^{Central}"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def tauJetMass(h, name, rebin=1, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "#Sigma E_{T}^{Forward} / #Sigma E_{T}^{Central}"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.001, "ymaxfactor": 1.5}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)



def topMass(h, name, rebin=20, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "m_{top} (GeV/c^{2})"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def ptTop(h, name, rebin=10, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
#    particle = "jet"
#    if "bjet" in name:
#        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{top} (GeV/c)"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0001, "xmax": 500, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)   
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
