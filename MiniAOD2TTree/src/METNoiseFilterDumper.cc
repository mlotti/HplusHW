#include "HiggsAnalysis/MiniAOD2TTree/interface/METNoiseFilterDumper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/Handle.h"

#include <iostream>

METNoiseFilterDumper::METNoiseFilterDumper(edm::ParameterSet& pset)
: booked(false),
  fTriggerResults(pset.getParameter<edm::InputTag>("triggerResults")),
  bPrintTriggerResultsList(pset.getUntrackedParameter<bool>("printTriggerResultsList")),
  bTriggerResultsListPrintedStatus(false),
  fCSCTightHaloFilter(pset.getParameter<std::string>("CSCTightHaloFilter")),
  fGoodVerticesFilter(pset.getParameter<std::string>("goodVerticesFilter")),
  fEEBadScFilter(pset.getParameter<std::string>("EEBadScFilter"))
  { }

METNoiseFilterDumper::~METNoiseFilterDumper() { }

void METNoiseFilterDumper::book(TTree* tree){
  theTree = tree;
  booked = true;
  theTree->Branch("METFilter_CSCTightHaloFilter",&bPassCSCTightHaloFilter);
  theTree->Branch("METFilter_GoodVerticesFilter",&bPassGoodVerticesFilter);
  theTree->Branch("METFilter_EEBadScFilter",&bPassEEBadScFilter);
}

bool METNoiseFilterDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  // Obtain trigger results object (some filters have been stored as paths there)
  edm::Handle<edm::TriggerResults> trgResults;
  iEvent.getByLabel(fTriggerResults, trgResults);
  if (!trgResults.isValid())
    throw cms::Exception("Assert") << "METFilters: edm::TriggerResults object is not valid!";
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*trgResults);
  if (!bTriggerResultsListPrintedStatus && bPrintTriggerResultsList) {
    std::cout << "TriggerResults list including METFilters (for information):" << std::endl;
    for (size_t i = 0; i < trgResults->size(); ++i) {
      std::cout << "  " <<  triggerNames.triggerName(i) << " status=" << trgResults->accept(i) << std::endl;
    }
    bTriggerResultsListPrintedStatus = true;
  }
  return filter();
}

bool METNoiseFilterDumper::filter(){
  return true;
}

void METNoiseFilterDumper::reset(){
// if(booked){
// }
}
