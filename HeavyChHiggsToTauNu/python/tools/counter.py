import math
import copy
import ROOT

from dataset import *
import tools

class CellFormatBase:
    def __init__(self, **kwargs):
        self._valueFormat = tools.kwargsDefault(kwargs, "valueFormat", "%.4g")
        self._uncertaintyFormat = tools.kwargsDefault(kwargs, "uncertaintyFormat", self._valueFormat)
        self._valueOnly = tools.kwargsDefault(kwargs, "valueOnly", False)

        uncertaintyPrecision = tools.kwargsDefault(kwargs, "uncertaintyPrecision", 4)
        self._uncertaintyEpsilon = math.pow(10., -1.0*uncertaintyPrecision)

    def format(self, count):
        value = self._valueFormat % count.value()
        uHigh = count.uncertaintyHigh()
        uLow = count.uncertaintyLow()

        if self._valueOnly or (uLow == None and uHigh == None):
            return self._formatValue(value)

        if (uLow == 0.0 and uHigh == 0.0) or (abs(uHigh-uLow)/uHigh < self._uncertaintyEpsilon):
            return self._formatValuePlusMinus(value, self._uncertaintyFormat % uLow)
        else:
            return self._formatValuePlusHighMinusLow(value, self._uncertaintyFormat % uHigh, self._uncertaintyFormat % uLow)


class CellFormatText(CellFormatBase):
    def __init__(self, **kwargs):
        CellFormatBase.__init__(self, **kwargs)

    def _formatValue(self, value):
        return value

    def _formatValuePlusMinus(self, value, uncertainty):
        return value + " +- " + uncertainty

    def _formatValuePlusHighMinusLow(self, value, uncertaintyHigh, uncertaintyLow):
        return value + " +"+uncertaintyHigh + " -"+uncertaintyLow

class CellFormatTeX(CellFormatBase):
    def __init__(self, **kwargs):
        CellFormatBase.__init__(self, **kwargs)

    def _formatValue(self, value):
        return self._texify(value)

    def _formatValuePlusMinus(self, value, uncertainty):
        return self._texify(value) + " \\pm " + self._texify(uncertainty)

    def _formatValuePlusHighMinusLow(self, value, uncertaintyHigh, uncertaintyLow):
        return "%s^{+ %s}_{- %s}" % (self._texify(value), self._texify(uncertaintyHigh), self._texify(uncertaintyLow))

    def _texify(self, number):
        if not "e" in number:
            return number

        return number.replace("e", "\times 10^{")+"}"

class TableFormatBase:
    def __init__(self, cellFormat, **kwargs):
        self.defaultCellFormat = cellFormat

        for x in ["beginTable", "endTable", "beginRow", "endRow", "beginColumn", "endColumn"]:
            try:
                setattr(self, "_"+x, kwargs[x])
            except KeyError:
                setattr(self, "_"+x, "")

    def beginTable(self, ncolumns):
        return self._beginTable

    def endTable(self):
        return self._endTable

    def beginRow(self, firstRow):
        return self._beginRow

    def endRow(self, lastRow):
        return self._endRow

    def beginColumn(self, firstColumn):
        return self._beginColumn

    def endColumn(self, lastColumn):
        return self._endColumn

    def format(self, count):
        return self.defaultCellFormat.format(count)


class TableFormatText(TableFormatBase):
    def __init__(self, cellFormat=CellFormatText(), beginRow="", columnSeparator = "  ", endRow = ""):
        TableFormatBase.__init__(self, cellFormat, beginTable="", endTable="", beginRow=beginRow, endRow=endRow,
                                 beginColumn="", endColumn=columnSeparator)

class TableFormatLaTeX(TableFormatBase):
    def __init__(self, cellFormat=CellFormatTeX()):
        TableFormatBase.__init__(self, cellFormat, endTable="\\end{tabular}",
                                 beginRow="  ", endRow = " \\\\",
                                 beginColumn="")

    def beginTable(self, ncolumns):
        return "\\begin{tabular}{%s}" % ("l"*ncolumns)

    def endColumn(self, lastColumn):
        if not lastColumn:
            return " && "
        else:
            return ""


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

    def deepCopy(self):
        return copy.deepcopy(self)

    def getNrows(self):
        return len(self.table)

    def getNcolumns(self):
        if self.getNrows() == 0:
            return 0
        return len(self.table[0])

    def getValue(self, irow, icol):
        return self.table[irow][icol]

    def setValue(self, irow, icol, value):
        self.table[irow][icol] = value

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

    def _getColumnWidth(self, icol):
        return self.columnWidths[icol]

    def _updateRowColumnWidths(self):
        rowNameWidth = 0
        if len(self.rowNames) > 0:
            rowNameWidth = max([len(x) for x in self.rowNames])
        self.columnWidths = [max(15, len(x)+1) for x in self.columnNames]

        self.rowNameFormat = "%%-%ds" % (rowNameWidth+2)
        self.columnFormat = "%%%ds"

    def _header(self, formatter):
        return ["Counter"] + self.columnNames

    def _content(self, formatter):
        content = []
        for irow in xrange(0, self.getNrows()):
            row = [self.rowNames[irow]]
            for icol in xrange(0, self.getNcolumns()):
                count = self.getValue(irow, icol)
                if count != None:
                    row.append(formatter.format(count))
                else:
                    row.append("")
            content.append(row)
        return content

    def _columnWidths(self, content):
        widths = [0]*(self.getNcolumns()+1)
        for row in content:
            for icol, col in enumerate(row):
                widths[icol] = max(widths[icol], len(col))
        return widths

    def format(self, formatter=TableFormatText()):
        content = [self._header(formatter)] + self._content(formatter)

        columnWidths = self._columnWidths(content)
        columnFormat = "{value:<{width}}"

        lines = [formatter.beginTable(self.getNcolumns()+1)]
        lastRow = self.getNrows()-1
        lastColumn = self.getNcolumns()
        for irow, row in enumerate(content):
            line = formatter.beginRow(irow==0)
            for icol, column in enumerate(row):
                line += formatter.beginColumn(icol==0)
                line += columnFormat.format(width=columnWidths[icol], value=column)
                line += formatter.endColumn(icol==lastColumn)
            line += formatter.endRow(irow==lastRow)
            lines.append(line)

        lines.append(formatter.endTable())
        return "\n".join(lines)

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
            self.subCounters[subname] = Counter(datasets.getHistoWrappers(counterDir+"/"+subname), countNameFunction)

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
