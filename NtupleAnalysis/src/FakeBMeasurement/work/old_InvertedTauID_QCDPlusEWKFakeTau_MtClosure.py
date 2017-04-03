#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1001;")

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
from HiggsAnalysis.NtupleAnalysis.tools.ShellStyles import *

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
    import QCDInvertedCombinedNormalizationFactors
except ImportError:
    print
    print "    WARNING, QCDInvertedCombinedNormalizationFactors.py not found!"
    print "    Run script InvertedTauID_CombinedNormalization.py to generate QCDInvertedCombinedNormalizationFactors.py"
    print     

class QCDPlusEWKFakeTau:

    def __init__(self, mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, normalization_nom, normalization_var, weights, labels, qgCorrection = False, splitted = False):
        self.mt_nom = []

        self.mt_var = []
        self.w_opt = []

        self.chisquares = []
        
        self.splitted = splitted

        self.labels = labels

        if splitted:
            self.doSplittedReWeighting(mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, normalization_nom, normalization_var, weights)
        else:
            self.doReWeighting(mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, normalization_nom, normalization_var, weights, qgCorrection)
            

    def doReWeighting(self, mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, normalization_nom, normalization_var, weights, qgCorrection):
        diffs = []
        w_dict = {}
        if not qgCorrection:
            weights = [1]
        else:
            print CaptionStyle(), "Weighting done inclusively", NormalStyle(),"\n"
        #print HighlightStyle(),"Weight:\tDifference:",NormalStyle()
        for w in weights:
            w_current = w
            for i in range(0,len(mt_qcdplusmcfakes_list)):
                bin = str(i)
                norm_var = getNormalization(bin, w, normalization_var)
                norm_nom = getNormalization(bin, 1, normalization_nom)
                w_dict[w] = norm_var
                if i == 0:
                    mt_var = mt_qcdplusddfakes_list[i].Clone()
                    mt_nom = mt_qcdplusmcfakes_list[i].Clone()
                    mt_var.Scale(norm_var)
                    mt_nom.Scale(norm_nom)
                    mt_nom.Add(mt_baselinefaketaus_list[i])
                else:
                    h_var = mt_qcdplusddfakes_list[i].Clone()
                    h_nom = mt_qcdplusmcfakes_list[i].Clone()
                    h_var.Scale(norm_var)
                    h_nom.Scale(norm_nom)
                    h_nom.Add(mt_baselinefaketaus_list[i])
                    mt_var.Add(h_var)
                    mt_nom.Add(h_nom)
            mt_opt = mt_var.Clone()

            diff = getDifference(mt_nom,mt_var)
            self.chisquares.append(-diff+1)
            #diff = mt_nom.Chi2Test(mt_var, "WW, CHI2")
            #diff = mt_nom.KolmogorovTest(mt_var, "M")
            #diff = math.fabs(1-mt_nom.Integral()/mt_var.Integral())
            #print w, "\t\t", diff
            diffs.append(diff)

        w_opt = weights[diffs.index(min(diffs))]
        mt_opt.Scale(w_dict[w_opt]/w_dict[w_current])
    
        if qgCorrection:
            print HighlightStyle(),"Optimal weight: w = ", w_opt, NormalStyle(),"\n"

        mt_nom.SetName("QCD(Data)+EWK+t#bar{t}(MC, mis-ID. #tau)")
        if qgCorrection:
            mt_opt.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau), q-g")
            mt_opt.SetLineColor(13)
        else:
            mt_opt.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau)")
            mt_opt.SetLineColor(16)

        mt_nom.SetLineColor(2)
        
        self.mt_nom = [mt_nom.Clone()]
        self.mt_var = [mt_opt.Clone()]
        self.w_opt = [w_opt]

    def doSplittedReWeighting(self, mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, normalization_nom, normalization_var, weights, qgCorrection = True):
        w_opts = []
        mt_opts = []
        mts_nom_norm = []
        w_dict = {}
        splittedBinning = [0,50,100,150,200,250,300,350,400] 
        # TODO: if w not in range [0.5, 1], do no reweigting
        print CaptionStyle(), "Weighting done in pT-splitted bins", NormalStyle(),"\n"
        for i in range(0,len(mt_qcdplusmcfakes_list)):
            print HighlightStyle(),"Bin:",self.labels[i],NormalStyle()
            bin = str(i)
            diffs = []
            #print HighlightStyle(),"Weight:\tDifference:",NormalStyle()
            norm_nom = getNormalization(bin, 1, normalization_nom)
            h_nom = mt_qcdplusmcfakes_list[i].Clone()
            h_nom.Scale(norm_nom)
            h_nom.Add(mt_baselinefaketaus_list[i])
            for w in weights:
                w_current = w
                norm_var = getNormalization(bin, w, normalization_var)
                w_dict[w] = norm_var
                h_var = mt_qcdplusddfakes_list[i].Clone()
                h_var.Scale(norm_var)
                
                # to improve statistics
                #h_nom = h_nom.Rebin(len(splittedBinning)-1,"", array.array("d",splittedBinning))
                #h_var = h_var.Rebin(len(splittedBinning)-1,"", array.array("d",splittedBinning))

                diff = getDifference(h_nom, h_var) # toimii parhaiten, ei binitysta
                #diff = h_nom.Chi2Test(h_var, "WW, CHI2") # oudot painot 
                #diff = h_nom.KolmogorovTest(h_var,"M") # saako kayttaa?
            
                diffs.append(diff)
                #print w, "\t\t", diff

            mt_opt = h_var.Clone()    
            w_opt = weights[diffs.index(min(diffs))]
            w_opts.append(w_opt)
            
            #if w_opt > 0.5:
            #    mt_opt.Scale(w_dict[w_opt]/w_dict[w_current])
            #else:
            #    mt_opt.Scale(1/w_dict[w_current])

            mt_opt.Scale(w_dict[w_opt]/w_dict[w_current])

            print HighlightStyle(),"Optimal weight: w = ", w_opt, NormalStyle(),"\n"

            h_nom.SetName("QCD(Data)+EWK+t#bar{t}(MC, mis-ID. #tau), p_{T} bin: "+bin)
            mt_opt.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau), p_{T} bin: "+bin)

            h_nom.SetLineColor(2)
            mt_opt.SetLineWidth(4)

            mt_opts.append(mt_opt.Clone())
            mts_nom_norm.append(h_nom.Clone())

        self.mt_nom = mts_nom_norm
        self.mt_var = mt_opts
        self.w_opt = w_opts

    def getOptimalWeight(self, bin = 0):
        return self.w_opt[bin]

    def getOptimalMt(self, bin = 0):
        return self.mt_var[bin].Clone()

    def getNominalMt(self, bin = 0):
        return self.mt_nom[bin].Clone()

    def getChiSquares(self):
        return self.chisquares

