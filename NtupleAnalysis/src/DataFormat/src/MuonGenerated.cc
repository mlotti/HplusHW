
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/MuonGenerated.h"

#include "Framework/interface/BranchManager.h"

void MuonGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  mgr.book(prefix()+"_isGlobalMuon", &fIsGlobalMuon);
}
