#! /usr/bin/env python

import sys
import os

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import sort

# data structures for the config file information

class ObservationInput:
    def __init__(self, counterDir, counter, shapeHisto):
	self.setChannel(1)
	self.setCounterDir(counterDir)
	self.setCounter(counter)
	self.setShapeHisto(shapeHisto)
	self.setFunction("Counter")
	self.setCounterHisto(os.path.join(counterDir,"counter"))

    def setChannel(self,channel):
	self.channel = channel

    def setCounterDir(self,dir):
	self.counterDir = dir

    def setCounter(self,counter):
	self.counter    = counter

    def setShapeHisto(self,histo):
	self.shapeHisto = histo

    def setFunction(self,function):
	self.function = function

    def setCounterHisto(self,histo):
	self.counterHisto = histo

    def setPaths(self, path, subpaths):
	self.path     = path
	self.subpaths = subpaths

	self.Print()

    def getChannel(self):
        return self.channel
        
    def getCounterDir(self):
        return self.counterDir
        
    def getCounter(self):
        return self.counter
        
    def getShapeHisto(self):
        return self.shapeHisto
        
    def getFunction(self):
        return self.function
        
    def getCounterHisto(self):
        return self.counterHisto

    def getPath(self):
        return self.path

    def getSubPaths(self):
        return self.subpaths

    def Print(self):
	print "ObservationInput :"
	print "    channel     ",self.channel
	print "    counterdir  ",self.counterDir
	print "    counter     ",self.counter
	print "    shapeHisto  ",self.shapeHisto
	print "    function    ",self.function
	print "    counterHisto",self.counterHisto
	print "    path        ",self.path
	print "    data        ",self.subpaths

class DataGroup:
    def __init__(self, 
                 name = "",
                 channel = 1, 
                 landsProcess = -999,
		 function = "", 
                 mass = -1, 
                 label = "", 
                 nuisances = [], 
                 shapeHisto = "", 
                 rootpath="", 
                 counter = "",
                 path = "", 
                 subpath = "", 
		 ewkmcpaths = "",
                 normalization = 1):
        self.name          = name
	self.channel       = channel
	self.landsProcess  = landsProcess
        self.function      = function
	self.mass          = mass
	self.label	   = label
	self.nuisances     = nuisances
	self.shapeHisto    = shapeHisto
        self.rootpath      = rootpath
	self.counter       = counter
	self.path	   = path
	self.subpath	   = subpath
	self.ewkmcpaths    = ewkmcpaths
	self.normalization = normalization

    def getId(self):
	return self.label

    def clone(self):
	return DataGroup(name         = self.name,
                         channel      = self.channel,
                         landsProcess = self.landsProcess,
			 function     = self.function,
                         mass         = self.mass,
                         label        = self.label,
                         nuisances    = self.nuisances,
                         shapeHisto   = self.shapeHisto,
                         rootpath     = self.rootpath,
			 counter      = self.counter,
                         path         = self.path,
                         ewkmcpaths   = self.ewkmcpaths,
                         subpath      = self.subpath,
                         normalization= self.normalization)

    def setName(self,name):
	self.name = name

    def setChannel(self,channel):
	self.channel = channel

    def setLandSProcess(self,landsProcess):
	self.landsProcess = landsProcess

    def setMass(self,mass):
	self.mass = mass

    def setFunction(self,function):
	self.function = function

    def setLabel(self, label):
	self.label = label

    def setNuisances(self,nuisances):
	self.nuisances = nuisances

    def setShapeHisto(self,histo):
	self.shapeHisto = histo

    def setRootpath(self,path):
        self.rootpath = rootpath
        
    def setCounter(self,counter):
	self.counter = counter

    def setPath(self,path):
	self.path = path

    def setSubPaths(self,path):
	self.subpath = path

    def setEWKMCPaths(self,paths):
	self.ewkmcpaths = paths

    def setNormalization(self,value):
	self.normalization = value

    def exists(self):
	if len(self.path) > 0:
	    return True
	return False

    def Print(self):
        print "    Name         ",self.name
	print "    Channel      ",self.channel
	print "    Label        ",self.label
	print "    LandS process",self.landsProcess
	print "    Mass         ",self.mass
        print "    Rootpath     ",self.rootpath
	print "    Counter      ",self.counter
	print "    Path         ",self.path
	print "    Subpaths     ",self.subpath
	print "    Normalization",self.normalization
	print "    Nuisances    ",self.nuisances
	print

