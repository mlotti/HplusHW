#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ConstantEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BinnedEfficiencyScaleFactor.h"

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
    fWeightAbsUncPlus = 0.0;
    fWeightAbsUncMinus = 0.0;
    fEfficiency = fWeight;
    fEfficiencyAbsUncPlus = fWeightAbsUncPlus;
    fEfficiencyAbsUncMinus = fWeightAbsUncMinus;
  }
  EmbeddingMuonEfficiency::Data::~Data() {}
  void EmbeddingMuonEfficiency::Data::check() const {
    if(isnan(fWeight))
      throw cms::Exception("Assert") << "EmbeddingMuonEfficiency::Data: This Data object was constructed with the default constructor, not with EmbeddingMuonEfficiency::getEventWeight(). There is something wrong in your code." << std::endl;
  }
  
  EmbeddingMuonEfficiency::EmbeddingMuonEfficiency(const edm::ParameterSet& iConfig):
    fMuonSrc(iConfig.getParameter<edm::InputTag>("muonSrc"))
  {
    std::string type = iConfig.getUntrackedParameter<std::string>("type");
    if(type == "constant")
      fEfficiencyScaleFactor.reset(new ConstantEfficiencyScaleFactor(iConfig));
    else if(type == "binned")
      fEfficiencyScaleFactor.reset(new BinnedEfficiencyScaleFactor(iConfig, "eta"));
    else
      throw cms::Exception("Configuration") << "EmbeddingMuonEfficiency: got invalid value for 'type' " << type 
                                            << ", valid values are 'constant' and 'binned'";
  }
  EmbeddingMuonEfficiency::~EmbeddingMuonEfficiency() {}

  EmbeddingMuonEfficiency::Data EmbeddingMuonEfficiency::getEventWeight(const edm::Event& iEvent) {
    if(fEfficiencyScaleFactor->getMode() == EfficiencyScaleFactorBase::kDisabled) {
      Data output;
      output.fWeight = 1.0;
      output.fEfficiency = 1.0;
      return output;
    }

    if(dynamic_cast<const ConstantEfficiencyScaleFactor *>(fEfficiencyScaleFactor.get())) {
      return getEventWeight(edm::Ptr<pat::Muon>(), iEvent.isRealData());
    }
    else {
      // Obtain original muon
      edm::Handle<edm::View<pat::Muon> > hmuon;
      iEvent.getByLabel(fMuonSrc, hmuon);

      if(hmuon->size() != 1)
        throw cms::Exception("Assert") << "Read " << hmuon->size() << " muons for the original muon, expected exactly 1. Muon src was " << fMuonSrc.encode() << std::endl;

      if(iEvent.isRealData())
         setRun(iEvent.id().run());
      return getEventWeight(hmuon->ptrAt(0), iEvent.isRealData());
    }
  }

  EmbeddingMuonEfficiency::Data EmbeddingMuonEfficiency::getEventWeight(const edm::Ptr<pat::Muon>& muon, bool isData) const {
    Data output;
    if(const ConstantEfficiencyScaleFactor *ceff = dynamic_cast<const ConstantEfficiencyScaleFactor *>(fEfficiencyScaleFactor.get())) {
      output = Data(ceff->getEventWeight(isData));
    }
    else if(const BinnedEfficiencyScaleFactor *beff = dynamic_cast<const BinnedEfficiencyScaleFactor *>(fEfficiencyScaleFactor.get())) {
      if(muon.isNull() || muon.get() == 0) {
        throw cms::Exception("Assert") << "EmbeddingMuonEfficiency::getEventWeight() got nullptr for muon while using BinnedEfficiencyScaleFactor";
      }
      output = Data(beff->getEventWeight(muon->eta(), isData));
    }

    // Weight is actually the inverse of the efficiency, but do this
    // only if the mode is one of the efficiencies
    EfficiencyScaleFactorBase::Mode mode = fEfficiencyScaleFactor->getMode();
    if(mode == EfficiencyScaleFactorBase::kDataEfficiency || mode == EfficiencyScaleFactorBase::kMCEfficiency) {
      if(output.fWeight != 0.0) {
        output.fWeightAbsUncPlus = output.fWeightAbsUncPlus / (output.fWeight*output.fWeight);
        output.fWeightAbsUncMinus = output.fWeightAbsUncMinus / (output.fWeight*output.fWeight);
        output.fWeight = 1.0/output.fWeight;
      }
    }
    return output;
  }
}
