#!/usr/bin/env python

######################################################################
#
# Produce a ROOT file with the histograms/counters from tau embedding
# as correctly normalized etc.
#
# The input is a multicrab directory produced with
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1" command line arguments
#
# Author: Matti Kortelainen
#
######################################################################


import os
import math
import time
import json
import array
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux


def processDirectory(dset, srcDirName, dstDir):
    # Get directories, recurse to them
    dirs = dset.getDirectoryContent(srcDirName, lambda o: isinstance(o, ROOT.TDirectory))
    dirs = filter(lambda n: n != "configInfo", dirs)

    for d in dirs:
        newDir = dstDir.mkdir(d)
        processDirectory(dset, os.path.join(srcDirName, d), newDir)

    # Then process histograms
    histos = dset.getDirectoryContent(srcDirName, lambda o: isinstance(o, ROOT.TH1))
    dstDir.cd()
    for hname in histos:
        drh = dset.getDatasetRootHisto(os.path.join(srcDirName, hname))
        hnew = drh.getHistogram() # TH1
        hnew.SetName(hname)
        hnew.SetDirectory(dstDir)
        if hname not in "SplittedBinInfo":
            tauEmbedding.scaleTauBRNormalization(hnew)
        hnew.Write()
#        ROOT.gDirectory.Delete(hname)
        hnew.Delete()

def main(output, dsetMgr):
    start = time.time()
    dset = dsetMgr.getDataset("Data")

    # Create analysis directory
    tmp = dset
    if not hasattr(tmp, "getSearchMode"):
        tmp = dset.datasets[0]
    analysisDirName = "signalAnalysis"+tmp.getSearchMode()+tmp.getDataEra()+tmp.getOptimizationMode()+tmp.getSystematicVariation()
    analysisDir = output.mkdir(analysisDirName)

    # Create config info directory
    configInfoDir = analysisDir.mkdir("configInfo")
    configInfoDir.cd()
    configInfoHist = ROOT.TH1F("configinfo", "configinfo", 2, 0, 2)
    configInfoHist.SetDirectory(configInfoDir)
    configInfoHist.GetXaxis().SetBinLabel(1, "control")
    configInfoHist.SetBinContent(1, 1)
    configInfoHist.GetXaxis().SetBinLabel(2, "luminosity")
    configInfoHist.SetBinContent(2, dset.getLuminosity())
    configInfoHist.Write()
    configInfoHist.Delete()

    # Process histograms
    processDirectory(dset, "", analysisDir)

    stop = time.time()
    print "Processed in %f.2 s" % (stop-start)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] multicrab-dir")
    parser.add_option("--allEras", dest="allEras", action="store_true", default=False,
                      help="Process all data eras (default is to process the longest one)")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Expected exactly one multicrab directory, got %d" % len(args))

    createArgs = {"directory": args[0], "includeOnlyTasks": "SingleMu"}
    datasetCreator = dataset.readFromMulticrabCfg(**createArgs)
    analysisName = ""
    for a in datasetCreator.getAnalyses():
        if len(a) > len(analysisName):
            analysisName = a
    if len(analysisName) == 0:
        raise Exception("Did not find analysis name")

    # Deduce eras
    eras = datasetCreator.getDataEras()
    letters = {}
    for e in eras:
        letters[e[-1]] = 1
    keys = letters.keys()
    keys.sort()
    tmp = eras[0]
    for k in keys[1:]:
        tmp += k
        eras.append(tmp)
    if not opts.allEras:
        tmp = eras[0]
        for e in eras[1:]:
            if len(e) > len(tmp):
                tmp = e
        eras = [tmp]

    # Create pseudo multicrab directory
    taskDir = multicrab.createTaskDir("embedding")

    f = open(os.path.join(taskDir, "codeVersion.txt"), "w")
    f.write(git.getCommitId()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeStatus.txt"), "w")
    f.write(git.getStatus()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeDiff.txt"), "w")
    f.write(git.getDiff()+"\n")
    f.close()
    # A bit of a kludgy way to indicate for datacard generator that this directory is from embedding (this can be obsolete way)
    f = open(os.path.join(taskDir, "multicrab.cfg"), "w")
    f.write("[Data]\n")
    f.write("dummy = embedded\n\n")
    f.close()
    f = open(os.path.join(taskDir, "inputInfo.txt"), "w")
    f.write("Embedded directory: %s\n" % args[0])

    resdir = os.path.join(taskDir, "Data", "res")
    os.makedirs(resdir)

    configInfoAdded = False

    for searchMode in datasetCreator.getSearchModes():
        for era in eras:
            for optMode in datasetCreator.getOptimizationModes():
                for systVar in [None]+datasetCreator.getSystematicVariations():
                    f.write("Analysis %s, searchMode %s, dataEra %s, optimizationMode %s, systematicVariation %s\n" % (analysisName, searchMode, era, optMode, systVar))
                    dsetMgr = datasetCreator.createDatasetManager(analysisName=analysisName, searchMode=searchMode,
                                                                  dataEra=era, optimizationMode=optMode,
                                                                  systematicVariation=systVar,
                                                                  enableSystematicVariationForData=True)

                    dsetMgr.loadLuminosities()
                    dsetMgr.mergeData()
                    # Open and close result file in order to prevent
                    # per-analysis time blowing up (because of ROOT)
                    if not configInfoAdded:
                        resultFile = ROOT.TFile.Open(os.path.join(resdir, "histograms-Data.root"), "RECREATE")
                        aux.addConfigInfo(resultFile, dsetMgr.getDataset("Data"), addLuminosity=False, dataVersionPostfix="pseudo", additionalText={"analysisName": analysisName})
                        configInfoAdded = True
                    else:
                        resultFile = ROOT.TFile.Open(os.path.join(resdir, "histograms-Data.root"), "UPDATE")

                    main(resultFile, dsetMgr)
                    resultFile.Close()
#                    break
#                break
#            break

    f.close()
    print "Created", taskDir
