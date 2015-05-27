#!/usr/bin/env python

import subprocess
import tempfile
import sys
import os
import re
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

class BranchInfo:
    def __init__(self, size, typeName):
        self.size = size
        self.typeName = typeName

# from ROOT printSizes.C
def GetBasketSize(branches, inclusive):
    return sum([GetBasketSizeBranch(b, inclusive) for b in branches])

def GetBasketSizeBranch(branch, inclusive):
    result = 0
    if branch:
        result = branch.GetZipBytes()
        if result <= 0:
            result = branch.GetTotBytes()
        if inclusive:
            result += GetBasketSize(branch.GetListOfBranches(), True)
    return result

def GetTotalSize(branch, inclusive):
    return GetBasketSizeBranch(branch, inclusive)
# end ROOT printSizes.C

def pretty(num):
    divisions = 0
    value = float(num)
    while value > 1024:
        value = value / 1024.0
        divisions += 1
    units = {0: "B", 1: "kB", 2: "MB", 3: "GB"}

    tmp = "%.1f" % value
    fmt = "%%.%df %%s" % (6-len(tmp))
    return fmt % (value, units[divisions])
#    return "%.1f %s" % (value, units[divisions])

def makeRegex(aggregate):
    split = aggregate.split("=")
    if len(split) == 1:
        name = split[0]
        regex = name
    else:
        (name, regex) = split
    return (name, re.compile(regex))

def main(opts, files):
    rootfile = files[0]
    
    macro = tempfile.NamedTemporaryFile(suffix=".C")
    macroname = os.path.basename(macro.name).replace(".C", "")
    macro.write("void %s(){\n  _file0->Map();\n}\n" % macroname)
    macro.flush()

    sizes = {}
    size_re = re.compile("N=(?P<size>\d+)\s+(?P<class>\S+)\s+")
    p = subprocess.Popen(["root", "-l", "-n", "-q", rootfile, macro.name], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    for line in output.split("\n"):
        m = size_re.search(line)
        if m and m.group("class") != "END":
            aux.addToDictList(sizes, m.group("class"), int(m.group("size")))

    macro.close()

    items = []
    for key, valueList in sizes.iteritems():
        items.append( (key, sum(valueList), len(valueList)) )
    items.sort(key=lambda x: x[1])

    if len(sizes) == 0:
        width = 10
    else:
        width = max([len(s) for s in sizes.iterkeys()])
    format = "%-"+str(width)+"s: %s (%d items)"
    
    for name, size, count in items:
        print format % (name, pretty(size), count)

    if opts.tree:
        f = ROOT.TFile.Open(rootfile)
        tree = f.Get(opts.tree)
        entries = tree.GetEntries()

        info = {}
        for branch in tree.GetListOfBranches():
            t = branch.GetClassName() # objects
            if t == "":
                t = branch.GetListOfLeaves()[0].GetTypeName() # basic types
            size = GetTotalSize(branch, True)
            info[branch.GetName()] = BranchInfo(size=size, typeName=t)
        f.Close()

        items = info.items()
        if opts.grep is not None:
            items = filter(lambda x: opts.grep in x[0], items)
        if len(opts.aggregate) > 0:
            aggregates = [makeRegex(a) for a in opts.aggregate]
            notFound = []
            aggregated = {}
            for key, value in items:
                found = False
                for name, regex in aggregates:
                    if regex.search(key):
                        try:
                            aggregated[name].size += value.size
                        except KeyError:
                            aggregated[name] = BranchInfo(value.size, "(aggregated)")
                        found = True
                        break
                if not found:
                    notFound.append( (key, value) )
            items = notFound + aggregated.items()


        if opts.sort_alpha:
            items.sort(key=lambda x: x[0])
        else:
            items.sort(key=lambda x: x[1].size)

        widthName = max([len(s) for s in info.iterkeys()])
        widthType = max([len(x.typeName) for x in info.itervalues()])
        format = "%-"+str(widthName+1)+"s %-"+str(widthType+1)+"s: %10s  %10s"

        print
        print format % ("Branch", "Type", "Compressed", "Fraction")
        totalSize = sum([x[1].size for x in items])
        for key, value in items:
            print format % (key, value.typeName, pretty(value.size), "%.1f %%" % (float(value.size) / totalSize * 100))
        print
        print "Total %s, %d entries => %s/entry" % (pretty(totalSize), entries, pretty(float(totalSize)/entries))

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] root_file")
    parser.add_option("--tree", dest="tree", default="",
                      help="Print the sizes of TTree branches. Give the path to the TTree.")
    parser.add_option("--sort-alpha", dest="sort_alpha", default=False, action="store_true",
                      help="Sort branches alphabetically instead of size")
    parser.add_option("--grep", dest="grep", default=None, type="string",
                      help="Show only branches containing this string")
    parser.add_option("-a", "--aggregate", dest="aggregate", default=[], action="append",
                      help="Aggregate branches, 'name=regex', if without '=' interpreted as 'name=name' (i.e. name is used as the regex)")

    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("You should give exactly one root_file, got %d" % len(args))
    
    sys.exit(main(opts, args))
