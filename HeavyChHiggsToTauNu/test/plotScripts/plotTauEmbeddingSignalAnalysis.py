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
import plotMuonAnalysis as muonAnalysis

# Configuration
analysis = "signalAnalysis"
#analysis = "signalAnalysisJESPlus03eta02METPlus00"
#analysis = "signalAnalysisJESPlus03eta02METMinus00"
#analysis = "signalAnalysisJESMinus03eta02METPlus00"
#analysis = "signalAnalysisJESMinus03eta02METMinus00"
#analysis = "signalAnalysisRtau0"
#analysis = "signalAnalysisRtau70"
#analysis = "signalAnalysisRtau80"

#analysis = "signalAnalysisCaloMet60"
#analysis = "signalAnalysisCaloMet60TEff"

#analysis = "signalAnalysisCaloMet60TEffJESPlus03eta02METPlus00"
#analysis = "signalAnalysisCaloMet60TEffJESMinus03eta02METPlus00"

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

countersWeighted = counters
#countersWeighted = counters+"/weighted"
if normalize:
    countersWeighted = counters+"/weighted"

output = "mt_ewk_lands.root"

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters,
#                                                   weightedCounters=countersWeighted, firstWeightedCount="All events"
                                                   )

    datasets.remove([
#        "SingleMu_160431-163261_May10",
#        "SingleMu_161119-161119_May10_Wed",
#        "SingleMu_163270-163869_May10",
#        "SingleMu_165088-166150_Prompt",
#        "SingleMu_166161-166164_Prompt",
#        "SingleMu_166346-166346_Prompt",
#        "SingleMu_166374-167043_Prompt",
#        "SingleMu_167078-167784_Prompt",
#        "SingleMu_167786-167913_Prompt_Wed"
        ])
    datasets.loadLuminosities()
#    datasets.remove(["Mu_136035-144114_Dec22", "Mu_146428-147116_Dec22", "Mu_147196-149294_Dec22"]) 

#    datasets41x = dataset.getDatasetsFromMulticrabCfg(cfgfile="/home/mkortela/hplus/CMSSW_4_1_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/tauEmbedding/multicrab_signalAnalysis_btag17_rtau0_caloMET60_taueff_pt40_110711_004336/multicrab.cfg", counters=counters)
#    datasets.extend(datasets41x)

#    datasetsDYQCD = dataset.getDatasetsFromMulticrabCfg(cfgfile="../multicrab_signalAnalysis_noEmuVetoEnd_MCGT_pt40_110714_111602/multicrab.cfg", counters=counters)
#    datasets.extend(datasetsDYQCD)

#    datasetsSignalAnalysis = dataset.getDatasetsFromMulticrabCfg(cfgfile="..//home/mkortela/hplus/norm/CMSSW_4_2_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/multicrab_110713_165352/multicrab.cfg")
#    datasetsSignalAnalysis.remove(filter(lambda n: "Tau_" in n, datasetsSignalAnalysis.getAllDatasetNames()))
#    datasets.extend(datasetsSignalAnalysis)
    
    plots.mergeRenameReorderForDataMC(datasets)

    mcOnly = not datasets.hasDataset("Data")
    mcLumi = 1062
#    mcLumi = 199.7
                                     

#    scaleLumi.signalLumi = 43.4024599650000037
#    scaleLumi.ewkLumi = datasets.getDataset("Data").getLuminosity()

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.18, dy=0.05, dh=-0.05)


    # Create the plot objects and pass them to the formatting
    # functions to be formatted, drawn and saved to files
    #opts = {"xmin": 40, "xmax": 200, "ymaxfactor":10, "ymin": 1e-1}
    opts = {"xmin": 40, "xmax": 200, "ymaxfactor":2, "ymin": 1e-1}
    rebin = 10

    def createPlot(name):
        kwargs = {}
        if mcOnly:
            kwargs["normalizeToLumi"] = mcLumi
        return plots.DataMCPlot(datasets, analysis+"/"+name, **kwargs)
    
    tauPt(createPlot("TauEmbeddingAnalysis_afterTauId_selectedTauPt"), opts=opts, rebin=rebin, ratio=False)
#    tauPt(createPlot("TauEmbeddingAnalysis_afterMetCut_selectedTauPt"), opts=opts, rebin=rebin, ratio=False)
    tauPt(createPlot("TauEmbeddingAnalysis_afterBTagging_selectedTauPt"), opts=opts, rebin=rebin, ratio=False)
    tauPt(createPlot("TauEmbeddingAnalysis_afterBTagging_selectedTauPtNoWeight"), opts=opts, rebin=10, ratio=False)
