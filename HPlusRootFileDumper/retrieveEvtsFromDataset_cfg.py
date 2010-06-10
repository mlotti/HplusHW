### This python config file runs on a dataset that is either stored locally or on any SE and extracts UNCHANGED a custom number of the available events. This is basically a mere copying of part or all of the dataset on my local file (or chosen destination)! Pretty cool!

import FWCore.ParameterSet.Config as cms

process = cms.Process("MyProcessName")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/0AA7C390-0F3C-DF11-BD65-000423D998BA.root'
  )
)

process.myOptions = cms.untracked.PSet(SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('test.root')
                               #fileName = cms.untracked.string('rfio:/castor/cern.ch/user/a/attikis/myOutputFile.root')
                               ### In case you want to drop everything and only keep a specific collection:
                               #outputCommands = cms.untracked.vstring('drop *', "keep *_generalTracks_*_*", "keep *_collectionYouWantToKeep_*_*")

 )

process.e = cms.EndPath(process.out)
