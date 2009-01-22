#!/usr/bin/env python
import re
import os
import sys

config = {"analysis": {"dir": "relval_ttbar_muons2taus_cmssw223_run1",
                       "queue": "1nh"},
          "analysis_noMerge": {"dir": "relval_ttbar_muons_removed_cmssw223_run1",
                               "queue": "1nh"}}

phase = "analysis"
#phase = "analysis_noMerge"

job = "analysis.job.sh"

submit = "qsub"
lsDir = "srm://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/MyEventData/muon2tau/%s" % config[phase]["dir"]
outputDir = "gsidcap://pacific02.csc.fi:22128/pnfs/csc.fi/data/cms/Events_matti/muon2tau/%s" % config[phase]["dir"]
root_re = re.compile("(?P<file>([^']*\.root))")

def main(argv):
    if len(argv) != 1:
        print "Usage: qsubmit.py <listfile>"
        return 1

    file = argv[0]

    # Check output directory existence
    ret = os.system("srmls %s >/dev/null 2>&1" % lsDir)
    if ret != 0:
        ret = os.system("srmmkdir %s" % lsDir)
        if ret != 0:
            return 1
        
    outputFile = phase+".root"
    ret = os.system("srmls %s/%s > /dev/null 2>&1" % (lsDir, outputFile))
    if ret != 0:
        cmd = "%s %s %s %s %s" % (submit, job, file, outputDir, outputFile)
        print cmd
        os.system(cmd)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
