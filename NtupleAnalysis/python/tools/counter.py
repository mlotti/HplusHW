## \package counter
# Counter utilities and classes
#
# Provides access to event counters stored in histograms ROOT files
# (counter.EventCounter, counter.Counter, counter.SimpleCounter,
# counter.HistoCounter) New rows can be added to existing counters
# from TTrees. Event counters can be normalized to cross section or
# luminosity.
#
# The counters can be transformed to a table (counter.CounterTable)
# to which some set of spreadsheet operations can be performed. Rows
# and columns can be extracted from a table (counter.CounterRow,
# counter.CounterColumn), and also added to table. Currently
# implemented operations are
# \li Cut efficiencies for table (counter.counterEfficiency())
# \li Cut efficiencies for columns (counter.efficiencyColumn())
# \li Sum columns (counter.sumColumn())
# \li Difference of columns (counter.subtractColumn())
# \li Ratio of columns (counter.divideColumn())
# \li Difference of rows (counter.subtractRow())
# \li Column-wise average of table (counter.meanRow())
# \li Column-wise least-square fit of zero-order polynomial of table (counter.meanRowFit())
# \li Column-wise maximum of table (counter.maxRow())
# \li Column-wise minimum of table (counter.minRow())
# \li Cell-wise average of many tables (counter.meanTable())
# \li Cell-wise least-square fit of zero-order polynomial of many tables (counter.meanTableFit())
#
# Tables can then be formatted for printing to a screen or saving to a
# file (counter.CounterTable.format() returns a string). Cell values
# can be formatted as 
# \li plain text (counter.CellFormatText)
# \li TeX (counter.CellFormatTex)
# the main difference being on how to show plus-minus signs and
# exponentials. Tables can be formatted (table and cell formatting are
# orthogonal) as
# \li plain text (counter.TableFormatText)
# \li LaTeX (counter.TableFormatLaTeX)
# \li ConTeXt TABLE (counter.TableFormatConteXtTABLE)
# the differences being on how to separate columns and rows.


import math
import copy
import re
import ROOT

import dataset
import utilities

## Add new bin to counter TH1 from an integral of another TH1
#
# \param counter   Counter TH1 to modify
# \param name      Name of the new count bin
# \param th1       TH1 whose integral is calculated
#
# Use case is the addition of rows to event counter
# (counter.SimpleCounter) from a TTree.
def _counterTh1AddBinFromTh1(counter, name, th1):
    new = ROOT.TH1F(counter.GetName(), counter.GetTitle(), counter.GetNbinsX()+1, 0, counter.GetNbinsX()+1)
    new.SetDirectory(0)
    new.Sumw2()
    
    # Copy the existing bins
    for bin in xrange(1, counter.GetNbinsX()+1):
        new.SetBinContent(bin, counter.GetBinContent(bin))
        new.SetBinError(bin, counter.GetBinError(bin))
        new.GetXaxis().SetBinLabel(bin, counter.GetXaxis().GetBinLabel(bin))

    # Calculate the integral of the new histogram with the uncertainty
    count = dataset.histoIntegrateToCount(th1)

    # Add the new count to the new counter
    new.SetBinContent(counter.GetNbinsX()+1, count.value())
    new.SetBinError(counter.GetNbinsX()+1, count.uncertainty())
    new.GetXaxis().SetBinLabel(counter.GetNbinsX()+1, name)

    return new

## Add new bisn to counter TH1 from bins of another TH1
#
# \param counter   Counter TH1 to modify
# \param th1       TH1 whose bins are copied
#
# Use case is the addition of rows to event counter
# (counter.SimpleCounter) from a TH1.
def _counterTh1AddBinsFromTh1(counter, th1):
    newnbins = counter.GetNbinsX()+th1.GetNbinsX()
    new = ROOT.TH1F(counter.GetName(), counter.GetTitle(), newnbins, 0, newnbins)
    new.SetDirectory(0)
    new.Sumw2()

    # Copy bins
    dstBin = 1
    for histo in [counter, th1]:
        for srcBin in xrange(1, histo.GetNbinsX()+1):
            new.SetBinContent(dstBin, histo.GetBinContent(srcBin))
            new.SetBinError(dstBin, histo.GetBinError(srcBin))
            new.GetXaxis().SetBinLabel(dstBin, histo.GetXaxis().GetBinLabel(srcBin))
            dstBin += 1

    return new

## Extract the position of the first digit in a number
def _numToDig(num):
    if num == 0:
        return 0
    log = math.log10(abs(num))
    if log >= 0:
        return int(log)+1
    else:
        # It's a bit complex to get it correctly
        # 0.9 -> -1
        # 0.1 -> -1
        # 0.09 -> -2
        # 0.01 -> -2
        return -math.ceil(abs(log))

_format_re = re.compile("%\.(?P<num>\d+)(?P<type>[fe])")

## Base class for cell formats.
# 
# The deriving classes must implement
# \li _formatValue(value)
# \li _formatValuePlusMinus(value, uncertainty)
# \li _formatValuePlusHighMinusLow(value, uncertaintyHigh, uncertaintyLow)
# 
# The value, uncertainty(High|Low) are strings formatted with the
# value/uncertaintyFormats. The deriving class may then apply
# additional formatting for the value/uncertainties, and it must
# construct the plusminus string for single uncertainty, and plus
# upper minus lower string for unequal upper/lower uncertainties.
class CellFormatBase:
    ## Constructor
    #
    # \param kwargs   Keyword arguments (see below)
    # 
    # <b>Keyword arguments</b>
    # \li\a valueFormat           Format string for float values (printf style; default: '%.6g')
    # \li\a uncertaintyFormat     Format string for uncertainties (default: same as valueFormat)
    # \li\a uncertaintyPrecision  Number of digits to use for comparing if
    #                             the lower and upper uncertainties are
    #                             equal (default: 4)
    # \li\a withPrecision         Number of digits in uncertainty in uncertainty to
    #                             report the value and uncertainty (default:
    #                             None). If specified, overrides
    #                             valueFormat, uncertaintyFormat, and
    #                             uncertaintyPrecision
    # \li\a valueOnly             Boolean, format the value only? (default: False)
    # \li\a beginCell             String to be inserted before the content of the cell (default: "")
    # \li\a endCell               String to be inserted after the content of the cell (default: "")
    def __init__(self, **kwargs):
        self._valueFormat = kwargs.get("valueFormat", "%.6g")
        self._uncertaintyFormat = kwargs.get("uncertaintyFormat", self._valueFormat)
        self._valueOnly = kwargs.get("valueOnly", False)
        self._beginCell = kwargs.get("beginCell", "")
        self._endCell = kwargs.get("endCell", "")

        uncertaintyPrecision = kwargs.get("uncertaintyPrecision", 4)
        self._withPrecision = kwargs.get("withPrecision", None)
        if self._withPrecision != None:
            uncertaintyPrecision = self._withPrecision

            valM = _format_re.match(self._valueFormat)
            uncM = _format_re.match(self._uncertaintyFormat)
            if not valM:
                raise Exception("Unsupported valueFormat '%s'" % self._valueFormat)
            if not uncM:
                raise Exception("Unsupported uncertaintyFormat '%s'" % self._uncertaintyFormat)
            if valM.group("type") != uncM.group("type"):
                raise Exception("Types of value and uncertainty formats must be the same (either 'f' or 'e', were '%s' and '%s')" % valM.group("type"), uncM.group("type"))
            self._valueType = valM.group("type")

        self._uncertaintyEpsilon = math.pow(10., -1.0*uncertaintyPrecision)


    ## Format the Count object.
    def format(self, count):
        val = count.value()
        uUp = count.uncertaintyHigh()
        uDown = count.uncertaintyLow()
        hasUncertainty = (uUp is not None  and uDown is not None)
        if hasUncertainty:
            uncertaintiesSame = (uUp == 0 or abs(uUp-uDown)/uUp < self._uncertaintyEpsilon)

        if self._withPrecision is None or not hasUncertainty:
            value = self._valueFormat % val
            if hasUncertainty:
                uUpf = self._uncertaintyFormat % uUp
                uDownf = self._uncertaintyFormat % uDown
        else:
            valDig = _numToDig(val)
            uncDig = min(_numToDig(uUp), _numToDig(uDown))

            position = uncDig - self._withPrecision
            # See if number of uncertainty digits changes because of rounding of uncertainty
            if position >= 0:
                valDig = _numToDig(round(val, -position))
                uncDig = min(_numToDig(round(uUp, -position)), _numToDig(round(uDown, -position)))
                position = uncDig - self._withPrecision

            if self._valueType == "f":
                if position < 0:
                    precision = abs(position)
                    if uncDig < 0:
                        precision -= 1
                else:
                    # This case is handled more below, need additional precision for the numbers
                    precision = 0
                    val = round(val, -position)
                    uUp = round(uUp, -position)
                    uDown = round(uDown, -position)
                valFmt = "%%.%df" % precision
                uncFmt = valFmt
            elif self._valueType == "e":
                precisionVal = valDig - position - 1
                precisionUnc = self._withPrecision - 1
                valFmt = "%%.%de" % precisionVal
                uncFmt = "%%.%de" % precisionUnc

            value = valFmt % val
            uUpf = uncFmt % uUp
            uDownf = uncFmt % uDown

        ret = self._beginCell

        if self._valueOnly or not hasUncertainty:
            ret += self._formatValue(value)
        else:
            if (uDown == 0.0 and uUp == 0.0) or uncertaintiesSame:
                ret += self._formatValuePlusMinus(value, uUpf)
            else:
                ret += self._formatValuePlusHighMinusLow(value, uUpf, uDownf)

        ret += self._endCell
        return ret

    ## \var _valueFormat
    # Format string for count value
    ## \var _uncertaintyFormat
    # Format string for count uncertainty
    ## \var _valueOnly
    # Format only the count value, ignore uncertainty
    ## \var _withPrecision
    # If not None, the number if digits to show from uncertainty (see \a withPrecision in __init__())
    ## \var _valueType
    # Type of value format (non-exponential (f) or exponential (e))
    ## \var _uncertaintyEpsilon
    # Asymmetric uncertainties smaller than this are considered to be
    # equal. Epsilon is calculated from the requested precision of
    # uncertainty.

