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

def splitFiles(files, filesPerEntry):
    if filesPerEntry < 0:
        return [(0, files)]
    i = 0
    ret = []
    def beg(ind):
        return ind*filesPerEntry
    def end(ind):
        return (ind+1)*filesPerEntry
    while beg(i) < len(files):
        ret.append( (i, files[beg(i):end(i)]) )
        i += 1
    return ret

def hadd(opts, mergeName, inputFiles):
    cmd = ["hadd"]
    if opts.filesInSE:
        cmd.append("-T") # don't merge TTrees via xrootd
    cmd.append(mergeName)
    cmd.extend(inputFiles)
    if opts.test:
        print " ".join(cmd)
        return 0
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    ret = p.returncode
    if ret != 0:
        print output
        print "Merging failed with exit code %d" % ret
        return 1
    return 0

def hplusHadd(opts, mergeName, inputFiles):
    intermediateFiles = []
    resultFiles = inputFiles[:]
    mergeRound = 0
    while len(resultFiles) > 1:
        splitted = splitFiles(resultFiles, opts.fastFilesPerMerge)
        resultFiles = []
        for index, files in splitted:
            if len(splitted) > 1 or mergeRound > 0:
                print "     merge round %d, split round %d" % (mergeRound, index)
            target = mergeName+"-m%d-s%d" % (mergeRound, index)
            if os.path.exists(target):
                shutil.move(target, target+".backup")
            cmd = ["hplusHadd.py", target]+files
            if opts.test:
                print " ".join(cmd)
            else:
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = p.communicate()[0]
                ret = p.returncode
                if ret != 0:
                    print output
                    print "Merging failed with exit code %d" % ret
                    return 1
                if "Error in" in output:
                    print output
            resultFiles.append(target)
            intermediateFiles.append(target)
        mergeRound += 1

    if intermediateFiles[-1] != resultFiles[0]:
        raise Exception("Assertion, intermediateFiles[-1] = %s != resultFiles[0] = %s" % (intermediateFiles[-1], resultFiles[0]))
    intermediateFiles.pop()

    for tmp in intermediateFiles:
        if opts.test:
            print "rm %s" % tmp
        else:
            os.remove(tmp)

    if opts.test:
        print "mv %s %s" % (resultFiles[0], mergeName)
    else:
        shutil.move(resultFiles[0], mergeName)
    
    return 0

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

        filesSplit = splitFiles(files, opts.filesPerMerge)
        if len(filesSplit) == 1:
            print "Task %s, merging %d file(s)" % (d, len(files))
        else:
            print "Task %s, merging %d file(s) to %d files" % (d, len(files), len(filesSplit))

        for index, inputFiles in filesSplit:
            tmp = d
            if len(filesSplit) > 1:
                tmp += "-%d" % index
            mergeName = os.path.join(d, "res", opts.output % tmp)
            if os.path.exists(mergeName) and not opts.test:
                shutil.move(mergeName, mergeName+".backup")

            # FIXME: add here reading of first xrootd file, finding all TTrees, and writing the TList to mergeName file
            if opts.filesInSE:
                raise Exception("--filesInSE feature is not fully implemented")

            if len(inputFiles) == 1:
                if opts.test:
                    print "cp %s %s" % (inputFiles[0], mergeName)
                else:
                    shutil.copy(inputFiles[0], mergeName)
                
            else:
                if opts.fast:
                    ret = hplusHadd(opts, mergeName, inputFiles)
                    if ret != 0:
                        return ret
                else:
                    ret = hadd(opts, mergeName, inputFiles)
                    if ret != 0:
                        return ret
    
            if len(filesSplit) > 1:
                print "  done %d" % index
            mergedFiles.append((mergeName, inputFiles))
            if opts.deleteImmediately:
                for srcFile in inputFiles:
                    if opts.test:
                        print "rm %s" % srcFile
                    else:
                        ps.remove(srcFile)
    
    deleteMessage = ""
    if opts.delete:
        deleteMessage = " (source files deleted)"
    if opts.deleteImmediately:
        deleteMessage = " (source files deleted immediately)"

    print
    print "Merged histogram files%s:" % deleteMessage
    for f, sourceFiles in mergedFiles:
        print "  %s (from %d file(s))" % (f, len(sourceFiles))
        if opts.delete and not opts.deleteImmediately:
            for srcFile in sourceFiles:
                if opts.test:
                    print "rm %s" % srcFile
                else:
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
    parser.add_option("--deleteImmediately", dest="deleteImmediately", default=False, action="store_true",
                      help="Delete the source files immediately after merging to save disk space (--delete deletes them after all crab tasks have been merged)")
    parser.add_option("--fast", dest="fast", default=False, action="store_true",
                      help="Use hplusHadd.py instead of hadd, it is faster but works only for TH1's. It also consumes (much) more memory, and is run for a couple of files at a time (see --fastFilesPerMerge).")
    parser.add_option("--fastFilesPerMerge", dest="fastFilesPerMerge", default=4, type="int",
                      help="With --fast, merge this many files at a time (default: 4)")
    parser.add_option("--filesPerMerge", dest="filesPerMerge", default=-1, type="int",
                      help="Merge at most this many files together, possibly resulting to multiple merged files. Use case: large ntuples. (default: -1 to merge all files to one)")
    parser.add_option("--filesInSE", dest="filesInSE", default=False, action="store_true",
                      help="The ROOT files to be merged are in an SE, merge the files from there. File locations are read from CMSSW_*.stdout files. NOTE: TTrees are not merged (it is assumed that due to TTrees the files are so big that they have to be stored in SE), but are replaced with TList of strings of the PFN's of the files via xrootd protocol.")
    
    (opts, args) = parser.parse_args()

    if opts.filesPerMerge == 0:
        parser.error("--filesPerMerge must be non-zero")

    sys.exit(main(opts, args))
