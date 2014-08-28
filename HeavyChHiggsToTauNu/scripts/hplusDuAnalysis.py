#!/usr/bin/env python

import sys
import re
import copy

from optparse import OptionParser

unitOrder = ["B", "kiB", "MiB", "GiB", "TiB"]
class Line:
    def __init__(self, line):
        (self.size, self.unit, self.path) = filter(lambda x: len(x) > 0, line.strip().split(" "))
        self.size = float(self.size)

    def addLineSize(self, line):
        if unitOrder.index(self.unit) < unitOrder.index(line.unit):
            self.size = self.convertSize(line.unit)
            self.unit = line.unit
        self.size += line.convertSize(self.unit)

        div = self.size
        for i in xrange(unitOrder.index(self.unit)+1, len(unitOrder)):
            div = div/1024.
            if div < 1.0:
                break
            self.size = div
            self.unit = unitOrder[i]

    def convertSize(self, unit):
        value = self.size

        fromUnit = unitOrder.index(self.unit)
        toUnit = unitOrder.index(unit)
        if fromUnit > toUnit:
            for i in range(toUnit, fromUnit):
                value = value*1024.
        elif fromUnit < toUnit:
            for i in range(fromUnit, toUnit):
                value = value/1024.

        return value

def lineCmp(a, b):
    if a.unit == b.unit:
        return cmp(a.size, b.size)
    return cmp(unitOrder.index(a.unit), unitOrder.index(b.unit))

def makeRegex(aggregate):
    split = aggregate.split("=")
    if len(split) == 1:
        name = split[0]
        regex = name
    else:
        (name, regex) = split
    return (name, re.compile(regex))

def main(opts, dufile):
    # Read file
    f = open(dufile)
    lines = []
    for line in f:
        lines.append(Line(line))
    f.close()

    # Set the base directory
    srmDir = opts.srmDir
    if srmDir == None:
        srmDir = lines[-1].path

    # Find Line for base directory and immediate subdirectories
    totalLine = None
    subLines = []
    for line in lines:
        if line.path == srmDir:
            totalLine = line
            continue
        if line.path.replace(srmDir+"/", "").count("/") == opts.depth:
            subLines.append(line)

    # Aggregation
    if len(opts.aggregate) > 0:
        aggregates = [makeRegex(a) for a in opts.aggregate]
        notFound = []
        aggregated = {}
        for line in subLines:
            found = False
            for name, regex in aggregates:
                if regex.search(line.path):
                    try:
                        aggregated[name].addLineSize(line)
                    except KeyError:
                        obj = copy.copy(line)
                        obj.path = name
                        aggregated[name] = obj
                    found = True
                    break
            if not found:
                notFound.append(line)
        subLines = notFound + aggregated.values()

    # Sorting
    subLines.sort(cmp=lineCmp, reverse=True)

    # Print results
    print "Total %6.2f %s in %s" % (totalLine.size, totalLine.unit, totalLine.path)
    print "Divided to"
    for line in subLines:
        convSize = line.convertSize(totalLine.unit)
        fraction = convSize / totalLine.size * 100
        
        print "  %4.1f %%  %6.2f %s  %s" % (fraction, line.size, line.unit, line.path)

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] du.txt")
    parser.add_option("--srmDir", dest="srmDir", default=None,
                      help="Specify the srm directory whose content to look (default is to pick the last one in the du.txt file)")
    parser.add_option("-a", "--aggregate", dest="aggregate", default=[], action="append",
                      help="Aggregate directories, 'name=regex', if without '=' interpreted as 'name=name' (i.e. name is used as the regex)")
    parser.add_option("-r", dest="depth", default=0, type="int",
                      help="Recursion depth (default: 0, i.e. look for immediate subdirectories of srmDir")
    (opts, args) = parser.parse_args()
    if not len(args) == 1:
        parser.error("You should give exactly one txt file, got %d" % len(args))

    # One '/' is implicitly included
    if opts.depth < 0:
        parser.error("-r should be >= 0, got %d" % opts.r)

    sys.exit(main(opts, args[0]))
