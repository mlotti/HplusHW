import FWCore.ParameterSet.Config as cms

process = cms.Process("NTUPLEMERGE")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#process.options = cms.untracked.PSet(
#      fileMode = cms.untracked.string('FULLMERGE')
#)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source('PoolSource',
#  noEventSort = cms.untracked.bool(True),
  fileNames = cms.untracked.vstring(
    "/store/group/local/HiggsChToTauNuFullyHadronic/ntuples/CMSSW_3_6_X/QCD_Pt30_Summer10_START336_V9_S09_v1_AODSIM_v4/HPlusOut_100_1.root",
    "/store/group/local/HiggsChToTauNuFullyHadronic/ntuples/CMSSW_3_6_X/QCD_Pt30_Summer10_START336_V9_S09_v1_AODSIM_v4/HPlusOut_101_1.root"
  )
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('HPlusOut.root')
)

process.outpath = cms.EndPath(process.out)

