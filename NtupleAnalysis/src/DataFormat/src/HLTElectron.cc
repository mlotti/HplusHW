#include "DataFormat/interface/HLTElectron.h"

#include "Framework/interface/BranchManager.h"

void HLTElectronCollection::setupBranches(BranchManager& mgr) {
  HLTElectronGeneratedCollection::setupBranches(mgr);  
}
