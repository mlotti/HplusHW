#include "Framework/interface/BaseSelector.h"

BaseSelector::BaseSelector(const boost::property_tree::ptree& config):
  fEventCounter(fEventWeight),
  fHistoWrapper(fEventWeight, config.get("histogramAmbientLevel", "Vital")),
  fIsMC(false)
{}
BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
}

