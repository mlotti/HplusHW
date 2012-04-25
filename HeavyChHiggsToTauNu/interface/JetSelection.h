// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class JetSelection {
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
      Data(const JetSelection *jetSelection, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const edm::PtrVector<pat::Jet>& getAllJets() const { return fJetSelection->fAllJets; }
      const edm::PtrVector<pat::Jet>& getSelectedJets() const { return fJetSelection->fSelectedJets; }
      const uint32_t getMinNumber() const { return fJetSelection->fMinNumberOfJets; }
      const int getHadronicJetCount() const { return fJetSelection->iNHadronicJets; }
      const int getHadronicJetCountInFwdDir() const { return fJetSelection->iNHadronicJetsInFwdDir; }
      const bool eventHasJetWithEMFraction07() const { return fJetSelection->bEMFraction07Veto; }
      const bool eventHasJetWithEMFraction08() const { return fJetSelection->bEMFraction08Veto; }
      
    private:
      const JetSelection *fJetSelection;
      const bool fPassedEvent;
    };
       
    JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~JetSelection();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    //    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau);

    //    Data  analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau);
    //    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau);
    //    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus);

  private:
    // Input parameters
    edm::InputTag fSrc;
    const double fPtCut;
    const double fEtaCut;
    const double fEMfractionCut;
    const double fMaxDR;
    const uint32_t fMinNumberOfJets;
    const double fJetIdMaxNeutralHadronEnergyFraction;
    const double fJetIdMaxNeutralEMEnergyFraction;
    const uint32_t fJetIdMinNumberOfDaughters;
    const double fJetIdMinChargedHadronEnergyFraction;
    const uint32_t fJetIdMinChargedMultiplicity;
    const double fJetIdMaxChargedEMEnergyFraction;
    const double fBetaCut;

    // Counters
    Count fCleanCutCount;
    Count fJetIdCount;
    Count fEMfractionCutCount;
    Count fEtaCutCount;
    Count fPtCutCount;
    Count fAllSubCount;
    Count fEMfraction08CutCount;
    Count fEMfraction07CutCount;
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

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Histograms
    TH1 *hPt;
    TH1 *hPtCentral;
    TH1 *hEta;
    TH1 *hPhi;
    TH1 *hNumberOfSelectedJets;
    TH1 *hjetEMFraction;
    TH1 *hjetChargedEMFraction;
    TH1 *hjetMaxEMFraction;
    TH1 *hMinDeltaRToOppositeDirectionOfTau;
    TH1 *hFirstJetPt;
    TH1 *hSecondJetPt;
    TH1 *hThirdJetPt;
    TH1 *hFourthJetPt;
    TH1 *hFirstJetEta;
    TH1 *hSecondJetEta;
    TH1 *hThirdJetEta;
    TH1 *hFourthJetEta;
    TH1 *hFirstJetPhi;
    TH1 *hSecondJetPhi;
    TH1 *hThirdJetPhi;
    TH1 *hFourthJetPhi;

    // Histograms for jet composition
    TH1 *hPtExcludedJets;
    TH1 *hEtaExcludedJets;
    TH1 *hPhiExcludedJets;
    TH1 *hNeutralEmEnergyFractionExcludedJets;
    TH1 *hNeutralMultiplicityExcludedJets;
    TH1 *hNeutralHadronEnergyFractionExcludedJets;
    TH1 *hNeutralHadronMultiplicityExcludedJets;
    TH1 *hPhotonEnergyFractionExcludedJets;
    TH1 *hPhotonMultiplicityExcludedJets;
    TH1 *hMuonEnergyFractionExcludedJets;
    TH1 *hMuonMultiplicityExcludedJets;
    TH1 *hChargedHadronEnergyFractionExcludedJets;
    TH1 *hChargedEmEnergyFractionExcludedJets;
    TH1 *hChargedMultiplicityExcludedJets;
    TH1 *hPartonFlavourExcludedJets;
    TH1 *hJECFactorExcludedJets;
    TH1 *hN60ExcludedJets;
    TH1 *hTowersAreaExcludedJets;
    TH1 *hJetChargeExcludedJets;
    TH1 *hPtDiffToGenJetExcludedJets;

    TH1 *hPtSelectedJets;
    TH1 *hEtaSelectedJets;
    TH1 *hPhiSelectedJets;
    TH1 *hNeutralEmEnergyFractionSelectedJets;
    TH1 *hNeutralMultiplicitySelectedJets;
    TH1 *hNeutralHadronEnergyFractionSelectedJets;
    TH1 *hNeutralHadronMultiplicitySelectedJets;
    TH1 *hPhotonEnergyFractionSelectedJets;
    TH1 *hPhotonMultiplicitySelectedJets;
    TH1 *hMuonEnergyFractionSelectedJets;
    TH1 *hMuonMultiplicitySelectedJets;
    TH1 *hChargedHadronEnergyFractionSelectedJets;
    TH1 *hChargedEmEnergyFractionSelectedJets;
    TH1 *hChargedMultiplicitySelectedJets;
    TH1 *hPartonFlavourSelectedJets;
    TH1 *hJECFactorSelectedJets;
    TH1 *hN60SelectedJets;
    TH1 *hTowersAreaSelectedJets;
    TH1 *hJetChargeSelectedJets;
    TH1 *hPtDiffToGenJetSelectedJets;

    // All jets
    edm::PtrVector<pat::Jet> fAllJets;
    // Selected jets
    edm::PtrVector<pat::Jet> fSelectedJets;
    // Not Selected jets
    edm::PtrVector<pat::Jet> fNotSelectedJets;
    int iNHadronicJets;
    int iNHadronicJetsInFwdDir;
    bool bEMFraction08Veto;
    bool bEMFraction07Veto;
    float fMinDeltaRToOppositeDirectionOfTau;
  };
}

#endif
