#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionManager.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

#include <limits>

namespace HPlus {
  // constructor and desturctor
  TopSelectionManager::TopSelectionManager(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& fHistoWrapper, const std::string topRecoName):
  
    //fTopSelectionCounter(eventCounter.addSubCounter("top", "Top selection")),
    //fTopChiSelectionCounter(eventCounter.addSubCounter("top", "Top Chi Selection")),
    //fTopWithMHSelectionCounter(eventCounter.addCounter("Top after Inv Mass selection")),
    //fTopWithBSelectionCounter(eventCounter.addSubCounter("top", "Top with B Selection")),
    //fTopWithWSelectionCounter(eventCounter.addSubCounter("top", "Top with W Selection")),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper),
    //    fTopWithMHSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithMHSelection"), eventCounter, fHistoWrapper)
    fTopRecoName(topRecoName)

    {}

  TopSelectionManager::~TopSelectionManager() {}

  // analyze
  TopSelectionManager::Data TopSelectionManager::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, edm::Ptr<pat::Jet> bjet, bool bjetPassed) {
    TopSelectionManager::Data TopSelectionData;
    if (fTopRecoName == "None")
      TopSelectionData.makeEventPassed();
    else if (fTopRecoName == "std")
      TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jets, bjets);
    else if (fTopRecoName == "chi")
      TopSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jets, bjets);
    else if (fTopRecoName == "Wselection" && bjetPassed)
      TopSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jets, bjet);
    else if (fTopRecoName == "Bselection" && bjetPassed)
      TopSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jets, bjet);
    return TopSelectionData;
    }       
}
