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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

# Configuration
analysis = "test"
#analysis = "signalAnalysis"
#analysis = "signalOptimisation"TauID_Rtau.png

treeDraw = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale")

#QCDfromData = True
QCDfromData = False

#mcOnly = False
mcOnly = True
mcOnlyLumi = 19638 # pb

searchMode = ""
#searchMode = "Heavy"

#dataEra = "Run2012AB"
dataEra = ""

#optMode = "OptQCDTailKillerZeroPlus"
optMode = ""


# main function
def main():
    # Read the datasets

    datasets = dataset.getDatasetsFromMulticrabCfg(analysisName=analysis)
    #datasets = dataset.getDatasetsFromMulticrabCfg(analysisName=analysis, searchMode=searchMode, dataEra=dataEra, optimizationMode=optMode)
    print "Dataset name",datasets.getDataDatasetNames()
    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
        histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    else:
        datasets.loadLuminosities()


    datasets.updateNAllEventsToPUWeighted()


    plots.mergeRenameReorderForDataMC(datasets)

    if mcOnly:
        print "Int.Lumi (manually set)",mcOnlyLumi
    else:
        print "Int.Lumi",datasets.getDataset("Data").getLuminosity()

#    print "norm=",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()

    datasets.getDataset("HplusToTBbar_M180").setCrossSection(0.392244*2*0.03936) # pb                                           
