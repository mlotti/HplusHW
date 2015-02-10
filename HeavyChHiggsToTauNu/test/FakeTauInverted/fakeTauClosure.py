#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *
import math
import sys
import os
import re
import array
import datetime

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics
import HiggsAnalysis.HeavyChHiggsToTauNu.qcdInverted.fakeRateWeighting as fakeRateWeighting
import HiggsAnalysis.HeavyChHiggsToTauNu.qcdInverted.qcdInvertedResult as qcdInvertedResult

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

era = "Run2012ABCD"
searchMode = "Light"

drawPlot1 = plots.PlotDrawer(
    ylabel = "w",
    cmsTextPosition="left", 
    createLegend=None,
)

drawPlot2 = plots.PlotDrawer(
    ylabel="Fake rate probability",
    cmsTextPosition="left",
    moveLegend={"dx": -0.07,"dy": 0.0},
    opts={"ymin": 0.0, "ymax": 0.2},
)

try:
    import QCDInvertedNormalizationFactors
except ImportError:
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_FakeTauNormalization.py to generate QCDInvertedNormalizationFactors.py"
    print

# refine the datasets given in the multicrab directories
def refinedDataSets(dirs, dataEra, searchMode, analysis, optMode, removeTT):
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)

    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()

    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets.getAllDatasetNames()))
    if removeTT:
        datasets.remove(filter(lambda name: "TTJets_SemiLept" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "TTJets_FullLept" in name, datasets.getAllDatasetNames()))
        datasets.remove(filter(lambda name: "TTJets_Hadronic" in name, datasets.getAllDatasetNames()))

    plots.mergeRenameReorderForDataMC(datasets)

    datasets.merge("EWK", [
        "TTJets",
        "WJets",
        "DYJetsToLL",
        "SingleTop",
        "Diboson"
        ])

    return datasets

# remove sample labels from dictionary keys
def getSimplifiedFactorDict(dictionary, samplename):
    simplified_dict = {}
    for key in dictionary.keys():
        if samplename in key:
            simplified_dict[key.replace(samplename,"")] = dictionary[key]
    return simplified_dict

def getNormalization(bin, w, normalization):
    if w != 1:
        norm = w*normalization[bin+"QCD"] + (1-w)*normalization[bin+"EWK_FakeTaus"]
    else:
        norm = w*normalization[bin+"QCD"]
    return norm

# plot MC vs data
def plotClosure(mt_nom, mt_var, name, optMode):
    style = tdrstyle.TDRStyle() 
    plot = plots.ComparisonPlot(mt_var, mt_nom)
    plot.createFrame(optMode.replace("Opt","mT_Closure_"+ name +"_"), createRatio=True, opts2={"ymin": 0.73, "ymax": 1.27})
    plot.frame.GetXaxis().SetTitle("m_{T}(tau,MET), GeV")
    plot.frame.GetYaxis().SetTitle("#LT Events / bin #GT")
    moveLegend={"dx": -0.3,"dy": 0.04}
    plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    histograms.addStandardTexts()
    plot.draw()
    plot.save()

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <multicrab dir>"
    print
    sys.exit()

