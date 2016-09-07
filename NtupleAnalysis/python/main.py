import os
import time
import copy
import json
import re

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import datasets as datasetsTest
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.git as git

_debugPUreweighting = False
_debugMemoryConsumption = False

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

    def __hasattr__(self, name):
        return name in self._data.keys()

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

    def __hasattr__(self, name):
        return hasattr(self._pset, name)

    def __setattr__(self, name, value):
        setattr(self.__dict__["_pset"], name, value)

    def exists(self, name):
        return name in self._pset._asDict()

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
    def __init__(self, name, files, dataVersion, lumiFile, pileup, nAllEvents):
        self._name = name
        self._files = files
        self._dataVersion = DataVersion(dataVersion)
        self._lumiFile = lumiFile
        self._pileup = pileup
        self._nAllEvents = nAllEvents

    def getName(self):
        return self._name

    def getFileNames(self):
        return self._files

    def getDataVersion(self):
        return self._dataVersion

    def getLumiFile(self):
        return self._lumiFile

    def getPileUp(self):
        return self._pileup
      
    def getNAllEvents(self):
        return self._nAllEvents

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

        prec = dataset.DatasetPrecursor(name, files)
        if dataVersion is None:
            dataVersion = prec.getDataVersion()
        pileUp = prec.getPileUp()
        nAllEvents = prec.getNAllEvents()
        prec.close()
        self._datasets.append( Dataset(name, files, dataVersion, lumiFile, pileUp, nAllEvents) )

    def addDatasets(self, names): # no explicit files possible here
        for name in names:
            self.addDataset(name)

    def addDatasetsFromMulticrab(self, directory, *args, **kwargs):
        blacklist = []
        if "blacklist" in kwargs.keys():
            if isinstance(kwargs["blacklist"], str):
                blacklist.append(kwargs["blacklist"])
            elif isinstance(kwargs["blacklist"], list):
                blacklist.extend(kwargs["blacklist"])
            else:
                raise Exception("Unsupported input format!")
            del kwargs["blacklist"]
