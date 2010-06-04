#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusGlobalElectronVeto.h"

#include <iostream>
#include <string>
#include <vector>

#include "DataFormats/EgammaCandidates/interface/ElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/Electron.h"

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include "DataFormats/Common/interface/Handle.h"

HPlusGlobalElectronVeto::HPlusGlobalElectronVeto(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("GlobalElectronVeto"),
HPlusAnalysis::HPlusSelectionBase(iConfig) {
  // Parse the list of triggers in the config file
  if (iConfig.exists("ElectronCollectionName")) {
    fElectronCollectionName = iConfig.getParameter<edm::InputTag>("ElectronCollectionName");
  } else {
    throw cms::Exception("Configuration") << "GlobalElectronVeto: InputTag 'ElectronCollectionName' is missing in config!" << std::endl;
  }
  if (iConfig.exists("MaxElectronPtCutValue")) {
    fCutValueMaxElectronPt = iConfig.getParameter<double>("MaxElectronPtCutValue");
  } else {
    throw cms::Exception("Configuration") << "GlobalElectronVeto: float value 'MaxElectronPtCutValue' is missing in config!" << std::endl;
  }
  std::string myElectronIDString;
  if (iConfig.exists("ElectronIdentificationType")) {
    myElectronIDString = iConfig.getParameter<std::string>("ElectronIdentificationType");
    if (myElectronIDString == "NoElectronIdentification") {
      fElectronIdentificationType = HPlusGlobalElectronVeto::kNoElectronIdentification;
    } else if (myElectronIDString == "RobustElectronIdentification") {
      fElectronIdentificationType = HPlusGlobalElectronVeto::kRobustElectronIdentification;
    } else if (myElectronIDString == "LooseElectronIdentification") {
      fElectronIdentificationType = HPlusGlobalElectronVeto::kLooseElectronIdentification;
    } else if (myElectronIDString == "TightElectronIdentification") {
      fElectronIdentificationType = HPlusGlobalElectronVeto::kTightElectronIdentification;
    } else {
      throw cms::Exception("Configuration") << "GlobalElectronVeto: ElectronIdentificationType == '"
        << myElectronIDString << "' is not implemented!" << std::endl
        << "See enumerator ElectronIdentificationType in HPlusGlobalElectronVeto.h for available options" << std::endl;
    }
  } else {
    throw cms::Exception("Configuration") << "GlobalElectronVeto: string value 'ElectronIdentificationType' is missing in config!" << std::endl;
  }
  // Initialize counters
  fGlobalElectronVetoInput = fCounter->addCounter("GlobalElectronVeto input");
  fPassedGlobalElectronVeto = fCounter->addCounter("GlobalElectronVeto passed");
  fElectronCollectionHandleEmpty = fCounter->addSubCounter("GlobalElectronVeto: Electron collection is empty");
  fAllElectronCandidates = fCounter->addSubCounter("GlobalElectronVeto: All mu candidates");
  fAfterElectronID = fCounter->addSubCounter("GlobalElectronVeto: Passed electron ID '"+myElectronIDString+"'");
  fAfterTrackRefNonNull = fCounter->addSubCounter("GlobalElectronVeto: Electron track found");
  fFailedPtCut = fCounter->addSubCounter("GlobalElectronVeto: After pT cut");
  
  // Declare produced items
  std::string alias;
  produces<float>(alias = "GlobalElectronVetoMaxElectronPt").setBranchAlias(alias);
}

HPlusGlobalElectronVeto::~HPlusGlobalElectronVeto() {
}

void HPlusGlobalElectronVeto::beginJob() {
  // Set histograms
  if (isHistogrammed()) {
    hElectronMaxPt = fFileService->make<TH1F>("HighestGlobalElectronPt", "Highest global electron p_{T}",  100, 0., 200.);
    hElectronEtaofHighest = fFileService->make<TH1F>("HighestGlobalElectronEta", "#eta of highest global electron", 120, -3.0, 3.0);
    hElectronPtAllElectrons = fFileService->make<TH1F>("AllGlobalElectronPt", "Electron p_{T} of all global electrons", 100, 0., 200.);
    hElectronEtaAllElectrons = fFileService->make<TH1F>("AllGlobalElectronEta", "#eta of all global electrons", 120, -3.0, 3.0);
  }
}

void HPlusGlobalElectronVeto::endJob() {

}

bool HPlusGlobalElectronVeto::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fCounter->addCount(fGlobalElectronVetoInput);
  // Get muon handle
  edm::Handle<reco::ElectronCollection> myElectronHandle;
  iEvent.getByLabel(fElectronCollectionName, myElectronHandle);
  if (!myElectronHandle->size()) {
    //edm::LogInfo("HPlus") << "Electron handle is empty!" << std::endl;
    // No muons --> global muon veto has been passed
    fCounter->addCount(fPassedGlobalElectronVeto);
    fCounter->addCount(fElectronCollectionHandleEmpty);
    return true;
  }
  
  std::auto_ptr<float> myHighestElectronPt(new float); // highest pt of muon that has passed all criteria
  /*
  // Analyze MC info to look for muons from a W
  TLorentzVector mcElectronFromW(0,0,0,0);
  std::vector<MCJet*> myMCLeptons = fMCTopology->getMCElectronsAndElectrons();
  std::vector<MCJet*>::iterator iMCLeptonEnd = myMCLeptons.end();
  for (std::vector<MCJet*>::iterator iMCLepton = myMCLeptons.begin(); iMCLepton != iMCLeptonEnd; ++iMCLepton) {
    if (!(*iMCLepton)->isMu()) continue; // true if the MC particle is a muon
    if (!(*iMCLepton)->originatesFromWDecay()) continue; // true if the MC particle comes from a W decay
    mcElectronFromW = *(*iMCLepton)->getJetParticle();
  }
  if (mcElectronFromW.Et() > 0) fHistograms->fill("h_McElectronFromW_pt",mcElectronFromW.Pt());
  */
  
  bool myDecisionStatus = true;

  // Loop over muons
  *myHighestElectronPt = 0;
  double myHighestElectronEta = -10;
  for (reco::ElectronCollection::const_iterator iElectron = myElectronHandle->begin(); iElectron != myElectronHandle->end(); ++iElectron) {
    fCounter->addCount(fAllElectronCandidates);

    // Add here electron identification
    
    fCounter->addCount(fAfterElectronID);
    /*
    // Obtain highest pT of muons
    reco::TrackRef myTrackRef = (*iElectron).globalTrack();
    if (myTrackRef.isNull()) continue;
    fCounter->addCount(fAfterTrackRefNonNull);
    // Plot pt and eta of all muons 
    if (isHistogrammed()) {
      hElectronPtAllElectrons->Fill(myTrackRef->pt());
      hElectronEtaAllElectrons->Fill(myTrackRef->eta());
    }
    
    double myElectronPt = myTrackRef->pt();
    //fHistograms->fill("h_vetoElectron_pt",(*iElectron)->Pt());
    //if (myElectronPt > 0) fHistograms->fill("h_vetoElectron_eta",(*iElectron)->Eta()); // protection against infinite eta
    //double DRmuonWmunu = 999;
    //if( mcElectronFromW.Et() > 0 ) DRmuonWmunu = (*iElectron)->DeltaR(mcElectronFromW);

    //if(!isolation(&(*iElectron)) ) continue;
    //fEventCounter->addSubCount("muon cands, isolation");
    //fHistograms->fill("h_ptIsolatedElectron",iElectron->Pt());

    // Check the muon pt
    if (myElectronPt > *myHighestElectronPt) {
      *myHighestElectronPt = myElectronPt;
      myHighestElectronEta = myTrackRef->eta();
    }
    if (myElectronPt < fCutValueMaxElectronPt) continue;
    fCounter->addCount(fFailedPtCut);
    
//  if(!muonTag(*iElectron) ) continue;
//  fEventCounter->addSubCount("muon cands, tagged");

    myDecisionStatus = false;
*/
  }
  /*
  if (isHistogrammed()) {
    hElectronMaxPt->Fill(*myHighestElectronPt);
    if (hElectronMaxPt > 0)
      hElectronEtaofHighest->Fill(myHighestElectronEta);
  }
  //if (!myDecisionStatus) std::cout << "failed" << std::endl;
   
  if (myDecisionStatus) {
    fCounter->addCount(fPassedGlobalElectronVeto);
    iEvent.put(myHighestElectronPt, "GlobalElectronVetoMaxElectronPt");
  }*/
  return myDecisionStatus;
}

DEFINE_FWK_MODULE(HPlusGlobalElectronVeto);
