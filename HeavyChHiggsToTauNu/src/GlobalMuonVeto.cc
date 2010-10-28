#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "TH1F.h"
#include "TH2F.h"

namespace HPlus {

  GlobalMuonVeto::GlobalMuonVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fMuonCollectionName(iConfig.getUntrackedParameter<edm::InputTag>("MuonCollectionName")),
    fMuonSelection(iConfig.getUntrackedParameter<std::string>("MuonSelection")),
    fMuonPtCut(iConfig.getUntrackedParameter<double>("MuonPtCut")),
    fMuonEtaCut(iConfig.getUntrackedParameter<double>("MuonEtaCut")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
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
    hMuonPt_InnerTrack = fs->make<TH1F>("GlobalMuonPt_InnerTrack", "GlobalMuonPt_InnerTrack", 400, 0., 400.);
    hMuonEta_InnerTrack = fs->make<TH1F>("GlobalMuonEta_InnerTrack", "GlobalMuonEta_InnerTrack", 60, -3., 3.);
    hMuonPt_GlobalTrack = fs->make<TH1F>("GlobalMuonPt_GlobalTrack", "GlobalMuonPt_GlobalTrack", 400, 0., 400.);
    hMuonEta_GlobalTrack = fs->make<TH1F>("GlobalMuonEta_GlobalTrack", "GlobalMuonEta_GlobalTrack", 60, -3., 3.);
    hMuonPt_InnerTrack_AfterSelection  = fs->make<TH1F>("GlobalMuonPt_InnerTrack_AfterSelection", "GlobalMuonPt_InnerTrack_AfterSelection", 400, 0., 400.);
    hMuonEta_InnerTrack_AfterSelection = fs->make<TH1F>("GlobalMuonEta_InnerTrack_AfterSelection", "GlobalMuonEta_InnerTrack_AfterSelection", 60, -3., 3.);
    hMuonPt_GlobalTrack_AfterSelection  = fs->make<TH1F>("GlobalMuonPt_GlobalTrack_AfterSelection", "GlobalMuonPt_GlobalTrack_AfterSelection", 400, 0., 400.);
    hMuonEta_GlobalTrack_AfterSelection = fs->make<TH1F>("GlobalMuonEta_GlobalTrack_AfterSelection", "GlobalMuonEta_GlobalTrack_AfterSelection", 60, -3., 3.);
  }

  GlobalMuonVeto::~GlobalMuonVeto() {}

  bool GlobalMuonVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

    if( fMuonSelection == "All" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "AllGlobalMuons" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "AllStandAloneMuons" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "AllTrackerMuons" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TrackerMuonArbitrated" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "AllArbitrated" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "GlobalMuonPromptTight" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationLoose" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationTight" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMOneStationLoose" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationOptimizedLowPtLoose" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationOptimizedLowPtTight" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "GMTkChiCompatibility" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "GMTkKinkTight" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationAngLoose" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationAngTight" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationOptimizedBarrelLowPtLoose" ) return MuonSelection(iEvent,iSetup); 
    else if( fMuonSelection == "TMLastStationOptimizedBarrelLowPtTight" ) return MuonSelection(iEvent,iSetup); 
    else{
      throw cms::Exception("Error") << "The MuonSelection \"" << fMuonSelection << "\" used as input in the python config file is invalid! Please choose one of the following valid options:\n All, AllGlobalMuons, AllStandAloneMuons, AllTrackerMuons, TrackerMuonArbitrated, AllArbitrated, GlobalMuonPromptTight, TMLastStationLoose, TMLastStationTight, TMOneStationLoose, TMLastStationOptimizedLowPtLoose, TMLastStationOptimizedLowPtTight, GMTkChiCompatibility, GMTkKinkTight, TMLastStationAngLoose, TMLastStationAngTight, TMLastStationOptimizedBarrelLowPtLoose, TMLastStationOptimizedBarrelLowPtTight.\n" << std::endl;
      return true;
    }
  }

