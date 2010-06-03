#include "HiggsAnalysis/HPlusRootFileDumper/interface/GlobalMuonVeto.h"

#include <iostream>
#include <sstream>

namespace HPlusAnalysis {

GlobalMuonVeto::GlobalMuonVeto() :
HPlusAnalysisBase("GlobalMuonVeto") {
  fMaxMuonPt = -1;
  fMuonTracks.reserve(20);
}

GlobalMuonVeto::~GlobalMuonVeto() {
}

void GlobalMuonVeto::setup(const edm::ParameterSet& iConfig) {
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
  fPassedGlobalMuonVeto = fCounter->addCounter("Global muon veto passed");
  fAllMuonCandidates = fCounter->addSubCounter("GlobalMuonVeto: All mu candidates");
  fAfterExcludedMuons = fCounter->addSubCounter("GlobalMuonVeto: Excluded mu removed");
  fAfterTrackRefNonNull = fCounter->addSubCounter("GlobalMuonVeto: Muon track found");
  fFailedPtCut = fCounter->addSubCounter("GlobalMuonVeto: After pT cut");
}

void GlobalMuonVeto::setRootTreeBranches(TTree& tree) {
  // Setup branches
  tree.Branch("MuonVeto_MaxMuonPt", &fMaxMuonPt);
  
  // Set histograms
  std::cout << "muon isHistogrammed=" << isHistogrammed() << std::endl;
  if (isHistogrammed()) {
    hMuonMaxPt = fFileService->make<TH1F>("N / 2 GeV/c", "Highest global #mu p_{T}, GeV/c", 100, 0., 200.);
    hMuonEtaofHighest = fFileService->make<TH1F>("N / 0.05", "#eta of highest global #mu", 120, -3.0, 3.0);
    hMuonPtAllMuons = fFileService->make<TH1F>("N / 2 GeV/c", "#mu p_{T} of all global #mu's, GeV/c", 100, 0., 200.);
    hMuonEtaAllMuons = fFileService->make<TH1F>("N / 0.05", "#eta of all global #mu's", 120, -3.0, 3.0);
  }
}

bool GlobalMuonVeto::apply(const edm::Event& iEvent) {
  // Initialize histogramming variables
  fMaxMuonPt = 0;
  fMuonTracks.clear();
  
  // Get muon handle
  edm::Handle<reco::MuonCollection> myMuonHandle;
  iEvent.getByLabel(fMuonCollectionName, myMuonHandle);
  if (!myMuonHandle->size()) {
    edm::LogInfo("HPlus") << "Muon handle is empty!" << std::endl;
    // No muons --> global muon veto has been passed
    fCounter->addCount(fPassedGlobalMuonVeto);
    return true;
  }
  
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
    if (isHistogrammed()) fMuonTracks.push_back(myTrackRef);
    double myMuonPt = myTrackRef->pt();
    //fHistograms->fill("h_vetoMuon_pt",(*iMuon)->Pt());
    //if (myMuonPt > 0) fHistograms->fill("h_vetoMuon_eta",(*iMuon)->Eta()); // protection against infinite eta
    //double DRmuonWmunu = 999;
    //if( mcMuonFromW.Et() > 0 ) DRmuonWmunu = (*iMuon)->DeltaR(mcMuonFromW);

    //if(!isolation(&(*iMuon)) ) continue;
    //fEventCounter->addSubCount("muon cands, isolation");
    //fHistograms->fill("h_ptIsolatedMuon",iMuon->Pt());

    // Check the muon pt
    if (myMuonPt > fMaxMuonPt)
      fMaxMuonPt = myMuonPt;
    std::cout << "muon pt=" << myMuonPt << ", max=" << fMaxMuonPt << std::endl;
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
  if (!myDecisionStatus) std::cout << "failed" << std::endl;
   
  if (myDecisionStatus) fCounter->addCount(fPassedGlobalMuonVeto);
  return myDecisionStatus;
}

void GlobalMuonVeto::fillRootTreeData(TTree& tree) {
  std::vector<reco::TrackRef>::const_iterator itEnd = fMuonTracks.end();
  for (std::vector<reco::TrackRef>::const_iterator it = fMuonTracks.begin(); it != itEnd; ++it) {
    if (abs((*it)->pt() - fMaxMuonPt) < 0.0001) {
      hMuonEtaofHighest->Fill((*it)->eta());
    }
    hMuonPtAllMuons->Fill((*it)->pt());
    hMuonEtaAllMuons->Fill((*it)->eta());
  }
  if (fMuonTracks.size()) {
    hMuonMaxPt->Fill(fMaxMuonPt);
  }
}


}


