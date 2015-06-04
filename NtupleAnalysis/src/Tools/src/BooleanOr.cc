#include "Tools/interface/BooleanOr.h"
#include "Framework/interface/Exception.h"

BooleanOr::BooleanOr() {}
BooleanOr::~BooleanOr() {}

void BooleanOr::setupBranches(BranchManager& mgr) {
  for(auto& name: fBranchNames) {
    const Branch<bool> *branch = nullptr;
    mgr.book(name, &branch);
    if(branch->isValid())
      fBranches.push_back(branch);
  }
}

void BooleanOr::throwEmpty() const {
  std::string names;
  for(auto& name: fBranchNames)
    names += name+ " ";
  throw hplus::Exception("DataFormat") << "BooleanOr: None of the requested brances '" << names << "' exist in the TTree";
}
