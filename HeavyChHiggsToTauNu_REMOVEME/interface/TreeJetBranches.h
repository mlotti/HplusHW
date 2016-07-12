// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeJetBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeJetBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeValueMapBranch.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}

class TTree;

namespace HPlus {
  class TreeJetBranches {
  public:
    TreeJetBranches(const edm::ParameterSet& iConfig, bool jetComposition, const std::string& prefix = "jets_");
    ~TreeJetBranches();

    void book(TTree *tree);
    void setValues(const edm::Event& iEvent);
    void reset();

    bool enabled() const { return fEnabled; }

    const edm::InputTag& getInputTag() const { return fJetSrc; }

  private:
    edm::InputTag fJetSrc;
    std::string fPrefix;
    bool fEnabled;
    bool fDetailsEnabled;
    bool fJetComposition;

    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef HPlus::TreeFunctionVectorBranch<pat::Jet> JetFunctionBranch;

    struct PileupID {
      PileupID(const std::string& prefix, const edm::InputTag& mvaSrc, const edm::InputTag& flagSrc);
      ~PileupID();

      void book(TTree *tree);
      void setValues(const edm::Event& iEvent, const edm::PtrVector<pat::Jet>& jets);
      void reset();

      std::string fPrefix;
      edm::InputTag fMVAValueSrc;
      edm::InputTag fIDFlagSrc;

      std::vector<double> fMVAValue;
      std::vector<bool> fIDFlagLoose;
      std::vector<bool> fIDFlagMedium;
      std::vector<bool> fIDFlagTight;
    };

    std::vector<XYZTLorentzVector> fJets;
    std::vector<JetFunctionBranch> fJetsFunctions;
    std::vector<PileupID> fJetsPileupIDs;
    std::vector<TreeValueMapBranch<float> > fJetsFloats;
    std::vector<TreeValueMapBranch<bool> > fJetsBools;

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
    std::vector<unsigned> fJetsNumberOfDaughters;
    std::vector<int> fJetsFlavour;
    std::vector<int> fJetsGenPartonPdgId;
    std::vector<double> fJetsJec;
    std::vector<double> fJetsArea;
    std::vector<bool> fJetsLooseId;
    std::vector<bool> fJetsTightId;
  };
}

#endif
