import math
import copy
import ROOT

from dataset import *

class FloatAutoFormat:
    def __init__(self, decimals=4):
        self.format = "%%%d."+str(decimals)+"g"
    def __call__(self, width):
        return self.format % width

class FloatDecimalFormat:
    def __init__(self, decimals=4):
        self.format = "%%%d."+str(decimals)+"f"
    def __call__(self, width):
        return self.format % width

class FloatExpFormat:
    def __init__(self, decimals=4):
        self.format = "%%%d."+str(decimals)+"e"
    def __call__(self, width):
        return self.format % width

class FormatText:
    def __init__(self, valuePrecision=4, errorPrecision=4,
                 begin="", separator = "  ", end = "",
                 numberFormat="g"): # f, e, g as for printf
        self.valuePrecision = valuePrecision
        self.errorPrecision = errorPrecision
        self.errorEpsilon = math.pow(10., -1.0*errorPrecision)
        self.begin = begin
        self.separator = separator
        self.end = end
        self.format = numberFormat
                 
    def beginTable(self):
        return ""

    def endTable(self):
        return ""

    def beginLine(self):
        return self.begin

    def endLine(self):
        return self.end

    def beginColumn(self):
        return ""

    def endColumn(self):
        return self.separator

    def number(self, value, error=None, errorLow=None, errorHigh=None):
        if error != None and (errorLow != None or errorHigh != None):
            raise Exception("Only either error or errorLow and errorHigh can be set")
        if errorLow != None and errorHigh == None or errorLow == None and errorHigh != None:
            raise Exception("Both errorLow and errorHigh must be set")

        fmt = "%"+str(self.valuePrecision)+"."+self.format
        ret = fmt % value
        if error == None and errorLow == None:
            return ret

        fmt = "%"+str(self.errorPrecision)+"."+self.format
        if error != None:
            ret += " +- " + fmt%error
            return ret

        if abs(errorHigh-errorLow)/errorHigh < self.errorEpsilon:
            ret += " +- " + fmt%errorLow
        else:
            ret += " + "+fmt%errorHigh + " - "+fmt%errorLow

# Create a new counter table with the counter efficiencies
def counterEfficiency(counterTable):
    result = counterTable.deepCopy()
    for icol in xrange(0, counterTable.getNcolumns()):
        prev = None
        for irow in xrange(0, counterTable.getNrows()):
            count = counterTable.getValue(irow, icol)
            value = None
            if count != None and prev != None:
                try:
                    value = Count(count.value() / prev.value(), None)
                except ZeroDivisionError:
                    pass
            prev = count
            result.setValue(irow, icol, value)
    return result

# Counter column
class CounterColumn:
    def __init__(self, name, rowNames, values):
        self.name = name
        self.rowNames = rowNames
        self.values = values

        if len(rowNames) != len(values):
            raise Exception("len(rowNames) != len(values) (%d != %d)" % (len(rowNames), len(values)))

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getNrows(self):
        return len(self.values)

    def getRowName(self, irow):
        return self.rowNames[irow]

    def getValue(self, irow):
        return self.values[irow]

