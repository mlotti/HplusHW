### This python config file runs on a dataset that is either stored locally or on any SE and extracts UNCHANGED a custom number of the available events. This is basically a mere copying of part or all of the dataset on my local file (or chosen destination)! Pretty cool!

import FWCore.ParameterSet.Config as cms

process = cms.Process("MyProcessName")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
#        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/0AA7C390-0F3C-DF11-BD65-000423D998BA.root'
        '/store/data/Run2010A/JetMETTauMonitor/RECO/v2/000/137/436/48526FDE-8F74-DF11-B2DC-000423D98E6C.root' #JPTJet collection present
  )
)

process.myOptions = cms.untracked.PSet(SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('JPTtest.root')
                               #fileName = cms.untracked.string('rfio:/castor/cern.ch/user/a/attikis/myOutputFile.root')
                               ### In case you want to drop everything and only keep a specific collection:
                               #outputCommands = cms.untracked.vstring('drop *', "keep *_generalTracks_*_*", "keep *_collectionYouWantToKeep_*_*")

 )

process.e = cms.EndPath(process.out)
