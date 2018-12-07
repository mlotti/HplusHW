#include "DataFormat/interface/HLTMuon.h"

#include "Framework/interface/BranchManager.h"

void HLTMuonCollection::setupBranches(BranchManager& mgr) {
  HLTMuonGeneratedCollection::setupBranches(mgr);  
}
