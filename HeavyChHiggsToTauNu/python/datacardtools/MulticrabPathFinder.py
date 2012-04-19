#! /usr/bin/env python

import sys
import os
import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import execute
        
# class to identify multicrab dirs from a given directory. Identifies separately the signal, ewk
# QCDfact and QCDinv dirs. If multiple directories are found, the latest is taken.

class MulticrabDirectoryDataType:
    UNKNOWN = 0
    OBSERVATION = 1
    SIGNAL = 2
    EWKTAUS = 3
    QCDFACTORISED = 4
    QCDINVERTED = 5
    DUMMY = 6

class MulticrabPathFinder:
    def __init__(self, path):
        multicrabpaths = self.scan(path)
        self._ewk_path     = self.ewkfind(multicrabpaths)
        print "- Using EWK+ttbar with genuine taus directory:", self._ewk_path
        self._signal_path  = self.signalfind(multicrabpaths)
        print "- Using signal and EWK+ttbar with fake taus directory:", self._signal_path
        self._qcdfact_path = self.qcdfactfind(multicrabpaths)
        print "- Using multi-jets (factorised) directory:", self._qcdfact_path
        self._qcdinv_path  = self.qcdinvfind(multicrabpaths)
        print "- Using multi-jets (inverted) directory:", self._qcdinv_path

    def getQCDFactorisedExists(self):
        return os.path.exists(self.getQCDfacPath())
    
    def getQCDFactorisedPath(self):
        return self.getQCDfacPath()
    
    def getQCDInvertedExists(self):
        return os.path.exists(self.getQCDinvPath())

    def getQCDInvertedPaths(self):
        return self.getSignalPath(),self.getEWKPath(),self.getQCDinvPath()
    
    def getSignalPath(self):
        return self._signal_path
    
    def getEWKPath(self):
        return self._ewk_path
    
    def getQCDfacPath(self):
        return self._qcdfact_path
    
    def getQCDinvPath(self):
        return self._qcdinv_path

    def getSubPaths(self,path,regexp,exclude=False):
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
        dirs = execute("ls %s"%path)
        for dir in dirs:
            dir = os.path.join(path,dir)
            if os.path.isdir(dir):
                filepath = os.path.join(dir,"multicrab.cfg")
		filepath2 = os.path.join(dir,"inputInfo.txt")
                if os.path.exists(filepath) or os.path.exists(filepath2):
                    multicrabdirs.append(dir)
        return multicrabdirs
    
    def ewkfind(self,dirs):
        return self.selectLatest(self.grep(dirs,"mbedding",file="inputInfo.txt"))
    
    def signalfind(self,dirs):
        ret_dirs = []
        signaldirs = self.grep(dirs,"signalAnalysis_cfg")
        for dir in signaldirs:
            adir = []
            adir.append(dir)
            ewkdir = self.ewkfind(adir)
            if len(ewkdir) == 0:
                ret_dirs.append(dir)
        return self.selectLatest(ret_dirs)
        
    def qcdfactfind(self,dirs):
        return self.selectLatest(self.grep(dirs,"QCDMeasurement_basic"))
        
    def qcdinvfind(self,dirs):
        return self.selectLatest(self.grep(dirs,"signalAnalysisInverted"))

    def grep(self,dirs,word,file="multicrab.cfg"):
        command = "grep " + word + " "
        founddirs = []
        for dir in dirs:
            multicrabfile = os.path.join(dir,file)
	    if os.path.exists(multicrabfile):
                grep = execute(command + multicrabfile)
                if grep != []:
                    founddirs.append(dir)
        if len(founddirs) == 0:
            return ""
        return founddirs

    def selectLatest(self,dirs):
        if len(dirs) == 0:
            return ""
        if len(dirs) > 1:
            print "  Warning, more than 1 path found"
            latest = dirs[0]
            for dir in dirs:
                print "    ",dir
                if os.path.getmtime(dir) > os.path.getmtime(latest):
                    latest = dir

            print "     taking the most recent one",latest
            return latest
        return dirs[0]
    


                            
