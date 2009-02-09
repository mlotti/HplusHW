#!/usr/bin/env python
import re
import os
import sys

from bsubmit import config, job, root_re

phase = "analysis"
#phase = "analysis_noMerge"

submit = "qsub"
baseDir = "/pnfs/csc.fi/data/cms/MyEventData/muon2tau"

def main(argv):
    if len(argv) != 1:
        print "Usage: qsubmit.py <listfile>"
        return 1

    files = []
    f = open(argv[0])
    for line in f:
        m = root_re.search(line)
        if m:
            files.append(m.group("file"));


    lsDir = "srm://madhatter.csc.fi:8443/%s/%s" % (baseDir, config[phase]["dir"])
    outputDir = "gsidcap://pacific01.csc.fi:22128/%s/%s" % (baseDir, config[phase]["dir"])

    # Check output directory existence
    existingOutputFiles = []
    try:
        existingOutputFiles = srmls(lsDir)
    except SrmException:
        ret = os.system("srmmkdir %s" % lsDir)
        if ret != 0:
            return 1
        
    for file in files:
        outputFile = "%s_%s" % (phase, os.path.basename(file))
        if not (lsDir+"/"+outputFile) in existingOutputFiles:
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

class SrmException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
   
def srmls(url):
    ret = []
    max_size = 1

    file_re = re.compile("(?P<size>\d+)\s+(?P<file>\S+)")
    cmd = "/opt/d-cache/srm/bin/srmls -srm_protocol_version=2 -server_mode=passive -streams_num=1 -count=%d -offset=%d"

    count = 500
    iter = 0
    while iter < 100:
        offset = iter*count
        iter += 1

        output = execute("%s %s" % (cmd%(count, offset), url))
        if len(output) > 0 and ("srm" in output[0] and "client" in output[0] and "error" in output[0]):
            raise SrmException("\n".join(output))
        files = []

        for line in output:
            m = file_re.search(line)
            if m:
                size = int(m.group("size"))
                max_size = max(max_size, size)
                files.append((m.group("file"), size)) 
                          
        for f, s in files:
            comp = f.split("/")
            bn = comp[-1]
            if len(bn) == 0:
                bn = comp[-2]
                bn += "/"

            name = url
            url2 = url+"/"
            if url2.find(bn) == -1:
                name = "%s%s" % (url2, bn)

            ret.append((name, s))

        if len(files) < count:
            break

    ret.sort()

    # If srmls returns multiple files for one URL, the URL represents
    # a directory. After sorting, this directory is first, and we
    # remove it.
    if len(ret) > 1:
        ret = ret[1:]

    ret = [x[0] for x in ret]
    
    return ret

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
