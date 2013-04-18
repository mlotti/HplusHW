import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.UnfoldedHistogramReader as unfoldedHistogramReader
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

if __name__ == "__main__":
    print HighlightStyle()+"Validating code of datacard generator ...\n"+NormalStyle()
    # Code validation for unfolded histogram reader
    unfoldedHistogramReader.validate()