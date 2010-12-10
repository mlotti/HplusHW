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
caloTauTagInfoForHLTTauEmuProducer.PVProducer = cms.InputTag('pixelVertices')
caloTauTagInfoForHLTTauEmuProducer.tkminPt = cms.double(1.0)
caloTauTagInfoForHLTTauEmuProducer.tkminPixelHitsn = cms.int32(2)
caloTauTagInfoForHLTTauEmuProducer.tkminTrackerHitsn = cms.int32(5)
caloTauTagInfoForHLTTauEmuProducer.tkmaxipt = cms.double(0.3) # FIXME, check units 


#CaloTau Producer
from RecoTauTag.RecoTau.CaloRecoTauProducer_cfi import caloRecoTauProducer as caloRecoTauProducerPrototype
caloTauHLTTauEmu = caloRecoTauProducerPrototype.clone()
caloTauHLTTauEmu.PVProducer = cms.InputTag('pixelVertices')
caloTauHLTTauEmu.MatchingConeSizeFormula = cms.string('0.20')
caloTauHLTTauEmu.TrackerSignalConeSizeFormula = cms.string('0.15')
caloTauHLTTauEmu.TrackerIsolConeSize_max = cms.double(0.5)
caloTauHLTTauEmu.TrackLeadTrack_maxDZ = cms.double(2.0) # FIXME, check units
caloTauHLTTauEmu.Track_minPt = cms.double(1.0)

#CaloTau isolation discriminator
#from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByLeadingTrackFinding_cfi import *
#from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByLeadingTrackPtCut_cfi import *
#from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByTrackIsolation_cfi import *
#from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByECALIsolation_cfi import *
#from RecoTauTag.RecoTau.CaloRecoTauDiscriminationByIsolation_cfi import *
#caloTauHLTTauEmuDiscriminationByLeadingTrackFinding = caloRecoTauDiscriminationByLeadingTrackFinding.clone()
#caloTauHLTTauEmuDiscriminationByTrackIsolation = caloRecoTauDiscriminationByTrackIsolation.clone()
#caloTauHLTTauEmuDiscriminationByECALIsolation = caloRecoTauDiscriminationByECALIsolation.clone()
#caloTauHLTTauEmuDiscriminationByECALIsolation.ECALisolAnnulus_maximumSumEtCut = cms.double(5.0)

HLTTauEmu = cms.Sequence(ak2CaloJets *
			 ak2JetTracksAssociatorAtVertex *
                         caloTauTagInfoForHLTTauEmuProducer *
			 caloTauHLTTauEmu
#			 caloTauHLTTauEmuDiscriminationByLeadingTrackFinding *
#		         caloTauHLTTauEmuDiscriminationByTrackIsolation *
#			 caloTauHLTTauEmuDiscriminationByECALIsolation
)
