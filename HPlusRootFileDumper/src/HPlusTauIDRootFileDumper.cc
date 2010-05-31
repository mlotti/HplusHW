#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauIDRootFileDumper.h"

#include "TLorentzVector.h"

#include <string>

HPlusTauIDRootFileDumper::HPlusTauIDRootFileDumper(const edm::ParameterSet& iConfig)
  : fTauDumper(0) {
  // Find chosen tau collection name
  edm::InputTag myTauCollectionName = iConfig.getParameter<edm::InputTag>("tauCollectionName");
  edm::LogInfo("Hplus") << "Using tau collection: " << myTauCollectionName.label(); 
  
  // Find different tau collection parameter sets
  std::vector<edm::ParameterSet> myPFTaus;
  if (iConfig.exists("PFTaus")) {
    myPFTaus = iConfig.getParameter<std::vector<edm::ParameterSet> >("PFTaus");
  } else {
    edm::LogWarning("HPlus") << "You might want to add a PFTaus vector of PSets to the py-file";
  }
  std::vector<edm::ParameterSet> myCaloTaus;
  if (iConfig.exists("CaloTaus")) {
    myCaloTaus = iConfig.getParameter<std::vector<edm::ParameterSet> >("CaloTaus");
  } else {
    edm::LogWarning("HPlus") << "You might want to add a CaloTaus vector of PSets to the py-file";
  }
  std::vector<edm::ParameterSet> myTCTaus;
  if (iConfig.exists("TCTaus")) {
    myTCTaus = iConfig.getParameter<std::vector<edm::ParameterSet> >("TCTaus");
  } else {
    edm::LogWarning("HPlus") << "You might want to add a TCTaus vector of PSets to the py-file";
  }
  
  // Create event counter object
  fCounter = new HPlusAnalysis::Counter();
  
  // Find correct tau collection from parameter sets
  edm::ParameterSet myTauCollectionParameters;
  for (size_t i = 0; i < myPFTaus.size(); ++i) {
    edm::InputTag mySource = myPFTaus[i].getParameter<edm::InputTag>("src");
    if (mySource.label() == myTauCollectionName.label()) {
      myTauCollectionParameters = myPFTaus[i];
      fTauDumper = new HPlusAnalysis::HPlusTauDumperPF(*this, myTauCollectionParameters, fCounter);
    }
  }
  for (size_t i = 0; i < myCaloTaus.size(); ++i) {
    edm::InputTag mySource = myCaloTaus[i].getParameter<edm::InputTag>("src");
    if (mySource.label() == myTauCollectionName.label()) {
      myTauCollectionParameters = myCaloTaus[i];
      fTauDumper = new HPlusAnalysis::HPlusTauDumperCaloTau(*this, myTauCollectionParameters, fCounter);
    }
  }
  for (size_t i = 0; i < myTCTaus.size(); ++i) {
    edm::InputTag mySource = myTCTaus[i].getParameter<edm::InputTag>("src");
    if (mySource.label() == myTauCollectionName.label()) {
      myTauCollectionParameters = myTCTaus[i];
      fTauDumper = new HPlusAnalysis::HPlusTauDumperCaloTau(*this, myTauCollectionParameters, fCounter);
    }
  }
  if (!fTauDumper)
    throw cms::Exception("Configuration") << "tau collection '" << myTauCollectionName.label() << "' not found in dataset" << std::endl;

  // Set up event counters - note: they will appear in the histograms in the order they are created
  fCounterIdAllEvents = fCounter->addCounter("All events");
  // add here other counters
  fCounterIdSavedEvents = fCounter->addCounter("Saved events");
  
  // Create selection manager and initialize it
  //fSelectionManager = new HPlusAnalysis::SelectionManager(fFileService, *fCounter);
  //fSelectionManager->setup(iConfig);

  // Set up ROOT tree branches
  //setupRootTreeBranches();
  
  // Set up produced item aliases
  std::string alias;
  produces<unsigned int>(alias = "evt").setBranchAlias(alias);
  produces<unsigned int>(alias = "run").setBranchAlias(alias);
  produces<unsigned int>(alias = "lumi").setBranchAlias(alias);
}

HPlusTauIDRootFileDumper::~HPlusTauIDRootFileDumper() {
  if (fTauDumper) delete fTauDumper;
  //delete fSelectionManager;
  delete fCounter;
}

/*
void HPlusTauIDRootFileDumper::setupRootTreeBranches() {
  // Add branches for event selections
  fSelectionManager->setRootTreeBranches(*fRootTree);
  
  // Add branches common to all tau collections
  fRootTree->Branch("run", &fRunNumber); // Note: do not change name - needed exactly like this for AnalysisPack
  fRootTree->Branch("lumi", &fLumiSection); // Note: do not change name - needed exactly like this for AnalysisPack
  fRootTree->Branch("evt", &fEventNumber); // Note: do not change name - needed exactly like this for AnalysisPack
  fTauDumper->setupCommonRootTreeBranches();
    
  // Add branches specific to the tau collection
  fTauDumper->setupSpecificRootTreeBranches();
}
*/
/*
void HPlusTauIDRootFileDumper::initializeRootTreeVariables() {
  // Initialize here variables common to all tau collections
  fEventNumber = -1;
  fRunNumber = -1;
  fLumiSection = -1;
  fTauDumper->initializeCommonBranchData();
  
  // Initialize the tau collection specific tree variables
  fTauDumper->initializeSpecificBranchData();
}
*/
// ------------ method called to for each event  ------------
void HPlusTauIDRootFileDumper::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fCounter->addCount(fCounterIdAllEvents);

  // Reset the ROOT tree variables
  //initializeRootTreeVariables();

  // Apply event selection here (trigger, ...)
  //if (!fSelectionManager->apply(iEvent)) return;
  // Fill branch data related to event selections
  //fSelectionManager->fillRootTreeData(*fRootTree);
  
  // Set event identifying variables
  std::auto_ptr<unsigned int> myRunNumber(new unsigned int);
  std::auto_ptr<unsigned int> myLumiSection(new unsigned int);
  std::auto_ptr<unsigned int> myEventNumber(new unsigned int);
  *myRunNumber = iEvent.run();
  *myLumiSection = iEvent.luminosityBlock();
  *myEventNumber = iEvent.id().event();

  iEvent.put(myRunNumber, "run");
  iEvent.put(myLumiSection, "lumi");
  iEvent.put(myEventNumber, "evt");
  
  
  //fTauDumper->setupCommonRootTreeBranches(iEvent);

  // Set tau-jet variables
  fTauDumper->setData(iEvent);
  // ROOT tree filling is called inside the tau dumper object
  // Therefore, do not add ROOT tree filling here
  fCounter->addCount(fCounterIdSavedEvents);
}

// ------------ method called once each job just before starting event loop  ------------
void HPlusTauIDRootFileDumper::beginJob() {

}

// ------------ method called once each job just after ending the event loop  ------------
void HPlusTauIDRootFileDumper::endJob() {
  fCounter->storeCountersToHistogram(fFileService);
  
  // Close ROOT file
  //edm::LogInfo("Hplus") << "Written and closed file " << fRootFilename;
}

//define this class as a plug-in
DEFINE_FWK_MODULE(HPlusTauIDRootFileDumper);
