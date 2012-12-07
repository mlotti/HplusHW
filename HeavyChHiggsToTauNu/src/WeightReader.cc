#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"

namespace HPlus {
  WeightReader::WeightReader(const edm::ParameterSet& iConfig):
    fWeightSrc(iConfig.getParameter<edm::InputTag>("weightSrc")),
    fEnabled(iConfig.getParameter<bool>("enabled")) {
  }
  WeightReader::~WeightReader() {}

  double WeightReader::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    if (!fEnabled)
      return 1.0;
    edm::Handle<double> myWeightHandle;
    iEvent.getByLabel(fWeightSrc, myWeightHandle);
    return *myWeightHandle;
  }
}
