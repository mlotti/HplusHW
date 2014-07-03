#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the muon MC and tau MC at
# generator level. The corresponding python job configurations are
# * genMuonDebugAnalysisNtupleAOD_cfg.py
# * genTauDebugAnalysisNtuple_cfg.py
#
#
# Authors: Matti Kortelainen
#
######################################################################

import os
import array
import math
from optparse import OptionParser

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
#mcLumi = 5000.0
mcLumi = 2300.0

class MuonSelectorArgs(dataset.SelectorArgs):
    def __init__(self, **kwargs):
        dataset.SelectorArgs.__init__(self,
                                      [("puWeight", ""),
                                       ("muonEff", "Run2011A"),
                                       ], **kwargs)

class TauSelectorArgs(dataset.SelectorArgs):
    def __init__(self, **kwargs):
        dataset.SelectorArgs.__init__(self,
                                      [("puWeight", "")
                                       ], **kwargs)

def main(opts):
#    muonDir = "/opt/data/matti/embedding/v44_5/multicrab_muonDebugAnalysisNtupleAod_130507_141258"
    muonDir = "/opt/data/matti/embedding/v44_5/multicrab_muonDebugAnalysisNtupleAod_130515_104754"
    tauDir = "/opt/data/matti/embedding/v44_5/multicrab_analysisTau_v44_5_GenTauDebug_130508_123329"


    muonDatasets = dataset.getDatasetsFromMulticrabCfg(directory=muonDir, weightedCounters=False)
    tauDatasets = dataset.getDatasetsFromMulticrabCfg(directory=tauDir, weightedCounters=False)

    plots.mergeRenameReorderForDataMC(muonDatasets)
    plots.mergeRenameReorderForDataMC(tauDatasets)

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    tdrstyle.setDarkBodyRadiatorPalette()
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION
    histograms.cmsText[histograms.CMSMode.SIMULATION] = "Simulation"
    histograms.createLegend.setDefaults(y1=0.93, y2=0.8, x1=0.7, x2=0.93)

    selectorArgsMuon = MuonSelectorArgs()
    selectorArgsTau = TauSelectorArgs()

    selectorArgsMuon.set(puWeight="Run2011A")
    selectorArgsTau.set(puWeight="Run2011A")

    args = {
        "process": opts.process,
        #"maxEvents": 100,
        #"printStatus": False
    }
    ntupleCacheMuon = dataset.NtupleCache("tree", "EmbeddingDebugMuonAnalysisSelector",
                                          selectorArgs=selectorArgsMuon, cacheFileName="histogramCacheMuon.root", 
                                          macros=["rochcor_wasym_v4.C"], **args)
    ntupleCacheTau = dataset.NtupleCache("tree", "EmbeddingDebugTauAnalysisSelector",
                                         selectorArgs=selectorArgsTau, cacheFileName="histogramCacheTau.root", **args)


    doPlots(muonDatasets.getDataset("TTJets"), tauDatasets.getDataset("TTJets"), ntupleCacheMuon, ntupleCacheTau)
    doCounters(muonDatasets, tauDatasets, "TTJets", ntupleCacheMuon, ntupleCacheTau)