# Counter table, separated from Counter class in order to contain only
# the table and to have the table operations separate
class CounterTable:
    def __init__(self):
        self.rowNames = []
        self.columnNames = []
        self.table = [] # table[row][column]

        self._updateRowColumnWidths()

    def _updateRowColumnWidths(self):
        rowNameWidth = 0
        if len(self.rowNames) > 0:
            rowNameWidth = max([len(x) for x in self.rowNames])
        self.columnWidths = [max(15, len(x)+1) for x in self.columnNames]

        self.rowNameFormat = "%%-%ds" % (rowNameWidth+2)
        self.columnFormat = "%%%ds"

    def deepCopy(self):
        return copy.deepcopy(self)

    def getNrows(self):
        return len(self.table)

    def getNcolumns(self):
        if self.getNrows() == 0:
            return 0
        return len(self.table[0])

    def getColumnWidth(self, icol):
        return self.columnWidths[icol]

    def getValue(self, irow, icol):
        return self.table[irow][icol]

    def setValue(self, irow, icol, value):
        self.table[irow][icol] = value

    def formatHeader(self):
        header = self.rowNameFormat % "Counter"
        for i, cname in enumerate(self.columnNames):
            header += (self.columnFormat%self.columnWidths[i]) % cname
        return header

    def formatFirstColumn(self, irow):
        return self.rowNameFormat % self.rowNames[irow]

    def indexColumn(self, name):
        return self.columnNames.index(name)

    def appendColumn(self, column):
        self.insertColumn(self.getNcolumns(), column)

    def insertColumn(self, icol, column):
        iname = 0
        icount = 0

        beginColumns = 0
        if len(self.table) > 0:
            beginColumns = len(self.table[0])

        while iname < len(self.rowNames)  and icount < column.getNrows():
            # Check if the current indices give the same counter name for both
            if self.rowNames[iname] == column.getRowName(icount):
                self.table[iname].insert(icol, column.getValue(icount))
                iname += 1
                icount += 1
                continue

            # Search the list of names for the name of count
            found = False
            for i in xrange(iname, len(self.rowNames)):
                if self.rowNames[i] == column.getRowName(icount):
                    self.table[i].insert(icol, column.getValue(icount))
                    iname = i+1
                    icount += 1
                    found = True
                    break
                else:
                    self.table[i].insert(icol, None)
            if found:
                continue

            # Count not found, insert the count after the previous
            # found name
            self.rowNames.insert(iname, column.getRowName(icount))
            row = [None]*(beginColumns+1)
            row[icol] = column.getValue(icount)
            self.table.insert(iname, row)
            iname += 1
            icount += 1

        # Add the remaining counters from column
        for i in xrange(icount, column.getNrows()):
            self.rowNames.append(column.getRowName(i))
            row = [None]*(beginColumns+1)
            row[icol] = column.getValue(i)
            self.table.append(row)

        # Sanity check
        for row in self.table:
            if len(row) < beginColumns+1:
                print row
                raise Exception("Internal error: len(row) = %d, beginColumns = %d" % (len(row), beginColumns))

        self.columnNames.insert(icol, column.getName())
        self._updateRowColumnWidths()

    def getColumn(self, icol):
        # Extract the data for the column
        rowNames = self.rowNames[:]
        colValues = [self.table[irow][icol] for irow in xrange(0, self.getNrows())]

        # Filter out Nones
        i = 0
        while i < len(colValues):
            if colValues[i] == None:
                del rowNames[i]
                del colValues[i]
                i -= 1
            i += 1

        # Construct the column object
        return CounterColumn(self.columnNames[icol], rowNames, colValues)

    def removeColumn(self, icol):
        def rowAllNone(row):
            for col in row:
                if col != None:
                    return False
            return True

        del self.columnNames[icol]
        irow = 0
        while irow < len(self.table):
            del self.table[irow][icol]
            if rowAllNone(self.table[irow]):
                del self.rowNames[irow]
                del self.table[irow]
                irow -= 1

            irow += 1

    def format(self, formatFunction=FloatAutoFormat()):
        content = [self.formatHeader()]

        for irow in xrange(0, self.getNrows()):
            line = self.formatFirstColumn(irow)
    
            for icol in xrange(0, self.getNcolumns()):
                count = self.getValue(irow, icol)
                if count != None:
                    line += formatFunction(self.getColumnWidth(icol)) % count.value()
                else:
                    line += " "*self.getColumnWidth(icol)
    
            content.append(line)
        return "\n".join(content)
            

# Counter for one dataset
class SimpleCounter:
    def __init__(self, histoWrapper, countNameFunction):
        self.histoWrapper = histoWrapper
        self.counter = None
        if countNameFunction != None:
            self.countNames = [countNameFunction(x) for x in histoWrapper.getBinLabels()]
        else:
            self.countNames = histoWrapper.getBinLabels()

    def normalizeToOne(self):
        if self.counter != None:
            raise Exception("Can't normalize after the counters have been created!")
        self.histoWrapper.normalizeToOne()

    def normalizeMCByCrossSection(self):
        if self.counter != None:
            raise Exception("Can't normalize after the counters have been created!")
        if self.histoWrapper.getDataset().isMC():
            self.histoWrapper.normalizeByCrossSection()

    def normalizeMCToLuminosity(self, lumi):
        if self.counter != None:
            raise Exception("Can't normalize after the counters have been created!")
        if self.histoWrapper.getDataset().isMC():
            self.histoWrapper.normalizeToLuminosity(lumi)

    def _createCounter(self):
        self.counter = [x[1] for x in histoToCounter(self.histoWrapper.getHistogram())]

    def getName(self):
        return self.histoWrapper.getDataset().getName()

    def getNrows(self):
        return len(self.countNames)

    def getRowName(self, icount):
        return self.countNames[icount]

    def getValue(self, icount):
        if self.counter == None:
            self._createCounter()
        return self.counter[icount]

    def getCountByName(self, name):
        if self.counter == None:
            self._createCounter()
        for i, cn in enumerate(self.countNames):
            if cn == name:
                return self.counter[i]
        raise Exception("No counter '%s'" % name)