#    datasets.getDataset("HplusToTBbar_M190").setCrossSection(0.350458*2*0.19494) # pb                                               datasets.getDataset("HplusToTBbar_M200").setCrossSection(0.313866*2*0.344933 ) # pb                                              datasets.getDataset("HplusToTBbar_M220").setCrossSection(0.253265*2*0.54397)                                                     datasets.getDataset("HplusToTBbar_M250").setCrossSection(0.185948*2*0.671231) # pb                                    
    datasets.getDataset("HplusToTBbar_M300").setCrossSection(0.114095*2*0.748078) # pb 

    
    # Remove signals other than M120
    datasets.remove(filter(lambda name: "W2Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W3Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "W4Jets" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "QCD_Pt20_MuEnriched" in name, datasets.getAllDatasetNames()))
    

      
    datasets.remove(filter(lambda name: "HplusToTBbar" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "HplusToTBbar" in name and not "M180" in name, datasets.getAllDatasetNames()))

#    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))

    datasets.remove(filter(lambda name: "HplusTB" in name and not "M600" in name, datasets.getAllDatasetNames()))
    
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
#    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    
#    datasets.merge("TTToHplus", ["TTToHplus", "Hplus_taunu_s-channel", "Hplus_taunu_t-channe", "Hplus_taunu_tW-channel"], keepSources=True)


#################################################3
#    datasets.remove(filter(lambda name: "TTJets" in name, datasets.getAllDatasetNames()))
#    datasets.merge("TTJets2", ["TTJets_FullLept", "TTJets_Hadronic", "TTJets_SemiLept"], keepSources=True)
###################################################

    datasets.remove(filter(lambda name: "Hplus_taunu_s-channel" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name and not "M120" in name, datasets.getAllDatasetNames()))

        
    # Remove QCD
    datasets.remove(filter(lambda name: "QCD" in name, datasets.getAllDatasetNames()))
    histograms.createLegend.moveDefaults(dx=-0.02)
    histograms.createLegend.moveDefaults(dh=-0.03)
    
#    datasets_lands = datasets.deepCopy()

    # Set the signal cross sections to the ttbar for datasets for lands

#    xsect.setHplusCrossSectionsToTop(datasets_lands)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.01, br_Htaunu=1)
#    xsect.setHplusCrossSectionsToBR(datasets, br_tH=1.0, br_Htaunu=1)
    addMassBRText.setBR(0.01)
    # Set the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)

    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    #datasets.merge("EWK", ["WJets", "DYJetsToLL", "SingleTop", "Diboson","TTJets"], keepSources=True)


    # Replace signal dataset with EWK+signal
    if False:
        ttjets2 = datasets.getDataset("TTJets").deepCopy()
        ttjets2.setName("TTJets2")
        ttjets2.setCrossSection(ttjets2.getCrossSection() - datasets.getDataset("TTToHplus_M120").getCrossSection())
        datasets.append(ttjets2)
        datasets.merge("EWKnoTT", ["WJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
        datasets.merge("TTToHplus_M120", ["TTToHplus_M120", "EWKnoTT", "TTJets2"])
        plots._legendLabels["TTToHplus_M120"] = "with H^{#pm}#rightarrow#tau^{#pm}#nu"
#        plots._legendLabels["TTToHplus_M120"] = "m_{H^{#pm}} = 120 GeV/c^{2}"
#        plots._legendLabels["TTToHplus_M80"] = "m_{H^{#pm}} = 80 GeV/c^{2}"
#        plots._legendLabels["TTToHplus_M160"] = "m_{H^{#pm}} = 160 GeV/c^{2}"
      
        
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create plots
    doPlots(datasets)

    # Print counters
    doCounters(datasets)
    
def doPlots(datasets):
    def createPlot(name, **kwargs):
        if mcOnly:
            # If 'normalizeToOne' is given in kwargs, we don't need the normalizeToLumi (or actually the library raises an Exception)
            args = {}
            args.update(kwargs)
            if not ("normalizeToOne" in args and args["normalizeToOne"]):
                args["normalizeToLumi"] = mcOnlyLumi
            return plots.MCPlot(datasets, name, **args)
        else:
            return plots.DataMCPlot(datasets, name, **kwargs)

    def pickSliceX(th2, ybinName):
        th1 = ROOT.TH1D(th2.GetName(), th2.GetTitle(), th2.GetNbinsX(), aux.th1Xmin(th2), aux.th1Xmax(th2))
        th1.Sumw2()
        ybin = None
        for bin in xrange(1, th2.GetNbinsY()+1):
            if th2.GetYaxis().GetBinLabel(bin) == ybinName:
                ybin = bin
                break
        if ybin is None:
            raise Exception("Did not find y bin label %s from histogram %s" % (ybinName, th2.GetName()))
        for xbin in xrange(0, th2.GetNbinsX()+2): # include under/overflow bins
            th1.SetBinContent(xbin, th2.GetBinContent(xbin, ybin))
            th1.SetBinError(xbin, th2.GetBinError(xbin, ybin))
        return th1

    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files
    
    # Primary vertices

#    vertexCount(createPlot("Vertices/verticesBeforeWeight", normalizeToOne=True), postfix="BeforeWeightTriggered")
#    vertexCount(createPlot("Vertices/verticesAfterWeight", normalizeToOne=True), postfix="AfterWeightTriggered")

#    vertexCount(createPlot("SignalSelectionFlowVsVertices", normalizeToOne=True, datasetRootHistoArgs={"modify": lambda th2: pickSliceX(th2, "#tau ID")}), postfix="AfterTauIDScaleFactors")

#    met2(createPlot("MET"), "met1", rebin=50)
  
    # Tau
    if True:
        tauPt(createPlot("TauPt"), "TauSelection_selected_taus_pt", rebin=1, ratio=False, opts={"xmax": 300, "ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.31, y=0.22))
        tauEta(createPlot("TauEta"),"TauSelection_selected_taus_eta", rebin=2, ratio=False, opts={"ymin": 1, "ymaxfactor": 50, "xmin": -2.5, "xmax": 2.5}, moveLegend={"dy":0.01, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.85))
 
#        drawPlot(createPlot("TauSelection/TauSelection_selected_taus_MC_purity"), "SelectedTausMCpurity",log=False,  xlabel="origin", ylabel="#tau jets", ratio=False, opts={"ymin": 10, "xmax": 6}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
#        drawPlot(createPlot("TauSelection/TauSelection_selected_taus_N"), "SelectedTaus", xlabel="", log=True,  ylabel="#tau jets", ratio=False, opts={ "xmax": 8}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
        
#    rtau(createPlot("TauSelection/TauID_RtauCut"), "TauID_Rtau", rebin=2, ratio=False, opts={"ymin": 1e-2, "ymaxfactor": 120, "xmax": 1.1}, moveLegend={"dx": -0.51,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
     
#    rtau(createPlot("tauID/TauID_RtauCut"), "TauID_Rtau", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)

    
    if False:
        rtau(createPlot("TauSelection/TauID_Rtau_DecayModeOneProng_ZeroPiZero"), "TauID_Rtau_DecayModeOneProng_ZeroPiZero", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
        rtau(createPlot("TauSelection/TauID_Rtau_DecayModeOneProng_OnePiZero"), "TauID_Rtau_DecayModeOneProng_OnePiZero", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
        rtau(createPlot("TauSelection/TauID_Rtau_DecayModeOneProng_TwoPiZero"), "TauID_Rtau_DecayModeOneProng_TwoPiZero", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)
        rtau(createPlot("TauSelection/TauID_Rtau_DecayModeOneProng_Other"), "TauID_Rtau_DecayModeOneProng_Other", rebin=2, opts={"ymin": 1e-2, "ymaxfactor": 15, "xmax": 1.1}, moveLegend={"dx": -0.5,"dy": 0.02}, textFunction=lambda: addMassBRText(x=0.31, y=0.22), cutLine=0.7)

    
#    selectionFlow(createPlot("SignalSelectionFlow"), "SignalSelectionFlow", rebin=1, ratio=False)
#    selectionFlowTauCand(createPlot("SignalSelectionFlow"), "SignalSelectionFlow", rebin=1, ratio=False)
#    selectionFlow(createPlot("SignalSelectionFlow"), "SignalSelectionFlow", rebin=1, opts={"ymin": 1, "ymaxfactor": 5} ) 
    

    # Electron veto
    if False:
        drawPlot(createPlot("electronPt"), "electronPt", rebin=2, xlabel="p_{T}^{electron} (GeV/c)", ylabel="Identified electrons / %.0f GeV/c", ratio=False,  opts={"xmax": 250,"xmin": 0, "ymaxfactor": 10}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=15)
        drawPlot(createPlot("ElectronSelection/ElectronEta_veto"), "electronEta", rebin=2, xlabel="#eta^{electron}", ylabel="Identified electrons / %.1f", ratio=False, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 20}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=[-2.5, 2.5])
        drawPlot(createPlot("ElectronSelection/NumberOfVetoElectrons"), "NumberOfVetoElectrons", xlabel="Number of selected veto electrons", ylabel="Events", ratio=False, opts={"xmax": 6,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=1)
    
    # Muon veto
        drawPlot(createPlot("muonPt"), "muonPt", rebin=2, xlabel="p_{T}^{muon} (GeV/c)", ylabel="Identified muons / %.0f GeV/c", ratio=False, log=True, opts={"ymaxfactor": 2,"xmax": 250,"xmin": 0}, textFunction=lambda: addMassBRText(x=0.35, y=0.9), cutLine=15)
#        drawPlot(createPlot("MuonSelection/LooseMuonEta"), "muonEta", rebin=2, xlabel="#eta^{muon}", ylabel="Identified muons / %.1f", ratio=False, opts={"xmin": -3,"ymin": 0.1, "xmax": 3, "ymaxfactor": 20}, moveLegend={"dy":0.01, "dx":-0.07, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.30, y=0.87), cutLine=[-2.5, 2.5])
#        drawPlot(createPlot("MuonSelection/NumberOfLooseMuons"), "NumberOfSelectedMuons", xlabel="Number of selected muons", ylabel="Events", ratio=False, opts={"xmax": 6,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=1)

    if False:
        # tau veto
        drawPlot(createPlot("TauVeto/TauSelection_selected_taus_pt"), "SelectedVetoTausPt", rebin=2, xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="#tau jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=15)
        drawPlot(createPlot("VetoTauSelection/SelectedFakeTauByPt"), "SelectedFakeVetoTauPt", rebin=2, xlabel="p_{T}^{#tau jet} (GeV/c)", ylabel="#tau jets / %.0f GeV/c", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=15)
        drawPlot(createPlot("VetoTauSelection/SelectedFakeTauByEta"), "SelectedFakeVetoTauEta", rebin=2, xlabel="#eta^{#tau jet}", ylabel="#tau jets / %.1f", opts={"ymaxfactor": 110}, moveLegend={"dy":0.01, "dx":-0.2, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.22), cutLine=[-2.4, 2.4])     

        
    # Jet selection
    drawPlot(createPlot("jetPt"), "jetPt", rebin=2, xlabel="p_{T}^{jet} (GeV/c)", ylabel="Jets / %.0f GeV/c", ratio=False, opts={"xmax": 400,"ymin": 0.01,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.3, y=0.87), cutLine=30)
#    drawPlot(createPlot("JetSelection/jet_eta"), "jetEta", rebin=2, xlabel="#eta^{jet}", ylabel="Jets / %.1f", ratio=False, opts={"xmin": -3.5, "xmax": 3.5, "ymaxfactor": 500}, moveLegend={"dy":0.01, "dx":-0.2, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.22), cutLine=[-2.4, 2.4])
#    drawPlot(createPlot("JetSelection/jet_phi"), "jetPhi", rebin=1, xlabel="#phi^{jet}", ylabel="Jets / %.2f", opts={"ymin": 20},textFunction=lambda: addMassBRText(x=0.3, y=0.87))
#    drawPlot(createPlot("JetSelection/NumberOfSelectedJets"), "NumberOfSelectedJets", xlabel="Number of selected jets", ylabel="Events", ratio=False, opts={"xmax": 11,"ymaxfactor": 2}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=3)
    
    # MET
#    drawPlot(createPlot("Met"), "Met", rebin=5, xlabel="PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", ratio=False, opts={"xmin": 0}, textFunction=lambda: addMassBRText(x=0.4, y=0.9), cutLine=60)
    drawPlot(createPlot("MetJetInHole"), "MetJetInHol", rebin=4, xlabel="PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", ratio=True, opts={"xmin": 0, "xmax": 500}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=60)
    drawPlot(createPlot("MetNoJetInHole"), "MetNoJetInHol", rebin=4, xlabel="PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", ratio=True, opts={"xmin": 0, "xmax": 500}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=60)


    # b jets
#    drawPlot(createPlot("Btagging/bjet_pt"), "bjetPt", rebin=3, xlabel="p_{T}^{b-tagged jet} (GeV/c)", ylabel="b-tagged jets / %.0f GeV/c", ratio=False, opts={"ymaxfactor": 2,"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
#    drawPlot(createPlot("Btagging/bjet_eta"), "bjetEta", rebin=2, xlabel="#eta^{b-tagged jet}", ylabel="b-tagged jets / %.1f", ratio=False, opts={"ymaxfactor": 20, "xmin": -2.4, "xmax": 2.4,"ymin": 0.01 }, moveLegend={"dy":0.01, "dh":-0.06}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
#    drawPlot(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBTaggedJets", xlabel="Number of selected b jets", ylabel="Events", opts={"xmax": 7}, ratio=False, textFunction=lambda: addMassBRText(x=0.45, y=0.87), cutLine=1)

#   

    if False:
        # top mass 
        drawPlot(createPlot("TopChiSelection/TopMass"), "TopMassWithChi", rebin=2, log=False, xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=300)

        drawPlot(createPlot("FullHiggsMass/TopMassSolution"), "TopMassWithHiggsMass", rebin=2, log=False, xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=300)

        drawPlot(createPlot("TopChiSelection/WMass"), "WMassWithChi", rebin=2, log=False, xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=50)
        drawPlot(createPlot("TopWithBSelection/TopMass"), "TopMassWithBsel", rebin=2, log=False,xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87), cutLine=250)
        drawPlot(createPlot("TopWithBSelection/WMass"), "WMassWithBsel", rebin=20, log=False,xlabel="m_{top} (GeV/c^{2})", ylabel="Events / %.0f GeV", opts={"xmax": 400}, textFunction=lambda: addMassBRText(x=0.4, y=0.87))
    
    
    if False:
      transverseMass2(createPlot("MCAnalysisOfSelectedEvents/transverseMassMuomFromW"), "transverseMassMuonFromW", rebin=3, ratio=False,log=False, opts={"xmax": 300,"ymaxfactor": 1.2}, textFunction=lambda: addMassBRText(x=0.2, y=0.87))

    transverseMass2(createPlot("shapeTransverseMass"), "shapeTransverseMass", rebin=3, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))
    transverseMass2(createPlot("shapeEWKFakeTausTransverseMass"), "shapeEWKFakeTausTransverseMass", rebin=5, ratio=False,log=False, opts={"xmax": 400,"ymaxfactor": 1.1}, textFunction=lambda: addMassBRText(x=0.35, y=0.87))

    
    if QCDfromData:
        plot = replaceQCDfromData(createPlot("transverseMass"), datasetsQCD, analysis+"/MTInvertedTauIdBtag")
        transverseMass2(plot, "transverseMass", rebin=20)


    # Delta phi
#    deltaPhi2(createPlot("deltaPhi"), "DeltaPhiTauMet", rebin=10, ratio=False, opts={"ymaxfactor": 50}, moveLegend={"dx":-0.21}, textFunction=lambda: addMassBRText(x=0.2, y=0.87), cutLine=[160])


    # Tailkiller cuts
#    drawPlot(createPlot("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"), "BackToBackJet1",  rebin=2, xlabel="(180^{o}-#Delta#phi(jet_{1},MET))^{2}}+ #sqrt{#Delta#phi(#tau,MET)^{2}", ylabel="Events", opts={"xmax": 270}, log=True, ratio=False, moveLegend={"dx":-0.4})
#    drawPlot(createPlot("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1Collinear"), "CollinearJet1", rebin=2, xlabel="#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{2}}", ylabel="Events", opts={"xmax": 270}, log=True, ratio=False)
    

    # Set temporarily the signal cross sections to a value from MSSM
#    xsect.setHplusCrossSections(datasets, tanbeta=20, mu=200)
#    datasets.getDataset("TTToHplusBHminusB_M120").setCrossSection(0.2*165)
#    datasets.getDataset("TTToHplusBWB_M120").setCrossSection(0.2*165)


#    path = "transverseMassWithRtauFakeMet"
#    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMassWithRtauFakeMet", rebin=20)
#    plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
#    transverseMass2(plot, "transverseMassWithRtauFakeMetQCDFromData", rebin=20)
    
#    path = "transverseMassDeltaPhiUpperCut"
#    transverseMass2(plots.DataMCPlot(datasets, path), "transverseMassDeltaPhiUpperCut", rebin=20)
#    plot = replaceQCDfromData(plots.DataMCPlot(datasets, path), datasetsQCD, path)
#    transverseMass2(plot, "transverseMassDeltaPhiUpperCutQCDFromData", rebin=20)


#    pasJuly = "met_p4.Et() > 70 && Max$(jets_btag) > 1.7"
#    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
#    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt+">>dist(40,0,400)", selection=pasJuly)), "transverseMass_metRaw", rebin=1)
#    transverseMass2(plots.DataMCPlot(datasets, treeDraw.clone(varexp=mt.replace("met", "metType1")+">>dist(40,0,400)", selection=pasJuly.replace("met", "metType1"))), "transverseMass_metType1", rebin=1)


#    mtContentComparison(datasets)
#    genComparison(datasets)
#    zMassComparison(datasets)
#    genQuarkComparison(datasets)
#    topMassComparison(datasets)
#    deltaPhiCorrelation(datasets)
#    deltaRComparison(datasets)
#    CollinearComparison(datasets)
#    BackToBackComparison(datasets)
#    topMassPurity(datasets) 
#    vertexComparison(datasets)
##    mtComparison(datasets)
#    MetComparison(datasets)
#    BetaComparison(datasets)
#    HiggsMassComparison(datasets)
#    InvMassComparison(datasets)
#    rtauComparison(datasets)
    

def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)

    # append row from the tree to the main counter
#    eventCounter.getMainCounter().appendRow("MET > 70", treeDraw.clone(selection="met_p4.Et() > 70"))

    ewkDatasets = [
        "WJets", "TTJets",
#        "WJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]

    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcOnlyLumi)
    else:
        eventCounter.normalizeMCByLuminosity()
    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
    # Default
#    cellFormat = counter.TableFormatText()
    # No uncertainties
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=False))
    print mainTable.format(cellFormat)



    print eventCounter.getSubCounterTable("MCinfo for selected events").format(cellFormat)

#    print eventCounter.getSubCounterTable("tauSelection").format()
#    print eventCounter.getSubCounterTable("TauIDPassedEvt::TauSelection_HPS").format(cellFormat)
#    print eventCounter.getSubCounterTable("TauIDPassedJets::TauSelection_HPS").format(cellFormat)
#    print eventCounter.getSubCounterTable("b-tagging").format(cellFormat)
#    print eventCounter.getSubCounterTable("Jet selection").format(cellFormat)
#    print eventCounter.getSubCounterTable("Jet main").format(cellFormat)    
#    print eventCounter.getSubCounterTable("VetoTauSelection").format(cellFormat)
#    print eventCounter.getSubCounterTable("MuonSelection").format(cellFormat)
#    print eventCounter.getSubCounterTable("MCinfo for selected events").format(cellFormat) 
#    print eventCounter.getSubCounterTable("ElectronSelection").format(cellFormat)  
#    print eventCounter.getSubCounterTable("top").format(cellFormat) 

    
#    latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f"))
#    print eventCounter.getMainCounterTable().format(latexFormat)

def vertexComparison(datasets):
    signal = "TTToHplusBWB_M120"
    background = "TTToHplusBWB_M120"
    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto("verticesBeforeWeight"),
                                 datasets.getDataset(background).getDatasetRootHisto("verticesAfterWeight")),
            "vertices_H120")

            
def deltaPhiCorrelation(datasets):

#    deltaPhiVsJet1 = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet1")])
#    deltaPhiVsJet1 = plots.PlotBase([datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet1")])
    deltaPhiVsJet1 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet1")])
    deltaPhiVsJet1.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity()) 
    deltaPhiVsJet1._setLegendStyles()
    deltaPhiVsJet1._setLegendLabels()
    deltaPhiVsJet1.histoMgr.setHistoDrawStyleAll("P")
    deltaPhiVsJet1.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
#    hdeltaPhiVsJet1 = deltaPhiVsJet1.histoMgr.getHisto("TTToHplus_M120").getRootHisto().Clone()
#    hdeltaPhiVsJet1 = deltaPhiVsJet1.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone()
    hdeltaPhiVsJet1 = deltaPhiVsJet1.histoMgr.getHisto("TTJets").getRootHisto().Clone()
    
    canvas55 = ROOT.TCanvas("canvas55","",500,500)
    
    hdeltaPhiVsJet1.RebinX(5)
    hdeltaPhiVsJet1.RebinY(5)
    hdeltaPhiVsJet1.SetMarkerColor(4)
    hdeltaPhiVsJet1.SetMarkerSize(1)
    hdeltaPhiVsJet1.SetMarkerStyle(20)
    hdeltaPhiVsJet1.SetFillColor(4)
    hdeltaPhiVsJet1.Draw("colz")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
#    tex1 = ROOT.TLatex(0.55,0.88,"Signal, m_{H#pm} = 120 GeV")
    tex1 = ROOT.TLatex(0.55,0.88,"ttbar + jets")
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw()    
    hdeltaPhiVsJet1.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
    hdeltaPhiVsJet1.GetYaxis().SetTitle("#Delta#phi(MET,jet1) (deg) ")
    canvas55.Print("DeltaPhiVsDeltaPhiMETjet1_tt.png")
    canvas55.Print("DeltaPhiVsDeltaPhiMETjet1_tt.C")
                                                                                            

#    deltaPhiVsJet2 = plots.PlotBase([datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet2")])
#    deltaPhiVsJet2 = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet2")])
    deltaPhiVsJet2 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet2")])
    deltaPhiVsJet2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        
    deltaPhiVsJet2._setLegendStyles()
    deltaPhiVsJet2._setLegendLabels()
    deltaPhiVsJet2.histoMgr.setHistoDrawStyleAll("P")
    deltaPhiVsJet2.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
   # deltaPhiVsJet2.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    hdeltaPhiVsJet2 = deltaPhiVsJet2.histoMgr.getHisto("TTToHplus_M120").getRootHisto().Clone()
#    hdeltaPhiVsJet2 = deltaPhiVsJet2.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone()
    hdeltaPhiVsJet2 = deltaPhiVsJet2.histoMgr.getHisto("TTJets").getRootHisto().Clone()
    canvas56 = ROOT.TCanvas("canvas56","",500,500)
    
    hdeltaPhiVsJet2.RebinX(5)
    hdeltaPhiVsJet2.RebinY(5)
    hdeltaPhiVsJet2.SetMarkerColor(4)
    hdeltaPhiVsJet2.SetMarkerSize(1)
    hdeltaPhiVsJet2.SetMarkerStyle(20)
    hdeltaPhiVsJet2.SetFillColor(4)
    hdeltaPhiVsJet2.Draw("colz")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
#    tex1 = ROOT.TLatex(0.55,0.88,"Signal, m_{H#pm} = 120 GeV")
    tex1 = ROOT.TLatex(0.55,0.88,"ttbar + jets")
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw()
        
    hdeltaPhiVsJet2.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
    hdeltaPhiVsJet2.GetYaxis().SetTitle("#Delta#phi(MET,jet2) (deg) ")
    canvas56.Print("DeltaPhiVsDeltaPhiMETjet2_tt.png")
    canvas56.Print("DeltaPhiVsDeltaPhiMETjet2_tt.C")

#    deltaPhiVsJet3 = plots.PlotBase([datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet3")])    
#    deltaPhiVsJet3 = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet3")])
    deltaPhiVsJet3 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet3")]) 
    deltaPhiVsJet3.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    deltaPhiVsJet3._setLegendStyles()
    deltaPhiVsJet3._setLegendLabels()
    deltaPhiVsJet3.histoMgr.setHistoDrawStyleAll("P")
    deltaPhiVsJet3.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2))
    
