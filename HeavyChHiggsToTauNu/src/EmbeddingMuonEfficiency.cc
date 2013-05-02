#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include <limits>
#include <cmath>

namespace HPlus {
  EmbeddingMuonEfficiency::Data::Data() {
    fWeight = std::numeric_limits<double>::quiet_NaN();
    fWeightAbsUnc = 1.0;
  }
  EmbeddingMuonEfficiency::Data::~Data() {}
  void EmbeddingMuonEfficiency::Data::check() const {
    if(isnan(fWeight))
      throw cms::Exception("Assert") << "EmbeddingMuonEfficiency::Data: This Data object was constructed with the default constructor, not with EmbeddingMuonEfficiency::getEventWeight(). There is something wrong in your code." << std::endl;
  }

  EmbeddingMuonEfficiency::EmbeddingMuonEfficiency(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper):
    //fMuonSrc(iConfig.getParameter<edm::InputTag>("muonSrc")),
    fEfficiencyScaleFactor(iConfig)
  {}
  EmbeddingMuonEfficiency::~EmbeddingMuonEfficiency() {}

  EmbeddingMuonEfficiency::Data EmbeddingMuonEfficiency::getEventWeight(const edm::Event& iEvent) {
    if(fEfficiencyScaleFactor.getMode() == EfficiencyScaleFactorBase::kDisabled) {
      Data output;
      output.fWeight = 1.0;
      return output;
    }

    // Obtain original muon
    edm::Handle<edm::View<pat::Muon> > hmuon;
    iEvent.getByLabel(fMuonSrc, hmuon);

    if(hmuon->size() != 1)
      throw cms::Exception("Assert") << "Read " << hmuon->size() << " muons for the original muon, expected exactly 1. Muon src was " << fMuonSrc.encode() << std::endl;

    setRun(iEvent.id().run());
    return getEventWeight(hmuon->at(0), iEvent.isRealData());

  }

  EmbeddingMuonEfficiency::Data EmbeddingMuonEfficiency::getEventWeight(const pat::Muon& muon, bool isData) {
    Data output(fEfficiencyScaleFactor.getEventWeight(isData));

    // Weight is actually the inverse of the efficiency
    if(output.fWeight != 0.0) {
      output.fWeightAbsUnc = output.fWeightAbsUnc / (output.fWeight*output.fWeight);
      output.fWeight = 1.0/output.fWeight;
    }
    return output;
  }
}