#        dataset._optionDefaults["input"] = "miniaod2tree*.root"
        dataset._optionDefaults["input"] = "histograms-*.root"
        dsetMgrCreator = dataset.readFromMulticrabCfg(directory=directory, *args, **kwargs)
        dsets = dsetMgrCreator.getDatasetPrecursors()
        dsetMgrCreator.close()

        for dset in dsets:
            isOnBlackList = False
            for item in blacklist:
                if dset.getName().startswith(item):
                    isOnBlackList = True
            if isOnBlackList:
                print "Ignoring dataset because of blacklist options: '%s' ..."%dset.getName()
            else:
                self.addDataset(dset.getName(), dset.getFileNames(), dataVersion=dset.getDataVersion(), lumiFile=dsetMgrCreator.getLumiFile())

    # kwargs for 'includeOnlyTasks' or 'excludeTasks' to set the datasets over which this analyzer is processed, default is all datasets

    def getDatasets(self):
        return self._datasets

    def setDatasets(self, datasets):
        self._datasets = datasets

    def getRuns(self):
        runmin = -1
        runmax = -1
        run_re = re.compile("\S+_Run20\S+_(?P<min>\d\d\d\d\d\d)_(?P<max>\d\d\d\d\d\d)")
        for d in self._datasets:
            if d.getDataVersion().isData():
                match = run_re.search(d.getName())
                if match:
                    min_ = int(match.group("min"))
                    max_ = int(match.group("max"))
                    if runmin < 0:
                        runmin = min_
                    else:
                        if min_ < runmin:
                            runmin = min_
                    if max_ > runmax:
                        runmax = max_
        return runmin,runmax

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
#            f = open(os.path.join(outputDir, "lumi.json"), "w")
#            json.dump(lumidata, f, sort_keys=True, indent=2)
#            f.close()

            # Add run range in a json file, if runMin and runMax in pset
            rrdata = {}
            for aname, analyzerIE in self._analyzers.iteritems():
                ana = analyzerIE.getAnalyzer()
                if hasattr(ana, "__call__"):
                    for dset in self._datasets:
                        if dset.getDataVersion().isData():
                            ana = ana(dset.getDataVersion())
                            if ana.__getattr__("runMax") > 0:
                                rrdata[aname] = "%s-%s"%(ana.__getattr__("runMin"),ana.__getattr__("runMax"))
                                #lumidata[aname] = ana.__getattr__("lumi")
                                break
            if len(rrdata) > 0:
                f = open(os.path.join(outputDir, "runrange.json"), "w")
                json.dump(rrdata, f, sort_keys=True, indent=2)
                f.close()

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

        # Init timing counters
        realTimeTotal = 0
        cpuTimeTotal = 0
        readMbytesTotal = 0
        callsTotal = 0


        # Process over datasets
        ndset = 0
        for dset in self._datasets:
            # Get data PU distributions from data
            #   This is done every time for a dataset since memory management is simpler to handle
            #   if all the histograms in memory are deleted after reading a dataset is finished
            hPUs = self._getDataPUhistos()
            # Initialize
            ndset += 1
            inputList = ROOT.TList()
            nanalyzers = 0
            anames = []
            usePUweights = False
            useTopPtCorrection = False
            nAllEventsPUWeighted = 0.0
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
                    # ttbar status for top pt corrections
                    ttbarStatus = "0"
                    useTopPtCorrection = analyzer.exists("useTopPtWeights") and analyzer.__getattr__("useTopPtWeights")
                    useTopPtCorrection = useTopPtCorrection and dset.getName().startswith("TT")
                    if useTopPtCorrection:
                        ttbarStatus = "1"
                    inputList.Add(ROOT.TNamed("isttbar", ttbarStatus))
                    # Pileup reweighting
                    (puAllEvents, puStatus) = self._parsePUweighting(dset, analyzer, aname, hPUs, inputList)
                    nAllEventsPUWeighted += puAllEvents
                    usePUweights = puStatus
                    # Sum skim counters (from ttree)
                    hSkimCounterSum = self._getSkimCounterSum(dset.getFileNames())
                    inputList.Add(hSkimCounterSum)
                    # Add name
                    anames.append(aname)
            if nanalyzers == 0:
                print "Skipping %s, no analyzers" % dset.getName()
                continue

            print "*** Processing dataset (%d/%d): %s"%(ndset, len(self._datasets), dset.getName())
            if dset.getDataVersion().isData():
                lumivalue = "--- not available in lumi.json (or lumi.json not available) ---"
                if dset.getName() in lumidata.keys():
                    lumivalue = lumidata[dset.getName()]
                print "    Luminosity: %s fb-1"%lumivalue
            print "    Using pileup weights:", usePUweights
            if useTopPtCorrection:
                print "    Using top pt weights: True"

            resDir = os.path.join(outputDir, dset.getName(), "res")
            resFileName = os.path.join(resDir, "histograms-%s.root"%dset.getName())

            os.makedirs(resDir)

            tchain = ROOT.TChain("Events")

            for f in dset.getFileNames():
                tchain.Add(f)
            tchain.SetCacheLearnEntries(1000);
            tchain.SetCacheSize(10000000) # Set cache size to 10 MB (somehow it is not automatically set contrary to ROOT docs)

            tselector = ROOT.SelectorImpl()

            # FIXME: TChain.GetEntries() is needed only to give a time
            # estimate for the analysis. If this turns out to be slow,
            # we could store the number of events along the file names
            # (whatever is the method for that)
            inputList.Add(ROOT.TNamed("entries", str(tchain.GetEntries())))
            if dset.getDataVersion().isMC():
                inputList.Add(ROOT.TNamed("isMC", "1"))
            else:
                inputList.Add(ROOT.TNamed("isMC", "0"))
            inputList.Add(ROOT.TNamed("options", self._options.serialize_()))
            inputList.Add(ROOT.TNamed("printStatus", "1"))

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
            if _debugMemoryConsumption:
                print "    MEMDBG: TChain cache statistics:"
                tchain.PrintCacheStats()
            
            # Obtain Nall events for top pt corrections
            NAllEventsTopPt = 0
            if useTopPtCorrection:
                for inname in dset.getFileNames():
                    fIN = ROOT.TFile.Open(inname)
                    h = fIN.Get("configInfo/topPtWeightAllEvents")
                    if h != None:
                        binNumber = 2 # nominal
                        if hasattr(analyzer, "topPtSystematicVariation"):
                            variation = getattr(analyzer, "topPtSystematicVariation")
                            if variation == "minus":
                                binNumber = 0
                            # FIXME: The bin is to be added to the ttrees
                            #elif variation == "plus":
                                #binNumber = 3
                                #if not h.GetXaxis().GetBinLabel().endsWith("Plus"):
                                    #raise Exception("This should not happen")
                        if binNumber > 0:
                            NAllEventsTopPt += h.GetBinContent(binNumber)
                    else:
                        raise Exception("Warning: Could not obtain N(AllEvents) for top pt reweighting")
                    ROOT.gROOT.GetListOfFiles().Remove(fIN)
                    fIN.Close()

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
            dv.Delete()
            cv = ROOT.TNamed("codeVersionAnalysis", git.getCommitId())
            cv.Write()
            cv.Delete()
            if not cinfo == None:
                # Add more information to configInfo
                n = cinfo.GetNbinsX()
                cinfo.SetBins(n+3, 0, n+3)
                cinfo.GetXaxis().SetBinLabel(n+1, "isData")
                cinfo.GetXaxis().SetBinLabel(n+2, "isPileupReweighted")
                cinfo.GetXaxis().SetBinLabel(n+3, "isTopPtReweighted")
                # Add "isData" column
                if not dset.getDataVersion().isMC():
                    cinfo.SetBinContent(n+1, cinfo.GetBinContent(1))
                # Add "isPileupReweighted" column
                if usePUweights:
                    cinfo.SetBinContent(n+2, nAllEventsPUWeighted / nanalyzers)
                # Add "isTopPtReweighted" column
                if useTopPtCorrection:
                    cinfo.SetBinContent(n+3, NAllEventsTopPt)
                # Write
                cinfo.Write()
                ROOT.gROOT.GetListOfFiles().Remove(fIN);
                fIN.Close()

            # Memory management
            configInfo.Delete()
            ROOT.gROOT.GetListOfFiles().Remove(tf);
            tf.Close()
            for item in inputList:
                if isinstance(item, ROOT.TObject):
                    item.Delete()
            inputList = None
            if hSkimCounterSum != None:
                hSkimCounterSum.Delete()
            if _debugMemoryConsumption:
                print "      MEMDBG: gDirectory", ROOT.gDirectory.GetList().GetSize()
                print "      MEMDBG: list ", ROOT.gROOT.GetList().GetSize()
                print "      MEMDBG: globals ", ROOT.gROOT.GetListOfGlobals().GetSize()
                #for item in ROOT.gROOT.GetListOfGlobals():
                    #print item.GetName()
                print "      MEMDBG: files", ROOT.gROOT.GetListOfFiles().GetSize()
                #for item in ROOT.gROOT.GetListOfFiles():
                #    print "          %d items"%item.GetList().GetSize()
                print "      MEMDBG: specials ", ROOT.gROOT.GetListOfSpecials().GetSize()
                for item in ROOT.gROOT.GetListOfSpecials():
                    print "          "+item.GetName()
                
                #gDirectory.GetList().Delete();
                #gROOT.GetList().Delete();
                #gROOT.GetListOfGlobals().Delete();
                #TIter next(gROOT.GetList());
                #while (TObject* o = dynamic_cast<TObject*>(next())) {
                  #o.Delete();
                #}
            
            # Performance and information
            timeStop = time.time()
            clockStop = time.clock()
            readCallsStop = ROOT.TFile.GetFileReadCalls()
            readBytesStop = ROOT.TFile.GetFileBytesRead()

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
            realTimeTotal += realTime
            cpuTimeTotal += cpuTime
            readMbytesTotal += readMbytes

        print
        if len(self._datasets) > 1:
            print "    Total: Real time %.2f, CPU time %.2f (%.1f %%), read %.2f MB, read speed %.2f MB/s" % (realTimeTotal, cpuTimeTotal, cpuTimeTotal/realTimeTotal*100, readMbytesTotal, readMbytesTotal/realTimeTotal)
        print "    Results are in", outputDir

        return outputDir

    ## Returns PU histograms for data
    def _getDataPUhistos(self):
        hPUs = {}
        for aname, analyzerIE in self._analyzers.iteritems():
            hPU = None
            for dset in self._datasets:
                if dset.getDataVersion().isData() and analyzerIE.runForDataset_(dset.getName()):
                    if hPU is None:
                        hPU = dset.getPileUp().Clone()
                    else:
                        hPU.Add(dset.getPileUp())
            if hPU != None:
                hPU.SetName("PileUpData")
                hPU.SetDirectory(None)
                hPUs[aname] = hPU
            #else:
            #    raise Exception("Cannot determine PU spectrum for data!")
        return hPUs
 
    ## Obtains PU histogram for MC
    # Returns tuple of N(all events PU weighted) and status of enabling PU weights
    def _parsePUweighting(self, dset, analyzer, aname, hDataPUs, inputList):
        if not dset.getDataVersion().isMC():
            return (0.0, False)
        hPUMC = None
        nAllEventsPUWeighted = 0.0
        if aname in hDataPUs.keys():
            if _debugPUreweighting:
                for k in range(hDataPUs[aname].GetNbinsX()):
                    print "DEBUG(PUreweighting): dataPU:%d:%f"%(k+1, hDataPUs[aname].GetBinContent(k+1))
            inputList.Add(hDataPUs[aname])
        else:
            n = 50
            hFlat = ROOT.TH1F("dummyPU"+aname,"dummyPU"+aname,n,0,n)
            hFlat.SetName("PileUpData")
            for k in range(n):
                hFlat.Fill(k+1, 1.0/n)
            inputList.Add(hFlat)
            hDataPUs[aname] = hFlat
        if dset.getPileUp() == None:
            raise Exception("Error: pileup spectrum is missing from dataset! Please switch to using newest multicrab!")
        hPUMC = dset.getPileUp().Clone()
        hPUMC.SetDirectory(None)

        if hPUMC.GetNbinsX() != hDataPUs[aname].GetNbinsX():
            raise Exception("Pileup histogram dimension mismatch! data nPU has %d bins and MC nPU has %d bins"%(hDataPUs[aname].GetNbinsX(), hPUMC.GetNbinsX()))
        hPUMC.SetName("PileUpMC")
        if _debugPUreweighting:
            for k in range(hPUMC.GetNbinsX()):
                print "Debug(PUreweighting): MCPU:%d:%f"%(k+1, hPUMC.GetBinContent(k+1))
        inputList.Add(hPUMC)
        if analyzer.exists("usePileupWeights"):
            usePUweights = analyzer.__getattr__("usePileupWeights")
            if hDataPUs[aname].Integral() > 0.0:
                factor = hPUMC.Integral() / hDataPUs[aname].Integral()
                for k in range(0, hPUMC.GetNbinsX()+2):
                    if hPUMC.GetBinContent(k) > 0.0:
                        w = hDataPUs[aname].GetBinContent(k) / hPUMC.GetBinContent(k) * factor
                        nAllEventsPUWeighted += w * hPUMC.GetBinContent(k)
        return (nAllEventsPUWeighted, usePUweights)
 
    ## Sums the skim counters from input files and returns a pset containing them 
    def _getSkimCounterSum(self, datasetFilenameList):
        hSkimCounterSum = None
        for inname in datasetFilenameList:
            fIN = ROOT.TFile.Open(inname)
            hSkimCounters = fIN.Get("configInfo/SkimCounter")
            if hSkimCounterSum == None:
                hSkimCounterSum = hSkimCounters.Clone()
                hSkimCounterSum.SetDirectory(None) # Store the histogram to memory TDirectory, not into fIN
            else:
                hSkimCounterSum.Add(hSkimCounters)
            hSkimCounters.Delete()
            fIN.Close()
        if hSkimCounterSum == None:
            # Construct an empty histogram
            hSkimCounterSum = ROOT.TH1F("SkimCounter","SkimCounter",1,0,1)
        else:
            # Format bin labels
            for i in range(hSkimCounterSum.GetNbinsX()):
                hSkimCounterSum.GetXaxis().SetBinLabel(i+1, "ttree: %s"%hSkimCounterSum.GetXaxis().GetBinLabel(i+1))
        hSkimCounterSum.SetName("SkimCounter")
        return hSkimCounterSum

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
        #Does not work anymore, since addDataset calls DatasetPrecursor, which fails to open foo1.root since it does not exist
        #def testDataset(self):
            #p = Process()
            #p.addDataset("Foo", ["foo1.root", "foo2.root"], dataVersion="data")
            #p.addDataset("Test", dataVersion="mc")

            #self.assertEqual(len(p._datasets), 2)
            #self.assertEqual(p._datasets[0].getName(), "Foo")
            #self.assertEqual(len(p._datasets[0].getFileNames()), 2)
            #self.assertEqual(p._datasets[0].getFileNames(), ["foo1.root", "foo2.root"])
            #self.assertEqual(p._datasets[1].getName(), "Test")
            #self.assertEqual(len(p._datasets[1].getFileNames()), 2)
            #self.assertEqual(p._datasets[1].getFileNames(), ["testfile1.root", "testfile2.root"])

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
