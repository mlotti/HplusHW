#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "TVector3.h"

namespace HPlus {
  GlobalMuonVeto::Data::Data(const GlobalMuonVeto *globalMuonVeto, bool passedEvent):
    fGlobalMuonVeto(globalMuonVeto), fPassedEvent(passedEvent) {}
  GlobalMuonVeto::Data::~Data() {}

  GlobalMuonVeto::GlobalMuonVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fMuonCollectionName(iConfig.getUntrackedParameter<edm::InputTag>("MuonCollectionName")),
    fMuonSelection(iConfig.getUntrackedParameter<std::string>("MuonSelection")),
    fMuonPtCut(iConfig.getUntrackedParameter<double>("MuonPtCut")),
    fMuonEtaCut(iConfig.getUntrackedParameter<double>("MuonEtaCut")),
    fMuonApplyIpz(iConfig.getUntrackedParameter<bool>("MuonApplyIpz")),
    fGlobalMuonVetoCounter(eventCounter.addSubCounter("GlobalMuon Selection","GlobalMuonVeto")),
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
    fMuonIDSubCountOther(eventCounter.addSubCounter("GlobalMuon ID","Other")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("GlobalMuonVeto");
    
    hMuonPt = makeTH<TH1F>(myDir, "GlobalMuonPt", "GlobalMuonPt;isolated muon p_{T}, GeV/c;N_{muons} / 5 GeV/c", 80, 0., 400.);
    hMuonEta = makeTH<TH1F>(myDir, "GlobalMuonEta", "GlobalMuonEta;isolated muon #eta;N_{muons} / 0.1", 60, -3., 3.);
    hMuonPt_matchingMCmuon = makeTH<TH1F>(myDir, "GlobalMuonPtmatchingMCmuon", "GlobalMuonPtmatchingMCmuon", 400, 0., 400.);
    hMuonEta_matchingMCmuon = makeTH<TH1F>(myDir, "GlobalMuonEtamatchingMCmuon", "GlobalMuonEtamatchingMCmuon", 400, -3., 3.);
    hMuonPt_matchingMCmuonFromW = makeTH<TH1F>(myDir, "GlobalMuonPtmatchingMCmuonFromW", "GlobalMuonPtmatchingMCmuonFromW", 400, 0., 400.);
    hMuonEta_matchingMCmuonFromW = makeTH<TH1F>(myDir, "GlobalMuonEtamatchingMCmuonFromW", "GlobalMuonEtamatchingMCmuonFromW", 400, -3., 3.);
    hMuonPt_InnerTrack = makeTH<TH1F>(myDir, "GlobalMuonPt_InnerTrack", "GlobalMuonPt_InnerTrack", 100, 0., 400.);
    hMuonEta_InnerTrack = makeTH<TH1F>(myDir, "GlobalMuonEta_InnerTrack", "GlobalMuonEta_InnerTrack", 60, -3., 3.);
    hMuonPt_GlobalTrack = makeTH<TH1F>(myDir, "GlobalMuonPt_GlobalTrack", "GlobalMuonPt_GlobalTrack", 100, 0., 400.);
    hMuonEta_GlobalTrack = makeTH<TH1F>(myDir, "GlobalMuonEta_GlobalTrack", "GlobalMuonEta_GlobalTrack", 60, -3., 3.);
    hMuonPt_AfterSelection  = makeTH<TH1F>(myDir, "GlobalMuonPt_AfterSelection", "GlobalMuonPt_AfterSelection", 100, 0., 400.);
    hMuonEta_AfterSelection = makeTH<TH1F>(myDir, "GlobalMuonEta_AfterSelection", "GlobalMuonEta_AfterSelection", 60, -3., 3.);
    hMuonPt_InnerTrack_AfterSelection  = makeTH<TH1F>(myDir, "GlobalMuonPt_InnerTrack_AfterSelection", "GlobalMuonPt_InnerTrack_AfterSelection", 100, 0., 400.);
    hMuonEta_InnerTrack_AfterSelection = makeTH<TH1F>(myDir, "GlobalMuonEta_InnerTrack_AfterSelection", "GlobalMuonEta_InnerTrack_AfterSelection", 60, -3., 3.);
    hMuonPt_GlobalTrack_AfterSelection  = makeTH<TH1F>(myDir, "GlobalMuonPt_GlobalTrack_AfterSelection", "GlobalMuonPt_GlobalTrack_AfterSelection", 100, 0., 400.);
    hMuonEta_GlobalTrack_AfterSelection = makeTH<TH1F>(myDir, "GlobalMuonEta_GlobalTrack_AfterSelection", "GlobalMuonEta_GlobalTrack_AfterSelection", 60, -3., 3.);
    hMuonImpactParameter = makeTH<TH1F>(myDir, "MuonImpactParameter", "MuonImpactParameter", 100, 0., 0.1);
    hMuonZdiff = makeTH<TH1F>(myDir, "MuonZdiff", "MuonZdiff", 100, 0., 10.);
 
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

  GlobalMuonVeto::~GlobalMuonVeto() {}

  GlobalMuonVeto::Data GlobalMuonVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex) {
    // Reset data variables
    fSelectedMuonPt = -1.0;
    fSelectedMuonEta = -999.99;
    fSelectedMuons.clear();
    fSelectedMuonsBeforeIsolation.clear();

    // Get result
    bool passEvent = MuonSelection(iEvent,iSetup, primaryVertex);
    return Data(this, passEvent);
  }

