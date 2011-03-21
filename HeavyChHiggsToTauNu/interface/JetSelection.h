// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_JetSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/METReco/interface/MET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
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
      const edm::PtrVector<pat::Jet>& getSelectedJets() const { return fJetSelection->fSelectedJets; }
      const uint32_t getMinNumber() const { return fJetSelection->fMin; }
      const int getHadronicJetCount() const { return fJetSelection->iNHadronicJets; }
      const int getHadronicJetCountInFwdDir() const { return fJetSelection->iNHadronicJetsInFwdDir; }
      
    private:
      const JetSelection *fJetSelection;
      const bool fPassedEvent;
    };
       
    JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~JetSelection();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus);

  private:
    // Input parameters
    edm::InputTag fSrc;
    edm::InputTag fSrc_met;
    //    METSelection fMETSelection;
    const double fMetCut;
    const double fPtCut;
    const double fEtaCut;
    const double fMaxDR;
    const uint32_t fMin;

    // Counters
    Count fCleanCutCount;
    Count fPtCutCount;
    Count fEtaCutCount;

    Count fAllSubCount;
    Count fCleanCutSubCount;
    Count fPtCutSubCount;
    Count fEtaCutSubCount;
    Count fnumberOfDaughtersCutSubCount;
    Count fchargedEmEnergyFractionCutSubCount;
    Count fneutralHadronEnergyFractionCutSubCount;
    Count fneutralEmEnergyFractionCutSubCount;
    Count fchargedHadronEnergyFractionCutSubCount;
    Count fchargedMultiplicityCutSubCount;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Histograms
    TH1 *hPt;
    TH1 *hPtCentral;
    TH1 *hEta;
    TH1 *hPhi;
    TH1 *hNumberOfSelectedJets;
    TH1 *hDeltaPhiJetMet;
    // Selected jets
    edm::PtrVector<pat::Jet> fSelectedJets;
    // Not Selected jets
    edm::PtrVector<pat::Jet> fNotSelectedJets;
    int iNHadronicJets;
    int iNHadronicJetsInFwdDir;
  };
}

#endif
