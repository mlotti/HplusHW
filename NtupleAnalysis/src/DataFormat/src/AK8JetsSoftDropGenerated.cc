// -*- c++ -*-
#include "DataFormat/interface/AK8JetsSoftDropGenerated.h"

#include "Framework/interface/BranchManager.h"

void AK8JetsSoftDropGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCjet.setupBranches(mgr);

  mgr.book(prefix()+"_IDloose", &fIDloose);
  mgr.book(prefix()+"_IDtight", &fIDtight);
  mgr.book(prefix()+"_IDtightLeptonVeto", &fIDtightLeptonVeto);
  mgr.book(prefix()+"_PUIDloose", &fPUIDloose);
  mgr.book(prefix()+"_PUIDmedium", &fPUIDmedium);
  mgr.book(prefix()+"_PUIDtight", &fPUIDtight);
  mgr.book(prefix()+"_originatesFromChargedHiggs", &fOriginatesFromChargedHiggs);
  mgr.book(prefix()+"_originatesFromTop", &fOriginatesFromTop);
  mgr.book(prefix()+"_originatesFromUnknown", &fOriginatesFromUnknown);
  mgr.book(prefix()+"_originatesFromW", &fOriginatesFromW);
  mgr.book(prefix()+"_originatesFromZ", &fOriginatesFromZ);
  mgr.book(prefix()+"_NjettinessAK8CHStau1", &fNjettinessAK8CHStau1);
  mgr.book(prefix()+"_NjettinessAK8CHStau2", &fNjettinessAK8CHStau2);
  mgr.book(prefix()+"_NjettinessAK8CHStau3", &fNjettinessAK8CHStau3);
  mgr.book(prefix()+"_NjettinessAK8CHStau4", &fNjettinessAK8CHStau4);
  mgr.book(prefix()+"_pfCombinedInclusiveSecondaryVertexV2BJetTags", &fPfCombinedInclusiveSecondaryVertexV2BJetTags);
  mgr.book(prefix()+"_hadronFlavour", &fHadronFlavour);
  mgr.book(prefix()+"_partonFlavour", &fPartonFlavour);
  mgr.book(prefix()+"_nSubjets", &fnSubjets);
  mgr.book(prefix()+"_hasBTagSubjet", &fhasBTagSubjet);
}
