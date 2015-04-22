
#include "DataFormat/interface/JetGenerated.h"

#include "Framework/interface/BranchManager.h"

void JetGeneratedCollection::setupBranches(BranchManager& mgr) {
  ParticleCollection::setupBranches(mgr);
  mgr.book(prefix()+"_secondaryVertex", &fSecondaryVertex);
  mgr.book(prefix()+"_trackCountingHighEffBJetTags", &fTrackCountingHighEffBJetTags);
  mgr.book(prefix()+"_trackCountingHighPurBJetTags", &fTrackCountingHighPurBJetTags);
  mgr.book(prefix()+"_jetProbabilityBJetTags", &fJetProbabilityBJetTags);
  mgr.book(prefix()+"_jetBProbabilityBJetTags", &fJetBProbabilityBJetTags);
  mgr.book(prefix()+"_PUIDloose", &fPUIDloose);
  mgr.book(prefix()+"_PUIDmedium", &fPUIDmedium);
  mgr.book(prefix()+"_PUIDtight", &fPUIDtight);
}
