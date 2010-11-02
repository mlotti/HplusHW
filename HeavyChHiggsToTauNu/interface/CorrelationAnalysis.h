// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_CorrelationAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_CorrelationAnalysis_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class CorrelationAnalysis {
  public:
    CorrelationAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    CorrelationAnalysis();
    ~CorrelationAnalysis();

    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    void analyze(const edm::PtrVector<reco::Candidate>&,const edm::PtrVector<reco::Candidate>&);
  
  private:
    void init();

    // Histograms
    TH1 *hPt;

  };
}

#endif