## Text cell format.
class CellFormatText(CellFormatBase):
    ## Constructor.
    #
    # \param kwargs (forwarded to CellFormatBase.__init__())
    def __init__(self, **kwargs):
        CellFormatBase.__init__(self, **kwargs)

    ## Format a value
    def _formatValue(self, value):
        return value

    ## Format a value and symmetric uncertainty
    def _formatValuePlusMinus(self, value, uncertainty):
        return value + " +- " + uncertainty

    ## Format a value and asymmetric uncertainties
    def _formatValuePlusHighMinusLow(self, value, uncertaintyHigh, uncertaintyLow):
        return value + " +"+uncertaintyHigh + " -"+uncertaintyLow

## TeX cell format.
class CellFormatTeX(CellFormatBase):
    ## Constructor.
    #
    # \param kwargs   Keyword arguments (see below, rest are forwarded to CellFormatBase.__init__)
    #
    # <b>Keyword arguments</b>
    # \li\a  texifyPower   Boolean, should the 1e4 to be converted to 1\\times 10^{4}? (default: True)
    def __init__(self, **kwargs):
        CellFormatBase.__init__(self, **kwargs)
        self._texifyPower = kwargs.get("texifyPower", True)
        self._texre = re.compile("(?P<sign>[+-])?(?P<mantissa>[^e]*)(e(?P<exponent>.*))?$")

    ## Format a value
    def _formatValue(self, value):
        return self._texify([value])[0]

    ## Format a value and symmetric uncertainty
    def _formatValuePlusMinus(self, value, uncertainty):
        (v, u) = self._texify([value, uncertainty])
        return v + " $\\pm$ " + u

    ## Format a value and asymmetric uncertainties
    def _formatValuePlusHighMinusLow(self, value, uncertaintyHigh, uncertaintyLow):
        (v, ul, uh) = self._texify([value, uncertaintyHigh, uncertaintyLow])
        return "%s^{+ %s}_{- %s}" % (v, ul, uh)

    ## TeXify the list of numbers.
    #
    # \param numbers   List of number strings
    # 
    # If the texifyPower is False, do nothing.
    # 
    # Convert the numbers such that their exponent is the maximum
    # one in the list.
    def _texify(self, numbers):
        if not self._texifyPower:
            return numbers

        # Check if none of the numbers have exponents
        if reduce(lambda x,y: x+y, map(lambda n: "e" in n, numbers)) == 0:
            return numbers

        maxExp = max([self._getExponent(n) for n in numbers])
        expStr = "\\times 10^{%d}" % maxExp

        # Only one number
        if len(numbers) == 1:
            return [self._texifyOne(n, maxExp)+expStr]

        # Many numbers, show the exponent only in the last one, use parenthesis
        ret = [self._texifyOne(n, maxExp) for n in numbers]
        ret[0] = "\\left("+ret[0]
        ret[-1] = ret[-1]+"\\right)"+expStr
        return ret

    ## Get the exponent of a number string
    def _getExponent(self, number):
        if not "e" in number:
            return 0
        m = self._texre.search(number)
        return int(m.group("exponent"))

    ## TeXify one number
    #
    # \param number     Number string
    # \param targetExp  Target exponent
    def _texifyOne(self, number, targetExp):
        m = self._texre.search(number)
        exp = m.group("exponent")
        if exp == None:
            exp = 0
        else:
            exp = int(exp)

        mantissa = m.group("mantissa")
        sign = m.group("sign")
        if sign == None:
            sign = ""

        if exp == targetExp:
            return mantissa
        elif exp < targetExp:
            return sign + "0."+ ("0"*(targetExp-exp-1)) + mantissa.replace(".", "")
        else:
            # Sanity check
            raise Exception("This condition should never happen")

    ## \var _texifyPower
    # Should exponentials be transformed to TeX format
    ## \var _texre
    # Regular expression for transforming exponential to TeX format

## Base class for table formats.
# 
# The deriving classes must either give the
# (begin|end)(Table|Row|Column) as arguments to the constructor, or
# implement the corresponding method(s) themselvels.
# 
# The format method should not be overridden by a deriving class.
class TableFormatBase:

    ## Constructor.
    # 
    # \param cellFormat   CellFormatBase (or anything deriving from it) for the default cell format
    # \param kwargs       Keyword arguments (see below)
    # 
    # <b>Keyword arguments</b>
    # \li\a beginTable    String for table beginning
    # \li\a endTable      String for table ending
    # \li\a beginRow      String for row beginning
    # \li\a endRow        String for for ending
    # \li\a beginColumn   String for column beginning
    # \li\a endColumn     String for column ending
    def __init__(self, cellFormat, **kwargs):
        self.defaultCellFormat = cellFormat
        self.columnCellFormat = {}

        for x in ["beginTable", "endTable", "beginRow", "endRow", "beginColumn", "endColumn"]:
            try:
                setattr(self, "_"+x, kwargs[x])
            except KeyError:
                setattr(self, "_"+x, "")

    ## Set column-specific format (overriding the default).
    # 
    # \param cellFormat     CellFormatBase object to format the column
    # \param kwargs         Keyword arguments (see below)
    # 
    # <b>Keyword arguments</b>
    # \li\a index     Column index
    # \li\a name      Column name
    # 
    # The column can be referred by index or by name. Only one of
    # them can be given.
    def setColumnFormat(self, cellFormat, **kwargs):
        ind = kwargs.get("index", None)
        if ind == None:
            ind = kwargs.get("name", None)
            if ind == None:
                raise Exception("Either 'index' or 'name' keyword argument is required")
        elif "name" in kwargs:
            raise Exception("Only one of keyword arguments 'index', 'name' can be given")

        self.columnCellFormat[ind] = cellFormat

    ## Format table beginning.
    # 
    # \param ncolumns   Number of columns in the table
    def beginTable(self, ncolumns):
        return self._beginTable

    ## Format table ending.
    def endTable(self):
        return self._endTable

    ## Format row beginning.
    # 
    # \param firstRow   Is this the first row?
    def beginRow(self, firstRow):
        return self._beginRow

    ## Format row ending.
    # 
    # \param lastRow   Is this the last row?
    def endRow(self, lastRow):
        return self._endRow

    ## Format column beginning.
    # 
    # \param firstColumn   Is this the first column?
    def beginColumn(self, firstColumn):
        return self._beginColumn

    ## Format column beginning.
    # 
    # \param lastColumn   Is this the last column?
    def endColumn(self, lastColumn):
        return self._endColumn

    ## Set the current column for column-specific formatting
    #
    # \param name    Name of the column
    # \param index   Index of the column
    #
    # Both the name and index of the column should be given, the
    # proper cell format is then looked up from a dictionary set up
    # with setColumnFormat().
    #
    # \todo This is not very intuitive, and feels a bit hackish solution
    def setCurrentColumn(self, name, index):
        self.currentCellFormat = self.defaultCellFormat
        for ind in [index, name]:
            if ind in self.columnCellFormat:
                self.currentCellFormat = self.columnCellFormat[ind]

    ## Format a cell.
    #
    # \param count   Count object to format
    def formatCell(self, count):
        if not hasattr(self, "currentCellFormat"):
            raise Exception("setCurrentColumn() must be called first")

        return self.currentCellFormat.format(count)

    ## \var defaultCellFormat
    # Default cell formatting object (counter.CellFormatBase)
    ## \var columnCellFormat
    # Dictionary holding column-specific cell formatting objects
    # (counter.CellFormatBase). The column names and indices serve as
    # keys.
    ## \var currentCellFormat
    # Cell formatting object for the current column

