// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GenParticleAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  
  class GenParticleAnalysis: public BaseSelection {
  public:
    class Data {
    public:
      Data();
      ~Data();

      void check() const;

      const edm::Ptr<reco::GenMET>& getGenMET() const {
	check();
        return fGenMet;
      }

      friend class GenParticleAnalysis;

    private:
      edm::Ptr<reco::GenMET> fGenMet;
    };

    GenParticleAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~GenParticleAnalysis();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event&, const edm::EventSetup&);
    Data analyze(const edm::Event&, const edm::EventSetup&);

    // edm::PtrVector<const reco::Candidate*> doQCDmAnalysis(const edm::Event&, const edm::EventSetup&); //doesn't work
    std::vector<const reco::Candidate*> doQCDmAnalysis(const edm::Event&, const edm::EventSetup&); // works
    // double doQCDmAnalysis(const edm::Event&, const edm::EventSetup&); // works

  private:
    Data privateAnalyze(const edm::Event&, const edm::EventSetup&);

    void init(HistoWrapper& histoWrapper);
    /*
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
    */

    edm::InputTag fSrc;
    edm::InputTag fMetSrc;
    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;
    edm::InputTag fThreeProngTauSrc;

    // Histograms
    WrappedTH1 *hHpMass;
    WrappedTH1 *hTauStatus;
    WrappedTH1 *hRtau1pHp;
    WrappedTH1 *hRtau13pHp;
    WrappedTH1 *hRtau3pHp;
    WrappedTH1 *hRtau1pW;
    WrappedTH1 *hRtau13pW;
    WrappedTH1 *hRtau3pW;
    WrappedTH1 *hptVisibleTau1pHp;
    WrappedTH1 *hptVisibleTau13pHp;
    WrappedTH1 *hptVisibleTau3pHp;
    WrappedTH1 *hptVisibleTau1pW;
    WrappedTH1 *hptVisibleTau13pW;
    WrappedTH1 *hptVisibleTau3pW;
    WrappedTH1 *hLeadingTrack1pHp;
    WrappedTH1 *hLeadingTrack1pW;
    WrappedTH1 *hEtaVisibleTau1pHp;
    WrappedTH1 *hEtaVisibleTau1pW;
    WrappedTH1 *hTauMass1pHp;
    WrappedTH1 *hTauMass1pW;
    WrappedTH1 *hThetaCM1pHp;
    WrappedTH1 *hThetaCM1pW;
    WrappedTH1 *hMagCM1pHp;
    WrappedTH1 *hMagCM1pW;	 
    WrappedTH1 *hBquarkMultiplicity;
    WrappedTH1 *hBquarkStatus2Multiplicity;
    WrappedTH1 *hBquarkStatus3Multiplicity;
    WrappedTH1 *hBquarkFromTopEta;
    WrappedTH1 *hBquarkNotFromTopEta;
    WrappedTH1 *hBquarkFromTopPt;
    WrappedTH1 *hBquarkNotFromTopPt;
    WrappedTH1 *hBquarkFromTopEtaPtCut;
    WrappedTH1 *hBquarkNotFromTopEtaPtCut;
    WrappedTH1 *hBquarkFromTopPtEtaCut;
    WrappedTH1 *hBquarkNotFromTopPtEtaCut;
    WrappedTH1 *hBquarkFromTopDeltaRTau;
    WrappedTH1 *hBquarkNotFromTopDeltaRTau;
    WrappedTH1 *hGenBquarkFromHiggsSideEta;
    WrappedTH1 *hGenBquarkFromHiggsSidePt;
    WrappedTH1 *hGenDeltaRHiggsSide;
    WrappedTH1 *hGenBquarkFromTopSideEta;
    WrappedTH1 *hGenBquarkFromTopSidePt;
    WrappedTH1 *hGenDeltaRTopSide;
    WrappedTH1 *hTopPt;
    WrappedTH1 *hTopPt_wrongB;
    WrappedTH1 *hGenMET;
    WrappedTH1 *hWPt;
    WrappedTH1 *hWEta;
    WrappedTH1 *hWPhi;

  };
}

#endif
