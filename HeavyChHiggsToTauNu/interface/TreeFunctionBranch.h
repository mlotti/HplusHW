// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeFunctionBranch_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeFunctionBranch_h

#include "CommonTools/Utils/interface/StringObjectFunction.h"

#include "TTree.h"

#include<string>

namespace HPlus {
  template <typename T>
  class TreeFunctionVectorBranch {
  public:
    TreeFunctionVectorBranch(const std::string& name, const std::string& function, bool lazy=true):
      fName(name), fFunction(function, lazy)
    {}
    ~TreeFunctionVectorBranch() {}

    void book(TTree *tree) {
      tree->Branch(fName.c_str(), &fValues);
    }

    template <typename Collection>
    void setValues(const Collection& collection) {
      for(typename Collection::const_iterator iter = collection.begin(); iter != collection.end(); ++iter) {
        fValues.push_back(this->fFunction(*iter));
      }
    }

    void reset() {
      fValues.clear();
    }

  private:
    std::string fName;
    StringObjectFunction<T> fFunction;
    std::vector<double> fValues;
  };
}

#endif
