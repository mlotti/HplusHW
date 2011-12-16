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

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")

#QCDfromData = True
QCDfromData = False


# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.loadLuminosities()

    # Take QCD from data
    datasetsQCD = None
    if QCDfromData:
        datasetsQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/rkinnune/signalAnalysis/CMSSW_4_2_8_patch2/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_111123_132128/multicrab.cfg", counters=counters)
        datasetsQCD.loadLuminosities()
        datasetsQCD.mergeData()
        datasetsQCD.remove(datasetsQCD.getMCDatasetNames())
        datasetsQCD.rename("Data", "QCD")
    
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

    # Remove signals other than M120
    #datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    # Remove QCD
    datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
    histograms.createLegend.moveDefaults(dx=-0.02)
    histograms.createLegend.moveDefaults(dh=-0.03)
    
    datasets_lands = datasets.deepCopy()

    # Set the signal cross sections to the ttbar for datasets for lands
    xsect.setHplusCrossSectionsToTop(datasets_lands)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section


    # Replace signal dataset with EWK+signal
    if True:
        ttjets2 = datasets.getDataset("TTJets").deepCopy()
        ttjets2.setName("TTJets2")
        ttjets2.setCrossSection(ttjets2.getCrossSection() - datasets.getDataset("TTToHplus_M120").getCrossSection())
        datasets.append(ttjets2)
        datasets.merge("EWKnoTT", ["WJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
        datasets.merge("TTToHplus_M120", ["TTToHplus_M120", "EWKnoTT", "TTJets2"])
        plots._legendLabels["TTToHplus_M120"] = "with H^{#pm}#rightarrow#tau^{#pm}#nu"

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Write mt histograms to ROOT file
    #writeTransverseMass(datasets_lands)

    # Print counters
    doCounters(datasets)

# write histograms to file
def writeTransverseMass(datasets_lands):
    mt = plots.DataMCPlot(datasets_lands, analysis+"/transverseMass")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    f = ROOT.TFile.Open(output, "RECREATE")
    mt_data = mt.histoMgr.getHisto("Data").getRootHisto().Clone("mt_data")
    mt_data.SetDirectory(f)
    mt_hw = mt.histoMgr.getHisto("TTToHplusBWB_M120").getRootHisto().Clone("mt_hw")
    mt_hw.SetDirectory(f)
    mt_hh = mt.histoMgr.getHisto("TTToHplusBHminusB_M120").getRootHisto().Clone("mt_hh")
    mt_hh.SetDirectory(f)
    f.Write()
    f.Close()


def doPlots(datasets):
    def createPlot(name, **kwargs):
        return plots.DataMCPlot(datasets, analysis+"/"+name, **kwargs)

    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files

    # Primary vertices
#    vertexCount(createPlot("verticesBeforeWeight", normalizeToOne=True), postfix="BeforeWeight")
#    vertexCount(createPlot("verticesAfterWeight", normalizeToOne=True), postfix="AfterWeight")
    vertexCount(createPlot("Vertices/verticesTriggeredBeforeWeight", normalizeToOne=True), postfix="BeforeWeightTriggered")
    vertexCount(createPlot("Vertices/verticesTriggeredAfterWeight", normalizeToOne=True), postfix="AfterWeightTriggered")
#    vertexCount(createPlot("verticesTriggeredBeforeWeight", normalizeToOne=False), postfix="BeforeWeightTriggeredNorm")
#    vertexCount(createPlot("verticesTriggeredAfterWeight", normalizeToOne=False), postfix="AfterWeightTriggeredNorm")
#    met2(createPlot("MET"), "met1", rebin=50)
    
    # Tau
    tauPt(createPlot("SelectedTau/SelectedTau_pT_AfterTauID"), "SelectedTau_pT_AfterTauID", rebin=10, opts={"xmax": 250}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
    tauEta(createPlot("SelectedTau/SelectedTau_eta_AfterTauID"),"SelectedTau_eta_AfterTauID", rebin=10, opts={"ymin": 1e-1, "ymaxfactor": 40, "xmin": -2.5, "xmax": 2.5}, moveLegend={"dy":0.01, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.85))
    tauPhi(createPlot("SelectedTau/SelectedTau_phi_AfterTauID"), "SelectedTau_phi_AfterTauID", rebin=10)
    rtau(createPlot("SelectedTau/SelectedTau_Rtau_AfterTauID"), "SelectedTau_Rtau_AfterTauID", rebin=10, opts={"ymin": 1e-2, "ymaxfactor": 5, "xmax": 1.1}, moveLegend={"dx": -0.5}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
    rtau(createPlot("tauID/TauID_RtauCut"), "TauID_Rtau", rebin=1, opts={"ymin": 1e-2, "ymaxfactor": 5, "xmax": 1.1}, moveLegend={"dx": -0.5}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
    
    tauPt(createPlot("SelectedTau/SelectedTau_pT_AfterCuts"), "SelectedTau_pT_AfterCuts", rebin=1, opts={"ymin": 1e-4})
    tauEta(createPlot("SelectedTau/SelectedTau_eta_AfterCuts"),"SelectedTau_eta_AfterCuts", rebin=1)
    rtau(createPlot("SelectedTau/SelectedTau_Rtau_AfterCuts"), "SelectedTau_Rtau_AfterCuts", rebin=10, opts={"ymin": 1e-2, "ymaxfactor": 5, "xmax": 1.1}, moveLegend={"dx": -0.5}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
#    leadingTrack(createPlot("TauEmbeddingAnalysis_afterTauId_leadPFChargedHadrPt"), ratio=True)
    
    selectionFlow(createPlot("SignalSelectionFlow"), "SignalSelectionFlow", rebin=1)
    
    leadingTrack(createPlot("SelectedTau/SelectedTau_TauLeadingTrackPt"),"SelectedTau_TauLeadingTrackPt", rebin=10)
#    rtau(createPlot("genRtau1ProngHp"), "genRtau1ProngHp")
#    rtau(createPlot("genRtau1ProngW"), "genRtau1ProngW")
   
#    tauCandPt(createPlot("TauSelection_all_tau_candidates_pt"), step="begin")
#    tauCandEta(createPlot("TauSelection_all_tau_candidates_eta"), step="begin" )
#    tauCandPhi(createPlot("TauSelection_all_tau_candidates_phi"), step="begin" )

    # Electron veto
    drawPlot(createPlot("GlobalElectronVeto/GlobalElectronPt"), "electronPt", rebin=3, xlabel="p_{T}^{electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", opts={"xmax": 250}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=15)
    drawPlot(createPlot("GlobalElectronVeto/GlobalElectronEta"), "electronEta", rebin=2, xlabel="#eta^{electron}", ylabel="Identified electrons / %.1f", opts={"xmin": -3, "xmax": 3, "ymaxfactor": 50}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=[-2.5, 2.5])

    # Muon veto
    drawPlot(createPlot("GlobalMuonVeto/GlobalMuonPt"), "muonPt", rebin=3, xlabel="p_{T}^{muon} (GeV/c)", ylabel="Identified muons / %.0f GeV/c", opts={"xmax": 250}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=15)
    drawPlot(createPlot("GlobalMuonVeto/GlobalMuonEta"), "muonEta", rebin=2, xlabel="#eta^{muon}", ylabel="Identified muons / %.1f", opts={"xmin": -3, "xmax": 3, "ymaxfactor": 40}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=[-2.5, 2.5])

    # Jet selection
    drawPlot(createPlot("JetSelection/jet_pt_central"), "centralJetPt", rebin=5, xlabel="p_{T}^{jet} (GeV/c)", ylabel="Jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=30)
    drawPlot(createPlot("JetSelection/jet_pt"), "jetPt", rebin=5, xlabel="p_{T}^{jet} (GeV/c)", ylabel="Jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=30)
    drawPlot(createPlot("JetSelection/jet_eta"), "jetEta", rebin=4, xlabel="#eta^{jet}", ylabel="Jets / %.1f", opts={"ymaxfactor": 110}, moveLegend={"dy":0.01, "dx":-0.2, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.22), cutLine=[-2.4, 2.4])
    drawPlot(createPlot("JetSelection/jet_phi"), "jetPhi", rebin=10, xlabel="#phi^{jet}", ylabel="Jets / %.2f", textFunction=lambda: addMassBRText(x=0.3, y=0.87))
    drawPlot(createPlot("JetSelection/NumberOfSelectedJets"), "NumberOfJets", xlabel="Number of selected jets", ylabel="Events / %.0f", opts={"xmax": 10}, textFunction=lambda: addMassBRText(x=0.67, y=0.6), cutLine=3)

    # MET
    drawPlot(createPlot("Met"), "Met", rebin=25, xlabel="Raw PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=50)

    # b jets
    drawPlot(createPlot("Btagging/bjet_pt"), "bjetPt", rebin=15, xlabel="p_{T}^{b-tagged jet} (GeV/c)", ylabel="b-tagged jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("Btagging/bjet_eta"), "bjetEta", rebin=8, xlabel="#eta^{b-tagged jet}", ylabel="b-tagged jets / %.1f", opts={"ymaxfactor": 30, "xmin": -2.4, "xmax": 2.4}, moveLegend={"dy":0.01, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    drawPlot(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBJets", xlabel="Number of selected b jets", ylabel="Events / %.0f", opts={"xmax": 6}, textFunction=lambda: addMassBRText(x=0.45, y=0.87), cutLine=1)

     
    # Transverse mass
#    transverseMass(createPlot("TauEmbeddingAnalysis_afterTauId_TransverseMass"))
    transverseMass2(createPlot("transverseMass"), "transverseMass_standard", rebin=20)
    transverseMass2(createPlot("transverseMassMET70"), "transverseMassMET70", rebin=20)
    transverseMass2(createPlot("transverseMassAfterDeltaPhi"), "transverseMassAfterDeltaPhi", rebin=20)
#    transverseMass2(createPlot("transverseMassAfterDeltaPhi160"), "transverseMassAfterDeltaPhi160", rebin=20)
#    transverseMass2(createPlot("transverseMassAfterDeltaPhi130"), "transverseMassAfterDeltaPhi130", rebin=20)
#    transverseMass2(createPlot("transverseMassBeforeFakeMet"), "transverseMassBeforeFakeMet", rebin=20)
#    transverseMass2(createPlot("transverseMassBeforeVeto"), "transverseMassBeforeVeto")
#    transverseMass2(createPlot("transverseMassAfterVeto"), "transverseMassAfterVeto")
#    transverseMass2(createPlot("transverseMassWithTopCut"), "transverseMassWithTopCut")

    transverseMass2(createPlot("transverseMass"), "transverseMass", rebin=20, log=False, textFunction=lambda: addMassBRText(x=0.4, y=0.87))

    if QCDfromData:
        plot = replaceQCDfromData(createPlot("transverseMass"), datasetsQCD, analysis+"/transverseMass")
        transverseMass2(plot, "transverseMass", rebin=20)


    # Delta phi
#    deltaPhi(createPlot("TauEmbeddingAnalysis_afterTauId_DeltaPhi"))
    deltaPhi2(createPlot("deltaPhi"), "DeltaPhiTauMet", rebin=20, opts={"ymaxfactor": 20}, moveLegend={"dx":-0.21}, textFunction=lambda: addMassBRText(x=0.2, y=0.87), cutLine=[160, 130])
    deltaPhi2(createPlot("FakeMETVeto/Closest_DeltaPhi_of_MET_and_selected_jets"), "DeltaPhiJetMet")


    # Set temporarily the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSections(datasets, tanbeta=20, mu=200)
#    datasets.getDataset("TTToHplusBHminusB_M120").setCrossSection(0.2*165)
#    datasets.getDataset("TTToHplusBWB_M120").setCrossSection(0.2*165)


#    path = analysis+"/transverseMassWithRtauFakeMet"
#    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMassWithRtauFakeMet", rebin=20)
#    plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
#    transverseMass2(plot, "transverseMassWithRtauFakeMetQCDFromData", rebin=20)
    
#    path = analysis+"/transverseMassDeltaPhiUpperCut"
#    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMassDeltaPhiUpperCut", rebin=20)
#    plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
#    transverseMass2(plot, "transverseMassDeltaPhiUpperCutQCDFromData", rebin=20)

#    transverseMass2(createPlot("transverseMassBeforeVeto"), "transverseMassBeforeVeto", rebin=20)
#    transverseMass2(createPlot("transverseMassAfterVeto"), "transverseMassAfterVeto", rebin=20)
#    transverseMass2(createPlot("transverseMassWithTopCut"), "transverseMassWithTopCut", rebin=20)
#    transverseMass2(createPlot("transverseMassWithRtau"), "transverseMassWithRtau", rebin=20)
#    transverseMass2(createPlot("transverseMassWithRtauFakeMet"), "transverseMassWithRtauFakeMet", rebin=20)
#    transverseMass2(createPlot("transverseMassDeltaPhiUpperCut"), "transverseMassDeltaPhiUpperCut", rebin=20)
#    transverseMass2(createPlot("transverseMassDeltaPhiUpperCutFakeMet"), "transverseMassDeltaPhiUpperCutFakeMet", rebin=20)
#    transverseMass2(createPlot("transverseMassBeforeMetCut"), "transverseMassBeforeMetCut", rebin=20)
#    transverseMass2(createPlot("transverseMassTopDeltaPhiFakeMET"), "transverseMassTopDeltaPhiFakeMET", rebin=20)
#    transverseMass2(createPlot("transverseMassRtauDeltaPhiFakeMET"), "transverseMassRtauDeltaPhiFakeMET", rebin=20)
#    transverseMass2(createPlot("transverseMassBtag33RtauDeltaPhiFakeMET"), "transverseMassBtag33RtauDeltaPhiFakeMET", rebin=20)
#    xsect.setHplusCrossSections(datasets, toTop=True)

#    jetEMFraction(createPlot("JetSelection/jetMaxEMFraction"), "jetMaxEMFraction", rebin=10)
#    jetEMFraction(createPlot("JetSelection/jetEMFraction"), "jetEMFraction", rebin=20)
#    jetEMFraction(createPlot("JetSelection/chargedJetEMFraction"), "chargedJetEMFraction", rebin=20)
   
    
   
#    jetPt(createPlot("ForwardJetVeto/MaxForwJetEt"), "maxForwJetPt")

#    etSumRatio(createPlot("ForwardJetVeto/EtSumRatio"), "etSumRatio")
#    tauJetMass(createPlot("TauJetMass"), "TauJetMass")
#    topMass(createPlot("TopSelection/jjbMass"), "jjbMass")
#    topMass(createPlot("TopSelection/Mass_jjbMax"), "topMass_old")

#    topMass(createPlot("TopSelection/Mass_Top"), "topMass_realTop")
#    topMass(createPlot("TopSelection/Mass_bFromTop"), "topMass_bFromTop") 
#    ptTop(createPlot("TopSelection/Pt_jjb"), "pt_jjb")
#    ptTop(createPlot("TopSelection/Pt_jjbmax"), "ptTop")
#    ptTop(createPlot("TopSelection/Pt_top"), "ptTop_realTop")
#    met2(createPlot("MET_BaseLineTauId"), "MET_BaseLineTauId", rebin=10)
#    met2(createPlot("MET_InvertedTauId"), "MET_InvertedTauId", rebin=10)
#    met2(createPlot("MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)   
#    met2(createPlot("MET_BaseLineTauIdAllCuts"), "MET_BaseLineTauIdAllCuts", rebin=10)
#    met2(createPlot("MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)    
    
    pasJuly = "met_p4.Et() > 70 && Max$(jets_btag) > 1.7"
    topMass(plots.DataMCPlot(datasets, treeDraw.clone(varexp="topreco_p4.M()>>dist(20,0,800)", selection=pasJuly)), "topMass", rebin=1)

    #met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="met_p4.Et()>>dist(20,0,400)")), "metRaw", rebin=1)
    #met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="metType1_p4.Et()>>dist(20,0,400)")), "metType1", rebin=1)

    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt+">>dist(40,0,400)", selection=pasJuly)), "transverseMass_metRaw", rebin=1)
    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt.replace("met", "metType1")+">>dist(40,0,400)", selection=pasJuly.replace("met", "metType1"))), "transverseMass_metType1", rebin=1)

#    genComparison(datasets)
#    zMassComparison(datasets)
#    topMassComparison(datasets)
#    topPtComparison(datasets) 
#    vertexComparison(datasets)
#    mtComparison(datasets)

def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)

    # append row from the tree to the main counter
    eventCounter.getMainCounter().appendRow("MET > 70", treeDraw.clone(selection="met_p4.Et() > 70"))

    ewkDatasets = [
        "WJets", "TTJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]

    eventCounter.normalizeMCByLuminosity()
#    eventCounter.normalizeMCToLuminosity(73)
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
    print mainTable.format()



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
#    signal = "TTToHplusBWB_M120_Summer11"
#    background = "TTToHplusBWB_M120_Summer11"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/verticesBeforeWeight"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/verticesAfterWeight")),
#            "vertices_H120")

def mtComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("TTToHplus_M80").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplus_M90").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplus_M100").getDatasetRootHisto(analysis+"/transverseMass"),
        datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplus_M140").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplus_M150").getDatasetRootHisto(analysis+"/transverseMass"),
#        datasets.getDataset("TTToHplus_M155").getDatasetRootHisto(analysis+"/transverseMass"),
        datasets.getDataset("TTToHplus_M160").getDatasetRootHisto(analysis+"/transverseMass"),
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "transverseMass_vs_mH", rebin=20)


          
##############def genComparison(datasets):
#    rtau = plots.PlotBase([
#        datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngHp"),
#        datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngW")
#        ])
#    rtau.histoMgr.normalizeToOne()
#    rtau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    rtau._setLegendStyles()
#    rtau._setLegendLabels()
#    st1 = styles.getDataStyle().clone()
#    st2 = st1.clone()
#    st2.append(styles.StyleLine(lineColor=ROOT.kRed))
#    rtau.histoMgr.forHisto(datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngHp"), st1)
#    rtau.histoMgr.forHisto(datasets.getDataset("TTJets").getDatasetRootHisto(analysis+"/GenParticleAnalysis/genRtau1ProngW"), st2)
    
#    rtau.histoMgr.setHistoDrawStyleAll("P")
################    rtauGen(rtau, "RtauGenerated", rebin=1)


    
#def genComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTJets_TuneZ2"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/genRtau1ProngHp"),
#                                 datasets.getDataset(bagkground).getDatasetRootHisto(analysis+"/genRtau1ProngW")),
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

def replaceQCDfromData(plot, datasetsQCD, path):
    normalization = 0.00606 * 0.86
    drh = datasetsQCD.getDatasetRootHistos(path)
    if len(drh) != 1:
        raise Exception("There should only one DatasetRootHisto, got %d", len(drh))
    histo = histograms.HistoWithDatasetFakeMC(drh[0].getDataset(), drh[0].getHistogram(), drh[0].getName())
    histo.getRootHisto().Scale(normalization)
    plot.histoMgr.replaceHisto("QCD", histo)
    return plot

# Helper function to flip the last two parts of the histogram name
# e.g. ..._afterTauId_DeltaPhi -> DeltaPhi_afterTauId
def flipName(name):
    tmp = name.split("_")
    return tmp[-1] + "_" + tmp[-2]

# Common drawing function
def drawPlot(h, name, xlabel, ylabel="Events / %.0f GeV/c", rebin=1, log=True, addMCUncertainty=True, ratio=False, opts={}, opts2={}, moveLegend={}, textFunction=None, cutLine=None, cutBox=None):
    if cutLine != None and cutBox != None:
        raise Exception("Both cutLine and cutBox were given, only either one can exist")

    if rebin > 1:
        h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    ylab = ylabel
    if "%" in ylabel:
        ylab = ylabel % h.binWidth()

    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    if addMCUncertainty:
        h.addMCUncertainty()

    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts.update(opts)
    _opts2.update(opts2)

    #if log:
    #    name = name + "_log"
    h.createFrame(name, createRatio=ratio, opts=_opts, opts2=_opts2)
    if log:
        h.getPad().SetLogy(log)
    h.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    # Add cut line and/or box
    if cutLine != None:
        lst = cutLine
        if not isinstance(lst, list):
            lst = [lst]

        for line in lst:
            h.addCutBoxAndLine(line, box=False, line=True)
    if cutBox != None:
        lst = cutBox
        if not isinstance(lst, list):
            lst = [lst]

        for box in lst:
            h.addCutBoxAndLine(**box)

    common(h, xlabel, ylab, textFunction=textFunction)

# Common formatting
def common(h, xlabel, ylabel, addLuminosityText=True, textFunction=None):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    if addLuminosityText:
        h.addLuminosityText()
    if textFunction != None:
        textFunction()
    h.save()

# Functions below are for plot-specific formattings. They all take the
# plot object as an argument, then apply some formatting to it, draw
# it and finally save it to files.

def vertexCount(h, prefix="", postfix="", ratio=True):
        xlabel = "Number of good vertices"
        ylabel = "Number of events"

        if h.normalizeToOne:
            ylabel = "Arbitrary units."

        h.stackMCHistograms()

        stack = h.histoMgr.getHisto("StackedMC")
        #hsum = stack.getSumRootHisto()
        #total = hsum.Integral(0, hsum.GetNbinsX()+1)
        #for rh in stack.getAllRootHistos():
        #    dataset._normalizeToFactor(rh, 1/total)
        #dataset._normalizeToOne(h.histoMgr.getHisto("Data").getRootHisto())

        h.addMCUncertainty()

        opts = {}
        opts_log = {"ymin": 1e-10, "ymaxfactor": 10, "xmax": 30}
        opts_log.update(opts)

        opts2 = {"ymin": 0.5, "ymax": 3}
        opts2_log = opts2
        #opts2_log = {"ymin": 5e-2, "ymax": 5e2}
        
        h.createFrame(prefix+"vertices"+postfix, opts=opts, createRatio=ratio, opts2=opts2)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        h.histoMgr.addLuminosityText()
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        h.save()

        h.createFrame(prefix+"vertices"+postfix+"_log", opts=opts_log, createRatio=ratio, opts2=opts2_log)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.getPad1().SetLogy(True)
        #h.getPad2().SetLogy(True)
        h.setLegend(histograms.createLegend())
        h.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        #    histograms.addLuminosityText(x=None, y=None, lumi=191.)
        h.histoMgr.addLuminosityText()
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        h.save()

def rtauGen(h, name, rebin=5, ratio=False):
    #h.setDefaultStyles()
    h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p^{leading track} / p^{#tau jet}"
    ylabel = "Events / %.2f" % h.binWidth()
    if "Mass" in name:
        xlabel = "m (GeV/c^{2})"
    if "Rtau" in name:
        ylabel = "A.u."
    elif "Pt" in name:
        xlabel = "p_{T}(GeV/c)"
    elif "vertices" in name:
        xlabel = "N_{vertices}"
        
    kwargs = {"ymin": 0.1, "xmax": 300}

  
    if "Rtau" in name:
        kwargs = {"ymin": 0.0001, "xmax": 1.1}        
    elif "Pt" in name:
        kwargs = {"ymin": 0.1, "xmax": 400}
    elif "Mass" in name:
        kwargs = {"ymin": 0.1, "xmax": 300}
        
#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
#    name = name+"_log"



    h.createFrame(name, **kwargs)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.75, 0.4, 0.9))
    common(h, xlabel, ylabel, addLuminosityText=False)

