// -*- c++ -*-
#ifndef Framework_Branch_h
#define Framework_Branch_h

#include "Framework/interface/BranchBase.h"
#include "Framework/interface/BranchTraits.h"
#include "Framework/interface/type.h"

#include "TTree.h"
#include "TBranch.h"

#include <string>

// Generic branch
template <typename T>
class Branch: public BranchBase {
public:
  explicit Branch(const std::string& n): BranchBase(n), data(0) {}
  virtual ~Branch() {}

  void setupBranch(TTree *tree) {
    // Protect SetBranchAddress() to avoid warning message, we'll deal
    // non-existing branches in another way
    TBranch *branch = tree->GetBranch(this->name.c_str());
    if(branch && isBranchTypeOk(std::string(branch->GetClassName()))) {
      tree->SetBranchAddress(this->name.c_str(), &data, &this->branch);
    }
  }
  typename BranchTraits<T>::ReturnType value() const {
    if(!cached) {
      assertValid();
      branch->GetEntry(this->entry);
      cached = true;
    }
    return BranchTraits<T>::get(data);
  }

  virtual std::string getTypeName() const {
    return type<T>();
  }

private:
  typename BranchTraits<T>::DataType data;
};

#endif
