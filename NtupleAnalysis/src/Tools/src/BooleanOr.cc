#include "Tools/interface/BooleanOr.h"
#include "Framework/interface/Exception.h"

#include <sstream>

BooleanOr::BooleanOr() {}
BooleanOr::~BooleanOr() {}

void BooleanOr::setupBranches(BranchManager& mgr) {
  for(auto& name: fBranchNames) {
    const Branch<bool> *branch = nullptr;
    mgr.book(name, &branch);
    if(branch->isValid()) {
      fBranches.push_back(branch);
    }
  }
}

void BooleanOr::setupBranchesAutoScanVersion(BranchManager& mgr) {
  for(auto& name: fBranchNames) {
    std::string genericName = name + "_vx";
    const Branch<bool> *branch = nullptr;
    mgr.book(genericName, &branch);
    if(branch->isValid()) {
      fBranches.push_back(branch);
    } else {
      for (int i = 0; i <= 100; ++i) {
        std::stringstream s;
        s << name;
        // Append version postfix; retain original string as first version
        if (i > 0)
          s << "_v" << i; 
        const Branch<bool> *branch = nullptr;
        mgr.book(s.str(), &branch);
        if(branch->isValid()) {
          fBranches.push_back(branch);
        }
      }
    }
  }
}

void BooleanOr::throwEmpty() const {
  std::string names;
  for(auto& name: fBranchNames) {
    if (names.size() > 0)
      names += ", ";
    names += name;
  }
  throw hplus::Exception("DataFormat") << "BooleanOr: None of the requested branches '" << names << "' exist in the TTree";
}
