#!/usr/bin/env python

import os
import sys
import glob
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

import ROOT

class Dataset:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    def getName(self):
        return self.name

    def setCrossSection(self, value):
        self.info["crossSection"] = value

    def getCrossSection(self):
        return self.info["crossSection"]

    def setAllEvents(self, allevTuple):
        self.normFactor = self.getCrossSection() / allevTuple[1]

    def getNormFactor(self):
        return self.normFactor

class Counter:
    def __init__(self, dataset, counter):
        self.dataset = dataset
        self.data = counter

    def getNames(self):
        return [x[0] for x in self.data]

    def getDataset(self):
        return self.dataset

    def getCounterValue(self, index):
        return self.data[index][1]

    def getCounterCrossSection(self, index):
        return self.dataset.getNormFactor() * self.getCounterValue(index)


class EventPrinter:
    def value(self, dataset, ictr):
        return dataset.getCounterValue(ictr)
    def format(self, width):
        return "%%%dd"%width
    def name(self):
        return "(events)"

class CrossSectionPrinter:
    def value(self, dataset, ictr):
        return dataset.getCounterCrossSection(ictr)
    def format(self, width):
        return "%%%d.4g"%width
    def name(self):
        return "(cross section in pb)"

def printCounter(counter, printer):
    if len(counter) == 0:
        return

    counters = counter[0].getNames()
    maxlen = max([len(x) for x in counters])

    clen = []
    for dataset in counter:
        clen.append(max(15, len(dataset.getDataset().getName())+2))

    lfmt = "%%-%ds" % (maxlen+2)
    dfmt = "%%%ds"

    hdr = lfmt % "Counter"
    for i, cdataset in enumerate(counter):
        hdr += (dfmt%clen[i]) % cdataset.getDataset().getName()
    print hdr

    for ictr, ctr in enumerate(counters):
        line = lfmt % ctr

        for i, dataset in enumerate(counter):
            line += printer.format(clen[i]) % printer.value(dataset, ictr)

        print line

def printDatasetInfo(counter):
    col1hdr = "Dataset"
    col2hdr = "Cross section (pb)"
    col3hdr = "Norm. factor"

    maxlen = max([len(x.getDataset().getName()) for x in counter]+[len(col1hdr)])
    c1fmt = "%%-%ds" % (maxlen+2)
    c2fmt = "%%%d.4g" % (len(col2hdr)+2)
    c3fmt = "%%%d.4g" % (len(col3hdr)+2)

    print (c1fmt%col1hdr)+"  "+col2hdr+"  "+col3hdr
    for cdataset in counter:
        dataset = cdataset.getDataset()
        print (c1fmt % dataset.getName()) + c2fmt%dataset.getCrossSection() + c3fmt%dataset.getNormFactor()


def main(opts):
    taskdirs = multicrab.getTaskDirectories(opts)

    crossSections = {}
    for o in opts.xsections:
        (name, value) = o.split(":")
        crossSections[name] = float(value)

    mainCounters = []
    subCounters = {}

    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", opts.input))
        if len(files) > 1:
            print "Error: only one file should match the input (%d matched) for task %s" % (len(files), d)
            return 1
        elif len(files) == 0:
            print "Error: no files matched to input for task %s" % d
            return 1


        f = ROOT.TFile.Open(files[0])
        info = counter.rescaleInfo(counter.histoToDict(f.Get("configInfo").Get("configinfo")))

        dataset = Dataset(d, info)
        if d in crossSections:
            dataset.setCrossSection(crossSections[d])

        directory = f.Get(opts.counterdir)
        dirlist = directory.GetListOfKeys()
        diriter = dirlist.MakeIterator()
        key = diriter.Next()

        while key:
            # main counter
            if key.GetName() == "counter":
                ctr = counter.histoToCounter(key.ReadObj())
                dataset.setAllEvents(ctr[0])
                mainCounters.append( Counter(dataset, ctr) )
            else:
                if key.GetName() in subCounters:
                    #subCounters[d][key.GetName()] = counter.histoToCounter(key.ReadObj())
                    subCounters[key.GetName()].append( Counter(dataset, counter.histoToCounter(key.ReadObj())) )
                else:
                    #subCounters[d] = {key.GetName(): counter.histoToCounter(key.ReadObj())}
                    subCounters[key.GetName()] = [ Counter(dataset, counter.histoToCounter(key.ReadObj())) ]

            key = diriter.Next()

    print "============================================================"
    print "Dataset info: "
    printDatasetInfo(mainCounters)
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
    printCounter(mainCounters, printer)
    print 

    for key, sub in subCounters.iteritems():
        print "============================================================"
        print "Subcounter %s %s: " % (key, printer.name())
        printCounter(sub, printer)
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
