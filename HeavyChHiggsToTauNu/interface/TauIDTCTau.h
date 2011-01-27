// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauIDTCTau_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauIDTCTau_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDBase.h"

namespace HPlus {
  class TauIDTCTau : public TauIDBase {
   public:
    /**
     * Implementation of the TCTau tau ID functionality
     */
    TauIDTCTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TauIDTCTau();

//    /// Returns true, if the tau candidate conditions are fulfilled (jet et, eta, ldg pt, e/mu veto) 
    bool passLeadingTrackCuts(pat::Tau& tau);
    bool passIsolation(pat::Tau& tau);
    bool passAntiIsolation(pat::Tau& tau);
    bool passRTauCut(pat::Tau& tau);
    bool passAntiRTauCut(pat::Tau& tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDIsolation;
  };
}

#endif
