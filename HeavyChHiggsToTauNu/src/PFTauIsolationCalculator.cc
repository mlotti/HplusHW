#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PFTauIsolationCalculator.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"

#include<vector>

#include <boost/foreach.hpp>

namespace HPlus {
  PFTauIsolationCalculator::PFTauIsolationCalculator(const edm::ParameterSet& iConfig):
    pvSrc_(iConfig.getParameter<edm::InputTag>("pvSrc"))
  {}
  PFTauIsolationCalculator::~PFTauIsolationCalculator() {}

  void PFTauIsolationCalculator::beginEvent(const edm::Event& iEvent) {
    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(pvSrc_, hvertex);
    thePV_ = hvertex->ptrAt(0);
  }

  void PFTauIsolationCalculator::calculateHpsLoose(const pat::Tau& tau, double *sumPt, size_t *occupancy) const {
    double minTrackPt = 1.0;
    int minPixelHits = 0;
    int minTrackHits = 8;
    double maxIP = 0.03;
    double maxChi2 = 100;
    double maxDeltaZ = 0.2;

    double minGammaEt = 1.5;

    calculate(tau, true, true, minTrackPt, minPixelHits, minTrackHits, maxIP, maxChi2, maxDeltaZ, minGammaEt, sumPt, occupancy);
  }

  void PFTauIsolationCalculator::calculateHpsMedium(const pat::Tau& tau, double *sumPt, size_t *occupancy) const {
    double minTrackPt = 0.8;
    int minPixelHits = 0;
    int minTrackHits = 3;
    double maxIP = 0.03;
    double maxChi2 = 100;
    double maxDeltaZ = 0.2;

    double minGammaEt = 0.8;

    calculate(tau, true, true, minTrackPt, minPixelHits, minTrackHits, maxIP, maxChi2, maxDeltaZ, minGammaEt, sumPt, occupancy);
  }

  void PFTauIsolationCalculator::calculateHpsTight(const pat::Tau& tau, double *sumPt, size_t *occupancy) const {
    double minTrackPt = 0.5;
    int minPixelHits = 0;
    int minTrackHits = 3;
    double maxIP = 0.03;
    double maxChi2 = 100;
    double maxDeltaZ = 0.2;

    double minGammaEt = 0.5;

    calculate(tau, true, true, minTrackPt, minPixelHits, minTrackHits, maxIP, maxChi2, maxDeltaZ, minGammaEt, sumPt, occupancy);
  }

  void PFTauIsolationCalculator::calculateShrinkingConeByIsolation(const pat::Tau& tau, double *sumPt, size_t *occupancy) const {
    double minTrackPt = 1.0;

    calculateShrinkingConeByIsolation(tau, minTrackPt, sumPt, occupancy);
  }

  void PFTauIsolationCalculator::calculateShrinkingConeByIsolation(const pat::Tau& tau, double minTrackPt, double *sumPt, size_t *occupancy) const {
    int minPixelHits = 0;
    int minTrackHits = 8;
    double maxIP = 0.03;
    double maxChi2 = 100;
    double maxDeltaZ = 0.2;

    double minGammaEt = 1.5;

    calculate(tau, true, true, minTrackPt, minPixelHits, minTrackHits, maxIP, maxChi2, maxDeltaZ, minGammaEt, sumPt, occupancy);
  }

  void PFTauIsolationCalculator::calculate(const pat::Tau& tau, bool includeTracks, bool includeGammas, double minTrackPt, int minPixelHits, int minTrackHits, double maxIP, double maxChi2, double maxDeltaZ, double minGammaEt, double *sumPt, size_t *occupancy) const {
    *sumPt = 0;
    *occupancy = 0;

    //includeTracks = false;
    //includeGammas = false;

    if(includeTracks) {
      reco::PFCandidateRefVector allCands = tau.isolationPFChargedHadrCands();
      if(allCands.isNonnull()) {
        reco::PFCandidateRefVector chargedCands = TauTagTools::filteredPFChargedHadrCands(allCands,
                                                                                          minTrackPt,
                                                                                          minPixelHits,
                                                                                          minTrackHits,
                                                                                          maxIP,
                                                                                          maxChi2,
                                                                                          maxDeltaZ,
                                                                                          *thePV_,
                                                                                          thePV_->position().z());
        *occupancy = *occupancy + chargedCands.size();
        for(size_t i=0; i<chargedCands.size(); ++i) {
          *sumPt = *sumPt + chargedCands[i]->pt();
        }
      }
    }

    if(includeGammas) {
      reco::PFCandidateRefVector allCands = tau.isolationPFGammaCands();
      if(allCands.isNonnull()) {
        reco::PFCandidateRefVector gammaCands = TauTagTools::filteredPFGammaCands(allCands, minGammaEt);

        *occupancy = *occupancy + gammaCands.size();
        for(size_t i=0; i<gammaCands.size(); ++i) {
          *sumPt = *sumPt + gammaCands[i]->pt();
        }
      }
    }
  }
}
