// -*- c++ -*-
#ifndef Tools_BooleanOr_h
#define Tools_BooleanOr_h

#include "Framework/interface/BranchManager.h"

#include <vector>
#include <string>

class BooleanOr {
public:
  BooleanOr();
  ~BooleanOr();

  void setBranchNames(const std::vector<std::string>& names) {
    fBranchNames = names;
  }
  /// Generic method for setting branches; branch name needs to be exact
  void setupBranches(BranchManager& mgr);
  /// Method for setting branches; a version postfix is automatically guessed
  void setupBranchesAutoScanVersion(BranchManager& mgr);
  
  bool value() const {
    if(fBranches.empty())
      throwEmpty();
    for(const Branch<bool> *branch: fBranches) {
      if(branch->value()) return true;
    }
    return false;
  }

  bool isEmpty() const {
    return fBranchNames.size() == 0;
    //    return fBranches.empty();
  }

private:
  void throwEmpty() const;

  std::vector<std::string> fBranchNames;
  std::vector<const Branch<bool> *> fBranches;
};

#endif
