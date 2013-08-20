// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeGenBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeGenBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}

class TTree;

namespace HPlus {
  class TreeGenBranches {
  public:
    TreeGenBranches(const edm::ParameterSet& iConfig);
    ~TreeGenBranches();

    void book(TTree *tree);
    void setValues(const edm::Event& iEvent);
    void reset();

    const edm::InputTag& getInputTag() const { return fGenSrc; }

  private:
    edm::InputTag fGenSrc;

    unsigned fNumberBquarks;
    unsigned fNumberWTaus;
    unsigned fNumberZTaus;
    unsigned fNumberHTaus;
    unsigned fNumberXTaus;
  };
}

#endif
