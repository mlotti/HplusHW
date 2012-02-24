import FWCore.ParameterSet.Config as cms
import copy

from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import *
hplusTrackQualityCuts = PFTauQualityCuts.clone()
hplusTrackQualityCuts.maxTrackChi2 = cms.double(10.)
hplusTrackQualityCuts.minTrackHits = cms.uint32(8)

from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackFinding_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByLeadingTrackPtCut_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByCharge_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByECALIsolation_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstElectron_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationAgainstMuon_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByTauPolarization_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByDeltaE_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByInvMass_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByFlightPathSignificance_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByNProngs_cfi import *
from RecoTauTag.RecoTau.PFRecoTauDiscriminationByTrackIsolation_cfi import *

HChTauIDSources = [("HChTauIDleadingTrackPtCut", "DiscriminationForChargedHiggsByLeadingTrackPtCut"),
                   ("HChTauIDcharge", "DiscriminationByCharge"),
                   ("HChTauIDtauPolarization", "DiscriminationByTauPolarization"),
                   ("HChTauIDDeltaE", "DiscriminationByDeltaE"),
                   ("HChTauIDInvMass", "DiscriminationByInvMass"),
                   ("HChTauIDFlightPathSignif", "DiscriminationByFlightPathSignificance"),
                   ("HChTauID1Prong", "DiscriminationBy1Prong"),
                   ("HChTauID3Prongs", "DiscriminationBy3Prongs"),
                   ("HChTauID3ProngCombined", "DiscriminationForChargedHiggsBy3ProngCombined"),
                   ("HChTauID1or3Prongs", "DiscriminationForChargedHiggsBy1or3Prongs"),
                   ("HChTauID", "DiscriminationForChargedHiggs")]

def addDiscriminator(process, tau, name, module):
    module.PFTauProducer = cms.InputTag(tau)
    process.__setattr__(tau+name, module)
    return module

def addDiscriminatorSequence(process, tau, postfix=""):
    leadingTrackFinding = "hpsPFTauDiscriminationByDecayModeFinding"+postfix
    
    lst = []

    lst.append(addDiscriminator(process, tau, "DiscriminationForChargedHiggsByLeadingTrackPtCut"+postfix,
                                pfRecoTauDiscriminationByLeadingTrackPtCut.clone(
                                   MinPtLeadingObject = cms.double(20.0),
                                   qualityCuts = hplusTrackQualityCuts
                                   )))

    lst.append(addDiscriminator(process, tau, "DiscriminationByCharge"+postfix,
                                pfRecoTauDiscriminationByCharge.clone()))

    # index -1 points to the last element in the list
    lst.append(addDiscriminator(process, tau, "DiscriminationForChargedHiggsByECALIsolation"+postfix, 
                                pfRecoTauDiscriminationByECALIsolation.clone()))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationForChargedHiggsAgainstElectron"+postfix,
                                pfRecoTauDiscriminationAgainstElectron.clone()))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationForChargedHiggsAgainstMuon"+postfix,
                                pfRecoTauDiscriminationAgainstMuon.clone()))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByTauPolarization"+postfix,
                                pfRecoTauDiscriminationByTauPolarization.clone()))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByDeltaE"+postfix,
                                pfRecoTauDiscriminationByDeltaE.clone()))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)
    
    lst.append(addDiscriminator(process, tau, "DiscriminationByInvMass"+postfix,
                                pfRecoTauDiscriminationByInvMass.clone()))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationByFlightPathSignificance"+postfix,
                                pfRecoTauDiscriminationByFlightPathSignificance.clone()))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationBy1Prong"+postfix,
                                pfRecoTauDiscriminationByNProngs.clone(
                                  nProngs = cms.uint32(1)
                                  )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationBy3Prongs"+postfix,
                                pfRecoTauDiscriminationByNProngs.clone(
                                  nProngs = cms.uint32(3)
                                  )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationForChargedHiggsBy3ProngCombined"+postfix,
                                pfRecoTauDiscriminationByNProngs.clone(
                                  nProngs = cms.uint32(3),
                                  Prediscriminants = cms.PSet(
	                               BooleanOperator = cms.string("and"),
	                               leadTrack = cms.PSet(
	                                   Producer = cms.InputTag(leadingTrackFinding),
	                                   cut = cms.double(0.5)
	                               ),
	                               deltaE = cms.PSet(
	                                   Producer = cms.InputTag(tau+'DiscriminationByDeltaE'+postfix),
	                                   cut = cms.double(0.5)
	                               ),
	                               invMass = cms.PSet(
	                                   Producer = cms.InputTag(tau+'DiscriminationByInvMass'+postfix),
	                                   cut = cms.double(0.5)
	                               ),
	                               flightPathSig = cms.PSet(
	                                   Producer = cms.InputTag(tau+'DiscriminationByFlightPathSignificance'+postfix),
	                                   cut = cms.double(0.5)
	                               )
	                          )
                                )))
    lst[-1].Prediscriminants.leadTrack.Producer = cms.InputTag(leadingTrackFinding)

    lst.append(addDiscriminator(process, tau, "DiscriminationForChargedHiggsBy1or3Prongs"+postfix,
                                pfRecoTauDiscriminationByLeadingTrackFinding.clone(
	 			    Prediscriminants = cms.PSet(
	 			        BooleanOperator = cms.string("or"),
	 			        oneProng = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationBy1Prong'+postfix),
	 			            cut = cms.double(0.5)
	 			        ),
	 			        threeProng = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationForChargedHiggsBy3ProngCombined'+postfix),
	 			            cut = cms.double(0.5)
	 			        )
	 			    )
	 			)))
    lst.append(addDiscriminator(process, tau, "DiscriminationForChargedHiggs",
       			        pfRecoTauDiscriminationByTrackIsolation.clone(
	                             Prediscriminants = cms.PSet(
	 			        BooleanOperator = cms.string("and"),
	 			        leadingTrack = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationForChargedHiggsByLeadingTrackPtCut'+postfix),
	 			            cut = cms.double(0.5)
	 			        ),
	 			        charge = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationByCharge'+postfix),
	 			            cut = cms.double(0.5)
	 			        ),
	 			        ecalIsolation = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationForChargedHiggsByECALIsolation'+postfix),
	 			            cut = cms.double(0.5)
	 			        ),
	 			        electronVeto = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationForChargedHiggsAgainstElectron'+postfix),
	 			            cut = cms.double(0.5)
	 			        ),
	 			        polarization = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationByTauPolarization'+postfix),
	 			            cut = cms.double(0.5)
	 			        ),
	 			        prongs = cms.PSet(
	 			            Producer = cms.InputTag(tau+'DiscriminationForChargedHiggsBy1or3Prongs'+postfix),
	 			            cut = cms.double(0.5)
	 			        )
	 			    )
	 			)))

    sequence = cms.Sequence()
    for m in lst:
        sequence *= m

    setattr(process, tau+"HplusDiscriminationSequence"+postfix, sequence)
    return sequence

def addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos=["hpsPFTau"], postfix=""):
    sequence = cms.Sequence()
    setattr(process, "PFTauDiscriminationSequenceForChargedHiggs"+postfix, sequence)
    
    for algo in tauAlgos:
        sequence *= addDiscriminatorSequence(process, algo, postfix)
    
    return sequence
