// -*- c++ -*-

#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FakeMETVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FakeMETVeto_h

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
  class FakeMETVeto: public BaseSelection {
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

      const bool passedEvent() const { return fPassedEvent; }
      const double closestDeltaPhi() const { return fClosestDeltaPhi; }
      const double closestDeltaPhiToJets() const { return fClosestDeltaPhiToJets; }
      const double closestDeltaPhiToTaus() const { return fClosestDeltaPhiToTaus; }

      friend class FakeMETVeto;

    private:
      bool fPassedEvent;

      /// Smallest DeltaPhi of MET and selected jets or tau
      double fClosestDeltaPhi;
      double fClosestDeltaPhiToJets;
      double fClosestDeltaPhiToTaus;
    };

    FakeMETVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~FakeMETVeto();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup,  const edm::Ptr<reco::Candidate>& tau , const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup,  const edm::Ptr<reco::Candidate>& tau , const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup,  const edm::Ptr<reco::Candidate>& tau , const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met);

    // Input parameters
    const double fMinDeltaPhi;

    // Counters
    //Count f;

    // Data

    // Histograms
    WrappedTH1 *hClosestDeltaPhi;
    WrappedTH1 *hClosestDeltaPhiToJets;
    WrappedTH1 *hClosestDeltaPhiToTaus;
    WrappedTH1 *hClosestDeltaPhiZoom;
    WrappedTH1 *hClosestDeltaPhiToJetsZoom;
    WrappedTH1 *hClosestDeltaPhiToTausZoom;
  };
}

#endif
