// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BjetSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BjetSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class BjetSelection: public BaseSelection {
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
      Data();
      ~Data();

      const edm::Ptr<pat::Jet>& getBjetTauSide() const { return BjetTauSide; }
      const edm::Ptr<pat::Jet>& getBjetTopSide() const { return BjetTopSide; }

      const bool passedEvent() const { return fPassedEvent; }

      friend class BjetSelection;

    private:
      // Variables
      bool fPassedEvent;
      edm::Ptr<pat::Jet> BjetTauSide;
      edm::Ptr<pat::Jet> BjetTopSide;

    };

    BjetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~BjetSelection();

    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met);
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

    edm::InputTag fSrc;
    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;

    // Histograms
    WrappedTH1 *hDeltaRmaxFromTop;
    WrappedTH1 *hDeltaRtauBtauSide;
    WrappedTH1 *hDeltaRHadTauBtauSide;
    WrappedTH1 *hDeltaRHadTauBtopSide;
    WrappedTH1 *hDeltaMinTauB;
    WrappedTH1 *hDeltaMaxTauB;
    WrappedTH1 *hPtBjetTauSide;
    WrappedTH1 *hEtaBjetTauSide;
    WrappedTH1 *hPtBjetTopSide;
    WrappedTH1 *hEtaBjetTopSide;
    WrappedTH1 *hPtBjetMax;
    WrappedTH1 *hEtaBjetMax;
    WrappedTH1 *hPtBjetMaxTrue;
    WrappedTH1 *hEtaBjetMaxTrue;
    WrappedTH1 *hDeltaMinTauBTrue;
    WrappedTH1 *hDeltaMaxTopBTrue;
    WrappedTH1 *hPtBjetTauSideTrue;
    WrappedTH1 *hEtaBjetTauSideTrue;
    WrappedTH1 *hPtBjetTopSideTrue;
    WrappedTH1 *hBquarkFromTopSideEta;
    WrappedTH1 *hBquarkFromTopSidePt;
    WrappedTH1 *hEtaBjetTopSideTrue;
    WrappedTH1 *hBquarkFromHiggsSideEta;
    WrappedTH1 *hBquarkFromHiggsSidePt;
    WrappedTH1 *hQquarkFromTopSideEta;
    WrappedTH1 *hQquarkFromTopSidePt;

    WrappedTH1 *hDeltaTauB;
    WrappedTH1 *hMassTopTop;
    WrappedTH1 *hMassTopHiggs;
    WrappedTH1 *hMassW;
    WrappedTH1 *hPtTopTop;
    WrappedTH1 *hPtTopHiggs;
    WrappedTH1 *hPtW;

  };
}

#endif
