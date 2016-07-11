// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauFakeRateAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauFakeRateAnalysis_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"

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
   * Class to analyse tau fake rate
   */
  class TauFakeRateAnalysis {
  public:
    TauFakeRateAnalysis(HistoWrapper& histoWrapper);
    ~TauFakeRateAnalysis();

    /**
     * Does tag and probe for a selected electron and the selected tau using Z->ee mass as a constraint.
     * Derives normalisation scale factors in bins of tau pT and tau decay mode
     */
    void analyseEToTauFakes(const VertexSelection::Data& vertexData,
                            const TauSelection::Data& tauData,
                            const FakeTauIdentifier::Data& fakeTauData,
                            const ElectronSelection::Data& electronData,
                            const MuonSelection::Data& muondata,
                            const JetSelection::Data& jetData,
                            const METSelection::Data& metData);
    /**
     * Analyses tau fake rate
     */
    void analyseTauFakeRate(const edm::Event& iEvent,
                            const VertexSelection::Data& vertexData,
                            TauSelection& tauSelection,
                            const TauSelection::Data& tauData,
                            FakeTauIdentifier& fakeTauIdentifier,
                            const JetSelection::Data& jetData);

  private:
    // Histograms
    // e -> tau fakes
    WrappedTH1* hEtoTauZmassAll;
    WrappedTH1* hEtoTauZmassDecayMode0;
    WrappedTH1* hEtoTauZmassDecayMode1;
    WrappedTH1* hEtoTauZmassDecayMode2;
    WrappedTH1* hEtoTauTauPtAll;
    WrappedTH1* hEtoTauTauPtDecayMode0;
    WrappedTH1* hEtoTauTauPtDecayMode1;
    WrappedTH1* hEtoTauTauPtDecayMode2;
    // tau fake rate
    WrappedTH1 *hTauVsJetDeltaPt;
    WrappedTH1 *hTauVsJetDeltaR;
    WrappedTH1 *hTauVsJetMCFlavor;
    WrappedTH1 *hTauVsJetDeltaPtGenuineTaus;
    WrappedTH1 *hTauVsJetDeltaPtElectrons;
    WrappedTH1 *hTauVsJetDeltaPtHeavyFlavor;
    WrappedTH1 *hTauVsJetDeltaRHeavyFlavor;
    WrappedTH1 *hTauVsJetDeltaPtLightFlavor;
    WrappedTH1 *hTauVsJetDeltaRLightFlavor;

    WrappedTH1 *hTauVsJetTauPtbBefore;
    WrappedTH1 *hTauVsJetTauPtbleptonicBefore;
    WrappedTH1 *hTauVsJetTauPtcBefore;
    WrappedTH1 *hTauVsJetTauPtudsBefore;
    WrappedTH1 *hTauVsJetTauPtgBefore;
    WrappedTH1 *hTauVsJetTauPteBefore;
    WrappedTH1 *hTauVsJetTauPtmuBefore;
    WrappedTH1 *hTauVsJetTauPtbAfter;
    WrappedTH1 *hTauVsJetTauPtbleptonicAfter;
    WrappedTH1 *hTauVsJetTauPtcAfter;
    WrappedTH1 *hTauVsJetTauPtudsAfter;
    WrappedTH1 *hTauVsJetTauPtgAfter;
    WrappedTH1 *hTauVsJetTauPteAfter;
    WrappedTH1 *hTauVsJetTauPtmuAfter;

    WrappedTH1 *hTauVsJetTauPtbByJetPtBefore;
    WrappedTH1 *hTauVsJetTauPtbleptonicByJetPtBefore;
    WrappedTH1 *hTauVsJetTauPtcByJetPtBefore;
    WrappedTH1 *hTauVsJetTauPtudsByJetPtBefore;
    WrappedTH1 *hTauVsJetTauPtgByJetPtBefore;
    WrappedTH1 *hTauVsJetTauPteByJetPtBefore;
    WrappedTH1 *hTauVsJetTauPtmuByJetPtBefore;
    WrappedTH1 *hTauVsJetTauPtbByJetPtAfter;
    WrappedTH1 *hTauVsJetTauPtbleptonicByJetPtAfter;
    WrappedTH1 *hTauVsJetTauPtcByJetPtAfter;
    WrappedTH1 *hTauVsJetTauPtudsByJetPtAfter;
    WrappedTH1 *hTauVsJetTauPtgByJetPtAfter;
    WrappedTH1 *hTauVsJetTauPteByJetPtAfter;
    WrappedTH1 *hTauVsJetTauPtmuByJetPtAfter;

  };
}

#endif