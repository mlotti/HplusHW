#!/usr/bin/env python

# Patch CMSSW.sh for skim and embedding steps in order to run cmsRun
# again to just copy the file. This somehow reorganizes the file so
# that reading the result should be faster.

#import tempfile
import subprocess
import shutil
from optparse import OptionParser
import sys
import os
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(opts):
    if len(opts.dirs) == 0:
        print "No directories given"
        return 1

    # (tmph, tmp) = tempfile.mkstemp(suffix=".patch")
    # print tmp

    # src = open("CMSSW_sh.patch")
    # dst = open(tmp, "w")
    # for line in src:
    #     dst.write(line.replace("%%INPUT%%", opts.input))
    # src.close()
    # dst.close()
#    os.remove(tmp)

    patch = ""
    src = open(os.path.join(os.environ["CMSSW_BASE"], "src/HiggsAnalysis/HeavyChHiggsToTauNu/test/tauEmbedding/CMSSW_sh.patch"))
    for line in src:
        patch += line.replace("%%INPUT%%", opts.input)
    src.close()
#    print patch

    taskDirs = multicrab.getTaskDirectories(opts)
    for d in taskDirs:
        cmd = ["patch", "-p0", os.path.join(d, "job", "CMSSW.sh")]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        p.communicate(patch)
        if p.returncode != 0:
            return p.returncode

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("-i", dest="input",
                      help="Input file")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
