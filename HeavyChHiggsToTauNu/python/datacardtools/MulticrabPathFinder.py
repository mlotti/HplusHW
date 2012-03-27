#! /usr/bin/env python

import sys
import os

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import execute
        
class MulticrabPathFinder:
    def __init__(self, config):
	path = config.Path
        multicrabpaths = self.scan(path)
        self.ewk_path     = self.ewkfind(multicrabpaths)
        self.signal_path  = self.signalfind(multicrabpaths)
        self.qcdfact_path = self.qcdfactfind(multicrabpaths)
        self.qcdinv_path  = self.qcdinvfind(multicrabpaths)

    def getQCDFactorizedExists(self):
        return os.path.exists(self.getQCDfacPath())
    
    def getQCDFactorizedPaths(self):
        return self.getSignalPath(),self.getEWKPath(),self.getQCDfacPath()
    
    def getQCDInvertedExists(self):
        return os.path.exists(self.getQCDinvPath())

    def getQCDInvertedPaths(self):
        return self.getSignalPath(),self.getEWKPath(),self.getQCDinvPath()
    
    def getSignalPath(self):
        return self.signal_path
    
    def getEWKPath(self):
        return self.ewk_path
    
    def getQCDfacPath(self):
        return self.qcdfact_path
    
    def getQCDinvPath(self):
        return self.qcdinv_path

    def scan(self,path):
        multicrabdirs = []
        dirs = execute("ls %s"%path)
        for dir in dirs:
            dir = os.path.join(path,dir)
            if os.path.isdir(dir):
                filepath = os.path.join(dir,"multicrab.cfg")
                if os.path.exists(filepath):
                    multicrabdirs.append(dir)
        return multicrabdirs
    
    def ewkfind(self,dirs):
        return self.selectLatest(self.grep(dirs,"embedding"))
    
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

    def grep(self,dirs,word):
        command = "grep " + word + " "
        founddirs = []
        for dir in dirs:
            multicrabfile = os.path.join(dir,"multicrab.cfg")
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
    


                            
