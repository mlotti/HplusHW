// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
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

namespace HPlus {
  class EventCounter;
  class HistoWrapper;
  class WrappedTH1;

  class TriggerSelection: public BaseSelection {
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
      const pat::TriggerObjectRefVector& getTauObjects() const { return fTaus; }
      const pat::TriggerObjectRefVector& getMetObjects() const { return fMets; }

    private:
      // Input parameters
      std::string fPath;

      // Counters
      Count fTriggerPathFoundCount;
      Count fTriggerPathAcceptedCount;

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
      Data();
      ~Data();

      const bool passedEvent() const { return fPassedEvent; }
      const pat::TriggerObjectRef getL1MetObject() const { return fL1Met; }
      const pat::TriggerObjectRef getHltMetObject() const { return fHltMet; }
      const bool hasTriggerPath() const { return fHasTriggerPath; }
      const size_t getTriggerTauSize() const { return fHltTaus.size(); }
      const pat::TriggerObjectRefVector& getTriggerTaus() const { return fHltTaus; }

      friend class TriggerSelection;

    private:
      // Analysis results
      pat::TriggerObjectRef fL1Met;
      pat::TriggerObjectRef fHltMet;
      pat::TriggerObjectRefVector fHltTaus;

      bool fHasTriggerPath;
      bool fPassedEvent;
    };

    TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~TriggerSelection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    bool passedTriggerBit(const edm::Event& iEvent, const edm::EventSetup& iSetup, TriggerPath*& returnPath, TriggerSelection::Data& output);

  private:
    std::vector<TriggerPath* > triggerPaths;
    const edm::InputTag fTriggerSrc;
    const edm::InputTag fPatSrc;
    std::string fL1MetCollection;
    const double fL1MetCut;
    const double fMetCut;

    TriggerMETEmulation fTriggerCaloMet;

    // Counters
    Count fTriggerAllCount;
    Count fTriggerPathCount;
    Count fTriggerBitCount;
    Count fTriggerCaloMetCount;
    Count fTriggerCount;

    Count fTriggerDebugAllCount;
    Count fTriggerL1MetPassedCount;
    Count fTriggerHltMetExistsCount;
    Count fTriggerHltMetPassedCount;

    TriggerSelectionType fTriggerSelectionType;
    
    // Histograms
    WrappedTH1 *hHltMetBeforeTrigger;
    WrappedTH1 *hHltMetAfterTrigger;
    WrappedTH1 *hHltMetSelected;
    WrappedTH1 *hTriggerParametrisationWeight;
    WrappedTH1 *hControlSelectionType;


    bool fThrowIfNoMet;
  };
}

#endif
