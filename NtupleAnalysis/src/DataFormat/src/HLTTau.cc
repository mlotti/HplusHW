#include "DataFormat/interface/HLTTau.h"

#include "Framework/interface/BranchManager.h"

void HLTTauCollection::setupBranches(BranchManager& mgr) {
  HLTTauGeneratedCollection::setupBranches(mgr);  
}

