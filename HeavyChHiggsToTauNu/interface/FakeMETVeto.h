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
   * Class for checking the smallest DeltaR of the MET and the selected jets and 
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
      double closestDeltaR() const { return fFakeMETVeto->fClosestDeltaR; }

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
    const double fMaxDeltaR;

    // Counters
    //Count f;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Data
    /// Smallest DeltaR of MET and selected jets or tau
    double fClosestDeltaR;
    double fClosestDeltaRToJets;
    double fClosestDeltaRToTaus;
    
    // Histograms
    TH1 *hClosestDeltaR;
    TH1 *hClosestDeltaRToJets;
    TH1 *hClosestDeltaRToTaus;
  };
}

#endif
