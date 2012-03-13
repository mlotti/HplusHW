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

import math, array, os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import plotMuonAnalysis as muonAnalysis

# Configuration
#analysis = "signalAnalysisRtau0"
#analysis = "signalAnalysisRtau70"
#analysis = "signalAnalysisRtau80"

#postfix = ""
#postfix = "CaloMet60"
postfix = "CaloMet60TEff"

analysis = "signalAnalysis"+postfix
#analysis = "signalAnalysisRtau0MET50"+postfix
analysisNoRtau = "signalAnalysisRtau0MET50"+postfix
#analysis = analysisNoRtau

#analysis = "signalAnalysisTauSelectionHPSTightTauBased"
#analysis = "signalAnalysisRelIso50"
#analysis = "signalAnalysisRelIso15"
#analysis = "signalAnalysisRelIso10"
#analysis = "signalAnalysisPfRelIso50"
#analysis = "signalAnalysisPfRelIso15"
#analysis = "signalAnalysisPfRelIso10"
#analysis = "signalAnalysisIsoTauVLoose"
#analysis = "signalAnalysisIsoTauLoose"
#analysis = "signalAnalysisIsoTauMedium"
#analysis = "signalAnalysisIsoTauTight"
#analysis = "signalAnalysisIsoTauLikeVLoose"
#analysis = "signalAnalysisIsoTauLikeLoose"
#analysis = "signalAnalysisIsoTauLikeMedium"
#analysis = "signalAnalysisIsoTauLikeTight"
#analysis = "signalAnalysisIsoTauLikeTightSc015"
#analysis = "signalAnalysisIsoTauLikeTightSc02"
#analysis = "signalAnalysisIsoTauLikeTightIc04"
#analysis = "signalAnalysisIsoTauLikeTightSc015Ic04"
#analysis = "signalAnalysisIsoTauLikeTightSc02Ic04"
#analysis = "signalAnalysisJESPlus03eta02METPlus10"
#analysis = "signalAnalysisJESMinus03eta02METPlus10"
#analysis = "signalAnalysisJESPlus03eta02METMinus10"
#analysis = "signalAnalysisJESMinus03eta02METMinus10"
counters = analysis+"Counters"

normalize = True
#normalize = False

#era = "EPS"
#era = "Run2011A-EPS"
era = "Run2011A"

tauEmbedding.normalize = normalize
tauEmbedding.era = era

countersWeighted = counters
if normalize:
    countersWeighted = counters+"/weighted"
#countersWeighted = counters+"/weighted"

tauPtOutput ="tauPt_ewk.root"
mtOutput = "mt_ewk_lands.root"

weight = "weightPileup"
weightBTagging = weight+"*weightBTagging"
#weight = ""
#weightBTagging = weight
if normalize:
    weight = "weightPileup*weightTrigger"
    weightBTagging = weight+"*weightBTagging"
treeDraw = dataset.TreeDraw(analysis+"/tree", weight=weight)

caloMetCut = "(tecalomet_p4.Et() > 60)"
caloMetNoHFCut = "(tecalometNoHF_p4.Et() > 60)"
metCut = "(met_p4.Et() > 50)"
bTaggingCut = "passedBTagging"
deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"
deltaPhi90Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 90)"


# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters,
#                                                   weightedCounters=countersWeighted, firstWeightedCount="All events"
                                                   )

    if era == "EPS":
        datasets.remove([
            "SingleMu_Mu_170722-172619_Aug05",
            "SingleMu_Mu_172620-173198_Prompt",
            "SingleMu_Mu_173236-173692_Prompt",
        ])
    elif era == "Run2011A-EPS":
        datasets.remove([
            "SingleMu_Mu_160431-163261_May10",
            "SingleMu_Mu_163270-163869_May10",
            "SingleMu_Mu_165088-166150_Prompt",
            "SingleMu_Mu_166161-166164_Prompt",
            "SingleMu_Mu_166346-166346_Prompt",
            "SingleMu_Mu_166374-167043_Prompt",
            "SingleMu_Mu_167078-167913_Prompt",

#            "SingleMu_Mu_170722-172619_Aug05",
#            "SingleMu_Mu_172620-173198_Prompt",
#            "SingleMu_Mu_173236-173692_Prompt",

            ])
    elif era == "Run2011A":
        pass
    else:
        raise Exception("Unsupported era "+era)
    datasets.loadLuminosities()
    #print datasets.getAllDatasetNames()
    #return

