// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TopSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TopSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionBase.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class Event;
  class EventSetup;
  class ParameterSet;
}

namespace HPlus {
  class TopSelection: public TopSelectionBase {
  typedef TopSelectionBase::Data Data;

  public:  
    TopSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~TopSelection();
  
  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<pat::Jet> iJetb);
    void init();

    // Input parameters
    const double fTopMassLow;
    const double fTopMassHigh;

    // Counters
    //Count fTopMassCount;

    edm::InputTag fSrc;
    
    // Histograms
    WrappedTH1* htopPt;
    WrappedTH1* htopMass;
    WrappedTH1* htopEta;
    WrappedTH1* htopMassAfterCut;
    WrappedTH1* htopMassRejected;
    WrappedTH1* hWPt;
    WrappedTH1* hWMass;
    WrappedTH1* hWEta;
    WrappedTH1 *hPtjjb;
    WrappedTH1 *hPtmax;
    WrappedTH1 *hPtmaxMatch;
    WrappedTH1 *hPtmaxBMatch;
    WrappedTH1 *hPtmaxQMatch;
    WrappedTH1 *hPtmaxMatchWrongB;
    WrappedTH1 *hjjbMass;
    WrappedTH1 *htopMassMatch;
    WrappedTH1 *hWMassMatch;
    WrappedTH1 *htopMassBMatch;
    WrappedTH1 *hWMassBMatch;
    WrappedTH1 *htopMassQMatch;
    WrappedTH1 *hWMassQMatch;
    WrappedTH1 *htopMassMatchWrongB;
    WrappedTH1 *hWMassMatchWrongB;  
  };
}

#endif
