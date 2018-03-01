#! /usr/bin/env python
'''
DESCRIPTION:
This module contains a class to identify multicrab dirs from a given directory. 
It Identifies separately the signal, ewk QCDfact and QCDinv dirs. If multiple 
directories are found, the most recent one is taken!
'''

#================================================================================================    
# Import modules
#================================================================================================    
import sys
import os
import re

from HiggsAnalysis.NtupleAnalysis.tools.aux import execute
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

#================================================================================================    
# Class Definition
#================================================================================================    
class MulticrabDirectoryDataType:
    UNKNOWN = 0
    OBSERVATION = 1
    SIGNAL = 2
    EWKTAUS = 3
    EWKFAKETAUS = 4
    QCDMC = 5
    QCDINVERTED = 6
    DUMMY = 7
    DATACARDONLY = 8

class MulticrabPathFinder:
    def __init__(self, path, h2tb=False, verbose=False):
        self._verbose        = verbose
        self._h2tb           = h2tb
        self._multicrabpaths = self.scan(path)
        self._signal_path    = self.signalfind(self._multicrabpaths)
        self._ewk_path       = self.ewkfind(self._multicrabpaths)
        self._qcdfact_path   = self.qcdfactfind(self._multicrabpaths)
        self._qcdinv_path    = self.qcdinvfind(self._multicrabpaths)
        self._fakeB_path     = self.fakeBfind(self._multicrabpaths)

    def Verbose(self, msg, printHeader=True):
        '''
        Calls Print() only if verbose options is set to true
        '''
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def Print(self, msg, printHeader=True):
        '''
        Simple print function. If verbose option is enabled prints, otherwise does nothing
        '''
        fName = __file__.split("/")[-1]
        fName = fName.replace(".pyc", ".py")
        if printHeader:
            print "=== ", fName
        print "\t", msg
        return

    def PrintInfo(self):
        table = []
        align = "{:>20} {:^1} {:<130}"
        title = align.format("Variable", "", "Value")
        hLine = 150*"="
        table.append(hLine)
        table.append(title)
        table.append(hLine)
        table.append( align.format("Verbose"        , "", self._verbose) )
        table.append( align.format("h2tb"           , "", self._h2tb) )
        table.append( align.format("#Multicrab Dirs", "", len(self._multicrabpaths)) )
        table.append( align.format("Signal Path"    , "", self._signal_path ) )
        table.append( align.format("EWK Path"       , "", self._ewk_path) )
        table.append( align.format("QCD Factorised" , "", self._qcdfact_path) )
        table.append( align.format("QCD Inverted"   , "", self._qcdinv_path ) )
        table.append(hLine)
        table.append("")
        for row in table:
            self.Print(row, False)
        return

    def getFakeBPath(self):
        return self.self.getFakeBPath()

    def getFakeBExists(self):
        return os.path.exists(self.getFakeBPath())

    def getQCDFactorisedExists(self):
        return os.path.exists(self.getQCDfacPath())

    def getQCDFactorisedPath(self):
        return self.getQCDfacPath()

    def getQCDInvertedExists(self):
        return os.path.exists(self.getQCDinvPath())

    def getQCDInvertedPaths(self):
        return self.getSignalPath(),self.getEWKPath(),self.getQCDinvPath()

    def getQCDInvertedPath(self):
        return self.getQCDinvPath()

    def getSignalPath(self):
        return self._signal_path

    def getEWKMCPath(self):
        return self._signal_path

    def getQCDMCPath(self):
        return self._signal_path

    def getGenuineBPath(self):
        return self._signal_path

    def getEWKPath(self):
        return self._ewk_path

    def getFakeBPath(self):
        return self._fakeB_path

    def getQCDfacPath(self):
        return self._qcdfact_path

    def getQCDinvPath(self):
        return self._qcdinv_path

    def getSubPaths(self, path, regexp, exclude=False):
	retDirs = []
	dirs = execute("ls %s"%path)
	path_re = re.compile(regexp)
	multicrab_re = re.compile("^multicrab_")
	for dir in dirs:
	    fulldir = os.path.join(path,dir)
	    if os.path.isdir(fulldir):
		match = path_re.search(dir)
		if match and not exclude:
		    retDirs.append(dir)
		if not match and exclude:
		    multicrabmatch = multicrab_re.search(dir)
		    if not multicrabmatch:
 		        retDirs.append(dir)
	return retDirs

    def scan(self,path):
        multicrabdirs = []
        dirs = execute("ls %s"% (path) )

        # For-loop: All directories in path
        for d in dirs:
            d = os.path.join(path, d)
            
            # Skill item if not a directory
            if not os.path.isdir(d):
                continue

            self.Verbose("Looking under directory %s" % (d))
            filepath1 = os.path.join(d, "multicrab.cfg")
            filepath2 = os.path.join(d, "inputInfo.txt")
            
            # If either of the above files exists save the dir for later use
            if os.path.exists(filepath1) or os.path.exists(filepath2):
                multicrabdirs.append(d)

        self.Verbose("Found %i directories:\n\t%s" % (len(multicrabdirs), "\n\t".join(multicrabdirs)) )
        return multicrabdirs

    def ewkfind(self,dirs):
        if self._h2tb:
            myWord = "Hplus2tbAnalysis"
            myFile = "multicrab.cfg"
        else:
            myWord = "mbedded"
            myFile = "multicrab.cfg"
        return self.selectLatest( self.grep(dirs, myWord, myFile) )

    def signalfind(self,dirs):
        if self._h2tb:
            myWord = "Hplus2tbAnalysis"
            myFile = "multicrab.cfg"
        else:
            myWord = "SignalAnalysis"
            myFile = "multicrab.cfg"
        return self.selectLatest( self.grep(dirs, myWord, myFile) )

    def qcdfactfind(self,dirs):
        myList  = []
        keyword = "pseudoMulticrab_QCDfactorised"
        for d in dirs:
            if keyword in d:
                myList.append(d)
        return self.selectLatest(myList)

    def qcdinvfind(self,dirs):
        myList  = []
        keyword = "pseudoMulticrab_QCDfactorised"
        for d in dirs:
            if keyword in d:
                myList.append(d)
        return self.selectLatest(myList)

    def fakeBfind(self,dirs):
        myList  = []
        keyword = "FakeBMeasurement"
        for d in dirs:
            if keyword in d:
                myList.append(d)
        return self.selectLatest(myList)

    def grep(self, dirs, word, file="multicrab.cfg"):
        command = "grep " + word + " "
        founddirs = []
        for dir in dirs:
            multicrabfile = os.path.join(dir,file)
	    if os.path.exists(multicrabfile):
                grep = execute(command + multicrabfile)
                if grep != []:
                    founddirs.append(dir)
                else:
                    s = dir.split("/")
                    if s[len(s)-1].startswith(word):
                        founddirs.append(dir)
        if len(founddirs) == 0:
            return ""
        return founddirs

    def selectLatest(self,dirs):
        if len(dirs) == 0:
            return ""
        if len(dirs) > 1:
            self.Print("More than 1 path found! Will take the most recent one:")
            latest = dirs[0]
            for dir in dirs:
                if os.path.getmtime(dir) > os.path.getmtime(latest):
                    latest = dir

            # Print all paths found and highlight the latest one
            for d in dirs:
                if d == latest:
                    #self.Print(ShellStyles.NoteStyle() + latest + ShellStyles.NormalStyle(), False)
                    self.Print(ShellStyles.SuccessStyle() + latest + ShellStyles.NormalStyle(), False)
                else:
                    self.Print(d, False)

            return latest
        return dirs[0]
