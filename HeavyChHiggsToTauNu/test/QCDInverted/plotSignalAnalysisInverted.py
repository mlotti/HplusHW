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
deltaPhi180 = False
deltaPhi160 = False
deltaPhi130 = True
btagging = False

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
        print "QCDfromData", QCDfromData
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

    print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    datasets_lands = datasets.deepCopy()

    # Set the signal cross sections to the ttbar for datasets for lands
    xsect.setHplusCrossSectionsToTop(datasets_lands)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section


    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Write mt histograms to ROOT file
#    writeTransverseMass(datasets_lands)

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
    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files


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


    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet4050"), "MTInvertedTauIdJet4050", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet5060"), "MTInvertedTauIdJet5060", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet6070"), "MTInvertedTauIdJet6070", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet7080"), "MTInvertedTauIdJet7080", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet80100"), "MTInvertedTauIdJet80100", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet100120"), "MTInvertedTauIdJet100120", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet120150"), "MTInvertedTauIdJet120150", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet150"), "MTInvertedTauIdJet150", rebin=20)                       
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJet"), "MTInvertedTauIdJet", rebin=20)
    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdJetPhi"), "MTInvertedTauIdJetPhi", rebin=20)
#    transverseMass2(plots.DataMCPlot(datasets_tm, analysis+"/MTInvertedTauIdMet"), "MTInvertedTauIdMet", rebin=10)  


    transverseMass2(plots.DataMCPlot(datasets, analysis+"/transverseMass"), "transverseMass", rebin=20)
    path = analysis+"/transverseMass"
    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMass", rebin=20)
    if QCDfromData:
        plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
        transverseMass2(plot, "transverseMass", rebin=20)




    jetPt(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_pt"), "jetPt", rebin=20)
    jetEta(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_eta"), "jetEta", rebin=10)
    jetPhi(plots.DataMCPlot(datasets, analysis+"/JetSelection/jet_phi"), "jetPhi", rebin=10)
    numberOfJets(plots.DataMCPlot(datasets, analysis+"/JetSelection/NumberOfSelectedJets"), "NumberOfJets")
    jetEMFraction(plots.DataMCPlot(datasets, analysis+"/JetSelection/jetMaxEMFraction"), "jetMaxEMFraction", rebin=10)
    jetEMFraction(plots.DataMCPlot(datasets, analysis+"/JetSelection/jetEMFraction"), "jetEMFraction", rebin=20)
#    jetEMFraction(plots.DataMCPlot(datasets, analysis+"/JetSelection/chargedJetEMFraction"), "chargedJetEMFraction", rebin=20)
   
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
    topMass(plots.DataMCPlot(datasets, analysis+"/TopSelection/jjbMass"), "jjbMass")
    topMass(plots.DataMCPlot(datasets, analysis+"/TopChiSelection/TopMass"), "topMass_chi")

  
    met2(plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdJets"), "MET_BaseLineTauIdJets", rebin=20)
    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdJets"), "MET_InvertedTauIdJets", rebin=20)
#    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)   
#    met2(plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdAllCuts"), "MET_BaseLineTauIdAllCuts", rebin=10)
#    met2(plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdAllCuts"), "MET_InvertedTauIdAllCuts", rebin=10)    
    
    pasJuly = "met_p4.Et() > 70 && Max$(jets_btag) > 1.7"
    topMass(plots.DataMCPlot(datasets, treeDraw.clone(varexp="topreco_p4.M()>>dist(20,0,800)", selection=pasJuly)), "topMass", rebin=1)

    met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="met_p4.Et()>>dist(20,0,400)")), "metRaw", rebin=1)
    met2(plots.DataMCPlot(datasets, treeDraw.clone(varexp="metType1_p4.Et()>>dist(20,0,400)")), "metType1", rebin=1)

    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt+">>dist(40,0,400)", selection=pasJuly)), "transverseMass_metRaw", rebin=1)
    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt.replace("met", "metType1")+">>dist(40,0,400)", selection=pasJuly.replace("met", "metType1"))), "transverseMass_metType1", rebin=1)

#    genComparison(datasets)
#    zMassComparison(datasets)
#    topMassComparison(datasets)
#    topPtComparison(datasets) 
#    vertexComparison(datasets)
    mtComparison(datasets)
    metComparison(datasets)
    
def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)

    # append row from the tree to the main counter
    eventCounter.getMainCounter().appendRow("MET > 70", treeDraw.clone(selection="met_p4.Et() > 70"))

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
#    signal = "TTToHplusBWB_M120_Summer11"
#    background = "TTToHplusBWB_M120_Summer11"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto(analysis+"/verticesBeforeWeight"),
#                                 datasets.getDataset(background).getDatasetRootHisto(analysis+"/verticesAfterWeight")),
#            "vertices_H120")