#    hdeltaPhiVsJet3 = deltaPhiVsJet3.histoMgr.getHisto("TTToHplus_M120").getRootHisto().Clone()
#    hdeltaPhiVsJet3 = deltaPhiVsJet3.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone()
    hdeltaPhiVsJet3 = deltaPhiVsJet3.histoMgr.getHisto("TTJets").getRootHisto().Clone()
    canvas57 = ROOT.TCanvas("canvas57","",500,500)
    
    hdeltaPhiVsJet3.RebinX(5)
    hdeltaPhiVsJet3.RebinY(5)
    hdeltaPhiVsJet3.SetMarkerColor(4)
    hdeltaPhiVsJet3.SetMarkerSize(1)
    hdeltaPhiVsJet3.SetMarkerStyle(20)
    hdeltaPhiVsJet3.SetFillColor(4)
    hdeltaPhiVsJet3.Draw("colz")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
#    tex1 = ROOT.TLatex(0.55,0.88,"Signal, m_{H#pm} = 120 GeV")
    tex1 = ROOT.TLatex(0.55,0.88,"ttbar + jets")
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw()
    hdeltaPhiVsJet3.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
    hdeltaPhiVsJet3.GetYaxis().SetTitle("#Delta#phi(MET,jet3) (deg) ")
    canvas57.Print("DeltaPhiVsDeltaPhiMETjet3_tt.png")
    canvas57.Print("DeltaPhiVsDeltaPhiMETjet3_tt.C")


    deltaPhiVsJet4 = plots.PlotBase([datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet4")])
#    deltaPhiVsJet4  = plots.PlotBase([datasets.getDataset("HplusTB_M200").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet4")]) 
#    deltaPhiVsJet4 = plots.PlotBase([datasets.getDataset("TTJets").getDatasetRootHisto("DeltaPhiVsDeltaPhiMETJet4")]) 
    deltaPhiVsJet4.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    deltaPhiVsJet4._setLegendStyles()
    deltaPhiVsJet4._setLegendLabels()

    deltaPhiVsJet4.histoMgr.setHistoDrawStyleAll("P")
    deltaPhiVsJet4.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(2)) 
    hdeltaPhiVsJet4 = deltaPhiVsJet4.histoMgr.getHisto("TTToHplus_M120").getRootHisto().Clone()
#    hdeltaPhiVsJet4 = deltaPhiVsJet4.histoMgr.getHisto("HplusTB_M200").getRootHisto().Clone()
#    hdeltaPhiVsJet4 = deltaPhiVsJet4.histoMgr.getHisto("TTJets").getRootHisto().Clone()
    canvas58 = ROOT.TCanvas("canvas58","",500,500)
#    hdeltaPhiVsJet4.setDefaultStyles()
    hdeltaPhiVsJet4.RebinX(5)
    hdeltaPhiVsJet4.RebinY(5)
    hdeltaPhiVsJet4.SetMarkerColor(4)
    hdeltaPhiVsJet4.SetMarkerSize(1)
    hdeltaPhiVsJet4.SetMarkerStyle(20)
    hdeltaPhiVsJet4.SetFillColor(4)
    hdeltaPhiVsJet4.Draw("colz")
    tex4 = ROOT.TLatex(0.2,0.95,"8 TeV       12 fb^{-1}       CMS Preliminary ")
    tex4.SetNDC()
    tex4.SetTextSize(20)
    tex4.Draw()
    tex1 = ROOT.TLatex(0.55,0.88,"Signal, m_{H#pm} = 120 GeV")
#    tex1 = ROOT.TLatex(0.55,0.88,"ttbar + jets")
    tex1.SetNDC()
    tex1.SetTextSize(15)
    tex1.Draw()
    hdeltaPhiVsJet4.GetXaxis().SetTitle("#Delta#phi(#tau jet,MET) (deg)")
    hdeltaPhiVsJet4.GetYaxis().SetTitle("#Delta#phi(MET,jet4) (deg) ")
    canvas58.Print("DeltaPhiVsDeltaPhiMETjet4_m120.png")
    canvas58.Print("DeltaPhiVsDeltaPhiMETjet4_m200.C")



 

def deltaRComparison(datasets):
    massPoints = [
        "TTToHplus_M80",
        "TTToHplus_M120",
        "TTToHplus_M160",
        #"HplusTB_M180",
        #"HplusTB_M200",
        #"HplusTB_M300"
        ]
    
#    mt = plots.PlotBase([datasets.getDataset(m).getDatasetRootHisto("transverseMass") for m in massPoints])
    mt = plots.PlotBase([datasets.getDataset(m).getDatasetRootHisto("DeltaR_TauMETJet4MET") for m in massPoints])
    mt.setEnergy(datasets.getEnergies())

def mtComparison(datasets):
    mt = plots.PlotBase([
#        datasets.getDataset("HplusTB_M180").getDatasetRootHisto("shapeTransverseMass"),
#        datasets.getDataset("HplusToTBbar_M180").getDatasetRootHisto("shapeTransverseMass"),

        datasets.getDataset("HplusTB_M180").getDatasetRootHisto("shapeTransverseMass"),
#        datasets.getDataset("HplusTB_M190").getDatasetRootHisto("transverseMass"),
        datasets.getDataset("HplusTB_M200").getDatasetRootHisto("shapeTransverseMass"),
#        datasets.getDataset("HplusTB_M250").getDatasetRootHisto("transverseMass"),
        datasets.getDataset("HplusTB_M300").getDatasetRootHisto("shapeTransverseMass"),
#        datasets.getDataset("TTToHplus_M90").getDatasetRootHisto("shapeTransverseMass"),
#        datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("shapeTransverseMass"),
#        datasets.getDataset("TTToHplus_M150").getDatasetRootHisto("shapeTransverseMass"),
#        datasets.getDataset("TTToHplusBWB_M160").getDatasetRootHisto("transverseMass"),
        ############ 
#        datasets.getDataset("QCD").getDatasetRootHisto("transverseMassNoBtagging"),
#        datasets.getDataset("QCD").getDatasetRootHisto("transverseMassNoBtaggingWithRtau"),        
        ])
    
    #   plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section MUST BE OFF
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mt.histoMgr.normalizeMCToOne(datasets.getDataset("Data").getLuminosity())    
    mt._setLegendStyles()
    mt._setLegendLabels()
#
#    st = [
#        styles.StyleCompound([styles.styles[3]]),
#        styles.StyleCompound([styles.styles[2]]),
#        styles.StyleCompound([styles.styles[1]]),
#        styles.StyleCompound([styles.styles[0]]),
#        ]
#    st[0].append(styles.StyleLine(lineWidth=3))
#    st[1].append(styles.StyleLine(lineStyle=2, lineWidth=3))
#    st[2].append(styles.StyleLine(lineStyle=3, lineWidth=3))
#    st[3].append(styles.StyleLine(lineStyle=4, lineWidth=3))
#
#    if len(massPoints) > len(st):
#        raise Exception("So far supporting max %d mass points" % len(st))
#
#    for i, histoName in enumerate(massPoints):
#        mt.histoMgr.forHisto(histoName, st[i])
#
##    mt.histoMgr.setHistoDrawStyleAll("P")
##    rtauGen(mt, "transverseMass_vs_mH", rebin=20, defaultStyles=False)
#    rtauGen(mt, "DeltaR_TauMETJet4MET_signalLight", rebin=5, defaultStyles=False)
##    rtauGen(mt, "transverseRtau", rebin=5, ratio=True, defaultStyles=False)
#
#
#def mtComparison(datasets):
#    massPoints = [
#        "TTToHplus_M80",
#        "TTToHplus_M120",
#        "TTToHplus_M160",
#        #"HplusTB_M180",
#        #"HplusTB_M200",
#        #"HplusTB_M250",
#        #"HplusTB_M300",
#        ]
#    
##    mt = plots.PlotBase([datasets.getDataset(m).getDatasetRootHisto("transverseMass") for m in massPoints])
##    mt = plots.PlotBase([datasets.getDataset(m).getDatasetRootHisto("transverseMassAfterBtagging") for m in massPoints])
#    mt = plots.PlotBase([datasets.getDataset(m).getDatasetRootHisto("transverseMassDeltaPhiJet4") for m in massPoints]) 
##    mt = plots.PlotBase([datasets.getDataset(m).getDatasetRootHisto("transverseMassAgainstTTCut") for m in massPoints])
##    mt.setEnergy(datasets.getEnergies())
#    
#    #   plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section MUST BE OFF
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
##    mt.histoMgr.normalizeMCToOne(datasets.getDataset("Data").getLuminosity())    
#    mt._setLegendStyles()
#    mt._setLegendLabels()
#    st = [
#        styles.StyleCompound([styles.styles[3]]),
#        styles.StyleCompound([styles.styles[2]]),
#        styles.StyleCompound([styles.styles[1]]),
#        styles.StyleCompound([styles.styles[0]]),
#        ]
#    st[0].append(styles.StyleLine(lineWidth=3))
#    st[1].append(styles.StyleLine(lineStyle=2, lineWidth=3))
#    st[2].append(styles.StyleLine(lineStyle=3, lineWidth=3))
#    st[3].append(styles.StyleLine(lineStyle=4, lineWidth=3))
#
#    if len(massPoints) > len(st):
#        raise Exception("So far supporting max %d mass points" % len(st))
#
#    for i, histoName in enumerate(massPoints):
#        mt.histoMgr.forHisto(histoName, st[i])
#


    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
#    mt.histoMgr.forHisto("HplusTB_M180", st1)
#    mt.histoMgr.forHisto("HplusToTBbar_M180", st2)
    mt.histoMgr.forHisto("HplusTB_M180", st1)
    mt.histoMgr.forHisto("HplusTB_M200", st2)
    mt.histoMgr.forHisto("HplusTB_M300", st3)

#    mt.histoMgr.forHisto("TTToHplus_M90", st1)
#    mt.histoMgr.forHisto("TTToHplus_M120", st2)
#    mt.histoMgr.forHisto("TTToHplus_M150", st3)
                
#    mt.histoMgr.setHistoDrawStyleAll("P")
#    rtauGen(mt, "transverseMass_vs_mH", rebin=20, defaultStyles=False)
    #rtauGen(mt, "transverseMassTauVeto", rebin=5, defaultStyles=False)
    rtauGen(mt, "transverseMassComparison", rebin=1, ratio=True, defaultStyles=False)

def mtContentComparison(datasets):

    def createHisto(path, name):
        drh = datasets.getDataset("TTJets").getDatasetRootHisto(path)
        drh.setName(name)
        return drh
    
    mt = plots.PlotBase([
        createHisto("shapeTransverseMass", "Selected tt+jet events"),
        createHisto("MCAnalysisOfSelectedEvents/transverseMassNoLeptonNotInTau", "No associated e, #mu, #tau jet"),
       # createHisto("MCAnalysisOfSelectedEvents/transverseMassLeptonNotInTau", "With associated e, #mu, #tau jet")])
        #createHisto("MCAnalysisOfSelectedEvents/transverseMassNoElMuNotInTau", "No associated electrons or muons"),
        #createHisto("MCAnalysisOfSelectedEvents/transverseMassNoElMuRealSignalTau", "No associated e or #mu , real signal #tau")]) 
        createHisto("MCAnalysisOfSelectedEvents/transverseMassNoLeptonRealSignalTau", "No associated e, #mu, #tau jet, real signal #tau")]) 
        #createHisto("MCAnalysisOfSelectedEvents/transverseMassElMuNotInTau", "With associated electrons and muons")])  
        #createHisto("MCAnalysisOfSelectedEvents/transverseMassElectronNotInTau", "Events with associated electron"),
        #createHisto("MCAnalysisOfSelectedEvents/transverseMassElectronFromW", "Events with W->e#nu"),
        #createHisto("MCAnalysisOfSelectedEvents/transverseMassElectronFromBottom", "Events with b->e+X")]) 

    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mt.histoMgr.normalizeMCToOne(datasets.getDataset("Data").getLuminosity())    
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=4))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=4))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=4))
    #mt.histoMgr.forHisto(datasets.getDataset("TTJets").getDatasetRootHisto("shapeTransverseMass"), st1)
    #mt.histoMgr.forHisto(datasets.getDataset("TTJets").getDatasetRootHisto("transverseMassNoLeptonNotInTau"), st2)
    #mt.histoMgr.forHisto(datasets.getDataset("TTJets").getDatasetRootHisto("transverseMassLeptonNotInTau"), st3)
    mt.histoMgr.forHisto("Selected tt+jet events", st3)
   # mt.histoMgr.forHisto("No associated electrons or muons", st1)
   # mt.histoMgr.forHisto("With associated electrons and muons", st2)
    mt.histoMgr.forHisto("No associated e, #mu, #tau jet, real signal #tau", st2)
    mt.histoMgr.forHisto("No associated e, #mu, #tau jet", st1)
   # mt.histoMgr.forHisto("With associated e, #mu, #tau jet", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "NoLeptonsRealTau_withTau", rebin=2, ratio=False, defaultStyles=False)
    #rtauGen(mt, "LeptonsInMt_TTJets_withTau", rebin=2, ratio=False, defaultStyles=False)
    
def CollinearComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("HplusTB_M180").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1Collinear"),
#        datasets.getDataset("HplusTB_M190").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet2Collinear"),
        datasets.getDataset("HplusTB_M200").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1Collinear"),
#        datasets.getDataset("HplusTB_M250").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet2Collinear"),
        datasets.getDataset("HplusTB_M300").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1Collinear"),
#        datasets.getDataset("TTToHplus_M90").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet3Collinear"),
#        datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet3Collinear"),
#        datasets.getDataset("TTToHplus_M160").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet3Collinear"),
        #datasets.getDataset("QCD").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1Collinear"),
        #datasets.getDataset("TTJets").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1Collinear"),    
        ])
    
    #   plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section MUST BE OFF
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mt.histoMgr.normalizeMCToOne(datasets.getDataset("Data").getLuminosity())    
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("HplusTB_M180", st1)
    mt.histoMgr.forHisto("HplusTB_M200", st2)
    mt.histoMgr.forHisto("HplusTB_M300", st3)
    #mt.histoMgr.forHisto("TTToHplus_M90", st1)
    #mt.histoMgr.forHisto("TTToHplus_M120", st2)
    #mt.histoMgr.forHisto("TTToHplus_M160", st3)
   # mt.histoMgr.forHisto("QCD", st1)
        #    mt.histoMgr.setHistoDrawStyleAll("P")
