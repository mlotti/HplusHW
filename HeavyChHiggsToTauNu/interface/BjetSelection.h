// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BjetSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BjetSelection_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;


namespace HPlus {
  class BjetSelection;

  class BjetSelection {
  public:
    typedef math::XYZTLorentzVector XYZTLorentzVector;
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
      Data(const BjetSelection *bjetSelection, bool passedEvent);
      ~Data();

      const edm::Ptr<pat::Jet>& getBjetTauSide() const { return fBjetSelection->BjetTauSide; }
      const edm::Ptr<pat::Jet>& getBjetTopSide() const { return fBjetSelection->BjetTopSide; }

      bool passedEvent() const { return fPassedEvent; }

    private:
      const BjetSelection *fBjetSelection;
      const bool fPassedEvent;
    };
    
    BjetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~BjetSelection();


   
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met);   

  private:
    void init();
    /*
    std::vector<const reco::GenParticle*> getImmediateMothers(const reco::Candidate&);
    std::vector<const reco::GenParticle*> getMothers(const reco::Candidate&);
    bool hasImmediateMother(const reco::Candidate&, int);
    bool hasMother(const reco::Candidate&, int);
    void printImmediateMothers(const reco::Candidate& );
    void printMothers(const reco::Candidate& );
    std::vector<const reco::GenParticle*> getImmediateDaughters(const reco::Candidate&);
    std::vector<const reco::GenParticle*> getDaughters(const reco::Candidate&);
    bool hasImmediateDaughter(const reco::Candidate&, int);
    bool hasDaughter(const reco::Candidate&, int);
    void printImmediateDaughters(const reco::Candidate& );
    void printDaughters(const reco::Candidate& );
    */


    // EventWeight object
    EventWeight& fEventWeight;
    edm::InputTag fSrc;

    
    // Histograms
    TH1 *hDeltaMinTauB;
    TH1 *hDeltaMaxTauB;
    TH1 *hPtBjetTauSide;
    TH1 *hEtaBjetTauSide;
    TH1 *hPtBjetTopSide;
    TH1 *hEtaBjetTopSide;
    TH1 *hDeltaMinTauBTrue;
    TH1 *hDeltaMaxTopBTrue;
    TH1 *hPtBjetTauSideTrue;
    TH1 *hEtaBjetTauSideTrue;
    TH1 *hPtBjetTopSideTrue;
    TH1 *hEtaBjetTopSideTrue;
    TH1 *hBquarkFromHiggsSideEta;
    TH1 *hBquarkFromHiggsSidePt;
    TH1 *hBquarkFromTopSideEta;
    TH1 *hBquarkFromTopSidePt;
    TH1 *hDeltaTauB;
    TH1 *hMassTopTop;
    TH1 *hMassTopHiggs;
    TH1 *hMassW;
    TH1 *hPtTopTop;
    TH1 *hPtTopHiggs;
    TH1 *hPtW;

    // Variables
    edm::Ptr<pat::Jet> BjetTauSide;
    edm::Ptr<pat::Jet> BjetTopSide;
   
  };
}

#endif
