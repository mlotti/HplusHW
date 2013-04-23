// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetDetailHistograms.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeadECALCells.h"
#include "CMGTools/External/interface/PileupJetIdentifier.h" // Will be at DataFormats/JetReco/interface from 6_x_y

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
      const edm::PtrVector<pat::Jet>& getSelectedJetsIncludingTau() const { return fSelectedJetsIncludingTau; }
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
      const double getReferenceJetToTauMatchDeltaR() const { return fReferenceJetToTauDeltaR; }
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
      edm::PtrVector<pat::Jet> fSelectedJetsIncludingTau;
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
      double fReferenceJetToTauDeltaR;
      double fReferenceJetToTauDeltaPt;
      double fReferenceJetToTauPtRatio;
    };

    JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    virtual ~JetSelection();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices = 1);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau, int nVertices = 1);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau, int nVertices = 1);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau, int nVertices);
    void obtainReferenceJetToTau(const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::Candidate>& tau, JetSelection::Data& output);
    void calculateMHT(JetSelection::Data& output, const edm::Ptr<reco::Candidate>& tau);

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
    PileupJetIdentifier::Id fJetPileUpWorkingPoint;
    edm::InputTag fJetPileUpMVAValuesSrc;
    edm::InputTag fJetPileUpIdFlagSrc;
    // Experimental input parameters
    const bool fApplyVetoForDeadECALCells;
    const double fDeadECALCellsVetoDeltaR;
    DeadECALCells fDeadECALCells;

    // Counters
    Count fAllCount;
    Count fDeadECALCellVetoCount;
    Count fCleanCutCount;
    Count fJetIdCount;
    Count fJetPUIDCount;
    Count fEMfractionCutCount;
    Count fEtaCutCount;
    Count fPtCutCount;
    Count fAllSubCount;
    Count fEMfraction08CutCount;
    Count fEMfraction07CutCount;
    Count fEventKilledByJetPUIDCount;
    Count fCleanCutSubCount;
    Count fneutralHadronEnergyFractionCutSubCount;
    Count fneutralEmEnergyFractionCutSubCount;
    Count fnumberOfDaughtersCutSubCount;
    Count fchargedHadronEnergyFractionCutSubCount;
    Count fchargedMultiplicityCutSubCount;
    Count fchargedEmEnergyFractionCutSubCount;
    Count fJetIdSubCount;
    Count fEMfractionCutSubCount;
    Count fJetPUIDSubCount;
    Count fEtaCutSubCount;
    Count fPtCutSubCount;
    Count fJetToTauReferenceJetNotIdentifiedCount;

    // Histograms
    WrappedTH1 *hPtIncludingTau;
    WrappedTH1 *hEtaIncludingTau;
    WrappedTH1 *hPhiIncludingTau;
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
    WrappedTH1 *hJetPUIDMvaResult;

    // Histograms for excluded jets (i.e. matching in DeltaR to tau jet)
    JetDetailHistograms* fExcludedJetsDetailHistograms;

    // Histograms for selected jets
    JetDetailHistograms* fSelectedJetsDetailHistograms;
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
