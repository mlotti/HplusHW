#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusGlobalMuonVeto.h"

#include <iostream>
#include <string>

//namespace HPlusAnalysis {

HPlusGlobalMuonVeto::HPlusGlobalMuonVeto(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("GlobalMuonVeto"),
HPlusAnalysis::HPlusSelectionBase(iConfig) {
  // Parse the list of triggers in the config file
  if (iConfig.exists("MuonCollectionName")) {
    fMuonCollectionName = iConfig.getParameter<edm::InputTag>("MuonCollectionName");
  } else {
    throw cms::Exception("Configuration") << "GlobalMuonVeto: InputTag 'MuonCollectionName' is missing in config!" << std::endl;
  }
  if (iConfig.exists("MaxMuonPtCutValue")) {
    fCutValueMaxMuonPt = iConfig.getParameter<double>("MaxMuonPtCutValue");
  } else {
    throw cms::Exception("Configuration") << "GlobalMuonVeto: float value 'MaxMuonPtCutValue' is missing! in config!" << std::endl;
  }
  // Initialize counters
  fGlobalMuonVetoInput = fCounter->addCounter("GlobalMuonVeto input");
  fPassedGlobalMuonVeto = fCounter->addCounter("GlobalMuonVeto passed");
  fMuonCollectionHandleEmpty = fCounter->addSubCounter("GlobalMuonVeto: Muon collection is empty");
  fAllMuonCandidates = fCounter->addSubCounter("GlobalMuonVeto: All mu candidates");
  fAfterExcludedMuons = fCounter->addSubCounter("GlobalMuonVeto: Excluded mu removed");
  fAfterTrackRefNonNull = fCounter->addSubCounter("GlobalMuonVeto: Muon track found");
  fFailedPtCut = fCounter->addSubCounter("GlobalMuonVeto: After pT cut");
  
  // Declare produced items
  std::string alias;
  produces<float>(alias = "GlobalMuonVetoMaxMuonPt").setBranchAlias(alias);
}

HPlusGlobalMuonVeto::~HPlusGlobalMuonVeto() {
}

void HPlusGlobalMuonVeto::beginJob() {
  // Set histograms
  if (isHistogrammed()) {
    hMuonMaxPt = fFileService->make<TH1F>("HighestGlobalMuPt", "Highest global #mu p_{T}",  100, 0., 200.);
    hMuonEtaofHighest = fFileService->make<TH1F>("HighestGlobalMuEta", "#eta of highest global #mu", 120, -3.0, 3.0);
    hMuonPtAllMuons = fFileService->make<TH1F>("AllGlobalMuPt", "#mu p_{T} of all global #mu's", 100, 0., 200.);
    hMuonEtaAllMuons = fFileService->make<TH1F>("AllGlobalMuEta", "#eta of all global #mu's", 120, -3.0, 3.0);
  }
}

void HPlusGlobalMuonVeto::endJob() {

}

bool HPlusGlobalMuonVeto::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fCounter->addCount(fGlobalMuonVetoInput);
  // Get muon handle
  edm::Handle<reco::MuonCollection> myMuonHandle;
  iEvent.getByLabel(fMuonCollectionName, myMuonHandle);
  if (!myMuonHandle->size()) {
    //edm::LogInfo("HPlus") << "Muon handle is empty!" << std::endl;
    // No muons --> global muon veto has been passed
    fCounter->addCount(fPassedGlobalMuonVeto);
    fCounter->addCount(fMuonCollectionHandleEmpty);
    return true;
  }
  
  std::auto_ptr<float> myHighestMuonPt(new float); // highest pt of muon that has passed all criteria
  /*
  // Analyze MC info to look for muons from a W
  TLorentzVector mcMuonFromW(0,0,0,0);
  std::vector<MCJet*> myMCLeptons = fMCTopology->getMCElectronsAndMuons();
  std::vector<MCJet*>::iterator iMCLeptonEnd = myMCLeptons.end();
  for (std::vector<MCJet*>::iterator iMCLepton = myMCLeptons.begin(); iMCLepton != iMCLeptonEnd; ++iMCLepton) {
    if (!(*iMCLepton)->isMu()) continue; // true if the MC particle is a muon
    if (!(*iMCLepton)->originatesFromWDecay()) continue; // true if the MC particle comes from a W decay
    mcMuonFromW = *(*iMCLepton)->getJetParticle();
  }
  if (mcMuonFromW.Et() > 0) fHistograms->fill("h_McMuonFromW_pt",mcMuonFromW.Pt());
  */
  
  bool myDecisionStatus = true;

  // Loop over muons
  *myHighestMuonPt = 0;
  double myHighestMuonEta = -10;
  for (reco::MuonCollection::const_iterator iMuon = myMuonHandle->begin(); iMuon != myMuonHandle->end(); ++iMuon) {
    fCounter->addCount(fAllMuonCandidates);

    // Match default muons to the list of excluded muons
    bool myMatchingStatus = false;
    for (std::vector<const reco::Muon*>::iterator iExcludedMuon = fExcludedMuons.begin();
         iExcludedMuon != fExcludedMuons.end(); ++iExcludedMuon) {
      if (!myMatchingStatus) {
        if (&(*iMuon) == *iExcludedMuon) {
          myMatchingStatus = true;
        }
      }
    }
    if (myMatchingStatus) continue;
    fCounter->addCount(fAfterExcludedMuons);
    
    // Obtain highest pT of muons
    reco::TrackRef myTrackRef = (*iMuon).globalTrack();
    if (myTrackRef.isNull()) continue;
    fCounter->addCount(fAfterTrackRefNonNull);
    // Plot pt and eta of all muons 
    if (isHistogrammed()) {
      hMuonPtAllMuons->Fill(myTrackRef->pt());
      hMuonEtaAllMuons->Fill(myTrackRef->eta());
    }
    
    double myMuonPt = myTrackRef->pt();
    //fHistograms->fill("h_vetoMuon_pt",(*iMuon)->Pt());
    //if (myMuonPt > 0) fHistograms->fill("h_vetoMuon_eta",(*iMuon)->Eta()); // protection against infinite eta
    //double DRmuonWmunu = 999;
    //if( mcMuonFromW.Et() > 0 ) DRmuonWmunu = (*iMuon)->DeltaR(mcMuonFromW);

    //if(!isolation(&(*iMuon)) ) continue;
    //fEventCounter->addSubCount("muon cands, isolation");
    //fHistograms->fill("h_ptIsolatedMuon",iMuon->Pt());

    // Check the muon pt
    if (myMuonPt > *myHighestMuonPt) {
      *myHighestMuonPt = myMuonPt;
      myHighestMuonEta = myTrackRef->eta();
    }
    if (myMuonPt < fCutValueMaxMuonPt) continue;
    fCounter->addCount(fFailedPtCut);
    
//  if(!muonTag(*iMuon) ) continue;
//  fEventCounter->addSubCount("muon cands, tagged");

    myDecisionStatus = false;

    // Fill fHistogram for muons which have failed the cuts
    /*if (DRmuonWmunu < 0.4) fHistograms->fill("h_McMuonFromW_selected_pt",mcMuonFromW.Pt());
    for (std::vector<MCJet*>::iterator iMCLepton = myMCLeptons.begin(); iMCLepton != iMCLeptonEnd; ++iMCLepton) {
      if (!(*iMCLepton)->isMu()) continue; // true if the MC particle is a muon
      double drmuons = (*iMuon)->DeltaR(*((*iMCLepton)->getJetParticle()));
      if (drmuons > 0.2) continue;
      fEventCounter->addSubCount("veto muon cands, mc match");
      if (!(*iMCLepton)->originatesFromWDecay()) continue;
      fEventCounter->addSubCount("veto muon cands, mc mu from W");
    }*/
  }
  if (isHistogrammed()) {
    hMuonMaxPt->Fill(*myHighestMuonPt);
    if (hMuonMaxPt > 0)
      hMuonEtaofHighest->Fill(myHighestMuonEta);
  }
  //if (!myDecisionStatus) std::cout << "failed" << std::endl;
   
  if (myDecisionStatus) {
    fCounter->addCount(fPassedGlobalMuonVeto);
    iEvent.put(myHighestMuonPt, "GlobalMuonVetoMaxMuonPt");
  }
  return myDecisionStatus;
}

//}

DEFINE_FWK_MODULE(HPlusGlobalMuonVeto);
