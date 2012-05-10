#!/usr/bin/env python

import sys
import subprocess

def main():
    args = sys.argv[1:]

    command = ["hplusMergeHistograms.py", "-i", "split\S+_limits_tree\S*\.root"]+args
    ret = subprocess.call(command)
    if ret != 0:
        raise Exception("hplusMergeHistograms failed with exit code %d, command was\n%s" %(ret, " ".join(command)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
