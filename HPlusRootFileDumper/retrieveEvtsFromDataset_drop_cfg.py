### This python config file runs on a dataset that is either stored locally or on any SE and extracts UNCHANGED a custom number of the available events. This is basically a mere copying of part or all of the dataset on my local file (or chosen destination)! Pretty cool!

import FWCore.ParameterSet.Config as cms

process = cms.Process("MyProcessName")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
                            # fileNames = cms.untracked.vstring("file:/afs/cern.ch/user/a/attikis/scratch0/CMSSW_3_5_2/src/analysis/myAnalyzer/patLayer1_fromAOD_PF2PAT_full.root")
                            fileNames = cms.untracked.vstring(
    #    'file:test.root'
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/F4C92A98-163C-DF11-9788-0030487C7392.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/F427D642-173C-DF11-A909-0030487C60AE.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/E27821C3-0C3C-DF11-9BD9-0030487CD718.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/D87D5469-2E3C-DF11-A470-000423D99896.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/B647CAD9-0E3C-DF11-886F-0030487CD716.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/A860D55E-193C-DF11-BE29-0030487C60AE.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/9884BC11-0C3C-DF11-8F9C-000423D986C4.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/92684831-233C-DF11-ABA0-0030487CD16E.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/90269E76-0D3C-DF11-A1A0-0030487CD840.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/8CAE3014-133C-DF11-A05D-000423D174FE.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/8C51BAC6-1A3C-DF11-A0EE-000423D94A04.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/8C042B04-2D3C-DF11-939F-0030487CD178.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/80471A6B-0E3C-DF11-8DCD-0030487C6A66.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/762824C3-0C3C-DF11-A4FD-0030487CD6D2.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/6A3533F5-103C-DF11-B3AA-00304879BAB2.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/4C8979D2-073C-DF11-B97B-000423D6AF24.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/26C8DED9-0E3C-DF11-9D83-0030487CD7B4.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/181C44F7-093C-DF11-A9CB-001D09F24FEC.root',
    '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/0AA7C390-0F3C-DF11-BD65-000423D998BA.root'
    
    )
                            #fileNames = cms.untracked.vstring("rfio:/castor/cern.ch/cms/store/relval/CMSSW_3_5_2/RelValTTbar/GEN-SIM-DIGI-RECO/MC_3XY_V21_FastSim-v1/0015/FE520833-1A1E-DF11-A76D-002618FDA279.root")
                            #)


process.myOptions = cms.untracked.PSet(SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('test3.root'),
                               #fileName = cms.untracked.string('rfio:/castor/cern.ch/user/a/attikis/myOutputFile.root')
                               ### In case you want to drop everything and only keep a specific collection:
                               #outputCommands = cms.untracked.vstring('drop *', "keep *_generalTracks_*_*", "keep *_collectionYouWantToKeep_*_*")
                               outputCommands = cms.untracked.vstring('drop *', "keep *_shrinkingConePFTauProducer_*_*", "keep *_shrinkingConePFTauDiscriminationAgainstElectron_*_*")
 )

process.e = cms.EndPath(process.out)
