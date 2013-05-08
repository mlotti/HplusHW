#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

namespace HPlus {
  TriggerSelection::Data::Data():
    fHasTriggerPath(false),
    fPassedEvent(false) {}
  TriggerSelection::Data::~Data() {}
  
  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fTriggerSrc(iConfig.getUntrackedParameter<edm::InputTag>("triggerSrc")),
    fPatSrc(iConfig.getUntrackedParameter<edm::InputTag>("patSrc")),
    fL1MetCollection(iConfig.getUntrackedParameter<std::string>("l1MetCollection")),
    fL1MetCut(iConfig.getUntrackedParameter<double>("l1MetCut")),
    fMetCut(iConfig.getUntrackedParameter<double>("hltMetCut")),
    fTriggerCaloMet(iConfig.getUntrackedParameter<edm::ParameterSet>("caloMetSelection"), eventCounter, histoWrapper),
    fTriggerAllCount(eventCounter.addSubCounter("Trigger", "All events")),
    fTriggerPathCount(eventCounter.addSubCounter("Trigger debug", "Path passed")),
    fTriggerBitCount(eventCounter.addSubCounter("Trigger","Bit passed")), 
    fTriggerCaloMetCount(eventCounter.addSubCounter("Trigger","CaloMET cut passed")), 
    fTriggerCount(eventCounter.addSubCounter("Trigger","Passed")),
    fTriggerDebugAllCount(eventCounter.addSubCounter("Trigger debug", "All events")),
    fTriggerL1MetPassedCount(eventCounter.addSubCounter("Trigger debug", "L1 MET passed")),
    fTriggerHltMetExistsCount(eventCounter.addSubCounter("Trigger debug", "HLT MET object exists")),
    fTriggerHltMetPassedCount(eventCounter.addSubCounter("Trigger debug", "HLT MET passed")),
    fThrowIfNoMet(iConfig.getUntrackedParameter<bool>("throwIfNoMet", true))
  {
    std::vector<std::string> paths = iConfig.getUntrackedParameter<std::vector<std::string> >("triggers");
    for(size_t i = 0; i < paths.size(); ++i){
      TriggerPath* path = new TriggerPath(paths[i],eventCounter);
      triggerPaths.push_back(path);
    }
    // Selection type
    std::string mySelectionType = iConfig.getUntrackedParameter<std::string>("selectionType");
    if (mySelectionType == "byTriggerBit") {
      fTriggerSelectionType = kTriggerSelectionByTriggerBit;
    } else if(mySelectionType == "disabled") {
      fTriggerSelectionType = kTriggerSelectionDisabled;
    } else throw cms::Exception("Configuration") << "TriggerSelection: no or unknown selection type! Options for 'selectionType' are: byTriggerBit, disabled (you chose '"
      << mySelectionType << "')" << std::endl;

    // Histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("Trigger");

    hHltMetBeforeTrigger = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Trigger_HLT_MET_Before_Trigger", "HLT_MET_After_Trigger;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
    hHltMetAfterTrigger = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Trigger_HLT_MET_After_Trigger", "HLT_MET_After_Trigger;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
    hHltMetSelected = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "Trigger_HLT_MET_Selected", "HLT_MET_Selected;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
    hTriggerParametrisationWeight = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Trigger_Parametrisation_Weight", "Trigger_Parametrisation_Weight;Weight*1000;N_{events} / 0.1 percent", 1000, 0., 1000.);
    hControlSelectionType = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "Control_Trigger_Selection_Type", "Control_Trigger_Selection_Type;;N_{events}", 3, 0., 3.);
    if (hControlSelectionType->isActive()) {
      hControlSelectionType->GetXaxis()->SetBinLabel(1, "byTriggerBit");
      hControlSelectionType->GetXaxis()->SetBinLabel(2, "byTriggerBit+ScaleFactor");
      hControlSelectionType->GetXaxis()->SetBinLabel(3, "byTriggerEffParam");
    }
  }

  TriggerSelection::~TriggerSelection() {
    for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i) delete *i;
  }

  TriggerSelection::Data TriggerSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup);
  }

  TriggerSelection::Data TriggerSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup);
  }

  TriggerSelection::Data TriggerSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    Data output;
    TriggerPath* returnPath = NULL;
    increment(fTriggerAllCount);

    hControlSelectionType->Fill(fTriggerSelectionType);
    if (fTriggerSelectionType == kTriggerSelectionByTriggerBit) {
      output.fPassedEvent = passedTriggerBit(iEvent, iSetup, returnPath, output);
    }
    if(returnPath) {
      output.fHasTriggerPath = true;
      output.fHltTaus = returnPath->getTauObjects();
    }

    // Possible caloMET cut should not be controlled by "disabled" bit
    if(fTriggerSelectionType == kTriggerSelectionDisabled) {
      output.fPassedEvent = true;
    }

    // Calo MET cut; needed for non QCD1, disabled for others
    if(output.fPassedEvent) {
      increment(fTriggerBitCount);
      TriggerMETEmulation::Data ret = fTriggerCaloMet.analyze(iEvent, iSetup);
      output.fPassedEvent = ret.passedEvent();
    }

    if(output.fPassedEvent) {
      increment(fTriggerCaloMetCount);
    }

    if(output.fPassedEvent) 
      increment(fTriggerCount);

    return output;
  }
  
  bool TriggerSelection::passedTriggerBit(const edm::Event& iEvent, const edm::EventSetup& iSetup, TriggerPath*& returnPath, TriggerSelection::Data& output) {
    bool passEvent = false;
    /*
    edm::Handle<edm::TriggerResults> htrigger;
    iEvent.getByLabel(fTriggerSrc, htrigger);

    // Do this first with plain edm::TriggerEvent because that we store for each event
    const edm::TriggerNames& triggerNames = iEvent.triggerNames(*htrigger);
    for(std::vector<TriggerPath *>::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i) {
      if((*i)->analyze(*htrigger, triggerNames)) {
        passEvent = true;
        break;
      }
    }
    if(!passEvent)
      return false;
    passEvent = false;
    */

    edm::Handle<pat::TriggerEvent> trigger;
    iEvent.getByLabel(fPatSrc, trigger);

    for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i){
      if((*i)->analyze(*trigger)) {
        passEvent = true;
        returnPath = *i;
      }
    }
    if(passEvent)
      increment(fTriggerPathCount);

    // Get L1/HLT MET object
    // but only if the trigger has been passed (otherwise it makes no sense to emulate MET)
    if(passEvent) {
      // Print all trigger object types of all triggers
      /*
      const pat::TriggerObjectCollection *objs = trigger->objects();
      for(pat::TriggerObjectCollection::const_iterator iObj = objs->begin(); iObj != objs->end(); ++iObj) {
        std::vector<int> types = iObj->triggerObjectTypes();
        if(types.empty())
          continue;
        std::cout << "Object , object types ";
        for(std::vector<int>::const_iterator iType = types.begin(); iType != types.end(); ++iType) {
          std::cout << *iType << " ";
        }
        std::cout << std::endl;
      }
      */

      increment(fTriggerDebugAllCount);
      // L1 MET
      if(fL1MetCut >= 0) {
        pat::TriggerObjectRefVector l1Mets = trigger->objects(trigger::TriggerL1ETM);
        bool found = false;
        for(size_t i=0 ;i<l1Mets.size(); ++i) {
          if(l1Mets[i]->collection() == fL1MetCollection) {
            found = true;
            output.fL1Met = l1Mets[i];
            break;
          }
        }
        if(!found) {
          std::stringstream ss;
          for(size_t i=0; i<l1Mets.size(); ++i) {
            if(i != 0)
              ss << ", ";
            ss << l1Mets[i]->collection();
          }
          throw cms::Exception("LogicError") << "TriggerSelection: did not find L1_ETM object with collection name " << fL1MetCollection << ". Available objects " << ss.str();
        }
        if(output.fL1Met->et() < fL1MetCut)
          passEvent = false;
      }
      if(!passEvent) return passEvent;
      increment(fTriggerL1MetPassedCount);


      // HLT MET
      if(fMetCut < 0) return passEvent;

      pat::TriggerObjectRefVector hltMets = trigger->objects(trigger::TriggerMET);
      /*
      for(size_t i=0; i<hltMets.size(); ++i) {
        std::cout << "HLT MET " << i
                  << " et " << hltMets[i]->et()
                  << " collection " << hltMets[i]->collection()
                  << std::endl;
      }
      */
      if(hltMets.size() == 0) {
        //std::cout << "HLT MET size is 0!" << std::endl;
        output.fHltMet = pat::TriggerObjectRef();
        if(fMetCut >= 0)
          passEvent = false;
      }
      else {
        if(hltMets.size() > 1) {
          pat::TriggerObjectRefVector selectedHltMet;
          for(size_t i=0; i<hltMets.size(); ++i) {
            if(trigger->objectInPath(hltMets[i],  returnPath->getPathName(), false)) { // for MET we don't require that the object was used in the last filter
              /*
              std::cout << "HLT MET " << i
                        << " et " << hltMets[i]->et()
                        << " collection " << hltMets[i]->collection()
                        << std::endl;
              */
              selectedHltMet.push_back(hltMets[i]);
              break;
            }
          }
          ///// HACK HACK HACK
          if(selectedHltMet.size() == 0) {
            for(size_t i=0; i<hltMets.size(); ++i) {
              if(hltMets[i]->collection() == "hltMet::HLT") {
                selectedHltMet.push_back(hltMets[i]);
                break;
              }
            }
          }
          ////// end of hack
          if(selectedHltMet.size() == 0) {
            if(fThrowIfNoMet) {
              std::stringstream ss;
              for(size_t i=0; i<hltMets.size(); ++i) {
                ss << hltMets[i]->collection() << " ";
              }

              throw cms::Exception("LogicError") << "Size of HLT MET collection is " << hltMets.size() 
                                                 << ", tried to find a MET object used in path " << returnPath->getPathName()
                                                 << " but did not find one."
                                                 << " HLT MET collections " << ss.str()
                                                 << std::endl;
            }
            return false;
          }
          hltMets = selectedHltMet;
        }
        
        increment(fTriggerHltMetExistsCount);
        output.fHltMet = hltMets[0];
        hHltMetBeforeTrigger->Fill(output.fHltMet->et());
        if (passEvent)
          hHltMetAfterTrigger->Fill(output.fHltMet->et());

        // Cut on HLT MET
        if(output.fHltMet->et() <= fMetCut) {
          passEvent = false;
        } else if (passEvent) {
          hHltMetSelected->Fill(output.fHltMet->et());
        }
        if(passEvent)
          increment(fTriggerHltMetPassedCount);
      }
    }
    return passEvent;
  }
  
  TriggerSelection::TriggerPath::TriggerPath(const std::string& path, EventCounter& eventCounter):
    fPath(path),
    fTriggerPathFoundCount(eventCounter.addSubCounter("Trigger paths","Path found ("+fPath+")")),
    fTriggerPathAcceptedCount(eventCounter.addSubCounter("Trigger paths","Path accepted ("+fPath+")"))
  {}

  TriggerSelection::TriggerPath::~TriggerPath() {}

  bool TriggerSelection::TriggerPath::analyze(const pat::TriggerEvent& trigger) {
    fTaus.clear();
    fMets.clear();

    const pat::TriggerPath *path = trigger.path(fPath);
    if(!path) return false;
    increment(fTriggerPathFoundCount);

    if(!path->wasAccept()) return false;
    increment(fTriggerPathAcceptedCount);

    pat::TriggerFilterRefVector filters = trigger.pathFilters(fPath, false);
    if(filters.size() == 0)
      throw cms::Exception("LogicError") << "No filters for fired path " << fPath << std::endl;
    pat::TriggerObjectRefVector objs = trigger.filterObjects(filters[filters.size()-1]->label());
    for(pat::TriggerObjectRefVector::const_iterator iObj = objs.begin(); iObj != objs.end(); ++iObj) {
      if((*iObj)->id(trigger::TriggerTau))
        fTaus.push_back(*iObj);
      else if((*iObj)->id(trigger::TriggerMET))
        fMets.push_back(*iObj);
    }

    /*
    objs = trigger.objectRefs();
    for(pat::TriggerObjectRefVector::const_iterator iObj = objs.begin(); iObj != objs.end(); ++iObj) {
      std::cout << "Object " << (iObj-objs.begin()) << " " << (*iObj)->collection() << std::endl;
    }
    for(pat::TriggerFilterRefVector::const_iterator iFilter = filters.begin(); iFilter != filters.end(); ++iFilter) {
      std::cout << "Filter " << (*iFilter)->label() << " object keys ";
      std::vector<unsigned> objectKeys = (*iFilter)->objectKeys();
      for(size_t i=0; i<objectKeys.size(); ++i) {
        std::cout << objectKeys[i] << " ";
      }
      std::cout << std::endl;

      pat::TriggerObjectRefVector objs = trigger.filterObjects((*iFilter)->label());
      for(pat::TriggerObjectRefVector::const_iterator iObj = objs.begin(); iObj != objs.end(); ++iObj) {
        std::cout << "  object " << (*iObj)->collection() << std::endl;
      }
    }
    */

    //std::cout << "============================================================" << std::endl;
    /*
    objs = trigger.objectRefs();
    for(pat::TriggerObjectRefVector::const_iterator iObj = objs.begin(); iObj != objs.end(); ++iObj) {
      std::cout << "Object " << (iObj-objs.begin()) << " " << (*iObj)->collection() << std::endl;
    }
    */
    /*
    for(pat::TriggerFilterRefVector::const_iterator iFilter = filters.begin(); iFilter != filters.end(); ++iFilter) {
      std::cout << "Filter " << (*iFilter)->label() << " object keys ";
      std::vector<unsigned> objectKeys = (*iFilter)->objectKeys();
      for(size_t i=0; i<objectKeys.size(); ++i) {
        std::cout << objectKeys[i] << " ";
      }
      std::cout << std::endl;

      pat::TriggerObjectRefVector objs = trigger.filterObjects((*iFilter)->label());
      for(pat::TriggerObjectRefVector::const_iterator iObj = objs.begin(); iObj != objs.end(); ++iObj) {
        std::cout << "  object " << (*iObj)->collection() << std::endl;
      }
    }
    std::cout << "------------------------------------------------------------" << std::endl;
    */

    return true;

    // Debugging
    /*
    pat::TriggerPathRefVector accepted = trigger.acceptedPaths();
    for(pat::TriggerPathRefVector::const_iterator iter = accepted.begin(); iter != accepted.end(); ++iter) {
      pat::TriggerFilterRefVector filters = trigger.pathFilters((*iter)->name(), false);
      pat::TriggerObjectRefVector objects = trigger.pathObjects((*iter)->name());
      std::vector<unsigned> filterIndices = (*iter)->filterIndices();
      std::cout << "*** (*iter)->name() = " << (*iter)->name() << std::endl;
      std::cout << "    path pointer " << trigger.path((*iter)->name()) << std::endl;
      std::cout << "    filter indices ";
      for(size_t i=0; i<filterIndices.size(); ++i) {
        std::cout << filterIndices[i] << " ";
      }
      std::cout << std::endl;
      std::cout << "    filters (" << filters.size() << ") ";
      for(pat::TriggerFilterRefVector::const_iterator i2 = filters.begin(); i2 != filters.end(); ++i2) {
        std::cout << (*i2)->label() << " ";
      }
      std::cout << std::endl
                << "    objects (" << objects.size() << ") ";
      for(pat::TriggerObjectRefVector::const_iterator i2 = objects.begin(); i2 != objects.end(); ++i2) {
        std::cout << (*i2)->collection() << " ";
      }
      std::cout << std::endl;
    }
    */

    // Below is legacy code, which might be helpful for debugging
    /*
    //pat::TriggerObjectRefVector coll = trigger.pathObjects(fPath);
    pat::TriggerObjectRefVector coll = trigger.objects(trigger::TriggerTau);
    //pat::TriggerObjectRefVector coll = trigger.objects(trigger::TriggerMuon);
    //pat::TriggerObjectRefVector coll = trigger.objects(trigger::TriggerMET);
    for(pat::TriggerObjectRefVector::const_iterator iter = coll.begin(); iter != coll.end(); ++iter) {
      pat::TriggerFilterRefVector filters = trigger.objectFilters(*iter);
      pat::TriggerPathRefVector paths = trigger.objectPaths(*iter, );
      std::cout << "Object from collection " << (*iter)->collection()
                << " passed paths ";
      for(pat::TriggerPathRefVector::const_iterator i2 = paths.begin(); i2 != paths.end(); ++i2) {
        std::cout << (*i2)->name() << " ";
      }
      std::cout << " passed filters ";
      for(pat::TriggerFilterRefVector::const_iterator i2 = filters.begin(); i2 != filters.end(); ++i2) {
        std::cout << (*i2)->label() << " ";
      }
      std::cout << std::endl;
    }

    pat::TriggerFilterRefVector filts = trigger.filterRefs();
    for(pat::TriggerFilterRefVector::const_iterator iter = filts.begin(); iter != filts.end(); ++iter) {
      std::vector<unsigned> keys = (*iter)->objectKeys();
      std::vector<int> ids = (*iter)->objectIds();
      std::cout << "Filter " << (*iter)->label() << " keys ";
      for(size_t i=0; i<keys.size(); ++i) { std::cout << keys[i] << " "; }
      std::cout << " ids ";
      for(size_t i=0; i<ids.size(); ++i) { std::cout << ids[i] << " "; }
      std::cout << " is firing " << (*iter)->isFiring() << std::endl;
      std::cout << std::endl;
    }
    */

    /*
    pat::TriggerPathRefVector accepted = trigger.acceptedPaths();
    for(pat::TriggerPathRefVector::const_iterator iter = accepted.begin(); iter != accepted.end(); ++iter) {
      if((*iter)->name() == fPath && (*iter)->wasAccept()) {
	//std::cout << "*** (*iter)->name() = " << (*iter)->name() << std::endl;
        pat::TriggerFilterRefVector filters = trigger.pathFilters(fPath, false);
        if(filters.size() == 0)
          throw cms::Exception("LogicError") << "No filters for fired path " << fPath << std::endl;
        pat::TriggerObjectRefVector objs = trigger.filterObjects(filters[filters.size()-1]->label());
        for(pat::TriggerObjectRefVector::const_iterator iObj = objs.begin(); iObj != objs.end(); ++iObj) {
          if((*iObj)->id(trigger::TriggerTau))
            fTaus.push_back(*iObj);
          else if((*iObj)->id(trigger::TriggerMET))
            fMets.push_back(*iObj);
        }

        //std::cout << "Trigger " << fPath << " fired, number of taus " << fTaus.size() << " number of mets " << fMets.size() << std::endl;
        increment(fTriggerCount);
        return true;
      }
    }
    return false;
    */
  }

  bool TriggerSelection::TriggerPath::analyze(const edm::TriggerResults& trigger, const edm::TriggerNames& triggerNames) {
    fTaus.clear();
    fMets.clear();
    for(size_t i=0; i<triggerNames.size(); ++i) {
      if(triggerNames.triggerName(i) == fPath && trigger.accept(i)) {
        return true;
      }
    }
    return false;
  }
}