#    rtauGen(mt, "transverseMass_vs_mH", rebin=20, defaultStyles=False)
    #rtauGen(mt, "transverseMassTauVeto", rebin=5, defaultStyles=False)
    rtauGen(mt, "CollinearTailKillerComparisonJet1_heavyHplus", rebin=2, ratio=False, defaultStyles=False)
    
def BackToBackComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("HplusTB_M180").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"),
#        datasets.getDataset("HplusTB_M190").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"),
        datasets.getDataset("HplusTB_M200").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"),
#        datasets.getDataset("HplusTB_M250").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"),
        datasets.getDataset("HplusTB_M300").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"),
#        datasets.getDataset("TTToHplus_M90").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet3BackToBack"),
#        datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet3BackToBack"),
#        datasets.getDataset("TTToHplus_M160").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet3BackToBack"),
        #datasets.getDataset("QCD").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"),
        #datasets.getDataset("TTJets").getDatasetRootHisto("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsJet1BackToBack"), 
        ])
    
    #   plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section MUST BE OFF
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    mt.histoMgr.normalizeMCToOne(datasets.getDataset("Data").getLuminosity())    
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("HplusTB_M180", st1)
    mt.histoMgr.forHisto("HplusTB_M200", st2)
    mt.histoMgr.forHisto("HplusTB_M300", st3)
   # mt.histoMgr.forHisto("TTToHplus_M90", st1)
   # mt.histoMgr.forHisto("TTToHplus_M120", st2)
   # mt.histoMgr.forHisto("TTToHplus_M160", st3)
    #mt.histoMgr.forHisto("QCD", st1)
