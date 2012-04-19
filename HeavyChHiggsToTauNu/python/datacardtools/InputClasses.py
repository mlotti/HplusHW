#! /usr/bin/env python

import sys
import os

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import sort

# data structures for the config file information

class ObservationInput:
    def __init__(self, dirPrefix, rateCounter, datasetDefinitions, shapeHisto):
	self.setDirPrefix(dirPrefix)
	self.setRateCounter(rateCounter)
	self.setDatasetDefinitions(datasetDefinitions)
	self.setShapeHisto(shapeHisto)

    def setDirPrefix(self,dir):
	self.dirPrefix = dir

    def setRateCounter(self,rateCounter):
	self.rateCounter = rateCounter

    def setDatasetDefinitions(self,datasetDefinitions):
        self.datasetDefinitions = datasetDefinitions

    def setShapeHisto(self,histo):
	self.shapeHisto = histo

    def getDirPrefix(self):
        return self.dirPrefix

    def getRateCounter(self):
        return self.rateCounter

    def getShapeHisto(self):
        return self.shapeHisto

    def Print(self):
	print "ObservationInput :"
	print "    dirPrefix   ",self.dirPrefix
	print "    rate counter",self.rateCounter
	print "    shapeHisto  ",self.shapeHisto

class DataGroup:
    def __init__(self, 
                 landsProcess = -999,
                 validMassPoints = [], 
                 label = "", 
                 nuisances = [], 
                 shapeHisto = "", 
                 dirPrefix = "",
                 rateCounter = "",
                 datasetType = "",
                 datasetDefinitions = [],
                 MCEWKDatasetDefinitions = [],
                 additionalNormalisation = 1.0):
	self.landsProcess  = landsProcess
	self.validMassPoints = validMassPoints
	self.label         = label
	self.nuisances     = nuisances
	self.shapeHisto    = shapeHisto
	self.dirPrefix    = dirPrefix
	self.rateCounter   = rateCounter
        self.datasetType   = datasetType
        self.datasetDefinitions = datasetDefinitions
        self.MCEWKDatasetDefinitions = MCEWKDatasetDefinitions
        self.additionalNormalisation = additionalNormalisation

    def getId(self):
	return self.label

    def clone(self):
	return DataGroup(landsProcess = self.landsProcess,
                         validMassPoints = self.validMassPoints,
                         label        = self.label,
                         nuisances    = self.nuisances,
                         shapeHisto   = self.shapeHisto,
                         dirPrefix   = self.dirPrefix,
                         rateCounter  = self.rateCounter,
                         datasetType  = self.datasetType,
                         datasetDefinitions = self.datasetDefinitions,
                         MCEWKDatasetDefinitions = self.MCEWKDatasetDefinitions,
                         additionalNormalisation= self.additionalNormalisation)

    def setLandSProcess(self,landsProcess):
	self.landsProcess = landsProcess

    def setValidMassPoints(self,validMassPoints):
	self.validMassPoints = validMassPoints

    def setLabel(self, label):
	self.label = label

    def setNuisances(self,nuisances):
	self.nuisances = nuisances

    def setShapeHisto(self,histo):
	self.shapeHisto = histo

    def setCounterHisto(self,dirPrefix):
	self.dirPrefix = dirPrefix

    def setRateCounter(self, rateCounter):
        self.rateCounter = rateCounter

    def setDatasetType(self,datasetType):
        self.datasetType = datasetType

    def setDatasetDefinitions(self,datasetDefinitions):
        self.datasetDefinitions = datasetDefinitions

    def setMCEWKDatasetDefinitions(self,MCEWKDatasetDefinitions):
        self.MCEWKDatasetDefinitions = MCEWKDatasetDefinitions

    def setAdditionalNormalisation(self,value):
	self.additionaNormalisation = value

    def Print(self):
	print "    Label        ",self.label
	print "    LandS process",self.landsProcess
	print "    Valid mass points",self.validMassPoints
	print "    dir. prefix      ",self.dirPrefix
	print "    datasetType  ",self.datasetType
	print "    datasetDefinitions",self.datasetDefinitions
	print "    MCEWKDatasetDefinitions",self.MCEWKDatasetDefinitions
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


class Nuisance:
    def __init__(self,
		id="",
		label="",
		distr="",
		function = "",
		QCDmode = "",
		value = -1,
		upperValue = -1,
		counter = "",
		numerator = -1, 
		denominator = -1, 
		histoDir = [],
		histograms = [],
		normalisation = [],
		scaling = 1.0):
	self.setId(id)
	self.setLabel(label)
	self.setDistribution(distr)
	self.setFunction(function)
	self.setQCDmode(QCDmode)
	self.setValue(value)
	self.setUpperValue(upperValue)
	self.setCounter(counter)
	self.setNumerator(numerator)
	self.setDenominator(denominator)
        self.setHistoDir(histoDir)
	self.setHistograms(histograms)
        self.setNormalisation(normalisation)
        self.setScaling(scaling)

    def setId(self,id):
	self.id = id

    def setLabel(self,label):
	self.label = label

    def setDistribution(self,distr):
	self.distr = distr

    def setFunction(self, function):
	self.function = function

    def setQCDmode(self, QCDmode):
        self.QCDmode = QCDmode

    def setValue(self,value):
	self.value = value

    def setUpperValue(self,upperValue):
        self.upperValue = upperValue

    def setCounterHisto(self, value):
	self.dirPrefix = value

    def setCounter(self, value):
	self.counter = value

    def setNumerator(self,value):
	self.numerator = value

    def setDenominator(self,value):
	self.denominator = value

    def setHistoDir(self, histoDir):
	self.histoDir = histoDir

    def setHistograms(self, histo):
	self.histo = histo

    def setNormalisation(self, norm):
	self.norm = norm

    def setScaling(self, scaling):
        self.scaling = scaling

    def getId(self):
	return self.id

    def Print(self):
	print "    ID            =",self.id
	print "    Label         =",self.label
        print "    Distribution  =",self.distr
        print "    Function      =",self.function
        if self.value > 0:
            print "    Value         =",self.value
        if len(self.dirPrefix) > 0:
            print "    CounterHisto  =",self.dirPrefix
        if len(self.counter) > 0:
            print "    Counter       =",self.counter
        if len(self.paths) > 0:
            print "    Paths         =",self.paths
        if len(self.histo) > 0:
            print "    Histograms    =",self.histo
        if len(self.norm) > 0:
            print "    Normalisation =",self.norm
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
