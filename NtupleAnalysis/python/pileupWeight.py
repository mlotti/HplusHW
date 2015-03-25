#! /usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet, File

import os

_pileupHistogramPath = "NtupleAnalysis/data/PUWeights"

def pileupWeight(data=None, mc=None, enabled=None):
    if data is not None and mc is not None and enabled is None:
        enabled = True
    if enabled is None:
        enabled = False

    pset = PSet(enabled=enabled)
    if not enabled:
        return pset
    if data is None:
        raise Exception("If pileupWeight is enabled, must give parameter 'data' for the data era")
    if mc is None:
        raise Exception("If pileupWeight is enabled, must give parameter 'mc' for the MC era")

    pset.data = File(os.path.join(_pileupHistogramPath, "PileupHistogramData"+data+".root"))
    pset.mc = File(os.path.join(_pileupHistogramPath, "PileupHistogramMC"+mc+".root"))
    return pset


if __name__ == "__main__":
    import unittest
    import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
    class TestPileupWeight(unittest.TestCase):
        def testDefault(self):
            puweight = pileupWeight()
            self.assertEqual(puweight.enabled, False)

        def testDataMcGiven(self):
            puweight = pileupWeight(data="2012D", mc="Summer12_S10")
            self.assertEqual(puweight.enabled, True)
            self.assertEqual(puweight.data, os.path.join(aux.higgsAnalysisPath(), _pileupHistogramPath, "PileupHistogramData2012D.root"))
            self.assertEqual(puweight.mc, os.path.join(aux.higgsAnalysisPath(), _pileupHistogramPath, "PileupHistogramMCSummer12_S10.root"))

        def testDisaled(self):
            puweight = pileupWeight(enabled=False)
            self.assertEqual(puweight.enabled, False)

        def testDataMcGivenDisabled(self):
            puweight = pileupWeight(data="2012D", mc="Summer12_S10", enabled=False)
            self.assertEqual(puweight.enabled, False)

    unittest.main()
