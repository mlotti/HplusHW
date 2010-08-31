import FWCore.ParameterSet.Config as cms

# Add an object selector, count filter and event counter for one cut
#
# process     cms.Process object where the modules are added
# sequence    cms.Sequence object where the modules are appended
# name        Name of a cut, used as a name of the object selector and as a part of a name for other modules
# src         Source collection InputTag
# cut         Cut expression
# min         Minimum number of selected objects (default: 1)
# selector    Selector module to use (default: CandViewSelector)
# counter     HPlusEventCountAnalyzer EDAnalyzer object, if the event count should be added to that (default: None)
#
# returns the name of the object selector module, so that it can be used in subsequent cuts
def addCut(process, sequence, name, src, cut, min=1, selector="CandViewLazyPtrSelector", counter=None):
    cutname = name
    filtername = name+"Filter"
    countname = "count"+name

    m1 = cms.EDFilter(selector,
                      src = src,
                      cut = cms.string(cut))
    m2 = cms.EDFilter("CandViewCountFilter",
                      src = cms.InputTag(name),
                      minNumber = cms.uint32(min))
    m3 = cms.EDProducer("EventCountProducer")
    process.__setattr__(cutname, m1)
    process.__setattr__(filtername, m2)
    process.__setattr__(countname, m3)

    for n in [m1, m2, m3]:
        sequence *= n

    if counter != None:
        counter.counters.append(cms.InputTag(countname))

    return cms.InputTag(cutname)

# Add module to process and append to a sequence
#
# process   cms.Process object
# sequence  cms.Sequence object
# name      Name of the module
# m         cms.ED(Analyzer/Producer/Filter) object
def addModule(process, sequence, name, m):
    process.__setattr__(name, m)
    sequence *= m

# Clones a module and adds the clone to process and sequence
#
# process    cms.Process object
# sequence   cms.Sequence object
# name       Name of the cloned module
# mod        ED(Analyzer/Producer/Filter) object to be cloned
#
# Returns the cloned module object, so that further customisations can be done
def cloneModule(process, sequence, name, mod):
    m = mod.clone()
    process.__setattr__(name, m)
    sequence *= m
    return m

# Add CandViewHistoAnalyzer to process and sequence
#
# process   cms.Process object
# sequence  cms.Sequence object
# name      Name of the module
# src       Source collection InputTag
# lst       List of Histo objects, one histogram is booked for each
def addHistoAnalyzer(process, sequence, name, src, lst):
    histos = cms.VPSet()
    for histo in lst:
        histos.append(histo.pset())
    addModule(process, sequence, name, cms.EDAnalyzer("CandViewHistoAnalyzer", src=src, histograms=histos))

# Add multiple CandViewHistoAnalyzers to process and sequence
#
# process   cms.Process object
# sequence  cms.Sequence object
# prefix    Common prefix for module names
# lst       List of the following tuples:
#           (name, source, histos), where
#           name         name of the histogramming module
#           source       source collection InputTag
#           histo        list of Histo objects
def addHistoAnalyzers(process, sequence, prefix, lst):
    for t in lst:
        addHistoAnalyzer(process, sequence, prefix+"_"+t[0], t[1], t[2])

def addMultiAnalyzer(process, sequence, name, lst, analyzer):
    m = cms.EDAnalyzer(analyzer)
    for t in lst:
        histos = cms.VPSet()
        for histo in t[2]:
            histos.append(histo.pset())
        
        m.__setattr__(t[0], cms.untracked.PSet(src = t[1], histograms = histos))
    process.__setattr__(name, m)
    sequence *= m
    return m

# Add CandViewMultiHistoAnalyzer to process and sequence
#
# process   cms.Process object
# sequence  cms.Sequence object
# name      Name of the module
# lst       List of the following tuples:
#           (name, source, histos), where
#           name     prefix of the histograms for this source collection
#           source   source collection InputTag
#           histo    list of Histo objects
def addMultiHistoAnalyzer(process, sequence, name, lst):
    return addMultiAnalyzer(process, sequence, name, lst, "CandViewMultiHistoAnalyzer")

def addMultiEfficiencyPerObjectAnalyzer(process, sequence, name, lst):
    return addMultiAnalyzer(process, sequence, name, lst, "CandViewMultiEfficiencyPerObjectAnalyzer")

def addMultiEfficiencyPerEventAnalyzer(process, sequence, name, lst):
    return addMultiAnalyzer(process, sequence, name, lst, "CandViewMultiEfficiencyPerEventAnalyzer")


# Helper class to decrease the required amount of typing when adding
# CandView(Multi)HistoAnalyzers to the analysis
class Histo:
    def __init__(self, name, expr, min, max, nbins, description=None, cuttype=None, minObjects=None, lazy=True):
        self.min = min
        self.max = max
        self.nbins = nbins
        self.name = name
        self.expr = expr
        self.lazy = lazy
        self.minObjects = minObjects
        self.cuttype = cuttype
        if description == None:
            self.descr = name
        else:
            self.descr = description

    def setCuttype(self, cuttype):
        self.cuttype = cuttype

    def setMinObjects(self, minObjects):
        self.minObjects = minObjects

    def setPlotquantity(self, quant):
        self.plotquantity = quant

    def getPlotQuantity(self):
        return self.plotquantity

    def pset(self):
        p = cms.PSet(min = cms.untracked.double(self.min),
                     max = cms.untracked.double(self.max),
                     nbins = cms.untracked.int32(self.nbins),
                     name = cms.untracked.string(self.name),
                     plotquantity = cms.untracked.string(self.expr),
                     description = cms.untracked.string(self.descr),
                     lazyParsing = cms.untracked.bool(self.lazy))
        if self.minObjects != None:
            p.minObjects = cms.untracked.uint32(self.minObjects)
        if self.cuttype != None:
            p.cuttype = cms.untracked.string(self.cuttype)
        
        return p
