#!/usr/bin/env python

######################################################################
#
# Produce a ROOT file with the histograms/counters from tau embedding
# as correctly normalized etc.
#
# The input is a set of multicrab directories produced with
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1" command line arguments
# and one multicrab directory with
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=True" in the config file
#
# Author: Matti Kortelainen
# Modified for QCD inverted tau method 22.11.2012/S.Lehti
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

analysis = "signalAnalysisInvertedTau"

############################################################
#
# !!!!  IMPORTANT NOTE  !!!!
#
# Following subtle bug remains
#
# 1. The precision of TH1F is not enough (ok, this is very small
#    effect, 1e-7). We should consider TH1D for all counters.
#
############################################################

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

    print "QCDInverted multicrab directory",dirQCDInv
    print 

    fINname = os.path.join(dirQCDInv,"histogramsForLands.root")
    if not os.path.exists(fINname):
        print "File histogramsForLands.root not found under",dirQCDInv
        print "Did you run plotSignalAnalysisInverted.py?"
        print "Exiting.."
        sys.exit()
                                        
    taskDir = multicrab.createTaskDir("QCDInverted")
    print "Created",taskDir

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

    datasetsQCDInv = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirQCDInv+"/multicrab.cfg", counters=analysis+"/counters", includeOnlyTasks="Tau_")
    datasetsQCDInv.loadLuminosities()
    datasetsQCDInv.mergeData()
        
    # Save luminosity
    data = {"Data": datasetsQCDInv.getDataset("Data").getLuminosity()}
    f = open(os.path.join(taskDir, "lumi.json"), "w")
    json.dump(data, f, indent=2)
    f.close()            

    directory = os.path.join(taskDir, "Data", "res")
    os.makedirs(directory)
    
    fOUT = ROOT.TFile.Open(os.path.join(directory, "histograms-Data.root"), "RECREATE")
    anadir = fOUT.mkdir(analysis)
    fIN = ROOT.TFile.Open(fINname,"R")
    histograms = fIN.GetListOfKeys()
    anadir.cd()
#    fOUT.cd()
#    fOUT.cd(analysis)
    integral = 0
    for h in histograms:
        histo = fIN.Get(h.GetName())
        integral = histo.Integral(0, histo.GetNbinsX()+1)
        histo.Write()
    fIN.Close()

#    anadir.cd()
    counterdir = anadir.mkdir("counters")
    anadir.cd("counters")
    counter = ROOT.TH1D("counter","counter",1,0,1)
    counter.SetBinContent(1,integral)
    counter.GetXaxis().SetBinLabel(1,"integral")
    counter.Write()
    weighteddir = counterdir.mkdir("weighted")
    weighteddir.cd()
    counter.Write()
    addConfigInfo(fOUT, datasetsQCDInv.getDataset("Data"))
    
    fOUT.Close()
                          
if __name__ == "__main__":
    main()