#    tauPt(createPlot("TauEmbeddingAnalysis_afterFakeMetVeto_selectedTauPt"), opts=opts, rebin=rebin, ratio=False)
#    tauEta(createPlot("TauEmbeddingAnalysis_afterTauId_selectedTauEta"), ratio=True)
#    tauPhi(createPlot("TauEmbeddingAnalysis_afterTauId_selectedTauPhi"), ratio=True)
#    leadingTrack(createPlot("TauEmbeddingAnalysis_afterTauId_leadPFChargedHadrPt"), ratio=True)
#    rtau(createPlot("tauID/TauID_RtauCut"), "TauIdRtau_afterTauId")
   
    tauCandPt(createPlot("tauID/TauSelection_all_tau_candidates_pt"), "tauCandidatePt", ratio=False)
    tauCandEta(createPlot("tauID/TauSelection_all_tau_candidates_eta"), "tauCandidateEta" , ratio=False)
    tauCandPhi(createPlot("tauID/TauSelection_all_tau_candidates_phi"), "tauCandidatePhi" , ratio=False)
    
#    muonPt(createPlot("TauEmbeddingAnalysis_begin_originalMuonPt"), ratio=True)
#    muonPt(createPlot("TauEmbeddingAnalysis_afterTauId_originalMuonPt"), ratio=True)
#    muonPt(createPlot("TauEmbeddingAnalysis_afterMetCut_originalMuonPt"), ratio=True)
    
#    muonEta(createPlot("TauEmbeddingAnalysis_begin_originalMuonEta"), ratio=True)
#    muonEta(createPlot("TauEmbeddingAnalysis_afterTauId_originalMuonEta"), ratio=True)
#    muonEta(createPlot("TauEmbeddingAnalysis_afterMetCut_originalMuonEta"), ratio=True)

 #   met(createPlot("TauEmbeddingAnalysis_begin_originalMet"), ratio=True)
 #   met(createPlot("TauEmbeddingAnalysis_afterTauId_originalMet"), ratio=True)
 #   met(createPlot("TauEmbeddingAnalysis_afterTauId_embeddingMet"), ratio=True)
 #   met(createPlot("TauEmbeddingAnalysis_begin_embeddingMet"), ratio=True)

    opts = {"xmin": 70, "ymaxfactor": 10}
    rebin = 10

#    met(createPlot("MET/met"))
#    met(createPlot("TauEmbeddingAnalysis_afterMetCut_originalMet"))
#    met(createPlot("TauEmbeddingAnalysis_afterBTagging_originalMet"))
#    met(createPlot("TauEmbeddingAnalysis_afterFakeMetVeto_originalMet"))
#    met(createPlot("TauEmbeddingAnalysis_afterMetCut_embeddingMet"))
#    met(createPlot("TauEmbeddingAnalysis_afterBTagging_embeddingMet"), opts=opts, rebin=rebin, ratio=False)
#    met(createPlot("TauEmbeddingAnalysis_afterFakeMetVeto_embeddingMet"), opts=opts, rebin=rebin, ratio=False)

#    deltaPhi(createPlot("TauEmbeddingAnalysis_afterTauId_DeltaPhi"))
#    deltaPhi(createPlot("TauEmbeddingAnalysis_afterTauId_DeltaPhiOriginal"))

    transverseMass(createPlot("TauEmbeddingAnalysis_begin_TransverseMass"))
    transverseMass(createPlot("TauEmbeddingAnalysis_afterTauId_TransverseMass"))
    transverseMass(createPlot("TauEmbeddingAnalysis_afterTauId_TransverseMassOriginal"))

    opts = {}
    transverseMass(createPlot("TauEmbeddingAnalysis_afterBTagging_TransverseMass"), opts=opts, rebin=rebin)
    transverseMass(createPlot("TauEmbeddingAnalysis_afterFakeMetVeto_TransverseMass"), opts=opts, rebin=rebin)

    mt = createPlot("TauEmbeddingAnalysis_afterBTagging_TransverseMass")
    scaleNormalization(mt)
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    f = ROOT.TFile.Open(output, "RECREATE")
    mt_data = mt.histoMgr.getHisto("Data").getRootHisto().Clone("mt_ewk")
    mt_data.SetDirectory(f)
    f.Write()
    f.Close()
    

