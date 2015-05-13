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

  void setupBranches(BranchManager& mgr);

  bool value() const {
    if(fBranches.empty())
      return true;
    //      throwEmpty();
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
