#include "Framework/interface/BaseSelector.h"

BaseSelector::BaseSelector(const ParameterSet& config):
  fEventCounter(fEventWeight),
  fHistoWrapper(fEventWeight, config.getParameter<std::string>("histogramAmbientLevel", "Vital")),
  fIsMC(false)
{}
BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
}

