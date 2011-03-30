// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementByMetFactorisationPart2_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDMeasurementByMetFactorisationPart2_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FactorizationTable.h"
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
  class QCDMeasurementByMetFactorisationPart2 {  
  public:
    explicit QCDMeasurementByMetFactorisationPart2(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~QCDMeasurementByMetFactorisationPart2();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
    // We need a reference in order to use the same object (and not a copied one) given in HPlusSignalAnalysisProducer
    EventWeight& fEventWeight;

    // Counters - order is important
    Count fAllCounter;
    Count fTriggerAndHLTMetCutCounter;
    Count fPrimaryVertexCounter;
    Count fOneProngTauSelectionCounter;
    Count fGlobalElectronVetoCounter;
    Count fGlobalMuonVetoCounter;
    Count fJetSelectionCounter2;
    Count fJetSelectionCounter;
    Count fMETCounter;
    Count fOneProngTauIDWithoutRtauCounter;
    Count fOneProngTauIDWithRtauCounter;
    Count fInvMassVetoOnJetsCounter;
    Count fEvtTopologyCounter;
    Count fBTaggingCounter;
    Count fFakeMETVetoCounter;
    
    // Counters for propagating result into signal region from reversed rtau control region
    Count fABCDNegativeRtauNegativeBTagCounter;
    Count fABCDNegativeRtauPositiveBTagCounter;
    Count fABCDPositiveRtauNegativeBTagCounter;
    Count fABCDPositiveRtauPositiveBTagCounter;

    // The order here defines the order the subcounters are printed at the program termination
    TriggerSelection fTriggerSelection;
    //TriggerTauMETEmulation  fTriggerTauMETEmulation;
    VertexSelection fPrimaryVertexSelection;
    TauSelection fOneProngTauSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    JetSelection fJetSelection;
    METSelection fMETSelection;
    InvMassVetoOnJets fInvMassVetoOnJets;
    EvtTopology fEvtTopology;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    
    // Factorization table
    FactorizationTable fFactorizationTable;
    
    // Histograms
    TH1 *hMETAfterJetSelection;
    TH1 *hWeightedMETAfterJetSelection;
    TH1 *hWeightedMETAfterTauIDNoRtau;
    TH1 *hWeightedMETAfterTauID;
    TH1 *hWeightedMETAfterBTagging;
    TH1 *hWeightedMETAfterFakeMETVeto;
    TH1 *hRTauAfterAllSelections;

    // TauID-MET Corralation plots
    TH1 *hMETRightBeforeTauID;
    TH1 *hMETRightAfterTauID;
    TH2 *hTauIDVsMETRightBeforeTauID;

    // Histograms for later change of factorization map
    TH1 *hNonWeightedTauPtAfterJetSelection;
    TH1 *hNonWeightedTauPtAfterTauIDNoRtau;
    TH1 *hNonWeightedTauPtAfterTauID;
    TH1 *hNonWeightedTauPtAfterBTagging;
    TH1 *hNonWeightedTauPtAfterFakeMETVeto;
    TH1 *fNonWeightedABCDNegativeRtauNegativeBTag;
    TH1 *fNonWeightedABCDNegativeRtauPositiveBTag;
    TH1 *fNonWeightedABCDPositiveRtauNegativeBTag;
    TH1 *fNonWeightedABCDPositiveRtauPositiveBTag;
    
    // Control histograms for P(MET>70)
    TH1 *hMETPassProbabilityAfterJetSelection;
    TH1 *hMETPassProbabilityAfterTauIDNoRtau;
    TH1 *hMETPassProbabilityAfterTauID;
    TH1 *hMETPassProbabilityAfterBTagging;
    TH1 *hMETPassProbabilityAfterFakeMETVeto;

  };
}

#endif