#    apply_v13_1_bugfix(datasets)

    tauEmbedding.updateAllEventsToWeighted(datasets)
    plots.mergeRenameReorderForDataMC(datasets)
    datasets.remove(["W3Jets"])

#    datasets.remove(["DYJetsToLL", "SingleTop", "Diboson", "QCD_Pt20_MuEnriched"])

    # Signal
    #keepSignal = "M80"
    #keepSignal = "M90"
    #keepSignal = "M100"
    #keepSignal = "M120"
    #keepSignal = "M140"
    #keepSignal = "M150"
    keepSignal = "M155"
    #keepSignal = "M160"
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    # Replace signal dataset with EWK+signal
    if False:
        datasets.remove(filter(lambda name: "TTToHplus" in name and not keepSignal in name, datasets.getAllDatasetNames()))
        xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
        #xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.1, br_Htaunu=1)
        plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

        ttjets2 = datasets.getDataset("TTJets").deepCopy()
        ttjets2.setName("TTJets2")
        ttjets2.setCrossSection(ttjets2.getCrossSection() - datasets.getDataset("TTToHplus_"+keepSignal).getCrossSection())
        datasets.append(ttjets2)
        datasets.merge("EWKnoTT", ["WJets", "DYJetsToLL", "SingleTop", "Diboson"], keepSources=True)
        #datasets.merge("TTToHplus_"+keepSignal, ["TTToHplus_"+keepSignal, "EWKnoTT", "TTJets2"])
        datasets.merge("EWKScaled", ["EWKnoTT", "TTJets2"])
        datasets.merge("EWKSignal", ["TTToHplus_"+keepSignal, "EWKScaled"], keepSources=True)
        plots._legendLabels["TTToHplus_"+keepSignal] = "with H^{#pm}#rightarrow#tau^{#pm}#nu"
    else:
        datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))

    #datasets.remove(filter(lambda name: "TTJets" not in name, datasets.getAllDatasetNames()))

    mcLumi = None
    if not datasets.hasDataset("Data"):
        mcLumi = 2173

#    scaleLumi.signalLumi = 43.4024599650000037
#    scaleLumi.ewkLumi = datasets.getDataset("Data").getLuminosity()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    histograms.createLegend.moveDefaults(dx=-0.04)
    #datasets.remove(["QCD_Pt20_MuEnriched"])
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dh=-0.05)
    #histograms.createLegend.moveDefaults(dx=-0.18, dy=0.05, dh=-0.05)

    doPlots(datasets, mcLumi)
    doCounters(datasets, mcLumi)


def apply_v13_1_bugfix(datasets):
    d = {
        "DYJetsToLL_M50_TuneZ2_Summer11": 36277956,
        "TTJets_TuneZ2_Summer11": 3701947,
        "T_s-channel_TuneZ2_Summer11": 259971,
        "T_t-channel_TuneZ2_Summer11": 3900171,
        "T_tW-channel_TuneZ2_Summer11": 814390,
        "Tbar_s-channel_TuneZ2_Summer11": 137980,
        "Tbar_t-channel_TuneZ2_Summer11": 1944826,
        "Tbar_tW-channel_TuneZ2_Summer11": 809984,
        "T_tW-channel_TuneZ2_Summer11": 814390,
        "Tbar_s-channel_TuneZ2_Summer11": 137980,
        "Tbar_t-channel_TuneZ2_Summer11": 1944826,
        "Tbar_tW-channel_TuneZ2_Summer11": 809984,
        "WJets_TuneZ2_Summer11": 81352576,
        "WW_TuneZ2_Summer11": 4225916,
        "WZ_TuneZ2_Summer11": 4265243,
        "ZZ_TuneZ2_Summer11": 4187885
        }
    for name, nevents in d.iteritems():
        datasets.getDataset(name).setNAllEvents(nevents)


# Create the plot objects and pass them to the formatting
# functions to be formatted, drawn and saved to files
def createPlotCommon(name, datasets, mcLumi=None):
    kwargs = {}
    if mcLumi != None:
        kwargs["normalizeToLumi"] = mcLumi
    name2 = name
    if isinstance(name, basestring):
        name2 = analysis+"/"+name
    return plots.DataMCPlot(datasets, name2, **kwargs)