## Text table format.
class TableFormatText(TableFormatBase):
    ## Constructor.
    # 
    # \param cellFormat        Cell formatting (default: CellFormatText())
    # \param beginRow          String for row beginning (default: '')
    # \param columnSeparator   String for column separation (default: '  ')
    # \param endRow            String for row ending (default: '')
    def __init__(self, cellFormat=CellFormatText(), beginRow="", columnSeparator = "  ", endRow = ""):
        TableFormatBase.__init__(self, cellFormat, beginTable="", endTable="", beginRow=beginRow, endRow=endRow,
                                 beginColumn="")
        self._columnSeparator = columnSeparator

    def endColumn(self, lastColumn):
        if not lastColumn:
            return self._columnSeparator
        else:
            return ""

    ## \var _columnSeparator
    # String for the column separator

## LaTeX table (tabular) format.
class TableFormatLaTeX(TableFormatBase):
    ## Constructor.
    # 
    # \param cellFormat    Cell formatting (default: CellFromatTeX())
    def __init__(self, cellFormat=CellFormatTeX()):
        TableFormatBase.__init__(self, cellFormat, endTable="\\end{tabular}",
                                 beginRow="  ", endRow = " \\\\",
                                 beginColumn="")

    def beginTable(self, ncolumns):
        return "\\begin{tabular}{%s}" % ("l"*ncolumns)

    def endColumn(self, lastColumn):
        if not lastColumn:
            return " & "
        else:
            return ""

## ConTeXt TABLE format.
#
# For more information see http://wiki.contextgarden.net/TABLE
class TableFormatConTeXtTABLE(TableFormatBase):
    ## Constructor.
    # 
    # \param cellFormat    Cell formatting (default: CellFromatTeX())
    def __init__(self, cellFormat=CellFormatTeX()):
        TableFormatBase.__init__(self, cellFormat, beginTable="\\bTABLE", endTable="\\eTABLE",
                                 beginRow="  \\bTR", endRow="\\eTR",
                                 beginColumn="\\bTD ", endColumn=" \\eTD")

## Split the columns of the table by separators
#
# Use case: CVS output from hplusPrintCounters
class TableSplitter:
    ## Constructor
    #
    # \param separators        Separators in cells to split the columns (either one string for one separator, or list of strings for many)
    # \param removeSeparators  Remove the separators from the cells?
    def __init__(self, separators, removeSeparators=False):
        if isinstance(separators, str):
            self._separators = [separators]
        else:
            self._separators = separators
        self._removeSeparators = removeSeparators

    ## Split table content
    #
    # \param content  Table content (in [row][column] 2D list)
    #
    # \return 2D list with split columns
    def split(self, content):
        nrows = len(content)
        if nrows == 0:
            return
        ncols = len(content[0])
        if ncols == 0:
            return

        ret = [[] for x in xrange(0, nrows)]

        for icol in xrange(0, ncols):
            # Do the splitting, and the maximum number of splits in the column
            nsplits = 0
            rows = []
            for irow in xrange(0, nrows):
                n = 0
                row = []
                cell = content[irow][icol]

                start = 0
                ind = 0
                while ind < len(cell):
                    foundSeparator = False
                    for sep in self._separators:
                        if cell[ind:ind+len(sep)] == sep:
                            row.append(cell[start:ind])
                            if not self._removeSeparators:
                                row.append(sep)
                            ind += len(sep)
                            start = ind

                            foundSeparator = True
                            break
                    if not foundSeparator:
                        ind += 1
                row.append(cell[start:len(cell)])
                            
                rows.append(row)
                nsplits = max(len(row), nsplits)

            # Then append empty cells for those rows which had less splits than the maximum
            for irow, cell in enumerate(rows):
                if len(cell) > nsplits:
                    raise Exception("This should never happen!")
                if len(cell) < nsplits:
                    cell += ["" for x in xrange(0, nsplits-len(cell))]
                ret[irow].extend(cell)
   
        return ret

    ## \var _separators
    # List of separators to split the text
    ## \var _removeSeparators
    # After splitting, should the separators be removed from the
    # result?

## Create a new counter table with the counter efficiencies.
#
# \param counterTable   counter.CounterTable object
#
# \return new counter.CounterTable object
#
# For each row, calculate the cut efficiency as (value from this
# row)/(value from previous row). Uncertainties are not covered.
def counterEfficiency(counterTable):
    result = counterTable.clone()
    for icol in xrange(0, counterTable.getNcolumns()):
        prev = None
        for irow in xrange(0, counterTable.getNrows()):
            count = counterTable.getCount(irow, icol)
            value = None
            if count != None and prev != None:
                try:
                    value = dataset.Count(count.value() / prev.value(), None)
                except ZeroDivisionError:
                    pass
            prev = count
            result.setCount(irow, icol, value)
    return result

## Calculate efficiencies for a column with error propagation uncertainties
#
# \param name    Name of the new column
# \param column  counter.CounterColumn object of counts
#
# Uncertainties are calculated with error propagation, which is not
# really correct way for binomial uncertainty (but is straightforward
# to calculate).
def efficiencyColumnErrorPropagation(name, column):
    origRownames = column.getRowNames()
    rows = []
    rowNames = []

    prev = None
    for irow in xrange(0, column.getNrows()):
        count = column.getCount(irow)
        value = None
        if count != None and prev != None:
            try:
                eff = count.value() / prev.value()
                relUnc = math.sqrt((count.uncertainty()/count.value())**2 + (prev.uncertainty()/prev.value())**2)

                value = dataset.Count(eff, eff*relUnc)
            except ZeroDivisionError:
                pass
        prev = count
        if value != None:
            rows.append(value)
            rowNames.append(origRownames[irow])
    return CounterColumn(name, rowNames, rows)

## Calculate efficiencies for a column with the normal approximation for uncertainties
#
# \param name    Name of the new column
# \param column  counter.CounterColumn object of counts
#
# Normal approximation is not very good either (see
# counter.efficiencyColumnErrorPropagation).
def efficiencyColumnNormalApproximation(name, column):
    # also approximate that p is small, so sigma = sqrt(Npassed)/sqrt(Ntotal)
    origRownames = column.getRowNames()
    rows = []
    rowNames = []

    prev = None
    for irow in xrange(0, column.getNrows()):
        count = column.getCount(irow)
        value = None
        if count != None and prev != None:
            try:
                eff = count.value() / prev.value()
                unc = count.uncertainty() / prev.value()

                value = dataset.Count(eff, unc)
            except ZeroDivisionError:
                pass
        prev = count
        if value != None:
            rows.append(value)
            rowNames.append(origRownames[irow])
    return CounterColumn(name, rowNames, rows)

## Calculate efficiencies for a column with the Clopper-Pearson method for uncertainties
#
# \param name    Name of the new column
# \param column  counter.CounterColumn object of counts
#
# Note that the counts in the column must be unweighted counts
# (i.e. for MC they should not be normalized or anything)
def efficiencyColumnClopperPearson(name, column):
    origRowNames = column.getRowNames()
    rows = []
    rowNames = []

    prev = None
    for irow in xrange(0, column.getNrows()):
        count = column.getCount(irow)
        value = None
        if count != None and prev != None:
            try:
                value = dataset.divideBinomial(count, prev)
            except ZeroDivisionError:
                pass
        prev = count
        if value != None:
            rows.append(value)
            rowNames.append(origRownames[irow])
    return CounterColumn(name, rowNames, rows)

## Calculate efficiencies for a column with the normal approximation for uncertainties
#
# \param name    Name of the new column
# \param column  counter.CounterColumn object of counts
# \param method  Name of uncertainty estimation method
#
# \todo If we want to do this seriously, we would want e.g.
# Clopper-Pearson. Then the weighted counts become an issue. This can
# be solved with TEfficiency, but requires changes to many levels
# (TEfficiencies must be created with the unweighted counts)
def efficiencyColumn(name, column, method="normalApproximation"):
    return {
        "normalApproximation": efficiencyColumnNormalApproximation,
        "errorPropagation": efficiencyColumnErrorPropagation,
        "clopperPearson": efficiencyColumnClopperPearson,
    }[method](name, column)

def efficiencyColumnFromTEfficiency(name, teff, rowNames):
    rows = []
    nbins = teff.GetTotalHistogram().GetNbinsX()
    if nbins != len(rowNames):
        raise Exception("Got %d bins from TEfficiency, but %d rowNames" % (nbins, len(rowNames)))
    for i in xrange(0, nbins):
        bin = i+1
        rows.append(dataset.CountAsymmetric(teff.GetEfficiency(bin), teff.GetEfficiencyErrorLow(bin), teff.GetEfficiencyErrorUp(bin)))
    return CounterColumn(name, rowNames, rows)

def efficiencyTableFromTEfficiencies(teffs, columnNames, rowNames):
    table = CounterTable()
    for teff, name in zip(teffs, columnNames):
        table.appendColumn(efficiencyColumnFromTEfficiency(name, teff, rowNames))
    return table

## Create a new counter.CounterColumn as the sum of the columns.
#
# \param name     Name of the new column
# \param columns  List of counter.CounterColumn objects
#
# \return New counter.CounterColumn object containing the sum of columns.
#
# Uncertainties are handled with the error propagation.
def sumColumn(name, columns):
    table = CounterTable()
    for c in columns:
        table.appendColumn(c)
    table.removeNonFullRows()
    nrows = table.getNrows()
    ncols = table.getNcolumns()

    rows = []
    for irow in xrange(nrows):
        count = dataset.Count(0,0)
        for icol in xrange(ncols):
            count.add(table.getCount(irow, icol))
        rows.append(count)

    return CounterColumn(name, table.getRowNames(), rows)


