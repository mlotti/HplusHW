
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/AK8JetGenerated.h"

#include "Framework/interface/BranchManager.h"

void AK8JetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCjet.setupBranches(mgr);

  mgr.book(prefix()+"_IDloose", &fIDloose);
  mgr.book(prefix()+"_IDtight", &fIDtight);
  mgr.book(prefix()+"_IDtightLeptonVeto", &fIDtightLeptonVeto);
  mgr.book(prefix()+"_PUIDloose", &fPUIDloose);
  mgr.book(prefix()+"_PUIDmedium", &fPUIDmedium);
  mgr.book(prefix()+"_PUIDtight", &fPUIDtight);
  mgr.book(prefix()+"_NjettinessAK8tau1", &fNjettinessAK8tau1);
  mgr.book(prefix()+"_NjettinessAK8tau2", &fNjettinessAK8tau2);
  mgr.book(prefix()+"_NjettinessAK8tau3", &fNjettinessAK8tau3);
  mgr.book(prefix()+"_ak8PFJetsCHSPrunedMass", &fAk8PFJetsCHSPrunedMass);
  mgr.book(prefix()+"_ak8PFJetsCHSSoftDropMass", &fAk8PFJetsCHSSoftDropMass);
  mgr.book(prefix()+"_corrPrunedMass", &fCorrPrunedMass);
  mgr.book(prefix()+"_sdsubjet1_csv", &fSdsubjet1_csv);
  mgr.book(prefix()+"_sdsubjet1_eta", &fSdsubjet1_eta);
  mgr.book(prefix()+"_sdsubjet1_mass", &fSdsubjet1_mass);
  mgr.book(prefix()+"_sdsubjet1_phi", &fSdsubjet1_phi);
  mgr.book(prefix()+"_sdsubjet1_pt", &fSdsubjet1_pt);
  mgr.book(prefix()+"_sdsubjet2_csv", &fSdsubjet2_csv);
  mgr.book(prefix()+"_sdsubjet2_eta", &fSdsubjet2_eta);
  mgr.book(prefix()+"_sdsubjet2_mass", &fSdsubjet2_mass);
  mgr.book(prefix()+"_sdsubjet2_phi", &fSdsubjet2_phi);
  mgr.book(prefix()+"_sdsubjet2_pt", &fSdsubjet2_pt);
  mgr.book(prefix()+"_pfCombinedInclusiveSecondaryVertexV2BJetTags", &fPfCombinedInclusiveSecondaryVertexV2BJetTags);
  mgr.book(prefix()+"_hadronFlavour", &fHadronFlavour);
  mgr.book(prefix()+"_nsoftdropSubjets", &fNsoftdropSubjets);
  mgr.book(prefix()+"_numberOfDaughters", &fNumberOfDaughters);
  mgr.book(prefix()+"_partonFlavour", &fPartonFlavour);
}
