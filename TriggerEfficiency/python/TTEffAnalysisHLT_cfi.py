import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.GeometryExtended_cff import *
from Configuration.StandardSequences.MagneticField_38T_cff import *

from Configuration.StandardSequences.SimL1Emulator_cff import *

# OpenHLT specificss
# Define the HLT reco paths
from HLTrigger.HLTanalyzers.HLTopen_cff import *

DQM = cms.Service( "DQM",)
DQMStore = cms.Service( "DQMStore",)

# pdt
from SimGeneral.HepPDTESSource.pythiapdt_cfi import *

#fix to the eta-phi distributions when using startup mc
openhltL25TauPixelSeeds.RegionFactoryPSet.RegionPSet.originHalfLength = cms.double( 15.0 )
### missing parameters
hltParticleFlowRecHitECAL.thresh_Cleaning = cms.double( 2.0 )
hltPFTauLooseIsolationDiscriminator.qualityCuts.primaryVertexSrc = cms.InputTag( "hltPixelVertices" )
hltPFTauLooseIsolationDiscriminator.qualityCuts.pvFindingAlgo = cms.string("highestWeightForLeadTrack")

# Remove L2.5 calo tau reconstruction, from 44x tracking takes way too much time
DoHLTTau.remove(TauOpenHLT)
DoHLTTau.remove(OpenHLTL25TauTrackIsolation)
DoHLTTau.remove(OpenHLTL25TauTrackReconstructionSequence)
del TauOpenHLT
del openhltL25TauConeIsolation
del openhltL25TauJetTracksAssociator
del openhltL25TauCtfWithMaterialTracks
del openhltL25TauCkfTrackCandidates
del openhltL25TauPixelSeeds
del OpenHLTL25TauTrackIsolation
del OpenHLTL25TauTrackReconstructionSequence

# Add the isolation sequence
DoHLTTau *= HLTPFTauMediumIsoSequence
HLTPFTauMediumIsoSequence *= hltPFTauMediumIsoTrackPt20Discriminator
DoHLTTau *= HLTPFTauSequence
hltPFTauTrackPt20Discriminator = hltPFTauMediumIsoTrackPt20Discriminator.clone(
    PFTauProducer = "hltPFTaus"
)
HLTPFTauSequence *= hltPFTauTrackPt20Discriminator

# Do also global L2 jet clustering
hltIconeJetGlobal = hltIconeTau1Regional.clone(
    src = "hltTowerMakerForAll"
)
openhltL2TauGlobalIsolationProducer = openhltL2TauIsolationProducer.clone(
    L2TauJetCollection = "hltIconeJetGlobal"
)
DoHLTTau *= (
    hltIconeJetGlobal *
    openhltL2TauGlobalIsolationProducer
)

# No vertex requirement for tau reconstruction (i.e. leading track)
#hltPFTauTagInfo.UsePVconstraint = False

# PFTauVertexSelector
pfTauVertexSelector = cms.EDFilter("PFTauVertexSelector",
    # Tau collection
    tauSrc = cms.InputTag('hltPFTausMediumIso'),
    # Vertex from primary vertex collection
    useVertex = cms.bool(True),
    vertexSrc = cms.InputTag("hltPixelVertices"),
    useBeamSpot = cms.bool(False),
    beamSpotSrc = cms.InputTag("dummy"),
    # use leading track instead of primary vertex collection
    useLeadingTrack = cms.bool(True),
    # Vertex from leading track to be used
    trackSrc = cms.VInputTag(cms.InputTag("hltIter4Merged")),
    # use leading RecoCandidate instead of primary vertex collection
    useLeadingRecoCandidate = cms.bool(False),
    # Vertex from RecoCandidate(e.g. lepton) track to be used
    recoCandidateSrc = cms.VInputTag(),
    useTriggerFilterElectrons = cms.bool(False),
    triggerFilterElectronsSrc = cms.InputTag("dummy"),
    useTriggerFilterMuons = cms.bool(False),
    triggerFilterMuonsSrc = cms.InputTag("dummy"),
    # max dZ distance to primary vertex
    dZ = cms.double(0.2),
    # filter events with at least N taus from PV
    filterOnNTaus = cms.uint32(0),

)
pfTauVertexSelectorMediumIso = pfTauVertexSelector.clone(
    tauSrc = "hltPFTaus"
)
#hltPFTauTagInfo.UsePVconstraint = False # no requirement of the leading track to come from PV 
#hltPFTausMediumIso.ChargedHadrCandLeadChargedHadrCand_tksmaxDZ=0.2 # make sure all tracks come from same vertex as the leading track
#hltPFTaus.ChargedHadrCandLeadChargedHadrCand_tksmaxDZ=0.2 # make sure all tracks come from same vertex as the leading track
DoHLTTau *= (
    pfTauVertexSelector *
    pfTauVertexSelectorMediumIso
)
