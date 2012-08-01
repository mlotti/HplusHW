#! /usr/bin/env python                                                                              

import sys
import time
import datetime
import os
import re

reweight_re = re.compile("Lumi/Pileup Reweighting")

def usage():
    print
    print "### Usage:   makePileUpWeight.py <multicrabdir>"
    print
    sys.exit()


def findFileWithPileUpWeights(fName):
    if os.path.isdir(fName):
	dirs = execute("ls %s"%fName)
	for dir in dirs:
	    subpath = os.path.join(fName,dir)
	    if os.path.isdir(subpath):
		subdirs = execute("ls %s"%subpath)
		for subdir in subdirs:
		    if subdir == "res":
			subsubpath = os.path.join(subpath,subdir)
			files = execute("ls %s/*.stdout"%subsubpath)
			for file in files:
			    if not os.path.isdir(file) and PileUpWeightsFound(file):
				return file
    else:
        return fName
    print "NO INPUT FOUND",fName

def PileUpWeightsFound(fName):
    fIN = open(fName)
    for line in fIN:
        match = reweight_re.search(line)
        if match:
            fIN.close()
            return True
    fIN.close()
    return False

def readPileUpWeightData(fName):
    data = []
#    data_re = re.compile("^   \d+ (?P<data>(\d+\.\d+|\d+|\d+\.\d+e\-\d+))")
    data_re = re.compile("^   \d+ (?P<data>(\S+))")
    fIN = open(fName)
    start = False
    for line in fIN:
        if start:
            data_match = data_re.search(line)
            if data_match:
                data.append(data_match.group("data"))
            else:
                return data
        match = reweight_re.search(line)
        if match:
            start = True
    return []

def writeMacro(data):
    fOUT = open("pileupWeight.C","w")

    t = datetime.datetime.now()
    EpochSeconds = time.mktime(t.timetuple())
    now = datetime.datetime.fromtimestamp(EpochSeconds)
    fOUT.write('//Generated on ' + now.ctime() + ' by makePileUpWeight.py\n')

    fOUT.write("double pileupWeightEPS(double npu) {\n")
    fOUT.write("  static double weights[] = {\n")
    for i,w in enumerate(data):
        fOUT.write("    "+w)
        if i < len(data) - 1:
            fOUT.write(",")
        fOUT.write("\n")

    fOUT.write("  };\n")
    fOUT.write("  size_t n = sizeof(weights)/sizeof(double);\n\n")
    fOUT.write("  int index = int(npu);\n")
    fOUT.write("  if(index < 0) index = 0;\n")
    fOUT.write("  if(index >= int(n)) index = n-1;\n\n")
    fOUT.write("  return weights[index];\n")
    fOUT.write("}\n")

    print "Created pileupWeight.C"

def writeRootMacro(fName):
    if PileUpWeightsFound(fName):
        data = readPileUpWeightData(fName)
        writeMacro(data)
    else:
        print "No PU reweight data found in",fName

def execute(cmd):
    f = os.popen(cmd)
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

def main():

    if len(sys.argv) == 1:
        usage()

    fIN = findFileWithPileUpWeights(sys.argv[1])
    writeRootMacro(fIN)
    
if __name__ == "__main__":
    main()
