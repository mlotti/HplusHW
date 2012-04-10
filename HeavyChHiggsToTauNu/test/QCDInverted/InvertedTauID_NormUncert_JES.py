#!/usr/bin/env python
import ROOT
#ROOT.gROOT.SetBatch(True)
from ROOT import *
import math
import sys
    
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
        
analysis = "signalAnalysis"
counters = analysis+"Counters"
analysisPlusPlus   = "signalAnalysisJESPlus03eta02METPlus10"
analysisMinusPlus  = "signalAnalysisJESMinus03eta02METPlus10"
analysisPlusMinus  = "signalAnalysisJESPlus03eta02METMinus10"
analysisMinusMinus = "signalAnalysisJESMinus03eta02METMinus10"


from InvertedTauID import *

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)

    datasets.merge("EWK", [
            "TTJets",
            "WJets",   
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])

    style = tdrstyle.TDRStyle()

    metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdJets")
    metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdJets")
    metBasePP = plots.DataMCPlot(datasets, analysisPlusPlus+"/MET_BaseLineTauIdJets")
    metBaseMP = plots.DataMCPlot(datasets, analysisMinusPlus+"/MET_BaseLineTauIdJets")
    metBasePM = plots.DataMCPlot(datasets, analysisPlusMinus+"/MET_BaseLineTauIdJets")
    metBaseMM = plots.DataMCPlot(datasets, analysisMinusMinus+"/MET_BaseLineTauIdJets")


    # Rebin before subtracting
    rebin = 20
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    metBasePP.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    metBaseMP.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    metBasePM.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
    metBaseMM.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))


    metInverted_data      = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdJets")
    metBase_data          = metBase.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets")
    metBase_EWK           = metBase.histoMgr.getHisto("EWK").getRootHisto().Clone(analysis+"/MET_BaselineTauIdJets")
    metBase_EWKplusplus   = metBasePP.histoMgr.getHisto("EWK").getRootHisto().Clone(analysisPlusPlus+"/MET_BaselineTauIdJets")
    metBase_EWKminusplus  = metBaseMP.histoMgr.getHisto("EWK").getRootHisto().Clone(analysisMinusPlus+"/MET_BaselineTauIdJets")
    metBase_EWKplusminus  = metBasePM.histoMgr.getHisto("EWK").getRootHisto().Clone(analysisPlusMinus+"/MET_BaselineTauIdJets")
    metBase_EWKminusminus = metBaseMM.histoMgr.getHisto("EWK").getRootHisto().Clone(analysisMinusMinus+"/MET_BaselineTauIdJets")

    invertedQCD = InvertedTauID()

    invertedQCD.setLabel("noError")
    invertedQCD.fitQCD(metInverted_data)
    invertedQCD.fitEWK(metBase_EWK)
    invertedQCD.fitData(metBase_data)
    normalizationWithEWK = invertedQCD.getNormalization()

    invertedQCD.setLabel("plusplusError")
    invertedQCD.fitEWK(metBase_EWKplusplus)
    invertedQCD.fitData(metBase_data)
    normalizationWithEWKplusplus = invertedQCD.getNormalization()

    invertedQCD.setLabel("minusplusError")
    invertedQCD.fitEWK(metBase_EWKminusplus)
    invertedQCD.fitData(metBase_data)
    normalizationWithEWKminusplus = invertedQCD.getNormalization()

    invertedQCD.setLabel("plusminusError")
    invertedQCD.fitEWK(metBase_EWKplusminus)
    invertedQCD.fitData(metBase_data)
    normalizationWithEWKplusminus = invertedQCD.getNormalization()

    invertedQCD.setLabel("minusminusError")
    invertedQCD.fitEWK(metBase_EWKminusminus)
    invertedQCD.fitData(metBase_data)
    normalizationWithEWKminusminus = invertedQCD.getNormalization()

    invertedQCD.Summary()

    print "Difference in normalization due to JES ++ variation",(normalizationWithEWK - normalizationWithEWKplusplus)/normalizationWithEWK
    print "Difference in normalization due to JES -+ variation",(normalizationWithEWK - normalizationWithEWKminusplus)/normalizationWithEWK
    print "Difference in normalization due to JES +- variation",(normalizationWithEWK - normalizationWithEWKplusminus)/normalizationWithEWK
    print "Difference in normalization due to JES -- variation",(normalizationWithEWK - normalizationWithEWKminusminus)/normalizationWithEWK

if __name__ == "__main__":
    main()

