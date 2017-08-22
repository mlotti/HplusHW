#include "DataFormat/interface/HLTBJet.h"

#include "Framework/interface/BranchManager.h"

void HLTBJetCollection::setupBranches(BranchManager& mgr) {
  HLTBJetGeneratedCollection::setupBranches(mgr);  
}

