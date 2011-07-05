#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "TH1F.h"

namespace HPlus {
  TriggerSelection::Data::Data(const TriggerSelection *triggerSelection, const TriggerPath *triggerPath, bool passedEvent):
    fTriggerSelection(triggerSelection), fTriggerPath(triggerPath), fPassedEvent(passedEvent) {}
  TriggerSelection::Data::~Data() {}
  
  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMetCut(iConfig.getUntrackedParameter<double>("hltMetCut")),
    fEventWeight(eventWeight),
    fTriggerTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerTauSelection"), eventCounter, eventWeight, 1, "triggerTau"),
    fTriggerMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerMETSelection"), eventCounter, eventWeight, "triggerMET"),
    fTriggerEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiency")),
    fTriggerCaloMet(iConfig.getUntrackedParameter<edm::ParameterSet>("caloMetSelection"), eventCounter, eventWeight),
    fTriggerPathCount(eventCounter.addSubCounter("Trigger", "Path passed")),
    fTriggerBitParamCount(eventCounter.addSubCounter("Trigger","Bit/parametrisation passed")), 
    fTriggerCount(eventCounter.addSubCounter("Trigger","Passed")),
    fTriggerHltMetExistsCount(eventCounter.addSubCounter("Trigger debug", "HLT MET object exists")),
    fTriggerParamAllCount(eventCounter.addSubCounter("Trigger parametrisation", "All events")),
    fTriggerParamTauCount(eventCounter.addSubCounter("Trigger parametrisation", "Tau passed")),
    fTriggerParamMetCount(eventCounter.addSubCounter("Trigger parametrisation", "Met passed")),
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
    } else if (mySelectionType == "byParametrisation") {
      fTriggerSelectionType = kTriggerSelectionByTriggerEfficiencyParametrisation;
    } else if(mySelectionType == "disabled") {
      fTriggerSelectionType = kTriggerSelectionDisabled;
    } else throw cms::Exception("Configuration") << "TriggerSelection: no or unknown selection type! Options for 'selectionType' are: byTriggerBit, byParametrisation, disabled (you chose '"
      << mySelectionType << "')" << std::endl;

    // Histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("Trigger");
    
    hHltMetBeforeTrigger = makeTH<TH1F>(myDir, "Trigger_HLT_MET_Before_Trigger", "HLT_MET_After_Trigger;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
    hHltMetAfterTrigger = makeTH<TH1F>(myDir, "Trigger_HLT_MET_After_Trigger", "HLT_MET_After_Trigger;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
    hHltMetSelected = makeTH<TH1F>(myDir, "Trigger_HLT_MET_Selected", "HLT_MET_Selected;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
    hTriggerParametrisationWeight = makeTH<TH1F>(myDir, "Trigger_Parametrisation_Weight", "Trigger_Parametrisation_Weight;Weight*1000;N_{events} / 0.1 percent", 1000, 0., 1000.);
    hControlSelectionType = makeTH<TH1F>(myDir, "Control_Trigger_Selection_Type", "Control_Trigger_Selection_Type;;N_{events}", 2, 0., 2.);
    hControlSelectionType->GetXaxis()->SetBinLabel(1, "byTriggerBit");
    hControlSelectionType->GetXaxis()->SetBinLabel(2, "byTriggerEffParam");
  }

  TriggerSelection::~TriggerSelection() {
    for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i) delete *i;
  }

  TriggerSelection::Data TriggerSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
    TriggerPath* returnPath = NULL;
    hControlSelectionType->Fill(fTriggerSelectionType, fEventWeight.getWeight());
    if (fTriggerSelectionType == kTriggerSelectionByTriggerBit)
      passEvent = passedTriggerBit(iEvent, iSetup, returnPath);
    else if (fTriggerSelectionType == kTriggerSelectionByTriggerEfficiencyParametrisation)
      passEvent = passedTriggerParametrisation(iEvent, iSetup);
    else if(fTriggerSelectionType == kTriggerSelectionDisabled)
      passEvent = true;
    
    if(passEvent) {
      increment(fTriggerBitParamCount);
      TriggerMETEmulation::Data ret = fTriggerCaloMet.analyze(iEvent, iSetup);
      passEvent = ret.passedEvent();
    }

    if(passEvent) increment(fTriggerCount);
    return Data(this, returnPath, passEvent);
  }
  
  bool TriggerSelection::passedTriggerBit(const edm::Event& iEvent, const edm::EventSetup& iSetup, TriggerPath*& returnPath) {
    edm::Handle<pat::TriggerEvent> trigger;
    iEvent.getByLabel(fSrc, trigger);
    bool passEvent = false;

    for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i){
      if((*i)->analyze(*trigger)) {
        passEvent = true;
        returnPath = *i;
      }
    }
    if(passEvent)
      increment(fTriggerPathCount);

    // Get HLT MET object
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
      pat::TriggerObjectRefVector hltMets = trigger->objects(trigger::TriggerMET);
      if(hltMets.size() == 0) {
        fHltMet = pat::TriggerObjectRef();
        if(fMetCut >= 0)
          passEvent = false;
      }
      else {
        if(hltMets.size() > 1) {
          pat::TriggerObjectRefVector selectedHltMet;
          for(size_t i=0; i<hltMets.size(); ++i) {
            if(trigger->objectInPath(hltMets[i],  returnPath->getPathName())) {
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
        fHltMet = hltMets[0];
        hHltMetBeforeTrigger->Fill(fHltMet->et(), fEventWeight.getWeight());
        if (passEvent)
          hHltMetAfterTrigger->Fill(fHltMet->et(), fEventWeight.getWeight());

        // Cut on HLT MET
        if(fHltMet->et() <= fMetCut) {
          passEvent = false;
        } else if (passEvent) {
          hHltMetSelected->Fill(fHltMet->et(), fEventWeight.getWeight());
        }
      }
    }
    return passEvent;
  }
  
  bool TriggerSelection::passedTriggerParametrisation(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fTriggerParamAllCount);
    // Get Tau object
    TauSelection::Data triggerTauData = fTriggerTauSelection.analyze(iEvent, iSetup);
    if (!triggerTauData.passedEvent()) return false; // Need to have at least (but preferably exactly) one tau in the events
    increment(fTriggerParamTauCount);
    // Get MET object 
    METSelection::Data triggerMetData = fTriggerMETSelection.analyze(iEvent, iSetup);
    //if (!triggerMetData.passedEvent()) return false;
    increment(fTriggerParamMetCount);
    // Obtain trigger efficiency and apply it as a weight
    double triggerEfficiency = fTriggerEfficiency.efficiency(*(triggerTauData.getSelectedTaus()[0]), *triggerMetData.getSelectedMET());
    hTriggerParametrisationWeight->Fill(triggerEfficiency, fEventWeight.getWeight());
    fEventWeight.multiplyWeight(triggerEfficiency);
    
    return true;
  }

  TriggerSelection::TriggerPath::TriggerPath(const std::string& path, EventCounter& eventCounter):
    fPath(path),
    fTriggerCount(eventCounter.addSubCounter("Trigger","Triggered ("+fPath+")"))
  {}

  TriggerSelection::TriggerPath::~TriggerPath() {}

  bool TriggerSelection::TriggerPath::analyze(const pat::TriggerEvent& trigger) {
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

    pat::TriggerPathRefVector accepted = trigger.acceptedPaths();
    for(pat::TriggerPathRefVector::const_iterator iter = accepted.begin(); iter != accepted.end(); ++iter) {
      /*
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
      */

      if((*iter)->name() == fPath && (*iter)->wasAccept()) {
	//std::cout << "*** (*iter)->name() = " << (*iter)->name() << std::endl;
        increment(fTriggerCount);
        return true;
      }
    }
    return false;
  }
}
