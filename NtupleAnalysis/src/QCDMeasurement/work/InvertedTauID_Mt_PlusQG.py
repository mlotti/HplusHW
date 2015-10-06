#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import *
import math
import sys
import os
import re
import array

import NtupleAnalysis.toolsdataset as dataset
import NtupleAnalysis.toolshistograms as histograms
import NtupleAnalysis.toolscounter as counter
import NtupleAnalysis.toolstdrstyle as tdrstyle
import NtupleAnalysis.toolsstyles as styles
import NtupleAnalysis.toolsplots as plots
import NtupleAnalysis.toolscrosssection as xsect
import NtupleAnalysis.toolssystematics as systematics

#dataEra = "Run2011AB"
dataEra = "Run2012ABCD"


searchMode = "Light"
#searchMode = "Heavy"

#HISTONAME = "shapeTransverseMass"
histoNameList = ["shapeEWKGenuineTausTransverseMass", "shapeTransverseMass"]

def EWKFakeFunction(x,par):
    #return par[0]**x[0]/math.factorial(x[0])*TMath.Exp(-par[0])
    return par[0]*TMath.Gaus(x[0],par[1],par[2],1)

def EWKFunction(x,par):
    value = 160
    if x[0] < value:
        return par[0]*TMath.Gaus(x[0],par[1],par[2],1)
    C = par[0]*TMath.Gaus(value,par[1],par[2],1)*TMath.Exp(value*par[3])
    return C*TMath.Exp(-x[0]*par[3])
                            

class FitFunction:
    def __call__( self, x, par ):
        return EWKFunction(x,par)

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <multicrab dir>"
    print
    sys.exit()

try:
    import QCDInvertedNormalizationFactors
except ImportError:
    print
    print "    WARNING, QCDInvertedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactors.py"
    print 

try:
    import QCDInvertedNormalizationFactorsFilteredEWKFakeTaus
except ImportError:
    print
    print "    WARNING, QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.py not found!"
    print "    Run script InvertedTauID_Normalization.py to generate QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.py"
    print 

