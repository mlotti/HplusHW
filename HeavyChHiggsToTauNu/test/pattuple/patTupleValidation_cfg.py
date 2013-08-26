import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "38X"
dataVersion = "39Xredigi"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object


process = cms.Process("PatValidation")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        "file:pattuple.root"
  )
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
del process.TFileService

process.analyzer = cms.EDAnalyzer(
    "HPlusPatTupleValidationAnalyzer",
    electrons = cms.untracked.VPSet(
        cms.PSet(
            src = cms.untracked.InputTag("selectedPatElectrons"),
            electronIDs = cms.untracked.vstring("simpleEleId95relIso", "simpleEleId95cIso",
                                                "simpleEleId90relIso", "simpleEleId90cIso",
                                                "simpleEleId85relIso", "simpleEleId85cIso",
                                                "simpleEleId80relIso", "simpleEleId80cIso",
                                                "simpleEleId70relIso", "simpleEleId70cIso",
                                                "simpleEleId60relIso", "simpleEleId60cIso")
        )
    )
)

process.path = cms.Path(process.analyzer)