def getDifference(mt_nom, mt_var):
    num = 0
    denom = 0
    for k in range(0,mt_nom.GetSize()): #mt bins
        #num += math.fabs(var_values[k])*(var_values[k]-nom_values[k])**2
        #denom += math.fabs(var_values[k])
        num += (mt_var.GetBinContent(k)-mt_nom.GetBinContent(k))**2
        denom += mt_var.GetBinContent(k)+mt_nom.GetBinContent(k)                   
    return num/denom

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

def refinedDataSets(dirs, dataEra, searchMode, analysis, optMode):
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
        bins.append(binname)
    return bins

def getNormalization(bin, w, normalization):
    if w != 1:
        norm = w*normalization[bin+"QCD"] + (1-w)*normalization[bin+"EWK_FakeTaus"]
    else:
        norm = w*normalization[bin+"QCD"]
    return norm
    
def printSummedDifference(mt_nom, mt_var):
    diff_sum = 0
    for bin in range(0, mt_nom.GetSize()): #mt bins
        diff_sum += math.fabs(mt_var.GetBinContent(bin) - mt_nom.GetBinContent(bin))
    print str(diff_sum) + "\t" + mt_var.GetName() 

def plotClosure(mt_nom, mts_var, name, optMode):
    #for mt_var in mts_var:
    #    printSummedDifference(mt_nom, mt_var)

    style = tdrstyle.TDRStyle()
    plot = plots.ComparisonManyPlot(mt_nom, mts_var)
    plot.createFrame(optMode.replace("Opt","mT_Closure_"+ name +"_"), createRatio=True)
        
    moveLegend={"dx": -0.325,"dy": 0.02,"dw":-0.14,"dh":-0.12}
        
    plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    histograms.addText(0.65, 0.3, optMode.replace("OptQCDTailKiller","R_{BB} ").replace("Plus",""), 25)
        
    histograms.addStandardTexts()
    
    plot.draw()
    plot.save()

