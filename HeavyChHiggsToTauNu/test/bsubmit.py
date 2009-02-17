#!/usr/bin/env python
import re
import os
import sys

config = {"analysis_original": {"dir": "TTJets_Fall08_cmssw2117_original_cmssw223_run1",
                                "queue": "8nh"},
          "analysis": {"dir": "TTJets_Fall08_cmssw2117_muonsReplacedWithTaus_cmssw223_run1",
                       "queue": "8nh"},
          "analysis_noMerge": {"dir": "TTJets_Fall08_cmssw2117_muonsRemoved_cmssw223_run1",
                               "queue": "8nh"}}

phase = "analysis"
#phase = "analysis_noMerge"

job = "analysis.job.sh"

submit = "bsub -q %s" % config[phase]["queue"]
outputDir = "rfio://%s/muon2tau/%s" % (os.environ.get("CASTOR_HOME"), config[phase]["dir"])
root_re = re.compile("(?P<file>([^']*\.root))")

def main(argv):
    if len(argv) != 1:
        print "Usage: bsubmit.py <listfile>"
        return 1

    files = []
    f = open(argv[0])
    for line in f:
        m = root_re.search(line)
        if m:
            files.append(m.group("file"));

    # Check output directory existence
    ret = os.system("rfdir %s >/dev/null 2>&1" % outputDir)
    if ret != 0:
        os.system("rfmkdir -p %s" % outputDir)

    for file in files:
        outputFile = "%s_%s" % (phase, os.path.basename(file))
        ret = os.system("rfdir %s/%s > /dev/null 2>&1" % (outputDir, outputFile))
        if ret != 0:
            cmd = "%s %s %s %s %s" % (submit, job, file, outputDir, outputFile)
            print cmd
            os.system(cmd)

    return 0

def execute(cmd):
    f = os.popen4(cmd)[1]
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
