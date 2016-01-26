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
  fIsMC(config.isMC()),
  bIsttbar(false),
  iTopPtVariation(0)
{
  boost::optional<std::string> flag = config.getParameterOptional<std::string>("topPtSystematicVariation");
  if (flag) {
    if (*flag== "plus") {
      iTopPtVariation = 1;
    } else if (*flag == "minus") {
      iTopPtVariation = -1;
    }
  }
}

BaseSelector::~BaseSelector() {
  fEventCounter.serialize();
  delete hNvtxBeforeVtxReweighting;
  delete hNvtxAfterVtxReweighting;
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
  if (fEvent.isMC() && fEvent.vertexInfo().branchesExist()) {
    hNvtxBeforeVtxReweighting->Fill(fEvent.vertexInfo().value());
    fEventWeight.multiplyWeight(fPileupWeight.getWeight(fEvent));
    //std::cout << "vtx: " << fPileupWeight.getWeight(fEvent) << std::endl;;
    hNvtxAfterVtxReweighting->Fill(fEvent.vertexInfo().value());
  }
  cPileupWeighted.increment();
  
  //====== Set prescale event weight // not needed right now
  cPrescaled.increment();
  
  //====== Top pT weighting
  if (fEvent.isMC() && isttbar()) {
    // For down variation, do not apply weight
    if (iTopPtVariation == 0) {
      fEventWeight.multiplyWeight(std::abs(fEvent.topPtWeight().weight()));
    } else if (iTopPtVariation == 1) {
      // For up variation, apply weight twice 
      fEventWeight.multiplyWeight(fEvent.topPtWeight().weight() * fEvent.topPtWeight().weight());
    }
  }
  cTopPtReweighted.increment();
  
  //====== Combining of W+jets and Z+jets inclusive and exclusive samples // not needed right now
  cExclusiveSamplesWeighted.increment();

  process(entry);
}
