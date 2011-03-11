// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementByMetFactorisation_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementByMetFactorisation_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "TTree.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class QCDMeasurementByMetFactorisation {
    /** Helper class for producing data/MC histograms
    **/
    class HistogramGroupByTauPt {
    public:
      HistogramGroupByTauPt(const edm::ParameterSet& iConfig, std::string name);
      ~HistogramGroupByTauPt();
      /// Fill MET to histogram corresponding to correct tau pT bin 
      void fill(double tauPt, double MET, double weight);
      
    private:
      std::vector<double> fPtBinEdges; 
      std::vector<TH1*> fHistograms;
    };
  
  public:
    explicit QCDMeasurementByMetFactorisation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~QCDMeasurementByMetFactorisation();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
    // We need a reference in order to use the same object (and not a copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    // Counters
    Count fAllCounter;
    Count fTriggerAndHLTMetCutCounter;
    Count fPrimaryVertexCounter;
    Count fOneProngTauSelectionCounter;
    Count fGlobalElectronVetoCounter;
    Count fGlobalMuonVetoCounter;
    Count fJetSelectionCounter;
    Count fInvMassVetoOnJetsCounter;
    Count fEvtTopologyCounter;
    Count fBTaggingCounter;
    Count fMETCounter;
    Count fFakeMETVetoCounter;
    Count fMETgt0AfterWholeSelectionCounter;
    Count fMETgt30AfterWholeSelectionCounter;
    Count fMETgt40AfterWholeSelectionCounter;
    Count fMETgt50AfterWholeSelectionCounter;
    Count fMETgt60AfterWholeSelectionCounter;
    Count fMETgt70AfterWholeSelectionCounter;
    Count fMETgt80AfterWholeSelectionCounter;

    // The order here defines the order the counters are printed at the program termination
    TriggerSelection fTriggerSelection;
    //TriggerTauMETEmulation  fTriggerTauMETEmulation;
    VertexSelection fPrimaryVertexSelection;
    TauSelection fOneProngTauSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    JetSelection fJetSelection;
    InvMassVetoOnJets fInvMassVetoOnJets;
    EvtTopology fEvtTopology;
    BTagging fBTagging;
    METSelection fMETSelection;
    FakeMETVeto fFakeMETVeto;
    
    // Histograms
    TH1 *hMETAfterTrigger;
    TH1 *hMETAfterElectronVeto;
    TH1 *hMETAfterMuonVeto;
    TH1 *hMETAfterTauSelection;
    TH1 *hMETAfterJetSelection;
    TH1 *hMETAfterInvMassVetoOnJets;
    TH1 *hMETAfterMET;
    TH1 *hMETAfterBTagging;
    TH1 *hMETAfterFakeMetVeto;
    TH1 *hMETAfterWholeSelection; // without MET Cut
    
    TH1 *hRTauAfterAllSelectionsExceptMETandFakeMetVeto;
    TH1 *hRTauAfterAllSelections;

    TH2 *hTauPtVsMET_AfterTauSelection;
    TH2 *hTauPtVsMET_AfterElectronVeto;
    TH2 *hTauPtVsMET_AfterMuonVeto;
    TH2 *hTauPtVsMET_AfterJetSelection;
    TH2 *hTauPtVsMET_AfterBTagging;
    TH2 *hTauPtVsMET_AfterMET;
    TH2 *hTauPtVsMET_AfterFakeMETVeto;

    HistogramGroupByTauPt hMETPlotsAfterTauSelection;
    HistogramGroupByTauPt hMETPlotsAfterMuonVeto;
    HistogramGroupByTauPt hMETPlotsAfterHadronicJetSelection2;
    HistogramGroupByTauPt hMETPlotsAfterHadronicJetSelection3;
    HistogramGroupByTauPt hMETPlotsAfterBTagging;
  };
}

#endif
