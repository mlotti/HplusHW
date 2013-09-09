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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

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
  int fTopEventClass;
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
    fTree->Branch("TopEventClass", &fTopEventClass);
  }

  reset();
}

HPlusPileUpNtupleAnalyzer::~HPlusPileUpNtupleAnalyzer() {}

void HPlusPileUpNtupleAnalyzer::reset() {
  fEventBranches.reset();
  fTrueNumInteractions = -1;
  fTopPt = -999;
  fTopBarPt = -999;
  fTopEventClass = -1;
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

    // First as from TtGenEvent the topology while treating taus as
    // hadrons
    if(hGenEvent->isFullHadronic(true)) fTopEventClass = 0;
    else if(hGenEvent->isSemiLeptonic(true)) fTopEventClass = 1;
    else if(hGenEvent->isFullLeptonic(true)) fTopEventClass = 2;
    else throw cms::Exception("Assert") << "ttGenEvent is not FullHadronic, SemiLeptonic, nor FullLeptonic (tau is not treated as lepton) in " << __FILE__ << ":" << __LINE__;

    // Then ask for taus, theck their decay, and modify the event class accordingly
    if(const reco::GenParticle *tauPlus = hGenEvent->tauPlus()) {
      edm::LogVerbatim("Ntuple") << "Has tau plus";
      const reco::GenParticle *d = HPlus::GenParticleTools::findTauDaughter(tauPlus);
      if(d) {
        edm::LogVerbatim("Ntuple") << "  has daughter " << d->pdgId();
        int id = std::abs(d->pdgId());
        if(id == 11 || id == 13) {
          ++fTopEventClass;
        }
      }
      else {
        fTopEventClass += 10;
      }
    }
    if(const reco::GenParticle *tauMinus = hGenEvent->tauMinus()) {
      edm::LogVerbatim("Ntuple") << "Has tau minus";
      const reco::GenParticle *d = HPlus::GenParticleTools::findTauDaughter(tauMinus);
      if(d) {
        edm::LogVerbatim("Ntuple") << "  has daughter " << d->pdgId();
        int id = std::abs(d->pdgId());
        if(id == 11 || id == 13) {
          ++fTopEventClass;
        }
      }
      else {
        fTopEventClass += 10;
      }
    }

    edm::LogVerbatim("Ntuple") << "Top event class (number of leptons) " << fTopEventClass;
    hGenEvent->print();
  }

  fTree->Fill();
  reset();
}

DEFINE_FWK_MODULE(HPlusPileUpNtupleAnalyzer);
