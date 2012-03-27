#! /usr/bin/env python

from ROOT import *

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

class DataCardGenerator:
    def __init__(self, config):
	self.config = config
#        self.name = config.DataCardName
#        self.massPoints = config.MassPoints
        
    def generate(self,dirs):
	signalDir = []
	signalDir.append(dirs[0])
	datasets = dataset.getDatasetsFromMulticrabDirs(signalDir,counters=self.config.CounterDir)
	datasets.loadLuminosities()
	plots.mergeRenameReorderForDataMC(datasets)
#	xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)
#	plots.mergeWHandHH(datasets)
	luminosity = datasets.getDataset("Data").getLuminosity()
        print "Luminosity = ",luminosity
