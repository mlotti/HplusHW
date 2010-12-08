// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerTauMETEmulation_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerTauMETEmulation_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "DataFormats/Math/interface/LorentzVector.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class TriggerTauMETEmulation {
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
      Data(const TriggerTauMETEmulation* TriggerTauMETEmulation, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }

    private:
      const TriggerTauMETEmulation *fTriggerTauMETEmulation;
      const bool fPassedEvent;
    };
    
    TriggerTauMETEmulation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TriggerTauMETEmulation();

    typedef math::XYZTLorentzVector LorentzVector;

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
/*
    const edm::Ptr<reco::MET> getSelectedMET() const {
      return fSelectedTriggerMET;
    }
*/
  private:
    bool tauSelection(const edm::Event&);
    bool metSelection(const edm::Event&);
    bool HLTTauFound(const edm::Event&,const LorentzVector&);

    // Input parameters
    edm::InputTag l1tauSrc;
    edm::InputTag l1cenSrc;
    edm::InputTag tauSrc;
    edm::InputTag metSrc;

    double l1tauPtCut;
    double l1cenPtCut;
    double tauPtCut;
    double tauLTrkCut;
    double metCut;
/*
    TH1* h_alltau;
    TH1* h_allmet;
    TH1* h_tau;
    TH1* h_met;
    TH1* h_taumet_tau;
    TH1* h_taumet_met;
*/
    // Counters
//    Count fmetEmulationCutCount;

    // Event weight object
    EventWeight& fEventWeight;

    // Histograms
//    TH1 *hMetBeforeEmulation;
//    TH1 *hMetAfterEmulation;

    // Selected jets
//    edm::Ptr<reco::MET> fSelectedTriggerMET;
  };
}

#endif