#    jetPt(createPlot("JetSelection/jet_pt"), "jetPtEmb")
#    jetEta(createPlot("JetSelection/jet_eta"), "jetEtaEmb")
#    jetPhi(createPlot("JetSelection/jet_phi"), "jetPhiEmb")
#    numberOfJets(createPlot("JetSelection/NumberOfSelectedJets"), "NumberOfJetsEmb")

#    jetPt(createPlot("Btagging/bjet1_pt"), "bjetPtEmb")
#    jetEta(createPlot("Btagging/bjet1_eta"), "bjetEtaEmb")
    #jetPhi(createPlot("Btagging/bjet_phi"), "bjetPhiEmb")
#    numberOfJets(createPlot("Btagging/NumberOfBtaggedJets"), "NumberOfBJetsEmb")

    eventCounter = counter.EventCounter(datasets, counters=countersWeighted)
    if mcOnly:
        eventCounter.normalizeMCToLuminosity(mcLumi)
    else:
        eventCounter.normalizeMCByLuminosity()
    scaleNormalization(eventCounter)
    table = eventCounter.getMainCounterTable()
#    table = eventCounter.getSubCounterTable("Trigger")
    muonAnalysis.addSumColumn(table)
    #    muonAnalysis.reorderCounterTable(table)
#    muonAnalysis.addDataMcRatioColumn(table)
    datasets.printInfo()
    print "============================================================"
    print "Main counter (%s)" % eventCounter.getNormalizationString()
    cellFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%f'))
    print table.format(cellFormat)

    print eventCounter.getSubCounterTable("TauIDPassedEvt::tauID_HPSTight").format(cellFormat)
    print eventCounter.getSubCounterTable("TauIDPassedEvt::triggerTau_HPSTight").format(cellFormat)
#    print eventCounter.getSubCounterTable("TauIDPassedJets::tauID_HPSTight").format()
    table = eventCounter.getSubCounterTable("Trigger")
    muonAnalysis.addSumColumn(table)
    print table.format(cellFormat)

    #latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f", valueOnly=True))
    #latexFormat = counter.TableFormatConTeXtTABLE(counter.CellFormatTeX(valueFormat="%.2f", ))
#    latexFormat = counter.TableFormatLaTeX(counter.CellFormatTeX(valueFormat="%.2f"))
#    print table.format(latexFormat)

def scaleMCHisto(histo, scale):
    if histo.isMC():
        scaleHisto(histo, scale)

def scaleDataHisto(histo, scale):
    if histo.isData():
        scaleHisto(histo, scale)

def scaleHisto(histo, scale):
    th1 = histo.getRootHisto()
    th1.Scale(scale)

def scaleHistos(plot, function, scale):
    plot.histoMgr.forEachHisto(lambda histo: function(histo, scale))

def scaleCounters(eventCounter, methodName, scale):
    getattr(eventCounter, methodName)(scale)

def scaleHistosCounters(obj, plotFunc, counterFunc, scale):
    if isinstance(obj, plots.PlotBase):
        scaleHistos(obj, plotFunc, scale)
    elif isinstance(obj, counter.EventCounter):
        scaleCounters(obj, counterFunc, scale)

def scaleMCfromWmunu(obj):
    # Data/MC scale factor from AN 2011/053, BR correction factor= 1/0.6479
    rho = 0.9509/0.6479
    scaleHistosCounters(obj, scaleMCHisto, "scaleMC", rho)

def scaleTauBR(obj):
    # tau -> hadrons branching fraction
    fraction = 0.648
    scaleHistosCounters(obj, scaleHisto, "scale", fraction)

def scaleMuTriggerEff(obj):
    # muon trigger efficiency
    #data = 0.9 # this is from teh hat
    #mc = 0.9 # this is from teh hat

    #data = 1 # this is from teh hat
    #mc = 1 # this is from teh hat

    # From all
    lumis = [3.1308106110000002, 5.0948740340000001, 27.696517908000001, 5.0667150779999997, 4.6417244929999999]
    data = (lumis[0]*0.840278 + lumis[1]*0.872416 + lumis[2]*0.886409 + (lumis[3]+lumis[4])*0.872181) / sum(lumis)

    # From 2011A only
#    data = 0.872181
    mc = 0.913055

    scaleHistosCounters(obj, scaleDataHisto, "scaleData", 1/data)
    scaleHistosCounters(obj, scaleMCHisto, "scaleMC", 1/mc)

