#ifndef HPLUSANALYSISHPLUSSELECTIONBASE_H
#define HPLUSANALYSISHPLUSSELECTIONBASE_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/Counter.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Event.h"

#include "TTree.h"

namespace HPlusAnalysis {

/**
Base class for H+ analysis

	@author Lauri Wendland
*/
class HPlusSelectionBase { // FIXME: Derive the class from EDFilter
 public:
  HPlusSelectionBase();
  ~HPlusSelectionBase();
  
  /// Method to set configuration related things
  virtual void setup(const edm::ParameterSet& iConfig);
  /// Method for setting ROOT tree branches
  virtual void setRootTreeBranches(TTree& tree);
  /// Method to apply the event selection; returns true if passed
  virtual bool apply(const edm::Event& iEvent);
  /// Method for filling ROOT tree branches with data
  virtual void fillRootTreeData(TTree& tree);
  
  /// Setter for options
  void setOptions(bool isApplied = true, bool isHistogrammed = true);
  /// Returns true, if selection is to be applied
  bool isApplied() const { return fIsApplied; }
  /// Returns true, if selection histograms are to be drawn
  bool isHistogrammed() const { return fIsHistogrammed; }
  
 protected:
  /// True, if the cut is applied
  bool fIsApplied;
  /// True, if the histograms of the cut are to be drawn
  bool fIsHistogrammed;
  
};

}

#endif