## Create a new counter.CounterColumn as column1-column2
#
# \param name     Name of the new column
# \param column1  counter.CounterColumn object
# \param column2  counter.CounterColumn object
#
# \return New counter.CounterColumn object as the difference of the two columns
#
# Uncertainties are handled with the error propagation.
def subtractColumn(name, column1, column2):
    table = CounterTable()
    table.appendColumn(column1)
    table.appendColumn(column2)
    table.removeNonFullRows()
    nrows = table.getNrows()

    rows = []
    for irow in xrange(nrows):
        count = table.getCount(irow, 0).clone() # column1
        dcount = table.getCount(irow, 1) # column2
            
        count.subtract(dcount)
        rows.append(count)

    return CounterColumn(name, table.getRowNames(), rows)

## Create a new counter.CounterColumn as column1/column2.
#
# \param name     Name of the new column
# \param column1  Numerator counter.CounterColumn object
# \param column2  Denominator counter.CounterColumn object
#
# \return New counter.CounterColumn object as the ratio of the two columns
#
# Uncertainties are handled with the error propagation (i.e. not
# suitable for binomial division, e.g. efficiency).
def divideColumn(name, column1, column2):
    table = CounterTable()
    table.appendColumn(column1)
    table.appendColumn(column2)
    table.removeNonFullRows()
    nrows = table.getNrows()

    origRownames = table.getRowNames()

    rows = []
    rowNames = []
    for irow in xrange(nrows):
        count = table.getCount(irow, 0).clone() # column1
        dcount = table.getCount(irow, 1) # column2
        if dcount.value() == 0:
            continue
            
        count.divide(dcount)
        rows.append(count)
        rowNames.append(origRownames[irow])

    return CounterColumn(name, rowNames, rows)

## Create a new counter.CounterRow as row1-row2
#
# \param name     Name of the new row
# \param row1  counter.CounterRow object
# \param row2  counter.CounterRow object
#
# \return New counter.CounterRow object as the difference of the two rows
#
# Uncertainties are handled with the error propagation.
def subtractRow(name, row1, row2):
    table = CounterTable()
    table.appendRow(row1)
    table.appendRow(row2)
    table.removeNonFullColumns()
    ncols = table.getNcolumns()

    cols = []
    for icol in xrange(ncols):
        count = table.getCount(0, icol).clone() # row1
        dcount = table.getCount(1, icol) # row2

        count.subtract(dcount)
        cols.append(count)

    return CounterRow(name, table.getColumnNames(), cols)
    

## Helper function for row operations
#
# \param table     counter.CounterTable object
# \param function  Function doing the accumulation
#
# \return Accumulated counter.CounterRow object
def accumulateRow(table, function):
    row = table.getRow(0).clone()
    for irow in xrange(1, table.getNrows()):
        for icol in xrange(table.getNcolumns()):
            count1 = row.getCount(icol)
            count2 = table.getCount(irow, icol)
            if count1 != None and count2 != None:
                count = function(count1, count2)
                row.setCount(icol, count)
            else:
                row.setCount(icol, None)
    return row

## Calculate row with column-wise averages of a table
#
# \param table                   counter.CounterTable object
# \param uncertaintyByAverage    By default uncertainties are propageted with error propagation. If this is set to true, take the mean of the uncertainties as the final uncertainty
#
# \return counter.CounterRow object containing the column-wise averages
#
# Use case for \a uncertaintyByAverage was the averaging in the
# embedding for HIG-11-019 preapproval (but was changed for approval)
def meanRow(table, uncertaintyByAverage=False):
    # Sum
    if uncertaintyByAverage:
        row = accumulateRow(table, lambda a, b: dataset.Count(a.value()+b.value(), a.uncertainty()+b.uncertainty()))
    else:
        def f(a, b):
            c = a.clone()
            c.add(b)
            return c
        row = accumulateRow(table, f)
    row.setName("Mean")

    # Average
    for icol in xrange(row.getNcolumns()):
        count = row.getCount(icol)
        if count != None:
            N = table.getNrows()
            row.setCount(icol, dataset.Count(count.value()/N, count.uncertainty()/N))

    return row

## Calculate row with column-wise a least square fit of the table
#
# \param table  counter.CounterTable object
#
# \return tuple with the row containing the values with uncertainties, and another row with the chi2 and ndof.
#
# For each column, fit a zero-order polynomial (constant) to the
# column values. The value and uncertainty from the fit is returned in
# one row. The chi2 and ndof ofthe fit are returned in another row,
# such that the count value is chi2, and uncertainty is ndof (hacky,
# but works).
def meanRowFit(table):
    valueRow = table.getRow(0).clone()
    valueRow.setName("Fit")
    chiRow = valueRow.clone()
    chiRow.setName("Chi2/ndof")
    for icol in xrange(table.getNcolumns()):
        values = []
        for irow in xrange(table.getNrows()):
            count = table.getCount(irow, icol)
            if count != None:
                values.append(count)


        (m, dm, chi2, ndof) = utilities.leastSquareFitPoly0([v.value() for v in values], [v.uncertainty() for v in values])
        if m != None:
            valueRow.setCount(icol, dataset.Count(m, dm))
            chiRow.setCount(icol, dataset.Count(chi2, ndof))
        else:
            valueRow.setCount(icol, None)
            chiRow.setCount(icol, None)

    return (valueRow, chiRow)

## Calculate the maximum of each column
#
# \param table   counter.CounterTable object
#
# \return counter.CounterRow object, cells contain the column-wise maximum values
def maxRow(table):
    row = accumulateRow(table, lambda a, b: max(a, b, key=lambda x: x.value()))
    row.setName("Max")
    return row

## Calculate the minimum of each column
#
# \param table   counter.CounterTable object
#
# \return counter.CounterRow object, cells contain the column-wise maximum values
def minRow(table):
    row = accumulateRow(table, lambda a, b: min(a, b, key=lambda x: x.value()))
    row.setName("Min")
    return row

## Remove columns and rows not found in all tables
#
# \param tables  List of counter.CounterTable objects
#
# \return new list of new counter.CounterTable objects
#
# Mainly used from counter.meanTable() and counter.meanTableFit()
def removeColumnsRowsNotInAll(tables):
    # Remove columns which are not in all tables
    tablesCopy = [t.clone() for t in tables]
    maxNcols = max([t.getNcolumns() for t in tables])
    iCol = 0
    while iCol < maxNcols:
        colName = tablesCopy[0].getColumnNames()[iCol]
        for table in tablesCopy[1:]:
            if colName != table.getColumnNames()[iCol]:
                for t in tablesCopy:
                    t.removeColumn(iCol)
                maxNcols -= 1
                continue
        iCol += 1

    # Remove rows which are not in all tables
    maxNrows = max([t.getNrows() for t in tables])
    iRow = 0
    while iRow < maxNrows:
        rowName = tablesCopy[0].getRowNames()[iRow]
        for table in tablesCopy[1:]:
            if rowName != table.getRowNames()[iRow]:
                for t in tablesCopy:
                    t.remoteRow(index=iRow)
                maxNrows -= 1
                continue
        iRow += 1

    return tablesCopy

## Remove rows not found in all tables
#
# \param tables  List of counter.CounterTable objects
#
# \return new list of new counter.CounterTable objects
#
# Mainly used from counter.meanTable() and counter.meanTableFit().
# Needed in addition of removeColulmnsRowsNotInAll() in order to allow
# partial embedding processing rounds (i.e. to not process all datasets)
def removeRowsNotInAll(tables):
    tablesCopy = [t.clone() for t in tables]

    maxNrows = max([t.getNrows() for t in tables])
    iRow = 0
    while iRow < maxNrows:
        if tablesCopy[0].getNrows() <= iRow:
            for t in tablesCopy[1:]:
                if table.getNrows() > iRow:
                    table.removeRow(index=iRow)
            maxNrows -= 1
            continue

        rowName = tablesCopy[0].getRowNames()[iRow]
        shouldRowBeRemoved = False
        for table in tablesCopy[1:]:
            if table.getNrows() <= iRow or rowName != table.getRowNames()[iRow]:
                shouldRowBeRemoved = True
        if shouldRowBeRemoved:
            for t in tablesCopy:
                if t.getNrows() > iRow:
                    t.removeRow(index=iRow)
            maxNrows -= 1
            continue
        iRow += 1

    return tablesCopy


