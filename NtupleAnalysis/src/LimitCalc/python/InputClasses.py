#! /usr/bin/env python

import sys
import os

from HiggsAnalysis.NtupleAnalysis.tools.aux import sort

# data structures for the config file information

class ObservationInput:
    def __init__(self, datasetDefinition, shapeHistoName, histoPath, additionalNormalisation=1.0):
        self.datasetDefinition = datasetDefinition
        self.histoPath = histoPath
        self.shapeHistoName = shapeHistoName
        self.additionalNormalisation = additionalNormalisation
        return

    def getShapeHisto(self):
        return self.shapeHistoName

    def Print(self):
	print "ObservationInput :"
	print "    shapeHisto  ", self.shapeHisto
        return


class DataGroup:
    def __init__(self, 
                 landsProcess = -999,
                 validMassPoints = [],
                 label = "", 
                 nuisances = [], 
                 shapeHistoName = "", 
                 histoPath = "",
                 datasetType = "",
                 datasetDefinition = None,
                 QCDfactorisedInfo = None,
                 additionalNormalisation = 1.0):
	self.landsProcess  = landsProcess
	self.validMassPoints = validMassPoints
	self.label         = label
	self.nuisances     = nuisances
	self.shapeHistoName = shapeHistoName
	self.histoPath = histoPath
        self.datasetType   = datasetType
        self.datasetDefinition = datasetDefinition
        self.QCDfactorisedInfo = QCDfactorisedInfo
        self.additionalNormalisation = additionalNormalisation
        return

    def getId(self):
	return self.label

    def clone(self):
	return DataGroup(landsProcess = self.landsProcess,
                         validMassPoints = self.validMassPoints,
                         label        = self.label,
                         nuisances    = self.nuisances,
                         shapeHistoName   = self.shapeHistoName,
                         histoPath = self.histoPath,
                         datasetType  = self.datasetType,
                         datasetDefinition = self.datasetDefinition,
                         QCDfactorisedInfo = self.QCDfactorisedInfo,
                         additionalNormalisation= self.additionalNormalisation)

    def setLandSProcess(self,landsProcess):
	self.landsProcess = landsProcess
        return

    def setValidMassPoints(self,validMassPoints):
	self.validMassPoints = list(validMassPoints)
        return

    def setLabel(self, label):
	self.label = label
        return

    def setNuisances(self, nuisances):
        if nuisances:
            self.nuisances = nuisances[:]
        return

    def setShapeHisto(self,path,histo):
	self.histoPath = path
	self.shapeHisto = histo
        return

    def setDatasetType(self,datasetType):
        self.datasetType = datasetType
        return

    def setDatasetDefinition(self,datasetDefinition):
        self.datasetDefinition = datasetDefinition
        return

    def setQCDfactorisedInfo(self,QCDfactorisedInfo):
        self.QCDfactorisedInfo = QCDfactorisedInfo
        return

    def setAdditionalNormalisation(self,value):
	self.additionaNormalisation = value
        return

    def Print(self):
	print "    Label        ",self.label
	print "    LandS process",self.landsProcess
	print "    Valid mass points",self.validMassPoints
	print "    datasetType  ",self.datasetType
	print "    datasetDefinition",self.datasetDefinition
	print "    Additional normalisation",self.additionalNormalisation
	print "    Nuisances    ",self.nuisances
        print
        return

def convertFromSystVariationToConstant(nuisanceList, name):
    '''
    Converts a single or a bunch of nuisances by ID from syst. variation to norm. uncertainty
    '''
    myList = []
    if isinstance(name, str):
        myList.append(name)
    elif isinstance(name, list):
        myList.extend(name)
    else:
        raise Exception()

    for n in myList:
        myFoundStatus = False
        for item in nuisanceList:
            if item.id == n:
                myFoundStatus = True
                item.setDistribution("lnN")
                if item.function == "ShapeVariation":
                    item.setFunction("ShapeVariationToConstant")
                elif item.function == "ConstantToShape":
                    item.function == "Constant"
                else:
                    raise Exception("Don't know what to do for function '%s'!"%item.function)
        #if not myFoundStatus:
        #    raise Exception("Error: cannot find name '%s' in nuisance names!"%n)
    # Print remaining shape variations
    if all("shapeQ" in item.distr for item in nuisanceList):
        print "\nShape uncertainties:"
    #if len(nuisanceList) > 0:
    for item in nuisanceList:
        if item.distr == "shapeQ":
            print "... %s"%item.id
    return

