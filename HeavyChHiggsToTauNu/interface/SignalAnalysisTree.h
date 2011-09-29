// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisTree_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisTree_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Ptr.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}

class TFileDirectory;

class TTree;


namespace HPlus {
  class SignalAnalysisTree {
  public:
    typedef math::XYZTLorentzVector XYZTLorentzVector;

    explicit SignalAnalysisTree(const edm::ParameterSet& iConfig, const std::string& bDiscriminator);
    ~SignalAnalysisTree();

    void init(TFileDirectory& dir);

    void setPrescaleWeight(double w) { fPrescaleWeight = w; }
    void setPileupWeight(double w)   { fPileupWeight = w; }
    void setTriggerWeight(double w)  { fTriggerWeight = w; }
    void setFillWeight(double w)  { fFillWeight = w; }

    void setNvertices(unsigned int n) { fNVertices = n; }
    void setBTagging(bool passed, double scaleFactor) { fPassedBTagging = passed; fBTaggingWeight = scaleFactor; }
    void setTop(const XYZTLorentzVector& top) { fTop = top; }

    void setRawMET(const edm::Ptr<reco::MET>& met) { fRawMet = met->p4(); fRawMetSumEt = met->sumEt(); }
    void setType1MET(const edm::Ptr<reco::MET>& met) { fType1Met = met->p4(); }
    void setType2MET(const edm::Ptr<reco::MET>& met) { fType2Met = met->p4(); }

    void fill(const edm::Event& iEvent, const edm::PtrVector<pat::Tau>& taus,
              const edm::PtrVector<pat::Jet>& jets,
              double alphaT);

  private:
    void reset();

    struct TauId {
      TauId(const std::string& n): name(n), value(false) {}
      void reset() { value = false; }
      std::string name;
      bool value;
    };

    const std::string fBdiscriminator;
    const bool fDoFill;
    const bool fTauEmbeddingInput;

    edm::InputTag fTauEmbeddingMuonSource;
    edm::InputTag fTauEmbeddingMetSource;
    edm::InputTag fTauEmbeddingCaloMetSource;

    TTree *fTree;

    unsigned int fEvent;
    unsigned int fLumi;
    unsigned int fRun;

    double fPrescaleWeight;
    double fPileupWeight;
    double fTriggerWeight;
    double fBTaggingWeight;
    double fFillWeight;

    unsigned int fNVertices;

    XYZTLorentzVector fTau;
    XYZTLorentzVector fTauLeadingChCand;
    unsigned int fTauSignalChCands;
    std::vector<TauId> fTauIds;

    std::vector<XYZTLorentzVector> fJets;
    std::vector<double> fJetsBtags;
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

    // MET is really 2-vector, but let's just use this for consistency
    XYZTLorentzVector fRawMet;
    double fRawMetSumEt;
    XYZTLorentzVector fType1Met;
    XYZTLorentzVector fType2Met;

    XYZTLorentzVector fTop;

    double fAlphaT;

    bool fPassedBTagging;

    // Tau embedding stuff
    XYZTLorentzVector fTauEmbeddingMuon;
    XYZTLorentzVector fTauEmbeddingMet;
    XYZTLorentzVector fTauEmbeddingCaloMet;
  };
}

#endif

