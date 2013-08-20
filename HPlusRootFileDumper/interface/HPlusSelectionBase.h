#ifndef HPLUSANALYSISHPLUSSELECTIONBASE_H
#define HPLUSANALYSISHPLUSSELECTIONBASE_H

// system include files
#include <memory>
#include <iostream>

#include "HiggsAnalysis/HPlusRootFileDumper/interface/Counter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

namespace HPlusAnalysis {

/**
Base class for H+ analysis

	@author Lauri Wendland
*/
class HPlusSelectionBase : public edm::EDFilter { // FIXME: Derive the class from EDFilter
 public:
  HPlusSelectionBase(const edm::ParameterSet& iConfig);
  ~HPlusSelectionBase();
  
  virtual void beginJob();
  /// Method to apply the event selection; returns true if passed
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  
  virtual void endJob();
  
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
