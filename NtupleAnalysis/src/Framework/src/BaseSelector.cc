#include "Framework/interface/BaseSelector.h"

BaseSelector::BaseSelector(const ParameterSet& config):
  fEvent(config),
  fEventCounter(fEventWeight),
  fHistoWrapper(fEventWeight, config.getParameter<std::string>("histogramAmbientLevel", "Vital")),
  fPileupWeight(config),
  cBaseAllEvents(fEventCounter.addCounter("Base::AllEvents")),
  fIsMC(config.isMC())
{}
BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
}

void BaseSelector::processInternal(Long64_t entry) {
    fEventWeight.beginEvent();
    // Set event weight as negative is generator weight is negative
    if (fEvent.isMC()) {
      if (fEvent.genWeight().weight() < 0.0) {
        fEventWeight.multiplyWeight(-1.0);
      }
    }
    // NOTE: this counter needs to be right after the generator weight is applied (and no other weights)
    cBaseAllEvents.increment(); 
    
    // PU reweighting
    fEventWeight.multiplyWeight(fPileupWeight.getWeight(fEvent));
    
    // Set prescale event weight // FIXME missing code
    
    process(entry);
  }
