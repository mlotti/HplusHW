// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeEventBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeEventBranches_h

namespace edm {
  class Event;
}

class TTree;

namespace HPlus {
  class TreeEventBranches {
  public:
    TreeEventBranches();
    ~TreeEventBranches();

    void book(TTree *tree);
    void setValues(const edm::Event& iEvent);
    void reset();

  private:
    unsigned int fEvent;
    unsigned int fLumi;
    unsigned int fRun;
  };
}

#endif
