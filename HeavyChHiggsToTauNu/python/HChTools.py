import FWCore.ParameterSet.Config as cms
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter

def addConfigInfo(process, options, dataVersion):
    process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer",
        dataVersion = cms.untracked.string(dataVersion.version)
    )
    if options.crossSection >= 0.:
        process.configInfo.crossSection = cms.untracked.double(options.crossSection)
        print "Dataset cross section has been set to %g pb" % options.crossSection
    if options.luminosity >= 0:
        process.configInfo.luminosity = cms.untracked.double(options.luminosity)
        print "Dataset integrated luminosity has been set to %g pb^-1" % options.luminosity
    return cms.Path(process.configInfo)


# Add an array of analysis+counter modules by varying one
# configuration parameter of the analysis module. This is done by
# cloning a given example module configuration and then calling a
# user-supplied function with the module and the value to modify the
# cloned configuration.
#
#
# process   cms.Process object where to add the modules and cms.Path
# prefix    Prefix string for the names of the modules and path
# prototype Module object to clone
# func      Function to be called for modifying one element of the job array
# values    List of parameter values
# names     If the str(x) for values produces an invalid python identifier
#           (e.g. they are floating point numbers with a dot), the names for
#           them must be given explicitly as a separate list. By default,
#           str(value) is used. This name is appended to the prefix to obtain
#           a name for the analysis module.

def addAnalysisArray(process, prefix, prototype, func, values, names=None, preSequence=None, additionalCounters=[]):
    if names == None:
        names = [str(x) for x in values]
    
    for index, value in enumerate(values):
        name = names[index]

        # Clone the prototype and call the modifier function
        module = prototype.clone()
        func(module, value)

        # Add the analysis modules and path
        addAnalysis(process, prefix+name, module, preSequence, additionalCounters)
        
def addAnalysis(process, analysisName, analysisModule, preSequence=None, additionalCounters=[]):
    # Counter and path names
    counterName = analysisName+"Counters"
    pathName = analysisName+"Path"

    # Counter module
    counter = cms.EDAnalyzer("HPlusEventCountAnalyzer",
        counterNames = cms.untracked.InputTag(analysisName, "counterNames"),
        counterInstances = cms.untracked.InputTag(analysisName, "counterInstances"),
        printMainCounter = cms.untracked.bool(False),
        printSubCounters = cms.untracked.bool(False),
        printAvailableCounters = cms.untracked.bool(False),
    )
    if len(additionalCounters) > 0:
        counter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

    # Path
    path = cms.Path()
    if preSequence != None:
        path *= preSequence
    path *= analysisModule
    path *= counter

    # Add modules and path to process
    setattr(process, analysisName, analysisModule)
    setattr(process, counterName, counter)
    setattr(process, pathName, path)

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
def addCut(process, sequence, name, src, cut, min=1, selector="HPlusCandViewLazyPtrSelector", counter=None):
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
    return m

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
def createHistoAnalyzer(src, lst):
    histos = cms.VPSet()
    for histo in lst:
        histos.append(histo.pset())
    return cms.EDanalyzer("CandViewHistoAnalyzer", src=src, histograms=histos)

def addHistoAnalyzer(process, sequence, name, src, lst):
    return addModule(process, sequence, name, createHistoAnalyzer(src, lst))

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

def createMultiAnalyzer(lst, analyzer):
    m = cms.EDAnalyzer(analyzer)
    for t in lst:
        histos = cms.VPSet()
        for histo in t[2]:
            histos.append(histo.pset())
        setattr(m, t[0], cms.untracked.PSet(src = t[1], histograms = histos))
    return m

def addMultiAnalyzer(process, sequence, name, lst, analyzer):
    m = createMultiAnalyzer(lst, analyzer)
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
    return addMultiAnalyzer(process, sequence, name, lst, "HPlusCandViewMultiHistoAnalyzer")

def addMultiEfficiencyPerObjectAnalyzer(process, sequence, name, lst):
    return addMultiAnalyzer(process, sequence, name, lst, "HPlusCandViewMultiEfficiencyPerObjectAnalyzer")