def doPlots(datasets, mcLumi=None):
    createPlot = lambda name: createPlotCommon(name, datasets, mcLumi)
    #opts = {"xmin": 40, "xmax": 200, "ymaxfactor":10, "ymin": 1e-1}
    opts = {"xmin": 40, "xmax": 200, "ymaxfactor":2, "ymin": 1e-1}
    opts2 = {"ymin": 0, "ymax": 2}
    rebin = 10
    tdTauPt = treeDraw.clone(varexp="tau_p4.Pt()>>tmp(16, 40, 200)")
    tdTauP = treeDraw.clone(varexp="tau_p4.P()>>tmp(16, 40, 200)")
    tdTauLeadPt = treeDraw.clone(varexp="tau_leadPFChargedHadrCand_p4.Pt()>>tmp(16, 40, 200)")
    tdTauLeadP = treeDraw.clone(varexp="tau_leadPFChargedHadrCand_p4.P()>>tmp(16, 40, 200)")
    tdRtau = treeDraw.clone(varexp="tau_leadPFChargedHadrCand_p4.P() / tau_p4.P() -1e-10 >>tmp(11, 0, 1.1)")
    tdDeltaPhi = treeDraw.clone(varexp="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 >>tmp(18, 0, 180)")

    drawPlot = tauEmbedding.drawPlot

    # Tau pt
    xlabel = "p_{T}^{#tau jet} (GeV/c)"
    drawPlot(createPlot("SelectedTau/SelectedTau_pT_AfterTauID"), "selectedTauPt_1AfterTauID", xlabel, opts=opts, rebin=rebin, ratio=False)
    drawPlot(createPlot(tdTauPt.clone()), "selectedTauPt_1AfterTauID_crosscheck", xlabel, opts=opts, ratio=False)
    drawPlot(createPlot(tdTauPt.clone(selection=metCut)), "selectedTauPt_2AfterMET", xlabel, opts=opts, ratio=False)

    optstmp = {}
    optstmp.update(opts)
    del optstmp["ymaxfactor"]
    optstmp["ymax"] = 60
    drawPlot(createPlot(tdTauPt.clone(selection=metCut+"&&"+bTaggingCut, weight=weightBTagging)),
             "selectedTauPt_3AfterBTagging", xlabel, opts=optstmp)
    drawPlot(createPlot(tdTauPt.clone(selection=metCut+"&&"+bTaggingCut+"&&"+deltaPhi160Cut, weight=weightBTagging)),
             "selectedTauPt_4AfterDeltaPhi160", xlabel, opts=optstmp)
    drawPlot(createPlot(tdTauPt.clone(selection=metCut+"&&"+bTaggingCut+"&&"+deltaPhi130Cut, weight=weightBTagging)),
             "selectedTauPt_4AfterDeltaPhi130", xlabel, opts=optstmp)

    drawPlot(createPlot(tdTauPt.clone(selection=metCut+"&&"+bTaggingCut, weight="")),
             "selectedTauPt_3AfterBTagging_notNormalized", xlabel, opts=optstmp, normalize=False)
    drawPlot(createPlot(tdTauPt.clone(selection=metCut+"&&"+bTaggingCut+"&&"+deltaPhi160Cut, weight="")),
             "selectedTauPt_4AfterDeltaPhi160_notNormalized", xlabel, opts=optstmp, normalize=False)
    drawPlot(createPlot(tdTauPt.clone(selection=metCut+"&&"+bTaggingCut+"&&"+deltaPhi130Cut, weight="")),
             "selectedTauPt_4AfterDeltaPhi130_notNormalized", xlabel, opts=optstmp, normalize=False)


    # Tau leading track pt
    xlabel = "p_{T}^{#tau leading track} (GeV/c)"
    drawPlot(createPlot(tdTauLeadPt.clone()), "selectedTauLeadPt_1AfterTauID", xlabel, opts=opts, ratio=False)

    # Tau p
    xlabel = "p^{#tau jet} (GeV/c)"
    drawPlot(createPlot(tdTauP.clone()), "selectedTauP_1AfterTauID", xlabel, opts=opts, ratio=False)

    # Tau leading track pt
    xlabel = "p^{#tau leading track} (GeV/c)"
    drawPlot(createPlot(tdTauLeadP.clone()), "selectedTauLeadP_1AfterTauID", xlabel, opts=opts,ratio=False)
    
    # Rtau
    xlabel = "R_{#tau}"
    drawPlot(createPlot(tdRtau.clone()), "selectedTauRtau_1AfterTauID", xlabel, ylabel="Events / %.f", opts={"ymin": 1e-1}, ratio=False)


    # DeltaPhi
    xlabel = "#Delta#phi(#tau jet, E_{T}^{miss}) (^{#circ})"
    def customDeltaPhi(h):
        yaxis = h.getFrame().GetYaxis()
        yaxis.SetTitleOffset(0.8*yaxis.GetTitleOffset())
    drawPlot(createPlot(tdDeltaPhi.clone()), "deltaPhi_1AfterTauID", xlabel, ylabel="Events / %.f^{#circ}", opts={"ymin": 1e-1, "ymaxfactor": 5}, opts2=opts2, moveLegend={"dx": -0.22, "dy":0.01, "dh": -0.03}, customise=customDeltaPhi, cutLine=[130, 160])

    # Data-driven control plots
    def drawControlPlot(path, xlabel, **kwargs):
        drawPlot(createPlot("ControlPlots/"+path), "controlPlots_"+path, xlabel, opts2=opts2, **kwargs)
    drawControlPlot("SelectedTau_pT_AfterStandardSelections", "#tau-jet p_{T} (GeV/c)", opts={"xmax": 250}, rebin=2, cutBox={"cutValue": 40, "greaterThan": True})
    drawControlPlot("SelectedTau_eta_AfterStandardSelections", "#tau-jet #eta", opts={"xmin": -2.2, "xmax": 2.2}, ylabel="Events / %.1f", rebin=4, moveLegend={"dy":-0.5, "dx":-0.1})
    drawControlPlot("SelectedTau_phi_AfterStandardSelections", "#tau-jet #phi", rebin=10, ylabel="Events / %.2f")
    drawControlPlot("SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts={"xmax": 250}, rebin=2, cutBox={"cutValue": 20, "greaterThan": True})
    drawControlPlot("SelectedTau_Rtau_AfterStandardSelections", "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", opts={"xmin": 0.65, "xmax": 1.05, "ymin": 1e-1, "ymaxfactor": 10}, rebin=5, ylabel="Events / %.2f", moveLegend={"dx":-0.4, "dy": 0.01, "dh": -0.03}, cutBox={"cutValue":0.7, "greaterThan":True})
    drawControlPlot("SelectedTau_p_AfterStandardSelections", "#tau-jet p (GeV/c)", rebin=2)
    drawControlPlot("SelectedTau_LeadingTrackP_AfterStandardSelections", "#tau-jet ldg. charged particle p (GeV/c)", rebin=2)
    #drawControlPlot("IdentifiedElectronPt_AfterStandardSelections", "Electron p_{T} (GeV/c)")
    #drawControlPlot("IdentifiedMuonPt_AfterStandardSelections", "Muon p_{T} (GeV/c)")
    drawControlPlot("Njets_AfterStandardSelections", "Number of jets", ylabel="Events")
    drawControlPlot("MET", "Uncorrected PF E_{T}^{miss} (GeV)", rebin=5, opts={"xmax": 400}, cutLine=50)
    drawControlPlot("NBjets", "Number of selected b jets", opts={"xmax": 6}, ylabel="Events", cutLine=1)

    # Number of EWK events for QCD measurement (not needed at the moment
    # del opts["xmin"]
    # del opts["xmax"]
    # f = ROOT.TFile.Open(tauPtOutput, "RECREATE")
    # bins = [40, 50, 60, 70, 80, 100, 120, 150, 300]
    # tauPtPrototype = ROOT.TH1F("tauPtHistoFoo", "Tau pt", len(bins)-1, array.array("d", bins))
    # tauPtPrototype.SetDirectory(ROOT.gDirectory)
    # for name, an in [
    #     ("AllSelectionsNoRtau", analysisNoRtau),
    #     ("AllSelections", analysis)
    #     ]:

    #     td = treeDraw.clone(tree=an+"/tree", varexp="tau_p4.Pt() >>tauPtHistoFoo", weight=weightBTagging, selection=metCut+"&&"+bTaggingCut)

    #     tauPt(createPlot(td), "selectedTauPt_9"+name, opts=opts)
    #     pt = createPlot(td)
    #     scaleNormalization(pt)
    #     pt_data = pt.histoMgr.getHisto("Data").getRootHisto().Clone("tauPt_ewk_"+name)
    #     pt_data.SetDirectory(f)
    #     pt_data.Write()
        
    # f.Close()

    opts = {"xmin": 70, "ymaxfactor": 10}
    rebin = 10

    tdMet = treeDraw.clone(varexp="met_p4.Et()>>tmp(20,0,200)")
    tdMetOrig = treeDraw.clone(varexp="temet_p4.Et()>>tmp(20,0,200)")

    opts = {}

    #tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(40,0,400)")
    tdMt = treeDraw.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) >>tmp(20,0,400)")
    #f = ROOT.TFile.Open(mtOutput, "RECREATE")

    ratio = True
    if normalize and not "Rtau0MET" in analysis:
        opts["ymax"] = 40
    elif not normalize:
        opts["xmax"] = 200
    deltaPhiLabel = "#Delta#phi(#tau jet, E_{T}^{miss})"
    for name, label, selection in [
        ("1AfterTauID", "", ""),
        ("2AfterMETCut", "", metCut),
        ("3AfterBTagging", "Without %s cut"%deltaPhiLabel, metCut+"&&"+bTaggingCut),
        #("3AfterBTagging_calo", caloMetCut+"&&"+metCut+"&&"+bTaggingCut),
        #("3AfterBTagging_caloNoHF", caloMetNoHFCut+"&&"+metCut+"&&"+bTaggingCut),
        ("4AfterDeltaPhi160", "%s < 160^{o}" % deltaPhiLabel, metCut+"&&"+bTaggingCut+"&&"+deltaPhi160Cut),
        ("4AfterDeltaPhi130", "%s < 130^{o}" % deltaPhiLabel, metCut+"&&"+bTaggingCut+"&&"+deltaPhi130Cut),
        ("4AfterDeltaPhi90", "%s < 90^{o}" % deltaPhiLabel, metCut+"&&"+bTaggingCut+"&&"+deltaPhi90Cut),
        ]:
        w = weight
        if bTaggingCut in selection:
            w = weightBTagging
        td = tdMt.clone(selection=selection, weight=w)
        p = createPlot(td.clone())
        p.appendPlotObject(histograms.PlotText(0.5, 0.55, label, size=20))
        drawPlot(p, "transverseMass_"+name, "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})", ylabel="Events / %.0f GeV/c^{2}", opts=opts, ratio=ratio, log=False)

        drawPlot(createPlot(td.clone(varexp="jets_btag >>tmp(30, 0, 3)")), "btagDiscriminator_"+name, "TCHE", ylabel="Jets / %.1f", ratio=ratio, opts={"ymin": 1e-1, "ymax": 1e2})

        #mt = createPlot(td.clone())
        #scaleNormalization(mt)
        #mt_data = mt.histoMgr.getHisto("Data").getRootHisto().Clone("mt_ewk_"+name)
        #mt_data.SetDirectory(f)
        #mt_data.Write()

    #path = ROOT.TNamed("producedInDirectory", os.getcwd())
    #path.Write()
    #f.Close()
    
