// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerMETEmulation.h"

#include <string>
#include <vector>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
  class TriggerResults;
  class TriggerNames;
}

namespace pat {
  class TriggerEvent;
}

class TH1;

namespace HPlus {
  class EventWeight;
  class EventCounter;

  class TriggerSelection {
  enum TriggerSelectionType {
    kTriggerSelectionByTriggerBit,
    kTriggerSelectionDisabled
  };
  
  public:
    class Data;
    class TriggerPath {
    public:
      TriggerPath(const std::string& path, EventCounter& eventCounter);
      ~TriggerPath();

      bool analyze(const pat::TriggerEvent& trigger);
      bool analyze(const edm::TriggerResults& trigger, const edm::TriggerNames& triggerNames);

      const std::string& getPathName() const { return fPath; }
      const pat::TriggerObjectRefVector getTauObjects() const { return fTaus; }
      const pat::TriggerObjectRefVector getMetObjects() const { return fMets; }

    private:
      // Input parameters
      std::string fPath;

      // Counters
      Count fTriggerCount;

      pat::TriggerObjectRefVector fMets;
      pat::TriggerObjectRefVector fTaus;
    };

      /**
     * Class to encapsulate the access to the data members of
     * TauSelection. If you want to add a new accessor, add it here
     * and keep all the data of TauSelection private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data(const TriggerSelection *triggerSelection, const TriggerPath *triggerPath, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }

      pat::TriggerObjectRef getHltMetObject() const {
        return fTriggerSelection->fHltMet;
      }

      size_t getTriggerTauSize() const {
        return fTriggerPath->getTauObjects().size();
      }

    private:
      const TriggerSelection *fTriggerSelection;
      const TriggerPath *fTriggerPath;
      const bool fPassedEvent;
    };

    TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TriggerSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
  private:
    bool passedTriggerBit(const edm::Event& iEvent, const edm::EventSetup& iSetup, TriggerPath*& returnPath);

  private:
    std::vector<TriggerPath* > triggerPaths;
    const edm::InputTag fTriggerSrc;
    const edm::InputTag fPatSrc;
    const double fMetCut;

    EventWeight& fEventWeight;
    TriggerMETEmulation fTriggerCaloMet;
    
    // Counters
    Count fTriggerAllCount;
    Count fTriggerPathCount;
    Count fTriggerBitCount;
    Count fTriggerCaloMetCount;
    Count fTriggerCount;

    Count fTriggerHltMetExistsCount;
    Count fTriggerHltMetPassedCount;

    TriggerSelectionType fTriggerSelectionType;
    
    // Histograms
    TH1 *hHltMetBeforeTrigger;
    TH1 *hHltMetAfterTrigger;
    TH1 *hHltMetSelected;
    TH1 *hTriggerParametrisationWeight;
    TH1 *hControlSelectionType;

    // Analysis results
    pat::TriggerObjectRef fHltMet;

    bool fThrowIfNoMet;
  };
}

#endif
