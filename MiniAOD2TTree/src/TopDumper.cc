#include "HiggsAnalysis/MiniAOD2TTree/interface/TopDumper.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/JetReco/interface/PileupJetIdentifier.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/NtupleAnalysis_fwd.h"

TopDumper::TopDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
    inputCollections = psets;
    booked           = false;

    edm::InputTag inputtag = inputCollections[0].getParameter<edm::InputTag>("src");
    topToken = iConsumesCollector.consumes<edm::View<reco::CATopJetTagInfo>>(inputtag);


    minMass = new std::vector<double>[inputCollections.size()];
    topMass = new std::vector<double>[inputCollections.size()];    
    wMass = new std::vector<double>[inputCollections.size()];
    nSubJets = new std::vector<int>[inputCollections.size()];    
}

TopDumper::~TopDumper(){}

void TopDumper::book(TTree* tree){
  booked = true;
  for(size_t i = 0; i < inputCollections.size(); ++i){
    std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
    if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();

    tree->Branch((name+"_minMass").c_str(),&minMass[i]);
    tree->Branch((name+"_topMass").c_str(),&topMass[i]);
    tree->Branch((name+"_wMass").c_str(),&wMass[i]);
    tree->Branch((name+"_nSubJets").c_str(),&nSubJets[i]);
  }
}

bool TopDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
	
        edm::Handle<edm::View<reco::CATopJetTagInfo>> topHandle;
	iEvent.getByToken(topToken, topHandle);

	if(topHandle.isValid()){
	  for(size_t i=0; i<topHandle->size(); ++i) {                                                                                            
	    const reco::CATopJetTagInfo& tagInfo = topHandle->at(i);
	    minMass[ic].push_back(tagInfo.properties().minMass);
	    topMass[ic].push_back(tagInfo.properties().topMass);
	    wMass[ic].push_back(tagInfo.properties().wMass);
	    nSubJets[ic].push_back(tagInfo.properties().nSubJets);
	  }
	}
    }
    return filter();
}

void TopDumper::reset(){
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){

	minMass[ic].clear();
	topMass[ic].clear();
        wMass[ic].clear();
	nSubJets[ic].clear();
    }
}
