import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools

_prototype = cms.untracked.PSet(
    data = cms.FileInPath("NOT_YET_SET"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11_PU_2011AB"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

eraRunMap = {
    "Run2011AB": ["runs_170722_180252"]
}

def getEfficiency():
    return _prototype.clone(
        data = HChTools.getEfficiencyJsonFullPath("met trigger scale factors", "metLegTriggerEfficiency2011", "loose")
    )

def getRunsForEra(era):
    try:
        return eraRunMap[era]
    except KeyError:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are %s" % (era, ", ".join(["'%s'"%e for e in eraRunMap.iterkeys()])))
