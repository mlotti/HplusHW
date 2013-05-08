#!/usr/bin/env python

######################################################################
#
# Produce a ROOT file with the histograms/counters from QCDInverted
# with mt constructed in tau pt bins
#
# Based on produceTauEmbeddingResult.py by M. Kortelainen
# Modified for QCD inverted tau method 22.11.2012/S.Lehti
# Updated 7.5.2013/S.Lehti
######################################################################

import os
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

#dataEra = "Run2011A"
#dataEra = "Run2011B"
dataEra = "Run2011AB"

analysis      = "signalAnalysisInvertedTau"
massPlots     = []
massPlotNames = []
controlPlots  = []

rebin = 10

massPlots.append("Inverted/MTInvertedAllCutsTailKiller")
massPlotNames.append("transverseMass")

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
    optModes = creator.getOptimizationModes()

    directory = os.path.join(taskDir, "Data", "res")
    os.makedirs(directory)

    fOUT = ROOT.TFile.Open(os.path.join(directory, "histograms-Data.root"), "RECREATE")
    
    for i,optMode in enumerate(optModes):

	datasetsQCDInv = creator.createDatasetManager(dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
	datasetsQCDInv.loadLuminosities()
	datasetsQCDInv.updateNAllEventsToPUWeighted()

	plots.mergeRenameReorderForDataMC(datasetsQCDInv)

        datasetsQCDInv.mergeData()
        datasetsQCDInv.merge("EWK", ["WJets", "DYJetsToLL", "SingleTop", "Diboson","TTJets"], keepSources=True)

	if i == 0:
	    # Save luminosity
	    data = {"Data": datasetsQCDInv.getDataset("Data").getLuminosity()}
	    f = open(os.path.join(taskDir, "lumi.json"), "w")
	    json.dump(data, f, indent=2)
	    f.close()
    
    	anadir = fOUT.mkdir(analysis+searchMode+optMode)

    	anadir.cd()
    	integrals = write(fOUT,datasetsQCDInv,massPlots,massPlotNames)

    	controlPlotDir = anadir.mkdir("ControlPlots")
    	anadir.cd("ControlPlots")
    	write(fOUT,datasetsQCDInv,controlPlots)
    	anadir.cd()

    	counterdir = anadir.mkdir("counters")
    	anadir.cd("counters")
    	counter = ROOT.TH1D("counter","counter",len(integrals),0,len(integrals))
    	for i,integral in enumerate(integrals):
	    binLabel = "integral"
	    counter.SetBinContent(i+1,integral)
            counter.GetXaxis().SetBinLabel(i+1,binLabel)
        counter.Write()
        weighteddir = counterdir.mkdir("weighted")
        weighteddir.cd()
        counter.Write()

    addConfigInfo(fOUT, datasetsQCDInv.getDataset("Data"))
    
    fOUT.Close()

    print "Created multicrab-like dir for LandS:",taskDir


from plotInvertedControlPlots import sumHistoBins
def write(fOUT,datasets,histonames,newnames = []):
    integrals = []
    for i,histoname in enumerate(histonames):
	name = histoname
	if len(newnames) == len(histonames):
	    name = massPlotNames[i]#+"_"+histoname.replace("/","_")
	histo = sumHistoBins(datasets,histoname,name,"Inverted tau ID",rebin=rebin)
	histo.Write()
	integrals.append(histo.Integral(0, histo.GetNbinsX()+1))

    return integrals
                          
if __name__ == "__main__":
    main()
