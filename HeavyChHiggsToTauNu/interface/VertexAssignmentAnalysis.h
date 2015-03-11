// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexAssignmentAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexAssignmentAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class VertexAssignmentAnalysis: public BaseSelection {
  public:
    VertexAssignmentAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~VertexAssignmentAnalysis();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    void silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch);
    /// Analyses the compatibility of the tau and the primary vertex
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch);

  private:
    void privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch);

    FakeTauIdentifier fFakeTauIdentifier;

    Count fAllEventsWithGenuineTaus;
    Count fGenuineTausWithCorrectPV;
    Count fAllEventsWithFakeTaus;
    Count fFakeTausWithCorrectPV;

    edm::Ptr<reco::Vertex> fSelectedVertex;
    // histograms
    WrappedTH1* hGenuineTauAllEventsByTauZ;
    WrappedTH1* hGenuineTauPassedEventsByTauZ;
    WrappedTH1* hGenuineTauAllEventsByPt;
    WrappedTH1* hGenuineTauPassedEventsByPt;
    WrappedTH1* hGenuineTauAllEventsByEta;
    WrappedTH1* hGenuineTauPassedEventsByEta;
    WrappedTH1* hGenuineTauAllEventsByPhi;
    WrappedTH1* hGenuineTauPassedEventsByPhi;
    WrappedTH1* hFakeTauAllEventsByTauZ;
    WrappedTH1* hFakeTauPassedEventsByTauZ;
    WrappedTH1* hFakeTauAllEventsByPt;
    WrappedTH1* hFakeTauPassedEventsByPt;
    WrappedTH1* hFakeTauAllEventsByEta;
    WrappedTH1* hFakeTauPassedEventsByEta;
    WrappedTH1* hFakeTauAllEventsByPhi;
    WrappedTH1* hFakeTauPassedEventsByPhi;
  };
}

#endif
