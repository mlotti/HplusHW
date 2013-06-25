from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.UnfoldedHistogramReader import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount import *


import ROOT
ROOT.gROOT.SetBatch(True) # no flashing canvases

## Class for calculating purity for QCD measurements
class Purity:
    def __init__(self, dataCounts, ewkCounts):
        self._data = []
        self._ewk = []
        if isinstance(dataCounts, list):
            self._data = list(dataCounts)
            self._ewk = list(ewkCounts)
        else:
            self._data.append(dataCounts)
            self._ewk.append(ewkCounts)
# FIXME