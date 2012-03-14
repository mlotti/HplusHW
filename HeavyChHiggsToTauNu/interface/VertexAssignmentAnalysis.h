// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexAssignmentAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexAssignmentAnalysis_h

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

class TH1;

namespace HPlus {
  class VertexAssignmentAnalysis {
  public:
    VertexAssignmentAnalysis(EventCounter& eventCounter, EventWeight& eventWeight);
    ~VertexAssignmentAnalysis();

    /// Analyses the compatibility of the tau and the primary vertex
    void analyze(bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch);

  private:
    FakeTauIdentifier fFakeTauIdentifier;
    
    EventWeight& fEventWeight;

    Count fAllEventsWithGenuineTaus;
    Count fGenuineTausWithCorrectPV;
    Count fAllEventsWithFakeTaus;
    Count fFakeTausWithCorrectPV;
    
    edm::Ptr<reco::Vertex> fSelectedVertex;
    // histograms
    TH1* hGenuineTauAllEventsByTauZ;
    TH1* hGenuineTauPassedEventsByTauZ;
    TH1* hGenuineTauAllEventsByPt;
    TH1* hGenuineTauPassedEventsByPt;
    TH1* hGenuineTauAllEventsByEta;
    TH1* hGenuineTauPassedEventsByEta;
    TH1* hGenuineTauAllEventsByPhi;
    TH1* hGenuineTauPassedEventsByPhi;
    TH1* hFakeTauAllEventsByTauZ;
    TH1* hFakeTauPassedEventsByTauZ;
    TH1* hFakeTauAllEventsByPt;
    TH1* hFakeTauPassedEventsByPt;
    TH1* hFakeTauAllEventsByEta;
    TH1* hFakeTauPassedEventsByEta;
    TH1* hFakeTauAllEventsByPhi;
    TH1* hFakeTauPassedEventsByPhi;
    
    
    
  };
}

#endif
