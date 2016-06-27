
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/MuonGenerated.h"

#include "Framework/interface/BranchManager.h"

void MuonGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCmuon.setupBranches(mgr);

  mgr.book(prefix()+"_TrgMatch_IsoMu16_eta2p1", &fTrgMatch_IsoMu16_eta2p1);
  mgr.book(prefix()+"_TrgMatch_IsoMu17_eta2p1", &fTrgMatch_IsoMu17_eta2p1);
  mgr.book(prefix()+"_TrgMatch_IsoMu18", &fTrgMatch_IsoMu18);
  mgr.book(prefix()+"_TrgMatch_IsoMu19_eta2p1", &fTrgMatch_IsoMu19_eta2p1);
  mgr.book(prefix()+"_TrgMatch_IsoMu20", &fTrgMatch_IsoMu20);
  mgr.book(prefix()+"_TrgMatch_IsoMu21_eta2p1", &fTrgMatch_IsoMu21_eta2p1);
  mgr.book(prefix()+"_TrgMatch_IsoMu22", &fTrgMatch_IsoMu22);
  mgr.book(prefix()+"_TrgMatch_IsoMu24", &fTrgMatch_IsoMu24);
  mgr.book(prefix()+"_isGlobalMuon", &fIsGlobalMuon);
  mgr.book(prefix()+"_muIDLoose", &fMuIDLoose);
  mgr.book(prefix()+"_muIDMedium", &fMuIDMedium);
  mgr.book(prefix()+"_muIDTight", &fMuIDTight);
  mgr.book(prefix()+"_relIsoDeltaBeta", &fRelIsoDeltaBeta);
  mgr.book(prefix()+"_charge", &fCharge);
}
