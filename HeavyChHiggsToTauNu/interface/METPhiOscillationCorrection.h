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

    /// Getters for corrected quantities
    double getCorrectedMET(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met);
    double getCorrectedMETphi(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met);

    /// Plot information for determining parametrisation
    void analyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData);
    void analyze(const edm::Event& iEvent, int nVertices, const edm::Ptr<reco::MET>& met);

  private:
    double getCorrectedMETX(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met);
    double getCorrectedMETY(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met);
    void privateAnalyze(const edm::Event& iEvent, int nVertices, const edm::Ptr<reco::MET>& met);
    // Input parameters

    // Counters

    // Histograms
    WrappedTH2 *hNVerticesVsMetX;
    WrappedTH2 *hNVerticesVsMetY;
    // FIXME: Add uncertainty histograms, etc.
  };
}

#endif
