// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeJetBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeJetBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

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
  class TreeJetBranches {
  public:
    TreeJetBranches(const edm::ParameterSet& iConfig, bool jetComposition);
    ~TreeJetBranches();

    void book(TTree *tree);
    void setValues(const edm::Event& iEvent);
    void reset();

    const edm::InputTag& getInputTag() const { return fJetSrc; }

  private:
    void setValues(const edm::View<pat::Jet>& muons);

    edm::InputTag fJetSrc;
    bool fJetComposition;

    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef HPlus::TreeFunctionVectorBranch<pat::Jet> JetFunctionBranch;

    std::vector<XYZTLorentzVector> fJets;
    std::vector<JetFunctionBranch> fJetsFunctions;

    std::vector<double> fJetsChf;
    std::vector<double> fJetsNhf;
    std::vector<double> fJetsElf;
    std::vector<double> fJetsPhf;
    std::vector<double> fJetsMuf;
    std::vector<int> fJetsChm;
    std::vector<int> fJetsNhm;
    std::vector<int> fJetsElm;
    std::vector<int> fJetsPhm;
    std::vector<int> fJetsMum;
    std::vector<double> fJetsJec;
    std::vector<double> fJetsArea;
    std::vector<bool> fJetsLooseId;
    std::vector<bool> fJetsTightId;
  };
}

#endif
