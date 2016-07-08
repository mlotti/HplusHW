#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"
#include "FWCore/Framework/interface/Event.h"

#include "TTree.h"

namespace HPlus {
  TreeEventBranches::TreeEventBranches() {}
  TreeEventBranches::~TreeEventBranches() {}

  void TreeEventBranches::book(TTree *tree) {
    tree->Branch("event", &fEvent);
    tree->Branch("lumi", &fLumi);
    tree->Branch("run", &fRun);
  }

  void TreeEventBranches::setValues(const edm::Event& iEvent) {
    fEvent = iEvent.id().event();
    fLumi = iEvent.id().luminosityBlock();
    fRun = iEvent.id().run();
  }

  void TreeEventBranches::reset() {
    fEvent = 0;
    fLumi = 0;
    fRun = 0;
  }
}
