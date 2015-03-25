#include "DataFormat/interface/GenJet.h"

#include "Framework/interface/BranchManager.h"

void GenJetCollection::setupBranches(BranchManager& mgr) {
  GenJetGeneratedCollection::setupBranches(mgr);
}
