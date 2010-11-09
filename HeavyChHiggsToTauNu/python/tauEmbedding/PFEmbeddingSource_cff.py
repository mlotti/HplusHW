import FWCore.ParameterSet.Config as cms

  
from Configuration.Generator.PythiaUESettings_cfi import *

TauolaNoPolar = cms.PSet(
    UseTauolaPolarization = cms.bool(False)
)
TauolaPolar = cms.PSet(
   UseTauolaPolarization = cms.bool(True)
)


from TauAnalysis.MCEmbeddingTools.MCParticleReplacer_cfi import *
newSource.algorithm = "ZTauTau"
newSource.ZTauTau.TauolaOptions.InputCards.mdtau = cms.int32(0)
newSource.ZTauTau.minVisibleTransverseMomentum = cms.untracked.double(0)
newSource.ZTauTau.transformationMode = cms.untracked.int32(3)

#source = cms.Source("PoolSource",
#        skipEvents = cms.untracked.uint32(0),
#        fileNames = cms.untracked.vstring('/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/E250F96A-CF7B-DF11-99E5-001BFCDBD1BE.root')
#)

muonSelectionPlaceholder = cms.Sequence()

adaptedMuonsFromWmunu = cms.EDProducer("HPlusMuonMetAdapter",
   muonSrc = cms.untracked.InputTag("selectedPatMuons"),
   metSrc = cms.untracked.InputTag("patMETsPF")
)


dimuonsGlobal = cms.EDProducer('ZmumuPFEmbedder',
    tracks = cms.InputTag("generalTracks"),
    selectedMuons = cms.InputTag("adaptedMuonsFromWmunu"),
    keepMuonTrack = cms.bool(False)
)

generator = newSource.clone()
generator.src = cms.InputTag("adaptedMuonsFromWmunu")

filterEmptyEv = cms.EDFilter("EmptyEventsFilter",
    minEvents = cms.untracked.int32(1),
    target =  cms.untracked.int32(1) 
)

ProductionFilterSequence = cms.Sequence(muonSelectionPlaceholder*adaptedMuonsFromWmunu*dimuonsGlobal*generator*filterEmptyEv)
