#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusJetSelection.h"

#include <iostream>
#include <string>
#include <vector>

#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/EgammaCandidates/interface/ElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/Electron.h"

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include "DataFormats/Common/interface/Handle.h"
#include <vector>
#include <algorithm>

namespace HPlusAnalysis {
  
  HPlusJetSelection::HPlusJetSelection(const edm::ParameterSet& iConfig) : 
    HPlusAnalysis::HPlusAnalysisBase("JetSelection"),
    HPlusAnalysis::HPlusSelectionBase(iConfig) {
    // Parse the list of triggers in the config file
    if (iConfig.exists("JetCollectionName")) {
      fJetCollectionName = iConfig.getParameter<edm::InputTag>("JetCollectionName");
    } else {
      throw cms::Exception("Configuration") << "JetSelection: InputTag 'JetCollectionName' is missing in config!" << std::endl;
    }
    
    if (iConfig.exists("CutMinJetEt")) {
      fCutMinJetEt = iConfig.getParameter<double>("CutMinJetEt");
    } else {
      throw cms::Exception("Configuration") << "JetSelection: double value 'CutMinJetEt' is missing in config!" << std::endl;
    }
    if (iConfig.exists("CutMinJetEt")) {
      fCutMinJetEt = iConfig.getParameter<double>("CutMinJetEt");
    } else {
      throw cms::Exception("Configuration") << "JetSelection: double value 'CutMinJetEt' is missing in config!" << std::endl;
    }
    if (iConfig.exists("CutMaxAbsJetEta")) {
      fCutMaxAbsJetEta = iConfig.getParameter<double>("CutMaxAbsJetEta");
    } else {
      throw cms::Exception("Configuration") << "JetSelection: double value 'CutMaxAbsJetEta' is missing in config!" << std::endl;
    }
    if (iConfig.exists("CutMaxEMFraction")) {
      fCutMaxEMFraction = iConfig.getParameter<double>("CutMaxEMFraction");
    } else {
      throw cms::Exception("Configuration") << "JetSelection: double value 'CutMaxEMFraction' is missing in config!" << std::endl;
    }
    // Initialize counters
    fCounterTest = fCounter->addCounter("TestCounter");
    fCounterJetsPriorSelection = fCounter->addCounter("All Jets");
    fCounterJetsPostSelection  = fCounter->addCounter("Selected Jets");
    fCounterJetCollectionHandleEmpty = fCounter->addCounter("Empty Jet Handle");
    
    std::string alias;
    // Declare produced items (class-specific):  Max Jet Et 
    produces<float>(alias = "JetSelectionMaxJetEt").setBranchAlias(alias);
  
  } //eof: HPlusAnalysis::HPlusSelectionBase(iConfig) {

  HPlusJetSelection::~HPlusJetSelection() {}
  
  void HPlusJetSelection::beginJob() {
    // Set histograms
    if (isHistogrammed()) {
      hLeadJetMaxEt = fFileService->make<TH1F>("LdgJetEt", "LdgJet Highest E_{T}",  100, 0., 200.);
    }
  }
  
  void HPlusJetSelection::endJob() {
    // Reset of variables?
    
  }
  
  bool HPlusJetSelection::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    
    bool decision = false; // filter decision true iff at least NJets survive the selection criteria.
    fCounter->addCount(fCounterTest);
    
    // ************************************************************************************************
    // FIXME: Do this for ALL data to be stored
    // std::auto_ptr<float> myHighestJetEt(new float); // highest pt of jet that has passed all criteria
    // ************************************************************************************************
    
    // Get JetCollection handle
    edm::Handle<reco::CaloJetCollection> myCaloJets;       // create an empty handle 
    iEvent.getByLabel(fJetCollectionName, myCaloJets);     // attach handle to JetCollection
    if (!myCaloJets->size()) {
      edm::LogInfo("HPlus") << "Jet handle is empty!" << std::endl;
      fCounter->addCount(fCounterJetCollectionHandleEmpty);
    return decision;
    }
    const size_t myJetCount = myCaloJets->size();
    
