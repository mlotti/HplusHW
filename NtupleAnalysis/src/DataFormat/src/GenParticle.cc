#include "DataFormat/interface/GenParticle.h"

#include "Framework/interface/BranchManager.h"

void GenParticleCollection::setupBranches(BranchManager& mgr) {
  GenParticleGeneratedCollection::setupBranches(mgr);
  mgr.book(prefix()+"_mother", &fMother);
  //mgr.book(prefix()+"_status", &fStatus);
  mgr.book(prefix()+"_tauProng", &fTauProng);
  mgr.book(prefix()+"_tauVisiblePt", &fTauVisiblePt);
  mgr.book(prefix()+"_tauVisiblePhi", &fTauVisiblePhi);
  mgr.book(prefix()+"_tauVisibleEta", &fTauVisibleEta);
  mgr.book(prefix()+"_tauSpinEffectsW", &fTauSpinEffectsW);
  mgr.book(prefix()+"_tauSpinEffectsHpm", &fTauSpinEffectsHpm);
  mgr.book(prefix()+"_associatedWithHpm", &fAssociatedWithHpm);

}
