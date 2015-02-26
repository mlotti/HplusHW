// -*- c++ -*-
#ifndef Framework_BranchManager_h
#define Framework_BranchManager_h

#include "Framework/interface/Branch.h"

#include "Rtypes.h"

#include <vector>
#include <string>
#include <memory>
#include <algorithm>

class TTree;

// Branch manager, to allow multiple analyzer modules
class BranchManager {
public:
  BranchManager();
  ~BranchManager();

  void setTree(TTree *tree) { fTree = tree; }

  template <typename T>
  void book(const std::string& branchName, Branch<T> **returnValue) {
    auto found = std::lower_bound(fBranches.begin(), fBranches.end(), branchName, [](const std::unique_ptr<BranchBase>& a, const std::string& b) {
        return a->getName() < b;
      });

    if(found == fBranches.end() || (*found)->getName() != branchName) {
      auto tmp = std::unique_ptr<BranchBase>(new Branch<T>(branchName));
      found = fBranches.insert(found, std::move(tmp));
    }
    Branch<T> *ptr = dynamic_cast<Branch<T> *>(found->get());
    if(!ptr) throwTypeMismatch(branchName, (*found)->getTypeName(), type<T>());
    ptr->setupBranch(fTree);
    *returnValue = ptr;
  }

  void setEntry(Long64_t entry) {
    for(auto&& branch: fBranches) {
      branch->setEntry(entry);
    }
  }

private:
  void throwTypeMismatch(const std::string& name, const std::string& oldType, const std::string& newType) const;
  TTree *fTree; // not the owner
  std::vector<std::unique_ptr<BranchBase>> fBranches;  // owner
};

#endif