def separateShapeAndNormalizationFromSystVariation(nuisanceList, name):
    myList = []
    if isinstance(name, str):
        myList.append(name)
    elif isinstance(name, list):
        myList.extend(name)
    else:
        raise Exception()

    for n in myList:
        myFoundStatus = False
        for item in nuisanceList:
            if item.id == n:
                myFoundStatus = True
                #item.setDistribution("lnN")
                if item.function == "ShapeVariation":
                    item.setFunction("ShapeVariationSeparateShapeAndNormalization")
                else:
                    raise Exception("Don't know what to do for function '%s'!"%item.function)
        #if not myFoundStatus:
        #    raise Exception("Error: cannot find name '%s' in nuisance names!"%n)
    # Print remaining shape variations
    print "\nShape and normalization uncertainties separated:"
    for item in nuisanceList:
        if item.distr == "shapeQ" and item.function == "ShapeVariationSeparateShapeAndNormalization":
            print "... %s"%item.id
    print ""
    return


class Nuisance:
    def __init__(self, id="", label="", distr="", function = "", **kwargs):
	self.setId(id)
	self.setLabel(label)
	self.setDistribution(distr)
	self.setFunction(function)
	self.kwargs = kwargs
        # self.PrintInfo()
        return

    def Verbose(self, msg, printHeader=False):
        '''
        Calls Print() only if verbose options is set to true
        '''
        if not opts.verbose:
            return
        Print(msg, printHeader)
        return

    def Print(self, msg, printHeader=True):
        '''
        Simple print function. If verbose option is enabled prints, otherwise does nothing.
        '''
        fName = __file__.split("/")[-1]
        fName = fName.replace(".pyc", ".py")
        if printHeader:
            print "=== ", fName
        print "\t", msg
        return

    def setId(self,id):
	self.id = id
        return

    def setLabel(self,label):
	self.label = label
        return

    def setDistribution(self,distr):
	self.distr = distr
        return

    def setFunction(self, function):
	self.function = function
        return

    def getArg(self, keyword):
        if keyword in self.kwargs.keys():
            return self.kwargs[keyword]
        return None
	
    def getId(self):
	return self.id
	
    def getDistribution(self):
	return self.distr
	
    def getFunction(self):
	return self.function

    def getLabel(self):
	return self.label
    
    def getKwarg(self, key):
        if key not in self.kwargs:
            #raise Exception("Unknown key %s no present in kewyword arguments" % (key))
            return "N/A"
        return self.kwargs[key]

    def PrintInfo(self):
        '''
        Print a summary of all variables
        (id, label, distr, funct.)
        that define this nuisance parameter
        '''
        table  = []
        align  = "{:<15} {:<35}"
        hLine  = "*"*50
        header = align.format("Variable", "Value")
        hLine  = "="*40
        table.append(hLine)        
        table.append(header)
        table.append(hLine)
        table.append(align.format("ID", self.getId()))
        table.append(align.format("Label", self.getLabel()))
        table.append(align.format("Distribution", self.getDistribution()))
        table.append(align.format("Function", self.getFunction()))
        # For-loop: All keywords arguments
        for key in self.kwargs:
            table.append(align.format(key, self.kwargs[key]))
        table.append(hLine)
        table.append("")

        # For-loop: All rows of the table
        for i, r in enumerate(table, 1):
            self.Print(r, i==1)
        return


class ControlPlotInput:
    def __init__(self,
                 title,
                 histoName,
                 details = {},
                 blindedRange = [],
                 evaluationRange = [],
                 flowPlotCaption = ""):
        self.title = title
        self.histoName = histoName
        self.details = details
        self.blindedRange = blindedRange
        self.evaluationRange = evaluationRange
        self.flowPlotCaption = flowPlotCaption
        return