## Create a new counter.CounterTable as the average of the tables
#
# \param tables  List of counter.CounterTable objects
# \param uncertaintyByAverage    By default uncertainties are propageted with error propagation. If this is set to true, take the mean of the uncertainties as the final uncertainty
#
# \return new counter.CounterTable object
#
# For each cell, calculate the average over the tables.
#
# Needed for the averaging in embedding.
def meanTable(tables, uncertaintyByAverage=False):
    if len(tables) == 0:
        raise Exception("Got 0 tables")

    #tablesCopy = removeRowsNotInAll(tables)
    tablesCopy = [t.clone() for t in tables]

    # Do the average
    table = tablesCopy[0]
    rowNames = table.getRowNames()
    colNames = table.getColumnNames()
    for rowName in rowNames:
        for colName in colNames:
            count1 = table.getCount(rowName=rowName, colName=colName)
            if count1 == None:
                continue
            count = count1.clone()
            N = 1

            for t in tablesCopy[1:]:
                if colName not in t.getColumnNames():
                    continue

                count2 = t.getCount(rowName=rowName, colName=colName)
                if count2 == None:
                    count = None
                    break
                N += 1
                if uncertaintyByAverage:
                    count = dataset.Count(count.value()+count2.value(), count.uncertainty()+count2.uncertainty())
                else:
                    count.add(count2)

            if count != None:
                table.setCount2(dataset.Count(count.value()/N, count.uncertainty()/N), rowName=rowName, colName=colName)
            else:
                table.setCount2(None, rowName=rowName, colName=colName)
    return table


def meanTableFast(tables, uncertaintyByAverage=False):
    if len(tables) == 0:
        raise Exception("Got 0 tables")

    tablesCopy = removeColumnsRowsNotInAll(tables)

    # Calculate the sums
    table = tablesCopy[0]
    nrows = table.getNrows()
    ncolumns = table.getNcolumns()
    for t in tablesCopy[1:]:
        for iRow in xrange(nrows):
            for iCol in xrange(ncolumns):
                count1 = table.getCount(iRow, iCol)
                count2 = t.getCount(iRow, iCol)
                if count1 != None and count2 != None:
                    if uncertaintyByAverage:
                        count = dataset.Count(count1.value()+count2.value(), count1.uncertainty()+count2.uncertainty())
                    else:
                        count = count1.clone()
                        count.add(count2)
                    table.setCount(iRow, iCol, count)
                else:
                    table.setCount(iRow, iCol, None)

    # Do the average
    N = len(tablesCopy)
    for iRow in xrange(nrows):
        for iCol in xrange(ncolumns):
            count = table.getCount(iRow, iCol)
            if count != None:
                table.setCount(iRow, iCol, dataset.Count(count.value()/N, count.uncertainty()/N))

    return table

## Create a new CounterTable as the fitted value of the tables
#
# \param tables  List of counter.CounterTable objects
#
# \return tuple with a table containing the values with uncertainties, and another table with the chi2 and ndof.
#
# For each cell, fit a zero-order polynomial (constant) to the values
# from tables. The value and uncertainty from the fit is returned in
# one table. The chi2 and ndof ofthe fit are returned in another
# table, such that the count value is chi2, and uncertainty is ndof
# (hacky, but works).
 
def meanTableFit(tables):
    if len(tables) == 0:
        raise Exception("Got 0 tables")

    tablesCopy = removeColumnsRowsNotInAll(tables)
    valueTable = tablesCopy[0].clone()
    chi2Table = valueTable.clone()
    nrows = valueTable.getNrows()
    ncolumns = valueTable.getNcolumns()
    for iRow in xrange(nrows):
        for iCol in xrange(ncolumns):
            values = []
            for t in tablesCopy:
                count = t.getCount(iRow, iCol)
                if count != None:
                    values.append(count)
            (m, dm, chi2, ndof) = utilities.leastSquareFitPoly0([v.value() for v in values], [v.uncertainty() for b in values])
            if m != None:
                valueTable.setCount(iRow, iCol, dataset.Count(m, dm))
                chi2Table.setCount(iRow, iCol, dataset.Count(chi2, ndof))
            else:
                valueTable.setCount(iRow, iCol, None)
                chi2Table.setCount(iRow, iCol, None)

    return (valueTable, chi2Table)
                

## Helper function for index or name access for counts in counter.CounterColumn, counter.CounterRow and counter.CounterTable
#
# \param index   Index of the count (can be None)
# \param name    Name of the count (can be None)
# \param names   List of names to look the index, if name is given
def _indexNameHelper(index, name, names):
    ind = index
    if index == None and name == None:
        raise Exception("Give either index or name, neither was given")
    if index != None and name != None:
        raise Exception("Give either index or name, not both")
    if index == None:
        try:
            ind = names.index(name)
        except ValueError:
            raise Exception("Name '%s' does not exist in list '%s'" %(name, ",".join(names)))
    return ind

## Class representing a column in counter.CounterTable.
#
# The columns in counter.CounterTable are not stored as CounterColumn
# objects, but can be exported/imported as CounterColumn objects.
class CounterColumn:
    ## Constructor
    #
    # \param name      Name of the column
    # \param rowNames  List of names of the rows
    # \param values    Values for rows (dataset.Count objects)
    #
    # Lengths of rowNames and values should be equal. 
    def __init__(self, name, rowNames, values):
        self.name = name
        self.rowNames = rowNames
        self.values = values

        if len(rowNames) != len(values):
            raise Exception("len(rowNames) != len(values) (%d != %d)" % (len(rowNames), len(values)))

    ## Clone a column
    def clone(self):
        return CounterColumn(self.name, self.rowNames[:], [v.clone() for v in self.values])

    ## Get the column values as (name, count) pairs
    def getPairList(self):
        return [(self.rowNames[i], self.values[i]) for i in xrange(0, len(self.values))]

    ## Get the name of the column
    def getName(self):
        return self.name

    ## Set the name of the colunn
    def setName(self, name):
        self.name = name

    ## Get the number of rows
    def getNrows(self):
        return len(self.values)

    ## Get row name with row index
    #
    # \param irow   Index of a row
    def getRowName(self, irow):
        return self.rowNames[irow]

    ## Get all row names
    def getRowNames(self):
        return self.rowNames

    ## Get count with row index or row name
    #
    # \param index   Row index (forwarded to counter._indexNameHelper())
    # \param name    Row name (forwarded to counter._indexNameHelper())
    def getCount(self, index=None, name=None):
        return self.values[_indexNameHelper(index, name, self.rowNames)]

    ## Set count to a row
    #
    # \param irow   Row index
    # \param count  New count
    def setCount(self, irow, count):
        self.values[irow] = count

    ## Remove row
    #
    # \param irow   Row index
    def removeRow(self, irow):
        del self.values[irow]
        del self.rowNames[irow]

    ## Multiply column with a value (possibly with uncertainty)
    #
    # \param value        Value to multiply with
    # \param uncertainty  Uncertainty of the value
    #
    # Uncertainty is propagated with error propagation
    def multiply(self, value, uncertainty=0):
        count = dataset.Count(value, uncertainty)
        for v in self.values:
            v.multiply(count)

    ## \var name
    # Name of the column
    ## \var rowNames
    # List of row names
    ## \var values
    # List of row values (dataset.Count objects, or None for non-existing value)

## Class representing a row in CounterTable
#
# The columns in counter.CounterTable are not stored as CounterColumn
# objects, but can be exported/imported as CounterColumn objects.
class CounterRow:
    ## Constructor
    #
    # \param name      Name of the row
    # \param columnNames  List of names of the columns
    # \param values    Values for columns (dataset.Count objects)
    #
    # Lengths of columnNames and values should be equal. 
    def __init__(self, name, columnNames, values):
        self.name = name
        self.columnNames = columnNames
        self.values = values

        if len(columnNames) != len(values):
            raise Exception("len(columnNames) != len(values) ( %d! = %d)" % (len(columnNames), len(values)))
    
    ## Clone a row
    def clone(self):
        return CounterRow(self.name, self.columnNames[:], [v.clone() for v in self.values])

    ## Get the name of the row
    def getName(self):
        return self.name

    ## Set the name of the row
    def setName(self, name):
        self.name = name

    ## Get the number of columns
    def getNcolumns(self):
        return len(self.values)

    ## Get column name with column index
    #
    # \param icol  Index of a colunmn
    def getColumnName(self, icol):
        return self.columnNames[icol]

    ## Get all column names
    def getColumnNames(self):
        return self.columnNames

    ## Get a count with column index or column name
    #
    # \param index   Column index (forwarded to counter._indexNameHelper())
    # \param name    Column name (forwarded to counter._indexNameHelper())
    def getCount(self, index=None, name=None):
        return self.values[_indexNameHelper(index, name, self.columnNames)]

    def setCount(self, icol, count):
        self.values[icol] = count

    def removeColumn(self, icol):
        del self.values[icol]
        del self.columnNames[icol]

    ## \var name
    # Name of the row
    ## \var columnNames
    # List of column names
    ## \var values
    # List of column values (dataset.Count objects, or None for non-existing value)


