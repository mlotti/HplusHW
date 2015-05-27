import os

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

_aliases = {
    "Test": "Test_v1",
    "TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6": "TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6_v1",
}

def getFiles(datasetName):
    basedir = os.path.join(aux.higgsAnalysisPath(), "NtupleAnalysis")

    name = _aliases.get(datasetName, datasetName)

    path = os.path.join(basedir, "data", name+".txt")
    if not os.path.exists(path):
        raise Exception("No files for dataset %s (i.e. file %s not found)" % (name, path))

    def strip(line):
        ret = line.rstrip()
        if "#" in ret:
            ret = ret[0:ret.index("#")]
        return ret

    with open(path) as f:
        return filter(lambda l: len(l) > 0, map(strip, f.readlines()))

if __name__ == "__main__":
    import unittest
    class TestFiles(unittest.TestCase):
        def testGetFiles(self):
            files = getFiles("Test_v1")
            self.assertEqual(len(files), 2)
            self.assertEqual(files[0], "testfile1.root")
            self.assertEqual(files[1], "testfile2.root")
        def testAlias(self):
            files1 = getFiles("Test")
            files2 = getFiles("Test_v1")
            self.assertEqual(files1, files2)

    unittest.main()
