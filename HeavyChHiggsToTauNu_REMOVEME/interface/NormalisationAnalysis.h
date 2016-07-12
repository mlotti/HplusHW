// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_NormalisationAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_NormalisationAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"

#include <string>
#include <vector>

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
   * Class to check normalisation of certain backgrounds and to derive normalisation scale factors
   */
  class NormalisationAnalysis {
  public:
    NormalisationAnalysis(EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string label);
    NormalisationAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string label);
    ~NormalisationAnalysis();

    virtual void analyse(const edm::Event& iEvent,
                          const TauSelection::Data& tauData,
                          const FakeTauIdentifier::Data& fakeTauData,
                          const ElectronSelection::Data& electronData,
                          const MuonSelection::Data& muonData,
                          const JetSelection::Data& jetData,
                          METTriggerEfficiencyScaleFactor* metTrgSF,
                          const QCDTailKiller::Data& tailKillerData,
                          const METSelection::Data& metData,
                          const BTagging::Data& btagData);

    virtual void createHistogramsAndCounters();

    std::string getHistogramDirectory() { return fMyDir; }
    void fillPlotsAfterSelection(bool isFakeTau, const TauSelection::Data& tauData, const JetSelection::Data& jetData, const METSelection::Data& metData, const BTagging::Data& btagData, double eventWeight, double zMass = -1);
    double getHiggsPt(const TauSelection::Data& tauData, const METSelection::Data& metData);

  private:
    /// Creates histograms
    void createCommonHistograms(std::string label);

  protected:
    /// Event counter object
    EventCounter& fEventCounter;
    /// HistoWrapper object
    HistoWrapper& fHistoWrapper;
    /// Directory for histograms
    std::string fMyDir;

    // Input parameters

    // Counters

    // Histograms ------------------------------------------
    // All histograms are after the full selection (it may differ from signal analysis)
    WrappedTH1* hTauPt;
    WrappedTH1* hNJets;
    WrappedTH1* hMET;
    WrappedTH1* hMETphi;
    WrappedTH1* hNBJets;
    WrappedTH1* hTransverseMass;
    WrappedTH1* hZMass;
    WrappedTH1* hHplusPt; // boost variable = vector sum of tau pt and MET

    WrappedTH1* hFakeTauTauPt;
    WrappedTH1* hFakeTauNJets;
    WrappedTH1* hFakeTauMET;
    WrappedTH1* hFakeTauMETphi;
    WrappedTH1* hFakeTauNBJets;
    WrappedTH1* hFakeTauTransverseMass;
    WrappedTH1* hFakeTauZMass;
    WrappedTH1* hFakeTauHplusPt;

  };
}

#endif