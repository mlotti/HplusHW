#!/usr/bin/env python

import os
import sys
import re
import ROOT
import array

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms

from plotTauLegEfficiency import getEfficiency,convert2TGraph,Print
from PythonWriter import PythonWriter
pythonWriter = PythonWriter()

ROOT.gROOT.SetBatch(True)
plotDir = "METLeg2016"

formats = [".pdf",".png"]

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

def main():

    if len(sys.argv) < 2:
        usage()

    analyze()


def analyze(analysis=None):

    paths = [sys.argv[1]]

    if not analysis == None:
        datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis)
    else:
        datasets = dataset.getDatasetsFromMulticrabDirs(paths)
        analysis = datasets.getAllDatasets()[0].getAnalysisName()

    analysisList = []
#    analysisList.append("METLeg_2016MET80_MET80")
#    analysisList.append("METLeg_2016ICHEP_MET90")
#    analysisList.append("METLeg_2016_MET90")

    met_re = re.compile("_(?P<met>MET\d+)$")
    if True:
    #for analysis in analysisList:

        met = "METX"
        met_match = met_re.search(analysis)
        if met_match:
            met = met_match.group("met")

        datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis)
#    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,includeOnlyTasks="Tau\S+25ns$|TTJets$")
#        datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,excludeTasks="Tau_Run2015C|Tau\S+25ns_Silver$|DYJetsToLL|WJetsToLNu$")
#    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,includeOnlyTasks="Tau_Run2015D_PromptReco_v4_246908_260426_25ns$|DYJetsToLL_M_50$")
#    datasetsMC = None
        datasetsMC = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,excludeTasks="Tau_")

        for d in datasets.getAllDatasets():
            print d.getName()
            style = tdrstyle.TDRStyle()

            dataset1 = datasets.getDataDatasets()
            dataset2 = dataset1
            createRatio = False
            if isinstance(datasetsMC,dataset.DatasetManager):
                dataset2 = datasetsMC.getMCDatasets()
                createRatio = True

        eff1_MET80 = getEfficiency(dataset1)
        eff2_MET80 = getEfficiency(dataset2)

        styles.dataStyle.apply(eff1_MET80)
        eff1_MET80.SetMarkerSize(1)
        if createRatio:
            styles.mcStyle.apply(eff2_MET80)
            eff2_MET80.SetMarkerSize(1.5)

        if createRatio:
            p = plots.ComparisonPlot(histograms.HistoGraph(eff1_MET80, "eff1_MET80", "p", "P"),
                                     histograms.HistoGraph(eff2_MET80, "eff2_MET80", "p", "P"))
        else:
            p = plots.PlotBase([histograms.HistoGraph(eff1_MET80, "eff1_MET80", "p", "P")])

        opts = {"ymin": 0, "ymax": 1.1}
        opts2 = {"ymin": 0.5, "ymax": 1.5}
        moveLegend = {"dx": -0.55, "dy": -0.15}

        name = "TauMET_"+analysis+"_DataVsMC_PFMET"

        legend1 = "Data"
        #    legend2 = "MC (TTJets)"
        legend2 = "MC"

        if createRatio:
            p.histoMgr.setHistoLegendLabelMany({"eff1_MET80": legend1, "eff2_MET80": legend2})
            p.createFrame(os.path.join(plotDir, name), createRatio=True, opts=opts, opts2=opts2)
        else:
            p.histoMgr.setHistoLegendLabelMany({"eff1_MET80": legend1})
            p.createFrame(os.path.join(plotDir, name), opts=opts, opts2=opts2)

        p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

        p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
        p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
        if createRatio:
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        histograms.addText(0.2, 0.6, "LooseIsoPFTau50_Trk30_eta2p1_"+met, 17)
        #    histograms.addText(0.2, 0.53, analysis.split("_")[len(analysis.split("_")) -1], 17)
        label = analysis.split("_")[1]
        histograms.addText(0.2, 0.53, label, 17)
        runRange = datasets.loadRunRange()
        histograms.addText(0.2, 0.46, "Runs "+runRange, 17)

        p.draw()
        lumi = 0.0
        for d in datasets.getDataDatasets():
            print "luminosity",d.getName(),d.getLuminosity()
            lumi += d.getLuminosity()
        print "luminosity, sum",lumi
        histograms.addStandardTexts(lumi=lumi)

        if not os.path.exists(plotDir):
            os.mkdir(plotDir)
        p.save(formats)

        pythonWriter.addParameters(plotDir,label,runRange,lumi,eff1_MET80)
        pythonWriter.addMCParameters(label,eff2_MET80)

    pythonWriter.writeJSON(os.path.join(plotDir,"metLegTriggerEfficiency_"+label+".json"))

    #########################################################################                                             

    eff1phi = getEfficiency(dataset1,"NumeratorPhi","DenominatorPhi")
    eff2phi = getEfficiency(dataset2,"NumeratorPhi","DenominatorPhi")

    styles.dataStyle.apply(eff1phi)
    styles.mcStyle.apply(eff2phi)
    eff1phi.SetMarkerSize(1)

    if isinstance(datasetsMC,dataset.DatasetManager):
        p_phi = plots.ComparisonPlot(histograms.HistoGraph(eff1phi, "eff1phi", "p", "P"),
                                     histograms.HistoGraph(eff2phi, "eff2phi", "p", "P"))
    else:
        p_phi = plots.PlotBase([histograms.HistoGraph(eff1phi, "eff1phi", "p", "P")])

    p_phi.histoMgr.setHistoLegendLabelMany({"eff1phi": legend1})
    if isinstance(datasetsMC,dataset.DatasetManager):
        p_phi.histoMgr.setHistoLegendLabelMany({"eff1phi": legend1, "eff2phi": legend2})

    opts = {"ymin": 0, "ymax": 0.1}
    name = "TauMET_"+analysis+"_DataVsMC_PFMETPhi"

    if createRatio:
        p_phi.createFrame(os.path.join(plotDir, name), createRatio=createRatio, opts=opts, opts2=opts2)
    else:
        p_phi.createFrame(os.path.join(plotDir, name), opts=opts, opts2=opts2)

    moveLegendPhi = {"dx": -0.5, "dy": -0.6, "dh": -0.1}
    p_phi.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegendPhi))

    p_phi.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p_phi.getFrame().GetXaxis().SetTitle("MET Type 1 #phi")
    if createRatio:
        p_phi.getFrame2().GetYaxis().SetTitle("Ratio")
        p_phi.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.4, 0.86, "LooseIsoPFTau50_Trk30_eta2p1_MET80", 17)
    histograms.addText(0.4, 0.78, analysis.split("_")[len(analysis.split("_")) -1], 17)
    histograms.addText(0.4, 0.71, "Runs "+datasets.loadRunRange(), 17)

    p_phi.draw()
    histograms.addStandardTexts(lumi=lumi)

    p_phi.save(formats)

    #########################################################################                                             
    """
    #### MET120

    analysis = "METLeg_2015CD_MET120"
    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis)
    for d in datasets.getAllDatasets():
        print d.getName()
    style = tdrstyle.TDRStyle()

    dataset1 = datasets.getDataDatasets()
    dataset2 = datasets.getMCDatasets()

    eff1_MET120 = getEfficiency(dataset1)
    eff2_MET120 = getEfficiency(dataset2)

    styles.dataStyle.apply(eff1_MET120)
    styles.mcStyle.apply(eff2_MET120)
    eff1_MET120.SetMarkerSize(1)
    eff2_MET120.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff1_MET120, "eff1_MET120", "p", "P"),
                             histograms.HistoGraph(eff2_MET120, "eff2_MET120", "p", "P"))

    opts = {"ymin": 0, "ymax": 1.1}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
    moveLegend = {"dx": -0.55, "dy": -0.15}

    name = "DataVsMC_L1HLTMET_PFMET_MET120"

    legend1 = "Data"
    legend2 = "MC"
    p.histoMgr.setHistoLegendLabelMany({"eff1_MET120": legend1, "eff2_MET120": legend2})

    p.createFrame(os.path.join(plotDir, name), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 0.0
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)
    """

    # CaloMET
    """
    #### MET80

    analysisc = "METLeg_2016B_CaloMET_MET80"
    datasetsc = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysisc)
    datasetsc = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysisc,excludeTasks="Tau\S+25ns_Silver$")
#    datasetsc = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysisc,includeOnlyTasks="Tau\S+25ns$|TTJets$")

    style = tdrstyle.TDRStyle()

    dataset1c = datasetsc.getDataDatasets()
    dataset2c = datasetsc.getMCDatasets()

#    eff1c_MET80 = getEfficiency(dataset1c)
    eff2c_MET80 = getEfficiency(dataset2c)

#    styles.dataStyle.apply(eff1c_MET80)
    styles.mcStyle.apply(eff2c_MET80)
#    eff1c_MET80.SetMarkerSize(1)
    eff2c_MET80.SetMarkerSize(1.5)
    eff2c_MET80.SetMarkerColor(4)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff2_MET80, "eff2_MET80", "p", "P"),
                             histograms.HistoGraph(eff2c_MET80, "eff2c_MET80", "p", "P"))

    namec = "TauMET_"+analysis+"_MC_TrgBitVsCaloMET80_PFMET"

    legend1c = "MC, trigger bit"
    legend2c = "MC, CaloMET > 80"
    p.histoMgr.setHistoLegendLabelMany({"eff2_MET80": legend1c, "eff2c_MET80": legend2c})

    p.createFrame(os.path.join(plotDir, namec), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 0.0
    for d in datasets.getDataDatasets():
        print "luminosity",d.getName(),d.getLuminosity()
        lumi += d.getLuminosity()
    print "luminosity, sum",lumi
    histograms.addStandardTexts(lumi=lumi)
    histograms.addText(0.2, 0.6, "LooseIsoPFTau50_Trk30_eta2p1_MET80", 17)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)
    """
    """
    #### MET120 

    analysisc = "METLeg_2015A_CaloMET_MET120"
    datasetsc = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysisc)

    style = tdrstyle.TDRStyle()

    dataset1c = datasetsc.getDataDatasets()
    dataset2c = datasetsc.getMCDatasets()

    eff1c_MET120 = getEfficiency(dataset1c)
    eff2c_MET120 = getEfficiency(dataset2c)

    styles.dataStyle.apply(eff1c_MET120)
    styles.mcStyle.apply(eff1c_MET120)
    eff1c_MET120.SetMarkerSize(1)
    eff2c_MET120.SetMarkerSize(1.5)

    p = plots.ComparisonPlot(histograms.HistoGraph(eff2_MET120, "eff2_MET120", "p", "P"),
                             histograms.HistoGraph(eff2c_MET120, "eff2c_MET120", "p", "P"))

    namec = "MC_TrgBitVsCaloMET120_L1HLTMET_PFMET"

    legend1c = "MC, trigger bit"
    legend2c = "MC, CaloMET > 120"
    p.histoMgr.setHistoLegendLabelMany({"eff2_MET120": legend1c, "eff2c_MET120": legend2c})

    p.createFrame(os.path.join(plotDir, namec), createRatio=True, opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(y1=0.8), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    p.getFrame().GetXaxis().SetTitle("MET Type 1 (GeV)")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    p.draw()
    lumi = 0.0
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)
    """

    #########################################################################                                                                                                                             

    namePU = "TauMET_"+analysis+"_DataVsMC_nVtx"

    eff1PU = getEfficiency(dataset1,"NumeratorPU","DenominatorPU")
    eff2PU = getEfficiency(dataset2,"NumeratorPU","DenominatorPU")

    styles.dataStyle.apply(eff1PU)
    styles.mcStyle.apply(eff2PU)
    eff1PU.SetMarkerSize(1)
    eff2PU.SetMarkerSize(1.5)

    if isinstance(datasetsMC,dataset.DatasetManager):
        pPU = plots.ComparisonManyPlot(histograms.HistoGraph(eff1PU, "eff1", "p", "P"),
                                      [histograms.HistoGraph(eff2PU, "eff2", "p", "P")])
        pPU.histoMgr.setHistoLegendLabelMany({"eff1": legend1, "eff2": legend2})
    else:
        pPU = plots.PlotBase([histograms.HistoGraph(eff1PU, "eff1", "p", "P")])
        pPU.histoMgr.setHistoLegendLabelMany({"eff1": legend1})


    opts = {"ymin": 0.001, "ymax": 0.1}
    moveLegend = {"dx": -0.5, "dy": -0.1, "dh": -0.1}
    if createRatio:
        pPU.createFrame(os.path.join(plotDir, namePU), createRatio=True, opts=opts, opts2=opts2)
    else:
        pPU.createFrame(os.path.join(plotDir, namePU), opts=opts, opts2=opts2)
    pPU.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
#    if createRatio:
#        pPU.getPad1().SetLogy(True)
#    else:
#        pPU.getPad().SetLogy(True)

    pPU.getFrame().GetYaxis().SetTitle("L1+HLT MET efficiency")
    pPU.getFrame().GetXaxis().SetTitle("Number of reco vertices")
    if createRatio:
        pPU.getFrame2().GetYaxis().SetTitle("Ratio")
        pPU.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.4, 0.85, "LooseIsoPFTau50_Trk30_eta2p1_MET80", 17)
    histograms.addText(0.4, 0.78, analysis.split("_")[len(analysis.split("_")) -1], 17)
    histograms.addText(0.4, 0.71, "Runs "+datasets.loadRunRange(), 17)

    pPU.draw()
    histograms.addStandardTexts(lumi=lumi)

    pPU.save(formats)

    print "Output written in",plotDir

if __name__ == "__main__":
    main()
