// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METPhiOscillationCorrection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METPhiOscillationCorrection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
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
  class WrappedTH2;

  /**
   * Class to contain plots to be repeated at different steps of analysis
   */
  class METPhiOscillationCorrection {
  public:
    METPhiOscillationCorrection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix);
    METPhiOscillationCorrection(EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix);
    ~METPhiOscillationCorrection();

    /// Plot information for determining parametrisation
    void analyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData);

  private:
    void privateAnalyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData);
    void initializeHistograms(HistoWrapper& histoWrapper, std::string prefix);
    // Input parameters

    // Counters

    // Histograms
    WrappedTH2 *hNVerticesVsMetX;
    WrappedTH2 *hNVerticesVsMetY;
    WrappedTH1 *hMETPhiUncorrected;
    WrappedTH1 *hMETPhiCorrected;
    WrappedTH1 *hMETUncorrected;
    WrappedTH1 *hMETCorrected;
    WrappedTH2 *hNVerticesVsMetXCorrected;
    WrappedTH2 *hNVerticesVsMetYCorrected;
    // FIXME: Add uncertainty histograms, etc.
  };
}

#endif
