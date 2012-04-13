#! /usr/bin/env python

from ROOT import *

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder as PathFinder

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import sort

class DataCardGenerator:
    def __init__(self, config):
	config.DataGroups.Print()
	config.Nuisances.Print()

	self.reportUnusedNuisances(config)

	self.config = config

    def reportUnusedNuisances(self,config):
	usedNuisances = []
        for nuisance in config.Nuisances.nuisances.keys():
	    for datagroup in config.DataGroups.datagroups.keys():
		for usedNuisance in config.DataGroups.get(datagroup).nuisances:
		    if usedNuisance == nuisance:
			usedNuisances.append(nuisance)
	usedNuisances = self.rmDuplicates(usedNuisances)
	unUsedNuisances = []
	for nuisance in config.Nuisances.nuisances.keys():
	    if nuisance not in usedNuisances:
		#print "UNUSED NUISANCE"
		#config.Nuisances.get(nuisance).Print
		unUsedNuisances.append(nuisance)
	print "Unused nuisances",sort(unUsedNuisances)

    def rmDuplicates(self,list):
	retlist = []
	for element in list:
	    if element not in retlist:
		retlist.append(element)
	return retlist

    def generate(self):
	signalDir = []
	signalDir.append(self.config.multicrabPaths.getSignalPath())
	datasets = dataset.getDatasetsFromMulticrabDirs(signalDir,counters=self.config.CounterDir)
	datasets.loadLuminosities()
	plots.mergeRenameReorderForDataMC(datasets)
	luminosity = datasets.getDataset("Data").getLuminosity()
        print "Luminosity = ",luminosity

