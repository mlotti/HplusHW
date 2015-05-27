// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_HistogramsInBins2Dim_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_HistogramsInBins2Dim_h

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
  class WrappedTH2;

  class HistogramsInBins2Dim {
  public:
    HistogramsInBins2Dim(HPlus::HistoWrapper::HistoLevel, EventCounter&,HistoWrapper& ,std::string, std::string, std::string, int, double, double,  int, double, double);
     ~HistogramsInBins2Dim();
    void Fill(double ,double, double);
    void Fill(double ,double, double, double); // for arbitrary weight
    // PtrVector has implicit conversion from PtrVector of anything deriving from reco::Candidate
    // Use silentAnalyze if you do not want to fill histograms or increment counters
 

  private:
    // Histograms
    WrappedTH2 *hInclusive;
    WrappedTH2 *h4050;
    WrappedTH2 *h5060;
    WrappedTH2 *h6070;
    WrappedTH2 *h7080;
    WrappedTH2 *h80100;
    WrappedTH2 *h100120;
    WrappedTH2 *h120;
  };
}

#endif
