// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeMuonBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeMuonBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeGenParticleBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeValueMapBranch.h"

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

    void setValues(const edm::PtrVector<pat::Muon>& muons, const edm::Event& iEvent);
    void setValuesCorrected(const edm::PtrVector<pat::Muon>& muons);

    void reset();

    bool enabled() const { return fEnabled; }

    const edm::InputTag& getInputTag() const { return fMuonSrc; }
    const std::string getPrefix() const { return fPrefix; }

  private:
    edm::InputTag fMuonSrc;
    edm::InputTag fMuonCorrectedSrc;
    std::string fPrefix;

    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef math::XYZVector XYZVector;
    typedef HPlus::TreeFunctionVectorBranch<pat::Muon> MuonFunctionBranch;

    std::vector<XYZTLorentzVector> fMuons;
    std::vector<XYZTLorentzVector> fMuonsCorrected;
    std::vector<XYZVector> fMuonsTuneP;
    std::vector<double> fMuonsTunePPtError;
    std::vector<int> fMuonsCharge;
    std::vector<double> fMuonsNormChi2;
    std::vector<MuonFunctionBranch> fMuonsFunctions;
    std::vector<TreeValueMapBranch<bool> > fMuonsBools;
    TreeGenParticleBranches fMuonsGenMatch;

    const bool fEnabled;
    const bool fMuonCorrectedEnabled;
    const bool fTunePEnabled;
  };
}

#endif
