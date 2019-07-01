#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/L1Trigger/interface/L1Candidate.h"

#include <regex>
#include "Math/VectorUtil.h"

TriggerDumper::TriggerDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
  : trgResultsToken(iConsumesCollector.consumes<edm::TriggerResults>(pset.getParameter<edm::InputTag>("TriggerResults"))),
    trgObjectsToken(iConsumesCollector.consumes<pat::TriggerObjectStandAloneCollection>(pset.getParameter<edm::InputTag>("TriggerObjects")))
    //  l1TausToken(iConsumesCollector.consumes<l1t::TauBxCollection>(pset.getParameter<edm::InputTag>("L1TauObjects"))),
    //  l1EtSumToken(iConsumesCollector.consumes<l1t::EtSumBxCollection>(pset.getParameter<edm::InputTag>("L1EtSumObjects")))
    //  trgL1ETMToken(iConsumesCollector.consumes<std::vector<l1extra::L1EtMissParticle>>(pset.getParameter<edm::InputTag>("L1Extra"))) 
{
  inputCollection = pset;
  booked = false;
  bookL1Tau = false;
  bookL1Jet = false;
  bookL1EtSum = false;

  triggerBits = inputCollection.getParameter<std::vector<std::string> >("TriggerBits");
  useFilter = inputCollection.getUntrackedParameter<bool>("filter",false);
  //    iBit = new bool[triggerBits.size()];

  trgMatchStr = inputCollection.getUntrackedParameter<std::vector<std::string> >("TriggerMatch",std::vector<std::string>());
  trgMatchDr = inputCollection.getUntrackedParameter<double>("TriggerMatchDR",0.1);

  if(inputCollection.exists("L1TauObjects")){
    l1TausToken = iConsumesCollector.consumes<l1t::TauBxCollection>(pset.getParameter<edm::InputTag>("L1TauObjects"));
    bookL1Tau = true;
  }

  if(inputCollection.exists("L1JetObjects")){
    l1JetsToken = iConsumesCollector.consumes<l1t::JetBxCollection>(pset.getParameter<edm::InputTag>("L1JetObjects"));
    bookL1Jet = true;
  }

  if(inputCollection.exists("L1EtSumObjects")){
    l1EtSumToken = iConsumesCollector.consumes<l1t::EtSumBxCollection>(pset.getParameter<edm::InputTag>("L1EtSumObjects"));
    bookL1EtSum = true;
  }

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

  if(bookL1EtSum){
    //theTree->Branch("L1MET_l1extra_x",&L1MET_l1extra_x);
    //theTree->Branch("L1MET_l1extra_y",&L1MET_l1extra_y);
    theTree->Branch("L1MET_pat_x",&L1MET_pat_x);
    theTree->Branch("L1MET_pat_y",&L1MET_pat_y);
    theTree->Branch("L1MET_x",&L1MET_x);
    theTree->Branch("L1MET_y",&L1MET_y);
    theTree->Branch("HLTMET_x",&HLTMET_x);
    theTree->Branch("HLTMET_y",&HLTMET_y);
  }
  if(bookL1Tau){
    theTree->Branch("L1Tau_pt",&L1Tau_pt);  
    theTree->Branch("L1Tau_eta",&L1Tau_eta);
    theTree->Branch("L1Tau_phi",&L1Tau_phi);
    theTree->Branch("L1Tau_e",&L1Tau_e);

    theTree->Branch("L1IsoTau_pt",&L1IsoTau_pt);
    theTree->Branch("L1IsoTau_eta",&L1IsoTau_eta);
    theTree->Branch("L1IsoTau_phi",&L1IsoTau_phi);
    theTree->Branch("L1IsoTau_e",&L1IsoTau_e);
  }
  if(bookL1Jet){
    theTree->Branch("L1Jet_pt",&L1Jet_pt);
    theTree->Branch("L1Jet_eta",&L1Jet_eta);
    theTree->Branch("L1Jet_phi",&L1Jet_phi);
    theTree->Branch("L1Jet_e",&L1Jet_e);
  }

  theTree->Branch("HLTTau_pt",&HLTTau_pt);  
  theTree->Branch("HLTTau_eta",&HLTTau_eta);
  theTree->Branch("HLTTau_phi",&HLTTau_phi);
  theTree->Branch("HLTTau_e",&HLTTau_e);

  theTree->Branch("HLTMuon_pt",&HLTMuon_pt);  
  theTree->Branch("HLTMuon_eta",&HLTMuon_eta);
  theTree->Branch("HLTMuon_phi",&HLTMuon_phi);
  theTree->Branch("HLTMuon_e",&HLTMuon_e);

  theTree->Branch("HLTElectron_pt",&HLTElectron_pt);  
  theTree->Branch("HLTElectron_eta",&HLTElectron_eta);
  theTree->Branch("HLTElectron_phi",&HLTElectron_phi);
  theTree->Branch("HLTElectron_e",&HLTElectron_e);

  // theTree->Branch("HLTJet_pt" , &HLTJet_pt);
  // theTree->Branch("HLTJet_eta", &HLTJet_eta); 
  // theTree->Branch("HLTJet_phi", &HLTJet_phi);
  // theTree->Branch("HLTJet_e"  , &HLTJet_e);

  theTree->Branch("HLTBJet_pt" , &HLTBJet_pt);
  theTree->Branch("HLTBJet_eta", &HLTBJet_eta); 
  theTree->Branch("HLTBJet_phi", &HLTBJet_phi);
  theTree->Branch("HLTBJet_e"  , &HLTBJet_e);

  // For-loop: All user-defined trigger names (TriggerBits)  
  for(size_t i = 0; i < triggerBits.size(); ++i){
    selectedTriggers.push_back(triggerBits[i]);
    // Do not find the exact names or versions of HLT path names
    // because they do change in the middle of the run causing buggy behavior
  }

  iBit         = new bool[selectedTriggers.size()];
  iCountAll    = new int[selectedTriggers.size()];
  iCountPassed = new int[selectedTriggers.size()];

  // For-loop: All the selected trigger names (TriggerBits) 
  for(size_t i = 0; i < selectedTriggers.size(); ++i){
    theTree->Branch(std::string(selectedTriggers[i]+"x").c_str(),&iBit[i]);
    iCountAll[i]    = 0;
    iCountPassed[i] = 0;
  }

  // Trigger matching
  std::regex obj_re("((Tau)|(Mu)|(Ele))");
//  std::regex obj_re("((Tau)|(Egamma))");
  for(size_t imatch = 0; imatch < trgMatchStr.size(); ++imatch){
    std::string name = "";
    std::smatch match;
    if (std::regex_search(trgMatchStr[imatch], match, obj_re) && match.size() > 0) name = match.str(0); 
    if(name=="Tau") name = "Taus"; // FIXME, these should come from the config
    if(name=="Mu") name = "Muons"; // FIXME, these should come from the config
    if(name=="Ele") name = "Electrons"; // FIXME, these should come from the config
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
  /*
    edm::Handle<std::vector<l1extra::L1EtMissParticle> > l1etmhandle;
    iEvent.getByToken(trgL1ETMToken, l1etmhandle);
    L1MET_l1extra_x = 0.0;
    L1MET_l1extra_y = 0.0;
    if(l1etmhandle.isValid() && l1etmhandle->size() > 0){
    L1MET_l1extra_x = l1etmhandle.product()->begin()->px();
    L1MET_l1extra_y = l1etmhandle.product()->begin()->py();
    }
  */

  // Get the trigger results
  edm::Handle<edm::TriggerResults> trgResultsHandle;
  iEvent.getByToken(trgResultsToken, trgResultsHandle);

  // Is the trigger results handle valid?
  if(trgResultsHandle.isValid()){
    names = iEvent.triggerNames(*trgResultsHandle);

    // For-loop: All selected triggers (TriggerBits) 
    for(size_t i = 0; i < selectedTriggers.size(); ++i){
      iBit[i] = false;

      // For-loop: All trigger results
      for(size_t j = 0; j < trgResultsHandle->size(); ++j){

	// Search for the selected triggers 
//	std::cout << selectedTriggers[i] << "\n";
	size_t pos = names.triggerName(j).find(selectedTriggers[i]);

	// If a selected trigger is found, set the "fire" bit accordingly
	if (pos == 0 && names.triggerName(j).size() > 0) {
	  iBit[i] = trgResultsHandle->accept(j);
//	  cout << names.triggerName(j)  << ", accept = " << trgResultsHandle->accept(j) << endl;
	  iCountAll[i] += 1;
	  if(trgResultsHandle->accept(j)) iCountPassed[i] += 1;
	  break;
	}

      }//For-loop: All trigger results
    }//For-loop: All selected triggers (TriggerBits) 
    
    std::vector<std::string> trgMatchPaths;
    // For-loop; All triggers for matching (TriggerMatch)
    for(size_t i = 0; i < trgMatchStr.size(); ++i){
      std::regex match_re(trgMatchStr[i]);

      // For-loop: All trigger results    
      for(size_t j = 0; j < trgResultsHandle->size(); ++j){

	if (std::regex_search(names.triggerName(j), match_re)) 
	  {
//	    std::cout << names.triggerName(j) << "\n";
	    trgMatchPaths.push_back(names.triggerName(j));
	  }

      }// For-loop: All trigger results
    } // For-loop: All triggers for matching (TriggerMatch) 


    L1MET_x  = 0;  
    L1MET_y  = 0;
    L1MET_pat_x  = 0;
    L1MET_pat_y  = 0;
    HLTMET_x = 0;
    HLTMET_y = 0;
    // edm::Handle<pat::TriggerObjectStandAloneCollection> patTriggerObjects;
    iEvent.getByToken(trgObjectsToken,patTriggerObjects);
    if(patTriggerObjects.isValid()){

      // For-loop: All PAT TriggerObjectStandAlone objects
      // see: http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_7_6_5/doc/html/db/d75/classpat_1_1TriggerObjectStandAlone.html
      for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
	
	// Unpack trigger names into indices
	patTriggerObject.unpackPathNames(names);
	
	if(patTriggerObject.id(trigger::TriggerL1ETM)){
	  L1MET_pat_x = patTriggerObject.p4().x(); 
	  L1MET_pat_y = patTriggerObject.p4().y();
	  //std::cout << "Trigger L1ETM (pat) " << patTriggerObject.p4().Pt() << std::endl;
	}
	

	// Trigger object is of type MET (see: http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_8_0_27/doc/html/da/d54/namespacetrigger.html)
	if(patTriggerObject.id(trigger::TriggerMET)){
	  HLTMET_x = patTriggerObject.p4().x();
	  HLTMET_y = patTriggerObject.p4().y();
	  //std::cout << "Trigger MET " << patTriggerObject.p4().Pt() << std::endl;
	}//triggerMET
	/*
	  if(patTriggerObject.id(trigger::TriggerL1Tau)){
	  L1Tau_pt.push_back(patTriggerObject.p4().Pt());  
	  L1Tau_eta.push_back(patTriggerObject.p4().Eta());
	  L1Tau_phi.push_back(patTriggerObject.p4().Phi());
	  L1Tau_e.push_back(patTriggerObject.p4().E());
	  //std::cout << "Trigger L1 tau " << patTriggerObject.p4().Pt() << std::endl;
	  }
	*/

	// Trigger object is of type Tau 
	if(patTriggerObject.id(trigger::TriggerTau)){
	  bool fired = false;
	  for(size_t i = 0; i < trgMatchPaths.size(); ++i){
	    if(patTriggerObject.hasPathName( trgMatchPaths[i], false, true )) fired = true;
	  }
	  if(fired){
	    HLTTau_pt.push_back(patTriggerObject.p4().Pt());
	    HLTTau_eta.push_back(patTriggerObject.p4().Eta());
	    HLTTau_phi.push_back(patTriggerObject.p4().Phi());
	    HLTTau_e.push_back(patTriggerObject.p4().E());
	  }
	  //std::cout << "Trigger Tau " << patTriggerObject.p4().Pt() << std::endl;
	}//triggerTau



	////////
	// Trigger object is of type Muon
        if(patTriggerObject.id(trigger::TriggerMuon)){
          bool fired = false;
          for(size_t i = 0; i < trgMatchPaths.size(); ++i){
            if(patTriggerObject.hasPathName( trgMatchPaths[i], true, true )) fired = true;
          }
          if(fired){
            HLTMuon_pt.push_back(patTriggerObject.p4().Pt());
            HLTMuon_eta.push_back(patTriggerObject.p4().Eta());
            HLTMuon_phi.push_back(patTriggerObject.p4().Phi());
            HLTMuon_e.push_back(patTriggerObject.p4().E());
          }
          //std::cout << "Trigger Muon " << patTriggerObject.p4().Pt() << std::endl;
        }//triggerMuon

	////////

        if (patTriggerObject.hasPathName( "HLT_Ele27_eta2p1_WPTight_Gsf_v8", true, true )) {
	  std::cout << "FIRED " << patTriggerObject.hasPathName( "HLT_Ele27_eta2p1_WPTight_Gsf_v8", true, true ) << std::endl;
	  std::cout << "Trigger id: " << std::endl;
	  std::cout << "Mu " << patTriggerObject.id(trigger::TriggerMuon) << std::endl;
          std::cout << "Ele " << patTriggerObject.id(trigger::TriggerElectron) << std::endl;
	  std::cout << "Tau " << patTriggerObject.id(trigger::TriggerTau) << std::endl;
	  std::cout << "Photon " << patTriggerObject.id(trigger::TriggerPhoton) << std::endl;
	  std::cout << "Cluster " << patTriggerObject.id(trigger::TriggerCluster) << std::endl;

	  std::cout << "Trigger paths: " << std::endl;
          for(size_t i = 0; i < patTriggerObject.pathNames().size(); ++i){
            std::cout << patTriggerObject.pathNames()[i] << std::endl;
          }
        }

        ////////
        // Trigger object is of type Electron
        if(patTriggerObject.id(trigger::TriggerElectron) || patTriggerObject.id(trigger::TriggerCluster)){
          bool fired = false;
          for(size_t i = 0; i < trgMatchPaths.size(); ++i){
            if(patTriggerObject.hasPathName( trgMatchPaths[i], true, true )) fired = true;
          }
          if(fired){
            HLTElectron_pt.push_back(patTriggerObject.p4().Pt());
            HLTElectron_eta.push_back(patTriggerObject.p4().Eta());
            HLTElectron_phi.push_back(patTriggerObject.p4().Phi());
            HLTElectron_e.push_back(patTriggerObject.p4().E());
          }
        }//triggerElectron

        ////////

	// // Trigger object is of type Jet
	// if(patTriggerObject.id(trigger::TriggerJet)){
	//   bool fired = false;
	//   
	//   for(size_t i = 0; i < trgMatchPaths.size(); ++i){
	//     
	//     // Get only those jets passing the last filter (PF Jets)
	//     // To see all filters go to https://cmswbm.cern.ch/cmsdb/servlet/RunSummary, 
	//     // insert run number, find the trigger of interest and click on it	    
	//     if(patTriggerObject.hasPathName( trgMatchPaths[i], true, true ))  // fixme: currently no jet passes
	//       {
	// 	fired = true; 
	// 	// cout << "*** trgMatchPaths["<<i<<"] = " << trgMatchPaths[i] << " fired" << endl;
	//       }
	//   }
	//   
	//   if(fired){
	//     // cout << "\ttriggerJet pt , eta, phi, collection = " << patTriggerObject.pt() << " " << patTriggerObject.eta()
	//     // << " " << patTriggerObject.phi() << ", " << patTriggerObject.collection() << endl;
	//     HLTJet_pt.push_back(patTriggerObject.p4().Pt());
	//     HLTJet_eta.push_back(patTriggerObject.p4().Eta());
	//     HLTJet_phi.push_back(patTriggerObject.p4().Phi());
	//     HLTJet_e.push_back(patTriggerObject.p4().E());
	//   }
	// 
	// }//triggerJet


	// Trigger object is of type BJet
	if(patTriggerObject.id(trigger::TriggerBJet)){
	  bool fired = false;
	  for(size_t i = 0; i < trgMatchPaths.size(); ++i){

	    // Get only those bjets passing the last filter (hltPFJetForBtag)
	    // To see all filters go to https://cmswbm.cern.ch/cmsdb/servlet/RunSummary, 
	    // insert run number, find the trigger of interest and click on it	    
	    if(patTriggerObject.hasPathName( trgMatchPaths[i], true, true ))
	      {
		fired = true;
		// cout << "*** trgMatchPaths["<<i<<"] = " << trgMatchPaths[i] << " fired. " << endl;
	      }
	  }

	  if(fired){
	    // cout << "\ttriggerBJet pt , eta, phi, collection = " << patTriggerObject.pt() << " " << patTriggerObject.eta()
		 // << " " << patTriggerObject.phi() << ", " << patTriggerObject.collection() << endl;
	    HLTBJet_pt.push_back(patTriggerObject.p4().Pt());
	    HLTBJet_eta.push_back(patTriggerObject.p4().Eta());
	    HLTBJet_phi.push_back(patTriggerObject.p4().Phi());
	    HLTBJet_e.push_back(patTriggerObject.p4().E());
	  }

	}//triggerBJet
	

      }// for-loop: patTriggerObjetcs

    }// if(patTriggerObjects.isValid()){

    if(bookL1Tau){
      edm::Handle<l1t::TauBxCollection> l1taus;
      iEvent.getByToken(l1TausToken, l1taus);
      if(l1taus.isValid()) {
	for(l1t::TauBxCollection::const_iterator i = l1taus->begin(); i != l1taus->end(); ++i) {
	  L1Tau_pt.push_back(i->pt());
	  L1Tau_eta.push_back(i->eta());
	  L1Tau_phi.push_back(i->phi());
	  L1Tau_e.push_back(i->energy());
	  //std::cout << "Trigger L1 tau (bx) " << i->pt() << std::endl;

	  if(i->hwIso() > 0){
	    L1IsoTau_pt.push_back(i->pt());
	    L1IsoTau_eta.push_back(i->eta());
	    L1IsoTau_phi.push_back(i->phi());
	    L1IsoTau_e.push_back(i->energy());
	    //std::cout << "Trigger L1 IsoTau (bx) " << i->pt() << std::endl;
	  }

	}
      }
    }

    if(bookL1Jet){
      edm::Handle<l1t::JetBxCollection> l1jets;
      iEvent.getByToken(l1JetsToken, l1jets);
      if(l1jets.isValid()) {
	for(l1t::JetBxCollection::const_iterator i = l1jets->begin(); i != l1jets->end(); ++i) {
	  L1Jet_pt.push_back(i->pt());
	  L1Jet_eta.push_back(i->eta());
	  L1Jet_phi.push_back(i->phi());
	  L1Jet_e.push_back(i->energy());
	  //std::cout << "Trigger L1 jet (bx) " << i->pt() << std::endl;
	}
      }
    }

    if(bookL1EtSum){
      edm::Handle<l1t::EtSumBxCollection> l1EtSum;
      iEvent.getByToken(l1EtSumToken, l1EtSum);
      if(l1EtSum.isValid() && l1EtSum.product()->size() > 0){
	for (int ibx = l1EtSum->getFirstBX(); ibx <= l1EtSum->getLastBX(); ++ibx) {
	  for (l1t::EtSumBxCollection::const_iterator it=l1EtSum->begin(ibx); it!=l1EtSum->end(ibx); it++) {
	    int type = static_cast<int>( it->getType() );
	    if(type == l1t::EtSum::EtSumType::kMissingEt) {
	      L1MET_x = it->px();
	      L1MET_y = it->py();
	      //std::cout << "Trigger L1ETM (bx) " << it->et() << std::endl;
	    }
	  }
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
    L1MET_pat_x = 0;
    L1MET_pat_y = 0;
    HLTMET_x = 0;
    HLTMET_y = 0;

    L1Tau_pt.clear(); 
    L1Tau_eta.clear();
    L1Tau_phi.clear();
    L1Tau_e.clear();

    L1IsoTau_pt.clear();
    L1IsoTau_eta.clear();
    L1IsoTau_phi.clear();
    L1IsoTau_e.clear();

    L1Jet_pt.clear();
    L1Jet_eta.clear();
    L1Jet_phi.clear();
    L1Jet_e.clear();

    HLTTau_pt.clear();
    HLTTau_eta.clear();
    HLTTau_phi.clear();
    HLTTau_e.clear();

    HLTMuon_pt.clear();
    HLTMuon_eta.clear();
    HLTMuon_phi.clear();
    HLTMuon_e.clear();

    HLTElectron_pt.clear();
    HLTElectron_eta.clear();
    HLTElectron_phi.clear();
    HLTElectron_e.clear();

    // HLTJet_pt.clear();
    // HLTJet_eta.clear();
    // HLTJet_phi.clear();
    // HLTJet_e.clear();

    HLTBJet_pt.clear();
    HLTBJet_eta.clear();
    HLTBJet_phi.clear();
    HLTBJet_e.clear();

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
//  std::cout << "matching" << "\n";
  for(size_t iobj = 0; iobj < objs.size(); ++iobj){
    for(int i = 0; i < nTrgDiscriminators; ++i){
      bool matchFound = false;

      std::string matchedTrgObject = trgMatchBranches[i];
      size_t len = matchedTrgObject.length();
      size_t pos = matchedTrgObject.find("_TrgMatch_") + 10;
      matchedTrgObject = matchedTrgObject.substr(pos,len-pos);

//      std::cout << id << " " << matchedTrgObject << "\n";

      if(!isCorrectObject(id,matchedTrgObject)) continue;

//      std::cout << "we are soon matching" << "\n";

      if(patTriggerObjects.isValid()){
	for (pat::TriggerObjectStandAlone patTriggerObject : *patTriggerObjects) {
	  patTriggerObject.unpackPathNames(names);
	  if(patTriggerObject.id(id)){
	    bool fired = false;
	    std::vector<std::string> pathNamesAll  = patTriggerObject.pathNames(false);
	    std::regex match_re(matchedTrgObject);
	    for(size_t i = 0; i < pathNamesAll.size(); ++i){
	      if (std::regex_search(pathNamesAll[i], match_re)) {
		if(patTriggerObject.hasPathName( pathNamesAll[i], true, true )) fired = true;
//		if((id == 82 || id==82) && patTriggerObject.hasPathName( pathNamesAll[i], true, true )) fired = true; 
	      }
	    }
	    if(!fired) continue;
//	    std::cout << "we are matching" << "\n";
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
  case trigger::TriggerElectron:
    sid = "Ele";
    break;
  case trigger::TriggerCluster:
    sid = "Ele";
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
