#!/usr/bin/env python

import sys
import os
import glob


import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab

failedFiles = []

def GetCrabDirectories(opts):
    #Verbose("GetCrabDirectories()")

    opts2 = None
    crabDirs = multicrab.getTaskDirectories(opts2)
    #crabDirs = GetIncludeExcludeDatasets(crabDirsTmp, opts)
    crabDirs = filter(lambda x: "multicrab_" not in x, crabDirs) #remove "multicrab_" directory from list                                                                                            
    return crabDirs

def exists(rootfile,histogram):
    passed = True
    obj = rootfile.Get(histogram)
    if not obj:
        passed = False
    return passed


def validate(fname):

    passed = True

    fIN = ROOT.TFile.Open(fname)

    # ceck file cleaning
    keys = fIN.GetListOfKeys()
    if len(keys) > 4:
        # not cleaned
        passed = False

    # check pileup histogram
    if not exists(fIN,"configInfo/pileup"):
        passed = False


    fIN.Close()

    if not passed:
        failedFiles.append(fname)

    report = fname+" "
    while len(report) < 120:
        report += "."
    if passed:
        report += '\033[92m Ok\033[0m'
    else:
        report += "\033[91m FAILED\033[0m"
    print report

def main():

    multicrabdir = sys.argv[1]
    if not os.path.exists(multicrabdir) or not os.path.isdir(multicrabdir):
        usage()

    opts = {}
    crabDirs     = GetCrabDirectories(opts)

    for index, d in enumerate(crabDirs):
        histoFiles = glob.glob(os.path.join(d, "results", "histograms*.root"))
        for f in histoFiles:
            validate(f)


    if len(failedFiles) > 0:
        print
        cmd = "rm "
        for f in failedFiles:
            cmd += f + " "
        print cmd


if __name__ == "__main__":
    main()
