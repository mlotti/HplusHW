#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"

#include <regex>
#include "Math/VectorUtil.h"

TriggerDumper::TriggerDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
: trgResultsToken(iConsumesCollector.consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("TriggerResults"))),
  trgObjectsToken(iConsumesCollector.consumes<pat::TriggerObjectStandAloneCollection>(pset.getParameter<edm::InputTag>("TriggerObjects"))),
  trgL1ETMToken(iConsumesCollector.consumes<std::vector<l1extra::L1EtMissParticle>>(pset.getParameter<edm::InputTag>("L1Extra"))) {
    inputCollection = pset;
    booked = false;

    triggerBits = inputCollection.getParameter<std::vector<std::string> >("TriggerBits");
    useFilter = inputCollection.getUntrackedParameter<bool>("filter",false);
//    iBit = new bool[triggerBits.size()];

    trgMatchStr = inputCollection.getUntrackedParameter<std::vector<std::string> >("TriggerMatch",std::vector<std::string>());
    trgMatchDr = inputCollection.getUntrackedParameter<double>("TriggerMatchDR",0.1);

    if(inputCollection.exists("TriggerPrescales")){
      trgPrescaleToken = iConsumesCollector.consumes<pat::PackedTriggerPrescales>(inputCollection.getUntrackedParameter<edm::ParameterSet>("TriggerPrescales").getParameter<edm::InputTag>("src"));
      trgPrescalePaths = inputCollection.getUntrackedParameter<edm::ParameterSet>("TriggerPrescales").getParameter<std::vector<std::string> >("paths");
    }
}
TriggerDumper::~TriggerDumper(){}

void TriggerDumper::book(TTree* tree){
    theTree = tree;
}

void TriggerDumper::book(const edm::Run& iRun, HLTConfigProvider hltConfig){

    if(booked) return;
    booked = true;

    theTree->Branch("L1MET_l1extra_x",&L1MET_l1extra_x);
    theTree->Branch("L1MET_l1extra_y",&L1MET_l1extra_y);
    theTree->Branch("L1MET_x",&L1MET_x);
    theTree->Branch("L1MET_y",&L1MET_y);
    theTree->Branch("HLTMET_x",&HLTMET_x);
    theTree->Branch("HLTMET_y",&HLTMET_y);
    
    theTree->Branch("HLTTau_pt",&HLTTau_pt);  
    theTree->Branch("HLTTau_eta",&HLTTau_eta);
    theTree->Branch("HLTTau_phi",&HLTTau_phi);
    theTree->Branch("HLTTau_e",&HLTTau_e);

//    std::vector<std::string> selectedTriggers;

    for(size_t i = 0; i < triggerBits.size(); ++i){
        selectedTriggers.push_back(triggerBits[i]);
        // Do not find the exact names or versions of HLT path names
        // because they do change in the middle of the run causing buggy behavior
    }

    iBit         = new bool[selectedTriggers.size()];
    iCountAll    = new int[selectedTriggers.size()];
    iCountPassed = new int[selectedTriggers.size()];

    for(size_t i = 0; i < selectedTriggers.size(); ++i){
        theTree->Branch(std::string(selectedTriggers[i]+"x").c_str(),&iBit[i]);
        iCountAll[i]    = 0;
        iCountPassed[i] = 0;
    }

    // Trigger matching
    std::regex obj_re("((Tau)|(Mu))");
    for(size_t imatch = 0; imatch < trgMatchStr.size(); ++imatch){
	std::string name = "";
	std::smatch match;
	if (std::regex_search(trgMatchStr[imatch], match, obj_re) && match.size() > 0) name = match.str(0); 
	if(name=="Tau") name = "Taus"; // FIXME, these should come from the config
        if(name=="Mu") name = "Muons"; // FIXME, these should come from the config
	name+= "_TrgMatch_";

	std::regex match_re(trgMatchStr[imatch]);
	for(size_t i = 0; i < selectedTriggers.size(); ++i){		
	    if (std::regex_search(selectedTriggers[i], match_re)) {
		std::string branchName = name+trgMatchStr[imatch];
		bool exists = false;
		for(size_t j = 0; j < trgMatchBranches.size(); ++j){
		    if(trgMatchBranches[j] == branchName){
		        exists = true;
		        break;
		    }
		}
		if(!exists) trgMatchBranches.push_back(branchName);
	    }
	}
    }
    nTrgDiscriminators = trgMatchBranches.size();
    trgdiscriminators = new std::vector<bool>[nTrgDiscriminators];
    for(size_t i = 0; i < trgMatchBranches.size(); ++i){
	theTree->Branch(trgMatchBranches[i].c_str(),&trgdiscriminators[i]);
    }

    int nTrgPrescales = trgPrescalePaths.size();
    trgprescales = new std::vector<int>[nTrgPrescales];
    for(size_t i = 0; i < trgPrescalePaths.size(); ++i){
        std::string bname = trgPrescalePaths[i]+"x_prescale";
        theTree->Branch(bname.c_str(),&trgprescales[i]);
    }
}

