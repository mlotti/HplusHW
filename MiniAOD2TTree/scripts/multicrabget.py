#!/usr/bin/env python
        
import os
import re
import sys
import subprocess

from CRABAPI.RawCommand import crabCommand            

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <multicrab dir|crab dir>"
    print
    sys.exit()

def main():

    if len(sys.argv) == 1:
        usage()

    dirs = sys.argv[1:]

    datasetdirs = []
    for d in dirs:
        if os.path.exists(d) and os.path.isdir(d):
            datasetdirs.append(os.path.abspath(d))
    if len(dirs) == 0:
        datasetdirs.append(os.path.abspath("."))

    datasets = []
    for d in datasetdirs:
        if os.path.exists(os.path.join(d,"results")):
            datasets.append(d)
        cands = execute("ls -tr %s"%d)
        for c in cands:
            path = os.path.join(d,c)
            if os.path.exists(os.path.join(path,"results")):
                datasets.append(path)

    class Report :
        def __init__(self,name,all,retrieved):
            self.name = name
            self.all  = str(all)
            self.retrieved = str(retrieved)
        def Print(self):
            name = os.path.basename(self.name)
            while len(name) < 30:
                name += " "
            print self.name,"retrieved =",self.retrieved,", all jobs =",self.all

    reports = []

    for d in datasets:
        print
        print os.path.basename(d)
        if os.system("grep Done %s"%os.path.join(d,"crab.log")) == 0: # If Done in the crab.log, skip.
#            print d,"done, skipping.."
            continue
        files = execute("ls %s"%os.path.join(d,"results"))
        try:
#        if 1 > 0:
            res = crabCommand('status', dir = d)
            finished,failed,retrievedLog,retrievedOut = retrievedFiles(d,res)
            if retrievedLog < finished:
                touch(d)
                dummy=crabCommand('getlog', dir = d)
            if retrievedOut < finished:
                dummy=crabCommand('getoutput', dir = d)
                touch(d)
            if failed > 0:
                dummy=crabCommand('resubmit', dir = d)

            finished,failed,retrievedLog,retrievedOut = retrievedFiles(d,res)
            retrieved = min(finished,retrievedLog,retrievedOut)
            alljobs = len(res['jobList'])
#            if len(files) == 0:
#                print "check len(files) == 0",d,alljobs,retrieved
#            print "Check reposrt"
            reports.append(Report(d,alljobs,retrieved))
            if retrieved == alljobs and retrieved > 0:
                os.system("sed -i -e '$a\Done. (Written by multicrabget.py)' %s"%os.path.join(d,"crab.log")) # Printing 'Done.' in crab.log when all output is retrieved.
        except:
            reports.append(Report(d,"?","?"))
            print "crab status command failed, skipping.."
    for r in reports:
        r.Print()


def retrievedFiles(directory,crabResults):
    retrievedLog = 0
    retrievedOut = 0
    finished     = 0
    failed       = 0
    for r in crabResults['jobList']:
        if r[0] == 'finished':
            finished += 1
            foundLog = exists(directory,"cmsRun_%i.log.tar.gz"%r[1])
            foundOut = exists(directory,"*_%i.root"%r[1])
            if foundLog:
                retrievedLog += 1
            if foundOut:
                retrievedOut += 1
        if r[0] == 'failed':
            failed += 1
    return finished,failed,retrievedLog,retrievedOut

def exists(dataset,filename):
    fname = os.path.join(dataset,"results",filename)
    fname = execute("ls %s"%fname)[0]
    return os.path.exists(fname)

def touch(path):
    if os.path.exists(path):
        os.system("touch %s"%path)

def execute(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (s_in, s_out) = (p.stdin, p.stdout)
        
    f = s_out
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
        
    f.close()
    return ret

if __name__ == "__main__":
    main()
