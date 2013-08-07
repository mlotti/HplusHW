// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TopSelectionBase_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TopSelectionBase_h

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

  class TopSelectionBase: public BaseSelection {
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

      friend class TopSelectionBase;

    private:
      bool fPassedEvent;
      // Variables
      XYZTLorentzVector top;
      XYZTLorentzVector W;
      edm::Ptr<pat::Jet> bjetInTop;
    };

  public:    
    TopSelectionBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~TopSelectionBase();
    
    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);

    // Overloading for BSelection


  private:
    virtual Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);
    void init();

    //Input parameters, counters and histograms are defined for each algorighm separately!
  };
}

#endif