  bool GlobalMuonVeto::MuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex){

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
    bool bMuonMatchingMCmuon = false;
    bool bMuonMatchingMCmuonFromW = false;
    
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
      // float myMuonPt  = myInnerTrackRef->pt();
      // float myMuonEta = myInnerTrackRef->eta();
      // float myMuonPhi = myInnerTrackRef->phi();
      float myMuonPt  = (*iMuon)->pt();
      float myMuonEta = (*iMuon)->eta();
      float myMuonPhi = (*iMuon)->phi();
      int myInnerTrackNTrkHits   = myInnerTrackRef->hitPattern().numberOfValidTrackerHits();
      int myInnerTrackNPixelHits = myInnerTrackRef->hitPattern().numberOfValidPixelHits();
      int myGlobalTrackNMuonHits  = myGlobalTrackRef->hitPattern().numberOfValidMuonHits(); 
      // Note: It is possible for a Global Muon to have zero muon hits. This happens because once the inner and outter tracks used to create
      // global fit to the muon track that covers all of the detector, hits that are incompatible to the new trajectory are removed 
      // (i.e. de-associated from the muon). This is the so called "outlier rejection". 
      // Note: For the Num

      // Fill histos with all-Muons Pt and Eta (no requirements on muons)
      hMuonPt->Fill(myMuonPt, fEventWeight.getWeight());
      hMuonEta->Fill(myMuonEta, fEventWeight.getWeight());
      hMuonPt_InnerTrack->Fill(myInnerTrackRef->pt(), fEventWeight.getWeight());
      hMuonEta_InnerTrack->Fill(myInnerTrackRef->eta(), fEventWeight.getWeight());
      hMuonPt_GlobalTrack->Fill(myGlobalTrackRef->pt(), fEventWeight.getWeight());
      hMuonEta_GlobalTrack->Fill(myGlobalTrackRef->eta(), fEventWeight.getWeight());

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
      if ( myGlobalTrackNMuonHits < 1) continue;
      bMuonNMuonlHitsCut = true;

      // 4) Global Track Chi Square / ndof must be less than 10
      if( (*iMuon)->normChi2() > 10) continue; 
      bMuonGlobalTrkChiSqCut = true;

      // 5) Impact Paremeter (d0) wrt beam spot < 0.02cm (applied to track from the inner tracker)
      // FIX ME
      // if ( myInnerTrackRef->dxy() < 0.02) continue; // This is the transverse IP w.r.t to (0,0,0). Replace latter with BeamSpot
      hMuonImpactParameter->Fill((*iMuon)->dB(),fEventWeight.getWeight()); 
      if ((*iMuon)->dB() > 0.02) continue; // This is the transverse IP w.r.t to beamline.
      bMuonImpactParCut = true;

      // 6) Check that muon has good PV (i.e diff between muon track at its vertex and the PV along the Z position < 1cm)
      if(fMuonApplyIpz) {
        if(primaryVertex.get() == 0)
          throw cms::Exception("LogicError") << "MuonApplyIpz is true, but got null primary vertex" << std::endl;
        if(std::abs(myInnerTrackRef->dz(primaryVertex->position())) < 1.0) continue; // This is the z-impact parameter w.r.t to selected primary vertex
        bMuonGoodPVCut = true;
      }

      fSelectedMuonsBeforeIsolation.push_back(*iMuon);

      // 7) Relative Isolation (around cone of DeltaR = 0.3) < 0.15. 
      float myTrackIso =  (*iMuon)->trackIso(); // isolation cones are dR=0.3 
      float myEcalIso  =  (*iMuon)->ecalIso();  // isolation cones are dR=0.3 
      float myHcalIso  =  (*iMuon)->hcalIso();  // isolation cones are dR=0.3 
      float relIsol = ( myTrackIso + myEcalIso + myHcalIso )/(myMuonPt);
      // std::cout << "relIsol = " << (*iMuon).isolationR03().sumPt << "/" << myMuonPt << " = " << relIsol << std::endl;
      if( relIsol > 0.15 ) continue; 
      // No muon isolation
      //      if( relIsol > 99999. ) continue;
      bMuonRelIsolationR03Cut = true;

      fSelectedMuons.push_back(*iMuon);

      // 8) Apply Pt and Eta cut requirements
      if (myMuonPt < fMuonPtCut) continue;
      bMuonPtCut = true;

      if (std::fabs(myMuonEta) > fMuonEtaCut) continue;
      bMuonEtaCut = true;
      
      // If Muon survives all cuts (1->8) then it is considered an isolated Muon. Now find the max Muon Pt of such isolated muons.
      if (myMuonPt > myHighestMuonPt) {
	myHighestMuonPt  = myMuonPt;
	myHighestMuonEta = myMuonEta;
	// std::cout << "myHighestMuonPt = " << myHighestMuonPt << ", myHighestMuonEta = " << myHighestMuonEta << std::endl;
      } //eof: if (myMuonPt > myHighestMuonPt) {
      
      // Fill histos after Selection
      hMuonPt_AfterSelection->Fill(myMuonPt, fEventWeight.getWeight());
      hMuonEta_AfterSelection->Fill(myMuonPt, fEventWeight.getWeight());
      hMuonPt_InnerTrack_AfterSelection->Fill(myMuonPt, fEventWeight.getWeight());
      hMuonEta_InnerTrack_AfterSelection->Fill(myMuonEta, fEventWeight.getWeight());
      hMuonPt_GlobalTrack_AfterSelection->Fill(myGlobalTrackRef->pt(), fEventWeight.getWeight());
      hMuonEta_GlobalTrack_AfterSelection->Fill(myGlobalTrackRef->eta(), fEventWeight.getWeight());
     

      // Selection purity from MC
      if(!iEvent.isRealData()) {
        for (size_t i=0; i < genParticles->size(); ++i){  
          const reco::Candidate & p = (*genParticles)[i];
          const reco::Candidate & muon = (**iMuon);
          int status = p.status();
          double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() , muon.p4() );
          if ( deltaR > 0.05 || status != 1) continue;
          bMuonMatchingMCmuon = true;
          hMuonPt_matchingMCmuon->Fill(myMuonPt, fEventWeight.getWeight());
          hMuonEta_matchingMCmuon->Fill(myMuonEta, fEventWeight.getWeight());
          int id = p.pdgId();
          if ( abs(id) == 13 ) {
            int numberOfTauMothers = p.numberOfMothers(); 
            for (int im=0; im < numberOfTauMothers; ++im){  
              const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
              if ( !dparticle) continue;
              int idmother = dparticle->pdgId();
              if ( abs(idmother) == 24 ) {
                bMuonMatchingMCmuonFromW = true;
                hMuonPt_matchingMCmuonFromW->Fill(myMuonPt, fEventWeight.getWeight());
                hMuonEta_matchingMCmuonFromW->Fill(myMuonEta, fEventWeight.getWeight());
              }
            }
          }
        }
      }



    }//eof: for(pat::MuonCollection::const_iterator iMuon = myMuonHandle->begin(); iMuon != myMuonHandle->end(); ++iMuon) {
  
    if(bMuonPresent) {
      increment(fMuonSelectionSubCountMuonPresent);
      if(bMuonHasGlobalOrInnerTrk) {
        increment(fMuonSelectionSubCountMuonHasGlobalOrInnerTrk);
        if(bMuonPtCut) {
          increment(fMuonSelectionSubCountPtCut);
          if(bMuonEtaCut) {
            increment(fMuonSelectionSubCountEtaCut);
            if(bMuonGlobalMuonOrTrkerMuon) {
              increment(fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon); 
              if(bMuonSelection) {
                increment(fMuonSelectionSubCountMuonSelection);
                if(bMuonNTrkerHitsCut) {
                  increment(fMuonSelectionSubCountNTrkerHitsCut);
                  if(bMuonNPixelHitsCut) {
                    increment(fMuonSelectionSubCountNPixelHitsCut);
                    if(bMuonNMuonlHitsCut) {
                      increment(fMuonSelectionSubCountNMuonlHitsCut);
                      if(bMuonGlobalTrkChiSqCut) {
                        increment(fMuonSelectionSubCountGlobalTrkChiSqCut);
                        if(bMuonImpactParCut) {
                          increment(fMuonSelectionSubCountImpactParCut);
                          if(bMuonRelIsolationR03Cut) {
                            increment(fMuonSelectionSubCountRelIsolationR03Cut);
                            if(bMuonGoodPVCut) {
                              increment(fMuonSelectionSubCountGoodPVCut);
			      if(bMuonMatchingMCmuon) {
				increment(fMuonSelectionSubCountMatchingMCmuon);
				if(bMuonMatchingMCmuonFromW) {
				  increment(fMuonSelectionSubCountMatchingMCmuonFromW);
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
      }
    }

    // Make a boolean that describes whether a Global Muon (passing all selection criteria) is found.
    bool bDecision = bMuonPresent*bMuonHasGlobalOrInnerTrk*bMuonPtCut*bMuonEtaCut*bMuonGlobalMuonOrTrkerMuon*bMuonSelection*bMuonNTrkerHitsCut*bMuonNPixelHitsCut*bMuonNMuonlHitsCut*bMuonGlobalTrkChiSqCut*bMuonImpactParCut*bMuonRelIsolationR03Cut;
    if(fMuonApplyIpz)
      bDecision = bDecision && bMuonGoodPVCut;

    // Now store the highest Muon Pt and Eta
    fSelectedMuonPt  = myHighestMuonPt;
    fSelectedMuonEta = myHighestMuonEta;
    // std::cout << "fSelectedMuonPt = " << fSelectedMuonsPt << ", fSelectedMuonsEta = " << fSelectedMuonsEta << std::endl;

    // If a Global Muon (passing all selection criteria) is found, do not increment counter. Return false.
    if(bDecision) return false;
    // Otherwise increment counter and return true.
    else increment(fGlobalMuonVetoCounter);
    return true;
    
  }//eof: bool GlobalMuonVeto::MuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  
}//eof: namespace HPlus {
