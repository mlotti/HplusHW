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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "TTree.h"
#include "TH2F.h"

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
    void createHistogramGroupByTauPt(std::string name);

    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    // Different forks of analysis
    void analyzeABCDByTauIsolationAndBTagging(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETDat, const ForwardJetVeto::Data forwardData, int tauPtBin, double weightWithoutMET);
    void analyzeFactorizedBTaggingAndRtau(const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data forwardData, int tauPtBin, double weightWithoutMET);
    void analyzeFactorizedBTaggingBeforeTauIDAndRtau(const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data forwardData, int tauPtBin, double weightWithoutMET);

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
    Count fForwardJetVetoCounter;
    
    // Counters for propagating result into signal region from reversed rtau control region

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
    ForwardJetVeto fForwardJetVeto;
    DeltaPhi fDeltaPhi;
    TransverseMass fTransverseMass;
    
    // Factorization table
    FactorizationTable fFactorizationTable;
    std::vector<double> fFactorizationBinLowEdges;
    
    // MET Histograms
    TH1 *hMETAfterJetSelection;
    TH1 *hWeightedMETAfterJetSelection;
    TH1 *hWeightedMETAfterTauIDNoRtau;
    TH1 *hWeightedMETAfterTauID;
    TH1 *hWeightedMETAfterBTagging;
    TH1 *hWeightedMETAfterFakeMETVeto;
    TH1 *hWeightedMETAfterForwardJetVeto;
    // After all selections -- FIXME move to separate class
    TH1 *hWeightedTauPtAfterAllSelections;
    TH1 *hWeightedTauEtaAfterAllSelections;
    TH1 *hWeightedRTauAfterAllSelections;
    TH1 *hWeightedNJetsAfterAllSelections;
    TH1 *hWeightedBJetsAfterAllSelections;
    TH1 *hWeightedMETAfterAllSelections;
    TH1 *hWeightedFakeMETVetoAfterAllSelections;
    TH1 *hWeightedDeltaPhiAfterAllSelections;
    TH1 *hWeightedTransverseMassAfterAllSelections;

    // TauID-MET Correlation plots -- will not work like this, need to do in separate class (does not measure full tauID or if changed, the tau sub counters will be messed up)
    TH1 *hTauIDMETCorrelationMETRightBeforeTauID; // FIXME
    TH1 *hTauIDMETCorrelationMETRightAfterTauID; // FIXME
    TH2 *hTauIDMETCorrelationTauIDVsMETRightBeforeTauID; // FIXME

    // METFactorization details
    TH1 *hMETFactorizationNJetsBefore;
    TH1 *hMETFactorizationNJetsAfter;
    TH2 *hMETFactorizationNJets;
    TH1 *hMETFactorizationBJetsBefore;
    TH1 *hMETFactorizationBJetsAfter;
    TH2 *hMETFactorizationBJets;

    // Standard cut path
    TH1 *hStdNonWeightedTauPtAfterJetSelection;
    TH1 *hStdNonWeightedTauPtAfterTauIDNoRtau;
    TH1 *hStdNonWeightedTauPtAfterTauID;
    TH1 *hStdNonWeightedTauPtAfterBTagging;
    TH1 *hStdNonWeightedTauPtAfterFakeMETVeto;
    TH1 *hStdNonWeightedTauPtAfterForwardJetVeto;
    TH1 *hStdWeightedRtau;
    TH1 *hStdWeightedBjets;
    TH1 *hStdWeightedFakeMETVeto;

    // Standard cuts with factorized rtau and b-tagging
    TH1 *hFactRtauBNonWeightedTauPtAfterJetSelection;
    TH1 *hFactRtauBNonWeightedTauPtAfterTauIDNoRtau;
    TH1 *hFactRtauBNonWeightedTauPtAfterTauID;
    TH1 *hFactRtauBNonWeightedTauPtAfterBTagging;
    TH1 *hFactRtauBNonWeightedTauPtAfterFakeMETVeto;
    TH1 *hFactRtauBNonWeightedTauPtAfterForwardJetVeto;

    // Standard cuts with factorized rtau and b-tagging
    TH1 *hFactRtauBBeforeTauIDNonWeightedTauPtAfterJetSelection;
    TH1 *hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauIDNoRtau;
    TH1 *hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauID;
    TH1 *hFactRtauBBeforeTauIDNonWeightedTauPtAfterBTagging;
    TH1 *hFactRtauBBeforeTauIDNonWeightedTauPtAfterFakeMETVeto;
    TH1 *hFactRtauBBeforeTauIDNonWeightedTauPtAfterForwardJetVeto;

    // ABCD(tau isol. vs. b-tag) cut path - ugly duplication, but fast code
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterJetSelection[4];
    TH2 *hABCDTauIsolBNonWeightedTauPtVsMET[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterMET[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterRtau[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[4];
    TH1 *hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[4];
    TH1 *hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[4];
    TH1 *hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[4];

    // Control histograms for P(MET>70)
    TH1 *hMETPassProbabilityAfterJetSelection;
    TH1 *hMETPassProbabilityAfterTauIDNoRtau;
    TH1 *hMETPassProbabilityAfterTauID;
    TH1 *hMETPassProbabilityAfterBTagging;
    TH1 *hMETPassProbabilityAfterFakeMETVeto;
    TH1 *hMETPassProbabilityAfterForwardJetVeto;


    std::vector<TH1*> fMETHistogramsByTauPt;
  };
}

#endif
