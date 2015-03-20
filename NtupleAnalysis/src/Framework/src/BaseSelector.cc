#include "Framework/interface/BaseSelector.h"

BaseSelector::BaseSelector(const ParameterSet& config):
  fEventCounter(fEventWeight),
  fHistoWrapper(fEventWeight, config.getParameter<std::string>("histogramAmbientLevel", "Vital")),
  fIsMC(config.isMC())
{
  pileUpWeightPath = config.getParameterOptional<std::string>("PileUpWeight.path");
  pileUpWeightData = config.getParameterOptional<std::string>("PileUpWeight.data");
  pileUpWeightMC   = config.getParameterOptional<std::string>("PileUpWeight.mc");
}
BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
}

