#!/usr/bin/env python

import sys
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.srm as srm

def main(argv):
    if len(argv) <= 1:
        print_help()
        return 0

    try:
        command = argv[1]
        if command == "help" or command == "-h" or command == "--help":
            print_help()
        elif command == "ls":
            print "\n".join(srm.ls(argv[2:]))
        elif command == "du":
            srm.du(argv[2:])
        elif command == "rm":
            srm.rm(argv[2:])
        elif command == "rmdir":
            srm.rmdir(argv[2:])
        else:
            print "Unkown command %s" % command
            print_help()
    except srm.SrmException, e:
        print "Exception: %s" % str(e)
        print_help()

    return 0


def print_help():
    print "Usage: hplusSrm ls    [-l]    URL"
    print "       hplusSrm rm    [-r -v] URL"
    print "       hplusSrm rmdir [-v]    URL"


if __name__ == "__main__":
    sys.exit(main(sys.argv))
