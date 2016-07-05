
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/ElectronGenerated.h"

#include "Framework/interface/BranchManager.h"

void ElectronGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  fMCelectron.setupBranches(mgr);

  mgr.book(prefix()+"_cutBasedElectronID_Spring15_25ns_V1_standalone_loose", &fCutBasedElectronID_Spring15_25ns_V1_standalone_loose);
  mgr.book(prefix()+"_cutBasedElectronID_Spring15_25ns_V1_standalone_medium", &fCutBasedElectronID_Spring15_25ns_V1_standalone_medium);
  mgr.book(prefix()+"_cutBasedElectronID_Spring15_25ns_V1_standalone_tight", &fCutBasedElectronID_Spring15_25ns_V1_standalone_tight);
  mgr.book(prefix()+"_cutBasedElectronID_Spring15_25ns_V1_standalone_veto", &fCutBasedElectronID_Spring15_25ns_V1_standalone_veto);
  mgr.book(prefix()+"_effAreaIsoDeltaBeta", &fEffAreaIsoDeltaBeta);
  mgr.book(prefix()+"_relIsoDeltaBeta", &fRelIsoDeltaBeta);
}
