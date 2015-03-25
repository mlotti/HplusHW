#include "DataFormat/interface/GenParticle.h"

#include "Framework/interface/BranchManager.h"

void GenParticleCollection::setupBranches(BranchManager& mgr) {
  GenParticleGeneratedCollection::setupBranches(mgr);
}