def doPlots(muonDataset, tauDataset, ntupleCacheMuon, ntupleCacheTau):
    def doStyle(h, color):
        th = h.getRootHisto()
        th.SetLineColor(color)
        th.SetLineWidth(3)

    global pc
    pc = 0
    
    def doPlotMuTau(quantity, step, stepTau="", **kwargs):
        if step != "":
            step = step+"_"
        if stepTau != "":
            stepTau = stepTau+"_"

        muonDrh = muonDataset.getDatasetRootHisto(ntupleCacheMuon.histogram("genmuon_"+step+quantity))
        tauDrh = tauDataset.getDatasetRootHisto(ntupleCacheTau.histogram("gentau_"+stepTau+quantity))
    
        muonDrh.setName("Muon")
        tauDrh.setName("Tau")
    
        p = plots.ComparisonPlot(muonDrh, tauDrh)
        p.histoMgr.normalizeMCToLuminosity(mcLumi)
        p.histoMgr.forHisto("Muon", lambda h: doStyle(h, ROOT.kRed))
        p.histoMgr.forHisto("Tau", lambda h: doStyle(h, ROOT.kBlue))

        args = {
            "opts2": {"ymin": 0.96, "ymax": 1.04}
        }
        args.update(kwargs)
   
        global pc
        pc += 1
        plots.drawPlot(p, ("%02d_genmuontau_"%pc)+step+quantity, xlabel="Gen "+quantity,
                       ratio=True, ratioYlabel="Muon/Tau", addLuminosityText=True, **args)
    
   
    def doPlotRecoMu(quantity, step, **kwargs):
        if step != "":
            step = step+"_"

        genDrh = muonDataset.getDatasetRootHisto(ntupleCacheMuon.histogram("genmuon_"+step+quantity))
        recoDrh = muonDataset.getDatasetRootHisto(ntupleCacheMuon.histogram("recomuon_"+step+quantity))
    
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

        global pc
        pc += 1
        plots.drawPlot(p, ("%02d_recogenmuon_"%pc)+step+quantity, xlabel="Reco/gen "+quantity,
                       ratio=True, ratioYlabel="Reco/Gen",
                       addLuminosityText=True, **args)

    def doPlotRecoMu2(quantity, step, **kwargs):
        if step != "":
            step = step+"_"

        drh = muonDataset.getDatasetRootHisto(ntupleCacheMuon.histogram("recomuon_"+step+quantity))
        p = plots.PlotBase([drh])
        p.histoMgr.normalizeMCToLuminosity(mcLumi)
        p.histoMgr.setHistoDrawStyleAll("COLZ")
        args = {
            "opts": {"ymin": -1, "ymax": 1}
        }
        args.update(kwargs)
        global pc
        pc += 1
        plots.drawPlot(p, ("%02d_recogenmuon_"%pc)+step+quantity, addLuminosityText=True, createLegend=None, backgroundColor=ROOT.kGray, **args)
        

    def doPlotRecoMuGenTau(quantity, step, stepTau="", saveCorrection=False, **kwargs):
        if step != "":
            step = step+"_"
        if stepTau != "":
            stepTau = stepTau+"_"

        muonDrh = muonDataset.getDatasetRootHisto(ntupleCacheMuon.histogram("recomuon_"+step+quantity))
        tauDrh = tauDataset.getDatasetRootHisto(ntupleCacheTau.histogram("gentau_"+stepTau+quantity))
    
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

        global pc
        pc += 1
        plots.drawPlot(p, ("%02d_recomuongentau_"%pc)+step+stepTau+quantity, xlabel="Reco/gen "+quantity,
                       ratio=True, ratioYlabel="Muon/Tau",
                       addLuminosityText=True, **args)

        if saveCorrection:
            ratio = p.ratioHistoMgr.getHistos()[0]
            tf = ROOT.TFile.Open("muonptcorrection.root", "RECREATE")
            corr = ratio.getRootHisto().Clone("correction_pt")
            for i in xrange(0, corr.GetNbinsX()+2):
                val = corr.GetBinContent(i)
                if val != 0.0:
                    corr.SetBinContent(i, 1/val)
            corr.SetDirectory(tf)
            tf.Write()
            tf.Close()
            print "Saved muon pt correction to muonptcorrection.root"

#    ptBinning = [0, 41]+range(45,120,5)+range(120,200,10)+range(200, 400, 40)+[400]
    ptBinning = [0, 5, 10, 15, 20, 25, 30, 35, 41]+range(45,120,5)+range(120,200,10)+range(200, 400, 40)+[400]
    etaBinning = [-2.1, -1.6, -1.2, -0.9, -0.6, -0.3, -0.2, 0.2, 0.3, 0.6, 0.9, 1.2, 1.6, 2.1]
    phiBinning = 2

    plots.drawPlot.setDefaults(ylabel="Events / %.1f - %.1f")
    ylabel_pt = "dEvents / dpt"

    step = ""
    doPlotMuTau("pt", step=step, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, ylabel=ylabel_pt)
    doPlotMuTau("eta", step=step)
    doPlotMuTau("phi", step=step, rebin=phiBinning)

    step = "afterRecoFound"
    opts2 = {"ymin": 0.9, "ymax": 1.05}
    doPlotMuTau("pt", step=step, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2, ylabel=ylabel_pt)
    doPlotMuTau("eta", step=step, rebin=etaBinning, opts2=opts2)
    doPlotMuTau("phi", step=step, rebin=phiBinning, opts2=opts2)

    doPlotRecoMu2("PtRes", step=step, xlabel="Reco muon pt", ylabel="(Reco pt - gen pt)/gen pt")

    step = "afterEffWeight"
    doPlotMuTau("pt", step=step, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2)
    doPlotMuTau("eta", step=step, rebin=etaBinning, opts2=opts2)
    doPlotMuTau("phi", step=step, rebin=phiBinning, opts2=opts2)

    opts2Reco = {"ymin": 0.75, "ymax": 1.1}
    doPlotRecoMu("pt", step=step, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt)
    doPlotRecoMu("eta", step=step, rebin=etaBinning)
    doPlotRecoMu("phi", step=step, rebin=phiBinning)

    doPlotRecoMuGenTau("pt", step=step, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt)
    doPlotRecoMuGenTau("eta", step=step, rebin=etaBinning)
    doPlotRecoMuGenTau("phi", step=step, rebin=phiBinning)

    stepTau = "afterMuonVeto"
    opts2Reco = {"ymin": 0.8, "ymax": 1.01}
    doPlotRecoMuGenTau("pt", step=step, stepTau=stepTau, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt, saveCorrection=True)
    doPlotRecoMuGenTau("eta", step=step, stepTau=stepTau, rebin=etaBinning)
    doPlotRecoMuGenTau("phi", step=step, stepTau=stepTau, rebin=phiBinning)

    step = "afterEffWeightScaleUp"
    doPlotRecoMuGenTau("pt", step=step, stepTau=stepTau, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt)
    doPlotRecoMuGenTau("eta", step=step, stepTau=stepTau, rebin=etaBinning)
    doPlotRecoMuGenTau("phi", step=step, stepTau=stepTau, rebin=phiBinning)

    step = "afterEffWeightScaleDown"
    doPlotRecoMuGenTau("pt", step=step, stepTau=stepTau, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt)
    doPlotRecoMuGenTau("eta", step=step, stepTau=stepTau, rebin=etaBinning)
    doPlotRecoMuGenTau("phi", step=step, stepTau=stepTau, rebin=phiBinning)

    step = "afterEffWeightMuscle"
    doPlotRecoMuGenTau("pt", step=step, stepTau=stepTau, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt)
    doPlotRecoMuGenTau("eta", step=step, stepTau=stepTau, rebin=etaBinning)
    doPlotRecoMuGenTau("phi", step=step, stepTau=stepTau, rebin=phiBinning)

    step = "afterEffWeightRochester"
    doPlotRecoMuGenTau("pt", step=step, stepTau=stepTau, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt)
    doPlotRecoMuGenTau("eta", step=step, stepTau=stepTau, rebin=etaBinning)
    doPlotRecoMuGenTau("phi", step=step, stepTau=stepTau, rebin=phiBinning)

    step = "afterEffWeightTuneP"
    doPlotRecoMuGenTau("pt", step=step, stepTau=stepTau, log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2=opts2Reco, ylabel=ylabel_pt)
    doPlotRecoMuGenTau("eta", step=step, stepTau=stepTau, rebin=etaBinning)
    doPlotRecoMuGenTau("phi", step=step, stepTau=stepTau, rebin=phiBinning)


    return

    doPlotMuEff("pt", log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1})
    doPlotMuEff("eta", rebin=etaBinning)
    doPlotMuEff("phi", rebin=phiBinning)

    doPlotRecoMuEff("pt", log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2={"ymin": 0.75, "ymax": 1.1})
    doPlotRecoMuEff("eta", rebin=etaBinning)
    doPlotRecoMuEff("phi", rebin=phiBinning)

    doPlotRecoMuGenTauEff("pt", log=True, rebin=ptBinning, divideByBinWidth=True, opts={"ymin": 0.1}, opts2={"ymin": 0.75, "ymax": 1.1})
    doPlotRecoMuGenTauEff("eta", rebin=etaBinning)
    doPlotRecoMuGenTauEff("phi", rebin=phiBinning)

