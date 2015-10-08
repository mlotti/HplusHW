# Description: Extension of counter with arbitrary many uncertainties
# Note: Make sure to include the keyword "stat" or "syst" in label of each uncertainty
#
# Authors: LAW

import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
from math import sqrt

## Represents counter count value with multiple uncertainty fields.
class ExtendedCount:
    ## Constructor
    def __init__(self, value, uncertaintyList, uncertaintyLabelList):
        # Make sure the values are of floating point type
        self._value = float(value)
        self._uncertaintyList = []
        for v in uncertaintyList:
            self._uncertaintyList.append(float(v))
        # Note: without the list(), one would copy the pointers instead of the values
        self._uncertaintyLabelList = list(uncertaintyLabelList)
        # check that list lengths match
        if len(uncertaintyList) != len(uncertaintyLabelList):
            raise Exception (ShellStyles.ErrorLabel()+"ExtendedCount::__init__(): please provide equal amount of entries for uncertaintyList and uncertaintyLabelList! (%d vs. %d)"%(len(uncertaintyList),len(uncertaintyLabelList)))
        # check that labels contain word 'stat' or 'syst'
        for item in self._uncertaintyLabelList:
            myFoundStatus = False
            if "stat" in item:
                myFoundStatus = True
            elif "syst" in item:
                myFoundStatus = True
            if not myFoundStatus:
                raise Exception (ShellStyles.ErrorLabel()+"ExtendedCount::__init__(): uncertainty labels must contain 'stat' or 'syst' in them!")

    def copy(self):
        return ExtendedCount(self._value, self._uncertaintyList, self._uncertaintyLabelList)

    def clone(self):
        return self.copy()

    def value(self):
        return self._value

    ## Return list of labels
    def labels(self):
        return self._uncertaintyLabelList

    ## Get uncertainty by label
    def uncertainty(self, label):
        for i in range(0, len(self._uncertaintyLabelList)):
            if label == self._uncertaintyLabelList[i]:
                return self._uncertaintyList[i]
        raise Exception(ShellStyles.ErrorLabel()+"ExtendedCount::uncertainty(): Cannot find asked label '%s'! options are: %s"%(label, ', '.join(map(str,self._uncertaintyLabelList))))

    # Getters for stat. uncertainty
    def statUncertainty(self):
        myUncertainty = 0.0
        for i in range(0, len(self._uncertaintyLabelList)):
            if "stat" in self._uncertaintyLabelList[i]:
                myUncertainty += self._uncertaintyList[i]**2
        return sqrt(myUncertainty)

    def statUncertaintyLow(self):
        return self.statUncertainty()

    def statUncertaintyHigh(self):
        return self.statUncertainty()

    # Getters for syst. uncertainty
    def systUncertainty(self):
        myUncertainty = 0.0
        for i in range(0, len(self._uncertaintyLabelList)):
            if "syst" in self._uncertaintyLabelList[i]:
                myUncertainty += self._uncertaintyList[i]**2
        return sqrt(myUncertainty)

    def systUncertaintyLow(self):
        return self.systUncertainty()

    def systUncertaintyHigh(self):
        return self.systUncertainty()

    # Getters for total uncertainty
    def totalUncertainty(self):
        myUncertainty = 0.0
        for i in range(0, len(self._uncertaintyLabelList)):
            myUncertainty += self._uncertaintyList[i]**2
        return sqrt(myUncertainty)

    def totalUncertaintyLow(self):
        return self.totalUncertainty()

    def totalUncertaintyHigh(self):
        return self.totalUncertainty()

    ## self = self + count
    def add(self, count):
        self._value += count._value
        for i in range(0, len(self._uncertaintyLabelList)):
            self._uncertaintyList[i] = sqrt(self._uncertaintyList[i]**2 + count.uncertainty(self._uncertaintyLabelList[i])**2)

    ## self = self - count
    def subtract(self, count):
        self.add(ExtendedCount(-count._value, count._uncertaintyList, count._uncertaintyLabelList))

    ## self = self * count
    def multiply(self, count):
        for i in range(0, len(self._uncertaintyLabelList)):
            self._uncertaintyList[i] = sqrt((count.value() * self._uncertaintyList[i])**2 +
                                            (self.value() * count.uncertainty(self._uncertaintyLabelList[i]))**2)
        self._value = self._value * count._value

    ## self = self * scalar (scalar has no uncertainties)
    def multiplyByScalar(self, scalar):
        for i in range(0, len(self._uncertaintyLabelList)):
            self._uncertaintyList[i] *= scalar
        self._value = self._value * scalar

    ## self = self / count
    def divide(self, count):
        for i in range(0, len(self._uncertaintyLabelList)):
            self._uncertaintyList[i] = sqrt((self._uncertaintyList[i] / count.value())**2 +
                                            (self._value / (count.value()**2) * count.uncertainty(self._uncertaintyLabelList[i]))**2)
        self._value = self._value / count._value

    ## self = self / scalar (scalar has no uncertainties)
    def divideByScalar(self, scalar):
        for i in range(0, len(self._uncertaintyLabelList)):
            self._uncertaintyList[i] /= scalar
        self._value = self._value / scalar

    ## minimum
    def minimum(self, count):
        if count == None:
            return
        if count.value() < self.value() and count.value() > 0.0:
            self._value = count._value
            self._uncertaintyList = list(count._uncertaintyList)
            self._uncertaintyLabelList = list(count._uncertaintyLabelList)

    ## maximum
    def maximum(self, count):
        if count == None:
            return
        if count.value() > self.value():
            self._value = count._value
            self._uncertaintyList = list(count._uncertaintyList)
            self._uncertaintyLabelList = list(count._uncertaintyLabelList)

    def printContents(self):
        s = "%f"%self.value()
        for i in range(0, len(self._uncertaintyLabelList)):
            s += " +- %f (%s)"%(self._uncertaintyList[i], self._uncertaintyLabelList[i])
        print s

    def getResultStringFull(self, formatStr):
        s = "%s"%formatStr%self.value()
        for i in range(0, len(self._uncertaintyLabelList)):
            s += " +- %s (%s)"%(formatStr, self._uncertaintyLabelList[i])%self._uncertaintyList[i]
        return s

    def getResultStringShort(self, formatStr):
        s = "%s"%formatStr%self.value()
        s += " +- %s (stat.)"%formatStr%self.statUncertainty()
        s += " +- %s (syst.)"%formatStr%self.systUncertainty()
        return s

    def getLatexStringFull(self, formatStr):
        s = "%s"%formatStr%self.value()
        for i in range(0, len(self._uncertaintyLabelList)):
            s += " $\\pm$ %s (%s)"%(formatStr, self._uncertaintyLabelList[i])%self._uncertaintyList[i]
        return s

    def getLatexStringShort(self, formatStr):
        s = "%s"%formatStr%self.value()
        s += " $\\pm$ %s (stat.)"%formatStr%self.statUncertainty()
        s += " $\\pm$ %s (syst.)"%formatStr%self.systUncertainty()
        return s

    ## \var _value
    # Value of the count
    ## \var _uncertaintyList
    # Uncertainties of the count
    ## \var _uncertaintyLabelList
    # Label of uncertainties of the count