def main():
    myShapeString = "shapeTransverseMass"
    myEWKfakeShapeString = "shapeEWKFakeTausTransverseMass"

    optimizationMode = "OptQCDTailKillerLoosePlus"
    myModuleInfoString = "%s_%s_%s"%(era, searchMode, optimizationMode)

    defaultBinning = [0,20,40,60,80,100,120,140,160,200,400]
    myBaselineMulticrabDir = "/mnt/flustre/epekkari/signal_2014-07-01_nominal"
    myInvertedMulticrabDir = "/mnt/flustre/epekkari/FixedBugsQCDPlusEWKFakeTau_140919_164308"
    
    # Inverted datasets
    dsetMgrCreator = dataset.readFromMulticrabCfg(directory=myInvertedMulticrabDir)
    dsetMgr = dsetMgrCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
    # Do the usual normalisation
    dsetMgr.updateNAllEventsToPUWeighted()
    dsetMgr.loadLuminosities()
    plots.mergeRenameReorderForDataMC(dsetMgr)
    dsetMgr.merge("EWK", ["TTJets","WJets","DYJetsToLL","SingleTop","Diboson"])
    # Obtain luminosity
    myLuminosity = dsetMgr.getDataset("Data").getLuminosity()

    # Fake rate weighting
    myFakeRateWeightCalculator = fakeRateWeighting.FakeRateWeightCalculator(dsetMgr, myShapeString, QCDInvertedNormalizationFactors.QCDInvertedNormalization, myLuminosity)

    # QCD normalization factors
    qcd_norm = getSimplifiedFactorDict(QCDInvertedNormalizationFactors.QCDInvertedNormalization, "QCD")
    
    # Convert from inverted to baseline
    qcdShape = qcdInvertedResult.QCDInvertedShape(myFakeRateWeightCalculator.getQCDShape(), myModuleInfoString, qcd_norm, optionPrintPurityByBins=False, optionDoNQCDByBinHistograms=False)
    fakeTauShape = qcdInvertedResult.QCDInvertedShape(myFakeRateWeightCalculator.getFakeTauShape(), myModuleInfoString, myFakeRateWeightCalculator.getTotalFakeRateProbabilities(), optionPrintPurityByBins=False, optionDoNQCDByBinHistograms=False)

    qcd_mt = qcdShape.getResultShape()
    fakeTau_mt = fakeTauShape.getResultShape()

    datasets_baseline = refinedDataSets([myBaselineMulticrabDir], era, searchMode, "signalAnalysis", optimizationMode, False)
    MCfake_mt_plot = plots.DataMCPlot(datasets_baseline, myEWKfakeShapeString)
    MCfake_mt = MCfake_mt_plot.histoMgr.getHisto("EWK").getRootHisto().Clone(myEWKfakeShapeString)
    # Add MC fakes from baseline
    qcd_mt.Add(MCfake_mt)

    qcd_mt.SetName("Mis-ID #tau, sim. EWK+t#bar{t} no #tau_{h}")
    fakeTau_mt.SetName("Mis-ID. #tau, data-driven EWK+t#bar{t} no #tau_{h}")
    qcd_mt.SetLineColor(2)
    qcd_mt.SetLineStyle(2)
    fakeTau_mt.SetLineColor(1)
    qcd_mt.SetLineWidth(2)
    fakeTau_mt.SetLineWidth(2)

    qcd_mt = qcd_mt.Rebin(len(defaultBinning)-1,"", array.array("d",defaultBinning))
    fakeTau_mt = fakeTau_mt.Rebin(len(defaultBinning)-1,"", array.array("d",defaultBinning))
    
    # Divide by binwidth
    for i in range(0,qcd_mt.GetSize()):
        qcd_mt.SetBinContent(i, qcd_mt.GetBinContent(i)/qcd_mt.GetBinWidth(i))
        fakeTau_mt.SetBinContent(i, fakeTau_mt.GetBinContent(i)/fakeTau_mt.GetBinWidth(i))
        qcd_mt.SetBinError(i, qcd_mt.GetBinError(i)/qcd_mt.GetBinWidth(i))
        fakeTau_mt.SetBinError(i, fakeTau_mt.GetBinError(i)/fakeTau_mt.GetBinWidth(i))

    # Plot results
    plotClosure(qcd_mt, fakeTau_mt, "Inclusive", optimizationMode)
    plotFakeRateProbabilities(myFakeRateWeightCalculator.getWeights(), myFakeRateWeightCalculator.getWeightErrors(), myFakeRateWeightCalculator.getSortedFactors(), optimizationMode)
    writeNormalizationToFile(myFakeRateWeightCalculator.getSortedTotalFakeRateProbabilities(), "fakenorm.py")



def plotFakeRateProbabilities(w_list, w_err_list, normalization, optMode):
    weights = ROOT.TH1F("weights", "weights", len(w_list), 0, len(w_list))
    ewkfake_frp = ROOT.TH1F("EWK+t#bar{t} no #tau_{h}", "EWK+t#bar{t} no #tau_h", len(w_list), 0, len(w_list))
    qcd_frp = ROOT.TH1F("Multijet", "Multijet", len(w_list), 0, len(w_list))
    fake_frp = ROOT.TH1F("Mis-ID. #tau_{h}", "Mis-ID. #tau_h", len(w_list), 0, len(w_list))
    for i in range(0, len(w_list)):
        weights.SetBinContent(i+1, w_list[i])
        ewkfake_frp.SetBinContent(i+1, getNormalization(str(i), 0, normalization))
        qcd_frp.SetBinContent(i+1, getNormalization(str(i), 1, normalization))
        fake_frp.SetBinContent(i+1, getNormalization(str(i), w_list[i], normalization)) 
        
    for i in xrange(1, len(w_list)+1):
        weights.SetBinError(i, w_err_list[i-1])
        ewkfake_frp.SetBinError(i, 0)
        qcd_frp.SetBinError(i, 0)
        fake_frp.SetBinError(i, 0)

    weights.SetMarkerSize(1.5)
    weights.SetLineWidth(2)

    ewkfake_frp.SetMarkerSize(1.5)
    ewkfake_frp.SetMarkerColor(kRed)
    ewkfake_frp.SetLineWidth(2)
    qcd_frp.SetMarkerSize(1.5)
    qcd_frp.SetMarkerColor(kBlue)
    qcd_frp.SetLineWidth(2)
    fake_frp.SetMarkerSize(1.5)
    fake_frp.SetMarkerColor(6)
    fake_frp.SetLineWidth(2)

    plotInRanges(weights,optMode)
    plotInRanges2([ewkfake_frp,qcd_frp,fake_frp],optMode)

