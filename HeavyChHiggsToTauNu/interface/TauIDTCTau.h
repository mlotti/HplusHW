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
    TauIDTCTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label, TFileDirectory& myDir);
    ~TauIDTCTau();

//    /// Returns true, if the tau candidate conditions are fulfilled (jet et, eta, ldg pt, e/mu veto) 
    bool passDecayModeFinding(const edm::Ptr<pat::Tau>& tau);
    bool passLeadingTrackCuts(const edm::Ptr<pat::Tau> tau);
    bool passNProngsCut(const edm::Ptr<pat::Tau> tau);
    size_t getNProngs(const edm::Ptr<pat::Tau> tau) const;
    bool passRTauCut(const edm::Ptr<pat::Tau> tau);
    double getRtauValue(const edm::Ptr<pat::Tau> tau) const;

  private:
  };
}

#endif