def selectionFlow(h, name, rebin=1, ratio=False):

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Cut"
    ylabel = "Events"
    
        
    #h.stackMCSignalHistograms()
    h.stackMCHistograms()       
    h.addMCUncertainty()
    scaleMCfromWmunu(h)

    njets = 5
    lastSelection = njets
    
    opts = {"xmax": lastSelection, "ymin": 0.1, "ymaxfactor": 2, "nbins": lastSelection}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    h.createFrame(name, opts=opts, createRatio=ratio, opts2=opts2)
    xaxis = h.getFrame().GetXaxis()
    xaxis.SetBinLabel(1, "Trigger")
    xaxis.SetBinLabel(2, "#tau ID+R_{#tau}")
    xaxis.SetBinLabel(3, "e veto")
    xaxis.SetBinLabel(4, "#mu veto")
    xaxis.SetBinLabel(5, "N_{jets}")
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.addLuminosityText()
    addMassBRText(x=0.4, y=0.87)
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
    


def tauPt(h, name, **kwargs):
    xlabel = "p_{T}^{#tau jet} (GeV/c)"
    drawPlot(h, name, xlabel, **kwargs)

def tauEta(h, name, **kwargs):
    xlabel = "#eta^{#tau jet}"
    ylabel = "Events / %.1f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
    