## Class to represent a table of counts.
# 
# It is separated from Counter class in order to contain only the
# table and to have certain table operations.
#
# Table is stored as 2D list of [row][column]. Rows and columns can be
# exported/imported as counter.CounterRow and counter.CounterColumn
# objects, respectively. Table values are dataset.Count objects, or
# None's if a count doesn't exist for some row/column.
class CounterTable:
    ## Constructor
    #
    # Table is constructed as empty
    def __init__(self):
        self.rowNames = []
        self.columnNames = []
        self.table = [] # table[row][column]

    ## Clone the table
    def deepCopy(self):
        return copy.deepcopy(self)

    ## Clone the table
    def clone(self):
        return self.deepCopy()

    ## Transpose the table
    def transpose(self):
        colNames = self.rowNames
        rowNames = self.columnNames

        table = []
        if len(self.table) > 0:
            for icol in xrange(len(self.table[0])):
                row = []
                for irow in xrange(len(self.table)):
                    row.append(self.table[irow][icol])
                table.append(row)

        self.table = table
        self.rowNames = rowNames
        self.columnNames = colNames

    def multiply(self, value, uncertainty=0):
        count = dataset.Count(value, uncertainty)
        for irow in xrange(len(self.table)):
            for icol in xrange(len(self.table[0])):
                self.table[irow][icol].multiply(count)

    ## Get the number of rows
    def getNrows(self):
        return len(self.table)

    ## Get the number of columns
    def getNcolumns(self):
        if self.getNrows() == 0:
            return 0
        return len(self.table[0])

    ## Get count with row and column index or name
    #
    # \param irow      Row index (forwarded to counter._indexNameHelper)
    # \param icol      Column index (forwarded to counter._indexNameHelper)
    # \param rowName   Row name (forwarded to counter._indexNameHelper)
    # \param colName   Column name (forwarded to counter._indexNameHelper)
    def getCount(self, irow=None, icol=None, rowName=None, colName=None):
        ir = _indexNameHelper(irow, rowName, self.rowNames)
        ic = _indexNameHelper(icol, colName, self.columnNames)

        return self.table[ir][ic]

    ## Set count with row and column index
    #
    # \param irow   Row index
    # \param icol   Column index
    # \param value  Value to insert (dataset.Count object)
    def setCount(self, irow, icol, value):
        self.table[irow][icol] = value

    ## Set count with row and column index or name
    #
    # \param value  Value to insert (dataset.Count object)
    # \param irow      Row index (forwarded to counter._indexNameHelper)
    # \param icol      Column index (forwarded to counter._indexNameHelper)
    # \param rowName   Row name (forwarded to counter._indexNameHelper)
    # \param colName   Column name (forwarded to counter._indexNameHelper)
    def setCount2(self, value, irow=None, icol=None, rowName=None, colName=None):
        ir = _indexNameHelper(irow, rowName, self.rowNames)
        ic = _indexNameHelper(icol, colName, self.columnNames)
        self.table[ir][ic] = value

    ## Get row names
    def getRowNames(self):
        return self.rowNames

    ## Rename rows
    #
    # \param mapping   Dictionary providing old name -> new name mapping
    def renameRows(self, mapping):
        for irow, row in enumerate(self.rowNames):
            if row in mapping:
                self.rowNames[irow] = mapping[row]

    ## Get column names
    def getColumnNames(self):
        return self.columnNames

    ## Rename columns
    #
    # \param mapping   Dictionary providing old name -> new name mapping
    def renameColumns(self, mapping):
        for icol, col in enumerate(self.columnNames):
            if col in mapping:
                self.columnNames[icol] = mapping[col]

    ## Get column index from column name
    def indexColumn(self, name):
        try:
            return self.columnNames.index(name)
        except ValueError:
            raise Exception("Column '%s' not found" % name)

    ## Append a column
    #
    # \param column  counter.CounterColumn or counter.Counter object
    #
    # New column is inserted as the last column in the table
    def appendColumn(self, column):
        self.insertColumn(self.getNcolumns(), column)

    ## Insert a column
    #
    # \param icol    Index where to insert the new column
    # \param column  counter.CounterColumn or counter.Counter object
    #
    # If the new column contains rows which don't already exist in the
    # table, these rows are added in the proper places in the table,
    # and the existing columns get None values. The row matching is
    # done with the row names.
    def insertColumn(self, icol, column):
        beginColumns = 0
        if len(self.table) > 0:
            beginColumns = len(self.table[0])

        if icol > beginColumns:
            raise Exception("Unable to insert column %d, table has only %d columns (may not insert to index larger than size)" % (icol, beginColumns))

        iname = 0
        icount = 0
        while iname < len(self.rowNames)  and icount < column.getNrows():
            # Check if the current indices give the same counter name for both
            if self.rowNames[iname] == column.getRowName(icount):
                self.table[iname].insert(icol, column.getCount(icount))
                iname += 1
                icount += 1
                continue

            # Search the list of names for the name of count
            found = False
            for i in xrange(iname, len(self.rowNames)):
                if self.rowNames[i] == column.getRowName(icount):
                    self.table[i].insert(icol, column.getCount(icount))
                    iname = i+1
                    icount += 1
                    found = True
                    break
            if found:
                continue

            # Count not found, insert the count after the previous
            # found name
            self.rowNames.insert(iname, column.getRowName(icount))
            row = [None]*(beginColumns+1)
            row[icol] = column.getCount(icount)
            self.table.insert(iname, row)
            iname += 1
            icount += 1

        # Add the remaining counters from column
        for i in xrange(icount, column.getNrows()):
            self.rowNames.append(column.getRowName(i))
            row = [None]*(beginColumns+1)
            row[icol] = column.getCount(i)
            self.table.append(row)

        for irow, row in enumerate(self.table):
            def value(count):
                if count == None:
                    return count
                else:
                    return count.value()
            # Append None to row if column didn't have 
            if len(row) == beginColumns:
                row.insert(icol, None)
            # Sanity check
            elif len(row) < beginColumns:
                print [value(c) for c in row]
                raise Exception("Internal error at row %d: len(row) = %d, beginColumns = %d" % (irow, len(row), beginColumns))
            elif len(row) > beginColumns+1:
                print [value(c) for c in row]
                raise Exception("Internal error at row %d: len(row) = %d, beginColumns = %d" % (irow, len(row), beginColumns))

        self.columnNames.insert(icol, column.getName())


    ## Get column by index or by name.
    #
    # \param index   Column index (forwarded to counter._indexNameHelper)
    # \param name    Column name (forwarded to counter._indexNameHelper)
    #
    # \return counter.CounterColumn object
    def getColumn(self, index=None, name=None):
        icol = _indexNameHelper(index, name, self.columnNames)
        
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

    ## Remove a column by index or by name
    #
    # \param index   Column index (forwarded to counter._indexNameHelper)
    # \param name    Column name (forwarded to counter._indexNameHelper)
    def removeColumn(self, index=None, name=None):
        icol = _indexNameHelper(index, name, self.columnNames)

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

    ## Keep these columns, remove all other columns
    #
    # \param names  List of column names to keep
    def keepOnlyColumns(self, names):
        for name in self.getColumnNames()[:]:
            if not name in names:
                self.removeColumn(name=name)

    ## Remove columns which are not full
    #
    # If row as at least one None, it is removed
    def removeNonFullColumns(self):
        nrows = self.getNrows()
        ncolumns = self.getNcolumns()
        removeColumns = []

        for icol in xrange(0, ncolumns):
            allFull = True
            for irow in xrange(0, nrows):
                if self.getCount(irow, icol) == None:
                    allFull = False
                    break
            if not allFull:
                removeColumns.append(icol-len(removeColumns)) # hack to take into account the change in indices when removing a column
        for icol in removeColumns:
            self.removeColumn(icol)

    ## Get row index from row name
    def indexRow(self, name):
        try:
            return self.rowNames.index(name)
        except ValueError:
            raise Exception("Row '%s' not found" % name)

    ## Append a row
    #
    # \param row  counter.CounterRow object
    #
    # New row is inserted as the last row in the table
    def appendRow(self, row):
        self.insertRow(self.getNrows(), row)

    ## Insert a row
    #
    # \param irow    Index where to insert the new row
    # \param row     counter.CounterRow object
    #
    # If the new row contains columns which don't already exist in the
    # table, these columnss are added in the proper places in the
    # table, and the existing rows get None values. The column
    # matching is done with the column names.
    def insertRow(self, irow, row):
        beginRows = len(self.table)

        if irow > beginRows:
            raise Exception("Unable to insert row %d, table has only %d rows (may not insert to index larger than size)" % (row, beginRows))


        # The columns which already exist in the table
        rowCells = [None]*self.getNcolumns()
        colNamesLeft = row.getColumnNames()[:]
        for icount in xrange(0, row.getNcolumns()):
            colName = row.getColumnName(icount)
            if colName in self.columnNames:
                rowCells[self.columnNames.index(colName)] = row.getCount(icount)
                del colNamesLeft[colNamesLeft.index(colName)]

        # The columns which are new
        if len(colNamesLeft) > 0:
            for name in colNamesLeft:
                rowCells.append(row.getCount(row.getColumnNames().index(name)))
            for i in xrange(0, self.getNrows()):
                self.table[i].extend([None]*len(colNamesLeft))
            self.columnNames.extend(colNamesLeft)

        self.table.insert(irow, rowCells)
        self.rowNames.insert(irow, row.getName())

    ## Get row by index or by name.
    #
    # \param index   Row index (forwarded to counter._indexNameHelper)
    # \param name    Row name (forwarded to counter._indexNameHelper)
    #
    # \return counter.CounterRow object
    def getRow(self, index=None, name=None):
        irow = _indexNameHelper(index, name, self.rowNames)
    
        colNames = self.columnNames[:]
        rowValues = self.table[irow][:]

        # Filter out Nones
        i = 0
        while i < len(rowValues):
            if rowValues[i] == None:
                del colNames[i]
                del rowValues[i]
                i -= 1
            i += 1

        # Constructo the row object
        return CounterRow(self.rowNames[irow], colNames, rowValues)

    ## Remove a row by index or by name
    #
    # \param index   Row index (forwarded to counter._indexNameHelper)
    # \param name    Row name (forwarded to counter._indexNameHelper)
    def removeRow(self, index=None, name=None):
        irow = _indexNameHelper(index, name, self.rowNames)

        del self.rowNames[irow]
        del self.table[irow]

    ## Keep these rows, remove all other rows
    #
    # \param names  List of row names to keep
    def keepOnlyRows(self, names):
        for name in self.getRowNames()[:]:
            if not name in names:
                self.removeRow(name=name)

    ## Remove rows which are not full
    #
    # If row as at least one None, it is removed
    def removeNonFullRows(self):
        nrows = self.getNrows()
        ncolumns = self.getNcolumns()
        removeRows = []

        for irow in xrange(0, nrows):
            allFull = True
            for icol in xrange(0, ncolumns):
                if self.getCount(irow, icol) == None:
                    allFull = False
                    break
            if not allFull:
                removeRows.append(irow-len(removeRows)) # hack to take into account the change in indices when removing a row
        for irow in removeRows:
            self.removeRow(index=irow)


    ## Header row for table formatting
    def _header(self):
        return ["Counter"] + self.columnNames

    ## Table content for table formatting
    #
    # \param formatter   Table formatting object (counter.TableFormatBase)
    def _content(self, formatter):
        content = []
        for irow in xrange(self.getNrows()):
            content.append([self.rowNames[irow]])

        for icol in xrange(self.getNcolumns()):
            formatter.setCurrentColumn(self.columnNames[icol], icol)

            for irow in xrange(self.getNrows()):
                count = self.getCount(irow, icol)
                if count != None:
                    content[irow].append(formatter.formatCell(count))
                else:
                    content[irow].append("")
        return content

    ## Calculate the column widths for table formatting
    def _columnWidths(self, content):
        widths = [0]*(len(content[0]))
        for row in content:
            for icol, col in enumerate(row):
                widths[icol] = max(widths[icol], len(col))
        return widths

    ## Format the table
    #
    # \param formatter   Table formatting object (counter.TableFormatBase)
    # \param splitter    Possible content splitter object (counter.TableSplitter)
    #
    # \return Table formatted as a string
    def format(self, formatter=TableFormatText(), splitter=None, header=True):
        if self.getNcolumns() == 0 or self.getNrows() == 0:
            return ""

        content = []
        if header:
            content.append(self._header())
        content.extend(self._content(formatter))

        if splitter != None:
            content = splitter.split(content)

        nrows = len(content)
        ncols = len(content[0])

        columnWidths = self._columnWidths(content)
        columnFormat = "{value:<{width}}"
        lines = [formatter.beginTable(ncols)]
        lastRow = nrows-1
        lastColumn = ncols-1
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

    ## \var rowNames
    # List of row names
    ## \var columnNames
    # List of column names
    ## \var table
    # 2D list of values (dataset.Count objects) [row][column]

