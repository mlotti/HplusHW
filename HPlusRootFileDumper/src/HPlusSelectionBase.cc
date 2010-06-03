#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

namespace HPlusAnalysis {

HPlusSelectionBase::HPlusSelectionBase(const edm::ParameterSet& iConfig) {
  fIsApplied = true;
  fIsHistogrammed = true;
  // Get general settings, if they have been specified
  if (iConfig.exists("IsAppliedStatus")) {
    fIsApplied = iConfig.getParameter<bool>("IsAppliedStatus");
  }
  if (iConfig.exists("IsHistogrammedStatus")) {
    fIsHistogrammed = iConfig.getParameter<bool>("IsHistogrammedStatus");
  }
}

HPlusSelectionBase::~HPlusSelectionBase() {

}

void HPlusSelectionBase::beginJob() {

}

/// Method to apply the event selection; returns true if passed
bool HPlusSelectionBase::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::LogWarning("HPlus") << "Did you forget to add to a selection class the 'filter'-method?";
  return false;
}

void HPlusSelectionBase::endJob() {

}

void HPlusSelectionBase::setOptions(bool isApplied, bool isHistogrammed) {
  fIsApplied = isApplied;
  fIsHistogrammed = isHistogrammed;
}

}
