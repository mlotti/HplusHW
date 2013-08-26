#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusJetSelection.h"

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/EgammaCandidates/interface/ElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/Electron.h"

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/Vector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/deltaR.h"

namespace HPlusAnalysis {
  
  HPlusJetSelection::HPlusJetSelection(const edm::ParameterSet& iConfig) : HPlusAnalysis::HPlusAnalysisBase("JetSelection"), HPlusAnalysis::HPlusSelectionBase(iConfig) {
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

    // Initialise booleans
    useCaloJets = false;
    useJPTJets  = false;
    decision    = false;    
    
    // See which jet collection was selected for analysing...
    if( (fJetCollectionName.label()).compare("ak5CaloJets") == 0){ 
      std::cout << "\n*** HPlusJetSelection::HPlusJetSelection() *** Have chosen to run on Jet-Collection \"ak5CaloJets\".\n"  << std::endl;
      useCaloJets = true;
    }
    else if(fJetCollectionName.label().compare("JetPlusTrackZSPCorJetAntiKt5") == 0){ 
      std::cout << "\n*** HPlusJetSelection::HPlusJetSelection() *** Have chosen to run on Jet-Collection \"JetPlusTrackZSPCorJetAntiKt5\".\n" << std::endl;
      useJPTJets = true;
    }
    else{ 
      std::cout << "\n*** HPlusJetSelection::HPlusJetSelection() *** ERROR: No Jet-Collection exists with the name \"" << fJetCollectionName.label() << "\"! Please select either a \"reco::caloJet\" or a \"reco::JPTJet\" collection."<< std::endl;
      fCounter->addCount(fCounterError);
    }
    
    // Initialize counters
    fCounterNEvts = fCounter->addCounter("Total #Evts (before selection)");
    fCounterNEvtsPassedSelection = fCounter->addCounter("Total #Evts (after selection)");
    fCounterJetsPriorSelection = fCounter->addCounter("#Jets (prior selection)");
    fCounterJetsPostSelection  = fCounter->addCounter("#Jets (after selection)");
    fCounterJetCollectionHandleEmpty = fCounter->addCounter("#Evts with Empty Jet Handle");
    fCounterError = fCounter->addCounter("Errors and Warnings");

    // Declare produced items (class-specific): 
    std::string alias;
    if(useCaloJets){    
      produces< std::vector<reco::CaloJet> >(alias = "LdgJet").setBranchAlias(alias);
      produces< std::vector<reco::CaloJet> >(alias = "SecondLdgJet").setBranchAlias(alias);
      produces< std::vector<reco::CaloJet> >(alias = "ThirdLdgJet").setBranchAlias(alias);
      produces< std::vector<reco::CaloJet> >(alias = "FourthLdgJet").setBranchAlias(alias);
      // produces< std::vector<reco::CaloJet> >(alias = "FifthLdgJet").setBranchAlias(alias);
      // produces< std::vector<std::vector<reco::CaloJet> > >(alias = "CaloJets").setBranchAlias(alias);
    }
    if(useJPTJets){
      produces< std::vector<reco::JPTJet> >(alias = "LdgJet").setBranchAlias(alias);
      produces< std::vector<reco::JPTJet> >(alias = "SecondLdgJet").setBranchAlias(alias);
      produces< std::vector<reco::JPTJet> >(alias = "ThirdLdgJet").setBranchAlias(alias);
      produces< std::vector<reco::JPTJet> >(alias = "FourthLdgJet").setBranchAlias(alias);
      // produces< std::vector<reco::JPTJet> >(alias = "FifthLdgJet").setBranchAlias(alias);
      // produces< std::vector<std::vector<reco::JPTJet> > >(alias = "JPTJets").setBranchAlias(alias);
    }
  
  } //eof: HPlusAnalysis::HPlusSelectionBase(iConfig) {

  HPlusJetSelection::~HPlusJetSelection() {}
  
