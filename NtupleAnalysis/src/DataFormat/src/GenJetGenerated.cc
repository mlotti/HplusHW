
#include "DataFormat/interface/GenJetGenerated.h"

#include "Framework/interface/BranchManager.h"

void GenJetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  //mgr.book(prefix()+"_secondaryVertex", &fSecondaryVertex);
  //mgr.book(prefix()+"_trackCountingHighEffBGenJetTags", &fTrackCountingHighEffBGenJetTags);
  //mgr.book(prefix()+"_trackCountingHighPurBGenJetTags", &fTrackCountingHighPurBGenJetTags);
  mgr.book(prefix()+"_pdgId", &fPdgId);
  //mgr.book(prefix()+"_PUIDloose", &fPUIDloose);
  //mgr.book(prefix()+"_PUIDmedium", &fPUIDmedium);
  //mgr.book(prefix()+"_PUIDtight", &fPUIDtight);
}
