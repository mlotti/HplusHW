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

    const edm::PtrVector<pat::Tau>& getSelectedTaus() const {
      return fSelectedTaus;
    }

  private:
    // Input parameters
    edm::InputTag fSrc;
    double fPtCut;
    double fEtaCut;
    double fLeadTrkPtCut;
    double fRtauCut;
    double fInvMassCut;

    // Counters
    Count fPtCutCount;
    Count fEtaCutCount;
    Count fagainstMuonCount;
    Count fagainstElectronCount;
    Count fLeadTrkPtCount;
    Count fnProngsCount;
    Count fHChTauIDchargeCount;
    Count fbyIsolationCount;
    Count fbyTrackIsolationCount;  
    Count fecalIsolationCount; 
    Count fRtauCount;
    Count fInvMassCount;

    Count fAllSubCount;
    Count fPtCutSubCount;
    Count fEtaCutSubCount;
    Count fagainstMuonSubCount;
    Count fagainstElectronSubCount;
    Count fLeadTrkPtSubCount;
    Count fnProngsSubCount;
    Count fHChTauIDchargeSubCount;
    Count fbyIsolationSubCount; 
    Count fbyTrackIsolationSubCount; 
    Count fecalIsolationSubCount; 
    Count fRtauSubCount;
    Count fInvMassSubCount;

    // Histograms
    TH1 *hPt;
    TH1 *hEta;
    TH1 *hEtaRtau;
    TH1 *hLeadTrkPt;
    TH1 *hIsolTrkPt;
    TH1 *hIsolTrkPtSum;
    TH1 *hIsolMaxTrkPt;
    TH1 *hnProngs;
    TH1 *hDeltaE;
    TH1 *hRtau;
    TH1 *hlightPathSignif;
    TH1 *hInvMass;


    // Selected tau
    edm::PtrVector<pat::Tau> fSelectedTaus;
  };
}

#endif
