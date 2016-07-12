#!/usr/bin/env python

######################################################################
#
# Produce a ROOT file with the histograms/counters from QCDInverted
# with mt constructed in tau pt bins
#
# Based on produceTauEmbeddingResult.py by M. Kortelainen
# Modified for QCD inverted tau method 22.11.2012/S.Lehti
# Updated 7.5.2013/S.Lehti
# Updated 19.6.2013/S.Lehti
######################################################################

import os
import re
import sys
import math
import json
import array
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import execute,addConfigInfo

searchMode = "Light"             
#searchMode = "Heavy"            


analysis      = "signalAnalysisInvertedTau"
massPlots     = []
massPlotNames = []
controlPlots  = []

rebin = 1


massPlots.append("shapeTransverseMass")
massPlots.append("shapeInvariantMass")

controlPlots.append("ForDataDrivenCtrlPlots")

def usage():
    print
    print "### Usage:   ",sys.argv[0]," <QCDInverted multicrab dir>"
    print
    sys.exit()

def found(word,filepath):
    command = "grep " + word + " " + filepath
    grep = execute(command)
    if grep != []:
        return True
    return False
    
def QCDInvertedDir(dirs):
    if len(dirs) > 1:
        print "More than 1 dir given, specify only one multicrab dir for QCDInverted"
        return False
    if not os.path.isdir(dirs[0]):
        print dirs[0],"not a directory"
        return False
    if not os.path.exists(os.path.join(dirs[0],"multicrab.cfg")):
        print "No multicrab.cfg found under",dirs[0]
        return False
    if not found("InvertedTau",os.path.join(dirs[0],"multicrab.cfg")):
        return False
    return True
        
