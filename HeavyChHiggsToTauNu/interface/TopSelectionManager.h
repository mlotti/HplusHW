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
  public:    
    typedef math::XYZTLorentzVector XYZTLorentzVector;
    typedef TopSelectionBase::Data Data;
    //counters
    //Count fTopSelectionCounter;
    //Count fTopChiSelectionCounter;
    //Count fTopWithBSelectionCounter;
    //Count fTopWithWSelectionCounter;
    //Count fTopWithMHSelectionCounter;
    
    //top selection algorithms
    TopSelection fTopSelection;
    TopChiSelection fTopChiSelection;
    TopWithBSelection fTopWithBSelection;
    TopWithWSelection fTopWithWSelection;
    //TopWithMHSelection fTopWithMHSelection;

    TopSelectionManager(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& fHistoWrapper, const std::string topRecoName);
    ~TopSelectionManager();
    
    //function declarations
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, edm::Ptr<pat::Jet> bjet, bool bjetPassed);
    bool getPassedTopRecoStatus();
    
  private:
    bool myTopRecoWithWSelectionStatus; //TODO is this needed?
    const std::string fTopRecoName;
    //Data TopSelectionData; //declared in cc
  };
}

#endif
