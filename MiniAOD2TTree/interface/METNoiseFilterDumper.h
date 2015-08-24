#ifndef METNoiseFilterDumper_h
#define METNoiseFilterDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTree.h"

#include <string>

class METNoiseFilterDumper {
public:
  METNoiseFilterDumper(edm::ParameterSet&);
  ~METNoiseFilterDumper();

  void book(TTree*);
  bool fill(edm::Event&, const edm::EventSetup&);
  void reset();

private:

  bool filter();
  bool useFilter;
  bool booked;

  TTree* theTree;

  const edm::InputTag fTriggerResults;
  //const edm::InputTag edm::InputTag triggerObjects;
  //const edm::InputTag edm::InputTag l1extra;
  const bool fPrintTriggerResultsList;
  bool fTriggerResultsListPrintedStatus;
  
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
  const std::string fCSCTightHaloFilter;
  const std::string fGoodVerticesFilter;
  const std::string fEEBadScFilter;
  // Note: HBHENoiseFilter is run separately as a python fragment
  
  // Data objects for ttree
  bool bPassCSCTightHaloFilter;
  bool bPassGoodVerticesFilter;
  bool bPassEEBadScFilter;
};
#endif
