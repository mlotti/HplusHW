// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleAnalysis_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class   GenParticleAnalysis {
  public:
    GenParticleAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    GenParticleAnalysis(EventCounter& eventCounter, EventWeight& eventWeight);
    ~GenParticleAnalysis();

    void analyze(const edm::Event&, const edm::EventSetup&);
  
  private:
    void init();
    
    // EventWeight object
    EventWeight& fEventWeight;
    //    edm::InputTag fSrc;
    //   const double fPtCut;
    //   const double fEtaCut;
    
    // Histograms
    TH1 *hHpMass;
    TH1 *hTauStatus;
    TH1 *hRtau1pHp;
    TH1 *hRtau13pHp;
    TH1 *hRtau3pHp;
    TH1 *hRtau1pW;
    TH1 *hRtau13pW;
    TH1 *hRtau3pW;
    TH1 *hptVisibleTau1pHp;
    TH1 *hptVisibleTau13pHp;
    TH1 *hptVisibleTau3pHp;
    TH1 *hptVisibleTau1pW;
    TH1 *hptVisibleTau13pW;
    TH1 *hptVisibleTau3pW;
    TH1 *hLeadingTrack1pHp;
    TH1 *hLeadingTrack1pW;
    TH1 *hEtaVisibleTau1pHp;
    TH1 *hEtaVisibleTau1pW;
    TH1 *hTauMass1pHp;
    TH1 *hTauMass1pW;
    TH1 *hThetaCM1pHp;
    TH1 *hThetaCM1pW;
    TH1 *hMagCM1pHp;
    TH1 *hMagCM1pW;	 
  };
}

#endif
