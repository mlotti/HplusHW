// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalOptimisation_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalOptimisation_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"
#include "TTree.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TH2;

namespace HPlus {
  class SignalOptimisation {
    class AnalysisVariation {
    public:
      AnalysisVariation(double tauPtCut, double rtau, double METcut, double btaggingDiscriminator, double fakeMETVetoCut);
      ~AnalysisVariation();
      
      bool analyse(const METSelection::Data& METData, const edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauData, const JetSelection::Data& jetData, BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const TopSelection::Data& topSelectionData, double transverseMass, double weight);
      std::string getLabel() { return fLabel; }

    private:
      std::string fLabel;
      double fTauPtCut;
      double fRtauCut;
      double fBTaggingDiscriminator;
      double fMETCut;
      double fFakeMETVetoCut;
      // event count after all selections
      TH1F* hEventCount;
      // distributions
      TH1F* hRtauAfterAllOthers;
      TH1F* hBTaggingDiscriminatorAfterAllOthers;
      TH1F* hMETAfterAllOthers;
      TH1F* hFakeMETVetoAfterAllOthers;
      TH1F* hTopSelectionAfterAllOthers;
      TH1F* hTransverseMassAfterAllOthers;
    };
  
  public:
    explicit SignalOptimisation(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~SignalOptimisation();

    // Interface towards the EDProducer
    // void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
    bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
    
  private:
    // void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    bool analyse(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    
    const double  ftransverseMassCut;

    Count fAllCounter;
    Count fTriggerCounter;
    Count fPrimaryVertexCounter;
    Count fTausExistCounter;
    Count fOneTauCounter;
    Count fMETCounter;
    Count fElectronVetoCounter;
    Count fMuonVetoCounter;
    Count fNJetsCounter;
    Count fBTaggingCounter;
    Count fFakeMETVetoCounter;
    Count fEvtTopologyCounter;
    Count fTopSelectionCounter;
    Count fZmassVetoCounter;
    Count ftransverseMassCutCounter;
    //
    EventWeight& fEventWeight;

    // Analysis variations
    std::vector<AnalysisVariation> fAnalyses;
    std::vector<Count> fAnalysisVariationCounters;
    
    // The order here defines the order the counters are printed at the program termination
    TriggerSelection fTriggerSelection;
    VertexSelection fPrimaryVertexSelection;
    GlobalElectronVeto fGlobalElectronVeto;
    GlobalMuonVeto fGlobalMuonVeto;
    TauSelection fOneProngTauSelection;
    METSelection fMETSelection;
    JetSelection fJetSelection;
    BTagging fBTagging;
    FakeMETVeto fFakeMETVeto;
    JetTauInvMass fJetTauInvMass;
    EvtTopology fEvtTopology;
    TopSelection fTopSelection;
    // GenParticleAnalysis fGenparticleAnalysis;
    ForwardJetVeto fForwardJetVeto;
    //
    VertexWeight fVertexWeight;

    // Histograms
    TH1 *hAlphaTInvMass;

    // for Tree
    TTree *myTree;

    bool bTauIDStatus;
    float fTauJetEt;
    float fTauJetEta;
    float fMET;
    float fFakeMETDeltaPhi;
    int iNHadronicJets;
    int iNHadronicJetsInFwdDir;
    int iNBtags;
    float fGlobalMuonVetoHighestPt;
    float fGlobalElectronVetoHighestPt;
    float fTransverseMass;
    float fAlphaT;
    float fHt;
    float fJt; // Jt = Ht - TauJetEt - LdgJetEt

  };
}

#endif
