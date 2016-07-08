// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeValueMapBranch_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeValueMapBranch_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "TTree.h"

#include<string>
#include<vector>

namespace HPlus {
  template <typename BranchType>
  class TreeValueMapBranch {
  public:
    TreeValueMapBranch(const std::string& name, const edm::InputTag& src): fName(name), fSrc(src) {}
    ~TreeValueMapBranch() {}

    void book(TTree *tree) {
      tree->Branch(fName.c_str(), &fValues);
    };

    template <typename CandType>
    void setValues(const edm::Event& iEvent, const edm::PtrVector<CandType>& cands) {
      edm::Handle<edm::ValueMap<BranchType> > hmap;
      iEvent.getByLabel(fSrc, hmap);

      for(size_t i=0; i<cands.size(); ++i) {
        fValues.push_back( (*hmap)[cands[i]] );
      }
    }

    void reset() {
      fValues.clear();
    }

  private:
    std::string fName;
    edm::InputTag fSrc;
    std::vector<BranchType> fValues;
  };
}

#endif
