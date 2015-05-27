// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
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

  class TauSelection: public BaseSelection {
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
    enum TauSelectionOperationMode {
      kNormalTauID, // Tau candidate selection + tau ID selections
      kTauCandidateSelectionOnly // Only tau candidate selection is applied
    };

    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data();
      ~Data();
      /// Returns true, if the selected tau has passed all selections
      bool passedEvent() const { return fPassedEvent; }
      /// Returns list of all tau candidates prior to any cuts
      const edm::PtrVector<pat::Tau>& getAllTauObjects() const { return fAllTauCandidates; }
      /// Returns list of selected tau candidates (i.e. taus after tau candidate selection, no isolation or rtau applied); Note: list can be empty if no tau was selected
      const edm::PtrVector<pat::Tau>& getSelectedTausBeforeIsolation() const { return fSelectedTauCandidates; }
      /// Returns list of selected taus (i.e. taus after tau candidate selection or after full tau ID); Note: list can be empty if no tau was selected
      const edm::PtrVector<pat::Tau>& getSelectedTaus() const { return fSelectedTaus; }
      /// Returns selected tau in the event (i.e. tau after tau candidate selection or after full tau ID); Note: list can be empty if no tau was selected
      const edm::Ptr<pat::Tau> getSelectedTau() const;
      /// Returns true if the selected tau passes the isolation criteria
      const bool selectedTauPassesIsolation() const { return bSelectedTauPassesIsolation; }
      /// Returns true if the selected tau passes the nprongs cut
      const bool selectedTauPassesNProngs() const { return bSelectedTauPassesNProngs; }
      /// Returns true if the selected tau passes the rtau cut
      const bool selectedTauPassesRtau() const { return bSelectedTauPassesRtau; }
      /// Returns true if the selected tau passes the isolation, Nprongs, and the Rtau cuts
      const bool selectedTauPassesFullTauID() const { return selectedTauPassesIsolation() && selectedTauPassesNProngs() && selectedTauPassesRtau(); }
      /// Returns true if no candidates pass isolation
      const bool selectedTausDoNotPassIsolation() const { return bSelectedTausDoNotPassIsolation; }
      /// Returns true if the selected tau passes NProngs and Rtau but not isolation
      const bool selectedTauPassesNProngsAndRtauButNotIsolation() const { return !selectedTauPassesIsolation() && selectedTauPassesNProngs() && selectedTauPassesRtau(); }
      /// Returns the Nprongs value of the selected tau
      const int getSelectedTauNProngsValue() const { return fSelectedTauNProngsValue; }
      /// Returns the Rtau value of the selected tau
      const double getSelectedTauRtauValue() const { return fSelectedTauRtauValue; }
      /// Invalidate data object (as a safety precaution)
      void invalidate() { fSelectedTau = edm::Ptr<pat::Tau>(); }
      /// Obtain event weight for tau decay mode
      double getTauDecayModeReweightingFactor() const { return fTauDecayModeReweightingFactor; }

      friend class TauSelection;

    private:
      bool fPassedEvent; // non-const because need to be set from TauSelectionFactorized via setSelectedTau(...)
      // Selected tau
      edm::PtrVector<pat::Tau> fAllTauCandidates;
      edm::PtrVector<pat::Tau> fSelectedTauCandidates;
      edm::PtrVector<pat::Tau> fSelectedTaus;
      edm::Ptr<pat::Tau> fSelectedTau;
      bool bSelectedTauPassesIsolation;
      bool bSelectedTauPassesNProngs;
      bool bSelectedTauPassesRtau;
      bool bSelectedTausDoNotPassIsolation;
      int fSelectedTauNProngsValue;
      double fSelectedTauRtauValue;
      double fTauDecayModeReweightingFactor;
    };

    TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string label = "TauSelection");
    ~TauSelection();

    edm::InputTag getSrc() const { return fSrc; }

    /// Default tauID, no filling of histograms or counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, double vertexZ);
    /// Default tauID
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, double vertexZ);
    /// tau ID on a given sample of taus, no filling of histograms or counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ);
    /// tau ID on a given sample of taus
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ);
    /// Trigger tau selection - find best unique tau candidate
    // Data analyzeTriggerTau(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    /// Method for setting selected tau (from factorization)
    Data setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passedEvent);
    /// Method for getting operating mode (needed for tau specific weight maps)
    const TauSelectionOperationMode getOperationMode() const { return fOperationMode; }
    /// Fill eta-phi histograms of fake taus (Note: do not use in final analysis, because it will fill multiple times counters and histograms)
    void analyseFakeTauComposition(FakeTauIdentifier& fakeTauIdentifier, const edm::Event& iEvent);
    /// Select the pat::Tau object which most likely passes the tau candidate selection + ID
    const edm::Ptr<pat::Tau> selectMostLikelyTau(const edm::PtrVector<pat::Tau>& taus, double vertexZ);
    /// Returns true if tau passes Decay Mode filter
    const bool passesDecayModeFilter(const edm::Ptr<pat::Tau>& tau) const;

    // Horror getters - these should never be used in analysis for other purposes than testing / debugging !!!
    // If you use these for analysis, you forget about the sorting in the case of multiple taus -> physics results will not be accurate
    /// Use only for testing/debugging !!!
    const bool getPassesIsolationStatusOfTauObject(const edm::Ptr<pat::Tau>& tau, std::string isolationString = "") const;
    /// Use only for testing/debugging !!!
    const double getIsolationValueOfTauObject(const edm::Ptr<pat::Tau>& tau, std::string isolationString = "") const;
    /// Use only for testing/debugging !!!
    const bool getPassesNProngsStatusOfTauObject(const edm::Ptr<pat::Tau>& tau) const;
    /// Use only for testing/debugging !!!
    const bool getPassesRtauStatusOfTauObject(const edm::Ptr<pat::Tau>& tau) const;
    /// Use only for testing/debugging !!!
    const int getNProngsOfTauObject(const edm::Ptr<pat::Tau>& tau) const;
    /// Use only for testing/debugging !!!
    const double getRtauOfTauObject(const edm::Ptr<pat::Tau>& tau) const;
    // End of horror getters

    std::string getIsolationDiscriminator() const { return fTauID->getIsolationDiscriminator(); }

  private:
    /// Default tauID called from analyze or silentAnalyze
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, double vertexZ);
    /// Default tauID called from analyze or silentAnalyze
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ);
    /// Method for doing tau selection chain
    void doTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ, TauSelection::Data& output);
    /// Method for doing tau candidate selection, to be called from doTauSelection
    void doTauCandidateSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ, TauSelection::Data& output);
    /// Method for doing tau ID selection, to be called from doTauSelection
    void doTauIdentification(const edm::Event& iEvent, const edm::EventSetup& iSetup, TauSelection::Data& output);
    /// Method for finalizing tau ID selection, to be called from doTauSelection
    void finalizeSelection(TauSelection::Data& output);
    
    // Internal histogramming routines
    /// Fills the histogram that describes the mode in which the tau selection was run
    void fillOperationModeHistogram();
    /// Analyzes the angular separation of trigger matched taus
    void analyzeSeparationOfTriggerMatchedTaus(const edm::PtrVector<pat::Tau>& taus);
    /// Fills information histograms for all tau candidates
    void fillHistogramsForTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    /// Fills information histograms for cleaned tau candidates
    void fillHistogramsForSelectedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    /// Fills information histograms for selected taus
    void fillHistogramsForSelectedTaus(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent);
    /// Analyzes the MC purity of the considered tau objects
    void ObtainMCPurity(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent, WrappedTH1* histogram);
    //void findBestTau(edm::PtrVector<pat::Tau>& bestTau, edm::PtrVector<pat::Tau>& taus);
    /// Obtains event weight based on tau decay mode 
    double getTauDecayModeReweightingFactor(const edm::Ptr<pat::Tau> tau);

  private:
    // Input parameters
    /// Tau source
    edm::InputTag fSrc;
    /// Option for analysing fake tau composition
    const bool fAnalyseFakeTauComposition;
    /// Option for Decay Mode filter
    const int fDecayModeFilterValue;
    /// tau decay mode reweighting for tau -> pi+ nu
    const double fTauDecayModeReweightFactorForZero;
    /// tau decay mode reweighting for tau -> pi+ pi0 nu
    const double fTauDecayModeReweightFactorForOne;
    /// tau decay mode reweighting for other decay modes
    const double fTauDecayModeReweightFactorForOther;
    /// TauID object
    TauIDBase* fTauID;
    /// Operation mode of tau selection
    TauSelectionOperationMode fOperationMode;
    /// Factorization table objects

    // Histograms
    WrappedTH1 *hTauIdOperatingMode;
    WrappedTH1 *hTauIdCandidateSelectionSortCategory;
    WrappedTH1 *hDecayModeTauCandidates;
    WrappedTH1 *hDecayModeSelectedTauCandidates;
    WrappedTH1 *hDecayModeSelectedTaus;
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

    //WrappedTH1 *hVLooseIsoNcands;
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

  };
}

#endif