  bool GlobalMuonVeto::MuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    /// the Collection is currently NOT available in the PatTuples but it will be soon (next pattuple production)
    /* FIX ME
    /// Create and attach handle to (Offline) Primary Vertices Collection
    edm::Handle<std::vector<reco::Vertex> > primaryVerticesHandle;
    //    edm::Handle<reco::VertexCollection> primaryVerticesHandle;
    iEvent.getByLabel("offlinePrimaryVertices", primaryVerticesHandle);
    /// Create an XYZ position to store the Primary Vertex
    math::XYZPoint PVPosition;

    /// Loop over all PV's. PV's are stored with decending Event Pt (PV candidate with highest associated Evt Trk Pt is stored first)
    for(unsigned int iPV = 0; iPV < primaryVerticesHandle->size(); ++iPV) {
      /// Get PV candidate
      reco::Vertex myPV = primaryVerticesHandle->at(iPV);
      /// Apply some quality to the PV candidate: a) PV is not fake, b) has more than 4 normalised degrees of freedom, 
      /// c) has a z position less than 15 cm, and d) distance in the XY plane less than 2 cm.
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
    /// Get beam spot
    edm::Handle<reco::BeamSpot> BeamSpotHandle;
    iEvent.getByLabel(beamSpotCollection, BeamSpotHandle);
    const reco::BeamSpot *myBeamSpot = BeamSpotHandle.product();
    const math::XYZPoint myBeamSpotPosition = myBeamSpot->position();
    impactParameter = fabs( (*iMuon)->innerTrack()->dxy(myBeamSpotPosition) );
    impactParameter = fabs( (*iElectron)->gsfTrack()->dxy(myBeamSpotPosition) );
    FIX ME */ 


    /// Create and attach handle to Muon Collection
    edm::Handle<std::vector<pat::Muon> > myMuonHandle;
    iEvent.getByLabel(fMuonCollectionName, myMuonHandle);
    
    /// In the case where the handle is empty...
    if ( !myMuonHandle->size() ){
      // std::cout << "Muon handle for '" << fMuonCollectionName << " is empty!" << std::endl;
    }

    /// Reset/initialise variables
    float myHighestMuonPt = -1;
    float myHighestMuonEta = -999.99;
    fSelectedMuonsPt = -1.0;
    fSelectedMuonsEta = -999.99;
    /// 
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
    
