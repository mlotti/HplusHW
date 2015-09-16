
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/ElectronGenerated.h"

#include "Framework/interface/BranchManager.h"

void ElectronGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCelectron.setupBranches(mgr);

  mgr.book(prefix()+"_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80", &fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp80);
  mgr.book(prefix()+"_mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", &fMvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90);
  mgr.book(prefix()+"_relIsoDeltaBeta", &fRelIsoDeltaBeta);
}
