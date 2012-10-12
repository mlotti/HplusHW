// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

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
      /// Returns true if the selected tau passes NProngs and Rtau but not isolation
      const bool selectedTauPassesNProngsAndRtauButNotIsolation() const;
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

    TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string label = "TauSelection");
    ~TauSelection();

    edm::InputTag getSrc() const { return fSrc; }

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
    /// Fill eta-phi histograms of fake taus (Note: do not use in final analysis, because it will fill multiple times counters and histograms)
    void analyseFakeTauComposition(FakeTauIdentifier& fakeTauIdentifier, const edm::Event& iEvent);

    // Select the pat::Tau object which most likely passes the tau candidate selection + ID
    const edm::Ptr<pat::Tau> selectMostLikelyTau(const edm::PtrVector<pat::Tau>& taus);

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
    void ObtainMCPurity(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent, WrappedTH1* histogram);
    //void findBestTau(edm::PtrVector<pat::Tau>& bestTau, edm::PtrVector<pat::Tau>& taus);

  private:
    // Input parameters
    edm::InputTag fSrc;
    const std::string fSelection;
    const bool fAnalyseFakeTauComposition;

    /// TauID object
    TauIDBase* fTauID;
    /// Operation mode of tau selection
    TauSelectionOperationMode fOperationMode;

    /// Factorization table objects

    // Counters
    Count fTauFound;

    // Histograms
    WrappedTH1 *hTauIdOperatingMode;
    WrappedTH1 *hPtTauCandidates; // Tau candidates == all taus in the pat::Tau collection
    WrappedTH1 *hPtSelectedTauCandidates; // Cleaned tau candidates == taus after jet et, jet eta, ldg pt, e/mu veto 
    WrappedTH1 *hPtSelectedTaus; // Selected taus == after all tauID cuts
    WrappedTH1 *hEtaTauCandidates;
    WrappedTH1 *hEtaSelectedTauCandidates;
    WrappedTH1 *hEtaSelectedTaus;

    WrappedTH2 *hEtaPhiTauCandidates;
    WrappedTH2 *hEtaPhiSelectedTauCandidates;
    WrappedTH2 *hEtaPhiSelectedTaus;

    WrappedTH1 *hPhiTauCandidates;
    WrappedTH1 *hPhiSelectedTauCandidates;
    WrappedTH1 *hPhiSelectedTaus;
    WrappedTH1 *hNumberOfTauCandidates;
    WrappedTH1 *hNumberOfSelectedTauCandidates;
    WrappedTH1 *hNumberOfSelectedTaus;
    WrappedTH1 *hMCPurityOfTauCandidates;
    WrappedTH1 *hMCPurityOfSelectedTauCandidates;
    WrappedTH1 *hMCPurityOfSelectedTaus;

    WrappedTH1 *hNTriggerMatchedTaus;
    WrappedTH1 *hNTriggerMatchedSeparateTaus;

    WrappedTH1 *hIsolationPFChargedHadrCandsPtSum;
    WrappedTH1 *hIsolationPFGammaCandsEtSum;

    WrappedTH1 *hTightChargedMaxPtBeforeIsolation;
    WrappedTH1 *hTightChargedSumPtBeforeIsolation;
    WrappedTH1 *hTightChargedOccupancyBeforeIsolation;
    WrappedTH1 *hTightGammaMaxPtBeforeIsolation;
    WrappedTH1 *hTightGammaSumPtBeforeIsolation;
    WrappedTH1 *hTightGammaOccupancyBeforeIsolation;
    WrappedTH1 *hTightChargedMaxPtAfterIsolation;
    WrappedTH1 *hTightChargedSumPtAfterIsolation;
    WrappedTH1 *hTightChargedOccupancyAfterIsolation;
    WrappedTH1 *hTightGammaMaxPtAfterIsolation;
    WrappedTH1 *hTightGammaSumPtAfterIsolation;
    WrappedTH1 *hTightGammaOccupancyAfterIsolation;
    WrappedTH1 *hHPSDecayMode;

    WrappedTH1 *hVLooseIsoNcands;
    WrappedTH1 *hLooseIsoNcands;
    WrappedTH1 *hMediumIsoNcands;
    WrappedTH1 *hTightIsoNcands;

    WrappedTH2 *hFakeElectronEtaPhiAfterKinematics;
    WrappedTH2 *hFakeElectronEtaPhiAfterAgainstElectron;
    WrappedTH2 *hFakeElectronEtaPhiAfterAgainstElectronAndDeadVeto;
    WrappedTH2 *hFakeElectronEtaPhiAfterIsolation;
    WrappedTH2 *hFakeElectronEtaPhiAfterIsolationAndDeadVeto;
    WrappedTH2 *hFakeElectronEtaPhiAfterNProngs;
    WrappedTH2 *hFakeElectronEtaPhiAfterNProngsAndDeadVeto;

    WrappedTH2 *hFakeJetEtaPhiAfterKinematics;
    WrappedTH2 *hFakeJetEtaPhiAfterAgainstElectron;
    WrappedTH2 *hFakeJetEtaPhiAfterAgainstElectronAndDeadVeto;
    WrappedTH2 *hFakeJetEtaPhiAfterIsolation;
    WrappedTH2 *hFakeJetEtaPhiAfterIsolationAndDeadVeto;
    WrappedTH2 *hFakeJetEtaPhiAfterNProngs;
    WrappedTH2 *hFakeJetEtaPhiAfterNProngsAndDeadVeto;

    WrappedTH2 *hGenuineTauEtaPhiAfterKinematics;
    WrappedTH2 *hGenuineTauEtaPhiAfterAgainstElectron;
    WrappedTH2 *hGenuineTauEtaPhiAfterAgainstElectronAndDeadVeto;
    WrappedTH2 *hGenuineTauEtaPhiAfterIsolation;
    WrappedTH2 *hGenuineTauEtaPhiAfterIsolationAndDeadVeto;
    WrappedTH2 *hGenuineTauEtaPhiAfterNProngs;
    WrappedTH2 *hGenuineTauEtaPhiAfterNProngsAndDeadVeto;

    // Selected tau
    edm::PtrVector<pat::Tau> fSelectedTauCandidates;
    edm::PtrVector<pat::Tau> fSelectedTaus;
  };
}

#endif