def writeNormalizationToFile(filename,optModeNormalizations,labels):
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

    for optMode in optModeNormalizations.keys():
        fOUT.write("QCDInvertedNormalization" + optMode + " = {\n")
        #for i in self.info:
        #    fOUT.write("    # %s\n"%i)
    
        maxLabelLength = 0
        i = 0
        while i < len(optModeNormalizations[optMode]):
            maxLabelLength = max(maxLabelLength,len(labels[i]))
            i = i + 1
    
        i = 0
        #print normalization
        while i < len(optModeNormalizations[optMode]):
            line = "    \"" + labels[i] + "\""
            while len(line) < maxLabelLength + 11:
                line += " "
                line += ": " + str(optModeNormalizations[optMode][i])
            if i < len(optModeNormalizations[optMode]) - 1:
                line += ","
            line += "\n"
            fOUT.write(line)
            i = i + 1
            
        fOUT.write("}\n")
        

    fOUT.close()
    print "\nNormalization factors written in file",filename,"\n"

def WriteLatexOutput(filename,optModes,optimalWeights):
    fOUT = open(filename,"w")
    now = datetime.datetime.now()
    #fOUT.write("\\documentstyle[graphicx,a4,12pt]{article}\n\n")
    #fOUT.write("\\begin{document}\n")
    #fOUT.write("Generated on %s by \\verb|%s|\n"%(now.ctime(),os.path.basename(sys.argv[0])))

    fOUT.write("\\begin{table}\n")
    fOUT.write("\\begin{center}\n")
    fOUT.write("\\caption{Optimal weights $w$ for each angular cut scenario.}\n")
    fOUT.write("\\vspace{5 mm}\n")
    fOUT.write("\\begin{tabular}{ l | r }\n")
    fOUT.write("\\label{" + filename.replace(".tex", "")  + "}\n")
    fOUT.write("\t\\textbf{Angular cut scenario} & \\textbf{Optimal} $w$ \\\\ \n")
    fOUT.write("\t\hline\n")
    scenario_re = re.compile("OptQCDTailKiller(?P<scenario>\w+)Plus")
    for i in range(0, len(optModes)):
        match = scenario_re.search(optModes[i])
        if match:
            scenario = str(match.group("scenario"))
            if scenario == "Loose" or scenario == "Medium" or scenario == "Tight":
                fOUT.write("\t" + scenario + " & " + str(optimalWeights[i]) + "\\\\ \n")
    fOUT.write("\\end{tabular}\n")
    fOUT.write("\\end{center}\n")
    fOUT.write("\\end{table}\n")
    #fOUT.write("\\end{document}\n")
    fOUT.close()
    print "Created latex file for fit figures   ",filename


