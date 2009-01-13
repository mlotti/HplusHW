#!/usr/bin/env python
import sys
import os
import commands
import getopt
import fileinput
import re

if len(sys.argv) == 1:
    print "\n"
    print "### Usage:   bsubmitAnalyzerJobs.py <data paths file>\n"
    print "### Example: bsubmitAnalyzerJobs.py ../python/QCD_Mike_PFTauFiltered_HighEfficiency.py\n"
    print "\n"
    sys.exit()


ConfigFile  = 'offlineAnalysis_cfg.py'
OutFileName = 'file:analysis.root'
#OutFileName = 'rfio:/castor/cern.ch/user/s/slehti/analysis.root'

root_re = re.compile("(?P<file>'([^']*\.root)')")
cfg_re  = re.compile("(\..*?)$")
out_re = re.compile("[^']*/([^/]*)\.root")
job_re  = re.compile("(\.py)")

i = 0
for dline in fileinput.input():
    match = root_re.search(dline)
    if match:
	i = i + 1
	jobNumber    = '_%i' %(i)
	cfgFileName = cfg_re.sub("%s\g<1>"%jobNumber, ConfigFile)
	inFileName = match.group("file")
	outFileName = cfg_re.sub("%s\g<1>"%jobNumber, OutFileName)


        cfgFile = open(cfgFileName, 'w')
	inFile = open(ConfigFile,'r')
        for line in inFile:
	    if 'outputFileName' in line:
                cfgFile.write('        outputFileName = cms.string("' + outFileName + '")\n')
            elif 'process.source = source' in line:
                cfgFile.write('process.source = cms.Source("PoolSource",\n')
	        cfgFile.write('    fileNames = cms.untracked.vstring(\n')
	        cfgFile.write('        ' + inFileName + '\n')
	        cfgFile.write('    )\n')
	        cfgFile.write(')\n')
	    elif 'input = cms.untracked.int32' in line:
		cfgFile.write('    input = cms.untracked.int32(-1)\n')
	    else:
	        cfgFile.write(line)
	inFile.close()
	cfgFile.close()

	jobFileName = job_re.sub(".job",cfgFileName)
	jobFile = open(jobFileName, 'w')
	jobFile.write("#!/bin/csh\n")
	jobFile.write("#@$-s /bin/csh\n")
	jobFile.write("cd ${LS_SUBCWD}\n")
	jobFile.write("eval `scramv1 runtime -csh`\n")
        jobFile.write("cd ${WORKDIR}\n")
	jobFile.write("cmsRun ${LS_SUBCWD}/" + cfgFileName + "\n")
	jobFile.write("cp *.root ${LS_SUBCWD}\n")
	jobFile.close()

    	cmd = "bsub -q 1nw " + jobFileName
	os.system("chmod +x "+ jobFileName)
    	os.system(cmd)
