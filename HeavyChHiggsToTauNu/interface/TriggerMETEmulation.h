// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerMETEmulation_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerMETEmulation_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class TriggerMETEmulation {
  public:
    TriggerMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~TriggerMETEmulation();

    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    const edm::Ptr<reco::MET> getSelectedMET() const {
      return fSelectedTriggerMET;
    }

  private:
    // Input parameters
    edm::InputTag fSrc;
    double fmetEmulationCut;

    // Counters
    Count fmetEmulationCutCount;

    // Histograms
    TH1 *hmetAfterTrigger;

    // Selected jets
    edm::Ptr<reco::MET> fSelectedTriggerMET;
  };
}

#endif