def mtComparison(datasets):
    
    ## After standard cuts
    if (deltaPhi180):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet100120")])
        mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet120150")])
        mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet150")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJet")])
             

  ## With MET > 70 GeV
                        
#   mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet4050")])
#   mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet5060")])
#    mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet6070")])
#    mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet7080")])
#    mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet80100")])
#    mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet100120")])
#    mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet120150")])
#    mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet150")])
#    mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdMet")])

## After deltaPhi < 160 cut
    if (deltaPhi160):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi100120")])
        mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi120150")])
        mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi150")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdJetPhi")])
             
## After deltaPhi < 130 cut
    if (deltaPhi130):
        mt4050 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass4050")])
        mt5060 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass5060")])
        mt6070 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass6070")])
        mt7080 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass7080")])
        mt80100 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass80100")])
        mt100120 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass100120")])
        mt120150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass120150")])
        mt150 = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass150")])
        mt = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MTInvertedTauIdTopMass")])






#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mt4050._setLegend(histograms.createLegend())


    mt4050._setLegendStyles()
    mt4050._setLegendLabels()
    mt4050.histoMgr.setHistoDrawStyleAll("P")

    mt4050.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))    



    hmt4050 = mt4050.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet4050")
    if (btagging):
        hmt4050.Scale(0.00926618859472)   # btag
    else:
        hmt4050.Scale(0.00903051176553)  # jets
    
    mt5060._setLegendStyles()
    mt5060._setLegendLabels()
    mt5060.histoMgr.setHistoDrawStyleAll("P")
    mt5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))
    hmt5060 = mt5060.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet5060")
    if (btagging):
        hmt5060.Scale(0.00734036139081) #btag
    else:
        hmt5060.Scale(0.00734356165245) #jets
    
    mt6070._setLegendStyles()
    mt6070._setLegendLabels()
    mt6070.histoMgr.setHistoDrawStyleAll("P")
    mt6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))    
    hmt6070 = mt6070.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet6070")
    if (btagging):
        hmt6070.Scale(0.00639483478917) #btag
    else:
        hmt6070.Scale(0.00602980674872) # jets
    
    mt7080._setLegendStyles()
    mt7080._setLegendLabels()
    mt7080.histoMgr.setHistoDrawStyleAll("P")
    mt7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hmt7080 = mt7080.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet7080")
    if (btagging):
        hmt7080.Scale(0.00305291117148) # btag
    else:
        hmt7080.Scale(0.00592912119185) #jets
    
    mt80100._setLegendStyles()
    mt80100._setLegendLabels()
    mt80100.histoMgr.setHistoDrawStyleAll("P")
    mt80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20)) 
    hmt80100 = mt80100.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet80100")
    if (btagging):
        hmt80100.Scale(0.00739504574301)  #btag
    else:
        hmt80100.Scale(0.00428978785202) #jets
    
    mt100120._setLegendStyles()
    mt100120._setLegendLabels()
    mt100120.histoMgr.setHistoDrawStyleAll("P")
    mt100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))     
    hmt100120 = mt100120.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet100120")
    if (btagging):
        hmt100120.Scale(0.00629352541869) #btag
    else:
        hmt100120.Scale(0.00660273694354) #jets
    
    mt120150._setLegendStyles()
    mt120150._setLegendLabels()
    mt120150.histoMgr.setHistoDrawStyleAll("P")
    mt120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))      
    hmt120150 = mt120150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet120150")
    if (btagging):
        hmt120150.Scale(0.00320604463821) # btag
    else:
        hmt120150.Scale(0.00433342965036) #jets
    
    mt150._setLegendStyles()
    mt150._setLegendLabels()
    mt150.histoMgr.setHistoDrawStyleAll("P")
    mt150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmt150 = mt150.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet150")
    if (btagging):
        hmt150.Scale(0.00196125593388) #btag
    else:
        hmt150.Scale(0.00155574283764) #jets
        
    mt._setLegendStyles()
    mt._setLegendLabels()
    mt.histoMgr.setHistoDrawStyleAll("P")
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))  
    hmt = mt.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MTInvertedTauIdJet")

# with b tagging
    if (btagging):
        hmt.Scale(0.00796880943964)
    else:
# after 3 jets        
        hmt.Scale(0.00660933932487)
        
    hmtSum = hmt4050.Clone("mtSum")
    hmtSum.SetName("mtSum")
    hmtSum.SetTitle("Inverted tau ID")
    hmtSum.Add(hmt5060)
    hmtSum.Add(hmt6070)
    hmtSum.Add(hmt7080)
    hmtSum.Add(hmt80100)
    hmtSum.Add(hmt100120)
    hmtSum.Add(hmt120150)
    hmtSum.Add(hmt150)
    
    canvas = ROOT.TCanvas("canvas","",500,500)
    canvas.Divide(3,3)
    canvas.cd(1)
    hmt4050.GetYaxis().SetTitle("Events")
    hmt4050.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    hmt4050.Draw()
    canvas.cd(2)
    hmt5060.Draw()
    canvas.cd(3)
    hmt6070.Draw()
    canvas.cd(4)
    hmt7080.Draw()
    canvas.cd(5)
    hmt80100.Draw()
    canvas.cd(6)
    hmt100120.Draw()
    canvas.cd(7)
    hmt120150.Draw()
    canvas.cd(8)
    hmt150.Draw()
    
    canvas.cd(9)
    hmtSum.Draw()
#    canvas.Print("mtComparison_PhiCut.png")
    if(btagging):
        if(deltaPhi180): 
            canvas.Print("mtComparison_btag.png")
            canvas.Print("mtComparison_btag.C")
        if(deltaPhi160):
            canvas.Print("mtComparison_btag_dphi160.png")
            canvas.Print("mtComparison_btag_dphi160.C")
        if(deltaPhi130):
            canvas.Print("mtComparison_btag_dphi130.png")
            canvas.Print("mtComparison_btag_dphi130.C")      
    else:
        if(deltaPhi180): 
            canvas.Print("mtComparison_3jets.png")
            canvas.Print("mtComparison_3jets.C")
        if(deltaPhi160):
            canvas.Print("mtComparison_3jets_dphi160.png")
            canvas.Print("mtComparison_3jets_dphi160.C")  
        if(deltaPhi130):
            canvas.Print("mtComparison_3jets_dphi130.png")
            canvas.Print("mtComparison_3jets_dphi130.C")  
        
##    rtauGen(mt4050, "transverseMass_vs_pttau", rebin=20)
    print "Integral  = ",hmtSum.Integral()
    
############
    canvas2 = ROOT.TCanvas("canvas2","",500,500)   
    hmtSum.Draw()
    hmtSum.GetYaxis().SetTitle("Events")
    hmtSum.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
    canvas2.Print("mtSum_PhiCut.png")

###########

    
    canvas3 = ROOT.TCanvas("canvas3","",500,500)
#    canvas3.SetLogy()
#    hmt.SetMaximum(3.0)
    hmt.SetMarkerColor(2)
    hmt.SetMarkerSize(1)
    hmt.SetMarkerStyle(21)
    hmt.Draw("EP")
    
    hmtSum.SetMarkerColor(4)
    hmtSum.SetMarkerSize(1)
    hmtSum.SetMarkerStyle(20)
    hmtSum.SetFillColor(4)
    hmtSum.Draw("same")
    
       
    tex1 = ROOT.TLatex(0.65,0.7,"No binning")
#    tex1 = ROOT.TLatex(0.3,0.4,"No binning")
    tex1.SetNDC()
    tex1.SetTextSize(23)
    tex1.Draw()    
    marker1 = ROOT.TMarker(0.6,0.715,hmt.GetMarkerStyle())
#    marker1 = ROOT.TMarker(0.25,0.415,hmt.GetMarkerStyle())
    marker1.SetNDC()
    marker1.SetMarkerColor(hmt.GetMarkerColor())
    marker1.SetMarkerSize(0.9*hmt.GetMarkerSize())
    marker1.Draw()   
#    tex2 = ROOT.TLatex(0.3,0.3,"With p_{T}^{#tau jet} bins")
    tex2 = ROOT.TLatex(0.65,0.6,"With p_{T}^{#tau jet} bins") 
    tex2.SetNDC()
    tex2.SetTextSize(23)
    tex2.Draw()    
#    marker2 = ROOT.TMarker(0.25,0.32,hmtSum.GetMarkerStyle())
    marker2 = ROOT.TMarker(0.6,0.615,hmtSum.GetMarkerStyle())
    marker2.SetNDC()
    marker2.SetMarkerColor(hmtSum.GetMarkerColor())
    marker2.SetMarkerSize(0.9*hmtSum.GetMarkerSize())
    marker2.Draw()
    
    tex3 = ROOT.TLatex(0.5,0.85,"With inverted #tau isolation")
    tex3.SetNDC()
    tex3.SetTextSize(20)
    tex3.Draw()

    tex5 = ROOT.TLatex(0.5,0.8,"MET > 70 GeV")
    tex5.SetNDC()
    tex5.SetTextSize(20)
