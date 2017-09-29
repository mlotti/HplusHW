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

    def getShapeHisto(self):
        return self.shapeHistoName

    def Print(self):
	print "ObservationInput :"
	print "    shapeHisto  ",self.shapeHisto

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

    def setValidMassPoints(self,validMassPoints):
	self.validMassPoints = list(validMassPoints)

    def setLabel(self, label):
	self.label = label

    def setNuisances(self,nuisances):
	self.nuisances = nuisances[:]

    def setShapeHisto(self,path,histo):
	self.histoPath = path
	self.shapeHisto = histo

    def setDatasetType(self,datasetType):
        self.datasetType = datasetType

    def setDatasetDefinition(self,datasetDefinition):
        self.datasetDefinition = datasetDefinition

    def setQCDfactorisedInfo(self,QCDfactorisedInfo):
        self.QCDfactorisedInfo = QCDfactorisedInfo

    def setAdditionalNormalisation(self,value):
	self.additionaNormalisation = value

    def Print(self):
	print "    Label        ",self.label
	print "    LandS process",self.landsProcess
	print "    Valid mass points",self.validMassPoints
	print "    datasetType  ",self.datasetType
	print "    datasetDefinition",self.datasetDefinition
	print "    Additional normalisation",self.additionalNormalisation
	print "    Nuisances    ",self.nuisances
        print

#class DataGroupInput:
#    def __init__(self):
#	self.datagroups = {}
#
#    def add(self,datagroup):
#	if datagroup.exists():
#	    self.datagroups[datagroup.getId()] = datagroup
#
#    def get(self,key):
#	return self.datagroups[key]
#
#    def Print(self):
#	print "DataGroups"
#        print "NuisanceTable"
#        for key in sorted(self.datagroups.keys()):
#            self.datagroups[key].Print()
#        print

## Converts a single or a bunch of nuisances by ID from syst. variation to norm. uncertainty
def convertFromSystVariationToConstant(nuisanceList, name):
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
    #print ""

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
    

class Nuisance:
    def __init__(self,
		id="",
		label="",
		distr="",
		function = "",
		**kwargs):
	self.setId(id)
	self.setLabel(label)
	self.setDistribution(distr)
	self.setFunction(function)
	self.kwargs = kwargs

    def setId(self,id):
	self.id = id

    def setLabel(self,label):
	self.label = label

    def setDistribution(self,distr):
	self.distr = distr

    def setFunction(self, function):
	self.function = function

    def getArg(self, keyword):
        if keyword in self.kwargs.keys():
            return self.kwargs[keyword]
        return None
	
    def getId(self):
	return self.id

    def Print(self):
	print "    ID            =",self.id
	print "    Label         =",self.label
        print "    Distribution  =",self.distr
        print "    Function      =",self.function
        #if self.value > 0:
            #print "    Value         =",self.value
        #if len(self.counter) > 0:
            #print "    Counter       =",self.counter
        #if len(self.paths) > 0:
            #print "    Paths         =",self.paths
        #if len(self.histo) > 0:
            #print "    Histograms    =",self.histo
        #if len(self.norm) > 0:
            #print "    Normalisation =",self.norm
	print

#class NuisanceTable:
    #def __init__(self):
	#self.nuisances = {}

    #def add(self,n):
	#if not self.exists(n):
	    #self.nuisances[n.getId()] = n
	#else:
	    #print "\nWarning, key",n.getId(),"already reserved to Nuisance"
	    #self.nuisances[n.getId()].Print()
	    #print "Exiting.."
	    #sys.exit()

    #def get(self,key):
        #return self.nuisances[key]

    #def merge(self,n1,n2):
	#print "merging nuisances is not yet implemented"

    #def reserve(self, ids, comment):
	#for id in ids:
	    #self.add(Nuisance(id=id,label=comment,distr= "lnN",function="Constant",value=0,reserved=True))

    #def exists(self, n):
	#if n.getId() in self.nuisances:
	    #return True
	#return False

    #def Print(self):
	#print "NuisanceTable"
	#for key in sort(self.nuisances.keys()):
	    #self.nuisances[key].Print()
	#print

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
