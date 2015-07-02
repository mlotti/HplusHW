
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/JetGenerated.h"

#include "Framework/interface/BranchManager.h"

void JetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  mgr.book(prefix()+"_jetProbabilityBJetTags", &fJetProbabilityBJetTags);
  mgr.book(prefix()+"_jetBProbabilityBJetTags", &fJetBProbabilityBJetTags);
  mgr.book(prefix()+"_PUIDloose", &fPUIDloose);
  mgr.book(prefix()+"_PUIDmedium", &fPUIDmedium);
  mgr.book(prefix()+"_PUIDtight", &fPUIDtight);
  mgr.book(prefix()+"_pileupJetIdfullDiscriminant", &fPileupJetIdfullDiscriminant);
  mgr.book(prefix()+"_combinedInclusiveSecondaryVertexBJetTags", &fCombinedInclusiveSecondaryVertexBJetTags);
  mgr.book(prefix()+"_combinedInclusiveSecondaryVertexV2BJetTags", &fCombinedInclusiveSecondaryVertexV2BJetTags);
  mgr.book(prefix()+"_combinedSecondaryVertexBJetTags", &fCombinedSecondaryVertexBJetTags);
  mgr.book(prefix()+"_jetBProbabilityBJetTags", &fJetBProbabilityBJetTags);
  mgr.book(prefix()+"_jetProbabilityBJetTags", &fJetProbabilityBJetTags);
  mgr.book(prefix()+"_simpleSecondaryVertexHighEffBJetTags", &fSimpleSecondaryVertexHighEffBJetTags);
  mgr.book(prefix()+"_simpleSecondaryVertexHighPurBJetTags", &fSimpleSecondaryVertexHighPurBJetTags);
  mgr.book(prefix()+"_trackCountingHighEffBJetTags", &fTrackCountingHighEffBJetTags);
  mgr.book(prefix()+"_trackCountingHighPurBJetTags", &fTrackCountingHighPurBJetTags);
}
