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
    elif opts.mode in ["xsect", "xsection", "crosssection", "crossSection", "eff"]:
        eventCounter.normalizeMCByCrossSection()
        quantity = "MC by cross section, data by events"
    else:
        print "Printing mode '%s' doesn't exist! The following ones are available 'events', 'xsect', 'eff'" % opts.mode
        return 1

    formatFunc = lambda table: table.format(counter.TableFormatText())
    if opts.mode == "eff":
        formatFunc = lambda table: counter.counterEfficiency(table).format(counter.TableFormatText(counter.CellFormatText(valueFormat="%.4f")))
        quantity = "Cut efficiencies"

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
    parser.add_option("-i", dest="input", type="string", default="histograms-*.root",
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: 'histograms-*.root')")
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")
    parser.add_option("--mode", "-m", dest="mode", type="string", default="events",
                      help="Output mode; available: 'events', 'xsect', 'eff' (default: 'events')")
#    parser.add_option("--format", "-f", dest="format", type="string", default="text",
#                      help="Output format; available: 'text' (default: 'text')")
    parser.add_option("--counterDir", "-c", dest="counterdir", type="string", default="signalAnalysisCounters",
                      help="TDirectory name containing the counters (default: signalAnalysisCounters")
    parser.add_option("--mainCounterOnly", dest="mainCounterOnly", action="store_true", default=False,
                      help="By default the main counter and the subcounters are all printed. With this option only the main counter is printed")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
