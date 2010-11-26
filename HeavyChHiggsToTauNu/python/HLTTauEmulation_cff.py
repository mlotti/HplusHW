import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak5CaloJets_cfi import *
ak2CaloJets = ak5CaloJets.clone()
ak2CaloJets.rParam = cms.double(0.2)

from RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi import *
ak2JetTracksAssociatorAtVertex = ic5JetTracksAssociatorAtVertex.clone()
ak2JetTracksAssociatorAtVertex.jets = cms.InputTag("ak2CaloJets")

#CaloTauTagInfo Producer
from RecoTauTag.RecoTau.CaloRecoTauTagInfoProducer_cfi import *
caloTauTagInfoForHLTTauEmuProducer = caloRecoTauTagInfoProducer.clone()
caloTauTagInfoForHLTTauEmuProducer.CaloJetTracksAssociatorProducer = cms.InputTag('ak2JetTracksAssociatorAtVertex')

#CaloTau Producer
from RecoTauTag.RecoTau.CaloRecoTauProducer_cfi import *
caloTauHLTTauEmu = caloRecoTauProducer.clone()

HLTTauEmu = cms.Sequence(ak2CaloJets *
			 ak2JetTracksAssociatorAtVertex *
                         caloRecoTauTagInfoProducer *
			 caloTauHLTTauEmu
)