#    mt.histoMgr.setHistoDrawStyleAll("P")
#    rtauGen(mt, "transverseMass_vs_mH", rebin=20, defaultStyles=False)
    #rtauGen(mt, "transverseMassTauVeto", rebin=5, defaultStyles=False)
    rtauGen(mt, "BackToBackTailKillerComparisonJet1_heavyHplus", rebin=2, ratio=False, defaultStyles=False)
        
def MetComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("Data").getDatasetRootHisto("Met"),
        datasets.getDataset("Data").getDatasetRootHisto("MetWithBtagging")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt.histoMgr.normalizeToOne()
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("Met", st1)
    mt.histoMgr.forHisto("MetWithBtagging", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")

    opts = {"ymin": 0.001, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = "Met"
#    mt.createFrameFraction(name, opts=opts, opts2=opts2)

    rtauGen(mt, "MetComparison", rebin=2, defaultStyles=False)


def BetaComparison(datasets):
    if mcOnly:
        return

    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("JetSelection/betaGenuine"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("JetSelection/betaPU"),
        datasets.getDataset("Data").getDatasetRootHisto("JetSelection/betaPU")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
#    mt.histoMgr.forHisto("betaGenuine", st1)
#    mt.histoMgr.forHisto("betaPU", st2)
    mt.histoMgr.forHisto(datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("JetSelection/betaGenuine"), st1)
    mt.histoMgr.forHisto(datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("JetSelection/betaPU"), st2)
    mt.histoMgr.forHisto(datasets.getDataset("Data").getDatasetRootHisto("JetSelection/betaPU"), st3) 
    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "BetaComparison_H120", rebin=5, defaultStyles=False)

    
def HiggsMassComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M80").getDatasetRootHisto("FullHiggsMass/HiggsMass"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("FullHiggsMass/HiggsMass"),
        datasets.getDataset("TTToHplusBWB_M160").getDatasetRootHisto("FullHiggsMass/HiggsMass")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))

    mt.histoMgr.forHisto("TTToHplusBWB_M80", st1)
    mt.histoMgr.forHisto("TTToHplusBWB_M120", st2)
    mt.histoMgr.forHisto("TTToHplusBWB_M160", st3) 
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "HiggsMassVsMass", rebin=2, defaultStyles=False)

def InvMassComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("FullHiggsMass/HiggsMass"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("FullHiggsMass/HiggsMassTauBmatch"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("FullHiggsMass/HiggsMassTauBMETmatch")
        ])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("HiggsMass", st1)
    mt.histoMgr.forHisto("HiggsMassTauBmatch", st2)
    mt.histoMgr.forHisto("HiggsMassTauBMETmatch", st3)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "HiggsMass_matching", rebin=2, defaultStyles=False)

    
def rtauComparison(datasets):
    mt = plots.PlotBase([
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("tauID/TauID_Rtau_DecayModeOneProng_ZeroPiZero"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("tauID/TauID_Rtau_DecayModeOneProng_OnePiZero"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("tauID/TauID_Rtau_DecayModeOneProng_TwoPiZero"),
        datasets.getDataset("TTToHplusBWB_M120").getDatasetRootHisto("tauID/TauID_Rtau_DecayModeOneProng_Other")])
    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("TTToHplus_M80", st1)
    mt.histoMgr.forHisto("TTToHplus_M120", st2)
    mt.histoMgr.forHisto("TTToHplus_M160", st3)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(mt, "rtau_vs_DecayModes", rebin=1, defaultStyles=False)



def topMassComparison(datasets):
    def createHisto(path, name):
        drh = datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(path)
        drh.setName(name)
        return drh
    
    top = plots.PlotBase([
        createHisto("TopSelection/TopMass", "Max(p_{T}^{jjb}) method"),
        createHisto("TopChiSelection/TopMass", "Min(#chi^{2}) method"),
        createHisto("TopWithBSelection/TopMass", "Min(#chi^{2}) with b-jet sel.")]) 
    top.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    top._setLegendStyles()
    top._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineColor=4, lineWidth=2))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3,lineColor=1, lineWidth=3))
    top.histoMgr.forHisto("Max(p_{T}^{jjb}) method", st3)
    top.histoMgr.forHisto("Min(#chi^{2}) method", st1)
    top.histoMgr.forHisto("Min(#chi^{2}) with b-jet sel.", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")

    rtauGen(top, "topMass120", rebin=1, defaultStyles=False)

def topMassPurity(datasets):
    def createHisto(path, name):
        drh = datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(path)
        drh.setName(name)
        return drh
    
    top = plots.PlotBase([
        createHisto("TopChiSelection/TopMass", "All combinations"),
        createHisto("TopChiSelection/TopMass_fullMatch", "Matched jets"),
        createHisto("TopChiSelection/TopMass_bMatch", "Matched b jet")]) 
    top.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    top._setLegendStyles()
    top._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineColor=4, lineWidth=2))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3,lineColor=1, lineWidth=3))
    top.histoMgr.forHisto("All combinations", st3)
    top.histoMgr.forHisto("Matched jets", st1)
    top.histoMgr.forHisto("Matched b jet", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    histograms.addText(0.25, 0.5, "Normalized to unit area", 17)
    rtauGen(top, "topMassPurity", rebin=1, defaultStyles=False)

    
def genQuarkComparison(datasets):
    def createHisto(path, name):
        drh = datasets.getDataset("TTToHplus_M120").getDatasetRootHisto(path)
        drh.setName(name)
        return drh
    
    quark = plots.PlotBase([
        createHisto("BjetSelection/PtBquarkFromTopSide", "b quark from top side"),
        createHisto("BjetSelection/PtQquarkFromTopSide", "q quark from top"),]) 
    quark.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    quark._setLegendStyles()
    quark._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[0]])
    st1.append(styles.StyleLine(lineColor=4, lineWidth=2))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st3.append(styles.StyleLine(lineStyle=3,lineColor=1, lineWidth=3))
    quark.histoMgr.forHisto("b quark from top side", st3)
    quark.histoMgr.forHisto("q quark from top", st1)
#    mt.histoMgr.setHistoDrawStyleAll("P")
    rtauGen(quark, "ptQuarks", rebin=3, defaultStyles=False)

    
##############def genComparison(datasets):
#    rtau = plots.PlotBase([
#        datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("GenParticleAnalysis/genRtau1ProngHp"),
#        datasets.getDataset("TTJets").getDatasetRootHisto("GenParticleAnalysis/genRtau1ProngW")
#        ])
#    rtau.histoMgr.normalizeToOne()
#    rtau.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
#    rtau._setLegendStyles()
#    rtau._setLegendLabels()
#    st1 = styles.getDataStyle().clone()
#    st2 = st1.clone()
#    st2.append(styles.StyleLine(lineColor=ROOT.kRed))
#    rtau.histoMgr.forHisto(datasets.getDataset("TTToHplus_M120").getDatasetRootHisto("GenParticleAnalysis/genRtau1ProngHp"), st1)
#    rtau.histoMgr.forHisto(datasets.getDataset("TTJets").getDatasetRootHisto("GenParticleAnalysis/genRtau1ProngW"), st2)
    
#    rtau.histoMgr.setHistoDrawStyleAll("P")
################    rtauGen(rtau, "RtauGenerated", rebin=1)


    
#def genComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTJets_TuneZ2"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto("genRtau1ProngHp"),
#                                 datasets.getDataset(bagkground).getDatasetRootHisto("genRtau1ProngW")),
#          "RtauGen_Hp_vs_tt")

    
#def zMassComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "DYJetsToLL"
#    rtauGen(plots.ComparisonPlot(datasets.getDataset(signal).getDatasetRootHisto("/TauJetMass"),
#                                 datasets.getDataset(background).getDatasetRootHisto("/TauJetMass")),
#            "TauJetMass_Hp_vs_Zll")
    

#def topPtComparison(datasets):
#    signal = "TTToHplusBWB_M120"
#    background = "TTToHplusBWB_M120"
#    rtauGen(plots.PlotBase([datasets.getDataset(signal).getDatasetRootHisto("TopSelection/Pt_jjb"),
#                            datasets.getDataset(background).getDatasetRootHisto("TopSelection/Pt_jjbmax"),
#                            datasets.getDataset(background).getDatasetRootHisto("TopSelection/Pt_top")]),
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
#    normalization = 0.00606 * 0.86
    normalization = 0.025
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
#    h.stackMCSignalHistograms()

#    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
    h.stackMCHistograms()
    
    if addMCUncertainty:
        h.addMCUncertainty()
        
    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    if not log:
        _opts["ymin"] = 0
        _opts["ymaxfactor"] = 1.1
