// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TopSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TopSelection_h

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
  class TopSelection;

  class TopSelection {
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
      Data(const TopSelection *TopSelection, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const double getTopMass() const { return fTopSelection->topMass; }
      const XYZTLorentzVector& getTopP4() const { return fTopSelection->top; }

    private:
      const TopSelection *fTopSelection;
      const bool fPassedEvent;
    };
    
    TopSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TopSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);

  private:
    // Input parameters
    const double fTopMassLow;
    const double fTopMassHigh;
    edm::InputTag fSrc;

    // Counters
    Count fTopMassCount;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Histograms
    TH1 *hPtjjb;
    TH1 *hPtmax;
    TH1 *hjjbMass;
    TH1 *htopMass;
    TH1 *hPtmaxTop;
    TH1 *hPtmaxTopReal;
    TH1 *hPtmaxTopHplus;
    TH1 *htopMassReal;
    TH1 *htopMassMaxReal;
    TH1 *htopMassRealHplus;
    TH1 *htopMassRealb;

    // Variables
    double topMass;
    XYZTLorentzVector top;
  };
}

#endif
