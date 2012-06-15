// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VetoTauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VetoTauSelection_h

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}
namespace reco {
  class Vertex;
}
namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

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

    VetoTauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~VetoTauSelection();

    /// Analyses the compatibility of the tau and the primary vertex
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau);

  private:
    // Parameters set in config file
    edm::InputTag fSrc;
    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;
    edm::InputTag fThreeProngTauSrc;
    const double fZMass;
    const double fZMassWindow;
    edm::InputTag fTauSource;
    edm::InputTag fMetSrc;
    edm::Ptr<reco::Vertex> thePV_;

    TauSelection fTauSelection;
    FakeTauIdentifier fFakeTauIdentifier;

    Count fAllEventsCounter;
    //    Count fVetoTauCandidatesCounter;
    Count fVetoTausSelectedCounter;
    Count fEventsCompatibleWithZMassCounter;
    Count fSelectedEventsCounter;

    // histograms
    WrappedTH1* hTauCandFromWPt;
    WrappedTH1* hTauCandAllPt;
    WrappedTH1* hCandidateTauNumber;
    WrappedTH1* hSelectedTauNumber;
    WrappedTH1* hSelectedGenuineTauByPt;
    WrappedTH1* hSelectedGenuineTauByEta;
    WrappedTH1* hSelectedGenuineTauByPhi;
    WrappedTH1* hSelectedFakeTauByPt;
    WrappedTH1* hSelectedFakeTauByEta;
    WrappedTH1* hSelectedFakeTauByPhi;
    WrappedTH1* hSelectedGenuineTauDiTauMass;
    WrappedTH1* hSelectedFakeTauDiTauMass;
    WrappedTH1* hSelectedTaus;

    edm::PtrVector<pat::Tau> fSelectedVetoTaus;
  };
}

#endif