def doCounters(datasets, mcLumi=None):
    createPlot = lambda name: createPlotCommon(name, datasets, mcLumi)
    eventCounter = counter.EventCounter(datasets, counters=countersWeighted)
   

    sels = [
#        "(sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) < 20)",
#        "(20 < sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))))", "(sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) < 80)",
#        "(80 < sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))))", "(sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))) < 120)",
#        "(120 < sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi()))))",
        ]
    tdCount = treeDraw.clone(weight=weightBTagging)
    tdCountMET = tdCount.clone(weight=weight, selection="&&".join(sels+[metCut]))
    tdCountBTagging = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut]))
    tdCountDeltaPhi160 = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut, deltaPhi160Cut]))
    tdCountDeltaPhi130 = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut, deltaPhi130Cut]))
    tdCountDeltaPhi90 = tdCount.clone(selection="&&".join(sels+[metCut, bTaggingCut, deltaPhi90Cut]))
    eventCounter.getMainCounter().appendRow("JetsForEffs", tdCount.clone(weight=weight, selection="&&".join(sels)))
    eventCounter.getMainCounter().appendRow("METForEffs", tdCountMET)
    eventCounter.getMainCounter().appendRow("BTagging", tdCountBTagging)
    eventCounter.getMainCounter().appendRow("DeltaPhi < 160", tdCountDeltaPhi160)
    eventCounter.getMainCounter().appendRow("DeltaPhi < 130", tdCountDeltaPhi130)
    eventCounter.getMainCounter().appendRow("DeltaPhi < 90", tdCountDeltaPhi90)

    td1 = tdCount.clone(selection=metCut+"&&"+bTaggingCut+"&& (tecalometNoHF_p4.Pt() > 60)")
    td2 = tdCount.clone(selection=metCut+"&&"+bTaggingCut+"&& (tecalomet_p4.Pt() > 60)")
    td3 = dataset.TreeDrawCompound(td1, {
            "SingleMu_Mu_170722-172619_Aug05": td2,
            "SingleMu_Mu_172620-173198_Prompt": td2,
            "SingleMu_Mu_173236-173692_Prompt": td2,
            })
    eventCounter.getMainCounter().appendRow("BTagging+CaloMetNoHF", td1)
    eventCounter.getMainCounter().appendRow("BTagging+CaloMet", td2)
    eventCounter.getMainCounter().appendRow("BTagging+CaloMet(NoHF)", td3)

    if mcLumi != None:
        eventCounter.normalizeMCToLuminosity(mcLumi)
    else:
        eventCounter.normalizeMCByLuminosity()
    tauEmbedding.scaleNormalization(eventCounter)

    ewkDatasets = [
        "WJets", "TTJets",
        "DYJetsToLL", "SingleTop", "Diboson"
        ]

    table = eventCounter.getMainCounterTable()
    mainTable = table
    muonAnalysis.addSumColumn(table)
    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