def addMultiEfficiencyPerEventAnalyzer(process, sequence, name, lst):
    return addMultiAnalyzer(process, sequence, name, lst, "HPlusCandViewMultiEfficiencyPerEventAnalyzer")


# Helper class to decrease the required amount of typing when adding
# CandView(Multi)HistoAnalyzers to the analysis
class Histo:
    def __init__(self, name, expr, min, max, nbins, description=None, cuttype=None, minObjects=None, lazy=True):
        self.min = min
        self.max = max
        self.nbins = nbins
        self.name = name
        self.plotquantity = expr
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
                     plotquantity = cms.untracked.string(self.plotquantity),
                     description = cms.untracked.string(self.descr),
                     lazyParsing = cms.untracked.bool(self.lazy))
        if self.minObjects != None:
            p.minObjects = cms.untracked.uint32(self.minObjects)
        if self.cuttype != None:
            p.cuttype = cms.untracked.string(self.cuttype)
        
        return p

def moduleConfEqual(m1, m2):
    if m1.type_() != m2.type_():
        return False

    names1 = m1.parameterNames_()
    names2 = m2.parameterNames_()
    if names1 != names2:
        return False

    for n in names1:
        if m1.getParameter(n).value() != m2.getParameter(n).value():
            return False

    return True

class AnalysisModule:
    def __init__(self, process, name, prefix="", selector=None, filter=None, invertFilter=False, counter=False):
        self.selector = selector
        self.filter = filter
        self.counter = None

        self.selectorName = prefix+name
        self.filterName = prefix+name+"Filter"
        self.counterName = prefix+"count"+name
        self.sequenceFilterName = prefix+name+"FilterSequence"
        self.sequenceName = prefix+name+"Sequence"

        self.filterSequence = cms.Sequence()
        filterN = 0
        if selector != None:
            #if not self._findSelector(process):
            process.__setattr__(self.selectorName, self.selector)
            self.filterSequence *= self.selector
            filterN += 1

        if filter != None:
            if selector != None:
                self.filter.src = cms.InputTag(self.selectorName)
            process.__setattr__(self.filterName, self.filter)
            if invertFilter:
                self.filterSequence *= ~self.filter
            else:
                self.filterSequence *= self.filter
            filterN += 1

        self.sequence = cms.Sequence()
        if filterN > 0:
            process.__setattr__(self.sequenceFilterName, self.filterSequence)
            self.sequence *= self.filterSequence
        if counter:
            self.counter = cms.EDProducer("EventCountProducer")
            process.__setattr__(self.counterName, self.counter)
            self.sequence *= self.counter
        
        process.__setattr__(self.sequenceName, self.sequence)

    # def _findSelector(self, process):
    #     filters = process.filters_()
    #     for name, module in filters.iteritems():
    #         if moduleConfEqual(module, self.selector):
    #             self.selectorName = name
    #             self.selector = module
    #             return True
    #     return False

    def getFilterSequence(self):
        return self.filterSequence

    def getSequence(self):
        return self.sequence

    def getSelectorInputTag(self):
        if self.selector == None:
            raise Exception("No selector for name %s!" % self.selectorName)
        return cms.InputTag(self.selectorName)

# Helpers for selector and count filter modules
def makeSelector(src, expression, selector):
    return cms.EDFilter(selector, src=src, cut=cms.string(expression))

def makeCountFilter(src, minNumber, maxNumber=None):
    if maxNumber == None:
        return cms.EDFilter("CandViewCountFilter",
                            src = src,
                            minNumber = cms.uint32(minNumber))
    else:
        return cms.EDFilter("PATCandViewCountFilter",
                            src = src,
                            minNumber = cms.uint32(minNumber),
                            maxNumber = cms.uint32(maxNumber))

