#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

import os
import re
import sys

if len(sys.argv) != 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)


eras = {}
eras["2016"] = "Run2016"

import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

def getDatasetsForEras(dsets,era):
    dset_re = re.compile(era)
    dOUT = []
    for dset in dsets:
        if dset.getDataVersion().isData():
            match = dset_re.search(dset.getName())
            if match:
                dOUT.append(dset)
        else:
            dOUT.append(dset)
    return dOUT

def createAnalyzer(dataVersion,era):
    a = Analyzer("L1Study",
        L1TauPt        = 30,
        L1ETM          = 70,
        TransverseMass = 50
    )
    a.runMin  = runmin
    a.runMax  = runmax
    return a


def addAnalyzer(era):
    process = Process(outputPrefix="L1Study")
    process.addDatasetsFromMulticrab(sys.argv[1])
    ds = getDatasetsForEras(process.getDatasets(),eras[era])
    process.setDatasets(ds)
    global runmin,runmax
    runmin,runmax = process.getRuns()
    process.addAnalyzer("L1Study_"+eras[era], lambda dv: createAnalyzer(dv, era))
    process.run()

addAnalyzer("2016")

