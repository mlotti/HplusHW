import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools

eraRunMap = {
    "Run2012A": ["runs_190456_202585"],
    "Run2012B": ["runs_190456_202585"],
    "Run2012C": ["runs_190456_202585"],
    "Run2012D": ["runs_202807_208686"],
    "Run2012AB": ["runs_190456_202585"],
    "Run2012ABC": ["runs_190456_202585"],
    "Run2012ABCD": ["runs_190456_208686"],
}

def setEfficiency(pset, isolation, againstMuon, againstElectron):
    pset.data = HChTools.getEfficiencyJsonFullPath("l1etm trigger scale factors", "metLegL1ETM40Efficiency2012", "2011Like")

def getRunsForEra(era):
    try:
        return eraRunMap[era]
    except KeyError:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are %s" % (era, ", ".join(["'%s'"%e for e in eraRunMap.iterkeys()])))
