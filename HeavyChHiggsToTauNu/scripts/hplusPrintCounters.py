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
    datasets = None
    if len(opts.files) > 0:
        datasets = dataset.getDatasetsFromRootFiles( [(x,x) for x in opts.files], counters=opts.counterdir)
    else:
        datasets = dataset.getDatasetsFromMulticrabCfg(opts=opts, counters=opts.counterdir)

    if os.path.exists(opts.lumifile):
        datasets.loadLuminosities(opts.lumifile)

    eventCounter = counter.EventCounter(datasets)
    

    print "============================================================"
    print "Dataset info: "
    datasets.printInfo()
    print

    quantity = "events"
    if opts.mode == "events":
        pass
    elif opts.mode in ["xsect", "xsection", "crosssection", "crossSection", "eff"]:
        eventCounter.normalizeMCByCrossSection()
        quantity = "MC by cross section, data by events"
    else:
        print "Printing mode '%s' doesn't exist! The following ones are available 'events', 'xsect', 'eff'" % opts.mode
        return 1

    formatFunc = lambda table: table.format(counter.TableFormatText())
    csvSplitter = counter.TableSplitter([" +- ", " +", " -"])
    if opts.csv:
        formatFunc = lambda table: table.format(counter.TableFormatText(columnSeparator=","), csvSplitter)
    if opts.mode == "eff":
        cellFormat = counter.CellFormatText(valueFormat="%.4f")
        formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatText(cellFormat))
        quantity = "Cut efficiencies"
        if opts.csv:
            formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatText(cellFormat, columnSeparator=","), csvSplitter)

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
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    dataset.addOptions(parser)
    parser.add_option("--mode", "-m", dest="mode", type="string", default="events",
                      help="Output mode; available: 'events', 'xsect', 'eff' (default: 'events')")
    parser.add_option("--csv", dest="csv", action="store_true", default=False,
                      help="Print in CSV format")
#    parser.add_option("--format", "-f", dest="format", type="string", default="text",
#                      help="Output format; available: 'text' (default: 'text')")
    parser.add_option("--mainCounterOnly", dest="mainCounterOnly", action="store_true", default=False,
                      help="By default the main counter and the subcounters are all printed. With this option only the main counter is printed")
    parser.add_option("--lumifile", dest="lumifile", type="string", default="lumi.json",
                      help="The JSON file to contain the dataset integrated luminosities")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
