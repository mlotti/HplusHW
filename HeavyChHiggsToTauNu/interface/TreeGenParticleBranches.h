// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeGenParticleBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeGenParticleBranches_h

#include "DataFormats/Math/interface/LorentzVector.h"

#include<vector>
#include<string>

namespace reco {
  class GenParticle;
}

class TTree;

namespace HPlus {
  class TreeGenParticleBranches {
  public:
    TreeGenParticleBranches(const std::string& prefix);
    ~TreeGenParticleBranches();

    void book(TTree *tree);
    void addValue(const reco::GenParticle *particle);
    void reset();

  private:
    typedef math::XYZTLorentzVector XYZTLorentzVector;

    std::string fPrefix;

    std::vector<XYZTLorentzVector> fP4;
    std::vector<int> fPdgId;
    std::vector<int> fMotherPdgId;
    std::vector<int> fGrandMotherPdgId;
  };
}

#endif
