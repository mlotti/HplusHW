#include "Framework/interface/BaseSelector.h"

BaseSelector::BaseSelector(const ParameterSet& config):
  fEvent(config),
  fEventCounter(fEventWeight),
  fHistoWrapper(fEventWeight, config.getParameter<std::string>("histogramAmbientLevel", "Vital")),
  fPileupWeight(config),
  fIsMC(config.isMC())
{}
BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
}

