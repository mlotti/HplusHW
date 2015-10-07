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

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.crosssection as xsect
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics

#dataEra = "Run2011AB"
dataEra = "Run2012ABCD"


searchMode = "Light"
#searchMode = "Heavy"


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

def getDataSets(dirs, dataEra, searchMode, analysis, optMode):
    datasets = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra,  searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
            
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()
    
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_t-channel" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "Hplus_taunu_tW-channel" in name, datasets.getAllDatasetNames()))
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

def getBins(histonames, name):
    bins = []
    for histoname in histonames:
        binname = histoname.replace(name,"")
        if not binname == "Inclusive":
            bins.append(binname)
    return bins

def getNormalization(bins,w,factors,qgCorrection):
    normalization = []
    for i,bin in enumerate(bins):
        label = str(i)
        #if i == len(bins) - 1:
        #    label = "Inclusive"
        if qgCorrection:
            normalization.append(w*factors[label] + (1-w)*factors[label+"EWK_FakeTaus"])
        else:
            normalization.append(factors[label])
    return normalization

def getMt(datasets,bins,name,normalization):
    for i,bin in enumerate(bins):
        mtplot = plots.DataMCPlot(datasets, name+"/"+name+bin)
        
        if i == 0:
            mt = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(name+"/"+name+bin)
            mt_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(name+"/"+name+bin)
                        
            mt.Add(mt_ewk,-1)
                                
            scale = normalization[i]
            mt.Scale(scale)
                
        #if i != 0 and bin != "Inclusive":
        else:
            h = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(name+"/"+name+bin)
            mt_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(name+"/"+name+bin)
                        
            h.Add(mt_ewk,-1)
                        
            scale = normalization[i]
            h.Scale(scale)
            
            mt.Add(h)
    return mt

def main(argv):

    dirs = []
    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    dirs_signal = ["../../SignalAnalysis_140605_143702/"]

    QCDInvertedNormalization = QCDInvertedNormalizationFactors.QCDInvertedNormalization
    QCDInvertedNormalizationFilteredEWKFakeTaus = QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.QCDInvertedNormalization
    analysis_inverted = "signalAnalysisInvertedTau"
    analysis = "signalAnalysis"

    optModes = []
    #optModes.append("OptQCDTailKillerZeroPlus")
    optModes.append("OptQCDTailKillerLoosePlus") 
    optModes.append("OptQCDTailKillerMediumPlus") 
    optModes.append("OptQCDTailKillerTightPlus") 

    varHistoName = "shapeEWKGenuineTausTransverseMass"
    nomHistoName = "shapeTransverseMass"
    signalHistoName = "shapeEWKFakeTausTransverseMass"

    #Optimal: 0.8, 0.82, 0.9

    #w_list = [0.65, 0.7, 0.76] #baseline ft
    w_list = [0.66, 0.67, 0.75]
    
    defaultBinning = systematics.getBinningForPlot("shapeTransverseMass")
    defaultBinning_array = array.array("d",defaultBinning)

    diff_opt = []
    for optMode in optModes:
        diff_list = []
        for w in w_list:
            var_values = []
            nom_values = []

            # baseline fake taus
            mt_baseline_faketaus_data = getDataSets(dirs_signal, dataEra, searchMode, analysis, optMode)
            mtplot_signalfaketaus = plots.DataMCPlot(mt_baseline_faketaus_data, signalHistoName)
            mt_signalfaketaus = mtplot_signalfaketaus.histoMgr.getHisto("EWK").getRootHisto().Clone(signalHistoName)

            # inverted fake taus
            mt_inverted_faketaus_data = getDataSets(dirs, dataEra, searchMode, analysis_inverted, optMode)

            histonames_var = mt_inverted_faketaus_data.getDataset("Data").getDirectoryContent(varHistoName)
            histonames_nom = mt_inverted_faketaus_data.getDataset("Data").getDirectoryContent(nomHistoName)


            bins_var = getBins(histonames_var, varHistoName)
            bins_nom = getBins(histonames_nom, nomHistoName)

            normalization_var_qg = getNormalization(bins_var,w,QCDInvertedNormalizationFilteredEWKFakeTaus,True)
            normalization_var = getNormalization(bins_var,w,QCDInvertedNormalizationFilteredEWKFakeTaus,False)
            normalization_nom = getNormalization(bins_nom,w,QCDInvertedNormalization,False)

            mt_var_qg = getMt(mt_inverted_faketaus_data,bins_var,varHistoName,normalization_var_qg)
            mt_var = getMt(mt_inverted_faketaus_data,bins_var,varHistoName,normalization_var)
            mt_nom = getMt(mt_inverted_faketaus_data,bins_nom,nomHistoName,normalization_nom)
                
            mt_nom.Add(mt_signalfaketaus)

            mt_var_qg.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau), q-g bal.")
            mt_var.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau)")
            mt_nom.SetName("QCD(Data)+EWK+t#bar{t}(MC, mis-ID. #tau)")

            mt_var_qg.SetLineWidth(4)
            mt_var.SetLineColor(14)
            mt_nom.SetLineColor(2)
            
            #mt_var_qg = mt_var_qg.Rebin(len(defaultBinning)-1,"",defaultBinning_array)
            #mt_var = mt_var.Rebin(len(defaultBinning)-1,"",defaultBinning_array)
            #mt_nom = mt_nom.Rebin(len(defaultBinning)-1,"",defaultBinning_array)

            for i in range(0,mt_nom.GetSize()):
                var_values.append(mt_var_qg.GetBinContent(i))
                nom_values.append(mt_nom.GetBinContent(i))
                
            style = tdrstyle.TDRStyle()

            varPlots = [mt_var, mt_var_qg]
            plot = plots.ComparisonManyPlot(mt_nom,varPlots)
            plot.createFrame(optMode.replace("Opt","Mt_DataDrivenVsMC_"+"w="+str(w)+"_"), createRatio=True)

            moveLegend={"dx": -0.35,"dy": 0.05}
            plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
            histograms.addText(0.65, 0.3, optMode.replace("OptQCDTailKiller","R_{BB} ").replace("Plus",""), 25)
            histograms.addCmsPreliminaryText()
            histograms.addEnergyText()
            lumi=mt_inverted_faketaus_data.getDataset("Data").getLuminosity()
            histograms.addLuminosityText(x=None, y=None, lumi=lumi)

            plot.draw()
            plot.save()

            #mt_var_qg.Delete()
            #mt_var.Delete()
            #mt_nom.Delete()
            
            #TFile.CurrentFile().Close("R")
            
            # difference metrics
            num = 0
            denom = 0
            for i in range(0,len(nom_values)):
                num += var_values[i]*(var_values[i]-nom_values[i])**2
                denom += var_values[i]
            diff = num/denom
            diff_list.append(diff)
        diff_opt.append(diff_list)

    os.system("rm MtOptimal/*")
    os.system("mkdir -p MtOptimal")
    print "\nWeights:\t",w_list,'\n'
    optimalWeights = {}
    for i in range(0,len(diff_opt)):
        print optModes[i]
        print "Differences:\t",diff_opt[i],"- Optimal: w =",w_list[diff_opt[i].index(min(diff_opt[i]))]
        optimalWeights[optModes[i]] = w_list[diff_opt[i].index(min(diff_opt[i]))]
        command = "cp *" + str(w_list[diff_opt[i].index(min(diff_opt[i]))])+"*"+optModes[i].replace("Opt","") + ".eps MtOptimal"
        os.system(command)
    print optimalWeights
    writeWeightsToFile("OptimalWeights.py",optimalWeights)
    writeNormalizationToFile("QCDPlusEWKFakeTauNormalizationFactors.py",normalization_var_qg,bins_var)

