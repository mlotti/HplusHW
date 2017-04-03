#include "DataFormat/interface/L1Jet.h"

#include "Framework/interface/BranchManager.h"

void L1JetCollection::setupBranches(BranchManager& mgr) {
  L1JetGeneratedCollection::setupBranches(mgr);  
}
