#include "DataFormat/interface/L1Tau.h"

#include "Framework/interface/BranchManager.h"

void L1TauCollection::setupBranches(BranchManager& mgr) {
  L1TauGeneratedCollection::setupBranches(mgr);  
}
