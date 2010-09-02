// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class TauSelection {
  public:
    TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~TauSelection();

    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    const edm::Ptr<pat::Tau> getSelectedTau() const {
      return fSelectedTau;
    }

  private:
    // Input parameters
    edm::InputTag fSrc;
    double fPtCut;
    double fEtaCut;
    double fLeadTrkPtCut;

    // Counters
    Count fPtCutCount;
    Count fEtaCutCount;
    Count fLeadTrkPtCount;

    Count fAllSubCount;
    Count fPtCutSubCount;
    Count fEtaCutSubCount;
    Count fLeadTrkPtSubCount;

    // Histograms
    TH1 *hPt;
    TH1 *hEta;
    TH1 *hLeadTrkPt;

    // Selected tau
    edm::Ptr<pat::Tau> fSelectedTau;
  };
}

#endif
