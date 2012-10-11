#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeTriggerBranches.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

#include "TTree.h"

namespace HPlus {
  TreeTriggerBranches::TreeTriggerBranches(const edm::ParameterSet& iConfig):
    fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerSrc"))
  {
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("triggerPaths");
    std::vector<std::string> names = pset.getParameterNames();
    for(size_t i=0; i<names.size(); ++i) {
      fPaths.push_back(TriggerPath(names[i], pset.getParameter<std::vector<std::string> >(names[i])));
    }
  }
  TreeTriggerBranches::~TreeTriggerBranches() {}


  void TreeTriggerBranches::book(TTree *tree) {
    for(size_t i=0; i<fPaths.size(); ++i) {
      tree->Branch(("trigger_"+fPaths[i].fBranchName).c_str(), &(fPaths[i].fDecision));
    }
  }

  void TreeTriggerBranches::setValues(const edm::Event& iEvent) {
    edm::Handle<pat::TriggerEvent> htrigger;
    iEvent.getByLabel(fPatTriggerSrc, htrigger);

    for(size_t i=0; i<fPaths.size(); ++i) {
      bool accept = false;
      for(size_t j=0; j<fPaths[i].fPathNames.size(); ++j) {
        const pat::TriggerPath *path = htrigger->path(fPaths[i].fPathNames[j]);
        if(path && path->wasAccept()) {
          accept = true;
          break;
        }
      }
      fPaths[i].fDecision = accept;
    }
  }

  void TreeTriggerBranches::reset() {
    for(size_t i=0; i<fPaths.size(); ++i)
      fPaths[i].fDecision = false;
  }
}
