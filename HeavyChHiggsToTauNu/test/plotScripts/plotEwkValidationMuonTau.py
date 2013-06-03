#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the muon MC and tau MC at
# generator level. The corresponding python job configurations are
# * genMuonDebugAnalysis_cfg.py
# * genMuonDebugAnalysisAOD_cfg.py
# * genTauDebugAnalysis_cfg.py
#
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import array
import math

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

#mcLumi = 5049.0
mcLumi = 5000.0

jetSelection = False
#jetSelection = True

def main():
#    muonDir = "../multicrab_muonDebugAnalysisAod_130503_112555"
#    muonDir = "../multicrab_muonDebugAnalysisAod_pt41_130506_124929"
    muonDir = "../multicrab_muonDebugAnalysisAod_pt41_muscle_pu_130506_163909"
    tauDir = "."

    if jetSelection:
        muonDir = "../multicrab_muonAnalysis_GenMuonDebug_130506_155845"
    

    args = {
        "analysisName": "debugAnalyzer",
        "dataEra": "Run2011A"
    }
    muArgs = {}
    muArgs.update(args)
    #muArgs["analysisName"] =  "debugAnalyzerMuscle"

    muonDatasets = dataset.getDatasetsFromMulticrabCfg(directory=muonDir, weightedCounters=False, **muArgs)
    tauDatasets = dataset.getDatasetsFromMulticrabCfg(directory=tauDir, weightedCounters=False, **args)

    plots.mergeRenameReorderForDataMC(muonDatasets)
    plots.mergeRenameReorderForDataMC(tauDatasets)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.cmsText[histograms.CMSMode.SIMULATION] = "Simulation"
    histograms.createLegend.setDefaults(y1=0.93, y2=0.8, x1=0.82, x2=0.93)

    doPlots(muonDatasets.getDataset("TTJets"), tauDatasets.getDataset("TTJets"))
    doCounters(muonDatasets, tauDatasets, "TTJets")

