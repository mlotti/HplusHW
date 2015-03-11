// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_NormalisationTTJetsEnriched_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_NormalisationTTJetsEnriched_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationAnalysis.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  /**
   * Class to check normalisation of ttbar enriched sample with genuine taus
   */
  class NormalisationTTJetsEnrichedWithGenuineTaus : public NormalisationAnalysis {
  public:
    NormalisationTTJetsEnrichedWithGenuineTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    NormalisationTTJetsEnrichedWithGenuineTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~NormalisationTTJetsEnrichedWithGenuineTaus();

    void analyse(const edm::Event& iEvent,
                 const TauSelection::Data& tauData,
                 const FakeTauIdentifier::Data& fakeTauData,
                 const ElectronSelection::Data& electronData,
                 const MuonSelection::Data& muonData,
                 const JetSelection::Data& jetData,
                 METTriggerEfficiencyScaleFactor* metTrgSF,
                 const QCDTailKiller::Data& tailKillerData,
                 const METSelection::Data& metData,
                 const BTagging::Data& btagData);

  private:

  };

  /**
   * Class to check normalisation of ttbar enriched sample, in the boosted WH style
   */
  class NormalisationTTJetsEnrichedBoostedWH : public NormalisationAnalysis {
  public:
    NormalisationTTJetsEnrichedBoostedWH(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    NormalisationTTJetsEnrichedBoostedWH(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~NormalisationTTJetsEnrichedBoostedWH();

    void analyse(const edm::Event& iEvent,
                 const TauSelection::Data& tauData,
                 const FakeTauIdentifier::Data& fakeTauData,
                 const ElectronSelection::Data& electronData,
                 const MuonSelection::Data& muonData,
                 const JetSelection::Data& jetData,
                 METTriggerEfficiencyScaleFactor* metTrgSF,
                 const QCDTailKiller::Data& tailKillerData,
                 const METSelection::Data& metData,
                 const BTagging::Data& btagData);

  private:

  };
  /**
   * Class to check normalisation of ttbar enriched sample with fake taus
   */
  class NormalisationTTJetsEnrichedWithFakeTaus : public NormalisationAnalysis {
  public:
    NormalisationTTJetsEnrichedWithFakeTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    NormalisationTTJetsEnrichedWithFakeTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~NormalisationTTJetsEnrichedWithFakeTaus();

    void analyse(const edm::Event& iEvent,
                 const TauSelection::Data& tauData,
                 const FakeTauIdentifier::Data& fakeTauData,
                 const ElectronSelection::Data& electronData,
                 const MuonSelection::Data& muonData,
                 const JetSelection::Data& jetData,
                 METTriggerEfficiencyScaleFactor* metTrgSF,
                 const QCDTailKiller::Data& tailKillerData,
                 const METSelection::Data& metData,
                 const BTagging::Data& btagData);

  private:

  };

}

#endif