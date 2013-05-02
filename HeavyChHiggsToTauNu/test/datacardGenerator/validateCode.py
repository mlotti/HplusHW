#! /usr/bin/env python

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.UnfoldedHistogramReader as unfoldedHistogramReader
import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.QCDfactorised as QCDfactorised

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

if __name__ == "__main__":
    ROOT.gROOT.SetBatch() # no flashing canvases
    print HighlightStyle()+"Validating code of datacard generator ...\n"+NormalStyle()
    # Code validation for unfolded histogram reader
    unfoldedHistogramReader.validate()
    QCDfactorised.validateQCDCountObject()