#    table = eventCounter.getSubCounterTable("Trigger")
    #    muonAnalysis.reorderCounterTable(table)
    muonAnalysis.addDataMcRatioColumn(table)
    if datasets.hasDataset("EWKSignal"):
        mainTable.insertColumn(7, counter.divideColumn("SignalFraction", mainTable.getColumn(name="TTToHplus_"+keepSignal), mainTable.getColumn(name="EWKSignal")))

    datasets.printInfo()
    print "============================================================"
    print "Main counter (%s)" % eventCounter.getNormalizationString()
    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.3f'))
    print table.format(cellFormat)

    tauTable = eventCounter.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight")
    #muonAnalysis.addSumColumn(tauTable)
    tauTable.insertColumn(2, counter.sumColumn("EWKMCsum", [tauTable.getColumn(name=name) for name in ewkDatasets]))
    print tauTable.format(cellFormat)

#    print eventCounter.getSubCounterTable("TauIDPassedJets::tauID_HPSTight").format()
#    table = eventCounter.getSubCounterTable("Trigger")
#    muonAnalysis.addSumColumn(table)
#    print table.format(cellFormat)

    mainTable.keepOnlyRows([
            "All events",
            "Trigger and HLT_MET cut",
            "taus == 1",
#            "trigger scale factor",
            "electron veto",
            "muon veto",
            "MET",
            "njets",
            "btagging",
            "btagging scale factor",
            "JetsForEffs",
            "METForEffs",
            "BTagging",
            "DeltaPhi < 160",
            "DeltaPhi < 130"
            ])
    tauTable.keepOnlyRows([
            "AllTauCandidates",
            "DecayModeFinding",
            "TauJetPt",
            "TauJetEta",
            "TauLdgTrackExists",
            "TauLdgTrackPtCut",
            "TauECALFiducialCutsCracksAndGap",
            "TauAgainstElectronCut",
            "TauAgainstMuonCut",
            #"EMFractionCut",
            "HPS",
            "TauOneProngCut",
            "TauRtauCut",
            ])

    #effFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%.4f'))
    effFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.4f'))
    #effFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat='%.4f'))
    for name, table in [("Main", mainTable), ("Tau ID", tauTable)]:
        effTable = counter.CounterTable()
        col = table.getColumn(name="Data")
        effTable.appendColumn(col)
        effTable.appendColumn(counter.efficiencyColumn(col.getName()+" eff", col))
        col = table.getColumn(name="EWKMCsum")
        effTable.appendColumn(col)
        effTable.appendColumn(counter.efficiencyColumn(col.getName()+" eff", col))
        print "%s counter efficiencies" % name
        print effTable.format(effFormat)


    print "Trigger uncertainties"
    bins = [40, 50, 60, 80]
    tauPtPrototype = ROOT.TH1F("tauPtTrigger", "Tau pt", len(bins)-1, array.array("d", bins))
    runs = [
        "(160431 <= run && run <= 167913)",
        "(170722 <= run && run <= 173198)",
        "(173236 <= run && run <= 173692)",
        #"(160431 <= run && run <= 173692)",
        ]
    for name, td in [
        ("BTagging", tdCountBTagging),
        ("DeltaPhi160", tdCountDeltaPhi160),
        ("DeltaPhi130", tdCountDeltaPhi130),
        ("DeltaPhi90", tdCountDeltaPhi90)
        ]:
        t = td.clone(varexp="tau_p4.Pt() >>tauPtTrigger")
        
        NallSum = 0
        NSum = 0
        absUncSquareSum = 0

        for runRegion in runs:
            #neventsPlot = createPlot(dataset.treeDrawToNumEntries(t.clone(weight="weightTrigger")))
            #uncertaintyPlot = createPlot(dataset.treeDrawToNumEntries(t.clone(weight="weightTriggerAbsUnc*weightTriggerAbsUnc/(weightTrigger*weightTrigger)")))
            tmp = t.clone(selection=t.selection+"&&"+runRegion)
            nallPlot = createPlot(tmp.clone(weight=""))
            neventsPlot = createPlot(tmp.clone(weight="weightTrigger"))
            uncertaintyPlot = createPlot(tmp.clone(weight="weightTriggerAbsUnc"))
            th1all = nallPlot.histoMgr.getHisto("Data").getRootHisto()
            th1 = neventsPlot.histoMgr.getHisto("Data").getRootHisto()
            th12 = uncertaintyPlot.histoMgr.getHisto("Data").getRootHisto()

            Nall = th1all.Integral(0, th1all.GetNbinsX()+1)
            N = th1.Integral(0, th1.GetNbinsX()+1)
            #absSum2 = th12.Integral(0, th12.GetNbinsX()+1)
            #absUnc = math.sqrt(absSum2)
            #absUnc = th12.Integral(0, 2)
            NallSum += Nall
            NSum += N
            absUnc = tauEmbedding.squareSum(th12)
            absUncSquareSum += absUnc
            absUnc = math.sqrt(absUnc)
            relUnc = 0
            if N > 0:
                relUnc = absUnc/N

            print "%-15s for runs %s Nall = %.2f, N = %.2f, absolute uncertainty %.2f, relative uncertainty %.4f" % (name, runRegion, Nall, N, absUnc, relUnc)


        absUnc = math.sqrt(absUncSquareSum)
        relUnc = absUnc/NSum

        print "%-15s Nall = %.2f, N = %.2f, absolute uncertainty %.2f, relative uncertainty %.4f" % (name, NallSum, NSum, absUnc, relUnc)
        print

    #latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f", valueOnly=True))
    #latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f", ))