bool TriggerDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
    edm::Handle<std::vector<l1extra::L1EtMissParticle> > l1etmhandle;
    iEvent.getByToken(trgL1ETMToken, l1etmhandle);
    L1MET_l1extra_x = 0.0;
    L1MET_l1extra_y = 0.0;
    if(l1etmhandle.isValid() && l1etmhandle->size() > 0){
	L1MET_l1extra_x = l1etmhandle.product()->begin()->px();
	L1MET_l1extra_y = l1etmhandle.product()->begin()->py();
    }

    edm::Handle<edm::TriggerResults> trgResultsHandle;
    iEvent.getByToken(trgResultsToken, trgResultsHandle);
    if(trgResultsHandle.isValid()){
	names = iEvent.triggerNames(*trgResultsHandle);

        for(size_t i = 0; i < selectedTriggers.size(); ++i){
            iBit[i] = false;
            for(size_t j = 0; j < trgResultsHandle->size(); ++j){
                size_t pos = names.triggerName(j).find(selectedTriggers[i]);
                if (pos == 0 && names.triggerName(j).size() > 0) {
                    iBit[i] = trgResultsHandle->accept(j);
                    iCountAll[i] += 1;
                    if(trgResultsHandle->accept(j)) iCountPassed[i] += 1;
                    continue;
                }
            }
        }

    	L1MET_x  = 0;  
    	L1MET_y  = 0;
        HLTMET_x = 0;
        HLTMET_y = 0;
//        edm::Handle<pat::TriggerObjectStandAloneCollection> patTriggerObjects;
        iEvent.getByToken(trgObjectsToken,patTriggerObjects);
        if(patTriggerObjects.isValid()){
	    for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
	        patTriggerObject.unpackPathNames(names);
                if(patTriggerObject.id(trigger::TriggerL1ETM)){
                    L1MET_x = patTriggerObject.p4().x(); 
                    L1MET_y = patTriggerObject.p4().y();
                //std::cout << "Trigger L1ETM " << patTriggerObject.p4().Pt() << std::endl;
		}
	        if(patTriggerObject.id(trigger::TriggerMET)){
                    HLTMET_x = patTriggerObject.p4().x();
                    HLTMET_y = patTriggerObject.p4().y();
		//std::cout << "Trigger MET " << patTriggerObject.p4().Pt() << std::endl;
	        }
	        if(patTriggerObject.id(trigger::TriggerTau)){

                    std::vector<std::string> pathNamesAll  = patTriggerObject.pathNames(false);
		    bool fired = false;
                    for(size_t i = 0; i < pathNamesAll.size(); ++i){
		      if(patTriggerObject.hasPathName( pathNamesAll[i], false, true )) fired = true;
                    }
		    if(fired){
                        HLTTau_pt.push_back(patTriggerObject.p4().Pt());
                        HLTTau_eta.push_back(patTriggerObject.p4().Eta());
                        HLTTau_phi.push_back(patTriggerObject.p4().Phi());
                        HLTTau_e.push_back(patTriggerObject.p4().E());
		    }
		//std::cout << "Trigger Tau " << patTriggerObject.p4().Pt() << std::endl;
	        }
            }
	}

        if(iEvent.isRealData() && trgPrescalePaths.size() > 0){
          edm::Handle<pat::PackedTriggerPrescales> trgPrescaleHandle;
          iEvent.getByToken(trgPrescaleToken, trgPrescaleHandle);
          if(trgPrescaleHandle.isValid()){
            pat::PackedTriggerPrescales prescales = *trgPrescaleHandle.product();
            prescales.setTriggerNames(names);
            for(std::vector<std::string>::const_iterator i = trgPrescalePaths.begin(); i != trgPrescalePaths.end(); ++i){
              int prescale = prescales.getPrescaleForName(*i,true);
              trgprescales->push_back(prescale);
              //std::cout << *i << " " << prescale << std::endl;
            }

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

      for(int i = 0; i < nTrgDiscriminators; ++i) trgdiscriminators[i].clear();

      trgprescales->clear();
    }
}

std::pair<int,int> TriggerDumper::counters(std::string path){

  int index = -1;
  for(size_t i = 0; i < selectedTriggers.size(); ++i){
    if(path==selectedTriggers[i]){
      index = i;
      break;
    }
  }
  if(index == -1) return std::pair<int,int>(0,0);

  return std::pair<int,int>(iCountAll[index],iCountPassed[index]);
}

void TriggerDumper::triggerMatch(int id,std::vector<reco::Candidate::LorentzVector> objs){
    for(size_t iobj = 0; iobj < objs.size(); ++iobj){
      for(int i = 0; i < nTrgDiscriminators; ++i){
        bool matchFound = false;

	std::string matchedTrgObject = trgMatchBranches[i];
	size_t len = matchedTrgObject.length();
	size_t pos = matchedTrgObject.find("_TrgMatch_") + 10;
	matchedTrgObject = matchedTrgObject.substr(pos,len-pos);

	if(!isCorrectObject(id,matchedTrgObject)) continue;

	if(patTriggerObjects.isValid()){
	    for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
		patTriggerObject.unpackPathNames(names);
		if(patTriggerObject.id(id)){
		    bool fired = false;
		    std::vector<std::string> pathNamesAll  = patTriggerObject.pathNames(false);
		    std::regex match_re(matchedTrgObject);
		    for(size_t i = 0; i < pathNamesAll.size(); ++i){
			if (std::regex_search(pathNamesAll[i], match_re)) {
			    if(patTriggerObject.hasPathName( pathNamesAll[i], false, true )) fired = true;
			}
		    }
		    if(!fired) continue;

		    double dr = ROOT::Math::VectorUtil::DeltaR(objs[iobj],patTriggerObject.p4());
		    if(dr < trgMatchDr) matchFound = true;
		}
	    }
        }
        trgdiscriminators[i].push_back(matchFound);
      }
    }
}

bool TriggerDumper::isCorrectObject(int id,std::string trgObject){
    std::string sid = "";
    switch (id) {
	case trigger::TriggerTau:
	    sid = "Tau";
	    break;
	case trigger::TriggerMuon:
	    sid = "Mu";
	    break;
	default:
	    std::cout << "Unknown trigger id " << id << " exiting.." << std::endl;
	    exit(1);
    }

    if(trgObject.find(sid) < trgObject.length()) return true;
    return false;
}
