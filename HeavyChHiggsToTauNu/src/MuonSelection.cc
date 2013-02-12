#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "Math/GenVector/VectorUtil.h"
#include "TLorentzVector.h"
#include "TVector3.h"

std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);

namespace HPlus {
  MuonSelection::Data::Data():
    fPassedEvent(false),
    fSelectedMuonPt(0.),
    fSelectedMuonEta(0.),
    fSelectedMuonPtBeforePtCut(0.) {}
  MuonSelection::Data::~Data() {}

  MuonSelection::MuonSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fMuonCollectionName(iConfig.getUntrackedParameter<edm::InputTag>("MuonCollectionName")),
    fMuonSelection(iConfig.getUntrackedParameter<std::string>("MuonSelection")),
    fMuonPtCut(iConfig.getUntrackedParameter<double>("MuonPtCut")),
    fMuonEtaCut(iConfig.getUntrackedParameter<double>("MuonEtaCut")),
    fMuonApplyIpz(iConfig.getUntrackedParameter<bool>("MuonApplyIpz")),
    fMuonSelectionCounter(eventCounter.addSubCounter("GlobalMuon Selection","MuonSelection")),
    fMuonSelectionSubCountMuonPresent(eventCounter.addSubCounter("GlobalMuon Selection","Muon present")),
    fMuonSelectionSubCountMuonHasGlobalOrInnerTrk(eventCounter.addSubCounter("GlobalMuon Selection","Muon has Global OR Inner Trk")),
    fMuonSelectionSubCountPtCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon Pt")),
    fMuonSelectionSubCountEtaCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon Eta")),
    fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon(eventCounter.addSubCounter("GlobalMuon Selection","Global OR Tracker Muon")),
    fMuonSelectionSubCountMuonSelection(eventCounter.addSubCounter("GlobalMuon Selection","Muon Selection")),
    fMuonSelectionSubCountNTrkerHitsCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon NTrkerHits")),
    fMuonSelectionSubCountNPixelHitsCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon NPixelHits")),
    fMuonSelectionSubCountNMuonlHitsCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon NMuonlHits")),
    fMuonSelectionSubCountGlobalTrkChiSqCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon GlobalTrkChiSq")),
    fMuonSelectionSubCountImpactParCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon ImpactPar")),
    fMuonSelectionSubCountRelIsolationR03Cut(eventCounter.addSubCounter("GlobalMuon Selection","Muon RelIsolationR03")),
    fMuonSelectionSubCountGoodPVCut(eventCounter.addSubCounter("GlobalMuon Selection","Muon GoodPV")),
    fMuonSelectionSubCountMatchingMCmuon(eventCounter.addSubCounter("GlobalMuon Selection","Muon matching MC Muon")),
    fMuonSelectionSubCountMatchingMCmuonFromW(eventCounter.addSubCounter("GlobalMuon Selection","Muon matching MC Muon From W")),
    fMuonIDSubCountAllMuonCandidates(eventCounter.addSubCounter("GlobalMuon ID","All Muon Candidates")),
    fMuonIDSubCountAll(eventCounter.addSubCounter("GlobalMuon ID","All")),
    fMuonIDSubCountAllGlobalMuons(eventCounter.addSubCounter("GlobalMuon ID","AllGlobalMuons")),
    fMuonIDSubCountAllStandAloneMuons(eventCounter.addSubCounter("GlobalMuon ID","AllStandAloneMuons")),
    fMuonIDSubCountAllTrackerMuons(eventCounter.addSubCounter("GlobalMuon ID","AllTrackerMuons")),
    fMuonIDSubCountTrackerMuonArbitrated(eventCounter.addSubCounter("GlobalMuon ID","TrackerMuonArbitrated")),
    fMuonIDSubCountAllArbitrated(eventCounter.addSubCounter("GlobalMuon ID","AllArbitrated")),
    fMuonIDSubCountGlobalMuonPromptTight(eventCounter.addSubCounter("GlobalMuon ID","GlobalMuonPromptTight")),
    fMuonIDSubCountTMLastStationLoose(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationLoose")),
    fMuonIDSubCountTMLastStationTight(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationTight")),
    fMuonIDSubCountTMOneStationLoose(eventCounter.addSubCounter("GlobalMuon ID","TMOneStationLoose")),
    fMuonIDSubCountTMLastStationOptimizedLowPtLoose(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationOptimizedLowPtLoose")),
    fMuonIDSubCountTMLastStationOptimizedLowPtTight(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationOptimizedLowPtTight")),
    fMuonIDSubCountGMTkChiCompatibility(eventCounter.addSubCounter("GlobalMuon ID","GMTkChiCompatibility")),
    fMuonIDSubCountGMTkKinkTight(eventCounter.addSubCounter("GlobalMuon ID","GMTkKinkTight")),
    fMuonIDSubCountTMLastStationAngLoose(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationAngLoose")),
    fMuonIDSubCountTMLastStationAngTight(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationAngTight")),
    fMuonIDSubCountTMLastStationOptimizedBarrelLowPtLoose(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationOptimizedBarrelLowPtLoose")),
    fMuonIDSubCountTMLastStationOptimizedBarrelLowPtTight(eventCounter.addSubCounter("GlobalMuon ID","TMLastStationOptimizedBarrelLowPtTight")),
    fMuonIDSubCountOther(eventCounter.addSubCounter("GlobalMuon ID","Other"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("MuonSelection");
    
    hMuonPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPt", "GlobalMuonPt;isolated muon p_{T}, GeV/c;N_{muons} / 5 GeV/c", 200, 0., 400.);
    hMuonEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEta", "GlobalMuonEta;isolated muon #eta;N_{muons} / 0.1", 60, -3., 3.);
    hMuonEta_identified = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "GlobalMuonEta_identified", "GlobalMuonEta;isolated muon #eta;N_{muons} / 0.1", 60, -3., 3.);
    hMuonPt_identified_eta = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "GlobalMuonPt_identified_eta", "GlobalMuonPt;isolated muon p_{T}, GeV/c;N_{muons} / 5 GeV/c", 81, 0., 400.);
    //    hMuonEta_test = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "GlobalMuonEta_test", "GlobalMuonEta;isolated muon #eta;N_{muons} / 0.1", 60, -3., 3.);
    //    hMuonPt_test = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "GlobalMuonPt_test", "GlobalMuonPt;isolated muon p_{T}, GeV/c;N_{muons} / 5 GeV/c", 81, -5., 400.);
    hNumberOfSelectedMuons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfSelectedMuons", "NumberOfSelectedMuons", 30, 0., 30.);
    hMuonPt_matchingMCmuon = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPtmatchingMCmuon", "GlobalMuonPtmatchingMCmuon", 200, 0., 400.);
    hMuonEta_matchingMCmuon = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEtamatchingMCmuon", "GlobalMuonEtamatchingMCmuon", 60, -3., 3.);
    hMuonPt_matchingMCmuonFromW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPtmatchingMCmuonFromW", "GlobalMuonPtmatchingMCmuonFromW", 200, 0., 400.);
    hMuonEta_matchingMCmuonFromW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEtamatchingMCmuonFromW", "GlobalMuonEtamatchingMCmuonFromW", 60, -3., 3.);
    hMuonPt_InnerTrack = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPt_InnerTrack", "GlobalMuonPt_InnerTrack", 200, 0., 400.);
    hMuonEta_InnerTrack = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEta_InnerTrack", "GlobalMuonEta_InnerTrack", 60, -3., 3.);
    hMuonPt_GlobalTrack = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPt_GlobalTrack", "GlobalMuonPt_GlobalTrack", 200, 0., 400.);
    hMuonEta_GlobalTrack = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEta_GlobalTrack", "GlobalMuonEta_GlobalTrack", 60, -3., 3.);
    hMuonPt_AfterSelection  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPt_AfterSelection", "GlobalMuonPt_AfterSelection", 200, 0., 400.);
    hMuonEta_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEta_AfterSelection", "GlobalMuonEta_AfterSelection", 60, -3., 3.);
    //    hMuonPt_InnerTrack_AfterSelection  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPt_InnerTrack_AfterSelection", "GlobalMuonPt_InnerTrack_AfterSelection", 100, 0., 400.);
    //    hMuonEta_InnerTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEta_InnerTrack_AfterSelection", "GlobalMuonEta_InnerTrack_AfterSelection", 60, -3., 3.);
    hMuonPt_GlobalTrack_AfterSelection  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonPt_GlobalTrack_AfterSelection", "GlobalMuonPt_GlobalTrack_AfterSelection", 100, 0., 400.);
    hMuonEta_GlobalTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalMuonEta_GlobalTrack_AfterSelection", "GlobalMuonEta_GlobalTrack_AfterSelection", 60, -3., 3.);
    hMuonImpactParameter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonImpactParameter", "MuonImpactParameter", 100, 0., 0.1);
    hMuonZdiff = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonZdiff", "MuonZdiff", 100, 0., 10.);
 
    // Check here that the muon selection is reasonable
    if(fMuonSelection != "All" &&
       fMuonSelection != "AllGlobalMuons" &&
       fMuonSelection != "AllStandAloneMuons" && 
       fMuonSelection != "AllTrackerMuons" && 
       fMuonSelection != "TrackerMuonArbitrated" && 
       fMuonSelection != "AllArbitrated" && 
       fMuonSelection != "GlobalMuonPromptTight" && 
       fMuonSelection != "TMLastStationLoose" && 
       fMuonSelection != "TMLastStationTight" && 
       fMuonSelection != "TMOneStationLoose" && 
       fMuonSelection != "TMLastStationOptimizedLowPtLoose" && 
       fMuonSelection != "TMLastStationOptimizedLowPtTight" && 
       fMuonSelection != "GMTkChiCompatibility" && 
       fMuonSelection != "GMTkKinkTight" && 
       fMuonSelection != "TMLastStationAngLoose" && 
       fMuonSelection != "TMLastStationAngTight" && 
       fMuonSelection != "TMLastStationOptimizedBarrelLowPtLoose" && 
       fMuonSelection != "TMLastStationOptimizedBarrelLowPtTight") { 
      throw cms::Exception("Error") << "The MuonSelection \"" << fMuonSelection << "\" used as input in the python config file is invalid! Please choose one of the following valid options:\n All, AllGlobalMuons, AllStandAloneMuons, AllTrackerMuons, TrackerMuonArbitrated, AllArbitrated, GlobalMuonPromptTight, TMLastStationLoose, TMLastStationTight, TMOneStationLoose, TMLastStationOptimizedLowPtLoose, TMLastStationOptimizedLowPtTight, GMTkChiCompatibility, GMTkKinkTight, TMLastStationAngLoose, TMLastStationAngTight, TMLastStationOptimizedBarrelLowPtLoose, TMLastStationOptimizedBarrelLowPtTight.\n" << std::endl;
    }
  }

  MuonSelection::~MuonSelection() {}

  MuonSelection::Data MuonSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, primaryVertex);
  }

  MuonSelection::Data MuonSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, primaryVertex);
  }

  MuonSelection::Data MuonSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex) {
    Data output;
    // Do analysis
    doMuonSelection(iEvent,iSetup, primaryVertex, output);
    output.fPassedEvent = output.fSelectedMuons.size() == 0;
    if (output.fPassedEvent)
      increment(fMuonSelectionCounter);
    return output;
  }

  MuonSelection::Data MuonSelection::silentAnalyzeWithoutIsolation(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyzeWithoutIsolation(iEvent, iSetup, primaryVertex);
  }

  MuonSelection::Data MuonSelection::analyzeWithoutIsolation(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyzeWithoutIsolation(iEvent, iSetup, primaryVertex);
  }

  MuonSelection::Data MuonSelection::privateAnalyzeWithoutIsolation(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex) {
    Data output;
    // Do analysis
    doMuonSelection(iEvent, iSetup, primaryVertex, output);
    output.fPassedEvent = output.fSelectedMuonsBeforeIsolation.size() == 0;
    if (output.fPassedEvent)
      increment(fMuonSelectionCounter);
    return output;
  }


  void MuonSelection::doMuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex, MuonSelection::Data& output){
    // the Collection is currently NOT available in the PatTuples but it will be soon (next pattuple production)
    /* FIX ME
   // Create and attach handle to (Offline) Primary Vertices Collection
    edm::Handle<std::vector<reco::Vertex> > primaryVerticesHandle;
    //    edm::Handle<reco::VertexCollection> primaryVerticesHandle;
    iEvent.getByLabel("offlinePrimaryVertices", primaryVerticesHandle);
    // Create an XYZ position to store the Primary Vertex
    math::XYZPoint PVPosition;

    // Loop over all PV's. PV's are stored with decending Event Pt (PV candidate with highest associated Evt Trk Pt is stored first)
    for(unsigned int iPV = 0; iPV < primaryVerticesHandle->size(); ++iPV) {
      // Get PV candidate
      reco::Vertex myPV = primaryVerticesHandle->at(iPV);
      // Apply some quality to the PV candidate: a) PV is not fake, b) has more than 4 normalised degrees of freedom, 
      // c) has a z position less than 15 cm, and d) distance in the XY plane less than 2 cm.
      if( !(myPV.isFake()) && (myPV.ndof()) > 4  && ( abs( myPV.z() < 15) ) && (myPV.position().Rho() < 2) ){
	PVPosition = primaryVerticesHandle->at(0).position();
	break; //once a good PV is found exit loop.
      }
      else{
	PVPosition.SetX(-999.99);
	PVPosition.SetY(-999.99);
	PVPosition.SetZ(-999.99);
      }
    } 
    FIX ME */

    /* FIX ME
    // Get beam spot
    edm::Handle<reco::BeamSpot> BeamSpotHandle;
    iEvent.getByLabel(beamSpotCollection, BeamSpotHandle);
    const reco::BeamSpot *myBeamSpot = BeamSpotHandle.product();
    const math::XYZPoint myBeamSpotPosition = myBeamSpot->position();
    impactParameter = fabs( (*iMuon)->innerTrack()->dxy(myBeamSpotPosition) );
    impactParameter = fabs( (*iElectron)->gsfTrack()->dxy(myBeamSpotPosition) );
    FIX ME */ 


    // Create and attach handle to Muon Collection
    edm::Handle<edm::View<pat::Muon> > myMuonHandle;
    iEvent.getByLabel(fMuonCollectionName, myMuonHandle);    
    edm::PtrVector<pat::Muon> muons = myMuonHandle->ptrVector();
    // In the case where the handle is empty...
    if ( !myMuonHandle->size() ){
      // std::cout << "Muon handle for '" << fMuonCollectionName << " is empty!" << std::endl;
    }

    edm::Handle <edm::View<reco::GenParticle> > genParticles;
    iEvent.getByLabel("genParticles", genParticles);

    // Reset/initialise variables
    float myHighestMuonPt = -1.0;
    float myHighestMuonPtBeforePtCut = -1.0;
    float myHighestMuonEta = -999.99;
    // 
    bool bMuonPresent = false;
    bool bMuonHasGlobalOrInnerTrk = false;
    bool bMuonPtCut = false;
    bool bMuonEtaCut = false;
    bool bMuonGlobalMuonOrTrkerMuon = false;
    bool bMuonSelection = false;
    bool bMuonNTrkerHitsCut = false;
    bool bMuonNPixelHitsCut = false;
    bool bMuonNMuonlHitsCut = false;
    bool bMuonGlobalTrkChiSqCut = false;
    bool bMuonImpactParCut = false;
    bool bMuonRelIsolationR03Cut = false;
    bool bMuonGoodPVCut = false;

    // Loop over all Muons
    for(edm::PtrVector<pat::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {

      // Keep track of the muons analyzed
      bMuonPresent = true;
      increment(fMuonIDSubCountAllMuonCandidates);

      // Keep track of the MuonID's. Just for my information. 
      // 28/10/2010 - pat::Muon::muonID() used instead of pat::Muon::isGood(). The latter is there only for backward compatibility.
      if( (*iMuon)->muonID("All") ) increment(fMuonIDSubCountAll);
      if( (*iMuon)->muonID("AllGlobalMuons") ) increment(fMuonIDSubCountAllGlobalMuons);
      if( (*iMuon)->muonID("AllStandAloneMuons") ) increment(fMuonIDSubCountAllStandAloneMuons);
      if( (*iMuon)->muonID("AllTrackerMuons") ) increment(fMuonIDSubCountAllTrackerMuons);  
      if( (*iMuon)->muonID("TrackerMuonArbitrated") ) increment(fMuonIDSubCountTrackerMuonArbitrated);
      if( (*iMuon)->muonID("AllArbitrated") ) increment(fMuonIDSubCountAllArbitrated);
      if( (*iMuon)->muonID("GlobalMuonPromptTight")  ) increment(fMuonIDSubCountGlobalMuonPromptTight);  
      if( (*iMuon)->muonID("TMLastStationLoose") ) increment(fMuonIDSubCountTMLastStationLoose); 
      if( (*iMuon)->muonID("TMLastStationTight") ) increment(fMuonIDSubCountTMLastStationTight); 
      if( (*iMuon)->muonID("TMOneStationLoose") ) increment(fMuonIDSubCountTMOneStationLoose);   
      if( (*iMuon)->muonID("TMLastStationOptimizedLowPtLoose") ) increment(fMuonIDSubCountTMLastStationOptimizedLowPtLoose);  
      if( (*iMuon)->muonID("TMLastStationOptimizedLowPtTight") ) increment(fMuonIDSubCountTMLastStationOptimizedLowPtTight);
      if( (*iMuon)->muonID("GMTkChiCompatibility") ) increment(fMuonIDSubCountGMTkChiCompatibility);  
      if( (*iMuon)->muonID("GMTkKinkTight") ) increment(fMuonIDSubCountGMTkKinkTight); 
      if( (*iMuon)->muonID("TMLastStationAngLoose") ) increment(fMuonIDSubCountTMLastStationAngLoose); 
      if( (*iMuon)->muonID("TMLastStationAngTight") ) increment(fMuonIDSubCountTMLastStationAngTight); 
      if( (*iMuon)->muonID("TMLastStationOptimizedBarrelLowPtLoose") ) increment(fMuonIDSubCountTMLastStationOptimizedBarrelLowPtLoose);
      if( (*iMuon)->muonID("TMLastStationOptimizedBarrelLowPtTight") ) increment(fMuonIDSubCountTMLastStationOptimizedBarrelLowPtTight);
      else{
	increment(fMuonIDSubCountOther);
      }

      // Obtain reference to a Muon track
      reco::TrackRef myGlobalTrackRef = (*iMuon)->globalTrack();
      reco::TrackRef myInnerTrackRef = (*iMuon)->innerTrack(); // inner tracks give best resolution for muons with Pt up to 200 GeV/c

      // Check that track was found.
      if ( myInnerTrackRef.isNull() || myGlobalTrackRef.isNull() ){
	// std::cout << "myInnerTrackRef.isNull()" << std::endl;
	// std::cout << "(*iMuon).isStandAloneMuon() = " << (*iMuon).isStandAloneMuon() << std::endl;
	// std::cout << "(*iMuon).isGlobalMuon() = " << (*iMuon).isGlobalMuon() << std::endl;
	// std::cout << "(*iMuon).isTrackerMuon() = " << (*iMuon).isTrackerMuon() << std::endl;
	// std::cout << "(*iMuon).isCaloMuon() = " << (*iMuon).isCaloMuon() << std::endl;
	continue; 
      }
      bMuonHasGlobalOrInnerTrk = true;
      
      // Muon Variables (Pt, Eta etc..)
      float myMuonPt  = (*iMuon)->pt();
      float myMuonEta = (*iMuon)->eta();
      int myInnerTrackNTrkHits   = myInnerTrackRef->hitPattern().numberOfValidTrackerHits();
      int myInnerTrackNPixelHits = myInnerTrackRef->hitPattern().numberOfValidPixelHits();
      //int myGlobalTrackNMuonHits  = myGlobalTrackRef->hitPattern().numberOfValidMuonHits(); 
      int myMatchedSegments = (*iMuon)->numberOfMatches();
      // Note: It is possible for a Global Muon to have zero muon hits. This happens because once the inner and outter tracks used to create
      // global fit to the muon track that covers all of the detector, hits that are incompatible to the new trajectory are removed 
      // (i.e. de-associated from the muon). This is the so called "outlier rejection". 
      // Note: For the Num

      // Fill histos with all-Muons Pt and Eta (no requirements on muons)
      hMuonPt->Fill(myMuonPt);
      hMuonEta->Fill(myMuonEta);
      hMuonPt_InnerTrack->Fill(myInnerTrackRef->pt());
      hMuonEta_InnerTrack->Fill(myInnerTrackRef->eta());
      hMuonPt_GlobalTrack->Fill(myGlobalTrackRef->pt());
      hMuonEta_GlobalTrack->Fill(myGlobalTrackRef->eta());

      // 1) Demand that the Muon is both a "GlobalMuon" And a "TrackerMuon"
      if( (!(*iMuon)->isGlobalMuon()) || (!(*iMuon)->isTrackerMuon()) ) continue;
      bMuonGlobalMuonOrTrkerMuon = true;

      // 2) Demand that the selected Muon Identification as defined in the python cfg is satisfied
      if( !((*iMuon)->muonID( fMuonSelection )) ) continue;
      bMuonSelection = true;
      
      // 3) NHits cuts (Trk, Pixel, Muon). There has to be at LEAST greater than 10 track hits.
      if ( myInnerTrackNTrkHits <= 10) continue;
      bMuonNTrkerHitsCut = true;

      if ( myInnerTrackNPixelHits < 1) continue;
      bMuonNPixelHitsCut = true;
      // std::cout << "myGlobalTrackNMuonHits = " << myGlobalTrackNMuonHits << std::endl;
      if(myMatchedSegments < 2) continue;
      bMuonNMuonlHitsCut = true;

      // 4) Global Track Chi Square / ndof must be less than 10
      if( (*iMuon)->normChi2() > 10) continue; 
      bMuonGlobalTrkChiSqCut = true;

      // 5) Impact Paremeter (d0) wrt beam spot < 0.02cm (applied to track from the inner tracker)
      double muonIp = std::abs((*iMuon)->dB());
      hMuonImpactParameter->Fill(muonIp);
      if (muonIp >= 0.02) continue; // This is the transverse IP w.r.t to beamline.
      bMuonImpactParCut = true;

      // 6) Check that muon has good PV (i.e diff between muon track at its vertex and the PV along the Z position < 1cm)
      if(fMuonApplyIpz) {
        if(primaryVertex.get() == 0)
          throw cms::Exception("LogicError") << "MuonApplyIpz is true, but got null primary vertex" << std::endl;
        if(std::abs(myInnerTrackRef->dz(primaryVertex->position())) < 1.0) continue; // This is the z-impact parameter w.r.t to selected primary vertex
        bMuonGoodPVCut = true;
      }
      output.fSelectedMuonsBeforeIsolationAndPtAndEtaCuts.push_back(*iMuon);
      
      // Store muons before isolation, but passing pt and eta cuts
      if (myMuonPt > fMuonPtCut && std::fabs(myMuonEta) < fMuonEtaCut)
        output.fSelectedMuonsBeforeIsolation.push_back(*iMuon);
      
      // 7) Relative Isolation
      /*(around cone of DeltaR = 0.3) < 0.15. 
      float myTrackIso =  (*iMuon)->trackIso(); // isolation cones are dR=0.3 
      float myEcalIso  =  (*iMuon)->ecalIso();  // isolation cones are dR=0.3 
      float myHcalIso  =  (*iMuon)->hcalIso();  // isolation cones are dR=0.3 
      float relIsol = ( myTrackIso + myEcalIso + myHcalIso )/(myMuonPt);
      // std::cout << "relIsol = " << (*iMuon).isolationR03().sumPt << "/" << myMuonPt << " = " << relIsol << std::endl;
      if( relIsol > 0.15 ) continue; 
      */
      // Delta beta corrected isolation
      double myChHadronIso      =  (*iMuon)->chargedHadronIso(); // isolation cones are dR=0.4
      double myNeutralHadronIso =  (*iMuon)->neutralHadronIso();  // isolation cones are dR=0.4
      double myPhotonIso        =  (*iMuon)->photonIso();  // isolation cones are dR=0.4
      double myPUChHadronIso    =  (*iMuon)->puChargedHadronIso();  // isolation cones are dR=0.4
      double myIsolation = myChHadronIso + std::max(myNeutralHadronIso + myPhotonIso - 0.5 * myPUChHadronIso, 0.0);
      double relIsol = myIsolation / myMuonPt;


      if (relIsol > 0.20) continue; // tight = 0.12; loose = 0.20


      bMuonRelIsolationR03Cut = true;
      output.fSelectedMuonsBeforePtAndEtaCuts.push_back(*iMuon);

      hMuonEta_identified->Fill(myMuonEta);

      // 8) Apply eta cut
      if (std::abs(myMuonEta) >= fMuonEtaCut) continue;
      bMuonEtaCut = true;
      myHighestMuonPtBeforePtCut = std::max(myHighestMuonPtBeforePtCut, myMuonPt);
      hMuonPt_identified_eta->Fill(myMuonPt);

      // 8) Apply Pt and Eta cut requirements

      if (myMuonPt < fMuonPtCut) continue;
      bMuonPtCut = true;
      output.fSelectedMuons.push_back(*iMuon);


      // If Muon survives all cuts (1->8) then it is considered an isolated Muon. Now find the max Muon Pt of such isolated muons.
      if (myMuonPt > myHighestMuonPt) {
	myHighestMuonPt  = myMuonPt;
	myHighestMuonEta = myMuonEta;
	// std::cout << "myHighestMuonPt = " << myHighestMuonPt << ", myHighestMuonEta = " << myHighestMuonEta << std::endl;
      } //eof: if (myMuonPt > myHighestMuonPt) {
      
      // Fill histos after Selection
      hMuonPt_AfterSelection->Fill(myMuonPt);
      hMuonEta_AfterSelection->Fill(myMuonEta);
      //      hMuonPt_InnerTrack_AfterSelection->Fill(myMuonPt);
      //      hMuonEta_InnerTrack_AfterSelection->Fill(myMuonEta);
      hMuonPt_GlobalTrack_AfterSelection->Fill(myGlobalTrackRef->pt());
      hMuonEta_GlobalTrack_AfterSelection->Fill(myGlobalTrackRef->eta());
     
      bool bMuonMatchingMCmuon = false;
      bool bMuonMatchingMCmuonFromW = false;

      // Selection purity from MC
      if(!iEvent.isRealData()) {
        for (size_t i=0; i < genParticles->size(); ++i){  
          const reco::Candidate & p = (*genParticles)[i];
          const reco::Candidate & muon = (**iMuon);
          int status = p.status();
          double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() , muon.p4() );
          if ( deltaR > 0.05 || status != 1) continue;
          int id = p.pdgId();
	  //	  std::cout << "matching part id " << id << std::endl;
          if ( abs(id) == 13 ) {
	    bMuonMatchingMCmuon = true;

	    std::vector<const reco::GenParticle*> mothers = getMothers(p);  
	    for(size_t d=0; d<mothers.size(); ++d) {
	      const reco::GenParticle dparticle = *mothers[d];
	      int idmother = dparticle.pdgId();
              if ( abs(idmother) == 24 ) {
                bMuonMatchingMCmuonFromW = true;
	      }
	    }

          }
	}

	if ( bMuonMatchingMCmuon ){
	  hMuonPt_matchingMCmuon->Fill(myMuonPt);
	  hMuonEta_matchingMCmuon->Fill(myMuonEta);
	  if ( bMuonMatchingMCmuonFromW  ){
	    hMuonPt_matchingMCmuonFromW->Fill(myMuonPt);
	    hMuonEta_matchingMCmuonFromW->Fill(myMuonEta);	    
	  }
	}
      }
    }
    //eof: for(pat::MuonCollection::const_iterator iMuon = myMuonHandle->begin(); iMuon != myMuonHandle->end(); ++iMuon) {
    // Fill histos after Selection

    // Order of if-sentences was corrected 27.10.2011 / LAW
    if(bMuonPresent) { // 0.1
      increment(fMuonSelectionSubCountMuonPresent);
      if(bMuonHasGlobalOrInnerTrk) { // 0.2
        increment(fMuonSelectionSubCountMuonHasGlobalOrInnerTrk);
        if(bMuonGlobalMuonOrTrkerMuon) { // 1
          increment(fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon); 
          if(bMuonSelection) { // 2
            increment(fMuonSelectionSubCountMuonSelection);
            if(bMuonNTrkerHitsCut) { // 3.1
              increment(fMuonSelectionSubCountNTrkerHitsCut);
              if(bMuonNPixelHitsCut) { // 3.2
                increment(fMuonSelectionSubCountNPixelHitsCut);
                if(bMuonNMuonlHitsCut) { // 3.3
                  increment(fMuonSelectionSubCountNMuonlHitsCut);
                  if(bMuonGlobalTrkChiSqCut) { // 4
                    increment(fMuonSelectionSubCountGlobalTrkChiSqCut);
                    if(bMuonImpactParCut) { // 5
                      increment(fMuonSelectionSubCountImpactParCut);
                      if(bMuonGoodPVCut || !fMuonApplyIpz) { // 6
                        increment(fMuonSelectionSubCountGoodPVCut);
                        if(bMuonRelIsolationR03Cut) { // 7
                          increment(fMuonSelectionSubCountRelIsolationR03Cut);
                          if(bMuonPtCut) { // 8.1
                            increment(fMuonSelectionSubCountPtCut);
                            if(bMuonEtaCut) { // 8.2
                              increment(fMuonSelectionSubCountEtaCut);
			      /*
                              if(bMuonMatchingMCmuon) { // 9
                                increment(fMuonSelectionSubCountMatchingMCmuon);
                                if(bMuonMatchingMCmuonFromW) { // 10
                                  increment(fMuonSelectionSubCountMatchingMCmuonFromW);
                                }
                              }
			      */
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    // Store the highest Muon Pt and Eta
    output.fSelectedMuonPt  = myHighestMuonPt;
    output.fSelectedMuonPtBeforePtCut = myHighestMuonPtBeforePtCut;
    output.fSelectedMuonEta = myHighestMuonEta;
    hNumberOfSelectedMuons->Fill(output.fSelectedMuons.size());
    // std::cout << "fSelectedMuonPt = " << fSelectedMuonsPt << ", fSelectedMuonsEta = " << fSelectedMuonsEta << std::endl;   
  }//eof: bool MuonSelection::MuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  
}//eof: namespace HPlus {
