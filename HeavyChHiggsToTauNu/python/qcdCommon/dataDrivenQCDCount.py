from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.UnfoldedHistogramReader import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount import *

import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases

## Container class for information of data and MC EWK at certain point of selection
class DataDrivenQCDShape:
    def __init__(self):
        self._name = ""
        #self._labelDictionary = None
        self._data = []
        self._ewk = []
        self._splittedHistoReader = None

    def readFromDsetMgr(self, dsetMgr, dsetLabelData, dsetLabelEwk, histoName):
        self._splittedHistoReader = SplittedHistoReader(dsetRootHisto.getHistogram())
    
    
    
    
    ## \var _labelDictionary
    # Dictionary for interpreting label of histogram into a human readable text
        
        