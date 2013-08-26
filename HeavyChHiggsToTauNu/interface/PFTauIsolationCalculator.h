// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_PFTauIsolationCalculator_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_PFTauIsolationCalculator_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Ptr.h"

#include <boost/utility.hpp>

namespace edm {
  class Event;
  class ParameterSet;
}
namespace reco {
  class Vertex;
}
namespace pat {
  class Tau;
}

namespace HPlus {

  class PFTauIsolationCalculator: private boost::noncopyable {
  public:
    PFTauIsolationCalculator(const edm::ParameterSet& iConfig);
    ~PFTauIsolationCalculator();

    void beginEvent(const edm::Event& iEvent);

    void calculateHpsLoose(const pat::Tau& tau, double *sumPt, double *maxPt, size_t *occupancy) const;
    void calculateHpsMedium(const pat::Tau& tau, double *sumPt, double *maxPt, size_t *occupancy) const;
    void calculateHpsTight(const pat::Tau& tau, double *sumPt, double *maxPt, size_t *occupancy) const;

    void calculateShrinkingConeByIsolation(const pat::Tau& tau, double *sumPt, double *maxPt, size_t *occupancy) const;
    void calculateShrinkingConeByIsolation(const pat::Tau& tau, double minTrackPt, double *sumPt, double *maxPt, size_t *occupancy) const;

    void calculate(const pat::Tau& tau, bool includeTracks, bool includeGammas, double minTrackPt, int minPixelHits, int minTrackHits, double maxIP, double maxChi2, double maxDeltaZ, double minGammaEt, double *sumPt, double *maxPt, size_t *occupancy) const;

  private:
    edm::InputTag pvSrc_;

    edm::Ptr<reco::Vertex> thePV_;
  };
}


#endif
