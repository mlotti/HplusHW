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
    
    histo.SetCanExtend(0)
    n = histo.GetNbinsX()
    moveBinContent(0,1,histo)
    moveBinContent(histo.GetNbinsX()+1,histo.GetNbinsX(),histo)
    if (n != histo.GetNbinsX()):
        raise Exception("Weird, the number of bins in the histogram just changed unexpectedly (%d vs %d)!"%(n, histo.GetNbinsX()))

if __name__ == "__main__":
    import unittest
    class TestFiles(unittest.TestCase):
        def testFlowBinsVisible(self):
            n = 10
            h = ROOT.TH1F("h","h",n,0,n)
            for i in range(n+2):
                h.Fill(i-1)
            self.assertEqual(h.GetNbinsX(), n)
            self.assertEqual(h.GetBinContent(0), 1)
            self.assertEqual(h.GetBinContent(1), 1)
            self.assertEqual(h.GetBinContent(n), 1)
            self.assertEqual(h.GetBinContent(n+1), 1)
            makeFlowBinsVisible(h)
            self.assertEqual(h.GetNbinsX(), n)
            self.assertEqual(h.GetBinContent(0), 0)
            self.assertEqual(h.GetBinContent(1), 2)
            self.assertEqual(h.GetBinContent(n), 2)
            self.assertEqual(h.GetBinContent(n+1), 0)

        def testFlowBinsVisible2(self):
            n = 10
            h = ROOT.TH1F("h","h",n,0,n)
            for i in range(n):
                h.Fill(i)
            self.assertEqual(h.GetNbinsX(), n)
            self.assertEqual(h.GetBinContent(0), 0)
            self.assertEqual(h.GetBinContent(1), 1)
            self.assertEqual(h.GetBinContent(n), 1)
            self.assertEqual(h.GetBinContent(n+1), 0)
            makeFlowBinsVisible(h)
            self.assertEqual(h.GetNbinsX(), n)
            self.assertEqual(h.GetBinContent(0), 0)
            self.assertEqual(h.GetBinContent(1), 1)
            self.assertEqual(h.GetBinContent(n), 1)
            self.assertEqual(h.GetBinContent(n+1), 0)

    unittest.main()