    /// Loop over all Muons
    for(pat::MuonCollection::const_iterator iMuon = myMuonHandle->begin(); iMuon != myMuonHandle->end(); ++iMuon) {

      /// Keep track of the muons analyzed
      bMuonPresent = true;
      increment(fMuonIDSubCountAllMuonCandidates);
      
      /// Keep track of the MuonID's. Just for my information
      if( (*iMuon).isGood("All") ) increment(fMuonIDSubCountAll);
      if( (*iMuon).isGood("AllGlobalMuons") ) increment(fMuonIDSubCountAllGlobalMuons);
      if( (*iMuon).isGood("AllStandAloneMuons") ) increment(fMuonIDSubCountAllStandAloneMuons);
      if( (*iMuon).isGood("AllTrackerMuons") ) increment(fMuonIDSubCountAllTrackerMuons);  
      if( (*iMuon).isGood("TrackerMuonArbitrated") ) increment(fMuonIDSubCountTrackerMuonArbitrated);
      if( (*iMuon).isGood("AllArbitrated") ) increment(fMuonIDSubCountAllArbitrated);
      if( (*iMuon).isGood("GlobalMuonPromptTight")  ) increment(fMuonIDSubCountGlobalMuonPromptTight);  
      if( (*iMuon).isGood("TMLastStationLoose") ) increment(fMuonIDSubCountTMLastStationLoose); 
      if( (*iMuon).isGood("TMLastStationTight") ) increment(fMuonIDSubCountTMLastStationTight); 
      if( (*iMuon).isGood("TMOneStationLoose") ) increment(fMuonIDSubCountTMOneStationLoose);   
      if( (*iMuon).isGood("TMLastStationOptimizedLowPtLoose") ) increment(fMuonIDSubCountTMLastStationOptimizedLowPtLoose);  
      if( (*iMuon).isGood("TMLastStationOptimizedLowPtTight") ) increment(fMuonIDSubCountTMLastStationOptimizedLowPtTight);
      if( (*iMuon).isGood("GMTkChiCompatibility") ) increment(fMuonIDSubCountGMTkChiCompatibility);  
      if( (*iMuon).isGood("GMTkKinkTight") ) increment(fMuonIDSubCountGMTkKinkTight); 
      if( (*iMuon).isGood("TMLastStationAngLoose") ) increment(fMuonIDSubCountTMLastStationAngLoose); 
      if( (*iMuon).isGood("TMLastStationAngTight") ) increment(fMuonIDSubCountTMLastStationAngTight); 
      if( (*iMuon).isGood("TMLastStationOptimizedBarrelLowPtLoose") ) increment(fMuonIDSubCountTMLastStationOptimizedBarrelLowPtLoose);
      if( (*iMuon).isGood("TMLastStationOptimizedBarrelLowPtTight") ) increment(fMuonIDSubCountTMLastStationOptimizedBarrelLowPtTight);
      else{
	increment(fMuonIDSubCountOther);
      }

      /// Obtain reference to a Muon track
      reco::TrackRef myGlobalTrackRef = (*iMuon).globalTrack();
      reco::TrackRef myInnerTrackRef = (*iMuon).innerTrack(); // inner tracks give best resolution for muons with Pt up to 200 GeV/c

      /// Check that track was found.
      if ( myInnerTrackRef.isNull() || myGlobalTrackRef.isNull() ){
	// std::cout << "myInnerTrackRef.isNull()" << std::endl;
	// std::cout << "(*iMuon).isStandAloneMuon() = " << (*iMuon).isStandAloneMuon() << std::endl;
	// std::cout << "(*iMuon).isGlobalMuon() = " << (*iMuon).isGlobalMuon() << std::endl;
	// std::cout << "(*iMuon).isTrackerMuon() = " << (*iMuon).isTrackerMuon() << std::endl;
	// std::cout << "(*iMuon).isCaloMuon() = " << (*iMuon).isCaloMuon() << std::endl;
	continue; 
      }
      bMuonHasGlobalOrInnerTrk = true;
      
      /// Fill histos with all-Muons Pt and Eta (no requirements on muons)
      hMuonPt_InnerTrack->Fill(myInnerTrackRef->pt());
      hMuonEta_InnerTrack->Fill(myInnerTrackRef->eta());
      hMuonPt_GlobalTrack->Fill(myGlobalTrackRef->pt());
      hMuonEta_GlobalTrack->Fill(myGlobalTrackRef->eta());

      /// Muon Variables (Pt, Eta etc..)
      float myMuonPt = myInnerTrackRef->pt();
      float myMuonEta = myInnerTrackRef->eta();
      int myInnerTrackNTrkHits   = myInnerTrackRef->hitPattern().numberOfValidTrackerHits();
      int myInnerTrackNPixelHits = myInnerTrackRef->hitPattern().numberOfValidPixelHits();
      int myInnerTrackNMuonHits  = myInnerTrackRef->hitPattern().numberOfValidMuonHits();

      /// 1) Apply Pt and Eta cut requirements
      if (myMuonPt < fMuonPtCut) continue;
      bMuonPtCut = true;

      if ( fabs(myMuonEta) > fMuonEtaCut) continue;
      bMuonEtaCut = true;
      
      /// 2) Demand that the Muon is both a "GlobalMuon" And a "TrackerMuon"
      if( (!(*iMuon).isGlobalMuon()) || (!(*iMuon).isTrackerMuon()) ) continue;
      bMuonGlobalMuonOrTrkerMuon = true;

      /// 3) Demand that the selected Muon Identification as defined in the python cfg is satisfied
      if( (*iMuon).isGood( fMuonSelection ) ) continue;
      bMuonSelection = true;
      
      /// 4) NHits cuts (Trk, Pixel, Muon)
      if ( myInnerTrackNTrkHits < 10) continue;
      bMuonNTrkerHitsCut = true;

      if ( myInnerTrackNPixelHits < 1) continue;
      bMuonNPixelHitsCut = true;
      
      if ( myInnerTrackNMuonHits < 1) continue;
      bMuonNMuonlHitsCut = true;

      /// 5) Global Track Chi Square / ndof must be less than 10
      if( (*iMuon).normChi2() < 10) continue; 
      bMuonGlobalTrkChiSqCut = true;

      /// 6) Impact Paremeter (d0) wrt beam spot < 0.02cm (applied to track from the inner tracker)
      /// FIX ME
      if ( myInnerTrackRef->dxy() < 0.02) continue; /// This is the transverse impact parameter w.r.t to (0,0,0). Replace latter with BeamSpot
      bMuonImpactParCut = true;
      
      /// 7) Relative Isolation (around cone of DeltaR = 0.3) < 0.15. 
      float relIsol = ( (*iMuon).isolationR03().sumPt )/myMuonPt;
      std::cout << "relIsol = " << (*iMuon).isolationR03().sumPt << "/" << myMuonPt << " = " << relIsol << std::endl;
      if( ( relIsol < 3.0) )continue; 
      bMuonRelIsolationR03Cut = true;

      /// 8) Check that muon has good PV (i.e diff between muon track at its vertex and the PV along the Z position < 1cm)
      /// FIX ME
      if ( fabs(myInnerTrackRef->dz()) < 1.0) continue; /// This is the z-impact parameter w.r.t to (0,0,0). Replace latter with BeamSpot
      bMuonGoodPVCut = true;      

      
      /// If Muon survives all cuts (1->8) then it is considered an isolated Muon. Now find the max Muon Pt of such isolated muons.
      if (myMuonPt > myHighestMuonPt) {
	myHighestMuonPt  = myMuonPt;
	myHighestMuonEta = myMuonEta;
	fSelectedMuonsPt  = myMuonPt;
	fSelectedMuonsEta = myMuonEta;
      } //eof: if (myMuonPt > myHighestMuonPt) {
      
      /// Fill histos after Selection
      hMuonPt_InnerTrack_AfterSelection->Fill(myMuonPt);
      hMuonEta_InnerTrack_AfterSelection->Fill(myMuonPt);
      hMuonPt_GlobalTrack_AfterSelection->Fill(myGlobalTrackRef->pt());
      hMuonEta_GlobalTrack_AfterSelection->Fill(myGlobalTrackRef->eta());

    }//eof: for(pat::MuonCollection::const_iterator iMuon = myMuonHandle->begin(); iMuon != myMuonHandle->end(); ++iMuon) {
  
