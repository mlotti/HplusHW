#!/usr/bin/env python

import os
import sys
import glob
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.counter as counter

def main(opts):
    datasets = None
    if len(opts.files) > 0:
        datasets = dataset.getDatasetsFromRootFiles( [(x,x) for x in opts.files], opts=opts, weightedCounters=opts.weighted)
    else:
        datasets = dataset.getDatasetsFromMulticrabCfg(opts=opts, weightedCounters=opts.weighted)

    if os.path.exists(opts.lumifile):
        datasets.loadLuminosities(opts.lumifile)

    if opts.weighted and opts.PUreweight:
        datasets.updateNAllEventsToPUWeighted(era=opts.dataEra)

    if opts.mergeData:
        datasets.mergeData()

    eventCounter = counter.EventCounter(datasets)
    

    print "============================================================"
    if opts.printInfo:
        print "Dataset info: "
        datasets.printInfo()
        print

    quantity = "events"
    if opts.mode == "events":
        pass
    elif opts.mode in ["xsect", "xsection", "crosssection", "crossSection", "eff"]:
        if not opts.PUreweight:
            print "Mode '%s' works only with PU reweighting, which you disabled with --noPUreweight" % opts.mode
            return 1
        eventCounter.normalizeMCByCrossSection()
        quantity = "MC by cross section, data by events"
    else:
        print "Printing mode '%s' doesn't exist! The following ones are available 'events', 'xsect', 'eff'" % opts.mode
        return 1

    cellFormat = counter.CellFormatText(valueOnly=opts.valueOnly, valueFormat=opts.format)
    formatFunc = lambda table: table.format(counter.TableFormatText(cellFormat))
    csvSplitter = counter.TableSplitter([" +- ", " +", " -"])
    if opts.csv:
        formatFunc = lambda table: table.format(counter.TableFormatText(cellFormat, columnSeparator=","), csvSplitter)
    if opts.mode == "eff":
        cellFormat = counter.CellFormatText(valueFormat="%.4f", valueOnly=opts.valueOnly)
        formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatText(cellFormat))
        quantity = "Cut efficiencies"
        if opts.csv:
            formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatText(cellFormat, columnSeparator=","), csvSplitter)

    if opts.subCounter is not None:
        print "============================================================"
        print "Subcounter %s %s: " % (opts.subCounter, quantity)
        print formatFunc(eventCounter.getSubCounterTable(opts.subCounter))
        print

        return 0


    print "============================================================"
    print "Main counter %s: " % quantity
    print formatFunc(eventCounter.getMainCounterTable())
    print 

    if not opts.mainCounterOnly:
        names = eventCounter.getSubCounterNames()
        names.sort()
        for name in names:
            print "============================================================"
            print "Subcounter %s %s: " % (name, quantity)
            print formatFunc(eventCounter.getSubCounterTable(name))
            print

    # print

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    dataset.addOptions(parser)
    parser.add_option("--weighted", dest="weighted", default=False, action="store_true",
                      help="Use weighted counters (i.e. adds '/weighted' to the counter directory path)")
    parser.add_option("--noPUreweight", dest="PUreweight", default=True, action="store_false",
                      help="Don't use PU weighted number of all events. Works only with 'events' mode.")
    parser.add_option("--mode", "-m", dest="mode", type="string", default="events",
                      help="Output mode; available: 'events', 'xsect', 'eff' (default: 'events')")
    parser.add_option("--csv", dest="csv", action="store_true", default=False,
                      help="Print in CSV format")
#    parser.add_option("--format", "-f", dest="format", type="string", default="text",
#                      help="Output format; available: 'text' (default: 'text')")
    parser.add_option("--mainCounterOnly", dest="mainCounterOnly", action="store_true", default=False,
                      help="By default the main counter and the subcounters are all printed. With this option only the main counter is printed")
    parser.add_option("--subCounter", dest="subCounter", type="string", default=None,
                      help="If given, print only this subcounter")
    parser.add_option("--format", dest="format", default="%.1f",
                       help="Value format string (default: '%.1f')")
    parser.add_option("--lumifile", dest="lumifile", type="string", default="lumi.json",
                      help="The JSON file to contain the dataset integrated luminosities")
    parser.add_option("--noinfo", dest="printInfo", action="store_false", default=True,
                      help="Don't print the dataset info")
    parser.add_option("--noerror", dest="valueOnly", action="store_true", default=False,
                      help="Don't print statistical errors")
    parser.add_option("--mergeData", dest="mergeData", action="store_true", default=False,
                      help="Merge all data datasets")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    sys.exit(main(opts))
