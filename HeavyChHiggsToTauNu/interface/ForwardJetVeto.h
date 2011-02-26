// -*- c++ -*-

#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ForwardJetVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ForwardJetVeto_h

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
  class ForwardJetVeto {
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
      Data(const ForwardJetVeto *forwardJetVeto, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      //      double closestDeltaPhi() const { return fFakeMETVeto->fClosestDeltaPhi; }

    private:
      const  ForwardJetVeto *fForwardJetVeto;
      const bool fPassedEvent;
    };
    
    ForwardJetVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~ForwardJetVeto();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    // Input parameters
    edm::InputTag fSrc;
    edm::InputTag fSrc_met;
    const double  fForwJetEtaCut;
    const double  fForwJetEtCut;
    const double  fEtSumRatioCut;
    const double  fEtaCut;
    const double  fPtCut;
   
   // Counters
    Count fForwardJetSubCount;
    Count fEtSumRatioSubCount;
    Count fEtMetSumRatioSubCount;
 
  

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Data

    
    // Histograms
    TH1 *hMaxForwJetEt;
    TH1 *hForwJetEt;
    TH1 *hForwJetEta;
    TH1 *hEtSumCentral;
    TH1 *hEtSumForward;
    TH1 *hEtSumRatio;
    TH1 *hEtMetSumRatio;
  };
}

#endif
