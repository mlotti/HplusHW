
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/JetGenerated.h"

#include "Framework/interface/BranchManager.h"

void JetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  mgr.book(prefix()+"_IDloose", &fIDloose);
  mgr.book(prefix()+"_IDtight", &fIDtight);
  mgr.book(prefix()+"_IDtightLeptonVeto", &fIDtightLeptonVeto);
  mgr.book(prefix()+"_PUIDloose", &fPUIDloose);
  mgr.book(prefix()+"_PUIDmedium", &fPUIDmedium);
  mgr.book(prefix()+"_PUIDtight", &fPUIDtight);
  mgr.book(prefix()+"_eJERdown", &fEJERdown);
  mgr.book(prefix()+"_eJERup", &fEJERup);
  mgr.book(prefix()+"_eJESdown", &fEJESdown);
  mgr.book(prefix()+"_eJESup", &fEJESup);
  mgr.book(prefix()+"_eMCjet", &fEMCjet);
  mgr.book(prefix()+"_etaJERdown", &fEtaJERdown);
  mgr.book(prefix()+"_etaJERup", &fEtaJERup);
  mgr.book(prefix()+"_etaJESdown", &fEtaJESdown);
  mgr.book(prefix()+"_etaJESup", &fEtaJESup);
  mgr.book(prefix()+"_etaMCjet", &fEtaMCjet);
  mgr.book(prefix()+"_phiJERdown", &fPhiJERdown);
  mgr.book(prefix()+"_phiJERup", &fPhiJERup);
  mgr.book(prefix()+"_phiJESdown", &fPhiJESdown);
  mgr.book(prefix()+"_phiJESup", &fPhiJESup);
  mgr.book(prefix()+"_phiMCjet", &fPhiMCjet);
  mgr.book(prefix()+"_pileupJetIdfullDiscriminant", &fPileupJetIdfullDiscriminant);
  mgr.book(prefix()+"_ptJERdown", &fPtJERdown);
  mgr.book(prefix()+"_ptJERup", &fPtJERup);
  mgr.book(prefix()+"_ptJESdown", &fPtJESdown);
  mgr.book(prefix()+"_ptJESup", &fPtJESup);
  mgr.book(prefix()+"_ptMCjet", &fPtMCjet);
  mgr.book(prefix()+"_pfCombinedInclusiveSecondaryVertexBJetTags", &fPfCombinedInclusiveSecondaryVertexBJetTags);
  mgr.book(prefix()+"_pfCombinedInclusiveSecondaryVertexV2BJetTags", &fPfCombinedInclusiveSecondaryVertexV2BJetTags);
  mgr.book(prefix()+"_pfCombinedMVABJetTag", &fPfCombinedMVABJetTag);
  mgr.book(prefix()+"_pfCombinedSecondaryVertexBJetTags", &fPfCombinedSecondaryVertexBJetTags);
  mgr.book(prefix()+"_pfJetBProbabilityBJetTags", &fPfJetBProbabilityBJetTags);
  mgr.book(prefix()+"_pfJetProbabilityBJetTags", &fPfJetProbabilityBJetTags);
  mgr.book(prefix()+"_hadronFlavour", &fHadronFlavour);
  mgr.book(prefix()+"_partonFlavour", &fPartonFlavour);
}
