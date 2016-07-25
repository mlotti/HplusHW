// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeGenTauBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeGenTauBranches_h

#include "DataFormats/Math/interface/LorentzVector.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"

namespace HPlus {
  class TreeGenTauBranches {
  public:
    TreeGenTauBranches(const std::string& prefix);
    ~TreeGenTauBranches();

    void book(TTree *tree);
    void addValue(const reco::GenParticle *tau);
    void reset();

  private:
    typedef math::XYZTLorentzVector XYZTLorentzVector;

    std::string fPrefix;

    TreeGenParticleBranches fGenParticle;
    std::vector<int> fDaughterPdgId;
    std::vector<XYZTLorentzVector> fVisibleP4;
  };
}

#endif