# Counter for many datasets
class Counter:
    def __init__(self, histoWrappers, countNameFunction):
        self.counters = [SimpleCounter(h, countNameFunction) for h in histoWrappers]

    def forEachDataset(self, func):
        for c in self.counters:
            func(c)

    def normalizeToOne(self):
        self.forEachDataset(lambda x: x.normalizeToOne())

    def normalizeMCByCrossSection(self):
        self.forEachDataset(lambda x: x.normalizeMCByCrossSection())

    def normalizeMCByLuminosity(self):
        lumi = None
        for c in self.counters:
            if c.histoWrapper.getDataset().isData():
                if lumi != None:
                    raise Exception("Unable to normalize by luminosity, more than one data datasts (you might want to merge data datasets)")
                lumi = c.histoWrapper.getDataset().getLuminosity()
        if lumi == None:
            raise Exception("Unable to normalize by luminosity. no data datasets")

        self.normalizeMCToLuminosity(lumi)

    def normalizeMCToLuminosity(self, lumi):
        self.forEachDataset(lambda x: x.normalizeMCToLuminosity(lumi))

    def getTable(self):
        table = CounterTable()
        for h in self.counters:
            table.appendColumn(h)
        return table

    def printCounter(self, format=FloatAutoFormat()):
        print self.getTable().format(format)

# Many counters
class EventCounter:
    def __init__(self, datasets, countNameFunction=None):
        counterNames = {}

        if len(datasets.getAllDatasets()) == 0:
            raise Exception("No datasets")

        # Pick all possible names of counters
        counterDir = None
        for dataset in datasets.getAllDatasets():
            if counterDir == None:
                counterDir = dataset.getCounterDirectory()
            else:
                if counterDir != dataset.getCounterDirectory():
                    raise Exception("Sanity check failed, datasets have different counter directories!")

            for name in dataset.getDirectoryContent(counterDir, lambda obj: isinstance(obj, ROOT.TH1)):
                counterNames[name] = 1

        try:
            del counterNames["counter"]
        except KeyError:
            raise Exception("Error: no 'counter' histogram in the '%s' directories" % counterDir)

        self.mainCounter = Counter(datasets.getHistoWrappers(counterDir+"/counter"), countNameFunction)
        self.subCounters = {}
        for subname in counterNames.keys():
            self.subCounters[subname] = Counter(datasets.getHistoWrappers(counterDir+"/"+subname, countNameFunction))

        self.normalization = "None"

    def _forEachCounter(self, func):
        func(self.mainCounter)
        for c in self.subCounters.itervalues():
            func(c)

    def normalizeToOne(self):
        self._forEachCounter(lambda x: x.normalizeToOne())
        self.normalization = "All normalized to unit area"

    def normalizeMCByCrossSection(self):
        self._forEachCounter(lambda x: x.normalizeMCByCrossSection())
        self.normalization = "MC normalized to cross section (pb)"

    def normalizeMCByLuminosity(self):
        self._forEachCounter(lambda x: x.normalizeMCByLuminosity())
        self.normalization = "MC normalized by data luminosity"

    def normalizeMCToLuminosity(self, lumi):
        self._forEachCounter(lambda x: x.normalizeMCToLuminosity(lumi))
        self.normalization = "MC normalized to luminosity %f pb^-1" % lumi

    def getMainCounter(self):
        return self.mainCounter

    def getMainCounterTable(self):
        return self.mainCounter.getTable()

    def getSubCounterNames(self):
        return self.subCounters.keys()

    def getSubCounter(self, name):
        return self.subCounters[name]

    def getSubCounterTable(self, name):
        return self.subCounters[name].getTable()

    def getNormalizationString(self):
        return self.normalization
