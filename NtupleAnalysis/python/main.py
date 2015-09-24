import os
import time
import copy
import json

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import datasets as datasetsTest
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git

class PSet:
    def __init__(self, **kwargs):
        self.__dict__["_data"] = copy.deepcopy(kwargs)

    def clone(self, **kwargs):
        pset = PSet(**self._data)
        for key, value in kwargs.iteritems():
            setattr(pset, key, value)
        return pset

    def __getattr__(self, name):
        return self._data[name]

    def __setattr__(self, name, value):
        self.__dict__["_data"][name] = value

    def _asDict(self):
        data = {}
        for key, value in self._data.iteritems():
            if isinstance(value, PSet):
                # Support for json dump of PSet
                data[key] = value._asDict()
            elif isinstance(value, list):
                # Support for json dump of list of PSets
                myList = []
                for item in value:
                    if isinstance(item, PSet):
                        myList.append(item._asDict())
                    else:
                        myList.append(item)
                data[key] = myList
            else:
                data[key] = value
        return data

    def __str__(self):
        return self.serialize_()

    def __repr__(self):
        return self.serialize_()

    def serialize_(self):
        return json.dumps(self._asDict(), sort_keys=True, indent=2)


def File(fname):
    fullpath = os.path.join(aux.higgsAnalysisPath(), fname)
    if not os.path.exists(fullpath):
        raise Exception("The file %s does not exist" % self._fullpath)
    return fullpath

class Analyzer:
    def __init__(self, className, **kwargs):
        self.__dict__["_className"] = className
        silentStatus = True
        if "silent" in kwargs:
            silentStatus = kwargs["silent"]
            del kwargs["silent"]
        if "config" in kwargs:
            if isinstance(kwargs["config"], PSet):
                self.__dict__["_pset"] = kwargs["config"]
            else:
                raise Exception("The keyword config should be used only for providing the parameters as a PSet!")
        else:
            self.__dict__["_pset"] = PSet(**kwargs)
        if not silentStatus:
            print "Configuration parameters:"
            print self.__dict__["_pset"]

    def __getattr__(self, name):
        return getattr(self._pset, name)

    def __setattr__(self, name, value):
        setattr(self.__dict__["_pset"], name, value)

    def className_(self):
        return self.__dict__["_className"]

    def config_(self):
        return self.__dict__["_pset"].serialize_()

class AnalyzerWithIncludeExclude:
    def __init__(self, analyzer, **kwargs):
        self._analyzer = analyzer
        if len(kwargs) > 0 and (len(kwargs) != 1 or not ("includeOnlyTasks" in kwargs or "excludeTasks" in kwargs)):
            raise Exception("AnalyzerWithIncludeExclude expects exactly 1 keyword argument, which is 'includeOnlyTasks' or 'excludeTasks'")
        self._includeExclude = {}
        self._includeExclude.update(kwargs)

    def getAnalyzer(self):
        return self._analyzer

    def runForDataset_(self, datasetName):
        if len(self._includeExclude) == 0:
            return True
        tasks = aux.includeExcludeTasks([datasetName], **(self._includeExclude))
        return len(tasks) == 1


class DataVersion:
    def __init__(self, dataVersion):
        self._version = dataVersion

        self._isData = "data" in self._version
        self._isMC = "mc" in self._version

    def __str__(self):
        return self._version

    def isData(self):
        return self._isData

    def isMC(self):
        return self._isMC

    def is53X(self):
        return "53X" in self._version

    def is74X(self):
        return "74X" in self._version

    def isS10(self):
        return self._isMC() and "S10" in self._version

class Dataset:
    def __init__(self, name, files, dataVersion, lumiFile):
        self._name = name
        self._files = files
        self._dataVersion = DataVersion(dataVersion)
        self._lumiFile = lumiFile

    def getName(self):
        return self._name

    def getFileNames(self):
        return self._files

    def getDataVersion(self):
        return self._dataVersion

    def getLumiFile(self):
        return self._lumiFile

class Process:
    def __init__(self, outputPrefix="analysis", outputPostfix="", maxEvents=-1):
        ROOT.gSystem.Load("libHPlusAnalysis.so")

        self._outputPrefix = outputPrefix
        self._outputPostfix = outputPostfix

        self._datasets = []
        self._analyzers = {}
        self._maxEvents = maxEvents
        self._options = PSet()

    def addDataset(self, name, files=None, dataVersion=None, lumiFile=None):
        if files is None:
            files = datasetsTest.getFiles(name)

        if dataVersion is None:
            prec = dataset.DatasetPrecursor(name, files)
            dataVersion = prec.getDataVersion()
            prec.close()
        self._datasets.append( Dataset(name, files, dataVersion, lumiFile) )

    def addDatasets(self, names): # no explicit files possible here
        for name in names:
            self.addDataset(name)

    def addDatasetsFromMulticrab(self, directory, *args, **kwargs):