def scaleMuTriggerIdEff(obj):
    # From 2011A only
    #data = 0.508487
    #mc = 0.541083
    # May10 in 41X
    #data = 0.891379
    #mc = 0.931707
    # 1fb in 42X
    data = 0.884462
    mc = 0.919829

    scaleHistosCounters(obj, scaleDataHisto, "scaleData", 1/data)
    scaleHistosCounters(obj, scaleMCHisto, "scaleMC", 1/mc)

def scaleWmuFraction(obj):
    Wtaumu = 0.038479

    scaleHistosCounters(obj, scaleHisto, "scale", 1-Wtaumu)

class LumiScaler:
    def __init__(self, signalLumi=1, ewkLumi=1):
        self.signalLumi = signalLumi
        self.ewkLumi = ewkLumi

    def getRho(self):
        return self.signalLumi / self.ewkLumi

    def __call__(self, obj):
        scaleHistosCounters(obj, scaleHisto, "scale", self.getRho())

scaleLumi = LumiScaler()   

def scaleNormalization(obj):
    if not normalize:
        return

    #scaleMCfromWmunu(obj) # data/MC trigger correction
    scaleMuTriggerIdEff(obj)
    scaleWmuFraction(obj)
    return

    scaleMuTriggerEff(obj)
    scaleTauBR(obj)
    scaleLumi(obj)

# Helper function to flip the last two parts of the histogram name
# e.g. ..._afterTauId_DeltaPhi -> DeltaPhi_afterTauId
def flipName(name):
    if "_" in name:
        tmp = name.split("_")
        return tmp[-1] + "_" + tmp[-2]
    return name.replace("/", "_")

# Common formatting
def common(h, xlabel, ylabel):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    h.addLuminosityText()
    h.save()

