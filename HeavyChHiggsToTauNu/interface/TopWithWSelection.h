// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TopWithWSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TopWithWSelection_h

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
  class TopWithWSelection;

  class TopWithWSelection {
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
      Data(const TopWithWSelection *TopWithWSelection, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const double getTopMass() const { return fTopWithWSelection->topMass; }
      const XYZTLorentzVector& getTopP4() const { return fTopWithWSelection->top; }

    private:
      const TopWithWSelection *fTopWithWSelection;
      const bool fPassedEvent;
    };
    
    TopWithWSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TopWithWSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> bjet);

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
    
    // Input parameters
    const double fTopMassLow;
    const double fTopMassHigh;
    const double fChi2Cut;

    // Counters
    Count fTopWithWMassCount;

    // EventWeight object
    EventWeight& fEventWeight;
    edm::InputTag fSrc;
    
    // Histograms
    TH1 *hPtTopChiCut;
    TH1 *hPtTop;
    TH1 *hjjMass;
    TH1 *htopMass;
    TH1 *htopMassMatch;
    TH1 *htopMassChiCut;
    TH1 *hWMass;
    TH1 *hWMassMatch;
    TH1 *hWMassChiCut;
    TH1 *hChi2Min;
    TH1 *htopMassBMatch;
    TH1 *hWMassBMatch;
    TH1 *htopMassQMatch;
    TH1 *hWMassQMatch;
    TH1 *htopMassMatchWrongB;
    TH1 *hWMassMatchWrongB;    
  
    // Variables
    double topMass;
    double wMass;
    XYZTLorentzVector top;
    XYZTLorentzVector W;
  };
}

#endif