    if(bMuonPresent) increment(fMuonSelectionSubCountMuonPresent);
    
    if(bMuonHasGlobalOrInnerTrk) increment(fMuonSelectionSubCountMuonHasGlobalOrInnerTrk);
    
    if(bMuonPtCut) increment(fMuonSelectionSubCountPtCut);
    
    if(bMuonEtaCut) increment(fMuonSelectionSubCountEtaCut);
    
    if(bMuonGlobalMuonOrTrkerMuon) increment(fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon); 
    
    if(bMuonSelection) increment(fMuonSelectionSubCountMuonSelection);
    
    if(bMuonNTrkerHitsCut) increment(fMuonSelectionSubCountNTrkerHitsCut);
    
    if(bMuonNPixelHitsCut) increment(fMuonSelectionSubCountNPixelHitsCut);
    
    if(bMuonNMuonlHitsCut) increment(fMuonSelectionSubCountNMuonlHitsCut);
    
    if(bMuonGlobalTrkChiSqCut) increment(fMuonSelectionSubCountGlobalTrkChiSqCut);
    
    if(bMuonImpactParCut) increment(fMuonSelectionSubCountImpactParCut);
    
    if(bMuonRelIsolationR03Cut) increment(fMuonSelectionSubCountRelIsolationR03Cut);
    
    if(bMuonGoodPVCut) increment(fMuonSelectionSubCountGoodPVCut);

    /// Make a boolean that describes whether a Global Muon (passing all selection criteria) is found.
    bool bDecision = bMuonPresent*bMuonHasGlobalOrInnerTrk*bMuonPtCut*bMuonEtaCut*bMuonGlobalMuonOrTrkerMuon*bMuonSelection*bMuonNTrkerHitsCut*bMuonNPixelHitsCut*bMuonNMuonlHitsCut*bMuonGlobalTrkChiSqCut*bMuonImpactParCut*bMuonRelIsolationR03Cut*bMuonGoodPVCut;

    /// If a Global Muon (passing all selection criteria) is found, do not increment counter. Return false.
    if(bDecision) return false;
    /// Otherwise increment counter and return true.
    else increment(fGlobalMuonVetoCounter);
    return true;
    
  }//eof: bool GlobalMuonVeto::MuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  
}//eof: namespace HPlus {
