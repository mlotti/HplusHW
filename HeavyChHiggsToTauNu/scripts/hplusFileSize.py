#!/usr/bin/env python

import subprocess
import tempfile
import sys
import os
import re

from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

def addToDict(d, key, num):
    old = d.get(key, 0)
    d[key] = old + num

def pretty(num):
    divisions = 0
    value = float(num)
    while value > 1024:
        value = value / 1024.0
        divisions += 1
    units = {0: "B", 1: "kB", 2: "MB", 3: "GB"}
    return "%.1f %s" % (value, units[divisions])

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
        macro = tempfile.NamedTemporaryFile(suffix=".C")
        macroname = os.path.basename(macro.name).replace(".C", "")
        macro.write("void %s(){\n TTree *tree=_file0->Get(\"%s\");\n tree->Print();\n}" % (macroname, opts.tree))
        macro.flush()

        sizes = {}
        branch_re = re.compile("Br\s*\d+\s*:(?P<branch>\S+)")
        br_vec_sub_re = re.compile("\[(?P<parent>\S+?)_\]")
        br_size_re = re.compile("Entries\s*:\s*(?P<entries>\d+).*File Size\s*=\s*(?P<size>\d+)")
        tree_size_re = re.compile("Entries\s*:\s*(?P<entries>\d+).*File  Size\s*=\s*(?P<size>\d+)")

        p = subprocess.Popen(["root", "-l", "-n", "-q", rootfile, macro.name], stdout=subprocess.PIPE)
        output = p.communicate()[0]

        currentBranch = None
        entries = None
        for line in output.split("\n"):
            if entries == None:
                m = tree_size_re.search(line)
                if m:
                    entries = int(m.group("entries"))
                    continue
            
            m = branch_re.search(line)
            if m: 
                currentBranch = m.group("branch")

            m = br_vec_sub_re.search(line)
            if m:
                currentBranch = m.group("parent")
                
            m = br_size_re.search(line)
            if m:
                addToDict(sizes, currentBranch, int(m.group("size")))

        macro.close()

        items = sizes.items()
        items.sort(key=lambda x: x[1])

        width = max([len(s) for s in sizes.iterkeys()])
        format = "%-"+str(width)+"s: %s"

        totalSize = 0
        for key, value in items:
            totalSize += value
            print format % (key, pretty(value))
        print
        print "Total %s, %d entries => %s/entry" % (pretty(totalSize), entries, pretty(float(totalSize)/entries))

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] root_file")
    parser.add_option("--tree", dest="tree", default="",
                      help="Print the sizes of TTree branches. Give the path to the TTree.")

    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("You should give exactly one root_file, got %d" % len(args))
    
    sys.exit(main(opts, args))
