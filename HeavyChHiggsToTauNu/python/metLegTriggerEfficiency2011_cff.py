import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools

eraRunMap = {
    "Run2011AB": ["runs_160431_180252"]
}

def setEfficiency(pset):
    pset.data = HChTools.getEfficiencyJsonFullPath("met trigger scale factors", "metLegTriggerEfficiency2011", "loose")

def getRunsForEra(era):
    try:
        return eraRunMap[era]
    except KeyError:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are %s" % (era, ", ".join(["'%s'"%e for e in eraRunMap.iterkeys()])))
