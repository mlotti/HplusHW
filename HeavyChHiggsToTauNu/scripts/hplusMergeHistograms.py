#!/usr/bin/env python

import os, re
import sys
import glob
import shutil
import subprocess
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

re_histos = []
re_se = re.compile("newPfn =\s*(?P<url>\S+)")
replace_madhatter = ("srm://madhatter.csc.fi:8443/srm/managerv2?SFN=", "root://madhatter.csc.fi:1094")

def getHistogramFile(stdoutFile):
    multicrab.assertJobSucceeded(stdoutFile)
    histoFile = None
    f = open(stdoutFile)
    for line in f:
        for r in re_histos:
            m = r.search(line)
            if m:
                histoFile = m.group("file")
                break
        if histoFile is not None:
            break
    f.close()
    return histoFile

def getHistogramFileSE(stdoutFile):
    multicrab.assertJobSucceeded(stdoutFile)
    histoFile = None
    f = open(stdoutFile)
    for line in f:
        m = re_se.search(line)
        if m:
            histoFile = m.group("url")
            break
    f.close()
    if histoFile != None:
        if not replace_madhatter[0] in histoFile:
            raise Exception("Other output SE's than madhatter are not supported at the moment (encountered PFN %s)"%histoFile)
        histoFile = histoFile.replace(replace_madhatter[0], replace_madhatter[1])
    return histoFile

def main(opts, args):
    crabdirs = multicrab.getTaskDirectories(opts)

    global re_histos
    re_histos.append(re.compile("^output files:.*?(?P<file>%s)" % opts.input))
    re_histos.append(re.compile("^\s+file\s+=\s+(?P<file>%s)" % opts.input))

    mergedFiles = []
    for d in crabdirs:
        d = d.replace("/", "")
        stdoutFiles = glob.glob(os.path.join(d, "res", "CMSSW_*.stdout"))

        files = []
        for f in stdoutFiles:
            try:
                if opts.filesInSE:
                    histoFile = getHistogramFileSE(f)
                    if histoFile != None:
                        files.append(histoFile)
                    else:
                        print "Task %s, skipping job %s: input root file not found from stdout" % (d, f)
                else:
                    histoFile = getHistogramFile(f)
                    if histoFile != None:
                        path = os.path.join(os.path.dirname(f), histoFile)
                        if os.path.exists(path):
                            files.append(path)
                        else:
                            print "Task %s, skipping job %s: input root file found from stdout, but does not exist" % (d, f)
                    else:
                        print "Task %s, skipping job %s: input root file not found from stdout" % (d, f)
            except multicrab.ExitCodeException, e:
                print "Task %s, skipping job %s: %s" % (d, f, str(e))

        if len(files) == 0:
            print "Task %s, skipping, no files to merge" % d
            continue
        for f in files:
            if not os.path.isfile(f):
                raise Exception("File %s is marked as output file in the  CMSSW_N.stdout, but does not exist" % f)

        filesSplit = []
        if opts.filesPerMerge < 0:
            filesSplit = [(0, files)]
        else:
            i = 0
            def beg(ind):
                return ind*opts.filesPerMerge
            def end(ind):
                return (ind+1)*opts.filesPerMerge
            while beg(i) < len(files):
                filesSplit.append((i, files[beg(i):end(i)]))
                i += 1

        if len(filesSplit) == 1:
            print "Task %s, merging %d file(s)" % (d, len(files))
        else:
            print "Task %s, merging %d file(s) to %d files" % (d, len(files), len(filesSplit))

        # If testing, end this iteration here
        if opts.test:
            continue

        for index, inputFiles in filesSplit:
            tmp = d
            if len(filesSplit) > 1:
                tmp += "-%d" % index
            mergeName = os.path.join(d, "res", opts.output % tmp)
            #cmd = "mergeTFileServiceHistograms -o %s -i %s" % ("histograms-"+d+".root", " ".join(files))
            #print files
            #ret = subprocess.call(["mergeTFileServiceHistograms",
            #                       "-o", mergeName,
            #                       "-i"]+files)
               
            if os.path.exists(mergeName):
                shutil.move(mergeName, mergeName+".backup")

            cmd = ["hadd"]
            if opts.filesInSE:
                cmd.append("-T") # don't merge TTrees via xrootd
            cmd.append(mergeName)
            cmd.extend(files)

            p = subprocess.Popen(["hadd", mergeName]+inputFiles, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p.communicate()[0]
            ret = p.returncode
            if ret != 0:
                print output
                print "Merging failed with exit code %d" % ret
                return 1

            # FIXME: add here reading of first xrootd file, finding all TTrees, and writing the TList to mergeName file
            if opts.filesInSE:
                raise Exception("--filesInSE feature is not fully implemented")

            if len(filesSplit) > 1:
                print "  done %d" % index
            mergedFiles.append((mergeName, inputFiles))
    
    # If testing, finish here
    if opts.test:
        return 0

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
    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Just test, do not do any merging or deleting (might be useful for checking what would happen)")
    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files)")
    parser.add_option("--filesPerMerge", dest="filesPerMerge", default=-1, type="int",
                      help="Merge at most this many files together, possibly resulting to multiple merged files. Use case: large ntuples. (default: -1 to merge all files to one)")
    parser.add_option("--filesInSE", dest="filesInSE", default=False, action="store_true",
                      help="The ROOT files to be merged are in an SE, merge the files from there. File locations are read from CMSSW_*.stdout files. NOTE: TTrees are not merged (it is assumed that due to TTrees the files are so big that they have to be stored in SE), but are replaced with TList of strings of the PFN's of the files via xrootd protocol.")
    
    (opts, args) = parser.parse_args()

    if opts.filesPerMerge == 0:
        parser.error("--filesPerMerge must be non-zero")

    sys.exit(main(opts, args))
