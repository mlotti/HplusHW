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
counters = analysis+"Counters/weighted"

# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    datasets.remove(["WJets_TuneD6T_Winter10", "TTJets_TuneD6T_Winter10",
                     "TTToHplusBWB_M140_Spring11","TTToHplusBWB_M80_Spring11","TTToHplusBWB_M90_Spring11",
                   "TTToHplusBWB_M155_Spring11","TTToHplusBWB_M150_Spring11","TTToHplusBWB_M160_Spring11","TTToHplusBWB_M100_Spring11",
                    "TTToHplusBHminusB_M80_Spring11","TTToHplusBHminusB_M100_Spring11","TTToHplusBHminusB_M160_Spring11",
                     "TTToHplusBHminusB_M150_Spring11","TTToHplusBHminusB_M140_Spring11","TTToHplusBHminusB_M155_Spring11", "TauPlusX_160431-161016_Prompt","TauPlusX_162803-162828_Prompt",
                     "QCD_Pt30to50_TuneZ2_Spring11","QCD_Pt50to80_TuneZ2_Spring11","QCD_Pt80to120_TuneZ2_Spring11",
                     "QCD_Pt120to170_TuneZ2_Spring11","QCD_Pt170to300_TuneZ2_Spring11","QCD_Pt300to470_TuneZ2_Spring11",
#                     "Tau_165970-166164_Prompt", "Tau_166374-167043_Prompt", "Tau_167078-167784_Prompt", "Tau_165088-165633_Prompt"
#                     "Tau_163270-163869_May10","Tau_161217-163261_May10", "Tau_160431-161176_May10"
                     ])
                     

    
    
    datasets.loadLuminosities()

    # Take signals from 42X
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    
    datasets.remove(["QCD_Pt30to50_TuneZ2_Summer11","QCD_Pt50to80_TuneZ2_Summer11","QCD_Pt80to120_TuneZ2_Summer11",
                     "QCD_Pt120to170_TuneZ2_Summer11","QCD_Pt170to300_TuneZ2_Summer11","QCD_Pt300to470_TuneZ2_Summer11",
                     "WJets_TuneZ2_Summer11", "TTJets_TuneZ2_Summer11", "DYJetsToLL_M50_TuneZ2_Summer11", "Tau_160431-161176_May10",                                                            
                     "Tau_161119-161119_May10_Wed", "Tau_161217-163261_May10", "Tau_163270-163869_May10",
                     "Tau_165088-165633_Prompt", "Tau_165103-165103_Prompt_Wed", "Tau_165970-166164_Prompt",
                     "Tau_166346-166346_Prompt", "Tau_166374-167043_Prompt", "Tau_167078-167784_Prompt",
                     "Tau_167786-167913_Prompt_Wed"
                     ])
    datasetsSignal = dataset.getDatasetsFromMulticrabCfg(cfgfile="multicrab.cfg", counters=counters)

    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    
    datasets_tm = datasets.deepCopy()
    
    genTopPt(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genTopPt", normalizeByCrossSection=True), "genTopPt")
    genTopPt(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genTopPt_wrongB", normalizeByCrossSection=True), "genTopPt_wrongB")
    genBquark_Eta(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genBquark_FromTop_Eta", normalizeByCrossSection=True), "genBquark_FromTop_Eta")
    genBquark_Eta(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genBquark_NotFromTop_Eta", normalizeByCrossSection=True), "genBquark_NotFromTop_Eta")
    genBquark_Pt(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genBquark_FromTop_Pt", normalizeByCrossSection=True), "genBquark_FromTop_Pt")
    genBquark_Pt(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genBquark_NotFromTop_Pt", normalizeByCrossSection=True), "genBquark_NotFromTop_Pt")
    genBquark_DeltaRTau(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genBquark_FromTop_DeltaRTau", normalizeByCrossSection=True), "genBquark_FromTop_DeltaRTau")
    genBquark_DeltaRTau(plots.MCPlot(datasets, analysis+"/GenParticleAnalysis/genBquark_NotFromTop_DeltaRTau", normalizeByCrossSection=True), "genBquark_NotFromTop_DeltaRTau")
 
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
    
def genTopPt(h, name, rebin=10, ratio=False):
    h.histoMgr.forEachHisto(styles.generator())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{top} (GeV/c)"
    ylabel = "Events /%.0f GeV/c" % h.binWidth()
    
    opts = {"ymin": 0.0001, "xmax": 600, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    h.getPad().SetLogy(False)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel, False)
    
def genBquark_Eta(h, name, rebin=10, ratio=False):
    h.histoMgr.forEachHisto(styles.generator())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#eta"
    ylabel = "Events /%.2f" % h.binWidth()
    
    opts = {"ymin": 0.0001, "xmin": -6, "xmax": 6, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    h.getPad().SetLogy(False)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel, False)
    
def genBquark_Pt(h, name, rebin=5, ratio=False):
    h.histoMgr.forEachHisto(styles.generator())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "p_{T}^{top} (GeV/c)"
    ylabel = "Events /%.1f GeV/c" % h.binWidth()
    
    opts = {"ymin": 0.0001, "xmax": 400, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    h.getPad().SetLogy(False)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel, False)
    
def genBquark_DeltaRTau(h, name, rebin=10, ratio=False):
    h.histoMgr.forEachHisto(styles.generator())
    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    xlabel = "#Delta_{R} to #tau"
    ylabel = "Events /%.2f" % h.binWidth()
    
#    scaleMCfromWmunu(h)  

    opts = {"ymin": 0.0001, "xmax": 8, "ymaxfactor": 1.1}
    opts2 = {"ymin": 0.01, "ymax": 1.5}
#    name = name+"_log"
    if ratio:
        h.createFrameFraction(name, opts=opts, opts2=opts2)
    else:
        h.createFrame(name, opts=opts)
#    h.createFrame(name)
    h.getPad().SetLogy(False)
    h.setLegend(histograms.createLegend())
    common(h, xlabel, ylabel, False)
    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
