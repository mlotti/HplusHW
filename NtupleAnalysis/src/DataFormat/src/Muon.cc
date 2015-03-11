#include "DataFormat/interface/Muon.h"

#include "Framework/interface/BranchManager.h"

void MuonCollection::setupBranches(BranchManager& mgr) {
  MuonGeneratedCollection::setupBranches(mgr);
}
