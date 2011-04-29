// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_JetTauInvMass_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_JetTauInvMass_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"

namespace edm {
  class ParameterSet;
}

class TH1;

namespace HPlus {

  class JetTauInvMass {
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
      Data(const JetTauInvMass *jetTauInvMass, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      //      const edm::PtrVector<pat::Jet>& getSelectedJets() const { return fJetTauInvMass->fSelectedJets; }
      //      const edm::PtrVector<pat::Jet>& getSelectedTaus() const { return fJetTauInvMass->fSelectedTaus; }
      //      const int getBJetCount() const { return fBTagging->iNBtags; }

    private:
      const JetTauInvMass *fJetTauInvMass;
      const bool fPassedEvent;
    };
    
    JetTauInvMass(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~JetTauInvMass();

    //    Data analyze(const edm::PtrVector<pat::Jet>& taus, const edm::PtrVector<pat::Jet>& jets);
    Data analyze(const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets);



  private:
    // Input parameters
    const double fMinMass;

    // Counters
    Count fInvMassCutCount;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Histograms
    TH1 *hTauJetMass;

    // Selected jets
    //    edm::PtrVector<pat::Jet> fSelectedJets;
    //    int iNBtags;
  };
}

#endif
