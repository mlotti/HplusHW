#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"

#include <regex>

TriggerDumper::TriggerDumper(edm::ParameterSet& pset){
    inputCollection = pset;
    booked = false;

    triggerResults = inputCollection.getParameter<edm::InputTag>("TriggerResults");
    triggerBits = inputCollection.getParameter<std::vector<std::string> >("TriggerBits");
    triggerObjects = inputCollection.getParameter<edm::InputTag>("TriggerObjects");
    l1extra = inputCollection.getParameter<edm::InputTag>("L1Extra");
    useFilter = inputCollection.getUntrackedParameter<bool>("filter",false);
//    iBit = new bool[triggerBits.size()];
}
TriggerDumper::~TriggerDumper(){}

void TriggerDumper::book(TTree* tree){
    theTree = tree;
}

void TriggerDumper::book(const edm::Run& iRun, HLTConfigProvider hltConfig){
    booked = true;
    theTree->Branch("L1MET_et",&L1MET);
    theTree->Branch("L1MET_phi",&L1METphi);
    theTree->Branch("HLTMET_et",&HLTMET);
    theTree->Branch("HLTMET_phi",&HLTMETphi);
    
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
    iEvent.getByLabel(l1extra, l1etmhandle);
    if(l1etmhandle.isValid()){
	L1MET    = l1etmhandle.product()->begin()->et();
	L1METphi = l1etmhandle.product()->begin()->phi();
    }

    iEvent.getByLabel(triggerResults,handle);
    if(handle.isValid()){
        edm::TriggerResults tr = *handle;
	bool fromPSetRegistry;
        edm::Service<edm::service::TriggerNamesService> tns;
	std::vector<std::string> hlNames;
        tns->getTrigPaths(tr, hlNames, fromPSetRegistry);

	for(size_t i = 0; i < triggerBits.size(); ++i){
	    std::regex hlt_re(triggerBits[i]);
	    int n = 0;
	    for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		if (std::regex_search(*j, hlt_re)) {
		    iBit[i] = handle->accept(n);
		    continue;
		}
		n++;
	    }  
	}
    }

    HLTMET    = 0;
    HLTMETphi = 0;
    edm::Handle<pat::TriggerObjectStandAloneCollection> patTriggerObjects;
    iEvent.getByLabel(triggerObjects,patTriggerObjects);
    if(patTriggerObjects.isValid()){
	for(pat::TriggerObjectStandAloneCollection::const_iterator patTriggerObject = patTriggerObjects->begin();
            patTriggerObject != patTriggerObjects->end(); ++patTriggerObject ) {
	    if(patTriggerObject->id(trigger::TriggerMET)){
                HLTMET    = patTriggerObject->p4().Pt();
                HLTMETphi = patTriggerObject->p4().Phi();
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
      L1MET = 0;
      L1METphi = 0;
      HLTMET = 0;
      HLTMETphi = 0;

      HLTTau_pt.clear();
      HLTTau_eta.clear();
      HLTTau_phi.clear();
      HLTTau_e.clear();
    }
}
