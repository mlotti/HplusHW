// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauIDPFTauBase_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauIDPFTauBase_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDBase.h"

namespace HPlus {
  class TauIDPFTauBase : public TauIDBase {
  public:

    /**
     * Base class for PF tau ID operations.
     * Actual tau ID specific classes are inherited from this class.
     */
    TauIDPFTauBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, const std::string& baseLabel);
    ~TauIDPFTauBase();

    /// Returns true, if the tau candidate conditions are fulfilled (jet et, eta, ldg pt, e/mu veto) 
    bool passLeadingTrackCuts(pat::Tau& tau);
    virtual bool passIsolation(pat::Tau& tau) = 0;
    virtual bool passAntiIsolation(pat::Tau& tau) = 0;
    bool passRTauCut(pat::Tau& tau);
    bool passAntiRTauCut(pat::Tau& tau);

  protected:
    // Tau ID selections concerning isolation (track, ECAL) are implemented in the specific tau ID classes

  };
}

#endif
