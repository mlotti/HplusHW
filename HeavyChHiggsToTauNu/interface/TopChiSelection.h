// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TopChiSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TopChiSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class Event;
  class EventSetup;
  class ParameterSet;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class TopChiSelection: public BaseSelection {
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

      const bool passedEvent() const { return fPassedEvent; }
      const double getTopMass() const { return top.M(); }
      const double getWMass() const { return W.M(); }
      const XYZTLorentzVector& getTopP4() const { return top; }
      const XYZTLorentzVector& getWP4() const { return W; }
      const edm::Ptr<pat::Jet>& getSelectedBjet() const { return bjetInTop; }

      friend class TopChiSelection;

    private:
      bool fPassedEvent;
      // Variables
      XYZTLorentzVector top;
      XYZTLorentzVector W;
      edm::Ptr<pat::Jet> bjetInTop;
    };
    
    TopChiSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~TopChiSelection();

     // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);
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
    // Input parameters
    const double fTopMassLow;
    const double fTopMassHigh;
    const double fChi2Cut;

    // Counters
    Count fTopChiMassCount;

    edm::InputTag fSrc;
    
    // Histograms
    
    WrappedTH1 *hPtTopChiCut;
    WrappedTH1 *hPtTop;
    WrappedTH1 *hjjbMass;
    WrappedTH1 *htopMass;
    WrappedTH1 *htopMassMatch;
    WrappedTH1 *htopMassChiCut;
    WrappedTH1 *hWMass;
    WrappedTH1 *hWMassMatch;
    WrappedTH1 *hWMassChiCut;
    WrappedTH1 *hChi2Min;
    WrappedTH1 *htopMassBMatch;
    WrappedTH1 *hWMassBMatch;
    WrappedTH1 *htopMassQMatch;
    WrappedTH1 *hWMassQMatch;
    WrappedTH1 *htopMassMatchWrongB;
    WrappedTH1 *hWMassMatchWrongB;

  };
}

#endif
