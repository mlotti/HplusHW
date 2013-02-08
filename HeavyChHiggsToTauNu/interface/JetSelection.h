// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeadECALCells.h"

#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::XYZTLorentzVector LorentzVector;


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  class JetSelection: public BaseSelection {
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
      Data();
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const edm::PtrVector<pat::Jet>& getAllJets() const { return fAllJets; }
      const edm::PtrVector<pat::Jet>& getAllIdentifiedJets() const { return fAllIdentifiedJets; }
      const edm::PtrVector<pat::Jet>& getSelectedJets() const { return fSelectedJets; }
      const edm::PtrVector<pat::Jet>& getSelectedJetsPt20() const { return fSelectedJetsPt20; }
      const int getHadronicJetCount() const { return iNHadronicJets; }
      const int getHadronicJetCountInFwdDir() const { return iNHadronicJetsInFwdDir; }
      const bool eventHasJetWithEMFraction07() const { return bEMFraction07Veto; }
      const bool eventHasJetWithEMFraction08() const { return bEMFraction08Veto; }
      // Analysing jet topology
      const double getMinEtaOfSelectedJetToGap() const { return fMinEtaOfSelectedJetToGap; }
      const double getEtaSpreadOfSelectedJets() const { return fEtaSpreadOfSelectedJets; }
      const double getAverageEtaOfSelectedJets() const { return fAverageEtaOfSelectedJets; }
      const double getAverageSelectedJetsEtaDistanceToTauEta() const { return fAverageSelectedJetsEtaDistanceToTauEta; }
      const double getDeltaPtJetTau() const { return fDeltaPtJetTau; }
      // MHT (based only on PF Jets)
      const LorentzVector& getMHTvector() const { return fMHT; }
      const double getMHT() const { return fMHT.pt(); }
      const double getMHTphi() const { return fMHT.phi(); }
      // Angles between MHT and jets (overlap with tau not considered)
      const double getDeltaPhiMHTJet1() const { return fDeltaPhiMHTJet1; }
      const double getDeltaPhiMHTJet2() const { return fDeltaPhiMHTJet2; }
      const double getDeltaPhiMHTJet3() const { return fDeltaPhiMHTJet3; }
      const double getDeltaPhiMHTJet4() const { return fDeltaPhiMHTJet4; }
      const double getDeltaPhiMHTTau() const { return fDeltaPhiMHTTau; }
      // Jet corresponding to tau
      const edm::Ptr<pat::Jet> getReferenceJetToTau() const { return fReferenceJetToTau; }
      const int getReferenceJetToTauPartonFlavour() const;
      const double getReferenceJetToTauDeltaPt() const { return fReferenceJetToTauDeltaPt; }
      const double getReferenceJetToTauPtRatio() const { return fReferenceJetToTauPtRatio; }

      friend class JetSelection;

    private:
      bool fPassedEvent;
      // All jets
      edm::PtrVector<pat::Jet> fAllJets;
      edm::PtrVector<pat::Jet> fAllIdentifiedJets;
      // Selected jets
      edm::PtrVector<pat::Jet> fSelectedJets;
      edm::PtrVector<pat::Jet> fSelectedJetsPt20;
      // Not Selected jets
      edm::PtrVector<pat::Jet> fNotSelectedJets;
      int iNHadronicJets;
      int iNHadronicJetsInFwdDir;
      float fMinDeltaRToOppositeDirectionOfTau;
      bool bEMFraction08Veto;
      bool bEMFraction07Veto;
      // Analysing jet topology
      double fMinEtaOfSelectedJetToGap;
      double fEtaSpreadOfSelectedJets;
      double fAverageEtaOfSelectedJets;
      double fAverageSelectedJetsEtaDistanceToTauEta;
      double fDeltaPtJetTau;
      // MHT (based only on PF Jets)
      LorentzVector fMHT;
      // Angles between MHT and jets (overlap with tau not considered)
      double fDeltaPhiMHTJet1;
      double fDeltaPhiMHTJet2;
      double fDeltaPhiMHTJet3;
      double fDeltaPhiMHTJet4;
      double fDeltaPhiMHTTau;
      // Jet corresponding to tau
      edm::Ptr<pat::Jet> fReferenceJetToTau;
      double fReferenceJetToTauDeltaPt;
      double fReferenceJetToTauPtRatio;
    };

    JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    virtual ~JetSelection();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau, int nVertices = 1);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau, int nVertices = 1);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau, int nVertices);
    bool passBetaCut(const edm::Ptr<pat::Jet>& jet, const edm::Event& iEvent, int nVertices);
    void obtainReferenceJetToTau(const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::Candidate>& tau, JetSelection::Data& output);
    void calculateMHT(JetSelection::Data& output, const edm::Ptr<reco::Candidate>& tau);
    void plotSelectedJetHistograms(const edm::Ptr<pat::Jet>& jet, const bool isRealData);
    void plotExcludedJetHistograms(const edm::Ptr<pat::Jet>& jet, const bool isRealData);

    // Input parameters
    edm::InputTag fSrc;
    const double fPtCut;
    const double fEtaCut;
    const double fEMfractionCut;
    const double fMaxDR;
    DirectionalCut fNumberOfJets;
    const double fJetIdMaxNeutralHadronEnergyFraction;
    const double fJetIdMaxNeutralEMEnergyFraction;
    const uint32_t fJetIdMinNumberOfDaughters;
    const double fJetIdMinChargedHadronEnergyFraction;
    const uint32_t fJetIdMinChargedMultiplicity;
    const double fJetIdMaxChargedEMEnergyFraction;
    DirectionalCut fBetaCut;
    std::string fBetaSrc;
    const bool fApplyVetoForDeadECALCells;
    const double fDeadECALCellsVetoDeltaR;

    DeadECALCells fDeadECALCells;

    // Counters
    Count fAllCount;
    Count fDeadECALCellVetoCount;
    Count fCleanCutCount;
    Count fJetIdCount;
    Count fBetaCutCount;
    Count fEMfractionCutCount;
    Count fEtaCutCount;
    Count fPtCutCount;
    Count fAllSubCount;
    Count fEMfraction08CutCount;
    Count fEMfraction07CutCount;
    Count fEventKilledByBetaCutCount;
    Count fCleanCutSubCount;
    Count fneutralHadronEnergyFractionCutSubCount;
    Count fneutralEmEnergyFractionCutSubCount;
    Count fnumberOfDaughtersCutSubCount;
    Count fchargedHadronEnergyFractionCutSubCount;
    Count fchargedMultiplicityCutSubCount;
    Count fchargedEmEnergyFractionCutSubCount;
    Count fJetIdSubCount;
    Count fEMfractionCutSubCount;
    Count fBetaCutSubCount;
    Count fEtaCutSubCount;
    Count fPtCutSubCount;
    Count fJetToTauReferenceJetNotIdentifiedCount;

    // Histograms
    WrappedTH1 *hPt;
    WrappedTH1 *hPtCentral;
    WrappedTH1 *hEta;
    WrappedTH1 *hPhi;
    WrappedTH1 *hNumberOfSelectedJets;
    WrappedTH1 *hjetEMFraction;
    WrappedTH1 *hjetChargedEMFraction;
    WrappedTH1 *hjetMaxEMFraction;
    WrappedTH1 *hMinDeltaRToOppositeDirectionOfTau;
    WrappedTH1 *hFirstJetPt;
    WrappedTH1 *hSecondJetPt;
    WrappedTH1 *hThirdJetPt;
    WrappedTH1 *hFourthJetPt;
    WrappedTH1 *hFirstJetEta;
    WrappedTH1 *hSecondJetEta;
    WrappedTH1 *hThirdJetEta;
    WrappedTH1 *hFourthJetEta;
    WrappedTH1 *hFirstJetPhi;
    WrappedTH1 *hSecondJetPhi;
    WrappedTH1 *hThirdJetPhi;
    WrappedTH1 *hFourthJetPhi;
    WrappedTH1 *hMinEtaOfSelectedJetToGap;

    // PU analysis
    WrappedTH1 *hBetaGenuine;
    WrappedTH1 *hBetaStarGenuine;
    WrappedTH1 *hMeanDRgenuine;
    WrappedTH1 *hBetaFake;
    WrappedTH1 *hBetaStarFake;
    WrappedTH1 *hMeanDRfake;
    WrappedTH2 *hBetaVsPUgenuine;
    WrappedTH2 *hBetaStarVsPUgenuine;
    WrappedTH2 *hMeanDRVsPUgenuine;
    WrappedTH2 *hBetaVsPUfake;
    WrappedTH2 *hBetaStarVsPUfake;
    WrappedTH2 *hMeanDRVsPUfake;

    // Histograms for excluded jets (i.e. matching in DeltaR to tau jet)
    WrappedTH1 *hPtExcludedJets;
    WrappedTH1 *hEtaExcludedJets;
    WrappedTH1 *hPhiExcludedJets;
    WrappedTH1 *hNeutralEmEnergyFractionExcludedJets;
    WrappedTH1 *hNeutralMultiplicityExcludedJets;
    WrappedTH1 *hNeutralHadronEnergyFractionExcludedJets;
    WrappedTH1 *hNeutralHadronMultiplicityExcludedJets;
    WrappedTH1 *hPhotonEnergyFractionExcludedJets;
    WrappedTH1 *hPhotonMultiplicityExcludedJets;
    WrappedTH1 *hMuonEnergyFractionExcludedJets;
    WrappedTH1 *hMuonMultiplicityExcludedJets;
    WrappedTH1 *hChargedHadronEnergyFractionExcludedJets;
    WrappedTH1 *hChargedEmEnergyFractionExcludedJets;
    WrappedTH1 *hChargedMultiplicityExcludedJets;
    WrappedTH1 *hPartonFlavourExcludedJets;
    WrappedTH1 *hJECFactorExcludedJets;
    WrappedTH1 *hN60ExcludedJets;
    WrappedTH1 *hTowersAreaExcludedJets;
    WrappedTH1 *hJetChargeExcludedJets;
    WrappedTH1 *hPtDiffToGenJetExcludedJets;

    // Histograms for selected jets
    WrappedTH1 *hPtSelectedJets;
    WrappedTH1 *hEtaSelectedJets;
    WrappedTH1 *hPhiSelectedJets;
    WrappedTH1 *hNeutralEmEnergyFractionSelectedJets;
    WrappedTH1 *hNeutralMultiplicitySelectedJets;
    WrappedTH1 *hNeutralHadronEnergyFractionSelectedJets;
    WrappedTH1 *hNeutralHadronMultiplicitySelectedJets;
    WrappedTH1 *hPhotonEnergyFractionSelectedJets;
    WrappedTH1 *hPhotonMultiplicitySelectedJets;
    WrappedTH1 *hMuonEnergyFractionSelectedJets;
    WrappedTH1 *hMuonMultiplicitySelectedJets;
    WrappedTH1 *hChargedHadronEnergyFractionSelectedJets;
    WrappedTH1 *hChargedEmEnergyFractionSelectedJets;
    WrappedTH1 *hChargedMultiplicitySelectedJets;
    WrappedTH1 *hPartonFlavourSelectedJets;
    WrappedTH1 *hJECFactorSelectedJets;
    WrappedTH1 *hN60SelectedJets;
    WrappedTH1 *hTowersAreaSelectedJets;
    WrappedTH1 *hJetChargeSelectedJets;
    WrappedTH1 *hPtDiffToGenJetSelectedJets;
    WrappedTH1 *hDeltaPtJetTau;
    WrappedTH1 *hDeltaRJetTau;

    // MHT related
    WrappedTH1 *hMHT;
    WrappedTH1 *hMHTphi;
    WrappedTH1 *hDeltaPhiMHTJet1;
    WrappedTH1 *hDeltaPhiMHTJet2;
    WrappedTH1 *hDeltaPhiMHTJet3;
    WrappedTH1 *hDeltaPhiMHTJet4;
    WrappedTH1 *hDeltaPhiMHTTau;

    // Reference tau related
    WrappedTH1 *hReferenceJetToTauMatchingDeltaR;
    WrappedTH1 *hReferenceJetToTauPartonFlavour;
    WrappedTH1 *hReferenceJetToTauDeltaPt;
    WrappedTH1 *hReferenceJetToTauPtRatio;

  };
}

#endif
