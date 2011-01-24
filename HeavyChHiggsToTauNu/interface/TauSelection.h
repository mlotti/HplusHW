// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectionCounterPackager.h"

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
      kTauIDHPSTauBased,
      kTauIDCombinedHPSTaNCTauBased
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
      const edm::PtrVector<pat::Tau>& getSelectedAntiTaus() const {
        return fTauSelection->fSelectedAntiTaus;
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
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// Method for setting selected tau (from factorization)
    Data setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passedEvent);
    /// Method for obtaining the tau ID algorithm type
    TauIDTypeEnumerator getTauIDType() const { return fTauIDType; }

    // Setters for options
    /// Disables the cut on the number of signal tracks
    void disableProngCut() { fApplyProngCutStatus = true; }
    /// Sets the tau ID to work as an anti-tau tagger (passed is true, if no tau candidates are identified as taus)   
    void setToAntiTaggingMode() { fAntiTagModeStatus = true; }
    /// Sets the tau ID to work as an anti-tau tagger (passed is true, if no tau candidates are isolated; ET and eta cuts are applied)   
    void setToAntiTaggingModeIsolationOnly() { fAntiTagModeIsolationOnlyStatus = true; }

  private:
    /// TauID specific to TCTau
    bool selectionByTCTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// TauID specific to PF shrinking cone tau
    bool selectionByPFTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// TauID specific to TaNC (neural network on top of PF shrinking cone tau)
    bool selectionByPFTauTaNCCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, const 
    edm::PtrVector<pat::Tau>& taus);
    /// TauID specific to HPS (Hadron+strips algorithm on top of PF shrinking cone tau)
    bool selectionByHPSTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// TauID specific to combined HPS+TaNC algorithms
    bool selectionByCombinedHPSTaNCTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);

    // Input parameters
    edm::InputTag fSrc;
    const std::string fSelection;
    const double fPtCut;
    const double fEtaCut;
    const double fLeadTrkPtCut;
    const double fRtauCut;
    const double fInvMassCut;
    TauIDTypeEnumerator fTauIDType;
    
    // Options
    /// If true (true=default), the cut on the number of signal tracks is applied
    bool fApplyProngCutStatus;
    /// If true (false=default), anti-tau tagging is applied (all cuts except ET and eta)
    bool fAntiTagModeStatus;
    /// If true (false=default), anti-tau tagging is applied (isolation only; ET and eta cuts are applied)
    bool fAntiTagModeIsolationOnlyStatus;
       
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

    // Subcounters packaged in one object
    SelectionCounterPackager* fSubCounters;
    
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
    TH1 *hTauIdOperatingMode;

    // Selected tau
    edm::PtrVector<pat::Tau> fSelectedTaus;
    edm::PtrVector<pat::Tau> fSelectedAntiTaus;
  };
}

#endif
