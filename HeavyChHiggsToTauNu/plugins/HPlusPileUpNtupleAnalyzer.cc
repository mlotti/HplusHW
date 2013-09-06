#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"

#include "TTree.h"

/**
 * This is an analyzer to produce an ntuple with the number of true
 * interactions per event. This is needed to obtain the PU-reweighted
 * number of all events for each MC dataset.
 */

class HPlusPileUpNtupleAnalyzer: public edm::EDAnalyzer {
public:
  HPlusPileUpNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~HPlusPileUpNtupleAnalyzer();

private:
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void reset();

  TTree *fTree;

  HPlus::TreeEventBranches fEventBranches;

  const edm::InputTag fPuSummarySrc;
  const edm::InputTag fTtGenEventSrc;
  float fTrueNumInteractions;
  float fTopPt;
  float fTopBarPt;
  int fTopEventClassTauIsLepton;
  int fTopEventClassTauIsNotLepton;
  const bool fTopBranchesEnabled;
};

HPlusPileUpNtupleAnalyzer::HPlusPileUpNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fPuSummarySrc(iConfig.getParameter<edm::InputTag>("puSummarySrc")),
  fTtGenEventSrc(iConfig.getParameter<edm::InputTag>("ttGenEventSrc")),
  fTopBranchesEnabled(iConfig.getParameter<bool>("topBranchesEnabled"))
{
  edm::Service<TFileService> fs;
  fTree = fs->make<TTree>("tree", "Tree");

  fEventBranches.book(fTree);
  fTree->Branch("TrueNumInteractions", &fTrueNumInteractions);
  if(fTopBranchesEnabled) {
    fTree->Branch("TopPt", &fTopPt);
    fTree->Branch("TopBarPt", &fTopBarPt);
    fTree->Branch("TopEventClassTauIsLepton", &fTopEventClassTauIsLepton);
    fTree->Branch("TopEventClassTauIsNotLepton", &fTopEventClassTauIsNotLepton);
  }

  reset();
}

HPlusPileUpNtupleAnalyzer::~HPlusPileUpNtupleAnalyzer() {}

void HPlusPileUpNtupleAnalyzer::reset() {
  fEventBranches.reset();
  fTrueNumInteractions = -1;
  fTopPt = -999;
  fTopBarPt = -999;
  fTopEventClassTauIsLepton = 0;
  fTopEventClassTauIsNotLepton = 0;
}

void HPlusPileUpNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventBranches.setValues(iEvent);

  edm::Handle<std::vector<PileupSummaryInfo> > hpu;
  iEvent.getByLabel(fPuSummarySrc, hpu);


  for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpu->begin(); iPV != hpu->end(); ++iPV) {
    if(iPV->getBunchCrossing() == 0)
      fTrueNumInteractions = iPV->getTrueNumInteractions();
  }

  if(fTopBranchesEnabled) {
    edm::Handle<TtGenEvent> hGenEvent;
    iEvent.getByLabel(fTtGenEventSrc, hGenEvent);

    const reco::GenParticle *top = hGenEvent->top();
    const reco::GenParticle *topBar = hGenEvent->topBar();
    if(!top) throw cms::Exception("Assert") << "Got null from ttGenEvent.top() in " << __FILE__ << ":" << __LINE__;
    if(!topBar) throw cms::Exception("Assert") << "Got null from ttGenEvent.topBar() in " << __FILE__ << ":" << __LINE__;

    fTopPt = top->pt();
    fTopBarPt = topBar->pt();

    if(hGenEvent->isFullHadronic(false)) fTopEventClassTauIsLepton = 1;
    else if(hGenEvent->isSemiLeptonic(false)) fTopEventClassTauIsLepton = 2;
    else if(hGenEvent->isFullLeptonic(false)) fTopEventClassTauIsLepton = 3;
    else throw cms::Exception("Assert") << "ttGenEvent is not FullHadronic, SemiLeptonic, nor FullLeptonic (tau is treated as lepton) in " << __FILE__ << ":" << __LINE__;

    if(hGenEvent->isFullHadronic(true)) fTopEventClassTauIsNotLepton = 1;
    else if(hGenEvent->isSemiLeptonic(true)) fTopEventClassTauIsNotLepton = 2;
    else if(hGenEvent->isFullLeptonic(true)) fTopEventClassTauIsNotLepton = 3;
    else throw cms::Exception("Assert") << "ttGenEvent is not FullHadronic, SemiLeptonic, nor FullLeptonic (tau is not treated as lepton) in " << __FILE__ << ":" << __LINE__;
  }

  fTree->Fill();
  reset();
}

DEFINE_FWK_MODULE(HPlusPileUpNtupleAnalyzer);
