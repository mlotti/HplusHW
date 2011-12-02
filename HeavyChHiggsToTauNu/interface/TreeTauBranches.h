// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeTauBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeTauBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}
namespace reco {
  class GenParticle;
}

class TTree;

namespace HPlus {
  class TreeTauBranches {
  public:
    TreeTauBranches(const edm::ParameterSet& iConfig);
    ~TreeTauBranches();

    void book(TTree *tree);
    void setValues(const edm::Event& iEvent);
    void setValues(const edm::Event& iEvent, const edm::View<reco::GenParticle>& genParticles);
    void reset();

  private:
    void setValues(const edm::View<pat::Tau>& muons);

    edm::InputTag fTauSrc;

    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef HPlus::TreeFunctionVectorBranch<pat::Tau> TauFunctionBranch;

    std::vector<XYZTLorentzVector> fTaus;
    std::vector<XYZTLorentzVector> fTausLeadingChCand;
    std::vector<unsigned> fTausSignalChCands;
    std::vector<double> fTausEmFraction;
    std::vector<int> fTausDecayMode;
    std::vector<TauFunctionBranch> fTausFunctions;
    std::vector<int> fTausPdgId;
    std::vector<int> fTausMotherPdgId;
    std::vector<int> fTausGrandMotherPdgId;
  };
}

#endif
