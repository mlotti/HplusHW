#ifndef METNoiseFilterDumper_h
#define METNoiseFilterDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTree.h"

#include <vector>
#include <string>

namespace edm {
  class Handle;
  class TriggerResults;
}

class METNoiseFilterDumper {
public:
  METNoiseFilterDumper(edm::ParameterSet&);
  ~METNoiseFilterDumper();

  void book(TTree*);
  bool fill(edm::Event&, const edm::EventSetup&);
  void reset();

private:
  void printAvailableFilters(edm::Handle<edm::TriggerResults>& trgResults);
  
  bool filter();
  bool useFilter;
  bool booked;

  TTree* theTree;

  const edm::InputTag fTriggerResults;
  //const edm::InputTag edm::InputTag triggerObjects;
  //const edm::InputTag edm::InputTag l1extra;
  const bool bPrintTriggerResultsList;
  bool bTriggerResultsListPrintedStatus;
  
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
  const std::vector<std::string> fFilters;
  // Note: HBHENoiseFilter is run separately as a python fragment
  
  // Data objects for ttree
  std::vector<bool> bFilters;
};
#endif