def doCounters(muonDatasets, tauDatasets, datasetName, ntupleCacheMuon, ntupleCacheTau):
    ecMuon = counter.EventCounter(muonDatasets)
    #ecMuonWeighted = counter.EventCounter(muonDatasets, counters="counters/weighted")
    ecTau = counter.EventCounter(tauDatasets)

    def isNotThis(name):
        return name != datasetName

    ecMuon.removeColumns(filter(isNotThis, muonDatasets.getAllDatasetNames()))
    #ecMuonWeighted.removeColumns(filter(isNotThis, muonDatasets.getAllDatasetNames()))
    ecTau.removeColumns(filter(isNotThis, tauDatasets.getAllDatasetNames()))

    ecMuon.normalizeMCToLuminosity(mcLumi)
    #ecMuonWeighted.normalizeMCToLuminosity(mcLumi)
    ecTau.normalizeMCToLuminosity(mcLumi)

    ecMuon.getMainCounter().appendRows(ntupleCacheMuon.histogram("counters/weighted/counter"))
    ecTau.getMainCounter().appendRows(ntupleCacheTau.histogram("counters/weighted/counter"))

    table = counter.CounterTable()
    muonCol = ecMuon.getMainCounterTable().getColumn(name=datasetName)
    muonCol.setName("Muon")
    #col.setCount(-1, ecMuonWeighted.getMainCounterTable().getCount(irow=-1, colName=datasetName))
    table.appendColumn(muonCol)
    tauCol = ecTau.getMainCounterTable().getColumn(name=datasetName)
    tauCol.setName("Tau")
    table.appendColumn(tauCol)

    print table.format()

    def printRatio(muonCount, tauCount):
        ratio1 = tauCol.getCount(name=tauCount).clone()
        ratio1.divide(muonCol.getCount(name=muonCount))

        ratio2 = muonCol.getCount(name=muonCount).clone()
        ratio2.divide(tauCol.getCount(name=tauCount))

        print "Tau/Muon = %f +- %f, Muon/Tau = %f +- %f" % (ratio1.value(), ratio1.uncertainty(), ratio2.value(), ratio2.uncertainty())

    print "Generator level"
    printRatio("= 1 gen muon", "= 1 gen tau")
    print

    print "Reco muon vs. gen tau, after muon veto"
    printRatio("muon id eff weighting", "reco muon veto")

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--process", dest="process", default=False, action="store_true",
                      help="Process ntuples")
    (opts, args) = parser.parse_args()
    main(opts)
