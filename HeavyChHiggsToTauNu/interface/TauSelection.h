// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDBase.h"

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
      const edm::PtrVector<pat::Tau>& getCleanedTauCandidates() const {
        return fTauSelection->fCleanedTauCandidates;
      }
      double getRtauOfSelectedTau() const {
        return fTauSelection->getSelectedRtauValue();
      }
      bool selectedTauPassedRtau() const {
        if (!fTauSelection->fSelectedTaus.size()) return false;
        return fTauSelection->fTauID->passRTauCut(fTauSelection->fSelectedTaus[0]);
      }
      bool selectedTauCandidatePassedRtau() const {
        if (!fTauSelection->fCleanedTauCandidates.size()) return false;
        return fTauSelection->fTauID->passRTauCut(fTauSelection->fCleanedTauCandidates[0]);
      }

    private:
      const TauSelection *fTauSelection;
      bool fPassedEvent; // non-const because need to be set from TauSelectionFactorized via setSelectedTau(...)
    };

    enum TauSelectionOperationMode {
      kNormalTauID, // Tau candidate selection + tau ID selections
      kTauCandidateSelectionOnly, // Only tau candidate selection is applied
      kTauIDWithoutRtauOnly, // For QCD bkg measurement - set internally
      kTauIDWithRtauOnly // For QCD bkg measurement - set internally
    };

    TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongNumber, std::string label);
    ~TauSelection();

    /// Default tauID
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// tau ID on a given sample of taus 
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// tau ID on cleaned tau candidates
    Data analyzeTauIDWithoutRtauOnCleanedTauCandidates(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// tau ID on selected tau candidates - to be applied after analyzeTauIDWithoutRtauOnCleanedTauCandidates
    //Data analyzeTauIDWithRtauOnCleanedTauCandidates(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// Method for setting selected tau (from factorization)
    Data setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passedEvent);
    /// Method for getting operating mode (needed for tau specific weight maps)
    TauSelectionOperationMode getOperationMode() const { return fOperationMode; }

  private:
    /// Method for doing tau selection
    bool doTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// Method for handling the result of tauID factorization 
    bool doFactorizationLookup();
    // Internal histogramming routines
    /// Fills the histogram that describes the mode in which the tau selection was run
    void fillOperationModeHistogram();

    void fillHistogramsForTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    void fillHistogramsForCleanedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    void fillHistogramsForSelectedTaus(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    void ObtainMCPurity(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent, TH1* histogram);

    double getSelectedRtauValue() const {
      if (fSelectedTaus.size())
        return fTauID->getRtauValue(fSelectedTaus[0]);
      else
        return -1.0; // safety
    }

  private:
    // Input parameters
    edm::InputTag fSrc;
    const std::string fSelection;
    const int fProngNumber;
    const std::string fLabel;

    /// TauID object
    TauIDBase* fTauID;
    /// Operation mode of tau selection
    TauSelectionOperationMode fOperationMode;

    /// Factorization table objects

    // Counters
    Count fTauFound;

    // EventWeight object
    EventWeight& fEventWeight;

    // Histograms
    TH1 *hTauIdOperatingMode;
    TH1 *hPtTauCandidates; // Tau candidates == all taus in the pat::Tau collection
    TH1 *hPtCleanedTauCandidates; // Cleaned tau candidates == taus after jet et, jet eta, ldg pt, e/mu veto 
    TH1 *hPtSelectedTaus; // Selected taus == after all tauID cuts
    TH1 *hEtaTauCandidates;
    TH1 *hEtaCleanedTauCandidates;
    TH1 *hEtaSelectedTaus;

    TH2 *hEtaPhiTauCandidates;
    TH2 *hEtaPhiCleanedTauCandidates;
    TH2 *hEtaPhiSelectedTaus;

    TH1 *hPhiTauCandidates;
    TH1 *hPhiCleanedTauCandidates;
    TH1 *hPhiSelectedTaus;
    TH1 *hNumberOfTauCandidates;
    TH1 *hNumberOfCleanedTauCandidates;
    TH1 *hNumberOfSelectedTaus;
    TH1 *hMCPurityOfTauCandidates;
    TH1 *hMCPurityOfCleanedTauCandidates;
    TH1 *hMCPurityOfSelectedTaus;

    TH1 *hVLooseIsoNcands;
    TH1 *hLooseIsoNcands;
    TH1 *hMediumIsoNcands;
    TH1 *hTightIsoNcands;

    // Selected tau
    edm::PtrVector<pat::Tau> fCleanedTauCandidates;
    edm::PtrVector<pat::Tau> fSelectedTaus;
  };
}

#endif
