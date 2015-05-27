// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_JetTauInvMass_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_JetTauInvMass_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class JetTauInvMass: public BaseSelection {
  public:
    /**
     * Class to encapsulate the access to the data members.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data();
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      //      const edm::PtrVector<pat::Jet>& getSelectedJets() const { return fJetTauInvMass->fSelectedJets; }
      //      const edm::PtrVector<pat::Jet>& getSelectedTaus() const { return fJetTauInvMass->fSelectedTaus; }
      //      const int getBJetCount() const { return fBTagging->iNBtags; }

      friend class JetTauInvMass;

    private:
      bool fPassedEvent;
    };

    JetTauInvMass(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~JetTauInvMass();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets);

    // Input parameters
    const double fMassResolution;

    // Counters
    Count fInvMassCutCount;

    // Histograms
    WrappedTH1 *hTauJetMass;
    WrappedTH1 *hClosestMass;

    // Selected jets
    //    edm::PtrVector<pat::Jet> fSelectedJets;
    //    int iNBtags;
  };
}

#endif
