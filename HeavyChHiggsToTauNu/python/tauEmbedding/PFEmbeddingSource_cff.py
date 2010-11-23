import FWCore.ParameterSet.Config as cms

  
from Configuration.Generator.PythiaUESettings_cfi import *

TauolaNoPolar = cms.PSet(
    UseTauolaPolarization = cms.bool(False)
)
TauolaPolar = cms.PSet(
   UseTauolaPolarization = cms.bool(True)
)

#source = cms.Source("PoolSource",
#        skipEvents = cms.untracked.uint32(0),
#        fileNames = cms.untracked.vstring('/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/E250F96A-CF7B-DF11-99E5-001BFCDBD1BE.root')
#)

adaptedMuonsFromWmunu = cms.EDProducer("HPlusMuonMetAdapter",
   muonSrc = cms.untracked.InputTag("tauEmbeddingMuons"),
   metSrc = cms.untracked.InputTag("pfMet")
)


dimuonsGlobal = cms.EDProducer('ZmumuPFEmbedder',
    tracks = cms.InputTag("generalTracks"),
    selectedMuons = cms.InputTag("tauEmbeddingMuons"),
    keepMuonTrack = cms.bool(False)
)

filterEmptyEv = cms.EDFilter("EmptyEventsFilter",
    minEvents = cms.untracked.int32(1),
    target =  cms.untracked.int32(1) 
)

# Avoid compilation error when TauAnalysis/MCEmbeddingTools is missing
try:
    from TauAnalysis.MCEmbeddingTools.MCParticleReplacer_cfi import *
    newSource.algorithm = "ZTauTau"

    # See https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideTauolaInterface for mdtau parameter
    #newSource.ZTauTau.TauolaOptions.InputCards.mdtau = cms.int32(0) # for all decay modes
    newSource.ZTauTau.TauolaOptions.InputCards.mdtau = cms.int32(230) # for hadronic modes
    newSource.ZTauTau.minVisibleTransverseMomentum = cms.untracked.double(0)
    newSource.ZTauTau.transformationMode = cms.untracked.int32(3)

    generator = newSource.clone()
    generator.src = cms.InputTag("adaptedMuonsFromWmunu")

    ProductionFilterSequence = cms.Sequence(adaptedMuonsFromWmunu*dimuonsGlobal*generator*filterEmptyEv)
except ImportError:
    print
    print "  TauAnalysis/MCEmbeddingTools package is missing"
    print
    pass

