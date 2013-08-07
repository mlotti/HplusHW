#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

#include <limits>

namespace HPlus {

  //constructor and destructor for TopSelectionBase::Data class
  TopSelectionBase::Data::Data():
    fPassedEvent(false) {}
  virtual TopSelection::Data::~Data() {}
  
  }
  
  //silentAnalyze
  TopSelectionBase::Data TopSelectionBase::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, jets, bjets);
  }

  //analyze
  TopSelectionBase::Data TopSelectionBase::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets, bjets);
  }
 
  private:
  //virtual privateAnalyze: defined separately for every topreco algorithm
  virtual TopSelectionBase::Data TopSelectionBase::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    Data output = 0;
  
}  
