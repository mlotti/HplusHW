#include "Framework/interface/BaseSelector.h"

BaseSelector::BaseSelector(const ParameterSet& config):
  fEvent(config),
  fEventCounter(fEventWeight),
  fHistoWrapper(fEventWeight, config.getParameter<std::string>("histogramAmbientLevel", "Vital")),
  fPileupWeight(config),
  cBaseAllEvents(fEventCounter.addCounter("Base::AllEvents")),
  cPileupWeighted(fEventCounter.addCounter("Base::PUReweighting")),
  cPrescaled(fEventCounter.addCounter("Base::Prescale")),
  cTopPtReweighted(fEventCounter.addCounter("Base::Weighted events with top pT")),
  cExclusiveSamplesWeighted(fEventCounter.addCounter("Base::Weighted events for exclusive samples")),
  fIsMC(config.isMC())
{}
BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
}

void BaseSelector::bookInternal(TDirectory *dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, "Weighting");
  hNvtxBeforeVtxReweighting = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, 
    "NvtxBeforeVtxReweighting", "NvtxBeforeVtxReweighting;N_{vertices};N_{events}", 60, 0, 60);
  hNvtxAfterVtxReweighting = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, 
    "NvtxAfterVtxReweighting", "NvtxAfterVtxReweighting;N_{vertices};N_{events}", 60, 0, 60);
}

void BaseSelector::processInternal(Long64_t entry) {
  fEventWeight.beginEvent();
  //====== Set event weight as negative is generator weight is negative
  if (fEvent.isMC()) {
    if (fEvent.genWeight().weight() < 0.0) {
      fEventWeight.multiplyWeight(-1.0);
    }
  }
  // NOTE: this counter needs to be right after the generator weight is applied (and no other weights)
  cBaseAllEvents.increment(); 
  
  //====== PU reweighting
  hNvtxBeforeVtxReweighting->Fill(fEvent.vertexInfo().value());
  fEventWeight.multiplyWeight(fPileupWeight.getWeight(fEvent));
  //std::cout << "vtx: " << fPileupWeight.getWeight(fEvent) << std::endl;;
  hNvtxAfterVtxReweighting->Fill(fEvent.vertexInfo().value());
  
  //====== Set prescale event weight // FIXME missing code
  cPileupWeighted.increment();
  
  //====== Top pT weighting // FIXME missing code
  if (fEvent.isMC()) {
    cTopPtReweighted.increment();
  }
  
  //====== Combining of W+jets and Z+jets inclusive and exclusive samples // FIXME missing code
  cExclusiveSamplesWeighted.increment();

  
  process(entry);
}
