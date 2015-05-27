#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMTWeight.h"

#include "FWCore/Framework/interface/Event.h"

namespace HPlus {
  EmbeddingMTWeight::EmbeddingMTWeight(const edm::ParameterSet& iConfig):
    fBinned(iConfig, "mt")
  {}

  EmbeddingMTWeight::~EmbeddingMTWeight() {}

  EmbeddingMTWeight::Data EmbeddingMTWeight::getEventWeight(double transverseMass, const edm::Event& iEvent) {
    fBinned.setRun(iEvent.id().run());
    return fBinned.getEventWeight(transverseMass, true);
  }

}