class Analysis:
    def __init__(self, process, seqname, options, prefix="", allCounterName="countAll", additionalCounters=[]):
        self.process = process
        self.prefix = prefix

        # Event counter for all events
        countAll = cms.EDProducer("EventCountProducer")
        setattr(self.process, prefix+allCounterName, countAll)

        # Create the analysis sequence
        self.sequence = cms.Sequence(countAll*process.configInfo)
        if hasattr(process, "genRunInfo"):
            self.sequence *= process.genRunInfo
        setattr(self.process, prefix+seqname, self.sequence)

        # Create the count analyzer
        counters = additionalCounters+[prefix+allCounterName]
        self.countAnalyzer = cms.EDAnalyzer("HPlusEventCountAnalyzer",
            counters = cms.untracked.VInputTag([cms.InputTag(c) for c in counters])
        )
        setattr(self.process, prefix+"countAnalyzer", self.countAnalyzer)

        self.histoIndex = 0
        self.modules = {}

    def getCountAnalyzer(self):
        return self.countAnalyzer

    # Main sequence methods
    def getSequence(self):
        return cms.Sequence(self.sequence * self.countAnalyzer)

    def appendToSequence(self, module):
        self.sequence *= module

    # Analysis module methods
    def hasAnalysisModule(self, name):
        return name in self.modules

    def getAnalysisModule(self, name):
        return self.modules[name]

    def addAnalysisModule(self, name, selector=None, filter=None, invertFilter=False, counter=False):
        m = AnalysisModule(self.process, name, self.prefix, selector, filter, invertFilter, counter)
        self.modules[name] = m

        if counter:
            self.countAnalyzer.counters.append(cms.InputTag(m.counterName))
            self.histoIndex += 1

        self.sequence *= m.getSequence()
        return m

    # Methods using analysis module methods
    def addProducer(self, name, module):
        m = self.addAnalysisModule(name, selector=module)
        return m.getSelectorInputTag()

    def addFilter(self, name, module, invert=False):
        self.addAnalysisModule(name, filter=module, invertFilter=invert, counter=True)

    def addCut(self, name, src, expression, minNumber=1, maxNumber=None, selector="HPlusCandViewLazyPtrSelector"):
        m = self.addAnalysisModule(name,
                                   selector=makeSelector(src, expression, selector),
                                   filter=makeCountFilter(cms.InputTag("dummy"), minNumber, maxNumber),
                                   counter=True)
        return m.getSelectorInputTag()

    # Methods using the methods above
    def addSelection(self, name, src, expression, selector="HPlusCandViewLazyPtrSelector"):
        return self.addProducer(name, makeSelector(src, expression, selector))

    def addTriggerCut(self, dataVersion, triggerConditions, name="Trigger", throw=True):
        m = triggerResultsFilter.clone()
        m.hltResults = cms.InputTag("TriggerResults", "", dataVersion.getTriggerProcess())
        m.l1tResults = cms.InputTag("")
        m.throw = cms.bool(throw) # Should it throw an exception if the trigger product is not found
        m.triggerConditions = cms.vstring(triggerConditions)

        self.addFilter(name, m)

    def addNumberCut(self, name, src, minNumber=1, maxNumber=None):
        self.addFilter(name, makeCountFilter(src, minNumber, maxNumber))

    # Analyzer methods, modifying the the main sequence
    def addAnalyzer(self, postfix, module):
        name = ("h%02d_"%self.histoIndex)+postfix
        setattr(self.process, self.prefix+name, module)
        self.sequence *= module
        return module

    def addHistoAnalyzer(self, postfix, src, histos):
        return self.addModule(("h%02d_"%self.histoIndex)+postfix, createHistoAnalyzer(src, histos))

    def addMultiHistoAnalyzer(self, postfix, histos):
        return self.addModule(("h%02d_"%self.histoIndex)+postfix, createMultiAnalyzer(histos, "HPlusCandViewMultiHistoAnalyzer"))

    def addCloneAnalyzer(self, postfix, module):
        return self.addCloneModule(("h%02d_"%self.histoIndex)+postfix, module)

    def addCloneModule(self, name, module):
        return self.addModule(name, module.clone())

    def addModule(self, name, module):
        setattr(self.process, self.prefix+name, module)
        self.sequence *= module
        return module
