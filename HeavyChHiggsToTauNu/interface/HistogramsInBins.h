// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_HistogramsInBins_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_HistogramsInBins_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class HistogramsInBins {
  public:
    HistogramsInBins(HPlus::HistoWrapper::HistoLevel, EventCounter&,HistoWrapper& ,std::string, std::string, int, double, double);
    ~HistogramsInBins();
   void Fill(double ,double);
   void Fill(double ,double, double); // for arbitrary weight
    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    // Use silentAnalyze if you do not want to fill histograms or increment counters
 

  private:
    // Histograms
    WrappedTH1 *hInclusive;
    WrappedTH1 *h4050;
    WrappedTH1 *h5060;
    WrappedTH1 *h6070;
    WrappedTH1 *h7080;
    WrappedTH1 *h80100;
    WrappedTH1 *h100120;
    WrappedTH1 *h120;
  };
}

#endif
