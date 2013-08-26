#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

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

  edm::InputTag fPuSummarySrc;
  float fTrueNumInteractions;
};

HPlusPileUpNtupleAnalyzer::HPlusPileUpNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fPuSummarySrc(iConfig.getParameter<edm::InputTag>("puSummarySrc"))
{
  edm::Service<TFileService> fs;
  fTree = fs->make<TTree>("tree", "Tree");

  fEventBranches.book(fTree);
  fTree->Branch("TrueNumInteractions", &fTrueNumInteractions);

  reset();
}

HPlusPileUpNtupleAnalyzer::~HPlusPileUpNtupleAnalyzer() {}

void HPlusPileUpNtupleAnalyzer::reset() {
  fEventBranches.reset();
  fTrueNumInteractions = -1;
}

void HPlusPileUpNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventBranches.setValues(iEvent);

  edm::Handle<std::vector<PileupSummaryInfo> > hpu;
  iEvent.getByLabel(fPuSummarySrc, hpu);


  for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpu->begin(); iPV != hpu->end(); ++iPV) {
    if(iPV->getBunchCrossing() == 0)
      fTrueNumInteractions = iPV->getTrueNumInteractions();
  }

  fTree->Fill();
  reset();
}

DEFINE_FWK_MODULE(HPlusPileUpNtupleAnalyzer);
