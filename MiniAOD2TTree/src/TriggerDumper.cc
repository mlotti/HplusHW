#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"

TriggerDumper::TriggerDumper(edm::ParameterSet& pset){
    inputCollection = pset;
    booked = false;

    triggerResults = inputCollection.getParameter<edm::InputTag>("TriggerResults");
    triggerBits = inputCollection.getParameter<std::vector<std::string> >("TriggerBits");
    triggerObjects = inputCollection.getParameter<edm::InputTag>("TriggerObjects");
    l1extra = inputCollection.getParameter<edm::InputTag>("L1Extra");
    useFilter = inputCollection.getUntrackedParameter<bool>("filter",false);
    iBit = new bool[triggerBits.size()];
}
TriggerDumper::~TriggerDumper(){}

void TriggerDumper::book(TTree* tree){
    booked = true;
    tree->Branch("L1_ETM",&L1MET);
    tree->Branch("L1_ETMphi",&L1METphi);
    tree->Branch("HLT_MET",&HLTMET);
    tree->Branch("HLT_METphi",&HLTMETphi);

    tree->Branch("HLTTau_pt",&HLTTau_pt);
    tree->Branch("HLTTau_eta",&HLTTau_eta);
    tree->Branch("HLTTau_phi",&HLTTau_phi);
    tree->Branch("HLTTau_e",&HLTTau_e);

    for(size_t i = 0; i < triggerBits.size(); ++i){
	tree->Branch(triggerBits[i].c_str(),&iBit[i]);
    }
}

bool TriggerDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

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
	    int n = 0;
	    for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		if(triggerBits[i] == *j) {
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
