// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class METSelection: public BaseSelection {
  public:
    enum Select {kRaw, kType1, kType1PhiCorrected, kType2};

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
      Data();
      ~Data();

      const bool passedEvent() const { return fPassedEvent; }
      const bool passedPreMetCut() const { return fPassedPreMetCut; }
      const edm::Ptr<reco::MET> getSelectedMET() const;
      const edm::Ptr<reco::MET> getPhiUncorrectedSelectedMET() const;
      const edm::Ptr<reco::MET> getPhiCorrectedSelectedMET() const;
      const edm::Ptr<reco::MET> getRawMET() const { return fRawMET; }
      const edm::Ptr<reco::MET> getType1MET() const;
      const edm::Ptr<reco::MET> getType2MET() const { return fType2MET; }
      const edm::Ptr<reco::MET> getCaloMET() const { return fCaloMET; }
      const edm::Ptr<reco::MET> getTcMET() const { return fTcMET; }
      const std::vector<reco::MET> getType1METCorrected() const { return fType1METCorrected; }
      friend class METSelection;

    private:
      bool fPassedEvent;
      bool fPassedPreMetCut;
      Select fMETMode;
      // MET objects
      edm::Ptr<reco::MET> fRawMET;
      edm::Ptr<reco::MET> fType1MET;
      edm::Ptr<reco::MET> fType2MET;
      edm::Ptr<reco::MET> fCaloMET;
      edm::Ptr<reco::MET> fTcMET;
      // For type I/II correction
      std::vector<reco::MET> fType1METCorrected;
      //std::vector<reco::MET> fType2METCorrected;
      // For MET phi oscillation
      std::vector<reco::MET> fPhiOscillationCorrectedType1MET;
    };

    METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, const std::string& label, const std::string& tauIsolationDiscriminator);
    ~METSelection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    // Here tau is always assumed isolated for type 1 correction
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);

    // Here non-isolated taus are taken as jets, if
    // fNonIsolatedTausAsJetsEnabled is true (from python
    // configuration)
    Data silentAnalyzeWithPossiblyIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);
    Data analyzeWithPossiblyIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);

    // Returns type I MET object for assumption "no isolated taus" (use case: common plots or met phi oscillation before tau selection)
    Data silentAnalyzeNoIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices);

    const double getCutValue() const { return fMetCut; }

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets, bool possiblyIsolatedTaus);

    

    enum PossiblyIsolatedTauMode { // Do TypeI (residual) correction for possibly isolated taus?
      kDisabled,       // equivalent to always
      kNever,          // Taus in (silent)analyzeWithPossiblyIsolatedTaus are always considered as jets
      kAlways,         // Taus in (silent)analyzeWithPossiblyIsolatedTaus are always considered as isolated taus
      kForIsolatedOnly // Taus in (silent)analyzeWithPossiblyIsolatedTaus are treated according to their isolation status (non-isolated as jets, isolated as taus)
    };

    reco::MET undoJetCorrectionForSelectedTau(const edm::Ptr<reco::MET>& met, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets, Select type, bool possibltyIsolatedTaus);
    reco::MET getPhiOscillationCorrectedMET(const edm::Ptr<reco::MET>& met, const bool isRealData, const int nVertices);

    // Input parameters
    edm::InputTag fRawSrc;
    edm::InputTag fType1Src;
    edm::InputTag fType2Src;
    edm::InputTag fCaloSrc;
    edm::InputTag fTcSrc;
    Select fSelect;

    const double fMetCut;
    const double fPreMetCut;
    // For type I/II correction
    const double fTauJetMatchingCone;
    const double fJetType1Threshold;
    std::string fJetOffsetCorrLabel;
    //double fType2ScaleFactor;
    std::string fTauIsolationDiscriminator;
    PossiblyIsolatedTauMode fDoTypeICorrectionForPossiblyIsolatedTaus;
    // For phi oscillation correction
    const double fPhiCorrectionSlopeXForData;
    const double fPhiCorrectionOffsetXForData;
    const double fPhiCorrectionSlopeYForData;
    const double fPhiCorrectionOffsetYForData;
    const double fPhiCorrectionSlopeXForMC;
    const double fPhiCorrectionOffsetXForMC;
    const double fPhiCorrectionSlopeYForMC;
    const double fPhiCorrectionOffsetYForMC;
    bool bDisablingOfPhiCorrectionNotifiedStatus;

    // Counters
    Count fTypeIAllEvents;
    Count fTypeITauRefJetFound;
    Count fTypeITauIsolated;
    Count fMetCutCount;

    // Histograms
    WrappedTH1 *hMet;
    WrappedTH1 *hMetPhi;
    WrappedTH1 *hMetSignif;
    WrappedTH1 *hMetSumEt;
    WrappedTH1 *hMetDivSumEt;
    WrappedTH1 *hMetDivSqrSumEt;

  };
}

#endif