## Counter from one histogram, can not be normalized/scaled further
#
# Use case: embedding results
#
# \todo Maybe this could be consolidated with counter.CounterColumn?
class HistoCounter:
    ## Constructor
    # 
    # \param name                 Name of this counter (column)
    # \param rootHisto            TH1 containing the counts
    # \param countNameFunction    Function for mapping the X axis bin labels to count names
    def __init__(self, name, rootHisto, countNameFunction=None):
        self.name = name
        cntr = dataset._histoToCounter(rootHisto)
        self.countNames = [x[0] for x in cntr]
        self.counter = [x[1] for x in cntr]

        if countNameFunction != None:
            self.countNames = [countNameFunction(x) for x in self.countNames]

    ## Set name of the counter
    def setName(self, name):
        self.name = name

    ## Get name of the counter
    def getName(self):
        return self.name

    ## Get number of rows
    def getNrows(self):
        return len(self.countNames)

    ## Get row name
    def getRowName(self, icount):
        return self.countNames[icount]

    ## Get count
    def getCount(self, icount):
        if self.counter == None:
            self._createCounter()
        return self.counter[icount]

    ## Get count by name
    def getCountByName(self, name):
        if self.counter == None:
            self._createCounter()
        for i, cn in enumerate(self.countNames):
            if cn == name:
                return self.counter[i]
        raise Exception("No count '%s' in counter '%s'" % (name, self.getName()))

    ## \var name
    # Name of the counter
    ## \var countNames
    # List of count names (rows)
    ## \var counter
    # List of counts (dataset.Count objects)

## Counter for one dataset (a column in the counter.CounterTable)
class SimpleCounter:
    ## Constructor
    #
    # \param  datasetRootHisto   dataset.DatasetRootHisto object containing the dataset and the histogram for the counter
    # \param  countNameFunction  Function for mapping the X axis bin labels to count names
    def __init__(self, datasetRootHisto, countNameFunction):
        self.datasetRootHisto = datasetRootHisto
        self.counter = None
        if countNameFunction != None:
            self.countNames = [countNameFunction(x) for x in datasetRootHisto.getBinLabels()]
        else:
            self.countNames = datasetRootHisto.getBinLabels()

    ## Append a row from TTree
    #
    # \param rowName    Name of the new row
    # \param treeDraw   dataset.TreeDraw object containing the TTree name, event selection, and weighting
    def appendRow(self, rowName, treeDraw):
        if self.counter != None:
            raise Exception("Can't add row after the counters have been created!")
        td = dataset.treeDrawToNumEntries(treeDraw) # get a clone suitable to calculate number of entries from
        drh = self.datasetRootHisto.getDataset().getDatasetRootHisto(td)
        self.datasetRootHisto.modifyRootHisto(lambda oldHisto, newHisto: _counterTh1AddBinFromTh1(oldHisto, rowName, newHisto), drh)
        self.countNames.append(rowName)

    ## Append rows from another TH1
    #
    # \param histoPath           Path to TH1
    # \param countNameFunction   Function for mappting the X axis bin labels to count names
    def appendRows(self, histoPath, countNameFunction=None):
        if self.counter != None:
            raise Exception("Can't add rows after the counters have been created!")

        drh = self.datasetRootHisto.getDataset().getDatasetRootHisto(histoPath)
        self.datasetRootHisto.modifyRootHisto(_counterTh1AddBinsFromTh1, drh)
        
        if countNameFunction != None:
            self.countNames.extend([countNameFunction(x) for x in drh.getBinLabels()])
        else:
            self.countNames.extend(drh.getBinLabels())

    ## Set normalization scheme to unit area
    def normalizeToOne(self):
        if self.counter != None:
            raise Exception("Can't normalize after the counters have been created!")
        self.datasetRootHisto.normalizeToOne()

    ## Set MC normalization scheme to cross section
    def normalizeMCByCrossSection(self):
        if self.counter != None:
            raise Exception("Can't normalize after the counters have been created!")
        if self.datasetRootHisto.getDataset().isMC():
            self.datasetRootHisto.normalizeByCrossSection()

    ## Set MC normalization scheme to luminosity
    #
    # \param lumi  Integrated luminosity (in pb^-1)
    def normalizeMCToLuminosity(self, lumi):
        if self.counter != None:
            raise Exception("Can't normalize after the counters have been created!")
        if self.datasetRootHisto.getDataset().isMC():
            self.datasetRootHisto.normalizeToLuminosity(lumi)

    ## Scale (multiply) the counter with a value
    def scale(self, value):
        if self.counter != None:
            raise Exception("Can't scale after the counters have been created!")
        self.datasetRootHisto.scale(value)

    def _createCounter(self):
        h = self.datasetRootHisto.getHistogram()
        self.counter = [x[1] for x in dataset._histoToCounter(h)]
        h.Delete()

    ## Get the name of the dataset
    def getName(self):
        return self.datasetRootHisto.getDataset().getName()

    ## Get number of rows
    def getNrows(self):
        return len(self.countNames)

    ## Get row names
    def getRowName(self, icount):
        return self.countNames[icount]

    ## Get count by row index
    def getCount(self, icount):
        if self.counter == None:
            self._createCounter()
        return self.counter[icount]

    ## Get dataset.Dataset object
    def getDataset(self):
        return self.datasetRootHisto.getDataset()

    ## Get count by row name
    def getCountByName(self, name):
        if self.counter == None:
            self._createCounter()
        for i, cn in enumerate(self.countNames):
            if cn == name:
                return self.counter[i]
        raise Exception("No count '%s' in counter '%s'" % (name, self.getName()))

    def constructTEfficiency(self, function):
        (passed, total) = function(self)
        return ROOT.TEfficiency(passed, total)

    ## \var datasetRootHisto
    # dataset.DatasetRootHisto object containing the dataset.Dataset
    # and ROOT histogram of the counter
    ## \var counter
    # List of dataset.Count objects constructed from the counter ROOT histogram
    ## \var countNames
    # List of count (row) names constructed from the counter ROOT histogram

