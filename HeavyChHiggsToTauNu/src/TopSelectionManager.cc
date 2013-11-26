#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelectionManager.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

#include <limits>

namespace HPlus {
  // constructor and desturctor
  TopSelectionManager::TopSelectionManager(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& fHistoWrapper, const std::string topRecoName):
    iConfig(iConfig),
    eventCounter(eventCounter),
    fHistoWrapper(fHistoWrapper),
    fTopRecoName(topRecoName)
    {
    if (topRecoName == "chi"){   
        fSelectedAlgorithm = new TopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper);
        }
    else if (topRecoName == "std"){
        fSelectedAlgorithm = new TopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper);
        }
    else if (topRecoName == "Wselection"){
        fSelectedAlgorithm = new TopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper);
        }
    else if (topRecoName == "Bselection"){ 
        fSelectedAlgorithm = new TopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper);
        }
    else 
        fSelectedAlgorithm = NULL;
    }

  TopSelectionManager::~TopSelectionManager() {
      delete fSelectedAlgorithm;
      }

  // analyze
  TopSelectionManager::Data TopSelectionManager::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, edm::Ptr<pat::Jet> bjet, bool bjetPassed) {
    TopSelectionManager::Data TopSelectionData;
    if(fSelectedAlgorithm){
        if (fTopRecoName == "None")
            TopSelectionData.makeEventPassed();
        else if (fTopRecoName == "std")
            TopSelectionData = fSelectedAlgorithm->analyze(iEvent, iSetup, jets, bjets);
        else if (fTopRecoName == "chi")
            TopSelectionData = fSelectedAlgorithm->analyze(iEvent, iSetup, jets, bjets);
        else if (fTopRecoName == "Wselection" && bjetPassed)
            TopSelectionData = fSelectedAlgorithm->analyze(iEvent, iSetup, jets, bjet);
        else if (fTopRecoName == "Bselection" && bjetPassed)
            TopSelectionData = fSelectedAlgorithm->analyze(iEvent, iSetup, jets, bjet);
        }
    return TopSelectionData;
    }       
    
    // silentAnalyze
   TopSelectionManager::Data TopSelectionManager::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, edm::Ptr<pat::Jet> bjet, bool bjetPassed){
    TopSelectionManager::Data TopSelectionData;
    if(fSelectedAlgorithm){
        if (fTopRecoName == "None")
            TopSelectionData.makeEventPassed();
        else if (fTopRecoName == "std")
            TopSelectionData = fSelectedAlgorithm->silentAnalyze(iEvent, iSetup, jets, bjets);
        else if (fTopRecoName == "chi")
            TopSelectionData = fSelectedAlgorithm->silentAnalyze(iEvent, iSetup, jets, bjets);
        else if (fTopRecoName == "Wselection" && bjetPassed)
            TopSelectionData = fSelectedAlgorithm->silentAnalyze(iEvent, iSetup, jets, bjet);
        else if (fTopRecoName == "Bselection" && bjetPassed)
            TopSelectionData = fSelectedAlgorithm->silentAnalyze(iEvent, iSetup, jets, bjet);
        }
    return TopSelectionData;
    }   
    
}
