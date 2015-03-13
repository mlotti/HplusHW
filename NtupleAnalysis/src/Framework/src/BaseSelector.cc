#include "Framework/interface/BaseSelector.h"

BaseSelector::BaseSelector(const ParameterSet& config):
  fEventCounter(fEventWeight),
  fHistoWrapper(fEventWeight, config.getParameter<std::string>("histogramAmbientLevel", "Vital")),
  fIsMC(false)
{
  boost::optional<std::string> pileUpWeightPath = config.getParameterOptional<std::string>("PileUpWeight.path");
  boost::optional<std::string> pileUpWeightData = config.getParameterOptional<std::string>("PileUpWeight.data");
  boost::optional<std::string> pileUpWeightMC   = config.getParameterOptional<std::string>("PileUpWeight.mc");
  if(pileUpWeightPath && pileUpWeightData && pileUpWeightMC)
     fPileupWeight.set(*pileUpWeightPath,*pileUpWeightData,*pileUpWeightMC,this->isData());
}
BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
}

