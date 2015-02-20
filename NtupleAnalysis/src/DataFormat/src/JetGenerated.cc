
#include "DataFormat/interface/JetGenerated.h"

#include "Framework/interface/BranchManager.h"

void JetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  mgr.book(prefix()+"_secondaryVertex", &fSecondaryVertex);
  mgr.book(prefix()+"_trackCountingHighEffBJetTags", &fTrackCountingHighEffBJetTags);
  mgr.book(prefix()+"_trackCountingHighPurBJetTags", &fTrackCountingHighPurBJetTags);
  mgr.book(prefix()+"_pdgId", &fPdgId);
}
