#! /usr/bin/env python

import sys
import os
import hashlib
import imp
import re
import ROOT
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git

def higgsAnalysisPath():
    if "HIGGSANALYSIS_BASE" in os.environ:
        return os.environ["HIGGSANALYSIS_BASE"]
    elif "CMSSW_BASE" in os.environ:
        return os.path.join(os.environ["CMSSW_BASE"], "src", "HiggsAnalysis")
    else:
        raise Exception("No $HIGGSANALYSIS_BASE nor $CMSSW_BASE environet variable. For standalone environment use setupStandalone.(c)sh, for CMSSW environment use cmsenv")

def execute(cmd):
    f = os.popen(cmd)
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

def load_module(code_path):
    try:
        try:
	    try:
   	        fIN = open(code_path, 'rb')
                return  imp.load_source(hashlib.sha224(code_path).hexdigest(), code_path, fIN)
	    except IOError:
	        print "File",code_path,"not found"
	        sys.exit()
        finally:
            try: fin.close()
            except: pass
    except:
	print "Problem importing file",code_path
	print "check the file with 'python",code_path,"'"
	sys.exit()

def sort(list):
    value_re = re.compile("(^\d+)(\D*$)")
    for t in list:
        i = len(list)
        while i > 1:
            match1 = value_re.search(list[i-1])
            match2 = value_re.search(list[i-2])  
            if int(match1.group(1)) < int(match2.group(1)):
                 swap(list,i-1,i-2)
            i = i - 1
    return list
        
def swap(list,n1,n2):
    tmp = list[n1]
    list[n1] = list[n2]
    list[n2] = tmp

def addConfigInfo(of, dataset):
    d = of.mkdir("configInfo")
    d.cd()

    # configinfo histogram
    configinfo = ROOT.TH1F("configinfo", "configinfo", 3, 0, 3)
    axis = configinfo.GetXaxis()

    def setValue(bin, name, value):
        axis.SetBinLabel(bin, name)
        configinfo.SetBinContent(bin, value)

    setValue(1, "control", 1)
    if dataset.isData():
        setValue(2, "luminosity", dataset.getLuminosity())
        setValue(3, "isData", 1)
    elif dataset.isMC():
        setValue(2, "crossSection", 1.0)
        setValue(3, "isData", 0)

    configinfo.Write()
    configinfo.Delete()

    # dataVersion
    ds = dataset
    if dataset.isData():
        ds = dataset.datasets[0]

    dataVersion = ROOT.TNamed("dataVersion", ds.dataVersion)
    dataVersion.Write()
    dataVersion.Delete()

    # codeVersion
    codeVersion = ROOT.TNamed("codeVersion", git.getCommitId())
    codeVersion.Write()
    codeVersion.Delete()

    of.cd()


def listDirectoryContent(tdirectory, predicate=None):
    dirlist = tdirectory.GetListOfKeys()

    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diriter = dirlist.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    key = diriter.Next()

    ret = []
    while key:
        if predicate is not None and predicate(key):
            ret.append(key.GetName())
        key = diriter.Next()
    return ret