def main(argv):
    dirs = []
    dirs_signal = []
    optimalWeights = []
    optModeNormalizations = {}

    if len(sys.argv) < 2:
	usage()

    dirs.append(sys.argv[1])

    dirs_signal.append(sys.argv[2])
    #dirs_signal = ["/mnt/flustre/epekkari/SignalFakeTauLimits_140808_095404"]

    labels_nom, QCDInvertedNormalization = getSortedLabelsAndFactors(QCDInvertedCombinedNormalizationFactors.QCDInvertedNormalization)
    labels_var, QCDInvertedNormalizationFilteredEWKFakeTaus = getSortedLabelsAndFactors(QCDInvertedCombinedNormalizationFactors.QCDInvertedNormalizationSeparatedFakeTaus)

    analysis_inverted = "signalAnalysisInvertedTau"
    analysis = "signalAnalysis"

    optModes = []
    #optModes.append("OptQCDTailKillerZeroPlus")
    optModes.append("OptQCDTailKillerLoosePlus") 
    optModes.append("OptQCDTailKillerMediumPlus") 
    optModes.append("OptQCDTailKillerTightPlus")
    optModes.append("OptQCDTailKillerNoCuts") 

    invertedgenuinetauHistoName = "shapeEWKGenuineTausTransverseMass"
    invertedinclusivetauHistoName = "shapeTransverseMass"
    baselinefaketauHistoName = "shapeEWKFakeTausTransverseMass"

    
    #weights = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    #weights = [0.736, 0.737, 0.738, 0.739, 0.74, 0.741, 0.742, 0.743, 0.744]
    #weights = [0.67, 0.675, 0.68, 0.685, 0.69, 0.695]
    #weights_splitted = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    weights = []
    for i in range(0, 101):
         weights.append(0.01*i)

    #defaultBinning = systematics.getBinningForPlot("shapeTransverseMass")
    defaultBinning = [0,20,40,60,80,100,120,140,160,200,400]
    defaultBinning_array = array.array("d",defaultBinning)

    for optMode in optModes:
        baseline_datasets = refinedDataSets(dirs_signal, dataEra, searchMode, analysis, optMode)
        inverted_datasets = refinedDataSets(dirs, dataEra, searchMode, analysis_inverted, optMode)

        histonames_var = inverted_datasets.getDataset("Data").getDirectoryContent(invertedgenuinetauHistoName)
        histonames_nom = inverted_datasets.getDataset("Data").getDirectoryContent(invertedinclusivetauHistoName)
        
        bins_var = getBins(histonames_var, invertedgenuinetauHistoName)
        bins_nom = getBins(histonames_nom, invertedinclusivetauHistoName)

        mt_qcdplusmcfakes_list = []
        mt_qcdplusddfakes_list = []
        mt_baselinefaketaus_list = []

        defaultBinning = [0,20,40,60,80,100,120,140,160,200,400]
        defaultBinning_array = array.array("d",defaultBinning)
        
        for i,bin in enumerate(bins_nom):
            mtplot_tau = plots.DataMCPlot(inverted_datasets, invertedinclusivetauHistoName+"/"+invertedinclusivetauHistoName+bin)
            mtplot_genuinetau = plots.DataMCPlot(inverted_datasets, invertedgenuinetauHistoName+"/"+invertedgenuinetauHistoName+bin)
            mtplot_baselinefaketau = plots.DataMCPlot(baseline_datasets, baselinefaketauHistoName+"/"+baselinefaketauHistoName+bin)
            
            # mt histos
            
            # nominal
            mt_qcdplusmcfakes = mtplot_tau.histoMgr.getHisto("Data").getRootHisto().Clone(invertedinclusivetauHistoName+"/"+invertedinclusivetauHistoName+bin)
            mt_tau_ewk = mtplot_tau.histoMgr.getHisto("EWK").getRootHisto().Clone(invertedinclusivetauHistoName+"/"+invertedinclusivetauHistoName+bin)
            mt_qcdplusmcfakes.Add(mt_tau_ewk,-1)
            mt_baselinefaketau_ewk = mtplot_baselinefaketau.histoMgr.getHisto("EWK").getRootHisto().Clone(baselinefaketauHistoName+"/"+baselinefaketauHistoName+bin)
            #mt_qcdplusmcfakes.Add(mt_baselinefaketau_ewk)
            
            # variational
            mt_qcdplusddfakes = mtplot_genuinetau.histoMgr.getHisto("Data").getRootHisto().Clone(invertedgenuinetauHistoName+"/"+invertedgenuinetauHistoName+bin)
            mt_genuinetau_ewk = mtplot_genuinetau.histoMgr.getHisto("EWK").getRootHisto().Clone(invertedgenuinetauHistoName+"/"+invertedgenuinetauHistoName+bin)
            mt_qcdplusddfakes.Add(mt_genuinetau_ewk,-1)
            
            if not "Inclusive" in bin:
                mt_qcdplusddfakes_list.append(mt_qcdplusddfakes)
                mt_qcdplusmcfakes_list.append(mt_qcdplusmcfakes)
                mt_baselinefaketaus_list.append(mt_baselinefaketau_ewk)

        # the actual calculations are done here

        noCorrections = QCDPlusEWKFakeTau(mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, QCDInvertedNormalization, QCDInvertedNormalizationFilteredEWKFakeTaus, weights, labels_nom, qgCorrection = False, splitted = False)

        print "\n",CaptionStyle(),"***Quark-Gluon jet imbalance correction***",NormalStyle(),"\n"
        print CaptionStyle(),"Optimization mode:",optMode,NormalStyle(),"\n"

        qgCorrected = QCDPlusEWKFakeTau(mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, QCDInvertedNormalization, QCDInvertedNormalizationFilteredEWKFakeTaus, weights, labels_nom, qgCorrection = True, splitted = False)
        qgCorrectedAndSplitted = QCDPlusEWKFakeTau(mt_qcdplusmcfakes_list, mt_qcdplusddfakes_list, mt_baselinefaketaus_list, QCDInvertedNormalization, QCDInvertedNormalizationFilteredEWKFakeTaus, weights, labels_nom, qgCorrection = True, splitted = True)

        weights_array = array.array("d", weights)
        chi2_array = array.array("d", qgCorrected.getChiSquares())
        c = TCanvas("Chi2_"+optMode,"Chi2_"+optMode,200,10,700,500);
        chi2gr = TGraph(len(weights), weights_array, chi2_array)
        chi2gr.Fit("gaus")
        chi2gr.Draw("ACP")
        c.Update()
        c.SaveAs("chi2_"+optMode+".png") 

        #print CaptionStyle(), "Summed differences in bins:", NormalStyle()
        
        # Splitted closure plots

        for i in range(0,len(bins_var)-1):
            mt_nom = qgCorrectedAndSplitted.getNominalMt(bin = i).Rebin(len(defaultBinning)-1,"",defaultBinning_array)
            mt_var = qgCorrectedAndSplitted.getOptimalMt(bin = i).Rebin(len(defaultBinning)-1,"",defaultBinning_array)
            #plotClosure(mt_nom, [mt_var], "bin="+str(i)+"_w="+str(qgCorrectedAndSplitted.getOptimalWeight(bin = i)), optMode)
            plotClosure(mt_nom, [mt_var], labels_nom[i], optMode)

        # Rebinning for combined plot

        mt_nom = noCorrections.getNominalMt().Rebin(len(defaultBinning)-1,"",defaultBinning_array)
        mt_var = noCorrections.getOptimalMt().Rebin(len(defaultBinning)-1,"",defaultBinning_array)                              
        mt_qg = qgCorrected.getOptimalMt().Rebin(len(defaultBinning)-1,"",defaultBinning_array)
        for i in range(0, len(bins_var)-1):
            mt_qcdplusddfakes_list[i] = mt_qcdplusddfakes_list[i].Rebin(len(defaultBinning)-1,"",defaultBinning_array)

        # Splitted histograms summed

        mt_splitted_qg = mt_qcdplusddfakes_list[0].Clone()
        norm_var = getNormalization(str(0), qgCorrectedAndSplitted.getOptimalWeight(bin=0), QCDInvertedNormalizationFilteredEWKFakeTaus)
        mt_splitted_qg.Scale(norm_var)
        mt_splitted_qg.SetName("QCD(Data)+EWK+t#bar{t}(Data, mis-ID. #tau), q-g p_{T}")
        for bin in range(1,len(bins_var)-1):
            norm_var = getNormalization(str(bin), qgCorrectedAndSplitted.getOptimalWeight(bin=bin), QCDInvertedNormalizationFilteredEWKFakeTaus)
            h_var = mt_qcdplusddfakes_list[bin].Clone()
            h_var.Scale(norm_var)
            mt_splitted_qg.Add(h_var)

        #print CaptionStyle(), "Summed differences:", NormalStyle()

        # Combined closure plot

        plotClosure(mt_nom, [mt_var, mt_qg, mt_splitted_qg], "Combined", optMode)
        plotClosure(mt_nom, [mt_qg], "NoSplitting", optMode)
        plotClosure(mt_nom, [mt_splitted_qg], "SplittedBin", optMode)

        print "Nominal Integral: ", mt_nom.Integral()
        print "Variational (qg) Integral: ", mt_qg.Integral()

        optimalNormalization = []
        for bin in bins_nom:
            optimalNormalization.append(getNormalization(bin, qgCorrected.getOptimalWeight(), QCDInvertedNormalizationFilteredEWKFakeTaus))
        optModeNormalizations[optMode] = optimalNormalization
            #optimalNormalization.append(getNormalization(bin, w_opt[i], QCDInvertedNormalizationFilteredEWKFakeTaus))#inclusive?
        #if optMode == "OptQCDTailKillerLoosePlus":
        #    writeNormalizationToFile("QCDPlusEWKFakeTauNormalizationFactors.py", optimalNormalization, labels_var)
        optimalWeights.append(qgCorrected.getOptimalWeight())
    
    optimalNormalizationOnlyQCD = []
    optimalNormalizationOnlyEWKFakeTau = []
    for bin in bins_nom:
        optimalNormalizationOnlyQCD.append(getNormalization(bin, 1, QCDInvertedNormalizationFilteredEWKFakeTaus))
        optimalNormalizationOnlyEWKFakeTau.append(getNormalization(bin, 0, QCDInvertedNormalizationFilteredEWKFakeTaus))
    optModeNormalizations["OnlyQCD"] =  optimalNormalizationOnlyQCD
    optModeNormalizations["OnlyEWKFakeTau"] = optimalNormalizationOnlyEWKFakeTau
    writeNormalizationToFile("QCDPlusEWKFakeTauNormalizationFactors.py", optModeNormalizations, labels_var)
    WriteLatexOutput("wtable.tex", optModes, optimalWeights)

if __name__ == "__main__":
    main(sys.argv)
