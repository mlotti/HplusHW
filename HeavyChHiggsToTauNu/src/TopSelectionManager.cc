#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionBase.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

#include <limits>

namespace HPlus {
  // constructor and desturctor
  TopSelectionManager::TopSelectionManager(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& fHistoWrapper, const std::string topRecoName, TopChiSelection topChiSelection):
  
    fTopSelectionCounter(eventCounter.addSubCounter("top", "Top selection")),
    fTopChiSelectionCounter(eventCounter.addSubCounter("top", "Top Chi Selection")),
    //fTopWithMHSelectionCounter(eventCounter.addCounter("Top after Inv Mass selection")),
    fTopWithBSelectionCounter(eventCounter.addSubCounter("top", "Top with B Selection")),
    fTopWithWSelectionCounter(eventCounter.addSubCounter("top", "Top with W Selection")),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    //fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper), //TODO: restore this!
    fTopChiSelection(topChiSelection),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper),
    //    fTopWithMHSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithMHSelection"), eventCounter, fHistoWrapper)
    fTopRecoName(topRecoName)

    {}

  TopSelectionManager::~TopSelectionManager() {}

  // constructor and destructor for TopSelectionManager::Data class
  /* TopSelectionManager::Data::Data():
    fPassedEvent(false) {}
  TopSelectionManager::Data::~Data() {}  */

  // analyze
  void TopSelectionManager::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, edm::Ptr<pat::Jet> bjet, bool bjetPassed) {

  // Top reco, no event cut
  // top mass with possible event cuts
    
    TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jets, bjets);
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);
      //hTransverseMassTopSelection->Fill(transverseMass); //TODO
    }

    TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jets, bjets);
    if (TopChiSelectionData.passedEvent() ) {
      increment(fTopChiSelectionCounter);
      //hTransverseMassTopChiSelection->Fill(transverseMass);
    }

    myTopRecoWithWSelectionStatus = false;

    if (bjetPassed) {
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jets, bjet);
      if (TopWithBSelectionData.passedEvent() ) {
        increment(fTopWithBSelectionCounter);
        //hTransverseMassTopBjetSelection->Fill(transverseMass); //TODO
      }
      TopWithWSelection::Data TopWithWSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jets, bjet);
      if (TopWithWSelectionData.passedEvent() ) {
        myTopRecoWithWSelectionStatus = true;
        increment(fTopWithWSelectionCounter);
        //hTransverseMassTopWithWSelection->Fill(transverseMass); //TODO
      }
    }
  }

//getPassedTopRecoStatus (to select events depending on top resonctruction)
    bool TopSelectionManager::getPassedTopRecoStatus() {
    if (fTopRecoName == "None")
      return true;
    else if (fTopRecoName == "std")
      return TopSelectionData.passedEvent();
    else if (fTopRecoName == "chi")
      return TopChiSelectionData.passedEvent();
    else if (fTopRecoName == "Wselection")
      return myTopRecoWithWSelectionStatus;
    else
      return false;
    }

}