# Functions below are for plot-specific formattings. They all take the
# plot object as an argument, then apply some formatting to it, draw
# it and finally save it to files.
def tauPt(h, rebin=5, ratio=True, opts={}, opts2={}):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{#tau jet} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()
    
    scaleNormalization(h)
#    h.stackMCHistograms()
#    h.addMCUncertainty()

    if h.histoMgr.hasHisto("Data"):
        th1 = h.histoMgr.getHisto("Data").getRootHisto()
        print name
        for bin in xrange(1, th1.GetNbinsX()+1):
            print "Bin %d, low edge %.0f, content %.3f" % (bin, th1.GetXaxis().GetBinLowEdge(bin), th1.GetBinContent(bin))
        print

    _opts = {"ymin": 0.01, "ymaxfactor": 2}
    _opts2 = {"ymin": 0.5, "ymax": 1.5}
    _opts.update(opts)
    _opts2.update(opts2)
    
    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=_opts, opts2=_opts2)
    else:
        h.createFrame(name, opts=_opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def tauEta(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#tau jet}"
    ylabel = "Events"
    scaleNormalization(h)
#    h.stackMCHistograms()
#    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.05, "ymax": 2.5}

    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def tauPhi(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#phi^{#tau jet}"
    ylabel = "Events"
    scaleNormalization(h)   
#    h.stackMCHistograms()
#    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
#    h.createFrame(name, opts=opts)
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend(0.2, 0.6, 0.4, 0.9))
    common(h, xlabel, ylabel)
    
def leadingTrack(h, rebin=5, ratio=True):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{leading track} (GeV/c)"
    ylabel = "Events / %.0f GeV/c" % h.binWidth()
    scaleNormalization(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}

    name = name+"_log"
    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def rtau(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "R_{#tau}"
    ylabel = "Events / %.2f" % h.binWidth()
    scaleNormalization(h)    
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 10}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    #h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def muonPt(h, rebin=5, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{#mu} (GeV/c)"
    ylabel = "Events / %.0f GeV" % h.binWidth()
    
    scaleNormalization(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def muonEta(h, rebin=5, ratio=False):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta^{#mu}"
    ylabel = "Events"
    
    scaleNormalization(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def met(h, rebin=5, ratio=True, opts={}, opts2={}):
    name = flipName(h.getRootHistoPath())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "MET (GeV)"
    if "embedding" in name:
        xlabel = "Embedded "+xlabel
    elif "original" in name:
        xlabel = "Original "+xlabel
    ylabel = "Events / %.0f GeV" % h.binWidth()

    scaleNormalization(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    _opts = {"ymin": 0.001, "ymaxfactor": 2}
    _opts2 = {"ymin": 0.5, "ymax": 1.5}

    _opts.update(opts)
    _opts2.update(opts2)

    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=_opts, opts2=_opts2)
    else:
        h.createFrame(name, opts=_opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def deltaPhi(h, rebin=40):
    name = flipName(h.getRootHistoPath())

    particle = "#tau jet"
    if "Original" in name:
        particle = "#mu"

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#Delta#phi(%s, MET) (rad)" % particle
    ylabel = "Events / %.2f rad" % h.binWidth()
    
    scaleNormalization(h)    
    h.stackMCHistograms()
    h.addMCUncertainty()

    #h.createFrameFraction(name)
    h.createFrame(name)
    h.setLegend(histograms.createLegend(0.2, 0.6, 0.4, 0.9))
    common(h, xlabel, ylabel)

def transverseMass(h, rebin=10, opts={}, opts_log={}):
    name = flipName(h.getRootHistoPath())

    particle = ""
    if "Original" in name:
        particle = "#mu"
        name = name.replace("TransverseMass", "MtOriginal")
    else:
        particle = "#tau jet"
        name = name.replace("TransverseMass", "MtEmbedding")

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "m_{T}(%s, MET) (GeV/c^{2})" % particle
    ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    
    scaleNormalization(h)   
#    h.stackMCHistograms()
#    h.addMCUncertainty()

    _opts = {"xmax": 200, "ymaxfactor": 1.5}
    _opts.update(opts)

    _opts_log = {"ymin": 1e-2, "ymaxfactor": 2}
    _opts_log.update(_opts)
    _opts_log.update(opts_log)

    #h.createFrameFraction(name, opts=opts)
    h.createFrame(name, opts=_opts)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

    name += "_log"
    h.createFrame(name, opts=_opts_log)
    h.setLegend(histograms.createLegend())
    ROOT.gPad.SetLogy(True)
    common(h, xlabel, ylabel)
    
def tauCandPt(h, name, rebin=1, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    xlabel = "p_{T}^{#tau-jet candidate} (GeV/c)"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleNormalization(h)
#    h.stackMCHistograms()
#    h.addMCUncertainty()

#    for histo in h.histoMgr.getHistos():
#        rh = histo.getRootHisto()
#        bin = 9
#        print "Bin %d, low edge %f" % (bin, rh.GetXaxis().GetBinLowEdge(bin))
#        all = rh.Integral(0, rh.GetNbinsX()+1)
#        passed = rh.Integral(bin, rh.GetNbinsX()+1)
#        print "%s: all %f, passed %f" % (histo.getName(), all, passed)
            

    opts = {"ymin": 0.01, "ymaxfactor": 5}
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

    
def tauCandEta(h, name, rebin=1, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    xlabel = "#eta^{#tau-jet candidate}" 
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleNormalization(h)
 #   h.stackMCHistograms()
 #   h.addMCUncertainty()

    opts = {"ymin": 0.1, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def tauCandPhi(h, name, rebin=1, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))

    xlabel = "#phi^{#tau-jet candidate}"
    ylabel = "Events / %.2f" % h.binWidth()
    
    scaleNormalization(h)
 #   h.stackMCHistograms()
 #   h.addMCUncertainty()

    opts = {"ymin": 1.0, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
def jetPt(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
#        name = name.replace("jetPt", "bjetPt")

    xlabel = "p_{T}^{%s} (GeV/c)" % particle
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    scaleNormalization(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.01, "ymaxfactor": 10}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name, opts=opts)
    #h.createFrameFraction(name, opts=opts)
    h.getPad().SetLogy(True)
    #h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

    
def jetEta(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
    xlabel = "#eta^{%s}" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    scaleNormalization(h)  
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 10.0, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def jetPhi(h, name, rebin=2, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "bjet" in name:
        particle = "bjet"
    xlabel = "#phi^{%s}" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    scaleNormalization(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 10.0, "ymaxfactor": 5}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)

def numberOfJets(h, name, rebin=1, ratio=True):
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    particle = "jet"
    if "Btagged" in name:
        particle = "bjet"
    xlabel = "Number of %ss" % particle
    ylabel = "Events / %.2f" % h.binWidth()
    scaleNormalization(h)
    h.stackMCHistograms()
    h.addMCUncertainty()

    opts = {"ymin": 0.0, "ymaxfactor": 1.2}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.getPad().SetLogy(True)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel)
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