def doPlots(muonDataset, tauDataset):
    def doStyle(h, color):
        th = h.getRootHisto()
        th.SetLineColor(color)
        th.SetLineWidth(3)
    
    def doPlotMuTau(quantity, **kwargs):
        muonDrh = muonDataset.getDatasetRootHisto("genmuon_"+quantity)
        tauDrh = tauDataset.getDatasetRootHisto("gentau_"+quantity)
    
        muonDrh.setName("Muon")
        tauDrh.setName("Tau")
    
        p = plots.ComparisonPlot(muonDrh, tauDrh)
        p.histoMgr.normalizeMCToLuminosity(mcLumi)
        p.histoMgr.forHisto("Muon", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Tau", lambda h: doStyle(h, ROOT.kBlue))
    
        plots.drawPlot(p, "genmuontau_"+quantity, xlabel="Gen "+quantity, ylabel="Events / %.2f",
                       ratio=True, ratioYlabel="Muon/Tau", opts2={"ymin": 0.96, "ymax": 1.04},
                       addLuminosityText=True, **kwargs)
    
    def doPlotMuEff(quantity, **kwargs):
        genDrh = muonDataset.getDatasetRootHisto("genmuon_"+quantity)
        idDrh = muonDataset.getDatasetRootHisto("genmuon_afterjet_"+quantity) # this has 1/eff normalization, but no jet selection despite its name
    
        genDrh.setName("Gen")
        idDrh.setName("Identified")
    
        p = plots.ComparisonPlot(idDrh, genDrh)
        p.histoMgr.normalizeMCToLuminosity(mcLumi)
        p.histoMgr.forHisto("Identified", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Gen", lambda h: doStyle(h, ROOT.kBlue))
    
        plots.drawPlot(p, "genmuon_id_"+quantity, xlabel="Gen "+quantity, ylabel="Events / %.2f",
                       ratio=True, ratioYlabel="ID'd/Gen", opts2={"ymin": 0.9, "ymax": 1.1},
                       addLuminosityText=True, **kwargs)
    
    def doPlotRecoMuEff(quantity, **kwargs):
        # this has 1/eff normalization, but no jet selection despite its name
        genDrh = muonDataset.getDatasetRootHisto("genmuon_afterjet_"+quantity)
        recoDrh = muonDataset.getDatasetRootHisto("recomuon_afterjet_"+quantity)
    
        genDrh.setName("Gen")
        recoDrh.setName("Reco")
    
        p = plots.ComparisonPlot(recoDrh, genDrh)
        p.histoMgr.normalizeMCToLuminosity(mcLumi)
        p.histoMgr.forHisto("Reco", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Gen", lambda h: doStyle(h, ROOT.kBlue))
    
        args = {
            "opts2": {"ymin": 0.9, "ymax": 1.1}
        }
        args.update(kwargs)

        plots.drawPlot(p, "recogenmuon_id_"+quantity, xlabel="Reco/gen "+quantity, ylabel="Events / %.2f",
                       ratio=True, ratioYlabel="Reco/Gen",
                       addLuminosityText=True, **args)

    def doPlotRecoMuGenTauEff(quantity, **kwargs):
        # this has 1/eff normalization, but no jet selection despite its name
        muonDrh = muonDataset.getDatasetRootHisto("recomuon_afterjet_"+quantity)
        tauDrh = tauDataset.getDatasetRootHisto("gentau_"+quantity)
    
        muonDrh.setName("Muon (reco)")
        tauDrh.setName("Tau (gen)")
    
        p = plots.ComparisonPlot(muonDrh, tauDrh)
        p.histoMgr.normalizeMCToLuminosity(mcLumi)
        p.histoMgr.forHisto("Muon (reco)", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Tau (gen)", lambda h: doStyle(h, ROOT.kBlue))
    
        args = {
            "opts2": {"ymin": 0.9, "ymax": 1.1}
        }
        args.update(kwargs)

        plots.drawPlot(p, "recomuongentau_id_"+quantity, xlabel="Reco/gen "+quantity, ylabel="Events / %.2f",
                       ratio=True, ratioYlabel="Muon/Tau",
                       addLuminosityText=True, **args)


    ptBinning = [0, 41]+range(45,120,5)+range(120,200,10)+range(200, 400, 40)+[400]
    etaBinning = [-2.1, -1.6, -1.2, -0.9, -0.6, -0.3, -0.2, 0.2, 0.3, 0.6, 0.9, 1.2, 1.6, 2.1]
    phiBinning = 2

    if not jetSelection:
        doPlotMuTau("pt", log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1})
        doPlotMuTau("eta")
        doPlotMuTau("phi", rebin=phiBinning)

        doPlotMuEff("pt", log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1})
        doPlotMuEff("eta", rebin=etaBinning)
        doPlotMuEff("phi", rebin=phiBinning)

        doPlotRecoMuEff("pt", log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2={"ymin": 0.75, "ymax": 1.1})
        doPlotRecoMuEff("eta", rebin=etaBinning)
        doPlotRecoMuEff("phi", rebin=phiBinning)

    doPlotRecoMuGenTauEff("pt", log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2={"ymin": 0.75, "ymax": 1.1})
    doPlotRecoMuGenTauEff("eta", rebin=etaBinning)
    doPlotRecoMuGenTauEff("phi", rebin=phiBinning)

def doCounters(muonDatasets, tauDatasets, datasetName):
    ecMuon = counter.EventCounter(muonDatasets)
    ecMuonWeighted = counter.EventCounter(muonDatasets, counters="counters/weighted")
    ecTau = counter.EventCounter(tauDatasets)

    def isNotThis(name):
        return name != datasetName

    ecMuon.removeColumns(filter(isNotThis, muonDatasets.getAllDatasetNames()))
    ecMuonWeighted.removeColumns(filter(isNotThis, muonDatasets.getAllDatasetNames()))
    ecTau.removeColumns(filter(isNotThis, tauDatasets.getAllDatasetNames()))

    ecMuon.normalizeMCToLuminosity(mcLumi)
    ecMuonWeighted.normalizeMCToLuminosity(mcLumi)
    ecTau.normalizeMCToLuminosity(mcLumi)

    table = counter.CounterTable()
    col = ecMuon.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Muon")
    col.setCount(-1, ecMuonWeighted.getMainCounterTable().getCount(irow=-1, colName=datasetName))
    muonEvents = col.getCount(name="= 1 gen muon").clone()
    muonEventsWeighted = col.getCount(-1).clone()
    table.appendColumn(col)
    col = ecTau.getMainCounterTable().getColumn(name=datasetName)
    col.setName("Tau")
    tauEvents = col.getCount(-1).clone()
    table.appendColumn(col)

    print table.format()

    ratio = tauEvents.clone()
    ratio.divide(muonEvents)
    ratioWeighted = tauEvents.clone()
    ratioWeighted.divide(muonEventsWeighted)
    print "Tau/Muon     = %f +- %f" % (ratio.value(), ratio.uncertainty())
    print "Tau/Muon(ID) = %f +- %f" % (ratioWeighted.value(), ratioWeighted.uncertainty())
    print

    ratio = muonEvents.clone()
    ratio.divide(tauEvents)
    ratioWeighted = muonEventsWeighted.clone()
    ratioWeighted.divide(tauEvents)
    print "Muon/Tau     = %f +- %f" % (ratio.value(), ratio.uncertainty())
    print "Muon(ID)/Tau = %f +- %f" % (ratioWeighted.value(), ratioWeighted.uncertainty())



if __name__ == "__main__":
    main()
