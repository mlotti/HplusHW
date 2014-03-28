#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"
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

namespace HPlus {
  MuonSelection::Data::Data():
    fSelectedMuonPt(0.),
    fSelectedMuonEta(0.),
    fSelectedMuonPtBeforePtCut(0.),
    fHasMuonFromCjetStatus(false),
    fHasMuonFromBjetStatus(false) {}
  MuonSelection::Data::~Data() {}

  MuonSelection::MuonSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fGenParticleSrc(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
    fMuonCollectionName(iConfig.getUntrackedParameter<edm::InputTag>("MuonCollectionName")),
    fApplyMuonIsolation(iConfig.getUntrackedParameter<bool>("applyMuonIsolation")),
    fMuonPtCut(iConfig.getUntrackedParameter<double>("MuonPtCut")),
    fMuonEtaCut(iConfig.getUntrackedParameter<double>("MuonEtaCut")),
    fMuonSelectionSubCountAllEvents(eventCounter.addSubCounter("MuonSelection","AllEvent")),
    fMuonSelectionSubCountMuonPresent(eventCounter.addSubCounter("MuonSelection","Muon present")),
    fMuonSelectionSubCountMuonHasGlobalOrInnerTrk(eventCounter.addSubCounter("MuonSelection","Muon has Global OR Inner Trk")),
    fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon(eventCounter.addSubCounter("MuonSelection","Global OR Tracker Muon")),
    fMuonSelectionSubCountPFMuonSelection(eventCounter.addSubCounter("MuonSelection","PF muon passed")),
    fMuonSelectionSubCountNTrkerHitsCut(eventCounter.addSubCounter("MuonSelection","Muon NTrkerHits")),
    fMuonSelectionSubCountNPixelHitsCut(eventCounter.addSubCounter("MuonSelection","Muon NPixelHits")),
    fMuonSelectionSubCountNMuonlHitsCut(eventCounter.addSubCounter("MuonSelection","Muon NMuonlHits")),
    fMuonSelectionSubCountGlobalTrkChiSqCut(eventCounter.addSubCounter("MuonSelection","Muon GlobalTrkChiSq")),
    fMuonSelectionSubCountImpactParCut(eventCounter.addSubCounter("MuonSelection","Muon ImpactPar")),
    fMuonSelectionSubCountGoodPVCut(eventCounter.addSubCounter("MuonSelection","Muon GoodPV")),
    fMuonSelectionSubCountRelIsolationCut(eventCounter.addSubCounter("MuonSelection","Muon RelIsolation")),
    fMuonSelectionSubCountEtaCut(eventCounter.addSubCounter("MuonSelection","Muon Eta")),
    fMuonSelectionSubCountPtCut(eventCounter.addSubCounter("MuonSelection","Muon Pt")),
    fMuonSelectionSubCountVetoMuonFound(eventCounter.addSubCounter("MuonSelection","Veto muon found")),
    fMuonSelectionSubCountMatchingMCmuon(eventCounter.addSubCounter("MuonSelection","Muon matching MC Muon")),
    fMuonSelectionSubCountMatchingMCmuonFromW(eventCounter.addSubCounter("MuonSelection","Muon matching MC Muon From W")),
    fMuonSelectionSubCountTightMuonFound(eventCounter.addSubCounter("MuonSelection","Tight muon found")),
    fMuonSelectionSubCountMuonVetoPassed(eventCounter.addSubCounter("MuonSelection","Muon veto passed")),
    fMuonSelectionSubCountPassedVetoAndMuonFromCjet(eventCounter.addSubCounter("MuonSelection", "Muon veto passed and mu in c jet")),
    fMuonSelectionSubCountPassedVetoAndMuonFromBjet(eventCounter.addSubCounter("MuonSelection", "Muon veto passed and mu in b jet"))

  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = histoWrapper.mkdir(HistoWrapper::kInformative, *fs, "MuonSelection");
    
    hTightMuonEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightMuonEta", "TightMuonEta;Tight muon #eta;N_{muons} / 0.1", 60, -3., 3.);
    hTightMuonPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightMuonPt", "TightMuonPt;Tight muon p_{T}, GeV/c;N_{muons} / 5 GeV/c", 80, 0., 400.);
    hLooseMuonEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "LooseMuonEta", "LooseMuonEta;Loose muon #eta;N_{muons} / 0.1", 60, -3., 3.);
    hLooseMuonPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "LooseMuonPt", "LooseMuonPt;Loose muon p_{T}, GeV/c;N_{muons} / 5 GeV/c", 80, 0., 400.);
    hNumberOfTightMuons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfTightMuons", "NumberOfTightMuons", 30, 0., 30.);
    hNumberOfLooseMuons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfLooseMuons", "NumberOfLooseMuons", 30, 0., 30.);
    hMuonPt_matchingMCmuon = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPtmatchingMCmuon", "MuonPtmatchingMCmuon", 80, 0., 400.);
    hMuonEta_matchingMCmuon = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEtamatchingMCmuon", "MuonEtamatchingMCmuon", 60, -3., 3.);
    hMuonPt_matchingMCmuonFromW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPtmatchingMCmuonFromW", "MuonPtmatchingMCmuonFromW", 80, 0., 400.);
    hMuonEta_matchingMCmuonFromW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEtamatchingMCmuonFromW", "MuonEtamatchingMCmuonFromW", 60, -3., 3.);
    hMuonPt_BeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPt_BeforeIsolation", "MuonPt_BeforeIsolation;muon p_{T} before isol., GeV/c;N_{muons} / 5 GeV/c", 80, 0., 400.);
    hMuonEta_BeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEta_BeforeIsolation", "MuonEta_BeforeIsolation;muon #eta before isol.;N_{muons} / 0.1", 60, -3., 3.);
    hMuonPt_InnerTrack_BeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPt_InnerTrack_BeforeIsolation", "MuonPt_InnerTrack_BeforeIsolation", 80, 0., 400.);
    hMuonEta_InnerTrack_BeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEta_InnerTrack_BeforeIsolation", "MuonEta_InnerTrack_BeforeIsolation", 60, -3., 3.);
    hMuonPt_GlobalTrack_BeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPt_GlobalTrack_BeforeIsolation", "MuonPt_GlobalTrack_BeforeIsolation", 80, 0., 400.);
    hMuonEta_GlobalTrack_BeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEta_GlobalTrack_BeforeIsolation", "MuonEta_GlobalTrack_BeforeIsolation", 60, -3., 3.);
    hMuonPt_AfterSelection  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPt_AfterSelection", "MuonPt_AfterSelection", 80, 0., 400.);
    hMuonEta_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEta_AfterSelection", "MuonEta_AfterSelection", 60, -3., 3.);
    //    hMuonPt_InnerTrack_AfterSelection  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPt_InnerTrack_AfterSelection", "MuonPt_InnerTrack_AfterSelection", 100, 0., 400.);
    //    hMuonEta_InnerTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEta_InnerTrack_AfterSelection", "MuonEta_InnerTrack_AfterSelection", 60, -3., 3.);
    hMuonPt_GlobalTrack_AfterSelection  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonPt_GlobalTrack_AfterSelection", "MuonPt_GlobalTrack_AfterSelection", 100, 0., 400.);
    hMuonEta_GlobalTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonEta_GlobalTrack_AfterSelection", "MuonEta_GlobalTrack_AfterSelection", 60, -3., 3.);
    hMuonTransverseImpactParameter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonTransverseImpactParameter", "MuonTransverseImpactParameter;#mu IP_{T} / mm", 100, 0., 2);
    hMuonDeltaIPz = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonDeltaIPz", "MuonDeltaIPz;|IP_{z}-PV_{z}| / cm;N_{muons}", 100, 0., 10.);
    hMuonRelIsol = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuonRelIsol", "MuonRelIsol;#mu Rel.Isol. #Delta#beta;N_{muons}", 120, 0., 1.2);

    hMuonEtaPhiForSelectedMuons = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
        "MuonEtaPhiForSelectedMuons", "MuonEtaPhiForSelectedMuons;#mu #eta; #mu #phi",
        60, -3.0, 3.0, 72, -3.14159265, 3.14159265);
    hMCMuonEtaPhiForPassedEvents = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
        "MCMuonEtaPhiForPassedEvents", "MCMuonEtaPhiForPassedEvents;MC #mu #eta; MC #mu #phi",
        60, -3.0, 3.0, 72, -3.14159265, 3.14159265);

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
    return output;
  }

  void MuonSelection::doMuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex, MuonSelection::Data& output){
    // Create and attach handle to Muon Collection
    edm::Handle<edm::View<pat::Muon> > myMuonHandle;
    iEvent.getByLabel(fMuonCollectionName, myMuonHandle);    
    edm::PtrVector<pat::Muon> muons = myMuonHandle->ptrVector();
    increment(fMuonSelectionSubCountAllEvents);

    edm::Handle <edm::View<reco::GenParticle> > genParticles;
    iEvent.getByLabel(fGenParticleSrc, genParticles);

    // Reset/initialise variables
    float myHighestMuonPt = -1.0;
    float myHighestMuonPtBeforePtCut = -1.0;
    float myHighestMuonEta = -999.99;
    //
    bool bMuonPresent = false;
    bool bMuonHasGlobalOrInnerTrk = false;
    bool bMuonGlobalMuonOrTrkerMuon = false;
    bool bMuonSelection = false;
    bool bMuonNTrkerHitsCut = false;
    bool bMuonNPixelHitsCut = false;
    bool bMuonNMuonlHitsCut = false;
    bool bMuonGlobalTrkChiSqCut = false;
    bool bMuonImpactParCut = false;
    bool bMuonRelIsolationCut = false;
    bool bMuonGoodPVCut = false;
    bool bMuonEtaCut = false;
    bool bMuonPtCut = false;
    bool bMuonMatchingMCmuon = false;
    bool bMuonMatchingMCmuonFromW = false;

    // Cache MC muons to speed up code (only one loop over gen particles)
    std::vector<const reco::GenParticle*> myMCMuons;
    if(!iEvent.isRealData()) {
      for (size_t i=0; i < genParticles->size(); ++i){  
        if ((*genParticles)[i].status() != 1) continue;
        if (std::abs((*genParticles)[i].pdgId()) != 13) continue;
        myMCMuons.push_back(&((*genParticles)[i]));
      }
    }

    // Loop over all Muons
    for(edm::PtrVector<pat::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {
      // Keep track of the muons analyzed
      bMuonPresent = true;

      // Obtain reference to a Muon track
      reco::TrackRef myGlobalTrackRef = (*iMuon)->globalTrack();
      reco::TrackRef myInnerTrackRef = (*iMuon)->innerTrack(); // inner tracks give best resolution for muons with Pt up to 200 GeV/c

      // Check that track was found.
      if ( myInnerTrackRef.isNull() || myGlobalTrackRef.isNull() ) continue;
      bMuonHasGlobalOrInnerTrk = true;

      // Muon Variables (Pt, Eta etc..)
      float myMuonPt  = (*iMuon)->pt();
      float myMuonEta = (*iMuon)->eta();
      //int myInnerTrackNTrkHits   = myInnerTrackRef->hitPattern().numberOfValidTrackerHits();
      int myInnerTrackNPixelHits = myInnerTrackRef->hitPattern().numberOfValidPixelHits();
      //int myGlobalTrackNMuonHits  = myGlobalTrackRef->hitPattern().numberOfValidMuonHits(); 
      //int myMatchedSegments = (*iMuon)->numberOfMatches();
      // Note: It is possible for a Global Muon to have zero muon hits. This happens because once the inner and outter tracks used to create
      // global fit to the muon track that covers all of the detector, hits that are incompatible to the new trajectory are removed 
      // (i.e. de-associated from the muon). This is the so called "outlier rejection". 

      // 1) Demand that the Muon is both a "GlobalMuon" And a "TrackerMuon"
      if (!((*iMuon)->isGlobalMuon())) continue;
      bMuonGlobalMuonOrTrkerMuon = true;

      // 2) Demand that the selected Muon Identification as defined in the python cfg is satisfied
      // disabled because it is not in the list in the approved objects page
      //if( !((*iMuon)->muonID( fMuonSelection )) ) continue;
      // from 4_4_0 onwards available check for PF muon
      if (!(*iMuon)->isPFMuon()) continue;
      bMuonSelection = true;

      // 3) NHits cuts (Trk, Pixel, Muon)
      if (!(myGlobalTrackRef->hitPattern().trackerLayersWithMeasurement() > 5)) continue;
      bMuonNTrkerHitsCut = true;

      if ( myInnerTrackNPixelHits < 1) continue;
      bMuonNPixelHitsCut = true;

      // Suppress punch through and decay of muons in flight
      if (!(myGlobalTrackRef->hitPattern().numberOfValidMuonHits() > 0)) continue;

      // std::cout << "myGlobalTrackNMuonHits = " << myGlobalTrackNMuonHits << std::endl;
      if (!((*iMuon)->numberOfMatchedStations() > 1)) continue;
      bMuonNMuonlHitsCut = true;

      // 4) Global Track Chi Square / ndof must be less than 10
      if( (*iMuon)->normChi2() > 10) continue; 
      bMuonGlobalTrkChiSqCut = true;

      // 5) Transverse impact paremeter (d0) wrt beam spot < 0.2 cm (applied to track from the inner tracker)
      double muonIp = std::abs((*iMuon)->dB());
      hMuonTransverseImpactParameter->Fill(muonIp);
      if (muonIp >= 0.2) continue; // This is the transverse IP w.r.t to beamline.
      bMuonImpactParCut = true;

      // 6) Check that muon IPz is compatible with PVz
      // remove for 2011, but enable for 2012
      if (primaryVertex.isNull())
        throw cms::Exception("LogicError") << "MuonApplyIpz is true, but got null primary vertex" << std::endl;
      double myDeltaIPz = std::fabs((*iMuon)->muonBestTrack()->dz(primaryVertex->position()));
      hMuonDeltaIPz->Fill(myDeltaIPz);
      if (myDeltaIPz > 0.5) continue; // This is the z-impact parameter w.r.t to selected primary vertex
      bMuonGoodPVCut = true;
      
      // Fill histos with all-Muons Pt and Eta (no requirements on muons)
      hMuonPt_BeforeIsolation->Fill(myMuonPt);
      hMuonEta_BeforeIsolation->Fill(myMuonEta);
      hMuonPt_InnerTrack_BeforeIsolation->Fill(myInnerTrackRef->pt());
      hMuonEta_InnerTrack_BeforeIsolation->Fill(myInnerTrackRef->eta());
      hMuonPt_GlobalTrack_BeforeIsolation->Fill(myGlobalTrackRef->pt());
      hMuonEta_GlobalTrack_BeforeIsolation->Fill(myGlobalTrackRef->eta());

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
      hMuonRelIsol->Fill(relIsol);

      if(myMuonPt >= fMuonPtCut && std::abs(myMuonEta) < fMuonEtaCut)
        output.fSelectedMuonsBeforeIsolation.push_back(*iMuon);

      // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Basline_muon_selections_for_2011
      if (fApplyMuonIsolation) {
        if (relIsol < 0.12) {
          hTightMuonEta->Fill(myMuonEta);
          if (std::abs(myMuonEta) < fMuonEtaCut)
            hTightMuonPt->Fill(myMuonPt);
        }
        if (relIsol > 0.20) {
          output.fSelectedNonIsolatedMuons.push_back(*iMuon);
          continue;
        }
      }
      bMuonRelIsolationCut = true;
      output.fSelectedMuonsBeforePtAndEtaCuts.push_back(*iMuon);

      // 8) Apply eta cut
      hLooseMuonEta->Fill(myMuonEta);
      if (std::abs(myMuonEta) >= fMuonEtaCut) continue;
      bMuonEtaCut = true;

      // 9) Apply pT cut 
      myHighestMuonPtBeforePtCut = std::max(myHighestMuonPtBeforePtCut, myMuonPt);
      hLooseMuonPt->Fill(myMuonPt);

      if (myMuonPt < fMuonPtCut) continue;
      bMuonPtCut = true;
      output.fSelectedMuonsLoose.push_back(*iMuon);
      if (relIsol < 0.12 || !fApplyMuonIsolation)
        output.fSelectedMuonsTight.push_back(*iMuon);


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
      hMuonEtaPhiForSelectedMuons->Fill((*iMuon)->eta(), (*iMuon)->phi());

      // Selection purity from MC
      if(!iEvent.isRealData()) {
        for (size_t i=0; i < myMCMuons.size(); ++i){
          const reco::Candidate & p = *(myMCMuons[i]);
          const reco::Candidate & muon = (**iMuon);
          double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() , muon.p4() );
          if (deltaR > 0.05) continue;
	  //	  std::cout `<< "matching part id " << id << std::endl;
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

    if(bMuonPresent) increment(fMuonSelectionSubCountMuonPresent);
    if(bMuonHasGlobalOrInnerTrk) increment(fMuonSelectionSubCountMuonHasGlobalOrInnerTrk);
    if(bMuonGlobalMuonOrTrkerMuon) increment(fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon); 
    if(bMuonSelection) increment(fMuonSelectionSubCountPFMuonSelection);
    if(bMuonNTrkerHitsCut) increment(fMuonSelectionSubCountNTrkerHitsCut);
    if(bMuonNPixelHitsCut) increment(fMuonSelectionSubCountNPixelHitsCut);
    if(bMuonNMuonlHitsCut) increment(fMuonSelectionSubCountNMuonlHitsCut);
    if(bMuonGlobalTrkChiSqCut) increment(fMuonSelectionSubCountGlobalTrkChiSqCut);
    if(bMuonImpactParCut) increment(fMuonSelectionSubCountImpactParCut);
    if(bMuonGoodPVCut) increment(fMuonSelectionSubCountGoodPVCut);
    if(bMuonRelIsolationCut) increment(fMuonSelectionSubCountRelIsolationCut);
    if(bMuonPtCut) increment(fMuonSelectionSubCountPtCut);
    if(bMuonEtaCut) increment(fMuonSelectionSubCountEtaCut);
    if (!output.passedMuonVeto()) increment(fMuonSelectionSubCountVetoMuonFound);
    if(bMuonMatchingMCmuon) increment(fMuonSelectionSubCountMatchingMCmuon);
    if(bMuonMatchingMCmuonFromW) increment(fMuonSelectionSubCountMatchingMCmuonFromW);
    if (output.foundTightMuon()) increment(fMuonSelectionSubCountTightMuonFound);
    if (output.passedMuonVeto()) increment(fMuonSelectionSubCountMuonVetoPassed);

    // Store the highest Muon Pt and Eta
    output.fSelectedMuonPt  = myHighestMuonPt;
    output.fSelectedMuonPtBeforePtCut = myHighestMuonPtBeforePtCut;
    output.fSelectedMuonEta = myHighestMuonEta;
    hNumberOfTightMuons->Fill(output.fSelectedMuonsTight.size());
    hNumberOfLooseMuons->Fill(output.fSelectedMuonsLoose.size());

    // Look further at MC muons
    if(!iEvent.isRealData()) {
      for (size_t i=0; i < myMCMuons.size(); ++i) {
        const reco::Candidate & p = (*genParticles)[i];
        if (p.pt() < fMuonPtCut) continue;
        // Plot eta-phi map of MC muons above pT threshold if event passed muon veto
        if (output.passedMuonVeto())
          hMCMuonEtaPhiForPassedEvents->Fill(p.eta(), p.phi());
        if (std::fabs(p.eta()) > fMuonEtaCut) continue;
        // Check if there are MC muons in the acceptance coming from b or c quarks
        const reco::Candidate* pmother = p.mother();
        while (pmother) {
          if (std::abs(pmother->pdgId()) == 4)
            output.fHasMuonFromBjetStatus = true;
          else if (std::abs(pmother->pdgId()) == 5)
            output.fHasMuonFromCjetStatus = true;
          // move to next
          pmother = pmother->mother();
        }
      }
    }

    if (output.passedMuonVeto()) {
      if (output.eventContainsMuonFromCJet())
        increment(fMuonSelectionSubCountPassedVetoAndMuonFromCjet);
      if (output.eventContainsMuonFromBJet())
        increment(fMuonSelectionSubCountPassedVetoAndMuonFromBjet);
    }

  }
}
