#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

#include <limits>

namespace HPlus {
  typedef TopSelectionBase::Data Data;

  //constructor and desturctor
  TopSelectionBase::TopSelectionBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper) {}
  TopSelectionBase::~TopSelectionBase() {}

  //constructor and destructor for TopSelectionBase::Data class
  TopSelectionBase::Data::Data():
    fPassedEvent(false) {}
  TopSelectionBase::Data::~Data() {}
  
  //analyze
  Data TopSelectionBase::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<pat::Jet> iJetb) {
    return privateAnalyze(iEvent, iSetup, jets, bjets, iJetb);
  }
 

  //privateAnalyze (dummy)
  Data TopSelectionBase::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<pat::Jet> iJetb) {
    Data output;
    return output;
  }

}
