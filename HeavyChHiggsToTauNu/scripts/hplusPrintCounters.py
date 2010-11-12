#!/usr/bin/env python

import os
import sys
import glob
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

import ROOT

def main(opts):
    crossSections = {}
    for o in opts.xsections:
        (name, value) = o.split(":")
        crossSections[name] = float(value)

    datasets = None
    if len(opts.files) > 0:
        datasets = dataset.getDatasetsFromRootFiles( [(x,x) for x in opts.files], opts.counterdir )
    else:
        datasets = dataset.getDatasetsFromMulticrabCfg(opts, opts.counterdir)
    eventCounter = counter.EventCounter(datasets)
    

    print "============================================================"
    print "Dataset info: "
    datasets.printInfo()
    print

    quantity = "events"
    if opts.mode == "events":
        pass
    elif opts.mode in ["xsect", "xsection", "crosssection", "crossSection"]:
        eventCounter.normalizeMCByCrossSection()
        quantity = "MC by cross section, data by events"
    else:
        print "Printing mode '%s' doesn't exist! The following ones are available 'events', 'xsect'" % opts.mode
        return 1

    print "============================================================"
    print "Main counter %s: " % quantity
    eventCounter.getMainCounter().printCounter(counter.FloatAutoFormat())
    print 

    if not opts.mainCounterOnly:
        names = eventCounter.getSubCounterNames()
        names.sort()
        for name in names:
            print "============================================================"
            print "Subcounter %s %s: " % (name, quantity)
            eventCounter.getSubCounter(name).printCounter(counter.FloatAutoFormat())
            print

    # print

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")
    parser.add_option("--mode", "-m", dest="mode", type="string", default="events",
                      help="Output mode; available: 'events', 'xsect' (default: 'events')")
#    parser.add_option("--format", "-f", dest="format", type="string", default="text",
#                      help="Output format; available: 'text' (default: 'text')")
    parser.add_option("--xsection", "-x", dest="xsections", type="string", action="append", default=[],
                      help="Override the cross sections in the ROOT file. 'datasetname:xsect' where xsect is the cross section in pb, e.g. 'QCD_Pt170:154'")
    parser.add_option("--counterDir", "-c", dest="counterdir", type="string", default="signalAnalysisCounters",
                      help="TDirectory name containing the counters (default: signalAnalysisCounters")
    parser.add_option("--mainCounterOnly", dest="mainCounterOnly", action="store_true", default=False,
                      help="By default the main counter and the subcounters are all printed. With this option only the main counter is printed")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