#    latexFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.2f"))
#    print table.format(latexFormat)

# def scaleMCfromWmunu(obj):
#     # Data/MC scale factor from AN 2011/053, BR correction factor= 1/0.6479
#     rho = 0.9509/0.6479
#     scaleHistosCounters(obj, scaleMCHisto, "scaleMC", rho)

# def scaleTauBR(obj):
#     # tau -> hadrons branching fraction
#     fraction = 0.648
#     scaleHistosCounters(obj, scaleHisto, "scale", fraction)

# def scaleMuTriggerEff(obj):
#     # muon trigger efficiency
#     #data = 0.9 # this is from teh hat
#     #mc = 0.9 # this is from teh hat

#     #data = 1 # this is from teh hat
#     #mc = 1 # this is from teh hat

#     # From all
#     lumis = [3.1308106110000002, 5.0948740340000001, 27.696517908000001, 5.0667150779999997, 4.6417244929999999]
#     data = (lumis[0]*0.840278 + lumis[1]*0.872416 + lumis[2]*0.886409 + (lumis[3]+lumis[4])*0.872181) / sum(lumis)

#     # From 2011A only
# #    data = 0.872181
#     mc = 0.913055

#     scaleHistosCounters(obj, scaleDataHisto, "scaleData", 1/data)
#     scaleHistosCounters(obj, scaleMCHisto, "scaleMC", 1/mc)

# class LumiScaler:
#     def __init__(self, signalLumi=1, ewkLumi=1):
#         self.signalLumi = signalLumi
#         self.ewkLumi = ewkLumi

#     def getRho(self):
#         return self.signalLumi / self.ewkLumi

#     def __call__(self, obj):
#         scaleHistosCounters(obj, scaleHisto, "scale", self.getRho())

# scaleLumi = LumiScaler()   

 
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
