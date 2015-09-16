#include "DataFormat/interface/PFCands.h"

#include "Framework/interface/BranchManager.h"

void PFCandsCollection::setupBranches(BranchManager& mgr) {
  PFcandidateGeneratedCollection::setupBranches(mgr);  
}

