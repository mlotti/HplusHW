#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include <string>
#include "TH1F.h"
#include "TH2F.h"

namespace HPlus {

  GlobalElectronVeto::GlobalElectronVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fElecCollectionName(iConfig.getUntrackedParameter<edm::InputTag>("ElectronCollectionName")),
    fElecSelection(iConfig.getUntrackedParameter<std::string>("ElectronSelection")),
    fElecPtCut(iConfig.getUntrackedParameter<double>("ElectronPtCut")),
    fElecEtaCut(iConfig.getUntrackedParameter<double>("ElectronEtaCut")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fElecSelectionSubCountElectronPresent(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Present")),
    fElecSelectionSubCountElectronHasGsfTrkOrTrk(eventCounter.addSubCounter("GlobalElectron Selection", "Electron has gsfTrack or track")),
    fElecSelectionSubCountPtCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Pt")),
    fElecSelectionSubCountEtaCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Eta")),
    fElecSelectionSubCountNLostHitsInTrkerCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Num of Lost Hits In Trker")),
    fElecSelectionSubCountmyElectronDeltaCotThetaCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Delta Cot(Theta)")),
    fElecSelectionSubCountmyElectronDistanceCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Distance (r-phi)")),
    fElecSelectionSubCountTransvImpactParCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Transverse Impact Parameter")),
    fElecSelectionSubCountDeltaRFromGlobalOrTrkerMuonCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron DeltaR From Global OrTrker Muon")),
    fElecSelectionSubCountRelIsolationR03Cut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron RelIsolationR03")),
    fElecIDSubCountAllElectronCandidates(eventCounter.addSubCounter("GlobalElectron ID", "All Electron Candidates")),
    fElecIDSubCountElecIDdLoose(eventCounter.addSubCounter("GlobalElectron ID", "eidLoose only")),
    fElecIDSubCountElecIDRobustLoose(eventCounter.addSubCounter("GlobalElectron ID", "eidRobustLoose only")),
    fElecIDSubCountElecIDTight(eventCounter.addSubCounter("GlobalElectron ID", "eidTight only")),
    fElecIDSubCountElecIDRobustTight(eventCounter.addSubCounter("GlobalElectron ID", "eidRobustTight only")),
    fElecIDSubCountElecIDRobustHighEnergy(eventCounter.addSubCounter("GlobalElectron ID", "eidRobustHighEnergy only")),
    fElecIDSubCountElecNoID(eventCounter.addSubCounter("GlobalElectron ID", "No ID")),
    fElecIDSubCountElecAllIDs(eventCounter.addSubCounter("GlobalElectron ID", "All IDs")),
    fElecIDSubCountOther(eventCounter.addSubCounter("GlobalElectron ID", "Other (multiple IDs)"))
  {
    edm::Service<TFileService> fs;
    hElectronPt  = fs->make<TH1F>("GlobalElectronPt", "GlobalElectronPt", 400, 0.0, 400.0);
    hElectronEta = fs->make<TH1F>("GlobalElectronEta", "GlobalElectronEta", 60, -3.0, 3.0);
    hElectronPt_gsfTrack  = fs->make<TH1F>("GlobalElectronPt_gsfTrack", "GlobalElectronPt_gsfTrack", 400, 0.0, 400.0);
    hElectronEta_gsfTrack = fs->make<TH1F>("GlobalElectronEta_gsfTrack", "GlobalElectronEta_gsfTrack", 60, -3.0, 3.0);
    hElectronPt_AfterSelection = fs->make<TH1F>("GlobalElectronPt_AfterSelection", "GlobalElectronPt_AfterSelection", 400, 0.0, 400.0);
    hElectronEta_AfterSelection = fs->make<TH1F>("GlobalElectronPt_AfterSelection", "GlobalElectronPt_AfterSelection", 60, -3.0, 3.0);
    hElectronPt_gsfTrack_AfterSelection = fs->make<TH1F>("GlobalElectronPt_gsfTrack_AfterSelection", "GlobalElectronPt_gsfTrack_AfterSelection", 400, 0.0, 400.0);
    hElectronEta_gsfTrack_AfterSelection = fs->make<TH1F>("GlobalElectronPt_gsfTrack_AfterSelection", "GlobalElectronPt_gsTrack_AfterSelection", 60, -3.0, 3.0);
  }

  GlobalElectronVeto::~GlobalElectronVeto() {}

  bool GlobalElectronVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

    if(fElecSelection == "kNoElectronIdentification")      return ElectronSelection(iEvent,iSetup);
    else if(fElecSelection == "kRobustElectronIdentification")  return ElectronSelection(iEvent,iSetup);
    else if(fElecSelection == "kLooseElectronIdentification")  return ElectronSelection(iEvent,iSetup);
    else if(fElecSelection == "kTightElectronIdentification")   return ElectronSelection(iEvent,iSetup);
    else{
      throw cms::Exception("Error") << "The ElectronSelection \"" << fElecSelection << "\" used as input in the python config file is invalid! Please choose one of the following valid options:\n kNoElectronIdentification, kRobustElectronIdentification, kLooseElectronIdentification, kTightElectronIdentification.\n" << std::endl;
      return true;
    }
  }
  
  bool GlobalElectronVeto::ElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup){
    
    /// Create and attach handle to Electron Collection
    edm::Handle<std::vector<pat::Electron> > myElectronHandle;
    iEvent.getByLabel(fElecCollectionName, myElectronHandle);

    /// Create and attach handle to All Tracks collection
    edm::Handle<reco::TrackCollection> myTracksHandle;
    iEvent.getByLabel("generalTracks", myTracksHandle);

    /// Create and attach handle to Muon Collection [Needed for Selection of Electrons - Requirement 5) ]
    edm::Handle<std::vector<pat::Muon> > myMuonHandle;
    iEvent.getByLabel("selectedPatMuons", myMuonHandle); /// Select muon id as GlobalMuonPromptTight?

    /// Get the Magnetic Field 
    /// FIXME: Use scale Current<->BField scale factor. see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/ConversionBackgroundRejection
    edm::ESHandle<MagneticField> myMagneticFieldESHandle;
    iSetup.get<IdealMagneticFieldRecord>().get(myMagneticFieldESHandle);
    double myBFieldInZAtZeroZeroZero = myMagneticFieldESHandle->inTesla(GlobalPoint(0.0,0.0,0.0)).z();
    // double myBFieldInZAtOneOneOne = myMagneticFieldESHandle->inTesla(GlobalPoint(1.0,1.0,1.0)).z();

    /* FIX ME
    /// Get beam spot
    edm::Handle<reco::BeamSpot> BeamSpotHandle;
    iEvent.getByLabel("offlineBeamSpot", BeamSpotHandle);
    const reco::BeamSpot *myBeamSpot = BeamSpotHandle.product();
    const math::XYZPoint myBeamSpotPosition = myBeamSpot->position();
    // float impactParameter = fabs( (*iElectron)->gsfTrack()->dxy(myBeamSpotPosition) );
    FIX ME */
    
    /// In the case where the Electron Collection handle is empty...
    if ( !myElectronHandle->size() ){
      // std::cout << "Electron handle for '" << fElecCollectionName << " is empty!" << std::endl;
    }
    
    /// Reset/initialise variables
    float myHighestElecPt = -1.0;
    float myHighestElecEta = -999.99;
    fSelectedElectronsPt = -1.0;
    fSelectedElectronsEta = -999.99;
    ///
    bool bElecPresent = false;
    bool bElecHasGsfTrkOrTrk = false;
    bool bElecPtCut = false;
    bool bElecEtaCut = false;
    bool bElecSelection = false; // if will use eID
    bool bElecNLostHitsInTrkerCut = false;
    bool bElecElectronDeltaCotThetaCut = false;
    bool bElecElectronDistanceCut = false;
    bool bElecRelIsolationR03Cut = false;
    bool bElecTransvImpactParCut = false;
    bool bElecDeltaRFromGlobalOrTrkerMuonCut = false;
    
    /// Loop over all Electrons
    for(pat::ElectronCollection::const_iterator iElectron = myElectronHandle->begin(); iElectron != myElectronHandle->end(); ++iElectron) {

      /// For Photon Conversion Rejection (Searching for the partner conversion track in the GeneralTrack Collection
      ConversionFinder convFinder;
      ConversionInfo convInfo = convFinder.getConversionInfo(*iElectron, myTracksHandle, myBFieldInZAtZeroZeroZero );
      /// Define the minimal distance in r-phi plane between the electron and its closest opposite sign track. DeltaR > 0.02
      double myElectronDistance = convInfo.dist();
      /// Define the minimal distance between the electron and its closest opposite sign track |Delta cot(Theta) | > 0.02
      double myElectronDeltaCotTheta = convInfo.dcot();
      double convradius = convInfo.radiusOfConversion();
      math::XYZPoint convPoint = convInfo.pointOfConversion();
      
      /// keep track of the electrons analyzed
      bElecPresent = true;
      increment(fElecIDSubCountAllElectronCandidates);

      /// Uncomment the piece of code below to cout all eID and result on current electron candidate
      /* 
      const std::vector<pat::Electron::IdPair>& myElectronIDs = (*iElectron).electronIDs();
      int myPairs = myElectronIDs.size();
      /// Loop over all tags to see which ones were satisfied
      for (int i = 0; i < myPairs; ++i) {
	std::string myElecIDtag = myElectronIDs[i].first;
	float myElecIDresult = myElectronIDs[i].second;
	std::cout << "idtag=" << myElecIDtag << ", result=" << myElecIDresult << std::endl;
      }//eof: for (int i = 0; i < myPairs; ++i) {
      */

      ///  Keep track of the ElectronID's. Just for my information
      bool bElecIDIsLoose = false;
      bool bElecIDIsRobustLoose = false;
      bool bElecIDIsTight = false;
      bool bElecIDIsRobustTight = false;
      bool bElecIDIsRobustHighEnergy = false;
      bool bElecNoID = false;
      bool bElecAllIDs = false;
      bool bMyElectronIDSelection = false; // put this as true according to your selection (if any used). CURRENTLY NOT USED
      if( (*iElectron).electronID("eidLoose") ) bElecIDIsLoose = true;
      if( (*iElectron).electronID("eidRobustLoose") ) bElecIDIsRobustLoose = true;
      if( (*iElectron).electronID("eidTight") ) bElecIDIsTight = true;
      if( (*iElectron).electronID("eidRobustTight") ) bElecIDIsRobustTight = true;
      if( (*iElectron).electronID("eidRobustHighEnergy") ) bElecIDIsRobustHighEnergy = true;
      else{
	// std::cout << "Other electron ID found..." << std::endl;
      }
      /// Now take care of eID counters
      if( (!bElecIDIsLoose) && (!bElecIDIsRobustLoose) && (!bElecIDIsTight) && (!bElecIDIsRobustTight) && (!bElecIDIsRobustHighEnergy) ){
	bElecNoID = true;
	increment(fElecIDSubCountElecNoID);}
      else if( (bElecIDIsLoose) && (bElecIDIsRobustLoose) && (bElecIDIsTight) && (bElecIDIsRobustTight) && (bElecIDIsRobustHighEnergy) ){
	bElecAllIDs = true;
	increment(fElecIDSubCountElecAllIDs);}
      else if( (bElecIDIsLoose) && (!bElecIDIsRobustLoose) && (!bElecIDIsTight) && (!bElecIDIsRobustTight) && (!bElecIDIsRobustHighEnergy) ){
	increment(fElecIDSubCountElecIDdLoose);}
      else if( (!bElecIDIsLoose) && (bElecIDIsRobustLoose) && (!bElecIDIsTight) && (!bElecIDIsRobustTight) && (!bElecIDIsRobustHighEnergy) ){
	increment(fElecIDSubCountElecIDRobustLoose);}
      else if( (!bElecIDIsLoose) && (!bElecIDIsRobustLoose) && (bElecIDIsTight) && (!bElecIDIsRobustTight) && (!bElecIDIsRobustHighEnergy) ){
	increment(fElecIDSubCountElecIDTight);}
      else if( (!bElecIDIsLoose) && (!bElecIDIsRobustLoose) && (!bElecIDIsTight) && (bElecIDIsRobustTight) && (!bElecIDIsRobustHighEnergy) ){
	increment(fElecIDSubCountElecIDRobustTight);}
      else if( (!bElecIDIsLoose) && (!bElecIDIsRobustLoose) && (!bElecIDIsTight) && (!bElecIDIsRobustTight) && (bElecIDIsRobustHighEnergy) ){
	increment(fElecIDSubCountElecIDRobustHighEnergy);}
      else if( (!bElecAllIDs) && (!bElecNoID) ){ increment(fElecIDSubCountOther);}
      else {
	// std::cout << "\n You forgot something !" << std::endl;
      }

      /// Obtain reference to an Electron track
      // reco::TrackRef myTrackRef = (*iElectron).track(); /// not in the pattuples 
      reco::GsfTrackRef myGsfTrackRef = (*iElectron).gsfTrack(); /// gsfElecs were selected to create the current PatTuples
      
      /// Check that track was found
      if (myGsfTrackRef.isNull()){
	// std::cout << "myGsfTrackRef.isNull()" << std::endl;
	continue;
      }
      bElecHasGsfTrkOrTrk = true;
      
      /// Electron Variables (Pt, Eta etc..)
      // float myElectronPt = myGsfTrackRef->pt();  // float myElectronPt = (*iElectron).p4().Pt();
      // float myElectronEta = myGsfTrackRef->eta();
      // float myElectronPhi = myGsfTrackRef->phi();
      float myElectronPt  = (*iElectron).pt();  // float myElectronPt = (*iElectron).p4().Pt();
      float myElectronEta = (*iElectron).eta();
      float myElectronPhi = (*iElectron).phi();
      float myTrackIso =  (*iElectron).dr03TkSumPt();
      float myEcalIso  =  (*iElectron).dr03EcalRecHitSumEt();
      float myHcalIso  =  (*iElectron).dr03HcalTowerSumEt();
      int iNLostHitsInTrker = myGsfTrackRef->hitPattern().numberOfLostHits();
      // float impactParameter = fabs( (*iElectron).gsfTrack()->dxy(myBeamSpotPosition) ); /// FIX ME?
      // float myTransverseImpactPar = fabs( (*iElectron).gsfTrack()->dxy() ); /// FIX ME?
      float myTransverseImpactPar = fabs( (*iElectron).dB() );  // This is the transverse IP w.r.t to beamline.
      float myRelativeIsolation = (myTrackIso + myEcalIso + myHcalIso)/(myElectronPt); // isolation cones are dR=0.3 

      /// Fill histos with all-Electrons Pt and Eta
      hElectronPt->Fill(myElectronPt);
      hElectronEta->Fill(myElectronEta);
      hElectronPt_gsfTrack->Fill(myGsfTrackRef->pt());
      hElectronEta_gsfTrack->Fill(myGsfTrackRef->eta());

      /// 1) Apply Pt and Eta cut requirements
      if (myElectronPt < fElecPtCut) continue;
      bElecPtCut = true;
      
      if (myElectronPt < fElecPtCut) continue;
      bElecEtaCut = true;
      
      /// 2) Validation of simple cut based eID (choose low efficiency => High Purity)
      
      /* FIX ME
      /// ?) Demand that the Electron passed the ? ID 
      // if(!bMyElectronIDSelection) continue;
      // bElecSelection = true; // if will use eID
      /// You can retrieve the value map decision very conveniently from the pat::Electron object as follows:
      std::cout << "Electron ID: 95relIso=" << myElec->electronID("simpleEleId95relIso")  
             << " 90relIso=" << myElec->electronID("simpleEleId90relIso") 
           << " 85relIso=" << myElec->electronID("simpleEleId85relIso") 
           << " 80relIso=" << myElec->electronID("simpleEleId80relIso") 
           << " 70relIso=" << myElec->electronID("simpleEleId70relIso") 
           << " 60relIso=" << myElec->electronID("simpleEleId60relIso")  << ...... <<
           << std::endl;
	   The value map returns a double with the following meaning:
	   
	   0: fails
	   1: passes electron ID only
	   2: passes electron Isolation only
	   3: passes electron ID and Isolation only
	   4: passes conversion rejection
	   5: passes conversion rejection and ID
	   6: passes conversion rejection and Isolation
	   7: passes the whole selection
	   
	   // std::cout << "(*iElectron).electronID(\"eidLoose\") = " << (*iElectron).electronID("eidLoose") << std::endl; /// FIX ME
	   FIX ME */

      /// 3) Photon conversion rejection (gamma->e+e-)
      /// If an electron has: |dist| < 0.02 && |delta cot(theta)| < 0.02 then it is regarded as coming from a conversion, and rejected
      /// a) Number of lost hits in the tracker
      if(iNLostHitsInTrker > 2) continue;
      bElecNLostHitsInTrkerCut = true;
      /// b) Minimal distance between the electron and its closest opposite sign track (|Delta cos(theta)|)
      if(myElectronDeltaCotTheta < 0.02) continue;
      bElecElectronDeltaCotThetaCut = true;
      /// c) Minimal distance between the electron and its closest opposite sign track in r-phi plane
      if( myElectronDistance < 0.02) continue;
      bElecElectronDistanceCut = true;

      /// 4) Transverse Impact Parameter wrt BeamSpot, applied on the gsfTrack of the Electron candidate
      if(myTransverseImpactPar > 0.04) continue;
      bElecTransvImpactParCut = true;
      
      /// 5) DeltaR between Electron candidate and any Global or Tracker Muonin the event whose number of hits in the inner tracker > 10
      /// Perform Muon Loop here to save cpu time
      float myElectronMuonDeltaR = 999.99;

      /// Loop over all Muons
      for(pat::MuonCollection::const_iterator iMuon = myMuonHandle->begin(); iMuon != myMuonHandle->end(); ++iMuon) {
	/// Check that there are muons present
	if(!myMuonHandle->size()){
	  continue;
	}
	
	/// Obtain reference to a Muon track
	reco::TrackRef myGlobalTrackRef = (*iMuon).globalTrack();
	reco::TrackRef myInnerTrackRef = (*iMuon).innerTrack(); // inner tracks give best resolution for muons with Pt up to 200 GeV/c

      /// Check that track was found for both Global AND Tracker Muons
      if ( myInnerTrackRef.isNull() || myGlobalTrackRef.isNull() ){
	continue; 
      }

      /// Muon Variables (Pt, Eta etc..)
      float myMuonPt = myInnerTrackRef->pt();
      float myMuonEta = myInnerTrackRef->eta();
      float myMuonPhi = myInnerTrackRef->phi();
      int myInnerTrackNTrkHits   = myInnerTrackRef->hitPattern().numberOfValidTrackerHits();
      
      /// Demand that the Muon is both a "GlobalMuon" And a "TrackerMuon"
      if( (!(*iMuon).isGlobalMuon()) || (!(*iMuon).isTrackerMuon()) ) continue;

      /// Demand Global or Tracker Muons to have at least 10 hits in the inner tracker
      if ( myInnerTrackNTrkHits < 10) continue;

      /// Calculate DeltaR between Electron candidate and Global or Tracker Muon
      myElectronMuonDeltaR = deltaR( myMuonEta, myMuonPhi,myElectronEta, myElectronPhi); 

    }//eof: for(pat::MuonCollection::const_iterator iMuon = myMuonHandle->begin(); iMuon != myMuonHandle->end(); ++iMuon) {
      if(myElectronMuonDeltaR < 0.1) continue;
      bElecDeltaRFromGlobalOrTrkerMuonCut = true;
      
      /// 6) Relative Isolation for Electron candidate
      if(myRelativeIsolation > 0.15) continue;
      bElecRelIsolationR03Cut = true;

      /// If Electron survives all cuts (1->6) then it is considered an isolated Electron. Now find the max Electron Pt.
      if (myElectronPt > myHighestElecPt) {
	myHighestElecPt = myElectronPt;
	myHighestElecEta = myElectronEta;
	// std::cout << "myHighestElecPt = " << myHighestElecPt << ", myHighestElecEta = " << myHighestElecEta << std::endl;
      }
      
      /// Fill histos after Selection
      hElectronPt_AfterSelection->Fill(myGsfTrackRef->pt());
      hElectronEta_AfterSelection->Fill(myGsfTrackRef->pt());
      hElectronPt_gsfTrack_AfterSelection->Fill(myGsfTrackRef->pt());
      hElectronEta_gsfTrack_AfterSelection->Fill(myGsfTrackRef->pt());
      
    }//eof: for(pat::ElectronCollection::const_iterator iElectron = myElectronHandle->begin(); iElectron != myElectronHandle->end(); ++iElectron) {
    // if(bElecSelection) increment(fElecSelectionSubCountElectronSelection);  // if will use eID
    
    if(bElecPresent) increment(fElecSelectionSubCountElectronPresent);

    if(bElecHasGsfTrkOrTrk) increment(fElecSelectionSubCountElectronHasGsfTrkOrTrk);
    
    if(bElecPtCut) increment(fElecSelectionSubCountPtCut);
    
    if(bElecEtaCut) increment(fElecSelectionSubCountEtaCut);
    
    if(bElecNLostHitsInTrkerCut) increment(fElecSelectionSubCountNLostHitsInTrkerCut);
    
    if(bElecElectronDeltaCotThetaCut) increment(fElecSelectionSubCountmyElectronDeltaCotThetaCut);
    
    if(bElecElectronDistanceCut) increment(fElecSelectionSubCountmyElectronDistanceCut);
    
    if(bElecTransvImpactParCut) increment(fElecSelectionSubCountTransvImpactParCut);
    
    if(bElecDeltaRFromGlobalOrTrkerMuonCut) increment(fElecSelectionSubCountDeltaRFromGlobalOrTrkerMuonCut);

    if(bElecRelIsolationR03Cut) increment(fElecSelectionSubCountRelIsolationR03Cut);
    
    /// Make a boolean that describes whether a Global Electron (passing all selection criteria) is found.
    bool bDecision = bElecPresent*bElecHasGsfTrkOrTrk*bElecPtCut*bElecEtaCut*bElecNLostHitsInTrkerCut*bElecElectronDeltaCotThetaCut*bElecElectronDistanceCut*bElecRelIsolationR03Cut*bElecTransvImpactParCut*bElecDeltaRFromGlobalOrTrkerMuonCut;

    /// Now store the highest Electron Pt and Eta
    fSelectedElectronsPt = myHighestElecPt;
    fSelectedElectronsEta = myHighestElecEta;
    // std::cout << "fSelectedElectronsPt = " << fSelectedElectronsPt << ", fSelectedElectronsEta = " << fSelectedElectronsEta << std::endl;
    
    /// If a Global Electron (passing all selection criteria) is found, do not increment counter. Return false.
    if(bDecision) return false;

    /// Otherwise increment counter and return true.
    else increment(fGlobalElectronVetoCounter);
    return true;
    
  }//eof: bool GlobalElectronVeto::ElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  
}//eof: namespace HPlus {
