#include "Tools/interface/BooleanOr.h"

BooleanOr::BooleanOr() {}
BooleanOr::~BooleanOr() {}

void BooleanOr::setupBranches(BranchManager& mgr) {
  for(auto& name: fBranchNames) {
    Branch<bool> *branch = nullptr;
    mgr.book(name, &branch);
    if(branch->isValid())
      fBranches.push_back(branch);
  }
}

void BooleanOr::throwEmpty() const {
  std::string names;
  for(auto& name: fBranchNames)
    names += name+ " ";
  throw std::runtime_error("BooleanOr: None of the requested brances '"+names+ "' exist in the TTree");
}