#    tex5.Draw()

    if(deltaPhi160):
        tex5 = ROOT.TLatex(0.5,0.8,"#Delta#phi(#tau jet, MET) < 160^{o}")
        tex5.SetNDC()
        tex5.SetTextSize(20)
        tex5.Draw()
    if(deltaPhi130):
        tex5 = ROOT.TLatex(0.5,0.8,"#Delta#phi(#tau jet, MET) < 130^{o}")
        tex5.SetNDC()
        tex5.SetTextSize(20)
        tex5.Draw()
        
    tex4 = ROOT.TLatex(0.2,0.95,"7 TeV       2.18 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    
    hmt.GetYaxis().SetTitle("Events / 10 GeV/c^{2}")
#    hmt.GetYaxis().SetTitleSize(20.0)
    hmt.GetYaxis().SetTitleOffset(1.5)
    hmt.GetXaxis().SetTitle("m_{T}(#tau jet, MET) (GeV/c^{2})")
#    canvas3.Print("mtInverted.png")
#    canvas3.Print("mtInverted.C")    
#    canvas3.Print("mtInverted_Met70_log.png")
#    canvas3.Print("mtInverted_Met70_log.C")
    if(btagging):
        if(deltaPhi180):  
            canvas3.Print("mtInverted_btag.png")
            canvas3.Print("mtInverted_btag.C")
        if(deltaPhi160):
            canvas3.Print("mtInverted_btag_dphi160.png")
            canvas3.Print("mtInverted_btag_dphi160.C")
        if(deltaPhi130):
            canvas3.Print("mtInverted_btag_dphi130.png")
            canvas3.Print("mtInverted_btag_dphi130.C")   
    else:
        if(deltaPhi180): 
            canvas3.Print("mtInverted_3jets.png")
            canvas3.Print("mtInverted_3jets.C")
        if(deltaPhi160):
            canvas3.Print("mtInverted_3jets_dphi160.png")
            canvas3.Print("mtInverted_3jets_dphi160.C")  
        if(deltaPhi130):
            canvas3.Print("mtInverted_3jets_dphi130.png")
            canvas3.Print("mtInverted_3jets_dphi130.C")




    fOUT = ROOT.TFile.Open("transverseMassQCDInverted.root", "RECREATE")
    hmtSum.SetDirectory(fOUT)
    fOUT.Write()
    fOUT.Close()

            
##  write histograms to file
def writeTransverseMass(datasets_lands):
    f = ROOT.TFile.Open(output, "RECREATE")
    hmtSum.SetDirectory(f)
    f.Write()
    f.Close()







    
def metComparison(datasets):
    met = plots.PlotBase([
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets4050"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets5060"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets6070"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets7080"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets80100"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets100120"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets120150"),
        datasets.getDataset("Data").getDatasetRootHisto(analysis+"/MET_InvertedTauIdJets150")
        ])
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    met._setLegendStyles()
    met._setLegendLabels()
    met.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(met, "met_vs_pttau", rebin=10)
          
       
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

def vertexCount(h, prefix="", postfix="", ratio=True):
        xlabel = "Number of good vertices"
        ylabel = "Number of events"

        if h.normalizeToOne:
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

        opts2 = {"ymin": 0.5, "ymax": 3}
        opts2_log = {"ymin": 5e-2, "ymax": 5e2}
        
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
        h.getPad2().SetLogy(True)
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
        kwargs = {"ymin": 0.1, "xmax": 300}
        
    kwargs = {"ymin": 0.1, "xmax": 300}
#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
    name = name+"_log"

    h.createFrame(name, **kwargs)
    h.getPad().SetLogy(True)
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
#    h.addMCUncertainty()
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
#    h.addMCUncertainty()
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
#    h.addMCUncertainty()
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
    
def transverseMass2(h,name, rebin=10, ratio=False):
#    name = flipName(h.getRootHistoPath())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(#tau jet, MET) (GeV/c^{2})" 
    ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    
    scaleMCfromWmunu(h)    
    #h.stackMCSignalHistograms()
    h.stackMCHistograms(stackSignal=False)#stackSignal=True)
    h.addMCUncertainty()
    
#    name = name+"_log"
    opts = {"ymin": 0.001, "ymaxfactor": 2.0,"xmax": 350 }
#    opts = {"xmax": 200 }
    opts2 = {"ymin": 0, "ymax": 3}
    h.createFrame(name, opts=opts, createRatio=ratio, opts2=opts2)
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
    h.setLegend(histograms.createLegend(0.7, 0.6, 0.9, 0.9))
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
