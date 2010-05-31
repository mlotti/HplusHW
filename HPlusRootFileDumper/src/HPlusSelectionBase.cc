#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

namespace HPlusAnalysis {

HPlusSelectionBase::HPlusSelectionBase() {
  fIsApplied = true;
  fIsHistogrammed = true;
}

HPlusSelectionBase::~HPlusSelectionBase() {

}

void HPlusSelectionBase::setup(const edm::ParameterSet& iConfig) { 
  edm::LogWarning("HPlus") << "Did you forget to add to a selection class the 'setup'-method?";
}

void HPlusSelectionBase::setRootTreeBranches(TTree& tree) {
  edm::LogWarning("HPlus") << "Did you forget to add to a selection class the 'setRootTreeBranches'-method?";
}

bool HPlusSelectionBase::apply(const edm::Event& iEvent) {
  edm::LogWarning("HPlus") << "Did you forget to add to a selection class the 'apply'-method?";
  return false;
}

void HPlusSelectionBase::fillRootTreeData(TTree& tree) {
  edm::LogWarning("HPlus") << "Did you forget to add to a selection class the 'fillRootTreeData'-method?";
}

void HPlusSelectionBase::setOptions(bool isApplied, bool isHistogrammed) {
  fIsApplied = isApplied;
  fIsHistogrammed = isHistogrammed;
}

}
