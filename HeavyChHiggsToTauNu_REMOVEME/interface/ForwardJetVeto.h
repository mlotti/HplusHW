// -*- c++ -*-

#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ForwardJetVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ForwardJetVeto_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/METReco/interface/MET.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  /**
   * Class for checking the smallest DeltaPhi of the MET and the selected jets and 
   */
  class ForwardJetVeto: public BaseSelection {
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
      //      double closestDeltaPhi() const { return fFakeMETVeto->fClosestDeltaPhi; }

      friend class ForwardJetVeto;
    private:
      bool fPassedEvent;
    };

    ForwardJetVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~ForwardJetVeto();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::MET>& met);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::MET>& met);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::MET>& met);

    // Input parameters
    edm::InputTag fSrc;
    const double  fForwJetEtaCut;
    const double  fForwJetEtCut;
    const double  fEtSumRatioCut;
    const double  fEtaCut;
    const double  fPtCut;
   
   // Counters
    Count fForwardJetSubCount;
    Count fEtSumRatioSubCount;
    Count fEtMetSumRatioSubCount;
 
    // Data

    // Histograms
    WrappedTH1 *hMaxForwJetEt;
    WrappedTH1 *hForwJetEt;
    WrappedTH1 *hForwJetEta;
    WrappedTH1 *hEtSumCentral;
    WrappedTH1 *hEtSumForward;
    WrappedTH1 *hEtSumRatio;
    WrappedTH1 *hEtMetSumRatio;
  };
}

#endif
