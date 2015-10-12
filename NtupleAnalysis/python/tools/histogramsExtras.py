## \package histogramsExtras
# Portable histogram utilities, separate from histograms to avoid circular dependencies

import math
import ROOT

## Adds the underflow and overflow bins to the first and last bins, respectively
def makeFlowBinsVisible(histo):
    def moveBinContent(sourceBin,targetBin,histo):
        histo.SetBinContent(targetBin, histo.GetBinContent(targetBin)+histo.GetBinContent(sourceBin))
        histo.SetBinError(targetBin, math.sqrt(histo.GetBinError(targetBin)**2+histo.GetBinError(sourceBin)**2))
        histo.SetBinContent(sourceBin,0.0)
        histo.SetBinError(sourceBin,0.0)
    moveBinContent(0,1,histo)
    moveBinContent(histo.GetNbinsX()+1,histo.GetNbinsX(),histo)

