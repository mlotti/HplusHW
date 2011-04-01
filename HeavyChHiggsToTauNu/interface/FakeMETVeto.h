// -*- c++ -*-

#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FakeMETVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FakeMETVeto_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/METReco/interface/MET.h"

#include "TH1.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  /**
   * Class for checking the smallest DeltaPhi of the MET and the selected jets and 
   */
  class FakeMETVeto {
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
      Data(const FakeMETVeto *fakeMETVeto, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      double closestDeltaPhi() const { return fFakeMETVeto->fClosestDeltaPhi; }

    private:
      const FakeMETVeto *fFakeMETVeto;
      const bool fPassedEvent;
    };
    
    FakeMETVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~FakeMETVeto();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<pat::Jet>& jets);

  private:
    // Input parameters
    edm::InputTag fSrc;
    const double fMinDeltaPhi;

    // Counters
    //Count f;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Data
    /// Smallest DeltaPhi of MET and selected jets or tau
    double fClosestDeltaPhi;
    double fClosestDeltaPhiToJets;
    double fClosestDeltaPhiToTaus;
    
    // Histograms
    TH1 *hClosestDeltaPhi;
    TH1 *hClosestDeltaPhiToJets;
    TH1 *hClosestDeltaPhiToTaus;
    TH1 *hClosestDeltaPhiZoom;
    TH1 *hClosestDeltaPhiToJetsZoom;
    TH1 *hClosestDeltaPhiToTausZoom;
  };
}

#endif
