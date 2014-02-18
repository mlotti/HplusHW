## \package CombineTools
# Python interface for running Combine with multicrab
#
# The interface for casual user is provided by the functions
# generateMultiCrab() (for LEP-CLs and LHC-CLs) and
# produceLHCAsymptotic (for LHC-CLs asymptotic).
#
# The multicrab configuration generation saves various parameters to
# taskdir/configuration.json, to be used in by combineMergeHistograms.py
# script. The script uses tools from this module, which write the
# limit results to taskdir/limits.json. I preferred simple text format
# over ROOT files due to the ability to read/modify the result files
# easily. Since the amount of information in the result file is
# relatively small, the performance penalty should be negligible.



import os
import re
import sys
import glob
import stat
import json
import time
import random
import shutil
import subprocess
from optparse import OptionParser

import multicrab
import multicrabWorkflows
import git
import aux

## The Combine git tag to be used (see https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit)
Combine_tag = "V03-05-00" # 06.02.2014
validCMSSWversions = ["CMSSW_6_1_1"]
## Common command-line options to Combine

## Command line options for creating Combine workspace
workspacePattern = "combineWorkspaceM%s.root"
workspaceOptionsBrLimitTemplate = "text2workspace.py %s -P HiggsAnalysis.CombinedLimit.ChargedHiggs:brChargedHiggs -o %s"%("%s",workspacePattern)
workspaceOptionsSigmaBrLimit    = "text2workspace.py %s -o combineWorkspaceM%s.root"%("%s",workspacePattern)

## Command line options for running Combine
asymptoticLimit = "combine -M Asymptotic --picky"
asymptoticLimitOptionExpectedOnly = " --run expected"

hybridLimit = "combine -M HybridNew --freq --hintMethod Asymptotic" # --testStat LHC

## Default number of crab jobs
defaultNumberOfJobs = 20

## Default number of first random number seed in the jobs
defaultFirstSeed = 1000


## Deduces from directory listing the mass point list
def obtainMassPoints(pattern):
    commonLimitTools.obtainMassPoints(pattern)

def readLuminosityFromDatacard(myPath, filename):
    commonLimitTools.readLuminosityFromDatacard(myPath, filename)

## Returns true if mass list contains only heavy H+
def isHeavyHiggs(massList):
    commonLimitTools.isHeavyHiggs(massList)

## Returns true if mass list contains only light H+
def isLightHiggs(massList):
    commonLimitTools.isLightHiggs(massList)

#class ParseLandsOutput:
#def parseLandsMLOutput(outputFileName):


## Create OptionParser, and add common LandS options to OptionParser object
#
# \param lepDefault     Boolean for the default value of --lep switch (if None, switch is not added)
# \param lhcDefault     Boolean for the default value of --lhc switch (if None, switch is not added)
# \param lhcasyDefault  Boolean for the default value of --lhcasy switch (if None, switch is not added)
#
# \return optparse.OptionParser object
def createOptionParser(lepDefault=None, lhcDefault=None, lhcasyDefault=None):
    commonLimitTools.createOptionParser(lepDefault, lhcDefault, lhcasyDefault)

## Parse OptionParser object
#
# \param parser   optparse.OptionParser object
#
# \return Options object
def parseOptionParser(parser):
    commonLimitTools.parseOptionParser(parser)

