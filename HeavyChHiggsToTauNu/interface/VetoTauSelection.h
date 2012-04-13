// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VetoTauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VetoTauSelection_h

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

class TH1;

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class VetoTauSelection {
  public:
    class Data {
    public:
      Data(const VetoTauSelection *vetoTauSelection, bool passedEvent);
      ~Data();

      /// Returns true, if the selected tau has passed all selections
      bool passedEvent() const { return fPassedEvent; }
      
      const edm::PtrVector<pat::Tau>& getSelectedVetoTaus() const { return fVetoTauSelection->fSelectedVetoTaus; }

    private:
      const VetoTauSelection *fVetoTauSelection;
      const bool fPassedEvent;
    };
  
    VetoTauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~VetoTauSelection();

    /// Analyses the compatibility of the tau and the primary vertex
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau);

  private:
    // Parameters set in config file
    const double fZMass;
    const double fZMassWindow;
    edm::InputTag fTauSource;
    edm::InputTag fMetSrc;
    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;
    edm::InputTag fThreeProngTauSrc;
    edm::InputTag fSrc;
    
    TauSelection fTauSelection;
    FakeTauIdentifier fFakeTauIdentifier;
    
    EventWeight& fEventWeight;

    Count fAllEventsCounter;
    //    Count fVetoTauCandidatesCounter;
    Count fVetoTausSelectedCounter;
    Count fEventsCompatibleWithZMassCounter;
    Count fSelectedEventsCounter;
    
    // histograms
    TH1* hTauCandFromWPt;
    TH1* hTauCandAllPt;
    TH1* hCandidateTauNumber;
    TH1* hSelectedTauNumber;
    TH1* hSelectedGenuineTauByPt;
    TH1* hSelectedGenuineTauByEta;
    TH1* hSelectedGenuineTauByPhi;
    TH1* hSelectedFakeTauByPt;
    TH1* hSelectedFakeTauByEta;
    TH1* hSelectedFakeTauByPhi;
    TH1* hSelectedGenuineTauDiTauMass;
    TH1* hSelectedFakeTauDiTauMass;
    TH1* hSelectedTaus;
    
    edm::PtrVector<pat::Tau> fSelectedVetoTaus;
  };
}

#endif
