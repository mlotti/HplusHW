#! /usr/bin/env python

import sys
import os
import hashlib
import imp
import re
import stat
import ROOT
import OrderedDict
import HiggsAnalysis.NtupleAnalysis.tools.git as git
import getpass
import socket

def Verbose(msg, printHeader=True):
    '''
    Calls Print() only if verbose options is set to true
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

def IsTH1(h, raiseExcept=False):
    if not isinstance(h, ROOT.TH1):
        msg = "Expected object of type ROOT.TH1, got \"%s\" instead" % (type(h))
        if raiseExcept:
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
        return False
    else:
        return True

def GetDecimalFormat(value):
    if value == 0.0:
        decFormat = "%.0f" % value
    elif abs(value) >= 1.0:
        decFormat = "%.0f" % value
    elif abs(value) >= 0.1:
        decFormat = "%.1f" % value
    elif abs(value) >= 0.01:
        decFormat = "%.2f" % value
    elif abs(value) >= 0.001:
        decFormat = "%.3f" % value
    else:
        decFormat = "%.4f" % value
    return decFormat

def GetTH1BinWidthString(myTH1, iBin):
    IsTH1(myTH1, raiseExcept=True)
     
    width = myTH1.GetBinWidth(iBin)
    return GetDecimalFormat(width)# + str(width)

def GetTH1BinRangeString(myTH1, iBin):
    IsTH1(myTH1, raiseExcept=True)

    lowEdge   = myTH1.GetXaxis().GetBinLowEdge(iBin)
    upEdge    = myTH1.GetXaxis().GetBinUpEdge(iBin)
    rangeStr  = GetDecimalFormat(lowEdge)
    rangeStr += " -> "
    rangeStr += GetDecimalFormat(upEdge)
    return rangeStr

def PrintTH1Info(myTH1):
    '''
    Generic histogram prints detailed tabled
    with the properties of a ROOT.TH1 instance object
    '''
    if not IsTH1(myTH1):
        return

    # Constuct the table
    table   = []
    align  = "{:>5} {:>10} {:^20} {:>15} {:^3} {:<10} {:>15} {:^3} {:<10}"
    header = align.format("Bin", "Bin Width", "Bin Range", "Bin Content", "+/-", "Error", "Cum. Integral", "+/-", "Error")
    hLine  = "="*100

    # Create table
    table.append("{:^100}".format(myTH1.GetName()))    
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # For-loop: All bins
    h = myTH1
    for j in range(0, myTH1.GetNbinsX()+1):
        binWidth      = GetTH1BinWidthString(myTH1, j)
        #binRange      = "%.1f -> %.1f" % (h.GetXaxis().GetBinLowEdge(j), h.GetXaxis().GetBinUpEdge(j) )
        binRange      = GetTH1BinRangeString(myTH1, j)
        binContent    = "%.2f" % h.GetBinContent(j)
        binError      = "%.2f" % h.GetBinError(j)
        integralError = ROOT.Double(0.0)
        integral      = h.IntegralAndError(0, j, integralError, "")
        table.append(align.format(j, binWidth, binRange, binContent, "+/-", binError,"%.1f" % integral, "+/-", "%.1f" % integralError))
    table.append(hLine)
    table.append("")

    for l in table:
        Print(l, False)
    return
        
def rchop(myString, endString):
    '''
    if myString ends with "/" return it without the "/"
    else return as is. 
    '''
    if myString.endswith(endString):
        return myString[:-len(endString)]
    return myString

def convertToURL(path, url=False):
    if not url:
        return path

    # Determine path according to hostname (CERN, FNAL)
    if "cern.ch" in socket.gethostname().lower():
        url  = "https://cmsdoc.cern.ch/~%s/" % (getpass.getuser())
        base = "/afs/cern.ch/user/%s/%s/public/html" % (getpass.getuser()[0], getpass.getuser())
    elif "fnal.gov" in socket.gethostname().lower():
        url  = "http://home.fnal.gov/~%s/" % (getpass.getuser())
        base = "/publicweb/%s/%s/" % (getpass.getuser()[0], getpass.getuser())
    else:
        raise Exception("Cannot determine URL path for host %s" % socket.gethostname())
    
    # Get the URL path
    pathURL = path.replace(base, url)
    return pathURL

def getSaveDirPath(pseudocrabDir, prefix="", postfix="", pseudocrabDir2=None):
    '''
    return the save dir path for all plotting scripts in this format:
    saveDir = <baseDir>/<prefix>/<pseudocrabDir>/<postFix>

    For LPC (FNAL):
    <baseDir> = "/publicweb/%s/%s/" % (getpass.getuser()[0], getpass.getuser())
    For LXPLUS (CERN):
    <baseDir> = "/afs/cern.ch/user/%s/%s/public/html" % (getpass.getuser()[0], getpass.getuser())
    '''
    # Remove trailing "/" if any
    pseudocrabDir = rchop(pseudocrabDir, "/")

    # If path contains other subDirs keep the last dir name
    if len(pseudocrabDir.split("/")) > 1:
        saveDir_1 = pseudocrabDir.split("/")[-1]
    else:
        saveDir_1 = pseudocrabDir

    # Determine <baseDir> according to hostname (CERN, FNAL)
    if "cern.ch" in socket.gethostname().lower():
        baseDir = "/afs/cern.ch/user/%s/%s/public/html" % (getpass.getuser()[0], getpass.getuser())
    elif "fnal.gov" in socket.gethostname().lower():
        baseDir = "/publicweb/%s/%s/" % (getpass.getuser()[0], getpass.getuser())
    else:
        baseDir = ""

    # Put everything together to get the final path
    if pseudocrabDir2 == None:
        saveDir = os.path.join(baseDir, prefix, saveDir_1, postfix)
    else:
        # Is there a secondmulticrab in the save path? (Use-case: Data-Driven plots)
        pseudocrabDir2 = rchop(pseudocrabDir2, "/")
        if len(pseudocrabDir2.split("/")) > 1:
            saveDir_2 = pseudocrabDir2.split("/")[-1]
        else:
            saveDir_2 = pseudocrabDir2
        saveDir = os.path.join(baseDir, prefix, saveDir_1, saveDir_1, postfix)
    return saveDir

def GetListOfEwkDatasets():
    return ["TT", "WJetsToQQ_HT_600ToInf", "DYJetsToQQHT", "SingleTop", "TTWJetsToQQ", "TTZToQQ", "Diboson", "TTTT"]

def cmsswVersion():
    if "CMSSW_VERSION" in os.environ:
        return os.environ["CMSSW_VERSION"]
    else:
        raise Exception("No $CMSSW_VERSION environment variable. Apply first cmsenv and then for standalone environment setupStandalone.(c)sh (needs to be done in test directory)")

def higgsAnalysisPath():
    if "HIGGSANALYSIS_BASE" in os.environ:
        return os.environ["HIGGSANALYSIS_BASE"]
    elif "CMSSW_BASE" in os.environ:
        return os.path.join(os.environ["CMSSW_BASE"], "src", "HiggsAnalysis")
    else:
        raise Exception("No $HIGGSANALYSIS_BASE nor $CMSSW_BASE environment variable. For standalone environment use setupStandalone.(c)sh, for CMSSW environment use cmsenv")

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

def addConfigInfo(of, dataset, addLuminosity=True, dataVersion=None, additionalText={}):
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
    while hasattr(ds, "datasets"):
        ds = ds.datasets[0]

    if dataVersion is None:
        dataVersion = ds.dataVersion

    dv = ROOT.TNamed("dataVersion", dataVersion)
    dv.Write()
    dv.Delete()

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

def th1Integral(th1):
    return th1.Integral(0, th1.GetNbinsX())

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

## Helper function to update keyword argument dictionary
#
# \param kwargs    Dictionary for keyword arguments
# \param obj       Object
# \param names     List of attribute names
#
# Constructs a new dictionary, where key,value pairs are taken from
# kwargs for all attribute names, or if some name does not exist in
# the kwargs, the value is taken from the object.
#
# The kwargs may not contain any other keys than the ones in names
# (typo protection)
def updateArgs(kwargs, obj, names):
    for k in kwargs.keys():
        if not k in names:
            raise Exception("Unknown keyword argument '%s', known arguments are %s" % ", ".join(names))

    args = {}
    for n in names:
        args[n] = kwargs.get(n, getattr(obj, n))
    return args

## Write content to file, and make the file executable
#
# \param filename   Path to file
# \param content    String to write to the file
# \param truncate   Truncate (True) or append (False)
def writeScript(filename, content, truncate=True):
    mode = "w"
    if not truncate:
        mode = "a"
    fOUT = open(filename, mode)
    fOUT.write(content)
    fOUT.close()

    # make the script executable
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IXUSR)

## Pick default value if value is None
def ifNotNoneElse(value, default):
    if value == None:
        return default
    return value

## Helper class to manage mass-specific configuration values
class ValuePerMass:
    ## Constructor
    #
    # \param dictionary   Input dictionary/ValuePerMass object/value
    #
    # If dictionary is dictionary, it must have a "default" key, and
    # it may have more than or equal to zero keys for the mass points.
    # The value of the "default" key is used as the default value for
    # those mass points for which the specific value is not given.
    #
    # If the dictionary is ValuePerMass object, the default and
    # per-mass values are copied from it.
    #
    # If the dictionary is something else, it is used as the default
    # value for all masses
    def __init__(self, dictionary):
        self.values = {}
        if isinstance(dictionary, dict):
            self.values.update(dictionary)
            self.default = self.values["default"]
            del self.values["default"]
        elif isinstance(dictionary, ValuePerMass):
            self.values.update(dictionary.values)
            self.default = dictionary.default
        else:
            self.default = dictionary

    ## Apply a function for all values
    #
    # \param function   Function taking one parameter (the value), the
    #                   return value is not used
    #
    # This allows sanity checks to be performed on the values.
    def forEachValue(self, function):
        function(self.default)
        for value in self.values.values():
            function(value)

    ## Get the value for a given mass point
    def getValue(self, mass):
        return self.values.get(mass, self.default)

    ## Serialize the object to a dictionary
    #
    # Another ValuePerMass can be constructed from the dictionary. The
    # dictionary can be written to a JSON file, allowing the
    # ValuePerMass to be constructed from other scripts.
    def serialize(self):
        ret = {"default": self.default}
        ret.update(self.values)
        return ret


# Helper function for getting up and down variance
# \param diffPlus  float for up variation - nominal
# \param diffMinus  float for down variation - nominal
#
# \return pair of floats (variance for minus, variance for plus)
def getProperAdditivesForVariationUncertainties(diffPlus, diffMinus):
    if diffPlus > 0 and diffMinus > 0:
        return (max(diffPlus, diffMinus)**2, 0.0)
    elif diffPlus < 0 and diffMinus < 0:
        return (0.0, max(-diffPlus, -diffMinus)**2)
    elif diffPlus > 0:
        return (diffPlus**2, diffMinus**2)
    elif diffPlus < 0:
        return (diffMinus**2, diffPlus**2)
    elif diffMinus > 0:
        return (diffMinus**2, diffPlus**2)
    elif diffMinus < 0:
        return (diffPlus**2, diffMinus**2)
    elif diffPlus == 0 and diffMinus == 0:
        return (0.0, 0.0)
    raise Exception("Error: Unknown situation diffPlus=%f, diffMinus=%f!"%(diffPlus, diffMinus))


## Helper function to choose tasks with includeOnlyTasks/excludeTasks
#
# \param tasks  List of strings for task names
# \param kwargs Keyword arguments (see below)
#
# <b>Keyword arguments</b>
# \li \a excludeTasks      String, or list of strings, to specify regexps.
#                          If a dataset name matches to any of the
#                          regexps, Dataset object is not constructed for
#                          that. Conflicts with \a includeOnlyTasks
# \li \a includeOnlyTasks  String, or list of strings, to specify
#                          regexps. Only datasets whose name matches
#                          to any of the regexps are kept. Conflicts
#                          with \a excludeTasks.
#
# \return List of selected tasks (all tasks if neither excludeTasks or includeOnlyTasks is given)
def includeExcludeTasks(tasks, **kwargs):
    if "excludeTasks" in kwargs and "includeOnlyTasks" in kwargs:
        raise Exception("Only one of 'excludeTasks' or 'includeOnlyTasks' is allowed")

    def getRe(arg):
        if isinstance(arg, basestring):
            arg = [arg]
        return [re.compile(a) for a in arg]

    if "excludeTasks" in kwargs:
        exclude = getRe(kwargs["excludeTasks"])
        tmp = []
        for task in tasks:
            found = False
            for e_re in exclude:
                if e_re.search(os.path.basename(task)):
                    found = True
                    break
            if found:
                continue
            tmp.append(task)
        return tmp

    if "includeOnlyTasks" in kwargs:
        include = getRe(kwargs["includeOnlyTasks"])
        tmp = []
        for task in tasks:
            found = False
            for i_re in include:
                if i_re.search(os.path.basename(task)):
                    found = True
                    break
            if found:
                tmp.append(task)
        return tmp

    return tasks

if __name__ == "__main__":
    import unittest


    class TestIncludeExcludeTasks(unittest.TestCase):
        def testNothing(self):
            tasks = ["Foo", "Bar", "Foobar"]
            selected = includeExcludeTasks(tasks)
            self.assertEqual(selected, tasks)

        def testInclude(self):
            tasks = ["Foo", "Bar", "Foobar"]
            selected = includeExcludeTasks(tasks, includeOnlyTasks="Foo")
            self.assertEqual(len(selected), 2)
            self.assertEqual(selected[0], "Foo")
            self.assertEqual(selected[1], "Foobar")

            selected = includeExcludeTasks(tasks, includeOnlyTasks="Foo$")
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0], "Foo")

            selected = includeExcludeTasks(tasks, includeOnlyTasks=["Foo$", "^B"])
            self.assertEqual(len(selected), 2)
            self.assertEqual(selected[0], "Foo")
            self.assertEqual(selected[1], "Bar")

        def testExclude(self):
            tasks = ["Foo", "Bar", "Foobar"]
            selected = includeExcludeTasks(tasks, excludeTasks="Foo")
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0], "Bar")

            selected = includeExcludeTasks(tasks, excludeTasks="Foo$")
            self.assertEqual(len(selected), 2)
            self.assertEqual(selected[0], "Bar")
            self.assertEqual(selected[1], "Foobar")

            selected = includeExcludeTasks(tasks, excludeTasks=["Foo$", "^B"])
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0], "Foobar")

        def testIncludeExclude(self):
            tasks = ["Foo", "Bar", "Foobar"]
            self.assertRaises(Exception, includeExcludeTasks, tasks, excludeTasks="Foo", includeOnlyTasks="Bar")

    unittest.main()

