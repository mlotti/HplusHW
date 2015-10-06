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

def sort(normdict):

    eq_re = re.compile("taup_Teq(?P<value>\d+)to")
    lt_re = re.compile("taup_Tlt(?P<value>\d+)")
    gt_re = re.compile("taup_Tgt(?P<value>\d+)")

    binmap = {}
    value = 0
    for bin in normdict.keys():
        match = eq_re.search(bin)
        if match:
            value = int(match.group("value"))
            binmap[value] = bin
            continue
        match = lt_re.search(bin)
        if match:
            value = int(match.group("value")) - 1
            binmap[value] = bin
            continue
        match = gt_re.search(bin)
        if match:
            value = int(match.group("value")) + 1
            binmap[value] = bin
            continue

    i = 0
    retdict = {}
    for bin in sorted(binmap.keys()):
        retdict[str(i)] = normdict[binmap[bin]]
        i += 1

    return retdict
    

def getSortedLabelsAndFactors(normdict):

    eq_re = re.compile("taup_Teq(?P<value1>\d+)to(?P<value2>\d+)(?P<name>\D+)") 
    lt_re = re.compile("taup_Tlt(?P<value1>\d+)(?P<name>\D+)")
    gt_re = re.compile("taup_Tgt(?P<value1>\d+)(?P<name>\D+)")
        
    namemap = {}
    binmap = {}
    labels = {}
    value = 0
    for bin in normdict.keys():
        match = eq_re.search(bin)
        if match:
            name = str(match.group("name"))
            value = int(match.group("value1"))
            binmap[bin] = value
            namemap[bin] = name
            labels[value] = bin.replace(name,"")
            continue
        match = lt_re.search(bin)
        if match:
            name = str(match.group("name"))
            value = int(match.group("value1")) - 1
            binmap[bin] = value
            namemap[bin] = name
            labels[value] = bin.replace(name,"")
            continue
        match = gt_re.search(bin)
        if match:
            name = str(match.group("name"))
            value = int(match.group("value1")) + 1
            binmap[bin] = value
            namemap[bin] = name
            labels[value] = bin.replace(name,"")
            continue
                    
    i = 0
    sortdict = {}
    binvalues = sorted(list(set(binmap.values())))

    sortedlabels = []
    for binnum in binvalues:
        sortdict[binnum] = str(i)
        sortedlabels.append(labels[binnum])
        i += 1
    sortedlabels.append("Inclusive")

    retdict = {}
    inc_re = re.compile("Inclusive*")
    for bin in normdict.keys():
        match = inc_re.search(bin)
        if not match:
            retdict[sortdict[binmap[bin]]+namemap[bin]] = normdict[bin]
        else:
            retdict[bin] = normdict[bin]
        
    return sortedlabels,retdict


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
        #if not binname == "Inclusive":
        bins.append(binname)
    return bins


def getNormalization(bins,w,factors,dataDriven,qgCorrection):
    normalization = []
    #print factors
    #print bins
    for i,bin in enumerate(bins):
        label = str(i)
        if i == len(bins) - 1:
            label = "Inclusive"
        if dataDriven:
            if qgCorrection:
                normalization.append(w*factors[label+"QCD"] + (1-w)*factors[label+"EWK_FakeTaus"])
            else:
                normalization.append(factors[label+"QCD"])
        else:
            if not bin == "Inclusive":
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
                
        if i != 0 and bin != "Inclusive":
            h = mtplot.histoMgr.getHisto("Data").getRootHisto().Clone(name+"/"+name+bin)
            mt_ewk = mtplot.histoMgr.getHisto("EWK").getRootHisto().Clone(name+"/"+name+bin)
                        
            h.Add(mt_ewk,-1)
                        
            scale = normalization[i]
            h.Scale(scale)
            
            mt.Add(h)
    return mt