def validateExtendedCount(codeValidator):
    codeValidator.setPackage("ExtendedCount")
    myLabels = ["stat.", "syst.", "systAlt."]
    a = ExtendedCount(987, [123, 456, 789], myLabels)
    codeValidator.test("value()", a.value(), 987)
    codeValidator.test("uncertainty() test1", a.uncertainty("stat."), 123)
    codeValidator.test("uncertainty() test2", a.uncertainty("syst."), 456)
    codeValidator.test("uncertainty() test3", a.uncertainty("systAlt."), 789)
    codeValidator.test("statUncertainty()", a.statUncertainty(), 123)
    codeValidator.test("statUncertaintyLow()", a.statUncertaintyLow(), 123)
    codeValidator.test("statUncertaintyHigh()", a.statUncertaintyHigh(), 123)
    codeValidator.test("systUncertainty()", a.systUncertainty(), sqrt(456**2+789**2))
    codeValidator.test("systUncertaintyLow()", a.systUncertaintyLow(), sqrt(456**2+789**2))
    codeValidator.test("systUncertaintyHigh()", a.systUncertaintyHigh(), sqrt(456**2+789**2))
    codeValidator.test("totalUncertainty()", a.totalUncertainty(), sqrt(123**2+456**2+789**2))
    codeValidator.test("totalUncertaintyLow()", a.totalUncertaintyLow(), sqrt(123**2+456**2+789**2))
    codeValidator.test("totalUncertaintyHigh()", a.totalUncertaintyHigh(), sqrt(123**2+456**2+789**2))
    # Test addition
    b = ExtendedCount(256, [156, 80, 0], myLabels)
    ac = a.clone()
    ac.add(b)
    codeValidator.test("add() test1", ac.value(), 987+256)
    codeValidator.test("add() test2", ac.uncertainty("stat."), sqrt(123**2+156**2))
    codeValidator.test("add() test3", ac.uncertainty("syst."), sqrt(456**2+80**2))
    codeValidator.test("add() test4", ac.uncertainty("systAlt."), 789)
    codeValidator.test("add() test5", ac.systUncertainty(), sqrt(456**2+80**2+789**2))
    # Test subtraction
    ac = a.clone()
    ac.subtract(b)
    codeValidator.test("subtract() test1", ac.value(), 987-256)
    codeValidator.test("subtract() test2", ac.uncertainty("stat."), sqrt(123**2+156**2))
    codeValidator.test("subtract() test3", ac.uncertainty("syst."), sqrt(456**2+80**2))
    codeValidator.test("subtract() test4", ac.uncertainty("systAlt."), 789)
    codeValidator.test("subtract() test5", ac.systUncertainty(), sqrt(456**2+80**2+789**2))
    # Test multiplication
    ac = a.clone()
    ac.multiply(b)
    codeValidator.test("multiply() test1", ac.value(), 987*256)
    codeValidator.test("multiply() test2", ac.uncertainty("stat."), sqrt((256*123)**2+(987*156)**2))
    codeValidator.test("multiply() test3", ac.uncertainty("syst."), sqrt((256*456)**2+(987*80)**2))
    codeValidator.test("multiply() test4", ac.uncertainty("systAlt."), 256*789)
    codeValidator.test("multiply() test5", ac.systUncertainty(), sqrt((256*456)**2+(987*80)**2+(256*789)**2))
    # Test division
    ac = a.clone()
    ac.divide(b)
    codeValidator.test("divide() test1", ac.value(), 987.0/256.0)
    codeValidator.test("divide() test2", ac.uncertainty("stat."), sqrt((123.0/256.0)**2+(987.0*156/256**2)**2))
    codeValidator.test("divide() test3", ac.uncertainty("syst."), sqrt((456.0/256.0)**2+(987.0*80/256**2)**2))
    codeValidator.test("divide() test4", ac.uncertainty("systAlt."), 789.0/256.0)
    codeValidator.test("divide() test5", ac.systUncertainty(), sqrt((456.0/256.0)**2+(987.0*80/256**2)**2+(789.0/256)**2))
    # Test minimum
    ac = a.clone()
    ac.minimum(b)
    codeValidator.test("minimum() test1", ac.value(), 256.0)
    codeValidator.test("minimum() test2", ac.totalUncertainty(), sqrt(156**2+80**2))
    # Test maximum
    ac = a.clone()
    ac.maximum(b)
    codeValidator.test("maximum() test1", ac.value(), 987.0)
    codeValidator.test("maximum() test2", ac.totalUncertainty(), sqrt(123**2+456**2+789**2))
    # Test strings
    codeValidator.test("getResultStringFull()", a.getResultStringFull("%.1f"), "987.0 +- 123.0 (stat.) +- 456.0 (syst.) +- 789.0 (systAlt.)")
    codeValidator.test("getResultStringShort()", a.getResultStringShort("%.1f"), "987.0 +- 123.0 (stat.) +- 911.3 (syst.)")
    codeValidator.test("getLatexStringFull()", a.getLatexStringFull("%.1f"), "987.0 $\\pm$ 123.0 (stat.) $\\pm$ 456.0 (syst.) $\\pm$ 789.0 (systAlt.)")
    codeValidator.test("getLatexStringShort()", a.getLatexStringShort("%.1f"), "987.0 $\\pm$ 123.0 (stat.) $\\pm$ 911.3 (syst.)")