    // Initialisation of variables (move to header)
    std::vector<reco::CaloJet> myUnsortedJets;
    std::vector<reco::CaloJet> mySortedJets;

    for (size_t i = 0; i < myJetCount; ++i) {
      const reco::CaloJet & myJet = (*myCaloJets)[i];
      myUnsortedJets.push_back(myJet);
    }
    
    // Loop over JetCollection
    for (std::vector<reco::CaloJet>::const_iterator iJet = myUnsortedJets.begin(); iJet != myUnsortedJets.end(); iJet++) {
      
      // Reference counter. Count total number of jets prior any selection in each Event.
      fCounter->addCount(fCounterJetsPriorSelection);
     
      // Count total number of jets prio any selection in each Event.
      fCounter->addCount(fCounterJetsPostSelection);
    }

    const size_t myUnsortedJetsSize = myUnsortedJets.size();
    std::cout << "myUnsortedJetsSize = " << myUnsortedJetsSize << std::endl;	      
    if(myUnsortedJetsSize!=0){sortCaloJets(myUnsortedJets, myUnsortedJetsSize);}
    
    // Re-set variables
    //delete myUnsortedJets;
    
    // End of function, return boolean
    return decision;
  }

  void HPlusJetSelection::sortCaloJets(std::vector<reco::CaloJet> caloJetsToSort, const size_t caloJetSize) {
    
    std::cout << "\n***** HPlusJetSelection::sortCaloJets(...) ***** " << std::endl;
    
    // Declare variables
    reco::CaloJet myTmpLdgJet;
    reco::CaloJet myTmpLdgJet_new;
    std::vector<reco::CaloJet> caloJetsSorted;
    std::vector<reco::CaloJet>::iterator myJet;
    std::vector<reco::CaloJet>::iterator myJetSorted;
    
    // Store the "first" N jets [wrt energy). 
    for ( size_t i = 0; i < caloJetSize; i++) {
      for ( myJet = caloJetsToSort.begin(); myJet != caloJetsToSort.end(); ++myJet) {
	
	if( (*myJet).energy() > myTmpLdgJet.energy() ){
	  myTmpLdgJet = (*myJet);

	}
	else{}
      }
      // Store myJet as ith-LdgJet (descending order in Energy)
      caloJetsSorted.push_back(myTmpLdgJet);
      // Delete myJet from vector list
      caloJetsToSort = eraseVectorElement(caloJetsToSort, myTmpLdgJet);
      myTmpLdgJet = myTmpLdgJet_new;
    }//eof: for ( size_t i = 0; i < caloJetsToSort.size(); i++) {
    
    // Cout the sorted jet energies
    for ( myJetSorted = caloJetsSorted.begin(); myJetSorted != caloJetsSorted.end(); ++myJetSorted) {
      std::cout << "(*myJetSorted).energy() = " << (*myJetSorted).energy() << std::endl;
    }
    
  }

  
  std::vector<reco::CaloJet> HPlusJetSelection::eraseVectorElement( std::vector<reco::CaloJet> myJetVector, reco::CaloJet test) {

    std::vector<reco::CaloJet>::iterator it;
    int counter = 0;
    //  bool success = false;

    for ( it = myJetVector.begin(); it!=myJetVector.end(); ++it) {

      if( (*it).energy() == test.energy() ){
	
	// std::cout << " Found match. Deleting vector with (*it).energy() = " << (*it).energy()  << std::endl;
	myJetVector.erase(myJetVector.begin()+counter);
	//	success = true;
	break;
      } else{counter++;}
    }

      return myJetVector;
    }
  

//   void HPlusJetSelection::eraseVectorElement(std::vector<reco::CaloJet> myVector, int member){

//     std::vector<reco::CaloJet>::const_iterator f = find(myVector.begin(), myVector.end(), member);
//     if( f != myVector.end() ){myVector.erase(f);}
//   }
  
  /////////
  DEFINE_FWK_MODULE(HPlusJetSelection); 
  
}//eof: namespace HPlusAnalysis {


