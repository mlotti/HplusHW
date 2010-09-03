// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class JetSelection {
  public:
    JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~JetSelection();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);

    const edm::PtrVector<pat::Jet>& getSelectedJets() const {
      return fSelectedJets;
    }

  private:
    // Input parameters
    edm::InputTag fSrc;
    double fPtCut;
    double fEtaCut;
    double fMaxDR;
    uint32_t fMin;

    // Counters
    Count fCleanCutCount;
    Count fPtCutCount;
    Count fEtaCutCount;

    Count fAllSubCount;
    Count fCleanCutSubCount;
    Count fPtCutSubCount;
    Count fEtaCutSubCount;

    // Histograms
    TH1 *hPt;
    TH1 *hEta;

    // Selected jets
    edm::PtrVector<pat::Jet> fSelectedJets;
  };
}

#endif
