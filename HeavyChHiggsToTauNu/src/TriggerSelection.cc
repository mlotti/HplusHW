#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "TH1F.h"

namespace HPlus {
  TriggerSelection::Data::Data(const TriggerSelection *triggerSelection, const TriggerPath *triggerPath, bool passedEvent):
    fTriggerSelection(triggerSelection), fTriggerPath(triggerPath), fPassedEvent(passedEvent) {}
  TriggerSelection::Data::~Data() {}
  
  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fTriggerSrc(iConfig.getUntrackedParameter<edm::InputTag>("triggerSrc")),
    fPatSrc(iConfig.getUntrackedParameter<edm::InputTag>("patSrc")),
    fMetCut(iConfig.getUntrackedParameter<double>("hltMetCut")),
    fEventWeight(eventWeight),
    fTriggerTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerTauSelection"), eventCounter, eventWeight, 1, "triggerTau"),
    fTriggerMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerMETSelection"), eventCounter, eventWeight, "triggerMET"),
    fTriggerEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiency")),
    fTriggerCaloMet(iConfig.getUntrackedParameter<edm::ParameterSet>("caloMetSelection"), eventCounter, eventWeight),
    fTriggerAllCount(eventCounter.addSubCounter("Trigger", "All events")),
    fTriggerPathCount(eventCounter.addSubCounter("Trigger debug", "Path passed")),
    fTriggerBitCount(eventCounter.addSubCounter("Trigger","Bit passed")), 
    fTriggerCaloMetCount(eventCounter.addSubCounter("Trigger","CaloMET cut passed")), 
    fTriggerCount(eventCounter.addSubCounter("Trigger","Passed")),
    fTriggerHltMetExistsCount(eventCounter.addSubCounter("Trigger debug", "HLT MET object exists")),
    fTriggerScaleFactorAllCount(eventCounter.addSubCounter("Trigger scale factor", "All events")),
    fTriggerScaleFactorAppliedCount(eventCounter.addSubCounter("Trigger scale factor", "Has tau pt>40")),
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
    } else if (mySelectionType == "byTriggerBitApplyScaleFactor") {
      fTriggerSelectionType = kTriggerSelectionByTriggerBitApplyScaleFactor;
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
    hControlSelectionType = makeTH<TH1F>(myDir, "Control_Trigger_Selection_Type", "Control_Trigger_Selection_Type;;N_{events}", 3, 0., 3.);
    hControlSelectionType->GetXaxis()->SetBinLabel(1, "byTriggerBit");
    hControlSelectionType->GetXaxis()->SetBinLabel(2, "byTriggerBit+ScaleFactor");
    hControlSelectionType->GetXaxis()->SetBinLabel(3, "byTriggerEffParam");
    hScaleFactor = makeTH<TH1F>(myDir, "TriggerScaleFactor", "TriggerScaleFactor;TriggerScaleFactor;N_{events}/0.01", 200., 0., 2.0);
    hScaleFactorRelativeUncertainty = makeTH<TH1F>(myDir, "TriggerScaleFactorRelativeUncertainty", "TriggerScaleFactorRelativeUncertainty;TriggerScaleFactorRelativeUncertainty;N_{events}/0.001", 2000., 0., 2.0);
    hScaleFactorAbsoluteUncertainty = makeTH<TH1F>(myDir, "TriggerScaleFactorAbsoluteUncertainty", "TriggerScaleFactorAbsoluteUncertainty;TriggerScaleFactorAbsoluteUncertainty;N_{events}/0.001", 2000., 0., 2.0);

    // Hard code trigger efficiency values for the scale factor
    fTriggerScaleFactor.setValue(40, 0.4035088, 0.06502412, 0.406639,  0.02247143);
    fTriggerScaleFactor.setValue(50, 0.7857143, 0.1164651,  0.6967213, 0.04239523);
    fTriggerScaleFactor.setValue(60, 0.8,       0.1108131,  0.8235294, 0.04892095);
    fTriggerScaleFactor.setValue(80, 1,         0.2496484,  0.7916667, 0.08808045);
  }

  TriggerSelection::~TriggerSelection() {
    for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i) delete *i;
  }

  TriggerSelection::Data TriggerSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = true;
    fScaleFactor = 1.0;
    TriggerPath* returnPath = NULL;
    increment(fTriggerAllCount);

    hControlSelectionType->Fill(fTriggerSelectionType, fEventWeight.getWeight());
    if (fTriggerSelectionType == kTriggerSelectionByTriggerBit ||
        fTriggerSelectionType == kTriggerSelectionByTriggerBitApplyScaleFactor) {
      passEvent = passedTriggerBit(iEvent, iSetup, returnPath);
    }
    
    // Calo MET cut; needed for non QCD1, disabled for others
    if(passEvent) {
      increment(fTriggerBitCount);
      TriggerMETEmulation::Data ret = fTriggerCaloMet.analyze(iEvent, iSetup);
      passEvent = ret.passedEvent();
    }

    // Trigger efficiency parametrisation, needed for non QCD1, disabled for others
    if(passEvent) {
      increment(fTriggerCaloMetCount);
      if (fTriggerSelectionType == kTriggerSelectionByTriggerEfficiencyParametrisation)
        passEvent = passedTriggerParametrisation(iEvent, iSetup);
    }

    if(passEvent) {
      increment(fTriggerCaloMetCount);
      //if (fTriggerSelectionType == kTriggerSelectionByTriggerBitApplyScaleFactor)
      //passEvent = passedTriggerScaleFactor(iEvent, iSetup); // do not apply trigger scale factor here, instead call it after tau isolation
      if(fTriggerSelectionType == kTriggerSelectionDisabled)
        passEvent = true;
    }
    
    if(passEvent) increment(fTriggerCount);
    return Data(this, returnPath, passEvent);
  }
  
  bool TriggerSelection::passedTriggerBit(const edm::Event& iEvent, const edm::EventSetup& iSetup, TriggerPath*& returnPath) {
    bool passEvent = false;
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
  
  bool TriggerSelection::passedTriggerScaleFactor(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    if (iEvent.isRealData()) return true;

    //increment(fTriggerParamAllCount);
    increment(fTriggerScaleFactorAllCount);
    // Get Tau object
    TauSelection::Data triggerTauData = fTriggerTauSelection.analyzeTriggerTau(iEvent, iSetup);
    if (!triggerTauData.passedEvent()) return false; // Need to have at least (but preferably exactly) one tau in the events
    //increment(fTriggerParamTauCount);
    // Do lookup of scale factor for MC
    double myPt = (triggerTauData.getSelectedTaus()[0])->pt();
    if (myPt > 40) {
      fScaleFactor = fTriggerScaleFactor.getScaleFactor(myPt);
      hScaleFactor->Fill(fScaleFactor, fEventWeight.getWeight());
      hScaleFactorRelativeUncertainty->Fill(fTriggerScaleFactor.getScaleFactorRelativeUncertainty(myPt), fEventWeight.getWeight());
      hScaleFactorAbsoluteUncertainty->Fill(fTriggerScaleFactor.getScaleFactorAbsoluteUncertainty(myPt), fEventWeight.getWeight());
      // Apply scale factor
      fEventWeight.multiplyWeight(fScaleFactor);
      increment(fTriggerScaleFactorAllCount);
    }

    // Get MET object 
    //    METSelection::Data triggerMetData = fTriggerMETSelection.analyze(iEvent, iSetup);
    //if (!triggerMetData.passedEvent()) return false;
    //increment(fTriggerParamMetCount);
    // Obtain trigger efficiency and apply it as a weight
    /*double triggerEfficiency = fTriggerEfficiency.efficiency(*(triggerTauData.getSelectedTaus()[0]), *triggerMetData.getSelectedMET());
    hTriggerParametrisationWeight->Fill(triggerEfficiency, fEventWeight.getWeight());
    fEventWeight.multiplyWeight(triggerEfficiency);*/
    
    return true;
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
    // abuse fScaleFactor to store the efficiency from parametrisation, as the variable is not used when parametrisation is
    fScaleFactor = triggerEfficiency;
    fEventWeight.multiplyWeight(fScaleFactor);

    return true;
  }

  TriggerSelection::TriggerPath::TriggerPath(const std::string& path, EventCounter& eventCounter):
    fPath(path),
    fTriggerCount(eventCounter.addSubCounter("Trigger paths","Triggered ("+fPath+")"))
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

  bool TriggerSelection::TriggerPath::analyze(const edm::TriggerResults& trigger, const edm::TriggerNames& triggerNames) {
    for(size_t i=0; i<triggerNames.size(); ++i) {
      if(triggerNames.triggerName(i) == fPath && trigger.accept(i)) {
        return true;
      }
    }
    return false;
  }


  TriggerSelection::TriggerScaleFactor::TriggerScaleFactor() { }
  TriggerSelection::TriggerScaleFactor::~TriggerScaleFactor() { }

  void TriggerSelection::TriggerScaleFactor::setValue(double ptLowEdge, double dataEff, double dataUncertainty, double MCEff, double MCUncertainty) {
    fTriggerEffPtBinEdge.push_back(ptLowEdge);
    fTriggerEffDataValues.push_back(dataEff);
    fTriggerEffDataUncertainty.push_back(dataUncertainty);
    fTriggerEffMCValues.push_back(MCEff);
    fTriggerEffMCUncertainty.push_back(MCUncertainty);
  }

  double TriggerSelection::TriggerScaleFactor::getScaleFactor(double tauPt) const {
    size_t myIndex = obtainIndex(tauPt);
    return fTriggerEffDataValues[myIndex] / fTriggerEffMCValues[myIndex];
  }

  double TriggerSelection::TriggerScaleFactor::getScaleFactorRelativeUncertainty(double tauPt) const {
    size_t myIndex = obtainIndex(tauPt);
    // Do error propagation for f = effData / effMC 
    double myDataPart = fTriggerEffDataUncertainty[myIndex] / fTriggerEffDataValues[myIndex];
    double myMCPart = fTriggerEffMCUncertainty[myIndex] / fTriggerEffMCValues[myIndex];
    return (std::sqrt(myDataPart*myDataPart + myMCPart*myMCPart));
  }
  double TriggerSelection::TriggerScaleFactor::getScaleFactorAbsoluteUncertainty(double tauPt) const {
    return getScaleFactor(tauPt) * getScaleFactorRelativeUncertainty(tauPt);
  }

  size_t TriggerSelection::TriggerScaleFactor::obtainIndex(double pt) const {
    size_t myEnd = fTriggerEffPtBinEdge.size();
    size_t myPos = 0;
    while (myPos < myEnd) {
      if (pt < fTriggerEffPtBinEdge[myPos]) {
        if (myPos == 0)
          return 0; // should never happen
        else
          return myPos-1;
      }
      ++myPos;
    }
    return myEnd-1; // return last bin
  }
}