##    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts2 = {"ymin": 0.0, "ymax": 2.0}
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
    h.addStandardTexts(addLuminosityText=addLuminosityText)
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


        opts = {"xmax": 40}
        opts_log = {"ymin": 1e-10, "ymaxfactor": 30, "xmax": 40}
        opts_log.update(opts)

        opts2 = {"ymin": 0, "ymax": 3}
        opts2_log = opts2
        #opts2_log = {"ymin": 5e-2, "ymax": 5e2}
        
        h.createFrame(prefix+"vertices"+postfix, opts=opts, createRatio=False, opts2=opts2)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)
        h.setLegend(histograms.createLegend())
        h.draw()
        h.addStandardTexts()
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        h.save()

        h.createFrame(prefix+"vertices"+postfix+"_log", opts=opts_log, createRatio=ratio, opts2=opts2_log)
        h.frame.GetXaxis().SetTitle(xlabel)
        h.frame.GetYaxis().SetTitle(ylabel)

        h.getPad().SetLogy(True)
        #h.getPad2().SetLogy(True)
        h.setLegend(histograms.createLegend())


        h.draw()
        h.addStandardTexts()
        if h.normalizeToOne:
            histograms.addText(0.35, 0.9, "Normalized to unit area", 17)
        h.save()

def rtauGen(h, name, rebin=2, ratio=False, defaultStyles=True):
    if defaultStyles:
        h.setDefaultStyles()
        h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    
    xlabel = "p^{leading track} / p^{#tau jet}"
#    xlabel = "#beta^{jet}"
    ylabel = "Events / %.2f" % h.binWidth()
    if "LeptonsInMt" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    if "NoLeptonsRealTau" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    if "Mass" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
#        xlabel = "m (GeV/c^{2})"
    if "HiggsMass" in name:
        xlabel = "m_{H^{#pm}} (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
#        xlabel = "m (GeV/c^{2})"
    if "topMass" in name:
        xlabel = "m_{top} (GeV/c^{2})"
    if "BackToBack" in name:
        xlabel = "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{2}}"
    if "Collinear" in name:
        xlabel = "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}}"
    if "vertex" in name:
        xlabel = "Raw PF E_{T}^{miss} (GeV)"
    if "Quark" in name:
        xlabel = "p_{T} (GeV)"
    if "Beta" in name:
        xlabel = "#beta^{jet}"
    if "Rtau" in name:
        ylabel = "A.u."
    elif "Pt" in name:
        xlabel = "p_{T}(GeV/c)"
    elif "vertices" in name:
        xlabel = "N_{vertices}"

        
    kwargs = {"ymin": 0.1, "xmax": 1.0}

    if "LeptonsInMt" in name: 
        kwargs = {"ymin": 0., "xmax": 300}
    if "NoLeptonsRealTau" in name: 
        kwargs = {"ymin": 0., "xmax": 300}
    if "Rtau" in name:
        kwargs = {"ymin": 0.0001, "xmax": 1.1}   
        kwargs = {"ymin": 0.1, "xmax": 1.1}     
        h.getPad().SetLogy(True)
    elif "Pt" in name:
        kwargs = {"ymin": 0.1, "xmax": 400}
        h.getPad().SetLogy(True)
    elif "Mass" in name:
        kwargs = {"ymin": 0.1, "xmax": 400}
    elif "DecayMode" in name:
        kwargs = {"ymin": 0.1, "xmax": 1.1}
    elif "Beta" in name:
        kwargs = {"ymin": 0.01, "xmax": 1.0}
    elif "DeltaR_TauMETJet" in name:
        kwargs = {"ymin": 0.01, "xmax": 260}
        xlabel = "#DeltaR in #Delta#phi(#tau,MET) vs #Delta#phi(jet4,MET) plane "
        ylabel = "Events" 

    if "Collinear" in name:
        kwargs = {"ymin": 0.0, "xmax": 270}   
        #kwargs = {"ymin": 0.1, "xmax": 1.1}
    if "BackToBack" in name:
        kwargs = {"ymin": 0.0, "xmax": 270}         

#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
#    name = name+"_log"

    h.createFrame(name, **kwargs)

#    histograms.addText(0.65, 0.7, "BR(t #rightarrow bH^{#pm})=0.05", 20)
    h.getPad().SetLogy(True)
    
    leg = histograms.createLegend(0.6, 0.75, 0.8, 0.9)
    h.getPad().SetLogy(True)
    if "LeptonsInMt" in name:
        h.getPad().SetLogy(False)
        leg = histograms.moveLegend(leg, dx=-0.18)
        histograms.addText(0.5, 0.65, "TailKiller cut: Tight", 20)
    if "NoLeptonsRealTau" in name:
        h.getPad().SetLogy(False)
        leg = histograms.moveLegend(leg, dx=-0.18)
        histograms.addText(0.5, 0.65, "TailKiller cut: Loose", 20)
    if "Mass" in name:
        h.getPad().SetLogy(False)
    if "Quark" in name:
        h.getPad().SetLogy(False)
    #leg = histograms.createLegend(0.6, 0.75, 0.8, 0.9)
    if "topMass" in name:
        leg = histograms.moveLegend(leg, dx=0.2)
    h.setLegend(leg)
    if "Collinear" in name:
       h.getPad().SetLogy(False)
    if "BackToBack" in name:
       h.getPad().SetLogy(False) 
    if  "vertex" in name:
        histograms.addText(0.75, 0.9, "Data", 22) 
        plots._legendLabels["Data"] = "vertex3"
    if "DeltaR_TauMETJet" in name:
        h.getPad().SetLogy(False)
        

    common(h, xlabel, ylabel)


    

def selectionFlow(h, name, rebin=1, ratio=False):

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Cut"
    ylabel = "Events"
    
    scaleMCfromWmunu(h)     
#    h.stackMCSignalHistograms()

    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
#    h.stackMCHistograms()
    
    
    h.addMCUncertainty()



    njets = 5
    lastSelection = njets
    
    
    opts = {"xmax": lastSelection, "ymin": 0.1, "ymaxfactor": 20, "nbins": lastSelection}
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
    h.addStandardTexts()
    addMassBRText(x=0.4, y=0.87)
    h.save()
    
def selectionFlowTauCand(h, name, rebin=1, ratio=True):

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "Cut"
    ylabel = "Events"
    
    scaleMCfromWmunu(h)     
#    h.stackMCSignalHistograms()

    h.stackMCHistograms(stackSignal=True)#stackSignal=True)    
#    h.stackMCHistograms()
    
    
    h.addMCUncertainty()


    
    deltaphi = 8
    lastSelection = deltaphi
    
    opts = {"xmax": lastSelection, "ymin": 1.0, "ymaxfactor": 20, "nbins": lastSelection}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    h.createFrame(name, opts=opts, createRatio=ratio, opts2=opts2)
    xaxis = h.getFrame().GetXaxis()
    xaxis.SetBinLabel(1, "Trigger")
    xaxis.SetBinLabel(2, "#tau candidate")
    xaxis.SetBinLabel(3, "e veto")
    xaxis.SetBinLabel(4, "#mu veto")
    xaxis.SetBinLabel(5, "N_{jets}")
    xaxis.SetBinLabel(6, "MET")
    xaxis.SetBinLabel(7, "b tagging")
    xaxis.SetBinLabel(8, "#Delta#phi")
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    h.draw()
    h.addStandardTexts()
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
    h.addStandardTexts()
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
    h.addStandardTexts()
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
    h.addStandardTexts()
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
#    name = name+"_log"
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
        self.br = 0.01
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
