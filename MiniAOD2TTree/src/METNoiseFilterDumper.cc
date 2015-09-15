#include "HiggsAnalysis/MiniAOD2TTree/interface/METNoiseFilterDumper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include <iostream>

METNoiseFilterDumper::METNoiseFilterDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
: useFilter(false),
  booked(false),
  trgResultsToken(iConsumesCollector.consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("triggerResults"))),
  bPrintTriggerResultsList(pset.getUntrackedParameter<bool>("printTriggerResultsList")),
  bTriggerResultsListPrintedStatus(false),
  fFilters(pset.getParameter<std::vector<std::string>>("filtersFromTriggerResults"))
  { }

METNoiseFilterDumper::~METNoiseFilterDumper() { }

void METNoiseFilterDumper::book(TTree* tree){
  theTree = tree;
  booked = true;
  
  bFilters = new bool[fFilters.size()];
  
  for (size_t i = 0; i < fFilters.size(); ++i) {
    theTree->Branch(("METFilter_"+fFilters[i]).c_str(), &bFilters[i]);
  }
}

bool METNoiseFilterDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  // Obtain trigger results object (some filters have been stored as paths there)
  edm::Handle<edm::TriggerResults> trgResults;
  iEvent.getByToken(trgResultsToken, trgResults);
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*trgResults);
  if (!trgResults.isValid())
    throw cms::Exception("Assert") << "METFilters: edm::TriggerResults object is not valid!";
  // Print info if requested
  if (!bTriggerResultsListPrintedStatus && bPrintTriggerResultsList) {
    printAvailableFilters(iEvent, trgResults);
  }
  // Store results
  for (size_t i = 0; i < fFilters.size(); ++i) {
    bool found = false;
    for (size_t j = 0; j < trgResults->size(); ++j) {
      if (fFilters[i].compare(triggerNames.triggerName(j)) == 0) {
        found = true;
        bFilters[i] = trgResults->accept(j);
      }
    }
    if (!found) {
      printAvailableFilters(iEvent, trgResults);
      throw cms::Exception("Assert") << "METFilters: key '" << fFilters[i] << "' not found in TriggerResults (see above list for available filters)!";
    }
  }
  return filter();
}

void METNoiseFilterDumper::printAvailableFilters(edm::Event& iEvent, edm::Handle<edm::TriggerResults>& trgResults) {
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*trgResults);
  std::cout << "TriggerResults list including METFilters (for information):" << std::endl;
  for (size_t i = 0; i < trgResults->size(); ++i) {
    std::cout << "  " <<  triggerNames.triggerName(i) << " status=" << trgResults->accept(i) << std::endl;
  }
  bTriggerResultsListPrintedStatus = true;
}

bool METNoiseFilterDumper::filter(){
  return true;
}

void METNoiseFilterDumper::reset(){
//   if(booked){
//   }
}