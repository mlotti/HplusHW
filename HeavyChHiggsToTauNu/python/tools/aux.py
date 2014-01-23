#! /usr/bin/env python

import sys
import os
import hashlib
import imp
import re
import ROOT
import OrderedDict
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

def addConfigInfo(of, dataset, addLuminosity=True, dataVersionPostfix="", additionalText={}):
    d = of.mkdir("configInfo")
    d.cd()

    # configinfo histogram
    configinfo = ROOT.TH1F("configinfo", "configinfo", 3, 0, 3)
    axis = configinfo.GetXaxis()

    def setValue(bin, name, value):
        axis.SetBinLabel(bin, name)
        configinfo.SetBinContent(bin, value)

    setValue(1, "control", 1)
    setValue(2, "energy", float(dataset.getEnergy()))
    if dataset.isData():
        if addLuminosity:
            setValue(3, "luminosity", dataset.getLuminosity())
    elif dataset.isMC():
        setValue(3, "crossSection", 1.0)

    configinfo.Write()
    configinfo.Delete()

    # dataVersion
    ds = dataset
    if dataset.isData():
        ds = dataset.datasets[0]

    dataVersion = ROOT.TNamed("dataVersion", ds.dataVersion+dataVersionPostfix)
    dataVersion.Write()
    dataVersion.Delete()

    # codeVersion
    codeVersion = ROOT.TNamed("codeVersion", git.getCommitId())
    codeVersion.Write()
    codeVersion.Delete()

    for name, content in additionalText.iteritems():
        txt = ROOT.TNamed(name, content)
        txt.Write()
        txt.Delete()

    of.cd()

def Get(tdir, name):
    o = tdir.Get(name)
    if o == None:
        return o
    # http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=15496
    # This one seems to save quite a lot of "garbage
    # collection" time
    ROOT.SetOwnership(o, True)
    if hasattr(o, "SetDirectory"):
        o.SetDirectory(0)
    return o

def Clone(obj, *args):
    cl = obj.Clone(*args)
    ROOT.SetOwnership(cl, True)
    if hasattr(cl, "SetDirectory"):
        cl.SetDirectory(0)
    return cl

def listDirectoryContent(tdirectory, predicate=None):
    if not hasattr(tdirectory, "GetListOfKeys"):
        return None

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
        elif predicate == None:
            ret.append(key.GetName())
        key = diriter.Next()
    return ret

def th1Xmin(th1):
    if th1 is None:
        return None
    return th1.GetXaxis().GetBinLowEdge(th1.GetXaxis().GetFirst())

def th1Xmax(th1):
    if th1 is None:
        return None
    return th1.GetXaxis().GetBinUpEdge(th1.GetXaxis().GetLast())

def th2Ymin(th2):
    if th2 is None:
        return None
    return th2.GetYaxis().GetBinLowEdge(th2.GetYaxis().GetFirst())

def th2Ymax(th2):
    if th2 is None:
        return None
    return th2.GetYaxis().GetBinUpEdge(th2.GetYaxis().GetLast())

## Copy (some) style attributes from one ROOT object to another
#
# \param src  Source object (copy attributes from)
# \param dst  Destination object (copy attributes to)
def copyStyle(src, dst):
    properties = []
    if hasattr(src, "GetLineColor") and hasattr(dst, "SetLineColor"):
        properties.extend(["LineColor", "LineStyle", "LineWidth"])
    if hasattr(src, "GetFillColor") and hasattr(dst, "SetFillColor"):
        properties.extend(["FillColor", "FillStyle"])
    if hasattr(src, "GetMarkerColor") and hasattr(dst, "SetMarkerColor"):
        properties.extend(["MarkerColor", "MarkerSize", "MarkerStyle"])

    for prop in properties:
        getattr(dst, "Set"+prop)(getattr(src, "Get"+prop)())

## Helper for adding a list to a dictionary
#
# \param d     Dictionary
# \param name  Key to dictionary
# \param item  Item to add to the list
#
# For dictionaries which have lists as items, this function creates
# the list with the \a item if \a name doesn't exist yet, or appends
# if already exists.
def addToDictList(d, name, item):
    if name in d:
        d[name].append(item)
    else:
        d[name] = [item]

## Add ROOT object to TLegend
#
# \param legend      TLegend object
# \param rootObject  ROOT object (TH1, TGraph, etc) to add to the legend
# \param legendLabel Legend label for this entry
# \param legendStyle Legend style for this entry
# \param canModify   True, if this function may modify \a rootObject
#
# \return Clone of rootObject, if the line color is changed for legend
# (see below). This object must be kept in memory until the legend is
# drawn. Otherwise, None.
#
# If legend style is "F", and the line and fill colors are the same,
# the line color is changed to black only for the legend
def addToLegend(legend, rootObject, legendLabel, legendStyle, canModify=False):
    # Hack to get the black border to the legend, only if the legend style is fill
    h = rootObject
    ret = None
    if "f" == legendStyle.lower():
        if not canModify:
            h = rootObject.Clone(h.GetName()+"_forLegend")
            if hasattr(h, "SetDirectory"):
                h.SetDirectory(0)
        h.SetLineWidth(1)
        if h.GetLineColor() == h.GetFillColor():
            h.SetLineColor(ROOT.kBlack)
        ret = h

    labels = legendLabel.split("\n")
    legend.AddEntry(h, labels[0], legendStyle)
    for lab in labels[1:]:
        legend.AddEntry(None, lab, "")

    return ret

## Class for holding multiple objects in a nice way
class MultiObject:
    def __init__(self):
        self._items = OrderedDict.OrderedDict()

    def add(self, name, item):
        if name in self._items:
            raise Exception("Item %s already exists" % name)
        self._items[name] = item

    def get(self, name):
        return self._items[name]

    def forEach(self, function):
        return [function(item) for item in self._items.itervalues()]

    ## Delegate all other calls to the contained objects
    def __getattr__(self, name):
        # https://mail.python.org/pipermail/python-list/2011-February/598125.html
        def _multiplex(*args, **kwargs):
            return [getattr(item, name)(*args, **kwargs) for item in self._items.itervalues()]
        return _multiplex

