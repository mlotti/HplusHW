// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VetoTauSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VetoTauSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

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

  class VetoTauSelection: public BaseSelection {
  public:
    class Data {
    public:
      Data();
      ~Data();

      /// Returns true, if the selected tau has passed all selections
      const bool passedEvent() const { return fPassedEvent; }

      const edm::PtrVector<pat::Tau>& getSelectedVetoTaus() const { return fSelectedVetoTaus; }

      friend class VetoTauSelection;

    private:
      bool fPassedEvent;
      edm::PtrVector<pat::Tau> fSelectedVetoTaus;
    };

    VetoTauSelection(const edm::ParameterSet& iConfig, const edm::ParameterSet& fakeTauSFandSystematicsConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~VetoTauSelection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau, double vertexZ);
    /// Analyses the compatibility of the tau and the primary vertex
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau, double vertexZ);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau, double vertexZ);
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
  };
}

#endif