class DataGroupInput:
    def __init__(self):
	self.datagroups = {}

    def add(self,datagroup):
	if datagroup.exists():
	    self.datagroups[datagroup.getId()] = datagroup

    def get(self,key):
	return self.datagroups[key]

    def Print(self):
	print "DataGroups"
        print "NuisanceTable"
        for key in sorted(self.datagroups.keys()):
            self.datagroups[key].Print()
        print


class Nuisance:
    def __init__(self,
		id="",
		label="",
		distr="",
		function = "",
		value = -1,
		counterHisto = "",
		counter = "",
		numerator = -1, 
		denominator = -1, 
		paths = [],
		histograms = [],
		normalization = [], 
		extranorm = 1, 
		reserved = False):
	self.setId(id)
	self.setLabel(label)
	self.setDistribution(distr)
	self.setFunction(function)
	self.setValue(value)
        self.setCounterHisto(counterHisto)
	self.setCounter(counter)
	self.setNumerator(numerator)
	self.setDenominator(denominator)
        self.setPaths(paths)
	self.setHistograms(histograms)
        self.setNormalization(normalization)
	self.setExtraNormalization(extranorm)
	self.setReserved(reserved)

    def setId(self,id):
	self.id = id

    def setLabel(self,label):
	self.label = label

    def setDistribution(self,distr):
	self.distr = distr

    def setFunction(self, function):
	self.function = function

    def setValue(self,value):
	self.value = value

    def setCounterHisto(self, value):
	self.counterHisto = value

    def setCounter(self, value):
	self.counter = value

    def setNumerator(self,value):
	self.numerator = value

    def setDenominator(self,value):
	self.denominator = value

    def setPaths(self, paths):
	self.paths = paths

    def setHistograms(self, histo):
	self.histo = histo

    def setNormalization(self, norm):
	self.norm = norm

    def setExtraNormalization(self, norm):
	self.extranorm = norm

    def setReserved(self,value):
	self.reserved = value

    def getId(self):
	return self.id

    def Print(self):
	print "    ID            =",self.id
	print "    Label         =",self.label
	if not self.reserved:
  	    print "    Distribution  =",self.distr
	    print "    Function      =",self.function
	    if self.value > 0:
	        print "    Value         =",self.value
	    if len(self.counterHisto) > 0:
		print "    CounterHisto  =",self.counterHisto
	    if len(self.counter) > 0:
                print "    Counter       =",self.counter
	    if len(self.paths) > 0:
		print "    Paths         =",self.paths
	    if len(self.histo) > 0:
	        print "    Histograms    =",self.histo
	    if len(self.norm) > 0:
	        print "    Normalization =",self.norm
	print

class NuisanceTable:
    def __init__(self):
	self.nuisances = {}

    def add(self,n):
	if not self.exists(n):
	    self.nuisances[n.getId()] = n
	else:
	    print "\nWarning, key",n.getId(),"already reserved to Nuisance"
	    self.nuisances[n.getId()].Print()
	    print "Exiting.."
	    sys.exit()

    def get(self,key):
        return self.nuisances[key]

    def merge(self,n1,n2):
	print

    def reserve(self, ids, comment):
	for id in ids:
	    self.add(Nuisance(id=id,label=comment,distr= "lnN",function="Constant",value=0,reserved=True))

    def exists(self, n):
	if n.getId() in self.nuisances:
	    return True
	return False

    def Print(self):
	print "NuisanceTable"
	for key in sort(self.nuisances.keys()):
	    self.nuisances[key].Print()
	print
