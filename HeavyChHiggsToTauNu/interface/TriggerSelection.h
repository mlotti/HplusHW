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
    kTriggerSelectionByTriggerBitApplyScaleFactor,
    kTriggerSelectionByTriggerEfficiencyParametrisation,
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

        private:
            // Input parameters
            std::string fPath;

            // Counters
            Count fTriggerCount;
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
      double getScaleFactor() const { return fTriggerSelection->fScaleFactor; }

      pat::TriggerObjectRef getHltMetObject() const {
        return fTriggerSelection->fHltMet;
      }

    private:
      const TriggerSelection *fTriggerSelection;
      const TriggerPath *fTriggerPath;
      const bool fPassedEvent;
    };

    class TriggerScaleFactor {
    public:
      TriggerScaleFactor();
      ~TriggerScaleFactor();

      void setValue(double ptLowEdge, double dataEff, double dataUncertainty, double MCEff, double MCUncertainty);
      double getScaleFactor(double tauPt) const;
      double getScaleFactorRelativeUncertainty(double tauPt) const;

    private:
      size_t obtainIndex(double pt) const;

      std::vector<double> fTriggerEffPtBinEdge;
      std::vector<double> fTriggerEffDataValues;
      std::vector<double> fTriggerEffDataUncertainty;
      std::vector<double> fTriggerEffMCValues;
      std::vector<double> fTriggerEffMCUncertainty;
    };


    TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TriggerSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    bool passedTriggerBit(const edm::Event& iEvent, const edm::EventSetup& iSetup, TriggerPath*& returnPath);
    bool passedTriggerScaleFactor(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    //bool passedTriggerParametrisation(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    std::vector<TriggerPath* > triggerPaths;
    const edm::InputTag fTriggerSrc;
    const edm::InputTag fPatSrc;
    const double fMetCut;

    EventWeight& fEventWeight;
    TauSelection fTriggerTauSelection;
    METSelection fTriggerMETSelection;
    TriggerEfficiency fTriggerEfficiency;
    TriggerMETEmulation fTriggerCaloMet;
    
    // Counters
    Count fTriggerAllCount;
    Count fTriggerPathCount;
    Count fTriggerBitCount;
    Count fTriggerCaloMetCount;
    Count fTriggerCount;

    Count fTriggerHltMetExistsCount;

    Count fTriggerScaleFactorAllCount;
    Count fTriggerScaleFactorAppliedCount;

    Count fTriggerParamAllCount;
    Count fTriggerParamTauCount;
    Count fTriggerParamMetCount;

    TriggerSelectionType fTriggerSelectionType;
    TriggerScaleFactor fTriggerScaleFactor;
    
    // Histograms
    TH1 *hHltMetBeforeTrigger;
    TH1 *hHltMetAfterTrigger;
    TH1 *hHltMetSelected;
    TH1 *hTriggerParametrisationWeight;
    TH1 *hControlSelectionType;

    TH1 *hScaleFactor;
    TH1 *hScaleFactorUncertainty;

    // Analysis results
    pat::TriggerObjectRef fHltMet;

    bool fThrowIfNoMet;
    double fScaleFactor;
  };
}

#endif