## Counter for many datasets (i.e. table, column per dataset)
class Counter:
    ## Constructor
    #
    # \param datasetRootHistos   List of dataset.DatasetRootHisto objects
    # \param countNameFunction  Function for mapping the X axis bin labels to count names
    #
    # Creates on counter.SimpleCounter for each dataset
    def __init__(self, datasetRootHistos, countNameFunction):
        self.counters = [SimpleCounter(h, countNameFunction) for h in datasetRootHistos]

    ## Loop through datasets calling the given function
    def forEachDataset(self, func):
        return [func(c) for c in self.counters]

    def getColumnNames(self):
        return [c.getName() for c in self.counters]

    ## Remove columns
    #
    # \param datasetNames   Names of datasets to remove
    def removeColumns(self, datasetNames):
        i = 0
        while i < len(self.counters):
            if self.counters[i].getName() in datasetNames:
                del self.counters[i]
            else:
                i += 1

    ## Append a row from TTree
    #
    # \param rowName    Name of the new row
    # \param treeDraw   dataset.TreeDraw object containing the TTree name, event selection, and weighting
    def appendRow(self, rowName, treeDraw):
        self.forEachDataset(lambda x: x.appendRow(rowName, treeDraw))

    ## Append rows from another TH1
    #
    # \param histoPath  Path to TH1
    def appendRows(self, histoPath):
        self.forEachDataset(lambda x: x.appendRows(histoPath))

    ## Set normalization scheme to unit area
    def normalizeToOne(self):
        self.forEachDataset(lambda x: x.normalizeToOne())

    ## Set MC normalization scheme to cross section
    def normalizeMCByCrossSection(self):
        self.forEachDataset(lambda x: x.normalizeMCByCrossSection())

    ## Set the MC normalization scheme to luminosity, take lumi from data dataset
    def normalizeMCByLuminosity(self):
        lumi = None
        for c in self.counters:
            if c.datasetRootHisto.getDataset().isData():
                if lumi != None:
                    raise Exception("Unable to normalize by luminosity, more than one data datasets (you might want to merge data datasets)")
                lumi = c.datasetRootHisto.getDataset().getLuminosity()
        if lumi == None:
            raise Exception("Unable to normalize by luminosity. no data datasets")

        self.normalizeMCToLuminosity(lumi)

    ## Set MC normalization scheme to luminosity
    #
    # \param lumi  Integrated luminosity (in pb^-1)
    def normalizeMCToLuminosity(self, lumi):
        self.forEachDataset(lambda x: x.normalizeMCToLuminosity(lumi))

    ## Scale (multiply) counters with a value
    def scale(self, value):
        self.forEachDataset(lambda x: x.scale(value))

    ## Scale (multiply) MC counters with a value
    def scaleMC(self, value):
        def scale(x):
            if x.getDataset().isMC():
                x.scale(value)
        self.forEachDataset(scale)

    ## Scale (multiply) data counters with a value
    def scaleData(self, value):
        def scale(x):
            if x.getDataset().isData():
                x.scale(value)
        self.forEachDataset(scale)

    ## Create counter.CounterTable() from the counters
    def getTable(self):
        table = CounterTable()
        for h in self.counters:
            table.appendColumn(h)
        return table

    def constructTEfficiencies(self, function):
        return self.forEachDataset(lambda x: x.constructTEfficiency(function))

    ## \var counters
    # List of counter.SimpleCounter objects, one per dataset

## Event counter corresponding to a dataset.DatasetManager
#
# Provides access to the main event counter, and the subcounters of
# all datasets in a dataset.DatasetManager.
class EventCounter:
    ## Constructor
    #
    # \param datasets            dataset.DatasetManager, or (single or list) dataset.Dataset (or similar) object
    # \param countNameFunction   Function for mapping the X axis bin labels to count names (optional)
    # \param counters            Counter directory within the dataset.Dataset TFiles (if not given, use the counter from dataset.DatasetManager object)
    # \param mainCounterOnly     If True, read only the main counter (default: False)
    # \param kwargs              Keyword arguments, passed to Dataset.getDatasetRootHisto() when reading the counter histograms
    #
    # Creates counter.Counter for the main counter and each subcounter
    def __init__(self, datasets, countNameFunction=None, counters=None, mainCounterOnly=False, **kwargs):
        counterNames = {}

        allDatasets = []
        if hasattr(datasets, "getAllDatasets"):
            allDatasets = datasets.getAllDatasets()
        elif isinstance(datasets, list):
            allDatasets = datasets[:]
        else:
            allDatasets = [datasets]

        if len(allDatasets) == 0:
            raise Exception("No datasets")

        # Take the default counter directory if none is explicitly given
        counterDir = counters
        if counterDir == None:
            for dataset in allDatasets:
                if counterDir == None:
                    counterDir = dataset.getCounterDirectory()
                else:
                    if counterDir != dataset.getCounterDirectory():
                        raise Exception("Sanity check failed, datasets have different counter directories!")
        # Pick all possible names of counters
        for dataset in allDatasets:
            for name in dataset.getDirectoryContent(counterDir, lambda obj: isinstance(obj, ROOT.TH1)):
                counterNames[name] = 1

        try:
            del counterNames["counter"]
        except KeyError:
            raise Exception("Error: no 'counter' histogram in the '%s' directories" % counterDir)

        def getDatasetRootHistos(path):
            return [d.getDatasetRootHisto(path, **kwargs) for d in allDatasets]

        self.mainCounter = Counter(getDatasetRootHistos(counterDir+"/counter"), countNameFunction)
        self.subCounters = {}
        if not mainCounterOnly:
            for subname in counterNames.keys():
                try:
                    self.subCounters[subname] = Counter(getDatasetRootHistos(counterDir+"/"+subname), countNameFunction)
                except:
                    pass

        self.normalization = "None"

    ## Remove columns
    #
    # \param datasetNames   Names of datasets to remove
    def removeColumns(self, datasetNames):
        self._forEachCounter(lambda c: c.removeColumns(datasetNames))

    ## Loop through all counters calling the given function
    def _forEachCounter(self, func):
        func(self.mainCounter)
        for c in self.subCounters.itervalues():
            func(c)

    ## Set normalization scheme to unit area
    def normalizeToOne(self):
        self._forEachCounter(lambda x: x.normalizeToOne())
        self.normalization = "All normalized to unit area"

    ## Set MC normalization scheme to cross section
    def normalizeMCByCrossSection(self):
        self._forEachCounter(lambda x: x.normalizeMCByCrossSection())
        self.normalization = "MC normalized to cross section (pb)"

    ## Set the MC normalization scheme to luminosity, take lumi from data dataset
    def normalizeMCByLuminosity(self):
        self._forEachCounter(lambda x: x.normalizeMCByLuminosity())
        self.normalization = "MC normalized by data luminosity"

    ## Set MC normalization scheme to luminosity
    #
    # \param lumi  Integrated luminosity (in pb^-1)
    def normalizeMCToLuminosity(self, lumi):
        self._forEachCounter(lambda x: x.normalizeMCToLuminosity(lumi))
        self.normalization = "MC normalized to luminosity %f pb^-1" % lumi

    ## Scale (multiply) counters with a value
    def scale(self, value):
        self._forEachCounter(lambda x: x.scale(value))
        self.normalization += " (scaled with %g)" % value

    ## Scale (multiply) data counters with a value
    def scaleMC(self, value):
        self._forEachCounter(lambda x: x.scaleMC(value))
        self.normalization += " (MC scaled with %g)" % value

    ## Create counter.CounterTable() from the counters
    def scaleData(self, value):
        self._forEachCounter(lambda x: x.scaleData(value))
        self.normalization += " (data scaled with %g)" % value

    ## Get the counter.Counter of main counter
    def getMainCounter(self):
        return self.mainCounter

    ## Get the counter.CounterTable from the main counter
    def getMainCounterTable(self):
        return self.mainCounter.getTable()

    ## Get names of subcounters
    def getSubCounterNames(self):
        return self.subCounters.keys()

    ## Get the counter.Counter of a subcounter
    #
    # \param name  Name of subcounter
    def getSubCounter(self, name):
        return self.subCounters[name]

    ## Get the counter.CounterTable from a subcounter
    #
    # \param name  Name of subcounter
    def getSubCounterTable(self, name):
        return self.subCounters[name].getTable()

    ## Get current normalization scheme string
    def getNormalizationString(self):
        return self.normalization

    ## \var mainCounter
    # counter.Counter object for the main counter
    ## \var subCounters
    # Dictionary of counter.Counter objects for the subcounters.
    # Subcounter names serve as the keys.
    ## \var normalization
    # Name of current normalization scheme
