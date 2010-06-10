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
    if (iConfig.exists("CutMinNJets")) {
      fCutMinNJets = iConfig.getParameter<double>("CutMinNJets");
    } else {
      throw cms::Exception("Configuration") << "JetSelection: int value 'CutMinNJets' is missing in config!" << std::endl;
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
    fCounterError = fCounter->addCounter("Random Errors");

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
    std::vector<reco::CaloJet> myFilteredJets;

    for (size_t i = 0; i < myJetCount; ++i) {
      const reco::CaloJet & myJet = (*myCaloJets)[i];
      myUnsortedJets.push_back(myJet);
    }
    
    // Loop over JetCollection
    for (std::vector<reco::CaloJet>::const_iterator iJet = myUnsortedJets.begin(); iJet != myUnsortedJets.end(); iJet++) {
      
      // Reference counter. Count total number of jets prior any selection in each Event.
      fCounter->addCount(fCounterJetsPriorSelection);
      
    }

    const size_t myUnsortedJetsSize = myUnsortedJets.size();
    // Call a function to take an unsorted caloJet vector and sort it according to caloJet-Energies
    if(myUnsortedJetsSize!=0){mySortedJets = sortCaloJets(myUnsortedJets, myUnsortedJetsSize);}
    const size_t mySortJetsSize = mySortedJets.size();
    if(mySortJetsSize==myUnsortedJetsSize){
      // Call filtering function
      myFilteredJets = filterCaloJets(mySortedJets, mySortJetsSize);
    }
    else{
      edm::LogInfo("HPlus") << "Jet handle is empty!" << std::endl;
      fCounter->addCount(fCounterError);
    }
    
    const size_t myFilteredJetsSize = myFilteredJets.size();
    if(myFilteredJetsSize!=0){
      std::vector<reco::CaloJet>::const_iterator iFilteredJet;
      std::cout << "*** myFilteredJetsSize != 0 ***" << std::endl;
      for(iFilteredJet =  myFilteredJets.begin(); iFilteredJet != myFilteredJets.end(); iFilteredJet++){
	// Count total number of jets prio any selection in each Event.
      fCounter->addCount(fCounterJetsPostSelection);
      std::cout << "(*iFilteredJet).energy()= " << (*iFilteredJet).energy() << std::endl;
      }
    }
    else{ std::cout << "*** WARNING:  myFilteredJetsSize == 0 ***" << std::endl; }
    
    return decision;
    
  }//eof:  HPlusJetSelection::analyze()
  
  std::vector<reco::CaloJet> HPlusJetSelection::sortCaloJets(std::vector<reco::CaloJet> caloJetsToSort, const size_t caloJetSize) {
    
    // Declare variables
    reco::CaloJet myTmpLdgJet;
    reco::CaloJet myTmpLdgJet_new;
    std::vector<reco::CaloJet> caloJetsSorted;
    std::vector<reco::CaloJet>::iterator myJet;
    
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
    // for ( myJet = caloJetsSorted.begin(); myJet != caloJetsSorted.end(); ++myJet) {
    //   std::cout << "(*myJetSorted).energy() = " << (*myJet).energy() << std::endl;
    // }

    return caloJetsSorted;
    
  }//eof: HPlusJetSelection::sortCaloJets()

  std::vector<reco::CaloJet> HPlusJetSelection::filterCaloJets(std::vector<reco::CaloJet> caloJetsSorted, const size_t caloJetSize) {
    
    // Declare variables
    reco::CaloJet myJet;
    std::vector<reco::CaloJet> caloJetsFiltered;
    std::vector<reco::CaloJet>::iterator it_caloJetsFiltered;
    bool passedNJets      = false;
    bool passedJetEt      = false;
    bool passedJetEta     = false;
    bool passedEMFraction = false;  
    int counter = 0;
    
    if(caloJetSize >=fCutMinNJets){
    
      std::cout << "---> Looping over filtered jets <--- " << std::endl;
      // Loop over sorted Jets and apply quality cuts
      for( it_caloJetsFiltered = caloJetsSorted.begin(); it_caloJetsFiltered != caloJetsSorted.end(); ++it_caloJetsFiltered) {
	
	if( (*it_caloJetsFiltered).energy() >= fCutMinJetEt){ passedJetEt = true;}
	if( fabs((*it_caloJetsFiltered).eta()) <= fCutMaxAbsJetEta){ passedJetEta = true;}
	if( (*it_caloJetsFiltered).emEnergyFraction() >= fCutMaxEMFraction ){ passedEMFraction = true;}
	//  std::cout << "(*it_caloJetsFiltered).energy() = " << (*it_caloJetsFiltered).energy() << std::endl;
	//  std::cout << "(*it_caloJetsFiltered).eta() = " << (*it_caloJetsFiltered).eta() << std::endl;
	//  std::cout << "(*it_caloJetsFiltered).emEnergyFraction() = " << (*it_caloJetsFiltered).emEnergyFraction() << std::endl;
	// Boolean will be used to erase those jets that do not satisfy criteria
	bool jetSurvives = ( passedJetEt && passedJetEta && passedEMFraction) ;
	if(!jetSurvives){ 
	  std::cout << "Jet did not survive " << std::endl;
	caloJetsSorted.erase(caloJetsSorted.begin()+counter);
	} // FIXME
	else{caloJetsFiltered.push_back(*it_caloJetsFiltered);}
					
	counter++;
      }
      
      const double myFilteredJetsSize = caloJetsFiltered.size();
      if( myFilteredJetsSize >= fCutMinNJets  ){ passedNJets = true;}
    }
    else{
      std::cout << "*** WARNING: caloJetSize < fCutMinNJets ***" << std::endl;
    }
    

    // To do's
    // 1) Save to edm ntuple: 
    //    a) the jets after selection
    //    b) the number of jets left after selection criteria, 
    //    c) Validation histograms including Jet Et, Eta of: "leading-Jet", "2nd-Jet", "3rd-Jet", "4th-Jet".
    //    d) Informative counters
    // 2) Return boolean decision if Event satisfies "jet-selection criteria", i.e. At least N jets are left after the steps 1) -> 4)
    
      return caloJetsFiltered;
    
  }//eof: HPlusJetSelection::filterCaloJets


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
  }//eof: HPlusJetSelection::eraseVectorElement(
  
  /////////
  DEFINE_FWK_MODULE(HPlusJetSelection); 
  
}//eof: namespace HPlusAnalysis {


