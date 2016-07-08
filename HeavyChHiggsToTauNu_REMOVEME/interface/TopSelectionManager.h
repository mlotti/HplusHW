// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TopSelectionManager_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TopSelectionManager_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionBase.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"

namespace edm {
  class Event;
  class EventSetup;
  class ParameterSet;
}

namespace HPlus {
  class TopSelectionManager {

  private:
    const edm::ParameterSet& iConfig;
    EventCounter& eventCounter;
    HistoWrapper& fHistoWrapper;
    const std::string fTopRecoName;

  public:    
    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef TopSelectionBase::Data Data;
    
    TopSelectionBase* fSelectedAlgorithm;

    TopSelectionManager(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& fHistoWrapper, const std::string topRecoName);
    ~TopSelectionManager();
    
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, edm::Ptr<pat::Jet> bjet, bool bjetPassed);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, edm::Ptr<pat::Jet> bjet, bool bjetPassed);
    bool getPassedTopRecoStatus();
        
  };
}

#endif
