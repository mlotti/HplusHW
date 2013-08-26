// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeTriggerBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeTriggerBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"

#include<vector>
#include<string>

namespace edm {
  class ParameterSet;
  class Event;
}
class TTree;

namespace HPlus {
  class TreeTriggerBranches {
  public:
    TreeTriggerBranches(const edm::ParameterSet& iConfig);
    ~TreeTriggerBranches();

    void book(TTree *tree);
    void setValues(const edm::Event& iEvent);
    void reset();

  private:
    edm::InputTag fPatTriggerSrc;

    struct TriggerPath {
      TriggerPath(const std::string& bn, const std::vector<std::string>& pns): fBranchName(bn), fPathNames(pns), fDecision(false) {}
      std::string fBranchName;
      std::vector<std::string> fPathNames;
      bool fDecision;
    };

    std::vector<TriggerPath> fPaths;
  };
}

#endif
