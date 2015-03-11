// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class EventCounter;
  class HistoWrapper;

  class VertexSelection: public BaseSelection {
  public:
    class Data {
    public:
      Data();
      ~Data();

      const bool passedEvent() const { return fPassedEvent; }
      const edm::Ptr<reco::Vertex>& getSelectedVertex() const { return fSelectedVertex; }
      size_t getNumberOfAllVertices() const { return fNumberOfAllVertices; }
      double getTrackSumPt() const { return fSumPt; }

      friend class VertexSelection;

    private:
      bool fPassedEvent;
      edm::Ptr<reco::Vertex> fSelectedVertex;
      double fSumPt;
      size_t fNumberOfAllVertices;
    };

    VertexSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~VertexSelection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    const edm::InputTag getSelectedSrc() const {
      return fSelectedSrc;
    }
    const edm::InputTag getAllSrc() const {
      return fAllSrc;
    }

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
    edm::InputTag fSelectedSrc;
    edm::InputTag fAllSrc;
    edm::InputTag fSumPtSrc;
    bool fEnabled;
  };
}

#endif