def writeNormalizationToFile(filename,normalization,bins):
    fOUT = open(filename,"w")
    
    now = datetime.datetime.now()

    era = "2012ABCD"
    
    fOUT.write("# Generated on %s\n"%now.ctime())
    fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    fOUT.write("\n")
    fOUT.write("import sys\n")
    fOUT.write("\n")
    fOUT.write("def QCDInvertedNormalizationSafetyCheck(era):\n")
    fOUT.write("    validForEra = \""+era+"\"\n")
    fOUT.write("    if not era == validForEra:\n")
    fOUT.write("        print \"Warning, inconsistent era, normalisation factors valid for\",validForEra,\"but trying to use with\",era\n")
    fOUT.write("        sys.exit()\n")
    fOUT.write("\n")
    fOUT.write("QCDInvertedNormalization = {\n")
    #for i in self.info:
    #    fOUT.write("    # %s\n"%i)

    maxLabelLength = 0
    i = 0
    while i < len(normalization):
        maxLabelLength = max(maxLabelLength,len(bins[i]))
        i = i + 1

    i = 0
    print normalization
    while i < len(normalization):
        line = "    \"" + bins[i] + "\""
        while len(line) < maxLabelLength + 11:
            line += " "
            line += ": " + str(normalization[i])
        if i < len(normalization) - 1:
            line += ","
        line += "\n"
        fOUT.write(line)
        i = i + 1
        
    fOUT.write("}\n")
    fOUT.close()
    print "Normalization factors written in file",filename
    


def writeWeightsToFile(filename,optimalWeights):
    fOUT = open(filename,"w")
    
    #now = datetime.datetime.now()
    
    #fOUT.write("# Generated on %s\n"%now.ctime())
    #fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    #fOUT.write("\n")
    fOUT.write("import sys\n")
    fOUT.write("\n")
    
    fOUT.write("QuarkGluonCorrectionFactors = {\n")
            
    i = 0
    optModes = optimalWeights.keys()
    while i < len(optModes):
        line = optModes[i] + ": " + str(optimalWeights[optModes[i]])
        if i < len(optimalWeights) - 1:
                line += ","
        line += "\n"
        fOUT.write(line)
        i = i + 1

    fOUT.write("}\n")
    fOUT.close()
                    
if __name__ == "__main__":
    main(sys.argv)
