// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingMuonIsolationQuantifier_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingMuonIsolationQuantifier_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class TauEmbeddingMuonIsolationQuantifier {
  public:
    //TauEmbeddingMuonIsolationQuantifier(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    TauEmbeddingMuonIsolationQuantifier(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~TauEmbeddingMuonIsolationQuantifier();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    //    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus);
    void analyzeAfterTrigger(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    void analyzeAfterJets(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    //    Data  analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau);
    //    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau);
    //    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus);

  private:
    double getTotalIsolationPt(double charged, double gamma, double puCharged, double k);
    double getMaxK(double charged, double gamma, double puCharged);
    // Input parameters
    //edm::InputTag fSrc;


    // Histograms
    WrappedTH1 *hChargedIsoPtSum;
    WrappedTH1 *hGammaIsoPtSum;
    WrappedTH1 *hChargedPUIsoPtSum;
    WrappedTH1 *hTotalIsoPtSum;
    WrappedTH1 *hKParam;
    WrappedTH1 *hChargedIsoPtSumAfterJets;
    WrappedTH1 *hKParamAfterJets;
    WrappedTH1 *hTotalIsoPtSumAfterJets;
  };
}

#endif
