#!/usr/bin/env python

import os
import sys
import glob
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

import ROOT

class EventPrinter:
    def value(self, counter, ictr):
        return counter.getCounterValue(ictr)
    def format(self, width):
        return "%%%dd"%width
    def name(self):
        return "(events)"

class CrossSectionPrinter:
    def value(self, counter, ictr):
        return counter.getCounterCrossSection(ictr)
    def format(self, width):
        return "%%%d.4g"%width
    def name(self):
        return "(cross section in pb)"

# counters is an array of counter.Counter objects, one element per
# dataset
def printCounter(counters, printer):
    if len(counters) == 0:
        return

    counterNames = counters[0].getNames()
    maxlen = max([len(x) for x in counterNames])

    clen = []
    for counter in counters:
        clen.append(max(15, len(counter.getDataset().getName())+2))

    lfmt = "%%-%ds" % (maxlen+2)
    dfmt = "%%%ds"

    hdr = lfmt % "Counter"
    for i, counter in enumerate(counters):
        hdr += (dfmt%clen[i]) % counter.getDataset().getName()
    print hdr

    for ictr, ctr in enumerate(counterNames):
        line = lfmt % ctr

        for i, counter in enumerate(counters):
            line += printer.format(clen[i]) % printer.value(counter, ictr)

        print line

def printDatasetInfo(datasets):
    col1hdr = "Dataset"
    col2hdr = "Cross section (pb)"
    col3hdr = "Norm. factor"

    maxlen = max([len(x.getName()) for x in datasets]+[len(col1hdr)])
    c1fmt = "%%-%ds" % (maxlen+2)
    c2fmt = "%%%d.4g" % (len(col2hdr)+2)
    c3fmt = "%%%d.4g" % (len(col3hdr)+2)

    print (c1fmt%col1hdr)+"  "+col2hdr+"  "+col3hdr
    for dataset in datasets:
        print (c1fmt % dataset.getName()) + c2fmt%dataset.getCrossSection() + c3fmt%dataset.getNormFactor()

def main(opts):
    taskdirs = multicrab.getTaskDirectories(opts)

    crossSections = {}
    for o in opts.xsections:
        (name, value) = o.split(":")
        crossSections[name] = float(value)

    counters = counter.Counters()

    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", opts.input))
        if len(files) > 1:
            print "Error: only one file should match the input (%d matched) for task %s" % (len(files), d)
            return 1
        elif len(files) == 0:
            print "Error: no files matched to input for task %s" % d
            return 1

        counters.addCounter(counter.readCountersFileDir(files[0], opts.counterdir, d, crossSections))


    print "============================================================"
    print "Dataset info: "
    printDatasetInfo(counters.getDatasets())
    print

    printer = None
    if opts.mode == "events":
        printer = EventPrinter()
    elif opts.mode in ["xsect", "xsection", "crosssection", "crossSection"]:
        printer = CrossSectionPrinter()
    else:
        print "Printing mode '%s' doesn't exist! The following ones are available 'events', 'xsect'" % opts.mode
        return 1

    print "============================================================"
    print "Main counter %s: " % printer.name()
    printCounter(counters.getMainCounters(), printer)
    print 

    for name in counters.getSubCounterNames():
        print "============================================================"
        print "Subcounter %s %s: " % (name, printer.name())
        printCounter(counters.getSubCounters(name), printer)
        print

    print

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("--mode", "-m", dest="mode", type="string", default="events",
                      help="Output mode; available: 'events', 'xsect' (default: 'events')")
#    parser.add_option("--format", "-f", dest="format", type="string", default="text",
#                      help="Output format; available: 'text' (default: 'text')")
    parser.add_option("--xsection", "-x", dest="xsections", type="string", action="append", default=[],
                      help="Override the cross sections in the ROOT file. 'datasetname:xsect' where xsect is the cross section in pb, e.g. 'QCD_Pt170:154'")
    parser.add_option("--counterDir", "-c", dest="counterdir", type="string", default="signalAnalysisCounters",
                      help="TDirectory name containing the counters (default: signalAnalysisCounters")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