def main():

    if len(sys.argv) == 1:
        usage()

    if not QCDInvertedDir(sys.argv[1:]):
        print "No QCD inverted dir recognized from input",sys.argv[1:]
        usage()

    dirQCDInv = sys.argv[1]
    dirs = []
    dirs.append(dirQCDInv)

    print "QCDInverted multicrab directory",dirQCDInv
    print 

                                        
    taskDir = multicrab.createTaskDir("QCDInverted")

    f = open(os.path.join(taskDir, "codeVersion.txt"), "w")
    f.write(git.getCommitId()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeStatus.txt"), "w")
    f.write(git.getStatus()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeDiff.txt"), "w")
    f.write(git.getDiff()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "inputInfo.txt"), "w")
    f.write("Original directory:\n%s\n\n" % "\n".join(dirQCDInv))
    f.write("\nQCDInverted analysis: %s\n" % analysis)
    f.close()
    f = open(os.path.join(taskDir, "multicrab.cfg"), "w")
    f.write("[Data]\n")
    f.write("CMSSW.pset = signalAnalysisInvertedTau_cfg.py\n")
    f.close()

        
    creator = dataset.readFromMulticrabCfg(directory=dirQCDInv)
    optModes = []#creator.getOptimizationModes()
    optModes.append("")
    dataEras = creator.getDataEras()
    dataEras = []
#    dataEras.append("Run2011A")
#    dataEras.append("Run2011AB")
    dataEras.append("Run2011B")
    print "optModes",optModes
    print "dataEras",dataEras

    directory = os.path.join(taskDir, "Data", "res")
    os.makedirs(directory)

    fOUT = ROOT.TFile.Open(os.path.join(directory, "histograms-Data.root"), "RECREATE")

    lumiSaved = False    
    for optMode in optModes:
	for dataEra in dataEras:

            datasetsQCDInv = creator.createDatasetManager(dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
            datasetsQCDInv.loadLuminosities()
            datasetsQCDInv.updateNAllEventsToPUWeighted()

            plots.mergeRenameReorderForDataMC(datasetsQCDInv)
            
            datasetsQCDInv.mergeData()
            datasetsQCDInv.merge("EWK", ["WJets", "DYJetsToLL", "SingleTop", "Diboson","TTJets"], keepSources=True)
            
            if not lumiSaved:
                # Save luminosity
                data = {"Data": datasetsQCDInv.getDataset("Data").getLuminosity()}
                f = open(os.path.join(taskDir, "lumi.json"), "w")
                json.dump(data, f, indent=2)
                f.close()
		lumiSaved = True
    
            anadir = fOUT.mkdir(analysis+searchMode+dataEra+optMode)

            anadir.cd()
            integrals = []
            for massPlot in massPlots:
                print "Processing",massPlot
                massPlotDir = anadir.mkdir(massPlot)
                anadir.cd(massPlot)
                integral = write(fOUT,datasetsQCDInv,[massPlot])
                integrals.append(integral[0])

  	    for controlPlot in controlPlots:
                print "Processing",controlPlot
                controlPlotDir = anadir.mkdir(controlPlot)
                anadir.cd(controlPlot)
                controlPlotNames = datasetsQCDInv.getDataset("Data").getDirectoryContent(controlPlot)
                controlPlotNamesWithPaths = []
                for controlPlotName in controlPlotNames:
                    controlPlotNamesWithPaths.append(os.path.join(controlPlot,controlPlotName))
                write(fOUT,datasetsQCDInv,controlPlotNamesWithPaths)
                anadir.cd()

    	    counterdir = anadir.mkdir("counters")
            anadir.cd("counters")
            counter = ROOT.TH1D("counter","counter",len(integrals),0,len(integrals))
            for i,integral in enumerate(integrals):
                binLabel = "integral_"+massPlots[i]
                counter.SetBinContent(i+1,integral)
                counter.GetXaxis().SetBinLabel(i+1,binLabel)
            counter.Write()
            weighteddir = counterdir.mkdir("weighted")
            weighteddir.cd()
            counter.Write()

    addConfigInfo(fOUT, datasetsQCDInv.getDataset("Data"))
    
    fOUT.Close()

    print "Created multicrab-like dir for LandS:",taskDir


def binFromTitle(title):
    binlt_re = re.compile("#.*(?P<value><\d+)")
    match = binlt_re.search(title)
    if match:
	return match.group("value")
    bineq_re = re.compile("#.*=(?P<value>\d+\.\.\d+)")
    match = bineq_re.search(title)
    if match:
	return match.group("value")
    bingt_re = re.compile("#.*(?P<value>>\d+)")
    match = bingt_re.search(title)
    if match:
	return match.group("value")

    print "Function binFromTitle: Histogram title",title,"did not match re's"
    sys.exit() 
    return None

from QCDInvertedNormalizationFactors import *
def sumHistoBins(datasets,histonames,newname="",newtitle="",rebin = 1):

    if len(histonames) == 0:
	print "No histograms to sum, exiting.."
	sys.exit()

    histos = []
    for histoname in histonames:
        histo_tmp = plots.PlotBase([datasets.getDataset("Data").getDatasetRootHisto(histoname)])
        histo_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
        histo = histo_tmp.histoMgr.getHisto("Data").getRootHisto().Clone()
	ptbin = binFromTitle(histo.GetTitle())
	if not ptbin in QCDInvertedNormalization.keys():
	    print "Key",ptbin,"not found in QCDInvertedNormalization."
	    print "Available keys:",QCDInvertedNormalization.keys() 
	    continue

        histo.Scale(QCDInvertedNormalization[ptbin])

        histoEWK_tmp = plots.PlotBase([datasets.getDataset("EWK").getDatasetRootHisto(histoname)])
        histoEWK_tmp.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
        histoEWK_tmp.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))
        histoEWK = histoEWK_tmp.histoMgr.getHisto("EWK").getRootHisto().Clone()
        histoEWK.Scale(QCDInvertedNormalization[ptbin+"EWK"])

        histo.Add(histoEWK, -1)
        histos.append(histo)

    sum = histos[0].Clone("sum")
    if len(newname)>0:
        sum.SetName(newname)
    if len(newtitle)>0:
        sum.SetTitle(newtitle)
    sum.Reset()

    for histo in histos:
        sum.Add(histo)
    return sum

def write(fOUT,datasets,dirnames,newnames = []):
    integrals = []
    for i,dirname in enumerate(dirnames):
	name = os.path.basename(dirname)
	if len(newnames) == len(dirnames):
	    name = massPlotNames[i]#+"_"+dirname.replace("/","_")
        print "check write dirname",dirname
        histonames = datasets.getDataset("Data").getDirectoryContent(dirname)
        print "check write histonames",histonames
	if histonames == None:
	    continue
	histonamesWithPath = []
	for histoname in histonames:
	    histonamesWithPath.append(os.path.join(dirname,histoname))    
	histo = sumHistoBins(datasets,histonamesWithPath,name,"Inverted tau ID",rebin=rebin)
	histo.Write()
	integrals.append(histo.Integral(0, histo.GetNbinsX()+1))

    return integrals
                          
if __name__ == "__main__":
    main()