#        dataset._optionDefaults["input"] = "miniaod2tree*.root"
        dataset._optionDefaults["input"] = "histograms-*.root"
        dsetMgrCreator = dataset.readFromMulticrabCfg(directory=directory, *args, **kwargs)
        dsets = dsetMgrCreator.getDatasetPrecursors()
        dsetMgrCreator.close()

        for dset in dsets:
            self.addDataset(dset.getName(), dset.getFileNames(), dataVersion=dset.getDataVersion(), lumiFile=dsetMgrCreator.getLumiFile())


    # kwargs for 'includeOnlyTasks' or 'excludeTasks' to set the datasets over which this analyzer is processed, default is all datasets
    def addAnalyzer(self, name, analyzer, **kwargs):
        if self.hasAnalyzer(name):
            raise Exception("Analyzer '%s' already exists" % name)
        self._analyzers[name] = AnalyzerWithIncludeExclude(analyzer, **kwargs)

    # FIXME: not sure if these two actually make sense
    def getAnalyzer(self, name):
        if not self.hasAnalyzer(name):
            raise Exception("Analyzer '%s' does not exist" % name)
        return self._analyzers[name].getAnalyzer()

    def removeAnalyzer(self, name):
        if not self.hasAnalyzer(name):
            raise Exception("Analyzer '%s' does not exist" % name)
        del self._analyzers[name]

    def hasAnalyzer(self, name):
        return name in self._analyzers

    def addOptions(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self._options, key, value)

    def run(self, proof=False, proofWorkers=None):
        outputDir = self._outputPrefix+"_"+time.strftime("%y%m%d_%H%M%S")
        if self._outputPostfix != "":
            outputDir += "_"+self._outputPostfix

        # Create output directory
        os.mkdir(outputDir)
        multicrabCfg = os.path.join(outputDir, "multicrab.cfg")
        f = open(multicrabCfg, "w")
        for dset in self._datasets:
            f.write("[%s]\n\n" % dset.getName())
        f.close()

        # Copy/merge lumi files
        lumifiles = set([d.getLumiFile() for d in self._datasets])
        lumidata = {}
        for fname in lumifiles:
            if not os.path.exists(fname):
                continue
            f = open(fname)
            data = json.load(f)
            f.close()
            for k in data.keys():
                if k in lumidata:
                    raise Exception("Luminosity JSON file %s has a dataset for which the luminosity has already been loaded; please check the luminosity JSON files\n%s" % (fname, k, "\n".join(lumifiles)))
            lumidata.update(data)
        if len(lumidata) > 0:
            f = open(os.path.join(outputDir, "lumi.json"), "w")
            json.dump(lumidata, f, sort_keys=True, indent=2)
            f.close()

        # Setup proof if asked
        _proof = None
        if proof:
            opt = ""
            if proofWorkers is not None:
                opt = "workers=%d"%proofWorkers
            _proof = ROOT.TProof.Open(opt)
            _proof.Exec("gSystem->Load(\"libHPlusAnalysis.so\");")

        # Process over datasets
        for dset in self._datasets:
            inputList = ROOT.TList()
            nanalyzers = 0
            for aname, analyzerIE in self._analyzers.iteritems():
                if analyzerIE.runForDataset_(dset.getName()):
                    nanalyzers += 1
                    analyzer = analyzerIE.getAnalyzer()
                    if hasattr(analyzer, "__call__"):
                        analyzer = analyzer(dset.getDataVersion())
                        if analyzer is None:
                            raise Exception("Analyzer %s was specified as a function, but returned None" % aname)
                        if not isinstance(analyzer, Analyzer):
                            raise Exception("Analyzer %s was specified as a function, but returned object of %s instead of Analyzer" % (aname, analyzer.__class__.__name__))

                    inputList.Add(ROOT.TNamed("analyzer_"+aname, analyzer.className_()+":"+analyzer.config_()))
            if nanalyzers == 0:
                print "Skipping %s, no analyzers" % dset.getName()
                continue


            print "Processing dataset", dset.getName()

            resDir = os.path.join(outputDir, dset.getName(), "res")
            resFileName = os.path.join(resDir, "histograms-%s.root"%dset.getName())

            os.makedirs(resDir)

            tchain = ROOT.TChain("Events")

            for f in dset.getFileNames():
                tchain.Add(f)
            tchain.SetCacheLearnEntries(100);

            tselector = ROOT.SelectorImpl()

            # FIXME: TChain.GetEntries() is needed only to give a time
            # estimate for the analysis. If this turns out to be slow,
            # we could store the number of events along the file names
            # (whatever is the method for that)
            inputList.Add(ROOT.SelectorImplParams(tchain.GetEntries(), dset.getDataVersion().isMC(), self._options.serialize_(), True))

            if _proof is not None:
                tchain.SetProof(True)
                inputList.Add(ROOT.TNamed("PROOF_OUTPUTFILE_LOCATION", resFileName))
            else:
                inputList.Add(ROOT.TNamed("OUTPUTFILE_LOCATION", resFileName))

            tselector.SetInputList(inputList)

            readBytesStart = ROOT.TFile.GetFileBytesRead()
            readCallsStart = ROOT.TFile.GetFileReadCalls()
            timeStart = time.time()
            clockStart = time.clock()

            if self._maxEvents > 0:
                tchain.SetCacheEntryRange(0, self._maxEvents)
                tchain.Process(tselector, "", self._maxEvents)
            else:
                tchain.Process(tselector)

            timeStop = time.time()
            clockStop = time.clock()
            readCallsStop = ROOT.TFile.GetFileReadCalls()
            readBytesStop = ROOT.TFile.GetFileBytesRead()

            # Write configInfo
            fIN = ROOT.TFile.Open(dset.getFileNames()[0])
            cinfo = fIN.Get("configInfo/configinfo")
            tf = ROOT.TFile.Open(resFileName, "UPDATE")
            configInfo = tf.Get("configInfo")
            if configInfo == None:
                configInfo = tf.mkdir("configInfo")
            configInfo.cd()
            dv = ROOT.TNamed("dataVersion", str(dset.getDataVersion()))
            dv.Write()
            cv = ROOT.TNamed("codeVersionAnalysis", git.getCommitId())
            cv.Write()
            if not cinfo == None:
                cinfo.Write()
                fIN.Close()
            tf.Close()

            calls = ""
            if _proof is not None:
                tchain.SetProof(False)
                queryResult = _proof.GetQueryResult()
                cpuTime = queryResult.GetUsedCPU()
                readMbytes = queryResult.GetBytes()/1024/1024
            else:
                cpuTime = clockStop-clockStart
                readMbytes = float(readBytesStop-readBytesStart)/1024/1024
                calls = " (%d calls)" % (readCallsStop-readCallsStart)
            realTime = timeStop-timeStart
            print "    Real time %.2f, CPU time %.2f (%.1f %%), read %.2f MB%s, read speed %.2f MB/s" % (realTime, cpuTime, cpuTime/realTime*100, readMbytes, calls, readMbytes/realTime)
            print

        print
        print "Results are in", outputDir

        return outputDir

