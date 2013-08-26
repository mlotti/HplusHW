#!/usr/bin/env python

# This script processes the stdin. Each line issumed to have srm url,
# and for each url the last file/dir is renamed to have TO_BE_DELETED
# prefix and postfix.


import sys
import subprocess
import re

host_re = re.compile("^(?P<host>[^:/]+://[^:/]+(:\d+)?/)(?P<dir>.*)$")

def isNotEmpty(str):
    return len(str) > 0

def removeSlashes(str):
    m = host_re.search(str)
    return m.group("host")+"/".join(filter(isNotEmpty, m.group("dir").split("/")))


def main():
    for url in sys.stdin:
        url = removeSlashes(url)
        m = host_re.search(url)
        comp = filter(isNotEmpty, m.group("dir").split("/"))
        bn = comp[-1]
        path = m.group("host")+"/".join(comp[:-1]) + "/TO_BE_DELETED___"+bn+"___TO_BE_DELETED"

        cmd = ["srmmv", url, path]
        ret = subprocess.call(cmd)
        if ret != 0:
            print "Following command returned %d" % ret
            print cmd
            return ret

    return 0


if __name__ == "__main__":
    sys.exit(main())