  void HPlusJetSelection::beginJob() {
    // Set histograms
    if (isHistogrammed()) {
      // myHisto =  fs->make<TH1D>(tName, tName, nBins, min, max ); // (const char*, const char*, Int_t, Float_t, Float_t)
      hLdgJetEt       = fFileService->make<TH1F>("LdgJetEt", "LdgJet  E_{T}",  202, -1.5, 200.5);// LdgJet Et 
      hSecondLdgJetEt = fFileService->make<TH1F>("SecondLdgJetEt", "2nd LdgJet  E_{T}",  202, -1.5, 200.5);
      hThirdLdgJetEt  = fFileService->make<TH1F>("ThirdLdgJetEt", "3rd LdgJet  E_{T}",  202, -1.5, 200.5);
      hFourthLdgJetEt = fFileService->make<TH1F>("FourthLdgJetEt", "4th LdgJet  E_{T}",  202, -1.5, 200.5);
      // hFifthLdgJetE = fFileService->make<TH1F>("FifthLdgJetEt", "5th LdgJet  E_{T}",  202, -1.5, 200.5);
      //
      hLdgJetEta       = fFileService->make<TH1F>("LdgJetEta", "LdgJet  E_{T}",  30, -3., 3.);// LdgJet Eta
      hSecondLdgJetEta = fFileService->make<TH1F>("SecondLdgJetEta", "2nd LdgJet  E_{T}",  30, -3., 3.);
      hThirdLdgJetEta  = fFileService->make<TH1F>("ThirdLdgJetEta", "3rd LdgJet  E_{T}",  30, -3., 3.);
      hFourthLdgJetEta = fFileService->make<TH1F>("FourthLdgJetEta", "4th LdgJet  E_{T}",  30, -3., 3.);
      // hFifthLdgJetEta = fFileService->make<TH1F>("FifthLdgJetEta", "5th LdgJet  E_{T}",  30, -3., 3.);
    }

  }
  
  void HPlusJetSelection::endJob() {
  }
  
  bool HPlusJetSelection::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // std::cout << "\n*** HPlusJetSelection::filter() *** The boolean useJPTJets = " <<  useJPTJets <<  "\n"  << std::endl; // deleteMe    
    
    // Use booleans to determine which functions to call (Collection-Dependent)
    if(useCaloJets){decision = doCaloJets(iEvent, iSetup);}
    else if(useJPTJets){decision = doJPTJets(iEvent, iSetup);}
    else{  
      std::cout << "ERROR: No jet-collection exists with the name \""<< fJetCollectionName.label() << "\"! Please select either a \"reco::caloJet\" or a \"reco::JPTJet\" collection."<< std::endl;
    }
    
