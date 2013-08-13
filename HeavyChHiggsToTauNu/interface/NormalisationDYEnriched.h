// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_NormalisationDYEnriched_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_NormalisationDYEnriched_h

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
   * Class to check normalisation of DY enriched sample with genuine taus
   */
  class NormalisationDYEnrichedWithGenuineTaus : public NormalisationAnalysis {
  public:
    NormalisationDYEnrichedWithGenuineTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    NormalisationDYEnrichedWithGenuineTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~NormalisationDYEnrichedWithGenuineTaus();

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
   * Class to check normalisation of DY enriched sample with fake taus
   */
  class NormalisationDYEnrichedWithFakeTaus : public NormalisationAnalysis {
  public:
    NormalisationDYEnrichedWithFakeTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    NormalisationDYEnrichedWithFakeTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~NormalisationDYEnrichedWithFakeTaus();

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