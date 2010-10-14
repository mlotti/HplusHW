// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h

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
  class METSelection {
  public:
    METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~METSelection();

    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    const edm::Ptr<reco::MET> getSelectedMET() const {
      return fSelectedMET;
    }
    // Variables
    float fMet;

  private:
    // Input parameters
    edm::InputTag fSrc;
    double fMetCut;

    // Counters
    Count fMetCutCount;

    // Histograms
    TH1 *hMet;

    // Selected jets
    edm::Ptr<reco::MET> fSelectedMET;
  };
}

#endif
