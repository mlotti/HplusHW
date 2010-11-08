// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
#include "TH2.h"

namespace HPlus {
  class TauSelection {
  public:
    enum TauIDTypeEnumerator {
      kTauIDCaloTauCutBased,
      kTauIDShrinkingConePFTauCutBased,
      kTauIDShrinkingConePFTauTaNCBased,
      kTauIDHPSTauBased
    };

    /**
     * Class to encapsulate the access to the data members of
     * TauSelection. If you want to add a new accessor, add it here
     * and keep all the data of TauSelection private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data(const TauSelection *tauSelection, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }

      const edm::PtrVector<pat::Tau>& getSelectedTaus() const {
        return fTauSelection->fSelectedTaus;
      }

    private:
      const TauSelection *fTauSelection;
      bool fPassedEvent; // non-const because need to be set from TauSelectionFactorized via setSelectedTau(...)
    };

    TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TauSelection();

    /// Default tauID
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// tau ID on a given sample of taus 
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Handle<edm::View<pat::Tau> >& taus);
    /// Method for setting selected tau (from factorization)
    Data setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passedEvent);

  private:
    bool selectionByTCTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Handle<edm::View<pat::Tau> >& taus);
    bool selectionByPFTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Handle<edm::View<pat::Tau> >& taus);
    bool selectionByPFTauTaNC(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Handle<edm::View<pat::Tau> >& taus);
    bool selectionByHPSTau(const edm::Event& iEvent, const edm::EventSetup& iSetup,
    edm::Handle<edm::View<pat::Tau> >& taus);


    // Input parameters
    edm::InputTag fSrc;
    const std::string fSelection;
    const double fPtCut;
    const double fEtaCut;
    const double fLeadTrkPtCut;
    const double fRtauCut;
    const double fInvMassCut;
    TauIDTypeEnumerator fTauIDType;

    // Counters
    Count fPtCutCount;
    Count fEtaCutCount;
    Count fagainstMuonCount;
    Count fagainstElectronCount;
    Count fLeadTrkPtCount;
    Count fTaNCCount;
    Count fHPSIsolationCount;
    Count fbyIsolationCount;
    Count fbyTrackIsolationCount;  
    Count fecalIsolationCount; 
    Count fnProngsCount;
    Count fHChTauIDchargeCount;
    Count fRtauCount;
    Count fInvMassCount;

    Count fAllSubCount;
    Count fPtCutSubCount;
    Count fEtaCutSubCount;
    Count fagainstMuonSubCount;
    Count fagainstElectronSubCount;
    Count fLeadTrkPtSubCount;
    Count fbyTaNCSubCount;
    Count fbyHPSIsolationSubCount;
    Count fbyIsolationSubCount; 
    Count fbyTrackIsolationSubCount; 
    Count fecalIsolationSubCount; 
    Count fnProngsSubCount;
    Count fHChTauIDchargeSubCount;
    Count fRtauSubCount;
    Count fInvMassSubCount;

    // EventWeight object
    EventWeight& fEventWeight;

    // Histograms
    TH1 *hPt;
    TH1 *hEta;
    TH1 *hPtAfterTauSelCuts;
    TH1 *hEtaAfterTauSelCuts;
    TH1 *hEtaRtau;
    TH1 *hLeadTrkPt;
    TH1 *hIsolTrkPt;
    TH1 *hIsolTrkPtSum;
    TH2 *hIsolTrkPtSumVsPtCut;
    TH2 *hNIsolTrksVsPtCut;
    TH1 *hIsolMaxTrkPt;
    TH1 *hnProngs;
    TH1 *hDeltaE;
    TH1 *hRtau;
    TH1 *hFlightPathSignif;
    TH1 *hInvMass;
    TH1 *hbyTaNC;

    // Selected tau
    edm::PtrVector<pat::Tau> fSelectedTaus;
  };
}

#endif
