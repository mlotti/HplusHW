#!/usr/bin/env python

import sys

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(argv):
    if len(argv) != 2:
        print "Expecting exacly one argument, the job range"
        return 1

    print ",".join([str(j) for j in multicrab.prettyToJobList(argv[1])])

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
