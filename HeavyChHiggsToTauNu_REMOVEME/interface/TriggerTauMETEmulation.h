// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerTauMETEmulation_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerTauMETEmulation_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include "DataFormats/Math/interface/LorentzVector.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/L1Emulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTTauEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTMETEmulation.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class TriggerTauMETEmulation: public BaseSelection {
  public:
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

      bool passedEvent() const { return fPassedEvent; }

      friend class TriggerTauMETEmulation;

    private:
      bool fPassedEvent;
    };

    TriggerTauMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~TriggerTauMETEmulation();

    typedef math::XYZTLorentzVector LorentzVector;

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
    L1Emulation* l1Emulation;
    HLTTauEmulation* hltTauEmulation;
    HLTMETEmulation* hltMETEmulation;
/*
    WrappedTH1* h_alltau;
    WrappedTH1* h_allmet;
    WrappedTH1* h_tau;
    WrappedTH1* h_met;
    WrappedTH1* h_taumet_tau;
    WrappedTH1* h_taumet_met;
*/
    // Counters
//    Count fmetEmulationCutCount;

  };
}

#endif