def main(argv):

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    QCDInvertedNormalization = QCDInvertedNormalizationFactors.QCDInvertedNormalization
    QCDInvertedNormalizationFilteredEWKFakeTaus = QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.QCDInvertedNormalization
    analysis = "signalAnalysisInvertedTau"
    optModes = []
    #optModes.append("OptQCDTailKillerZeroPlus")
    optModes.append("OptQCDTailKillerLoosePlus") 
    optModes.append("OptQCDTailKillerMediumPlus") 
    optModes.append("OptQCDTailKillerTightPlus") 
    #optModes.append("OptQCDTailKillerVeryTightPlus")
    #optModes.append("OnlyGenuineMCTausFalse")
    #optModes.append("OnlyGenuineMCTausTrue")

    #Optimal: 0.8, 0.82, 0.9
    #w1_list = [0.8, 0.82, 0.84, 0.87]
    #w1_list = [0.8, 0.82, 0.9, 1]
    w1_list = [0.9]

    defaultBinning = systematics.getBinningForPlot("shapeTransverseMass")

    diff_opt = []
    for optMode in optModes:
        diff_list = []
        for w1 in w1_list:
            var_values = []
            nom_values = []
            w2 = 1 - w1
            
            color = 1

            #signal

            dirs_signal = ["../../SignalAnalysis_140605_143702/"]
            datasets_signal = dataset.getDatasetsFromMulticrabDirs(dirs_signal,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis.replace("InvertedTau",""), optimizationMode=optMode)
            
            datasets_signal.updateNAllEventsToPUWeighted()
            datasets_signal.loadLuminosities()
            
            datasets_signal.remove(filter(lambda name: "TTToHplus" in name, datasets_signal.getAllDatasetNames()))
            datasets_signal.remove(filter(lambda name: "HplusTB" in name, datasets_signal.getAllDatasetNames()))
            datasets_signal.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets_signal.getAllDatasetNames()))
            datasets_signal.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets_signal.getAllDatasetNames()))
            datasets_signal.remove(filter(lambda name: "TTJets_SemiLept" in name, datasets_signal.getAllDatasetNames()))
            datasets_signal.remove(filter(lambda name: "TTJets_FullLept" in name, datasets_signal.getAllDatasetNames()))
            datasets_signal.remove(filter(lambda name: "TTJets_Hadronic" in name, datasets_signal.getAllDatasetNames()))
            
            plots.mergeRenameReorderForDataMC(datasets_signal)
            
            datasets_signal.merge("EWK", [
                "TTJets",
                "WJets",
                "DYJetsToLL",
                "SingleTop",
                "Diboson"
                ])
            
            mtplot_signalfaketaus = plots.DataMCPlot(datasets_signal, "shapeEWKFakeTausTransverseMass")
            mt_signalfaketaus = mtplot_signalfaketaus.histoMgr.getHisto("EWK").getRootHisto().Clone("shapeEWKFakeTausTransverseMass")
            mt_signalfaketaus.SetName("BaselineFakeTaus")

            myBinning = [0, 20, 40, 60, 80, 100, 120, 140, 160, 200, 400]
            myArray = array.array("d",myBinning)

            fitBinning = []
            for i in range(0,45):
               fitBinning.append(i*10) 
            fitArray = array.array("d",fitBinning)

            mt_baseline = mt_signalfaketaus

            #rangeMin = mt_signalfaketaus.GetXaxis().GetXmin()
            #rangeMax = mt_signalfaketaus.GetXaxis().GetXmax()
            #theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,4)
            #theFit.SetParLimits(0,0.5,10000)
            #theFit.SetParLimits(1,90,10000)
            #theFit.SetParLimits(2,30,10000)
            #theFit.SetParLimits(3,0.001,10000)
            #mt_signalfaketaus.Fit(theFit,"R")
            #theFit.SetRange(mt_signalfaketaus.GetXaxis().GetXmin(),mt_signalfaketaus.GetXaxis().GetXmax())
            #theFit.SetLineStyle(2)
            #theFit.SetLineColor(4)
            #theFit.SetLineWidth(3)
            #theFit.Draw()
            #mt_corr = theFit.GetHistogram()
            #mt_corr = mt_corr.Rebin(len(fitBinning)-1,"",fitArray)
            #mt_corr.Scale(mt_baseline.GetMaximum()/mt_corr.GetMaximum())
            
            for HISTONAME in histoNameList:
                var = False
                if HISTONAME == "shapeEWKGenuineTausTransverseMass":
                    var = True
                datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)

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

                histonames = datasets.getDataset("Data").getDirectoryContent(HISTONAME)

                bins = []
                for histoname in histonames:
                    binname = histoname.replace(HISTONAME,"")
                    if not binname == "Inclusive":
                        bins.append(binname)

                for i,bin in enumerate(bins):
                    mtplot = plots.DataMCPlot(datasets, HISTONAME+"/"+HISTONAME+bin)

                    if i == 0:
                        mt = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                        mt_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                        mtn = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin) 
                        mtn_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)

                        if var:
                            legendName = "QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau)"
                        else:
                            legendName = "QCD(Data)+EWK+t#bar{t}(MC, mis-ID. #tau)"
                        legendName = legendName.replace("Plus","")
                        mt.SetName(legendName)
                        mt.SetLineColor(color)
                        mt.Add(mt_ewk,-1)
                        mtn.Add(mtn_ewk,-1)
                        mtn.Scale(QCDInvertedNormalization[str(i)])

                        if var:
                            scale = w1*QCDInvertedNormalizationFilteredEWKFakeTaus[str(i)] + w2*QCDInvertedNormalizationFilteredEWKFakeTaus[str(i)+"EWK_FakeTaus"]
                            mt.Scale(scale)
                        else:
                            mt.Scale(QCDInvertedNormalization[str(i)])
                        color += 1
                        if color == 5:
                            color += 1
                    else:
                        h = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                        mt_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                        hn = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)
                        mtn_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(HISTONAME+"/"+HISTONAME+bin)

                        h.Add(mt_ewk,-1)
                        hn.Add(mtn_ewk,-1)
                        hn.Scale(QCDInvertedNormalization[str(i)])

                        if var:
                            scale = w1*QCDInvertedNormalizationFilteredEWKFakeTaus[str(i)] + w2*QCDInvertedNormalizationFilteredEWKFakeTaus[str(i)+"EWK_FakeTaus"]
                            h.Scale(scale)
                        else:
                            h.Scale(QCDInvertedNormalization[str(i)])
                        mt.Add(h)
                        mtn.Add(hn)

                #mt = mt.Rebin(len(myBinning)-1,"",myArray)
                #mt_corr = mt_corr.Rebin(len(myBinning)-1,"",myArray)
                
                if not var:
                    mt.Add(mt_baseline)
                    #mt.Add(mt_corr) 
                    
                #myBinning = []    
                #for i in range(0,11):
                #    myBinning.append(20*i)
                #myBinning.append(400)
                
                #myArray = array.array("d",defaultBinning)
                mt = mt.Rebin(len(myBinning)-1,"",myArray)

                for i in range(0,mt.GetSize()):
                    if var:
                        var_values.append(mt.GetBinContent(i))
                    else:
                        nom_values.append(mt.GetBinContent(i))
                
                if var:
                    #mt.SetLineStyle(2)
                    var_hist = mt
                else:
                    #mt.SetLineStyle(2)
                    nom_hist = mt

                style = tdrstyle.TDRStyle()

                #gStyle.SetOptStat(1101)
                #mt_data.SetStats(1)
                #gPad.Update()
                bins = [0, 390, 400]
                arr = array.array("d",bins)
                mtn = mtn.Rebin(len(bins)-1,"",arr)
                plot_data = plots.PlotBase()
                plot_data.histoMgr.appendHisto(histograms.Histo(mtn,"Data"))
                plot_data.createFrame("Data_"+HISTONAME+"_"+optMode+"_"+str(w1))
                plot_data.draw()
                plot_data.save()


            plot = plots.ComparisonPlot(nom_hist,var_hist)
            plot.createFrame(optMode.replace("Opt","Mt_"+"w1="+str(w1)+"_w2="+str(w2)+"_DataDrivenVsMC_"), createRatio=True)

            moveLegend={"dx": -0.295,"dy": 0.05}
            plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
            histograms.addText(0.65, 0.20, optMode.replace("OptQCDTailKiller","R_{BB} ").replace("Plus",""), 25)
            histograms.addCmsPreliminaryText()
            histograms.addEnergyText()
            lumi=datasets.getDataset("Data").getLuminosity()
            histograms.addLuminosityText(x=None, y=None, lumi=lumi)

            plot.draw()
            plot.save()

            num = 0
            denom = 0
            #print var_values
            for i in range(0,len(nom_values)):
                num += var_values[i]*(var_values[i]-nom_values[i])**2
                denom += var_values[i]
            diff = num/denom
            diff_list.append(diff)
        diff_opt.append(diff_list)

    print w1_list,'\n'
    for i in range(0,len(diff_opt)):
        print diff_opt[i]
        print w1_list[diff_opt[i].index(min(diff_opt[i]))]

    mt_baseline = mt_baseline.Rebin(len(bins)-1,"",arr)
    plot_bft = plots.PlotBase()
    plot_bft.histoMgr.appendHisto(histograms.Histo(mt_baseline,"baseline"))
    #mt_corr.Scale(2)
    #plot_bft.histoMgr.appendHisto(histograms.Histo(mt_corr,"test"))


    #rangeMin = mt_signalfaketaus.GetXaxis().GetXmin()
    #rangeMax = mt_signalfaketaus.GetXaxis().GetXmax()
    #theFit = TF1('theFit',FitFunction(),rangeMin,rangeMax,4)
    #theFit.SetParLimits(0,0.5,10000)
    #theFit.SetParLimits(1,90,10000)
    #theFit.SetParLimits(2,30,10000)
    #theFit.SetParLimits(3,0.001,10000)
    #mt_signalfaketaus.Fit(theFit,"R")
    #theFit.SetRange(mt_signalfaketaus.GetXaxis().GetXmin(),mt_signalfaketaus.GetXaxis().GetXmax())
    #theFit.SetLineStyle(2)
    #theFit.SetLineColor(4)
    #theFit.SetLineWidth(3)
    #theFit.Draw()

    #mt_corr = theFit.GetHistogram()
    #mt_corr = mt_corr.Rebin(len(fitBinning)-1,"",fitArray)
    #mt_corr.Scale(mt_baseline.GetMaximum()/mt_corr.GetMaximum())
    #plot_bft.histoMgr.appendHisto(histograms.Histo(mt_corr,"test"))
    #plot_bft.histoMgr.appendHisto(histograms.Histo(theFit,"theFit"))

    plot_bft.createFrame('BaselineFakeTaus')
    plot_bft.draw()
    plot_bft.save()
    
if __name__ == "__main__":
    main(sys.argv)
