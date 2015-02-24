#include "DataFormat/interface/Jet.h"

#include "Framework/interface/BranchManager.h"

void JetCollection::setupBranches(BranchManager& mgr) {
  JetGeneratedCollection::setupBranches(mgr);
}
