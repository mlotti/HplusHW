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
  hbheNoiseTokenRun2LooseToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("hbheNoiseTokenRun2LooseSource"))),
  hbheNoiseTokenRun2TightToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("hbheNoiseTokenRun2TightSource"))),
  hbheIsoNoiseToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("hbheIsoNoiseTokenSource"))),
  badPFMuonFilterToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("badPFMuonFilterSource"))),
  badChargedCandidateFilterToken(iConsumesCollector.consumes<bool>(pset.getParameter<edm::InputTag>("badChargedCandidateFilterSource"))),
  bPrintTriggerResultsList(pset.getUntrackedParameter<bool>("printTriggerResultsList")),
  bTriggerResultsListPrintedStatus(false),
  fFilters(pset.getParameter<std::vector<std::string>>("filtersFromTriggerResults"))
  { }

METNoiseFilterDumper::~METNoiseFilterDumper() { }

void METNoiseFilterDumper::book(TTree* tree){
  theTree = tree;
  booked = true;
  
  bFilters = new bool[fFilters.size()+5];
  
  for (size_t i = 0; i < fFilters.size(); ++i) {
    theTree->Branch(("METFilter_"+fFilters[i]).c_str(), &bFilters[i]);
  }
  theTree->Branch("METFilter_hbheNoiseTokenRun2Loose",  &bFilters[fFilters.size()]);
  theTree->Branch("METFilter_hbheNoiseTokenRun2Tight",  &bFilters[fFilters.size()+1]);
  theTree->Branch("METFilter_hbheIsoNoiseToken",        &bFilters[fFilters.size()+2]);
  theTree->Branch("METFilter_badPFMuonFilter",          &bFilters[fFilters.size()+3]);
  theTree->Branch("METFilter_badChargedCandidateFilter",&bFilters[fFilters.size()+4]);
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
  edm::Handle<bool> hbheNoiseLooseHandle;
  iEvent.getByToken(hbheNoiseTokenRun2LooseToken, hbheNoiseLooseHandle);
  bFilters[fFilters.size()] = *hbheNoiseLooseHandle;
  edm::Handle<bool> hbheNoiseTightHandle;
  iEvent.getByToken(hbheNoiseTokenRun2TightToken, hbheNoiseTightHandle);
  bFilters[fFilters.size()+1] = *hbheNoiseTightHandle;
  edm::Handle<bool> hbheIsoNoiseHandle;
  iEvent.getByToken(hbheIsoNoiseToken, hbheIsoNoiseHandle);
  bFilters[fFilters.size()+2] = *hbheIsoNoiseHandle;
  edm::Handle<bool> badPFMuonFilterHandle;
  iEvent.getByToken(badPFMuonFilterToken,badPFMuonFilterHandle);
  bFilters[fFilters.size()+3] = *badPFMuonFilterHandle;
  edm::Handle<bool> badChargedCandidateFilterHandle;
  iEvent.getByToken(badChargedCandidateFilterToken,badChargedCandidateFilterHandle);
  bFilters[fFilters.size()+4] = *badChargedCandidateFilterHandle;
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