    return decision;
    
  }//eof: HPlusJetSelection::filter()
  
  // CALOJETS
  bool HPlusJetSelection::doCaloJets(edm::Event& iEvent, const edm::EventSetup& iSetup){
    // The filter decision is true iff at least NJets survive the selection criteria (on Et, Eta, EMFraction)
    bool jetsPassCriteria = false; 
    
    // JetSelection specific variables
    std::auto_ptr< std::vector<reco::CaloJet> > myDataLdgJet(new std::vector<reco::CaloJet>);       // highest Et jet passing criteria
    std::auto_ptr< std::vector<reco::CaloJet> > myDataSecondLdgJet(new std::vector<reco::CaloJet>); // 2nd highest Et jet passing criteria
    std::auto_ptr< std::vector<reco::CaloJet> > myDataThirdLdgJet(new std::vector<reco::CaloJet>);  // 3rd highest Et jet passing criteria
    std::auto_ptr< std::vector<reco::CaloJet> > myDataFourthLdgJet(new std::vector<reco::CaloJet>); // 4th highest Et jet passing criteria
    // std::auto_ptr< std::vector<reco::CaloJet> > myDataFifthLdgJet(new std::vector<reco::CaloJet>); // 5th highest Et jet passing criteria
    // std::auto_ptr< std::vector<std::vector<reco::CaloJet> > >myDataCaloJets(new std::vector<std::vector<reco::CaloJet> >); // FIXME?
    
    // Get JetCollection handle
    edm::Handle<reco::CaloJetCollection> myCaloJets;       // create an empty handle 
    iEvent.getByLabel(fJetCollectionName, myCaloJets);     // attach handle to JetCollection
    if (!myCaloJets->size()) {
      edm::LogInfo("HPlus") << "*** WARNING: Jet handle is empty! ***" << std::endl;
      fCounter->addCount(fCounterJetCollectionHandleEmpty);
      return jetsPassCriteria;
    }else{fCounter->addCount(fCounterNEvts);}
      
    // Get the number of CaloJets present in the Evt
    const size_t myJetCount = myCaloJets->size();
    
    // Initialisation of variables (move to header)
    std::vector<reco::CaloJet> myUnsortedJets;
    std::vector<reco::CaloJet> mySortedJets;
    std::vector<reco::CaloJet> myFilteredJets;
    std::vector<reco::CaloJet> myEmptyJets;
    
    // Step 1) Store all jets in a vector
    // **********************************
    for (size_t i = 0; i < myJetCount; ++i) {
      const reco::CaloJet & myCaloJet = (*myCaloJets)[i];
      myUnsortedJets.push_back(myCaloJet);
      fCounter->addCount(fCounterJetsPriorSelection);
    }
    
    // Step 2) Order Jets according to Jet Energy
    // ******************************************
    const size_t myUnsortedJetsSize = myUnsortedJets.size();
    // Call a function to take an unsorted caloJet vector and sort it according to caloJet-Energies
    if(myUnsortedJetsSize!=0){mySortedJets = sortCaloJets(myUnsortedJets, myUnsortedJetsSize);}
    const size_t mySortJetsSize = mySortedJets.size();
    
    // Step 3) Filter the now ordered Jets: Apply Jet Et, Eta and EMFraction Cuts
    // **************************************************************************
    if(mySortJetsSize == myUnsortedJetsSize){ myFilteredJets = filterCaloJets(mySortedJets, mySortJetsSize); }
    else{
      edm::LogInfo("HPlus") << "WARNING! The number of sorted jets is NOT the same as the number of un-sorted jets!!! Filling filteredJets vector with empty vector..." << std::endl;
      fCounter->addCount(fCounterError);
      myFilteredJets = myEmptyJets; // something went wrong => pass "myfilteredJets" vector as an empty vector
    }
    
    // Step 4) Last criterion: Is the number of jets enough? 
    // *****************************************************
    const size_t myFilteredJetsSize = myFilteredJets.size();
    if( myFilteredJetsSize >= fCutMinNJets ){ jetsPassCriteria = true;}
    
    // Step 5) Save variables to ntuple 
    // *********************************
    // myDataCaloJets->push_back(myFilteredJets); // FIXME?
    
    if(myFilteredJetsSize!=0){
      // Loop over all the filtered jets
      for(std::vector<reco::CaloJet>::const_iterator iFilteredJet =  myFilteredJets.begin(); iFilteredJet != myFilteredJets.end(); iFilteredJet++){	
	fCounter->addCount(fCounterJetsPostSelection);
      }
      if(jetsPassCriteria){
	// Keep the 4 leading jets momenta.
	myDataLdgJet->push_back( myFilteredJets.at(0));
	myDataSecondLdgJet->push_back( myFilteredJets.at(1)); 
 	myDataThirdLdgJet->push_back( myFilteredJets.at(2));
 	myDataFourthLdgJet->push_back( myFilteredJets.at(3));
	// myDataFifthLdgJet->push_back( myFilteredJets.at(4));

	// Step 6) Fill some validation histograms
	// ***************************************
	hLdgJetEt->Fill(myFilteredJets.at(0).et()); // LdgJet Energy
	hSecondLdgJetEt->Fill(myFilteredJets.at(1).et());
	hThirdLdgJetEt->Fill(myFilteredJets.at(2).et());
	hFourthLdgJetEt->Fill(myFilteredJets.at(3).et());
	// hFifthLdgJetEt->Fill(myFilteredJets.at(4).et());
	hLdgJetEta->Fill(myFilteredJets.at(0).eta()); // LdgJet Eta
	hSecondLdgJetEta->Fill(myFilteredJets.at(1).eta());
	hThirdLdgJetEta->Fill(myFilteredJets.at(2).eta());
	hFourthLdgJetEta->Fill(myFilteredJets.at(3).eta());
	// hFifthLdgJetEta->Fill(myFilteredJets.at(4).eta());
      } else{
	// Fill with empty vector
	reco::CaloJet myEmptyCaloJet;
	myDataLdgJet->push_back( myEmptyCaloJet );
	myDataSecondLdgJet->push_back( myEmptyCaloJet ); 
	myDataThirdLdgJet->push_back( myEmptyCaloJet );
 	myDataFourthLdgJet->push_back( myEmptyCaloJet );
	// myDataFifthLdgJet->push_back( myEmptyCaloJet);
      }
    } else{ 
      // Fill histos with "error-values"
      hLdgJetEt->Fill(-1.0);
      hSecondLdgJetEt->Fill(-1.0);
      hThirdLdgJetEt->Fill(-1.0);
      hFourthLdgJetEt->Fill(-1.0);
      // hFifthLdgJetEt->Fill(-1.0);
      hLdgJetEta->Fill(-999.0);
      hSecondLdgJetEta->Fill(-999.0);
      hThirdLdgJetEta->Fill(-999.0);
      hFourthLdgJetEta->Fill(-999.0);
      // hFifthLdgJetEta->Fill(-999.0);
    }
    
    // Step 7) Put event data
    // **********************
    iEvent.put(myDataLdgJet, "LdgJet");
    iEvent.put(myDataSecondLdgJet, "SecondLdgJet");
    iEvent.put(myDataThirdLdgJet, "ThirdLdgJet");
    iEvent.put(myDataFourthLdgJet, "FourthLdgJet");
    // iEvent.put(myDataFifthLdgJet, "FifthLdgJet");
    // iEvent.put(myDataCaloJets, "CaloJets"); // likely to cause problems: different number of entries than rest of vectors 
    
    // Keep track of how many Evts the jet selection cuts were satisfied
    if(jetsPassCriteria){fCounter->addCount(fCounterNEvtsPassedSelection);}
    
    // Return true if "fCutMinNJets" Jets satisfy the cuts on Jet Et, Jet Eta and Jet EMFraction.
    return jetsPassCriteria;

  }//eof:  HPlusJetSelection::doCaloJets()

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
	} else{}
      }
      // Store myJet as ith-LdgJet (descending order in Energy)
      caloJetsSorted.push_back(myTmpLdgJet);
      // Delete myJet from vector list
      caloJetsToSort = eraseVectorElement(caloJetsToSort, myTmpLdgJet);
      myTmpLdgJet = myTmpLdgJet_new;
    }//eof: for ( size_t i = 0; i < caloJetsToSort.size(); i++) {

    return caloJetsSorted;
    
  }//eof: HPlusJetSelection::sortCaloJets()          

  std::vector<reco::CaloJet> HPlusJetSelection::filterCaloJets(std::vector<reco::CaloJet> caloJetsSorted, const size_t caloJetSize) {
    // Declare variables
    std::vector<reco::CaloJet> caloJetsFiltered;
    std::vector<reco::CaloJet>::iterator it_caloJetsFilteredCands;
    std::vector<reco::CaloJet>::iterator it_caloJetsFiltered;
    bool passedJetEt      = false;
    bool passedJetEta     = false;
    bool passedEMFraction = false;  
    bool jetSurvives = false;   
    
    if(caloJetSize >= fCutMinNJets){
      
      // Loop over sorted Jets and apply quality cuts
      for( it_caloJetsFilteredCands = caloJetsSorted.begin(); it_caloJetsFilteredCands != caloJetsSorted.end(); ++it_caloJetsFilteredCands) {
	passedJetEt      = false;
	passedJetEta     = false;
	passedEMFraction = false;
	if( (*it_caloJetsFilteredCands).et() >= fCutMinJetEt){ passedJetEt = true;}
	if( fabs((*it_caloJetsFilteredCands).eta()) <= fCutMaxAbsJetEta){ passedJetEta = true;}
	if( (*it_caloJetsFilteredCands).emEnergyFraction() <= fCutMaxEMFraction ){ passedEMFraction = true;}
	
	// Boolean will be used to erase those jets that do not satisfy criteria
	jetSurvives = ( passedJetEt && passedJetEta && passedEMFraction) ;
	if(jetSurvives){ 
	  caloJetsFiltered.push_back(*it_caloJetsFilteredCands);
	} 
	else{ 
	  // std::cout << "Jet did not survive " << std::endl;  
	}
      }
    }
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
	// success = true;
	break;
      } else{counter++;}
    }
    
    return myJetVector;
    
  }//eof: HPlusJetSelection::eraseVectorElement()



  // JPTJETS
  bool HPlusJetSelection::doJPTJets(edm::Event& iEvent, const edm::EventSetup& iSetup){

    // The filter decision is true iff at least NJets survive the selection criteria (on Et, Eta, EMFraction)
    bool jetsPassCriteria = false; 
    
    // JetSelection specific variables
    std::auto_ptr< std::vector<reco::JPTJet> > myDataLdgJet(new std::vector<reco::JPTJet>);       // highest Et jet passing criteria
    std::auto_ptr< std::vector<reco::JPTJet> > myDataSecondLdgJet(new std::vector<reco::JPTJet>); // 2nd highest Et jet passing criteria
    std::auto_ptr< std::vector<reco::JPTJet> > myDataThirdLdgJet(new std::vector<reco::JPTJet>);  // 3rd highest Et jet passing criteria
    std::auto_ptr< std::vector<reco::JPTJet> > myDataFourthLdgJet(new std::vector<reco::JPTJet>); // 4th highest Et jet passing criteria
    // std::auto_ptr< std::vector<reco::JPTJet> > myDataFifthLdgJet(new std::vector<reco::JPTJet>); // 5th highest Et jet passing criteria
    // std::auto_ptr< std::vector<std::vector<reco::JPTJet> > >myDataJPTJets(new std::vector<std::vector<reco::JPTJet> >); // FIXME?
    
    // Get JetCollection handle
    edm::Handle<reco::JPTJetCollection> myJPTJets;       // create an empty handle 
    iEvent.getByLabel(fJetCollectionName, myJPTJets);     // attach handle to JetCollection
    if (!myJPTJets->size()) {
      edm::LogInfo("HPlus") << "*** WARNING: Jet handle is empty! ***" << std::endl;
      fCounter->addCount(fCounterJetCollectionHandleEmpty);
      return jetsPassCriteria;
    }else{fCounter->addCount(fCounterNEvts);}
      
    // Get the number of JPTJets present in the Evt
    const size_t myJetCount = myJPTJets->size();
    
    // Initialisation of variables (move to header)
    std::vector<reco::JPTJet> myUnsortedJets;
    std::vector<reco::JPTJet> mySortedJets;
    std::vector<reco::JPTJet> myFilteredJets;
    std::vector<reco::JPTJet> myEmptyJets;
    
    // Step 1) Store all jets in a vector
    // **********************************
    for (size_t i = 0; i < myJetCount; ++i) {
      const reco::JPTJet & myJPTJet = (*myJPTJets)[i];
      myUnsortedJets.push_back(myJPTJet);
      fCounter->addCount(fCounterJetsPriorSelection);
    }
    
    // Step 2) Order Jets according to Jet Energy
    // ******************************************
    const size_t myUnsortedJetsSize = myUnsortedJets.size();
    // Call a function to take an unsorted caloJet vector and sort it according to caloJet-Energies
    if(myUnsortedJetsSize!=0){mySortedJets = sortJPTJets(myUnsortedJets, myUnsortedJetsSize);}
    const size_t mySortJetsSize = mySortedJets.size();
    
    // Step 3) Filter the now ordered Jets: Apply Jet Et, Eta and EMFraction Cuts
    // **************************************************************************
    if(mySortJetsSize == myUnsortedJetsSize){ myFilteredJets = filterJPTJets(mySortedJets, mySortJetsSize); }
    else{
      edm::LogInfo("HPlus") << "WARNING! The number of sorted jets is NOT the same as the number of un-sorted jets!!! Filling filteredJets vector with empty vector..." << std::endl;
      fCounter->addCount(fCounterError);
      myFilteredJets = myEmptyJets; // something went wrong => pass "myfilteredJets" vector as an empty vector
    }
    
    // Step 4) Last criterion: Is the number of jets enough? 
    // *****************************************************
    const size_t myFilteredJetsSize = myFilteredJets.size();
    if( myFilteredJetsSize >= fCutMinNJets ){ jetsPassCriteria = true;}
    
    // Step 5) Save variables to ntuple 
    // *********************************
    // myDataJPTJets->push_back(myFilteredJets); // FIXME?
    
    if(myFilteredJetsSize!=0){
      // Loop over all the filtered jets
      for(std::vector<reco::JPTJet>::const_iterator iFilteredJet =  myFilteredJets.begin(); iFilteredJet != myFilteredJets.end(); iFilteredJet++){	
	fCounter->addCount(fCounterJetsPostSelection);
      }
      if(jetsPassCriteria){
	// Keep the 4 leading jets momenta.
	myDataLdgJet->push_back( myFilteredJets.at(0));
	myDataSecondLdgJet->push_back( myFilteredJets.at(1)); 
 	myDataThirdLdgJet->push_back( myFilteredJets.at(2));
 	myDataFourthLdgJet->push_back( myFilteredJets.at(3));
	// myDataFifthLdgJet->push_back( myFilteredJets.at(4));

	// Step 6) Fill some validation histograms
	// ***************************************
	hLdgJetEt->Fill(myFilteredJets.at(0).et()); // LdgJet Energy
	hSecondLdgJetEt->Fill(myFilteredJets.at(1).et());
	hThirdLdgJetEt->Fill(myFilteredJets.at(2).et());
	hFourthLdgJetEt->Fill(myFilteredJets.at(3).et());
	// hFifthLdgJetEt->Fill(myFilteredJets.at(4).et());
	hLdgJetEta->Fill(myFilteredJets.at(0).eta()); // LdgJet Eta
	hSecondLdgJetEta->Fill(myFilteredJets.at(1).eta());
	hThirdLdgJetEta->Fill(myFilteredJets.at(2).eta());
	hFourthLdgJetEta->Fill(myFilteredJets.at(3).eta());
	// hFifthLdgJetEta->Fill(myFilteredJets.at(4).eta());
      } else{
	// Fill with empty vector
	reco::JPTJet myEmptyJPTJet;
	myDataLdgJet->push_back( myEmptyJPTJet );
	myDataSecondLdgJet->push_back( myEmptyJPTJet ); 
	myDataThirdLdgJet->push_back( myEmptyJPTJet );
 	myDataFourthLdgJet->push_back( myEmptyJPTJet );
	// myDataFifthLdgJet->push_back( myEmptyJPTJet);
      }
    } else{ 
      // Fill histos with "error-values"
      hLdgJetEt->Fill(-1.0);
      hSecondLdgJetEt->Fill(-1.0);
      hThirdLdgJetEt->Fill(-1.0);
      hFourthLdgJetEt->Fill(-1.0);
      // hFifthLdgJetEt->Fill(-1.0);
      hLdgJetEta->Fill(-999.0);
      hSecondLdgJetEta->Fill(-999.0);
      hThirdLdgJetEta->Fill(-999.0);
      hFourthLdgJetEta->Fill(-999.0);
      // hFifthLdgJetEta->Fill(-999.0);
    }
    
    // Step 7) Put event data
    // **********************
    iEvent.put(myDataLdgJet, "LdgJet");
    iEvent.put(myDataSecondLdgJet, "SecondLdgJet");
    iEvent.put(myDataThirdLdgJet, "ThirdLdgJet");
    iEvent.put(myDataFourthLdgJet, "FourthLdgJet");
    // iEvent.put(myDataFifthLdgJet, "FifthLdgJet");
    // iEvent.put(myDataJPTJets, "JPTJets"); // likely to cause problems: different number of entries than rest of vectors 
    
    // Keep track of how many Evts the jet selection cuts were satisfied
    if(jetsPassCriteria){fCounter->addCount(fCounterNEvtsPassedSelection);}
    
    // Return true if "fCutMinNJets" Jets satisfy the cuts on Jet Et, Jet Eta and Jet EMFraction.
    return jetsPassCriteria;

  }//eof:  HPlusJetSelection::doJPTJets()
  
  std::vector<reco::JPTJet> HPlusJetSelection::sortJPTJets(std::vector<reco::JPTJet> JPTJetsToSort, const size_t JPTJetSize) {

    // Declare variables
    reco::JPTJet myTmpLdgJet;
    reco::JPTJet myTmpLdgJet_new;
    std::vector<reco::JPTJet> JPTJetsSorted;
    std::vector<reco::JPTJet>::iterator myJet;
    // Store the "first" N jets [wrt energy).
    for ( size_t i = 0; i < JPTJetSize; i++) {
      for ( myJet = JPTJetsToSort.begin(); myJet != JPTJetsToSort.end(); ++myJet) {
	if( (*myJet).energy() > myTmpLdgJet.energy() ){ 
	  myTmpLdgJet = (*myJet);
	} else{}
      }
      // Store myJet as ith-LdgJet (descending order in Energy)
      JPTJetsSorted.push_back(myTmpLdgJet);
      // Delete myJet from vector list
      JPTJetsToSort = eraseVectorElement(JPTJetsToSort, myTmpLdgJet);
      myTmpLdgJet = myTmpLdgJet_new;
    }//eof: for ( size_t i = 0; i < JPTJetsToSort.size(); i++) {

    return JPTJetsSorted;
    
  }//eof: HPlusJetSelection::sortJPTJets()           

  std::vector<reco::JPTJet> HPlusJetSelection::filterJPTJets(std::vector<reco::JPTJet> JPTJetsSorted, const size_t JPTJetSize) {

    // Declare variables
    std::vector<reco::JPTJet> JPTJetsFiltered;
    std::vector<reco::JPTJet>::iterator it_JPTJetsFilteredCands;
    std::vector<reco::JPTJet>::iterator it_JPTJetsFiltered;
    bool passedJetEt      = false;
    bool passedJetEta     = false;
    bool passedEMFraction = false;  
    bool jetSurvives = false;   
    
    if(JPTJetSize >= fCutMinNJets){
      
      // Loop over sorted Jets and apply quality cuts
      for( it_JPTJetsFilteredCands = JPTJetsSorted.begin(); it_JPTJetsFilteredCands != JPTJetsSorted.end(); ++it_JPTJetsFilteredCands) {
	passedJetEt      = false;
	passedJetEta     = false;
	passedEMFraction = false;
	if( (*it_JPTJetsFilteredCands).et() >= fCutMinJetEt){ passedJetEt = true;}
	if( fabs((*it_JPTJetsFilteredCands).eta()) <= fCutMaxAbsJetEta){ passedJetEta = true;}
	if( (*it_JPTJetsFilteredCands).chargedEmEnergyFraction() <= fCutMaxEMFraction ){ passedEMFraction = true;}    // FIXME
	// if( (*it_JPTJetsFilteredCands).neutralEmEnergyFraction() <= fCutMaxEMFraction ){ passedEMFraction = true;} // FIXME
	std::cout << "*** HPlusJetSelection::filterJPTJets() *** WARNING! Using JPTJet.chargedEmEnergyFraction() for the EMFraction, and NOT JPTJet.neutralEmEnergyFraction() ...! " << std::endl;

	// Boolean will be used to erase those jets that do not satisfy criteria
	jetSurvives = ( passedJetEt && passedJetEta && passedEMFraction) ;
	if(jetSurvives){ 
	  JPTJetsFiltered.push_back(*it_JPTJetsFilteredCands);
	} 
	else{ 
	  // std::cout << "Jet did not survive " << std::endl;  
	}
      }
    }
    return JPTJetsFiltered;
    
  }//eof: HPlusJetSelection::filterJPTJets


  std::vector<reco::JPTJet> HPlusJetSelection::eraseVectorElement( std::vector<reco::JPTJet> myJetVector, reco::JPTJet test) {

    std::vector<reco::JPTJet>::iterator it;
    int counter = 0;
    //  bool success = false;

    for ( it = myJetVector.begin(); it!=myJetVector.end(); ++it) {

      if( (*it).energy() == test.energy() ){
	
	// std::cout << " Found match. Deleting vector with (*it).energy() = " << (*it).energy()  << std::endl;
	myJetVector.erase(myJetVector.begin()+counter);
	// success = true;
	break;
      } else{counter++;}
    }
    return myJetVector;
  }//eof: HPlusJetSelection::eraseVectorElement()



































  
  DEFINE_FWK_MODULE(HPlusJetSelection); 
  
}//eof: namespace HPlusAnalysis {
