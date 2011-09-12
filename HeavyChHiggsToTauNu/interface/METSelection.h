// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class METSelection {
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
      Data(const METSelection *metSelection, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const edm::Ptr<reco::MET> getSelectedMET() const { return fMETSelection->fSelectedMET; }
    
    private:
      const METSelection *fMETSelection;
      const bool fPassedEvent;
    };
    
    METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label);
    ~METSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
  private:
    // Input parameters
    edm::InputTag fSrc;
    double fMetCut;

    // Counters
    Count fMetCutCount;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Histograms
    TH1 *hMet;
    TH1 *hMetSignif;
    TH1 *hMetSumEt;
    TH1 *hMetDivSumEt;
    TH1 *hMetDivSqrSumEt;

    // Selected jets
    edm::Ptr<reco::MET> fSelectedMET;
  };
}

#endif
