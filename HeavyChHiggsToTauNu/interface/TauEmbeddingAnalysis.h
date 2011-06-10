// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingAnalysis_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Ptr.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}
namespace reco {
  class MET;
  class Muon;
}
namespace pat {
  class Tau;
}

class TFileDirectory;

class TH1;

#include "TH2.h"

namespace HPlus {
  class EventWeight;

  class TauEmbeddingAnalysis {
    // Class for one set of histograms
    class Histograms {
    public:
      Histograms();
      ~Histograms();

      void book(TFileDirectory& fd, const std::string& prefix);

      // Fill the histograms (add more objects to arguments if necessary)
      void fill(double weight, const reco::MET *originalMet, const reco::MET *embeddingMet, const reco::Muon* originalMuon, const pat::Tau* selectedTau);

    private:
      // Histograms
      TH1 *hOriginalMet;
      TH1 *hEmbeddingMet;
      TH1 *hOriginalMuonPt;
      TH1 *hOriginalMuonEta;
      TH1 *hOriginalMuonPhi;
      TH1 *hSelectedTauPt;
      TH1 *hSelectedTauEta;
      TH1 *hSelectedTauPhi;
      TH1 *hSelectedTauIsolation05;
      TH1 *hSelectedTauIsolation10;
      TH1 *hleadPFChargedHadrPt;
      TH1 *hRtau;
      TH1 *hDeltaPhiOriginal;
      TH1 *hTransverseMassOriginal;
      TH1 *hDeltaPhi;
      TH1 *hTransverseMass;
      TH2 *hEmbVSOrigMet;
      TH2 *hDeltaPhiEmbVSOrig;
      TH2 *hMTEmbVSOrig; 
    };

  public:
    TauEmbeddingAnalysis(const edm::ParameterSet& iConfig, EventWeight& eventWeight);
    ~TauEmbeddingAnalysis();

    // Read the objects from the event and fill the fBegin
    void beginEvent(const edm::Event&, const edm::EventSetup&);

    void setSelectedTau(const edm::Ptr<pat::Tau>& tau);

    // Fill the rest of the histogram sets
    void fillAfterTauId();
    void fillAfterMetCut();
    void fillAfterBTagging();
    void fillAfterFakeMetVeto();

    // just to provide the method and do nothing, I'm lazy to fix AlphatAnalysis, Matti 2011-06-03
    void fillEnd() {}

    bool isEmbeddingInput() const {
      return fEmbeddingMode;
    }

  private:
    edm::InputTag fOriginalMetSrc;
    edm::InputTag fEmbeddingMetSrc;
    edm::InputTag fOriginalMuonSrc;

    bool fEmbeddingMode;

    // EventWeight object
    EventWeight& fEventWeight;

    // Histogram sets
    Histograms fBegin;
    Histograms fAfterTauId;
    Histograms fAfterMetCut;
    Histograms fAfterBTagging;
    Histograms fAfterFakeMetVeto;

    // Holders of the objects
    edm::Ptr<reco::MET> fOriginalMet;
    edm::Ptr<reco::MET> fEmbeddingMet;
    edm::Ptr<pat::Tau> fSelectedTau;
    edm::Ptr<reco::Muon> fOriginalMuon;

  };
}


#endif
