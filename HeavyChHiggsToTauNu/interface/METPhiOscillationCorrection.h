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
  class METPhiOscillationCorrection: public BaseSelection {
  public:
    /**
     * Class to encapsulate the access to the data members of
     * TauSelection. If you want to add a new accessor, add it here
     * and keep all the data private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data();
      ~Data();

      const double getCorrectionFactor() const { return fCorrectionFactor; }

      friend class METPhiOscillationCorrection;

    private:
      double fCorrectionFactor;
    };

    METPhiOscillationCorrection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~METPhiOscillationCorrection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    METPhiOscillationCorrection::Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const METSelection::Data& metData);
    METPhiOscillationCorrection::Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const METSelection::Data& metData);

  private:
    METPhiOscillationCorrection::Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const METSelection::Data& metData);
    // Input parameters

    // Counters

    // Histograms
    WrappedTH2 *hNVerticesVsMetX;
    WrappedTH2 *hNVerticesVsMetY;
    // FIXME: Add uncertainty histograms, etc.
  };
}

#endif
