// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisTree_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisTree_h

#include "DataFormats/Common/interface/Ptr.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


#include<vector>

namespace edm {
  class Event;
}

class TFileDirectory;

class TTree;


namespace HPlus {
  class SignalAnalysisTree {
  public:
    explicit SignalAnalysisTree(const std::string& bDiscriminator);
    ~SignalAnalysisTree();

    void init(TFileDirectory& dir);

    void setPrescaleWeight(double w) { fPrescaleWeight = w; }
    void setPileupWeight(double w)   { fPileupWeight = w; }
    void setTriggerWeight(double w)  { fTriggerWeight = w; }

    void setNvertices(unsigned int n) { fNVertices = n; }

    void fill(const edm::Event& iEvent, const edm::PtrVector<pat::Tau>& taus,
              const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met);

  private:
    void reset();

    const std::string fBdiscriminator;

    TTree *fTree;

    unsigned int fEvent;
    unsigned int fLumi;
    unsigned int fRun;

    double fPrescaleWeight;
    double fPileupWeight;
    double fTriggerWeight;

    unsigned int fNVertices;

    math::XYZTLorentzVector fTau;
    math::XYZTLorentzVector fTauLeadingChCand;

    std::vector<math::XYZTLorentzVector> fJets;
    std::vector<double> fJetsBtags;
    std::vector<double> fJetsEMfracs;

    // MET is really 2-vector, but let's just use this for consistency
    math::XYZTLorentzVector fMet;
  };
}

#endif

