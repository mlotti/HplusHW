import FWCore.ParameterSet.Config as cms
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter

# Add an array of analysis+counter modules by varying one
# configuration parameter of the analysis module. This is done by
# cloning a given example module configuration and then calling a
# user-supplied function with the module and the value to modify the
# cloned configuration.
#
#
# process   cms.Process object where to add the modules and cms.Path
# prefix    Prefix string for the names of the modules and path
# exemplar  Module object to clone
# func      Function to be called for modifying one element of the job array
# values    List of parameter values
# names     If the str(x) for values produces an invalid python identifier
#           (e.g. they are floating point numbers with a dot), the names for
#           them must be given explicitly as a separate list. By default,
#           str(value) is used. This name is appended to the prefix to obtain
#           a name for the analysis module.

def addAnalysisArray(process, prefix, exemplar, func, values, names=None):
    if names == None:
        names = [str(x) for x in values]
    
    for index, value in enumerate(values):
        name = names[index]
        
        # Module and path names
        analysisName = prefix+name
        counterName = analysisName+"Counters"
        pathName = analysisName+"Path"

        # Clone the exemplar and call the modifier function
        m = exemplar.clone()
        func(m, value)

        counter = cms.EDAnalyzer("HPlusEventCountAnalyzer",
            counterNames = cms.untracked.InputTag(analysisName, "counterNames"),
            counterInstances = cms.untracked.InputTag(analysisName, "counterInstances"),
            verbose = cms.untracked.bool(False)
        )

        # Add modules and path to process
        process.__setattr__(analysisName, m)
        process.__setattr__(counterName, counter)
        process.__setattr__(pathName, cms.Path(m*counter))


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
def addHistoAnalyzer(process, sequence, name, src, lst):
    histos = cms.VPSet()
    for histo in lst:
        histos.append(histo.pset())
    return addModule(process, sequence, name, cms.EDAnalyzer("CandViewHistoAnalyzer", src=src, histograms=histos))

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


class Analysis:
    def __init__(self, process, seqname, options, allCounterName="countAll", additionalCounters=[]):
        self.process = process

        # Generator and configuration info analyzers
        process.genRunInfo = cms.EDAnalyzer("HPlusGenRunInfoAnalyzer", src = cms.untracked.InputTag("generator"))
        process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer")
        if options.crossSection >= 0.:
            process.configInfo.crossSection = cms.untracked.double(options.crossSection)
            print "Dataset cross section has been set to %g pb" % options.crossSection
        if options.luminosity >= 0:
            process.configInfo.luminosity = cms.untracked.double(options.luminosity)
            print "Dataset integrated luminosity has been set to %g pb^-1" % options.luminosity

        # Event counter for all events
        countAll = cms.EDProducer("EventCountProducer")
        process.__setattr__(allCounterName, countAll)

        # Create the analysis sequence
        self.sequence = cms.Sequence(countAll*process.genRunInfo*process.configInfo)
        self.process.__setattr__(seqname, self.sequence)

        # Create the count analyzer
        counters = additionalCounters+[allCounterName]
        self.process.countAnalyzer = cms.EDAnalyzer("HPlusEventCountAnalyzer", counters = cms.untracked.VInputTag([cms.InputTag(c) for c in counters]))

        self.histoIndex = 0

    def getSequence(self):
        return cms.Sequence(self.sequence * self.process.countAnalyzer)

    def appendToSequence(self, module):
        self.sequence *= module

    def getCountPath(self):
        return self.process.countAnalyzerPath

    def addTriggerCut(self, dataVersion, triggerConditions, name="Trigger", throw=True):
        filtername = name+"Trigger"
        countname = "count"+name

        m1 = triggerResultsFilter.clone()
        m1.hltResults = cms.InputTag("TriggerResults", "", dataVersion.getTriggerProcess())
        m1.l1tResults = cms.InputTag("")
        m1.throw = cms.bool(throw) # Should it throw an exception if the trigger product is not found
        m1.triggerConditions = cms.vstring(triggerConditions)

        m2 = cms.EDProducer("EventCountProducer")

        self.process.__setattr__(filtername, m1)
        self.process.__setattr__(countname, m2)

        self.sequence *= m1
        self.sequence *= m2

        self.process.countAnalyzer.counters.append(cms.InputTag(countname))

        self.histoIndex += 1

    def addSelection(self, name, src, expression, selector="HPlusCandViewLazyPtrSelector"):
        # Create the EDModule objects
        m1 = cms.EDFilter(selector,
                          src = src,
                          cut = cms.string(expression))
        self.process.__setattr__(name, m1)
        self.sequence *= m1
        return cms.InputTag(name)

    def addCut(self, name, src, expression, minNumber=1, maxNumber=None, selector="HPlusCandViewLazyPtrSelector"):
        selected = self.addSelection(name, src, expression, selector)
        self.addNumberCut(name, selected, minNumber, maxNumber)

        # Return the InputTag of the selected collection
        return selected

    def addNumberCut(self, name, src, minNumber=1, maxNumber=None):
        filtername = name+"Filter"
        countname = "count"+name
        
        m2 = None
        if maxNumber == None:
            m2 = cms.EDFilter("CandViewCountFilter",
                              src = src,
                              minNumber = cms.uint32(minNumber))
        else:
            m2 = cms.EDFilter("PATCandViewCountFilter",
                              src = src,
                              minNumber = cms.uint32(minNumber),
                              maxNumber = cms.uint32(maxNumber))

        m3 = cms.EDProducer("EventCountProducer")

        # Add the modules to process and to the analysis sequence
        self.process.__setattr__(filtername, m2)
        self.process.__setattr__(countname, m3)

        for m in [m2, m3]:
            self.sequence *= m

        # Add the counter product to the countAnalyzer
        self.process.countAnalyzer.counters.append(cms.InputTag(countname))

        # Increase the histogram index
        self.histoIndex += 1

    def addAnalyzer(self, postfix, module):
        name = ("h%02d_"%self.histoIndex)+postfix
        self.process.__setattr__(name, module)
        self.sequence *= module
        return module

    def addCloneAnalyzer(self, postfix, module):
        return self.addCloneModule(("h%02d_"%self.histoIndex)+postfix, module)

    def addHistoAnalyzer(self, postfix, src, histos):
        return addHistoAnalyzer(self.process, self.sequence, ("h%02d_"%self.histoIndex)+postfix, src, histos)

    def addMultiHistoAnalyzer(self, postfix, histos):
        return addMultiAnalyzer(self.process, self.sequence, ("h%02d_"%self.histoIndex)+postfix, histos, "HPlusCandViewMultiHistoAnalyzer")

    def addCloneMultiHistoAnalyzer(self, postfix, module):
        return self.addCloneModule(("h%02d_"%self.histoIndex)+postfix, module)

    def addCloneHistoAnalyzer(self, postfix, module):
        return self.addCloneModule(("h%02d_"%self.histoIndex)+postfix, module)

    def addCloneModule(self, name, module):
        m = module.clone()
        self.process.__setattr__(name, m)
        self.sequence *= m
        return m