if __name__ == "__main__":
    import unittest
    class TestPSet(unittest.TestCase):
        def testConstruct(self):
            d = {"foo": 1, "bar": 4}
            a = PSet(**d)
            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar, 4)
            d["foo"] = 5
            self.assertEqual(a.foo, 1)

        def testClone(self):
            a = PSet(foo=1, bar=4)
            b = a.clone()
            self.assertEqual(b.foo, a.foo)
            self.assertEqual(b.bar, a.bar)
            a.foo = 5
            self.assertEqual(a.foo, 5)
            self.assertEqual(b.foo, 1)

            c = a.clone(foo=10, xyzzy=42)
            self.assertEqual(a.foo, 5)
            self.assertEqual(c.foo, 10)
            self.assertEqual(c.xyzzy, 42)

        def testRecursive(self):
            a = PSet(foo=1, bar=PSet(a=4, b="foo"))
            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar.a, 4)
            self.assertEqual(a.bar.b, "foo")

        def testSet(self):
            a = PSet()
            a.foo = 1
            a.bar = "foo"

            setattr(a, "xyzzy", 42)

            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar, "foo")
            self.assertEqual(a.xyzzy, 42)

        def testSerialize(self):
            a = PSet(foo=1, bar=PSet(a=0.5, b="foo"))
            a.xyzzy = 42
            setattr(a, "fred", 56)
            self.assertEqual(a.serialize_(), """{
  "bar": {
    "a": 0.5, 
    "b": "foo"
  }, 
  "foo": 1, 
  "fred": 56, 
  "xyzzy": 42
}""")
        def testSerializeListOfPSet(self):
            a = PSet(foo=1, bar=[PSet(a=0.5),PSet(a=0.7)])
            self.assertEqual(a.serialize_(), """{
  "bar": [
    {
      "a": 0.5
    }, 
    {
      "a": 0.7
    }
  ], 
  "foo": 1
}""")

    class TestFile(unittest.TestCase):
        def testConstruct(self):
            f = File("NtupleAnalysis/python/main.py")
            self.assertEqual(f, os.path.join(aux.higgsAnalysisPath(), "NtupleAnalysis/python/main.py"))
            self.assertRaises(Exception, File, "NtupleFoo")

        def testSerialize(self):
            a = PSet(foo=File("NtupleAnalysis/python/main.py"))
            self.assertEqual(a.serialize_(), """{
  "foo": "%s/NtupleAnalysis/python/main.py"
}""" % aux.higgsAnalysisPath())

    class TestAnalyzer(unittest.TestCase):
        def testConstruct(self):
            a = Analyzer("Foo", foo=1, bar="plop", xyzzy = PSet(fred=42))
            self.assertEqual(a.className_(), "Foo")
            self.assertEqual(a.foo, 1)
            self.assertEqual(a.bar, "plop")
            self.assertEqual(a.xyzzy.fred, 42)
            self.assertEqual(a.config_(), """{
  "bar": "plop", 
  "foo": 1, 
  "xyzzy": {
    "fred": 42
  }
}""")

        def testModify(self):
            a = Analyzer("Foo", foo=1)
            self.assertEqual(a.foo, 1)

            a.bar = "plop"
            a.foo = 2
            setattr(a, "xyzzy", PSet(a=10))
            self.assertEqual(a.foo, 2)
            self.assertEqual(a.bar, "plop")
            self.assertEqual(a.xyzzy.a, 10)
            self.assertEqual(a.config_(), """{
  "bar": "plop", 
  "foo": 2, 
  "xyzzy": {
    "a": 10
  }
}""")

            a.xyzzy.a = 20
            self.assertEqual(a.xyzzy.a, 20)

            setattr(a, "xyzzy", 50.0)
            self.assertEqual(a.xyzzy, 50.0)

    class TestAnalyzerWithIncludeExclude(unittest.TestCase):
        def testIncludeExclude(self):
            a = AnalyzerWithIncludeExclude(None, includeOnlyTasks="Foo")
            self.assertEqual(a.runForDataset_("Foo"), True)
            self.assertEqual(a.runForDataset_("Bar"), False)
            self.assertEqual(a.runForDataset_("Foobar"), True)

            a = AnalyzerWithIncludeExclude(None, excludeTasks="Foo")
            self.assertEqual(a.runForDataset_("Foo"), False)
            self.assertEqual(a.runForDataset_("Bar"), True)
            self.assertEqual(a.runForDataset_("Foobar"), False)

    class TestProcess(unittest.TestCase):
        def testDataset(self):
            p = Process()
            p.addDataset("Foo", ["foo1.root", "foo2.root"], dataVersion="data")
            p.addDataset("Test", dataVersion="mc")

            self.assertEqual(len(p._datasets), 2)
            self.assertEqual(p._datasets[0].getName(), "Foo")
            self.assertEqual(len(p._datasets[0].getFileNames()), 2)
            self.assertEqual(p._datasets[0].getFileNames(), ["foo1.root", "foo2.root"])
            self.assertEqual(p._datasets[1].getName(), "Test")
            self.assertEqual(len(p._datasets[1].getFileNames()), 2)
            self.assertEqual(p._datasets[1].getFileNames(), ["testfile1.root", "testfile2.root"])

        def testAnalyzer(self):
            p = Process()
            p.addAnalyzer("Test1", Analyzer("FooClass", foo=1))
            p.addAnalyzer("Test2", Analyzer("FooClass", foo=2))

            self.assertEqual(len(p._analyzers), 2)
            self.assertTrue(p.hasAnalyzer("Test1"))
            self.assertTrue(p.hasAnalyzer("Test2"))
            self.assertFalse(p.hasAnalyzer("Test3"))

            self.assertEqual(p.getAnalyzer("Test1").foo, 1)
            self.assertEqual(p.getAnalyzer("Test2").foo, 2)

            p.removeAnalyzer("Test2")
            self.assertEqual(len(p._analyzers), 1)
            self.assertTrue(p.hasAnalyzer("Test1"))
            self.assertFalse(p.hasAnalyzer("Test2"))

        def testOptions(self):
            p = Process()
            p.addOptions(Foo = "bar", Bar = PSet(x=1, y=2.0))

            self.assertEqual(p._options.Foo, "bar")
            self.assertEqual(p._options.Bar.x, 1)
            self.assertEqual(p._options.Bar.y, 2)

            p.addOptions(Foo = "xyzzy", Plop = PSet(x=1, b=3))

            self.assertEqual(p._options.Foo, "xyzzy")
            self.assertEqual(p._options.Plop.x, 1)
            self.assertEqual(p._options.Plop.b, 3)

        def testSelectorImpl(self):
            t = ROOT.SelectorImpl()

            # dummy test
            self.assertEqual(isinstance(t, ROOT.TSelector), True)

    unittest.main()