def tauPhi(h, name, **kwargs):
    xlabel = "#phi^{#tau jet}"
    ylabel = "Events / %.1f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
    
def leadingTrack(h, name, rebin=5, ratio=False):
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
    h.setLegend(histograms.createLegend(0.65, 0.65, 0.9, 0.93))
    common(h, xlabel, ylabel)

def rtau(h, name, **kwargs):
    xlabel = "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}"
    ylabel = "Events / %.2f"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)

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


    
def met2(h, name, rebin=10, ratio=True):
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
    h.setLegend(histograms.createLegend(0.65, 0.65, 0.9, 0.93))
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
    
def deltaPhi2(h, name, **kwargs):
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss})^{#circ}"
    ylabel = "Events / %.0f^{#circ}"
    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)

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
    
def transverseMass2(h, name, **kwargs):
    xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})" 
    ylabel = "Events / %.0f GeV/c^{2}"

    drawPlot(h, name, xlabel, ylabel=ylabel, **kwargs)
       
def jetPt(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    opts = {"ymin": 0.001,"xmax": 500.0, "ymaxfactor": 2}
    opts2 = {"ymin": 0.05, "ymax": 1.5}
    particle = "jet"
    if "bjet" in name:
        particle = "b jet"
    if "electron" in name:
        particle = "electron"
        opts["xmax"] = 400
    if "muon" in name:
        particle = "muon"
        opts["xmax"] = 400
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{%s} (GeV/c)" % particle
#    xlabel = "p_{T}^{muon} (GeV/c)" 
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleMCfromWmunu(h)  
    h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)
    h.addMCUncertainty()


    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.6, 0.65, 0.9, 0.92))
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

    opts = {"ymin": 0.01,"xmin": -5,"xmax": 5, "ymaxfactor": 10}
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

    xlabel = "EMfraction in jets" 
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
    h.setLegend(histograms.createLegend(0.6, 0.6, 0.9, 0.92))
    common(h, xlabel, ylabel)
    
def numberOfJets(h, name, rebin=1, ratio=False):
    opts = {"ymin": 0.01,"xmax": 10.0, "ymaxfactor": 2.0}
    opts2 = {"ymin": 0.05, "ymax": 1.5}

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "BJets" in name:
        particle = "b jet"
        opts["xmax"] = 6
    xlabel = "Number of %ss" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleMCfromWmunu(h)
    h.stackMCHistograms()
    h.addMCUncertainty()
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.setLegend(histograms.createLegend(0.65, 0.65, 0.9, 0.92))
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

class AddMassBRText:
    def __init__(self):
        self.mass = 120
        self.br = 0.05
        self.size = 20
        self.separation = 0.04

    def setMass(self, mass):
        self.mass = mass

    def setBR(self, br):
        self.br = br

    def __call__(self, x, y):
        mass = "m_{H^{#pm}} = %d GeV/c^{2}" % self.mass
        br = "BR(t #rightarrow bH^{#pm})=%.2f" % self.br

        histograms.addText(x, y, mass, size=self.size)
        histograms.addText(x, y-self.separation, br, size=self.size)

addMassBRText = AddMassBRText()
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