def main(argv):

    dirs = []
    dirs_signal = []

    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    #dirs_signal = ["../../SignalAnalysis_140605_143702/"]
    dirs_signal.append(sys.argv[2])
    #dirs_signal = ["/mnt/flustre/epekkari/SignalFakeTauLimits_140808_095404"]

    QCDInvertedNormalization = sort(QCDInvertedNormalizationFactors.QCDInvertedNormalization)
    labels,QCDInvertedNormalizationFilteredEWKFakeTaus = getSortedLabelsAndFactors(QCDInvertedNormalizationFactorsFilteredEWKFakeTaus.QCDInvertedNormalization)

    analysis_inverted = "signalAnalysisInvertedTau"
    analysis = "signalAnalysis"

    optModes = []
    #optModes.append("OptQCDTailKillerZeroPlus")
    optModes.append("OptQCDTailKillerLoosePlus") 
    #optModes.append("OptQCDTailKillerMediumPlus") 
    #optModes.append("OptQCDTailKillerTightPlus") 

    varHistoName = "shapeEWKGenuineTausTransverseMass"
    nomHistoName = "shapeTransverseMass"
    signalHistoName = "shapeEWKFakeTausTransverseMass"

    #w_list = [0.66, 0.67, 0.75] # golden old
    #w_list = [0.95, 0.955, 0.96, 0.965, 0.97, 0.975, 0.98, 0.985, 0.99, 0.995, 1]    
    #w_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    #w_list = [0.74, 0.741, 0.742, 0.743, 0.744, 0.745, 0.746, 0.747]
    w_list = [0.743]

    #defaultBinning = systematics.getBinningForPlot("shapeTransverseMass")
    defaultBinning = [0,20,40,60,80,100,120,140,160,200,400]
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

            normalization_var_qg = getNormalization(bins_var,w,QCDInvertedNormalizationFilteredEWKFakeTaus,True,True)
            normalization_var = getNormalization(bins_var,w,QCDInvertedNormalizationFilteredEWKFakeTaus,True,False)
            normalization_nom = getNormalization(bins_nom,w,QCDInvertedNormalization,False,False)

            mt_var_qg = getMt(mt_inverted_faketaus_data,bins_var,varHistoName,normalization_var_qg)
            mt_var = getMt(mt_inverted_faketaus_data,bins_var,varHistoName,normalization_var)
            mt_nom = getMt(mt_inverted_faketaus_data,bins_nom,nomHistoName,normalization_nom)
                
            mt_nom.Add(mt_signalfaketaus)

            mt_var_qg.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau), corr.")
            mt_var.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau)")
            mt_nom.SetName("QCD(Data)+EWK+t#bar{t}(MC, mis-ID. #tau)")

            mt_var_qg.SetLineWidth(4)
            mt_var.SetLineColor(14)
            mt_nom.SetLineColor(2)
            
            mt_var_qg = mt_var_qg.Rebin(len(defaultBinning)-1,"",defaultBinning_array)
            mt_var = mt_var.Rebin(len(defaultBinning)-1,"",defaultBinning_array)
            mt_nom = mt_nom.Rebin(len(defaultBinning)-1,"",defaultBinning_array)

            for i in range(0,mt_nom.GetSize()):
                var_values.append(mt_var_qg.GetBinContent(i))
                nom_values.append(mt_nom.GetBinContent(i))
                
            style = tdrstyle.TDRStyle()

            varPlots = [mt_var, mt_var_qg]
            plot = plots.ComparisonManyPlot(mt_nom,varPlots)
            plot.createFrame(optMode.replace("Opt","Mt_DataDrivenVsMC_"+"w="+str(w)+"_"), createRatio=True)

            moveLegend={"dx": -0.325,"dy": 0.02,"dw":-0.14,"dh":-0.12}
            
            plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
            #plot.setLegend(histograms.createLegend(x1=0.5, y1=0.7, x2=0.7, y2=0.95, textSize=0.1))
            histograms.addText(0.65, 0.3, optMode.replace("OptQCDTailKiller","R_{BB} ").replace("Plus",""), 25)
            histograms.addCmsPreliminaryText()
            histograms.addEnergyText()
            lumi=mt_inverted_faketaus_data.getDataset("Data").getLuminosity()
            histograms.addLuminosityText(x=None, y=None, lumi=lumi)

            plot.draw()
            plot.save()

            mt_var_qg.Delete()
            mt_var.Delete()
            mt_nom.Delete()

            mt_baseline_faketaus_data.close()
            mt_inverted_faketaus_data.close()
            ROOT.gROOT.CloseFiles()
            ROOT.gROOT.GetListOfCanvases().Delete()
            ROOT.gDirectory.GetList().Delete()

            # difference metrics
            num = 0
            denom = 0
            for i in range(0,len(nom_values)):
                num += var_values[i]*(var_values[i]-nom_values[i])**2
                denom += var_values[i]
            diff = num/denom
            diff_list.append(diff)
        diff_opt.append(diff_list)

    #os.system("rm MtOptimal/*")
    #os.system("mkdir -p MtOptimal")
    print "\nWeights:\t",w_list,'\n'
    optimalWeights = {}
    for i in range(0,len(diff_opt)):
        print optModes[i]
        print "Differences:\t",diff_opt[i],"- Optimal: w =",w_list[diff_opt[i].index(min(diff_opt[i]))]
        optimalWeights[optModes[i]] = w_list[diff_opt[i].index(min(diff_opt[i]))]
        #command = "cp *" + str(w_list[diff_opt[i].index(min(diff_opt[i]))])+"*"+optModes[i].replace("Opt","") + ".eps MtOptimal"
        #os.system(command)
    print optimalWeights

    optimalNormalization = getNormalization(bins_var,optimalWeights["OptQCDTailKillerLoosePlus"],QCDInvertedNormalizationFilteredEWKFakeTaus,True,True)
    writeNormalizationToFile("QCDPlusEWKFakeTauNormalizationFactors.py",optimalNormalization,labels)

def writeNormalizationToFile(filename,normalization,labels):
    fOUT = open(filename,"w")
    
    now = datetime.datetime.now()
    
    fOUT.write("# Generated on %s\n"%now.ctime())
    fOUT.write("# by %s\n"%os.path.basename(sys.argv[0]))
    fOUT.write("\n")
    fOUT.write("import sys\n")
    fOUT.write("\n")
    fOUT.write("def QCDInvertedNormalizationSafetyCheck(era):\n")
    fOUT.write("    validForEra = \""+dataEra+"\"\n")
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
        maxLabelLength = max(maxLabelLength,len(labels[i]))
        i = i + 1

    i = 0
    #print normalization
    while i < len(normalization):
        line = "    \"" + labels[i] + "\""
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
                        
if __name__ == "__main__":
    main(sys.argv)
