// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeMuonBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeMuonBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"

#include<vector>
#include<string>

namespace edm {
  class ParameterSet;
  class Event;
}
namespace reco {
  class GenParticle;
}

class TTree;

namespace HPlus {
  class TreeMuonBranches {
  public:
    TreeMuonBranches(const edm::ParameterSet& iConfig, const std::string& prefix="muons");
    ~TreeMuonBranches();

    void book(TTree *tree);

    size_t setValues(const edm::Event& iEvent);
    size_t setValues(const edm::Event& iEvent, const edm::View<reco::GenParticle>& genParticles);

    void setValues(const edm::PtrVector<pat::Muon>& muons);

    void reset();

    const edm::InputTag& getInputTag() const { return fMuonSrc; }

  private:
    edm::InputTag fMuonSrc;
    std::string fPrefix;

    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef HPlus::TreeFunctionVectorBranch<pat::Muon> MuonFunctionBranch;

    std::vector<XYZTLorentzVector> fMuons;
    std::vector<MuonFunctionBranch> fMuonsFunctions;
    TreeGenParticleBranches fMuonsGenMatch;
  };
}

#endif
