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
     * 
     * Note: There might be multiple selected taus in the event.
     *       In that case, the first in the list is the selected tau
     *       in the event (the most isolated).
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data(const TauSelection *tauSelection, bool passedEvent);
      ~Data();
      /// Returns true, if the selected tau has passed all selections
      bool passedEvent() const { return fPassedEvent; }
      /// Returns list of selected taus (i.e. taus after tau candidate selection or after full tau ID); Note: list can be empty if no tau was selected
      const edm::PtrVector<pat::Tau>& getSelectedTaus() const;
      /// Returns selected tau in the event (i.e. tau after tau candidate selection or after full tau ID); Note: list can be empty if no tau was selected
      const edm::Ptr<pat::Tau> getSelectedTau() const;
      /// Returns the number of prongs of the selected tau
      const size_t getNProngsOfSelectedTau() const;
      /// Returns the number of prongs of the selected tau
      const double getRtauOfSelectedTau() const;
      /// Returns true if the selected tau passes the isolation criteria
      const bool selectedTauPassesIsolation() const;
      /// Returns true if the selected tau passes the nprongs cut
      const bool selectedTauPassesNProngs() const;
      /// Returns true if the selected tau passes the rtau cut
      const bool selectedTauPassesRtau() const;
      /// Returns true if the selected tau passes the isolation, Nprongs, and the Rtau cuts
      const bool selectedTauPassesFullTauID() const { return selectedTauPassesIsolation() && selectedTauPassesNProngs() && selectedTauPassesRtau(); }
      /// Returns true if no candidates pass isolation
      const bool selectedTausDoNotPassIsolation() const;
      /// Returns true if the selected tau passes a specified discriminator
      const bool selectedTauPassesDiscriminator(std::string discr, double cutPoint) const;
      
    private:
      const TauSelection *fTauSelection;
      bool fPassedEvent; // non-const because need to be set from TauSelectionFactorized via setSelectedTau(...)
    };

    enum TauSelectionOperationMode {
      kNormalTauID, // Tau candidate selection + tau ID selections
      kTauCandidateSelectionOnly // Only tau candidate selection is applied
    };

    TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label = "TauSelection");
    ~TauSelection();

    /// Default tauID
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// tau ID on a given sample of taus
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// Trigger tau selection - find best unique tau candidate
    // Data analyzeTriggerTau(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// tau ID on cleaned tau candidates
    Data analyzeTauIDWithoutRtauOnSelectedTauCandidates(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> tauCandidate);
    /// tau ID on selected tau candidates - to be applied after analyzeTauIDWithoutRtauOnSelectedTauCandidates
    //Data analyzeTauIDWithRtauOnSelectedTauCandidates(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// Method for setting selected tau (from factorization)
    Data setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passedEvent);
    /// Method for getting operating mode (needed for tau specific weight maps)
    const TauSelectionOperationMode getOperationMode() const { return fOperationMode; }

  private:
    /// Method for doing tau selection
    bool doTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);
    /// Method for handling the result of tauID factorization
    bool doFactorizationLookup();
    // Internal histogramming routines
    /// Fills the histogram that describes the mode in which the tau selection was run
    void fillOperationModeHistogram();

    void fillHistogramsForTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    void fillHistogramsForSelectedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    void fillHistogramsForSelectedTaus(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    void ObtainMCPurity(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent, TH1* histogram);
    //void findBestTau(edm::PtrVector<pat::Tau>& bestTau, edm::PtrVector<pat::Tau>& taus);

  private:
    // Input parameters
    edm::InputTag fSrc;
    const std::string fSelection;

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
    TH1 *hPtSelectedTauCandidates; // Cleaned tau candidates == taus after jet et, jet eta, ldg pt, e/mu veto 
    TH1 *hPtSelectedTaus; // Selected taus == after all tauID cuts
    TH1 *hEtaTauCandidates;
    TH1 *hEtaSelectedTauCandidates;
    TH1 *hEtaSelectedTaus;

    TH2 *hEtaPhiTauCandidates;
    TH2 *hEtaPhiSelectedTauCandidates;
    TH2 *hEtaPhiSelectedTaus;

    TH1 *hPhiTauCandidates;
    TH1 *hPhiSelectedTauCandidates;
    TH1 *hPhiSelectedTaus;
    TH1 *hNumberOfTauCandidates;
    TH1 *hNumberOfSelectedTauCandidates;
    TH1 *hNumberOfSelectedTaus;
    TH1 *hMCPurityOfTauCandidates;
    TH1 *hMCPurityOfSelectedTauCandidates;
    TH1 *hMCPurityOfSelectedTaus;

    TH1 *hNTriggerMatchedTaus;
    TH1 *hNTriggerMatchedSeparateTaus;

    TH1 *hIsolationPFChargedHadrCandsPtSum;
    TH1 *hIsolationPFGammaCandsEtSum;

    TH1 *hTightChargedMaxPtBeforeIsolation;
    TH1 *hTightChargedSumPtBeforeIsolation;
    TH1 *hTightChargedOccupancyBeforeIsolation;
    TH1 *hTightGammaMaxPtBeforeIsolation;
    TH1 *hTightGammaSumPtBeforeIsolation;
    TH1 *hTightGammaOccupancyBeforeIsolation;
    TH1 *hTightChargedMaxPtAfterIsolation;
    TH1 *hTightChargedSumPtAfterIsolation;
    TH1 *hTightChargedOccupancyAfterIsolation;
    TH1 *hTightGammaMaxPtAfterIsolation;
    TH1 *hTightGammaSumPtAfterIsolation;
    TH1 *hTightGammaOccupancyAfterIsolation;
    TH1 *hHPSDecayMode;

    TH1 *hVLooseIsoNcands;
    TH1 *hLooseIsoNcands;
    TH1 *hMediumIsoNcands;
    TH1 *hTightIsoNcands;

    // Selected tau
    edm::PtrVector<pat::Tau> fSelectedTauCandidates;
    edm::PtrVector<pat::Tau> fSelectedTaus;
  };
}

#endif
