import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMtoMEConvert")
process.load("DQMServices.Examples.test.MessageLogger_cfi")

process.load("Configuration.StandardSequences.EDMtoMEAtJobEnd_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	"file:output.root"
    )
)

#import os, glob
#directory = "TTJets_TuneZ2_Spring11/res"
#directory = "QCD_Pt80to120_TuneZ2_Spring11/res"
#directory = "TauPlusX_160404-161312_Prompt/res"
#directory = "Tau_160404-161176_Prompt/res"
#directory = "Tau_161216-161312_Prompt/res"
#process.source.fileNames = ["file:%s"%x for x in glob.glob(os.path.join(directory, "*.root"))]

process.p1 = cms.Path(process.EDMtoMEConverter*process.dqmSaver)