def plotInRanges(th1, optMode):
    xaxis = th1.GetXaxis()
    xaxis.SetBinLabel(1, "41-50")
    xaxis.SetBinLabel(2, "50-60")
    xaxis.SetBinLabel(3, "60-70")
    xaxis.SetBinLabel(4, "70-80")
    xaxis.SetBinLabel(5, "80-100")
    xaxis.SetBinLabel(6, "100-120")
    xaxis.SetBinLabel(7, "> 120")

    def foo(p):
        xaxis = p.getFrame().GetXaxis()
        xaxis.LabelsOption("u")
        xaxis.SetTitleOffset(xaxis.GetTitleOffset()*1.4)
        p.getPad().SetBottomMargin(0.16)

    p = plots.PlotBase([th1])
    p.setLuminosity("19.7")
    h = p.histoMgr.getHisto("weights")
    h.setDrawStyle("PE")
  
    drawPlot1(p, "weights_"+optMode.replace("OptQCDTailKiller",""),
             xlabel="p_{T}^{#tau_{h}} bin (GeV)",
             customizeBeforeDraw=foo
    )

def plotInRanges2(th1_list, optMode):
    xaxis = th1_list[0].GetXaxis()
    xaxis.SetBinLabel(1, "41-50")
    xaxis.SetBinLabel(2, "50-60")
    xaxis.SetBinLabel(3, "60-70")
    xaxis.SetBinLabel(4, "70-80")
    xaxis.SetBinLabel(5, "80-100")
    xaxis.SetBinLabel(6, "100-120")
    xaxis.SetBinLabel(7, "> 120")

    def foo(p):
        xaxis = p.getFrame().GetXaxis()
        xaxis.LabelsOption("u")
        xaxis.SetTitleOffset(xaxis.GetTitleOffset()*1.4)
        p.getPad().SetBottomMargin(0.16)

    p = plots.PlotBase(th1_list)
    p.setLuminosity("19.7")
    
    p.histoMgr.setHistoLegendStyleAll("F")

    hewk = p.histoMgr.getHisto("EWK+t#bar{t} no #tau_{h}")
    hewk.setDrawStyle("PE")
    hewk.setLegendStyle("P")

    hqcd = p.histoMgr.getHisto("Multijet")
    hqcd.setDrawStyle("PE")
    hqcd.setLegendStyle("P")

    hfake = p.histoMgr.getHisto("Mis-ID. #tau_{h}")
    hfake.setDrawStyle("PE")
    hfake.setLegendStyle("P")
  
    drawPlot2(p, "frp_"+optMode.replace("OptQCDTailKiller",""),
             xlabel="p_{T}^{#tau_{h}} bin (GeV)",
             customizeBeforeDraw=foo
    )

def plotVariableWidth(th1Inp):
    bins = [0, 41, 50, 60, 70, 80, 100, 120, 200]

    th1 = ROOT.TH1F("factors2", "factors2", len(bins)-1, array.array("d", bins))

    aux.copyStyle(th1Inp, th1)

    for i in xrange(2, len(bins)):
        th1.SetBinContent(i, th1Inp.GetBinContent(i-1))
        th1.SetBinError(i, th1Inp.GetBinError(i-1))

def foo(p):
    xaxis = p.getFrame().GetXaxis()
    xaxis.LabelsOption("u")
    xaxis.SetTitleOffset(xaxis.GetTitleOffset()*1.4)
    p.getPad().SetBottomMargin(0.16)

    p = plots.PlotBase([th1])
    p.setLuminosity("19.7")
    h = p.histoMgr.getHisto("factors2")
    h.setDrawStyle("PE")
    drawPlot(p, "qcd_normalization_varwidth",
             xlabel="#tau_{h} ^{}p_{T} (GeV)",
             errorBarsX=True)

def writeNormalizationToFile(normFactors,filename):
    fOUT = open(filename,"w")
    now = datetime.datetime.now()

    fOUT.write("# Generated on %s\n"%now.ctime())
    fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    fOUT.write("\n")
    fOUT.write("import sys\n")
    fOUT.write("\n")
    fOUT.write("def QCDInvertedNormalizationSafetyCheck(era):\n")
    fOUT.write("    validForEra = \""+"2012ABCD"+"\"\n")
    fOUT.write("    if not era == validForEra:\n")
    fOUT.write("        print \"Warning, inconsistent era, normalisation factors valid for\",validForEra,\"but trying to use with\",era\n")
    fOUT.write("        sys.exit()\n")
    fOUT.write("\n")
    fOUT.write("QCDInvertedNormalization = {\n")
    #for i in self.info:
    #    fOUT.write("    # %s\n"%i)
        
    maxLabelLength = 1
    i = 0
    while i < len(normFactors):
        line = "    \"" + str(i) + "\""
        while len(line) < maxLabelLength + 11:
            line += " "
        line += ": " + str(normFactors[str(i)+"FakeTau"])
        if i < len(normFactors) - 1 :
            line += ","
        line += "\n"
        fOUT.write(line)
        i = i + 1
        
    fOUT.write("}\n")
    fOUT.close()
    print "Normalization factors written in file",filename

if __name__ == "__main__":
    main()
