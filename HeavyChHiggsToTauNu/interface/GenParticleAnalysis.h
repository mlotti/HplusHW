// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleAnalysis_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
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
    ~GenParticleAnalysis();

    void analyze(const edm::Event&, const edm::EventSetup&);
    // edm::PtrVector<const reco::Candidate*> doQCDmAnalysis(const edm::Event&, const edm::EventSetup&); //doesn't work
    std::vector<const reco::Candidate*> doQCDmAnalysis(const edm::Event&, const edm::EventSetup&); // works
    // double doQCDmAnalysis(const edm::Event&, const edm::EventSetup&); // works

  private:
    void init();
    std::vector<const reco::GenParticle*> getImmediateMothers(const reco::Candidate&);
    std::vector<const reco::GenParticle*> getMothers(const reco::Candidate&);
    bool hasImmediateMother(const reco::Candidate&, int);
    bool hasMother(const reco::Candidate&, int);
    void printImmediateMothers(const reco::Candidate& );
    void printMothers(const reco::Candidate& );
    std::vector<const reco::GenParticle*> getImmediateDaughters(const reco::Candidate&);
    std::vector<const reco::GenParticle*> getDaughters(const reco::Candidate&);
    bool hasImmediateDaughter(const reco::Candidate&, int);
    bool hasDaughter(const reco::Candidate&, int);
    void printImmediateDaughters(const reco::Candidate& );
    void printDaughters(const reco::Candidate& );
    
    // EventWeight object
    EventWeight& fEventWeight;
    edm::InputTag fSrc;
    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;
    edm::InputTag fThreeProngTauSrc;
    
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
    TH1 *hBquarkMultiplicity;
    TH1 *hBquarkStatus2Multiplicity;
    TH1 *hBquarkStatus3Multiplicity;
    TH1 *hBquarkFromTopEta;
    TH1 *hBquarkNotFromTopEta;
    TH1 *hBquarkFromTopPt;
    TH1 *hBquarkNotFromTopPt;
    TH1 *hBquarkFromTopDeltaRTau;
    TH1 *hBquarkNotFromTopDeltaRTau;
    TH1 *hTopPt;
    TH1 *hTopPt_wrongB;
  };
}

#endif
