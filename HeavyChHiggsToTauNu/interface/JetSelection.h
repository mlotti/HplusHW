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

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class JetSelection {
  public:
    JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~JetSelection();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus);
  
    /// Variables
    int iNHadronicJets;
    
    const edm::PtrVector<pat::Jet>& getSelectedJets() const {
      return fSelectedJets;
    }

    uint32_t getMinNumber() const {
      return fMin;
    }
  
  private:
    // Input parameters
    edm::InputTag fSrc;
    edm::InputTag fSrc_met;
    //    METSelection fMETSelection;
    double fMetCut;
    double fPtCut;
    double fEtaCut;
    double fMaxDR;
    uint32_t fMin;

    // Counters
    Count fCleanCutCount;
    Count fPtCutCount;
    Count fEtaCutCount;

    Count fAllSubCount;
    Count fCleanCutSubCount;
    Count fPtCutSubCount;
    Count fEtaCutSubCount;

    // Histograms
    TH1 *hPt;
    TH1 *hEta;
    TH1 *hNumberOfSelectedJets;
    TH1 *hDeltaPhiJetMet;
    // Selected jets
    edm::PtrVector<pat::Jet> fSelectedJets;
  };
}

#endif
