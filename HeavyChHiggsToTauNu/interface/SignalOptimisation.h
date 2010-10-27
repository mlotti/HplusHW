// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalOptimisation_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalOptimisation_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
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
  public:
    explicit SignalOptimisation(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~SignalOptimisation();

    // Interface towards the EDProducer
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    double  ftransverseMassCut;

    Count fAllCounter;

    TriggerSelection fTriggerSelection;
    TriggerMETEmulation  fTriggerMETEmulation;
    TauSelection fTauSelection;
    METSelection fMETSelection;
    JetSelection fJetSelection;
    BTagging fBTagging;
    EvtTopology fEvtTopology;
    GlobalMuonVeto fGlobalMuonVeto;
    GlobalElectronVeto fGlobalElectronVeto;
    
    // Histograms
    TH1 *hAlphaTInvMass;
    
    /// for Tree
    TTree *myTree;
    std::vector<bool> *bTauIDStatus;
    std::vector<float> *fTauJetEt;
    std::vector<float> *fMET;
    std::vector<int> *iNHadronicJets;
    std::vector<int> *iNBtags;
    std::vector<float> *fGlobalMuonVetoHighestPt;
    std::vector<float> *fGlobalElectronVetoHighestPt;
    std::vector<float> *fTransverseMass;
    std::vector<float> *fDeltaPhi;
    std::vector<float> *fAlphaT;
    

  };
}

#endif
