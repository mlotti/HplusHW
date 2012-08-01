#!/usr/bin/env python

import os, re
import sys
import glob
import shutil
import subprocess
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

re_histo = None

def getHistogramFile(stdoutFile):
    multicrab.assertJobSucceeded(stdoutFile)
    histoFile = None
    f = open(stdoutFile)
    for line in f:
        m = re_histo.search(line)
        if m:
            histoFile = m.group("file")
            continue
    f.close()
    return histoFile

def main(opts, args):
    crabdirs = multicrab.getTaskDirectories(opts)

    global re_histo
    re_histo = re.compile("^output files:.*?(?P<file>%s)" % opts.input)

    mergedFiles = []
    for d in crabdirs:
        d = d.replace("/", "")
        stdoutFiles = glob.glob(os.path.join(d, "res", "CMSSW_*.stdout"))

        files = []
        for f in stdoutFiles:
            try:
                histoFile = getHistogramFile(f)
                if histoFile != None:
                    files.append(os.path.join(os.path.dirname(f), histoFile))
                else:
                    print "Skipping task %s, job %s: input root file not found" % (d, f)
            except multicrab.ExitCodeException, e:
                print "Skipping task %s, job %s: %s" % (d, f, str(e))
            
        if len(files) == 0:
            print "Task %s, skipping, no files to merge" % d
            continue
        for f in files:
            if not os.path.isfile(f):
                raise Exception("File %s is marked as output file in the  CMSSW_N.stdout, but does not exist" % f)

        print "Task %s, merging %d file(s)" % (d, len(files))

        mergeName = os.path.join(d, "res", opts.output % d)
        #cmd = "mergeTFileServiceHistograms -o %s -i %s" % ("histograms-"+d+".root", " ".join(files))
        #print files
        #ret = subprocess.call(["mergeTFileServiceHistograms",
        #                       "-o", mergeName,
        #                       "-i"]+files)
        if os.path.exists(mergeName):
            shutil.move(mergeName, mergeName+".backup")

        p = subprocess.Popen(["hadd", mergeName]+files, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        ret = p.returncode
        if ret != 0:
            print output
            print "Merging failed with exit code %d" % ret
            return 1
        mergedFiles.append((mergeName, files))

    deleteMessage = ""
    if opts.delete:
        deleteMessage = " (source files deleted)"

    print
    print "Merged histogram files%s:" % deleteMessage
    for f, sourceFiles in mergedFiles:
        print "  %s (from %d file(s))" % (f, len(sourceFiles))
        if opts.delete:
            for srcFile in sourceFiles:
                os.remove(srcFile)

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("-i", dest="input", type="string", default="histograms_.*?\.root",
                      help="Regex for input root files (note: remember to escape * and ? !) (default: 'histograms_.*?\.root')")
    parser.add_option("-o", dest="output", type="string", default="histograms-%s.root",
                      help="Pattern for merged output root files (use '%s' for crab directory name) (default: 'histograms-%s.root')")
    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files)")
    
    (opts, args) = parser.parse_args()

    sys.exit(main(opts, args))
