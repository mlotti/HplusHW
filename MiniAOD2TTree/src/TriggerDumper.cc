#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"

#include <regex>

TriggerDumper::TriggerDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
: trgResultsToken(iConsumesCollector.consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("TriggerResults"))),
  trgObjectsToken(iConsumesCollector.consumes<pat::TriggerObjectStandAloneCollection>(pset.getParameter<edm::InputTag>("TriggerObjects"))),
  trgL1ETMToken(iConsumesCollector.consumes<std::vector<l1extra::L1EtMissParticle>>(pset.getParameter<edm::InputTag>("L1Extra"))) {
    inputCollection = pset;
    booked = false;

    triggerBits = inputCollection.getParameter<std::vector<std::string> >("TriggerBits");
    useFilter = inputCollection.getUntrackedParameter<bool>("filter",false);
//    iBit = new bool[triggerBits.size()];
}
TriggerDumper::~TriggerDumper(){}

void TriggerDumper::book(TTree* tree){
    theTree = tree;
}

void TriggerDumper::book(const edm::Run& iRun, HLTConfigProvider hltConfig){
    booked = true;
    theTree->Branch("L1MET_x",&L1MET_x);
    theTree->Branch("L1MET_y",&L1MET_y);
    theTree->Branch("HLTMET_x",&HLTMET_x);
    theTree->Branch("HLTMET_y",&HLTMET_y);
    
    theTree->Branch("HLTTau_pt",&HLTTau_pt);  
    theTree->Branch("HLTTau_eta",&HLTTau_eta);
    theTree->Branch("HLTTau_phi",&HLTTau_phi);
    theTree->Branch("HLTTau_e",&HLTTau_e);

    std::vector<std::string> selectedTriggers;

    for(size_t i = 0; i < triggerBits.size(); ++i){
        std::regex hlt_re(triggerBits[i]);
        std::vector<std::string> hltPaths = hltConfig.triggerNames();
        for(size_t i = 0; i < hltPaths.size(); ++i){
            if (std::regex_search(hltPaths[i], hlt_re)) {
                selectedTriggers.push_back(hltPaths[i]);
            }
        }
    }

    iBit = new bool[selectedTriggers.size()];
    for(size_t i = 0; i < selectedTriggers.size(); ++i){
        theTree->Branch(selectedTriggers[i].c_str(),&iBit[i]);
    }
}

bool TriggerDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    edm::Handle<std::vector<l1extra::L1EtMissParticle> > l1etmhandle;
    iEvent.getByToken(trgL1ETMToken, l1etmhandle);
    L1MET_x = 0.0;
    L1MET_y = 0.0;
    if(l1etmhandle.isValid() && l1etmhandle->size() > 0){
	L1MET_x = l1etmhandle.product()->begin()->x();
	L1MET_y = l1etmhandle.product()->begin()->y();
    }

    edm::Handle<edm::TriggerResults> trgResultsHandle;
    iEvent.getByToken(trgResultsToken, trgResultsHandle);
    if(trgResultsHandle.isValid()){
        edm::TriggerResults tr = *trgResultsHandle;
	bool fromPSetRegistry;
        edm::Service<edm::service::TriggerNamesService> tns;
	std::vector<std::string> hlNames;
        tns->getTrigPaths(tr, hlNames, fromPSetRegistry);

	for(size_t i = 0; i < triggerBits.size(); ++i){
            iBit[i] = false;
            std::regex hlt_re(triggerBits[i]);
	    int n = 0;
	    for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		if (std::regex_search(*j, hlt_re)) {
		    iBit[i] = trgResultsHandle->accept(n);
		    continue;
		}
		n++;
	    }  
	}
    }

    HLTMET_x = 0;
    HLTMET_y = 0;
    edm::Handle<pat::TriggerObjectStandAloneCollection> patTriggerObjects;
    iEvent.getByToken(trgObjectsToken,patTriggerObjects);
    if(patTriggerObjects.isValid()){
	for(pat::TriggerObjectStandAloneCollection::const_iterator patTriggerObject = patTriggerObjects->begin();
            patTriggerObject != patTriggerObjects->end(); ++patTriggerObject ) {
	    if(patTriggerObject->id(trigger::TriggerMET)){
                HLTMET_x = patTriggerObject->p4().x();
                HLTMET_y = patTriggerObject->p4().y();
		//std::cout << "Trigger MET " << patTriggerObject->p4().Pt() << std::endl;
	    }
	    if(patTriggerObject->id(trigger::TriggerTau)){
                HLTTau_pt.push_back(patTriggerObject->p4().Pt());
                HLTTau_eta.push_back(patTriggerObject->p4().Eta());
                HLTTau_phi.push_back(patTriggerObject->p4().Phi());
                HLTTau_e.push_back(patTriggerObject->p4().E());
		//std::cout << "Trigger Tau " << patTriggerObject->p4().Pt() << std::endl;
	    }
	}
    }

    return filter();
}

bool TriggerDumper::filter(){
    if(!useFilter) return true;

    bool passed = false;
    for(size_t i = 0; i < triggerBits.size(); ++i){
	if(iBit[i]) passed = true;
    }
    return passed;
}

void TriggerDumper::reset(){
    if(booked){
      for(size_t i = 0; i < triggerBits.size(); ++i) iBit[i] = 0;
      L1MET_x = 0;
      L1MET_y = 0;
      HLTMET_x = 0;
      HLTMET_y = 0;

      HLTTau_pt.clear();
      HLTTau_eta.clear();
      HLTTau_phi.clear();
      HLTTau_e.clear();
    }
}
