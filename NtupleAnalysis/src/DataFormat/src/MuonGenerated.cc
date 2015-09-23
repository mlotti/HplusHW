
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/MuonGenerated.h"

#include "Framework/interface/BranchManager.h"

void MuonGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCmuon.setupBranches(mgr);

  mgr.book(prefix()+"_isGlobalMuon", &fIsGlobalMuon);
  mgr.book(prefix()+"_muIDLoose", &fMuIDLoose);
  mgr.book(prefix()+"_muIDMedium", &fMuIDMedium);
  mgr.book(prefix()+"_muIDTight", &fMuIDTight);
  mgr.book(prefix()+"_relIsoDeltaBeta", &fRelIsoDeltaBeta);
}
