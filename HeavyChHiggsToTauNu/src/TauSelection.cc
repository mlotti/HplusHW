#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TH1F.h"

namespace HPlus {
  TauSelection::Data::Data(const TauSelection *tauSelection, bool passedEvent):
    fTauSelection(tauSelection), fPassedEvent(passedEvent) {}
  TauSelection::Data::~Data() {}

  TauSelection::TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSelection(iConfig.getUntrackedParameter<std::string>("selection")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fLeadTrkPtCut(iConfig.getUntrackedParameter<double>("leadingTrackPtCut")),
    fRtauCut(iConfig.getUntrackedParameter<double>("rtauCut")),
    fInvMassCut(iConfig.getUntrackedParameter<double>("invMassCut")),
    fPtCutCount(eventCounter.addSubCounter("Tau main","Tau pt cut")),
    fEtaCutCount(eventCounter.addSubCounter("Tau main","Tau eta cut")),
    fagainstMuonCount(eventCounter.addSubCounter("Tau main","Tau againstMuon discriminator")),
    fagainstElectronCount(eventCounter.addSubCounter("Tau main","Tau againstElectron discriminator")),
    fLeadTrkPtCount(eventCounter.addSubCounter("Tau main","Tau leading track pt cut")),
    fTaNCCount(eventCounter.addSubCounter("Tau main","Tau TaNC cut")),
    fHPSIsolationCount(eventCounter.addSubCounter("Tau main","Tau HPS isolation cut")),
    fbyIsolationCount(eventCounter.addSubCounter("Tau main","Tau byIsolation discriminator")),
    fbyTrackIsolationCount(eventCounter.addSubCounter("Tau main","Tau byTrackIsolation cut")),
    fecalIsolationCount(eventCounter.addSubCounter("Tau main","Tau ecalIsolation discriminator")),
    fnProngsCount(eventCounter.addSubCounter("Tau main","Tau number of prongs cut")),
    fHChTauIDchargeCount(eventCounter.addSubCounter("Tau main","Tau charge cut")),
    fRtauCount(eventCounter.addSubCounter("Tau main","Tau Rtau cut")),
    fInvMassCount(eventCounter.addSubCounter("Tau main","Tau InvMass cut")),
    fAllSubCount(eventCounter.addSubCounter("Tau identification", "all tau candidates")),
    fPtCutSubCount(eventCounter.addSubCounter("Tau identification", "pt cut")),
    fEtaCutSubCount(eventCounter.addSubCounter("Tau identification", "eta cut")),
    fagainstMuonSubCount(eventCounter.addSubCounter("Tau identification","againstMuon discriminator")),
    fagainstElectronSubCount(eventCounter.addSubCounter("Tau identification","againstElectron discriminator")),
    fLeadTrkPtSubCount(eventCounter.addSubCounter("Tau identification", "leading track pt cut")),
    fbyTaNCSubCount(eventCounter.addSubCounter("Tau identification","Tau TaNC cut")),
    fbyHPSIsolationSubCount(eventCounter.addSubCounter("Tau identification","Tau HPS isolation cut")),
    fbyIsolationSubCount(eventCounter.addSubCounter("Tau identification", "byIsolation discriminator")),
    fbyTrackIsolationSubCount(eventCounter.addSubCounter("Tau identification", "byTrackIsolation cut")),
    fecalIsolationSubCount(eventCounter.addSubCounter("Tau identification", "ecalIsolation discriminator")),
    fnProngsSubCount(eventCounter.addSubCounter("Tau identification", "number of prongs cut")),
    fHChTauIDchargeSubCount(eventCounter.addSubCounter("Tau identification", "Tau charge cut")),
    fRtauSubCount(eventCounter.addSubCounter("Tau identification","Tau Rtau cut")),
    fInvMassSubCount(eventCounter.addSubCounter("Tau identification","Tau InvMass cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    hPt = makeTH<TH1F>(*fs, "tau_pt", "tau_pt", 100, 0., 200.);
    hEta = makeTH<TH1F>(*fs, "tau_eta", "tau_eta", 60, -3., 3.);
    hPtAfterTauSelCuts = makeTH<TH1F>(*fs, "tau_pt_afterTauSelCuts", "tau_pt_afterTauSelCuts", 100, 0., 200.);
    hEtaAfterTauSelCuts = makeTH<TH1F>(*fs, "tau_eta_afterTauSelCuts", "tau_eta_afterTauSelCuts", 60, -3., 3.);
    hEtaRtau = makeTH<TH1F>(*fs, "tau_eta_Rtau", "tau_eta_Rtau", 60, -3., 3.);
    hLeadTrkPt = makeTH<TH1F>(*fs, "tau_leadtrk_pt", "tau_leadtrk_pt", 100, 0., 100.);
    hIsolTrkPt = makeTH<TH1F>(*fs, "tau_isoltrk_pt", "tau_isoltrk_pt", 100, 0., 20.);
    hIsolTrkPtSum = makeTH<TH1F>(*fs, "tau_isoltrk_ptsum", "tau_isoltrk_ptsum", 100, 0., 20.);
    hIsolTrkPtSumVsPtCut = makeTH<TH2F>(*fs, "tau_isoltrk_ptsum_vs_ptcut", "tau_isoltrk_ptsum_vs_ptcut", 6, 0.45, 1.05, 100, 0., 20.);
    hNIsolTrksVsPtCut = makeTH<TH2F>(*fs, "tau_ntrks_vs_ptcut", "tau_ntrks_vs_ptcut", 6, 0.45, 1.05,10,0.,10.);
    hIsolMaxTrkPt = makeTH<TH1F>(*fs, "tau_isomaxltrk_pt", "tau_isolmaxtrk_pt", 100, 0., 20.);
    hnProngs = makeTH<TH1F>(*fs, "tau_nProngs", "tau_nProngs", 10, 0., 10.);
    hRtau = makeTH<TH1F>(*fs, "tau_Rtau", "tau_Rtau", 100, 0., 1.2);
    hDeltaE = makeTH<TH1F>(*fs, "tau_DeltaE", "tau_DeltaE", 100, 0., 1.);
    hFlightPathSignif = makeTH<TH1F>(*fs, "tau_lightPathSignif", "tau_lightPathSignif", 100, 0., 10);
    hInvMass = makeTH<TH1F>(*fs, "tau_InvMass", "tau_InvMass", 50, 0., 5.);
    hbyTaNC = makeTH<TH1F>(*fs, "tau_TaNC", "tau_TaNC", 100, 0., 1.);
    
    // Check that tauID algorithm selection is ok
    if     (fSelection == "CaloTauCutBased")             fTauIDType = kTauIDCaloTauCutBased;
    else if(fSelection == "ShrinkingConePFTauCutBased")  fTauIDType = kTauIDShrinkingConePFTauCutBased;
    else if(fSelection == "ShrinkingConePFTauTaNCBased") fTauIDType = kTauIDShrinkingConePFTauTaNCBased;
    else if(fSelection == "HPSTauBased")                 fTauIDType = kTauIDHPSTauBased;
    else throw cms::Exception("Error") << "TauSelection: no or unknown tau selection used! Options for 'selection' are: CaloTauCutBased, ShrinkingConePFTauCutBased, ShrinkingConePFTauTaNCBased, HPSTauBased" << std::endl;
  }

  TauSelection::~TauSelection() {}

  TauSelection::Data TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
    // Obtain tau collection from src specified in config
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);
    // Do selection
    if     (fTauIDType == kTauIDCaloTauCutBased)
      passEvent = selectionByTCTauCuts(iEvent,iSetup,htaus->ptrVector());
    else if(fTauIDType == kTauIDShrinkingConePFTauCutBased)
      passEvent = selectionByPFTauCuts(iEvent,iSetup,htaus->ptrVector());
    else if(fTauIDType == kTauIDShrinkingConePFTauTaNCBased)
      passEvent = selectionByPFTauTaNC(iEvent,iSetup,htaus->ptrVector());
    else if(fTauIDType == kTauIDHPSTauBased)
      passEvent = selectionByHPSTau(iEvent,iSetup,htaus->ptrVector());
    return Data(this, passEvent);
  }

  TauSelection::Data TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus) {
    bool passEvent = false;
    // Do selection
    if     (fTauIDType == kTauIDCaloTauCutBased)             passEvent = selectionByTCTauCuts(iEvent,iSetup,taus);
    else if(fTauIDType == kTauIDShrinkingConePFTauCutBased)  passEvent = selectionByPFTauCuts(iEvent,iSetup,taus);
    else if(fTauIDType == kTauIDShrinkingConePFTauTaNCBased) passEvent = selectionByPFTauTaNC(iEvent,iSetup,taus);
    else if(fTauIDType == kTauIDHPSTauBased)                 passEvent = selectionByHPSTau(iEvent,iSetup,taus);
    return Data(this, passEvent);
  }

  bool TauSelection::selectionByPFTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus){
    fSelectedTaus.clear();
    fSelectedTaus.reserve(taus.size());

    size_t ptCutPassed = 0;
    size_t etaCutPassed = 0;
    size_t leadTrkPtCutPassed = 0;
    size_t nProngsCutPassed = 0;
    size_t HChTauIDchargeCutPassed = 0;
    size_t byIsolationCutPassed = 0;
    size_t ecalIsolationCutPassed = 0;
    size_t againstElectronCutPassed = 0;
    size_t againstMuonCutPassed = 0;
    size_t RtauCutPassed = 0;
    size_t InvMassCutPassed = 0;

    // Fill initial histograms and do the first selection
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      edm::Ptr<pat::Tau> iTau = *iter;

      increment(fAllSubCount);

      hPt->Fill(iTau->pt(), fEventWeight.getWeight());
      hEta->Fill(iTau->eta(), fEventWeight.getWeight());
      reco::PFCandidateRef  leadTrk = iTau->leadPFChargedHadrCand(); 
      //      reco::TrackRef leadTrk = iTau->leadTrack();
      //      if(leadTrk.isNonnull())
      //        hLeadTrkPt->Fill(leadTrk->pt(), fEventWeight.getWeight());
      //      uint16_t nSigTk        =  thePFTauRef->signalPFChargedHadrCands().size();
      uint16_t nSigTracks        =  iTau->signalPFChargedHadrCands().size();


      if(!(iTau->pt() > fPtCut)) continue;
      increment(fPtCutSubCount);
      ++ptCutPassed;

      if(!(std::abs(iTau->eta()) < fEtaCut)) continue;
      increment(fEtaCutSubCount);
      ++etaCutPassed;

      if(iTau->tauID("againstMuon") < 0.5 ) continue; 
      increment(fagainstMuonSubCount);
      ++againstMuonCutPassed;

      if(iTau->tauID("againstElectron") < 0.5 ) continue; 
      increment(fagainstElectronSubCount);
      ++againstElectronCutPassed;

      if(leadTrk.isNonnull())
        hLeadTrkPt->Fill(leadTrk->pt(), fEventWeight.getWeight());

      if(leadTrk.isNull() || !(leadTrk->pt() > fLeadTrkPtCut)) continue;
      increment(fLeadTrkPtSubCount);
      ++leadTrkPtCutPassed;

 
     
      float ptmax = 0;
      float ptsum = 0;

      /*
      const reco::PFCandidateRefVector& isolCands = iTau->isolationPFChargedHadrCands();
      reco::PFCandidateRefVector::const_iterator iCand = isolCands.begin();
      //      const reco::TrackRefVector& isolCands = iTau->isolationTracks();
      //      reco::TrackRefVector::const_iterator iCand = isolCands.begin();
      //      std::cout << " isol cands " << isolCands.size() << std::endl;
      for(; iCand != isolCands.end(); ++iCand) {
	float pt = (*iCand)->pt();
	ptsum += pt; 
	if (pt > ptmax) ptmax = pt;
	hIsolTrkPt->Fill(pt, fEventWeight.getWeight());
	//	std::cout << " isol track pt " << pt << std::endl;
	//iCand->pt()
      }
      hIsolMaxTrkPt->Fill(ptmax, fEventWeight.getWeight());
      hIsolTrkPtSum->Fill(ptsum, fEventWeight.getWeight());

      for(int iCut = 0; iCut < 5; ++iCut){
	double cut = 0.5 + 0.1*iCut;
	double sum  = 0;
	int nTracks = 0;
	for(size_t iTr = 0; iTr < isolCands.size(); ++iTr) {
	  float pt = isolCands[iTr]->pt();
	  if(pt < cut) continue;
	  sum+=pt;
	  nTracks++;
	}
	hIsolTrkPtSumVsPtCut->Fill(cut,sum, fEventWeight.getWeight());
	hNIsolTrksVsPtCut->Fill(cut,float(nTracks), fEventWeight.getWeight());
      } 
      */
      
      if(iTau->tauID("byIsolation") < 0.5) continue; 
      increment(fbyIsolationSubCount);
      ++byIsolationCutPassed;

      if(iTau->tauID("ecalIsolation") < 0.5) continue; 
      increment(fecalIsolationSubCount);
      ++ecalIsolationCutPassed;

      //      std::cout << " signal trk  " << nSigTracks  <<  "  iTau->signalTracks().size()) "  <<  iTau->signalTracks().size() << std::endl;       
      hnProngs->Fill(nSigTracks, fEventWeight.getWeight());    
      //      if(iTau->tauID("HChTauID1Prong") < 0.5 && iTau->tauID("HChTauID3Prongs") < 0.5) continue; 
      if(iTau->tauID("HChTauID1Prong") < 0.5 ) continue; 
      //      if( nSigTracks != 1 ) continue; 
      increment(fnProngsSubCount);
      ++nProngsCutPassed;
 
      if(iTau->tauID("HChTauIDcharge") < 0.5) continue; 
      increment(fHChTauIDchargeSubCount);
      ++HChTauIDchargeCutPassed;
  
      //float Rtau = leadTrk->p()/iTau->p();
      //      Rtau = leadTrk->p()/iTau->p();
      //hRtau->Fill(Rtau, fEventWeight.getWeight());
    
      //float Rtau = 0;
      //if (iTau->p() > 0) leadTrk->p()/iTau->p();
      float Rtau = iTau->tauID("HChTauIDtauPolarizationCont");
      if (Rtau > 1 ) {
	hEtaRtau->Fill(iTau->eta(), fEventWeight.getWeight());
      }
      hRtau->Fill(Rtau, fEventWeight.getWeight());


      if(Rtau < fRtauCut) continue; 
      increment(fRtauSubCount);
      ++RtauCutPassed;
      
      float DeltaE = iTau->tauID("HChTauIDDeltaECont");
      hDeltaE->Fill(DeltaE, fEventWeight.getWeight());

      float flightPathSignif = iTau->tauID("HChTauIDFlightPathSignifCont");
      hFlightPathSignif->Fill(flightPathSignif, fEventWeight.getWeight());

      // DeltaE and flight path are not applied - why?
      // They should be applied for 3-prongs only

      float InvMass = iTau->tauID("HChTauIDInvMassCont");
      hInvMass->Fill(InvMass, fEventWeight.getWeight());
      //      continue;
     
      if(InvMass > fInvMassCut) continue;
      increment(fInvMassSubCount);
      ++InvMassCutPassed;


      // Fill Histos after Tau Selection Cuts
      hPtAfterTauSelCuts->Fill(iTau->pt(), fEventWeight.getWeight());
      hEtaAfterTauSelCuts->Fill(iTau->eta(), fEventWeight.getWeight());

      fSelectedTaus.push_back(iTau);
    }

    if(ptCutPassed == 0) return false;
    increment(fPtCutCount);

    if(etaCutPassed == 0) return false;      
    increment(fEtaCutCount);

    if(againstMuonCutPassed == 0) return false;      
    increment(fagainstMuonCount);

    if(againstElectronCutPassed == 0) return false;      
    increment(fagainstElectronCount);

    if(leadTrkPtCutPassed == 0) return false;
    increment(fLeadTrkPtCount);  
     
    if(byIsolationCutPassed == 0) return false;
    increment(fbyIsolationCount);
	
    if(ecalIsolationCutPassed == 0) return false;
    increment(fecalIsolationCount);

    if(nProngsCutPassed == 0) return false;
    increment(fnProngsCount);

    if(HChTauIDchargeCutPassed == 0) return false;
    increment(fHChTauIDchargeCount); 
       
    if(RtauCutPassed == 0) return false;
    increment(fRtauCount);
     
    if(InvMassCutPassed == 0) return false;
    increment(fInvMassCount);
    
    
//    if(fSelectedTaus.size() > 1)
//      return false;
    
    return true;
  }

  bool TauSelection::selectionByPFTauTaNC(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus){
	// NC input corresponds to isolation and mass 
	fSelectedTaus.clear();
	fSelectedTaus.reserve(taus.size());

	size_t againstElectronCutPassed = 0;
	size_t againstMuonCutPassed = 0;
	size_t ptCutPassed = 0;
    	size_t etaCutPassed = 0;
    	size_t leadTrkPtCutPassed = 0;
	size_t nProngsCutPassed = 0;
	size_t HChTauIDchargeCutPassed = 0;
	size_t byTaNCCutPassed = 0;
	size_t RtauCutPassed = 0;
	//size_t InvMassCutPassed = 0;

	for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
		edm::Ptr<pat::Tau> iTau = *iter;
		
		increment(fAllSubCount);
      		hPt->Fill(iTau->pt(), fEventWeight.getWeight());
      		hEta->Fill(iTau->eta(), fEventWeight.getWeight());

      		if(!(iTau->pt() > fPtCut)) continue;
      		increment(fPtCutSubCount);
      		++ptCutPassed;

      		if(!(std::abs(iTau->eta()) < fEtaCut)) continue;
      		increment(fEtaCutSubCount);
      		++etaCutPassed;

		//////////////////////////////////////////////////////////////////////

		if(iTau->tauID("againstMuon") < 0.5 ) continue;
      		increment(fagainstMuonSubCount);
      		++againstMuonCutPassed;

      		if(iTau->tauID("againstElectron") < 0.5 ) continue;
      		increment(fagainstElectronSubCount);
      		++againstElectronCutPassed;

      		reco::PFCandidateRef  leadTrk = iTau->leadPFChargedHadrCand();
      		if(leadTrk.isNonnull()) hLeadTrkPt->Fill(leadTrk->pt(), fEventWeight.getWeight());

      		if(leadTrk.isNull() || !(leadTrk->pt() > fLeadTrkPtCut)) continue;
      		increment(fLeadTrkPtSubCount);
      		++leadTrkPtCutPassed;

		hbyTaNC->Fill(iTau->tauID("byTaNC"), fEventWeight.getWeight());
		//		if(iTau->tauID("byTaNC") < 0.6) continue;
//		if(iTau->tauID("byTaNCfrQuarterPercent") < 0.5) continue;
		if(iTau->tauID("byTaNCfrTenthPercent") < 0.5) continue; // This is the tightest selection
//		if(iTau->tauID("byTaNCfrOnePercent") < 0.5) continue;
//		if(iTau->tauID("byTaNCfrHalfPercent") < 0.5) continue;
		increment(fbyTaNCSubCount);
		++byTaNCCutPassed;

		//       std::cout << " after isolation tanC " << std::endl;   

		hnProngs->Fill(iTau->signalTracks().size(), fEventWeight.getWeight());
		//		if(iTau->tauID("HChTauID1Prong") < 0.5 && iTau->tauID("HChTauID3Prongs") < 0.5) continue;
		if(iTau->tauID("HChTauID1Prong") < 0.5 ) continue;
		increment(fnProngsSubCount);
		++nProngsCutPassed;

		if(iTau->tauID("HChTauIDcharge") < 0.5) continue; 
		increment(fHChTauIDchargeSubCount);
		++HChTauIDchargeCutPassed;

		//float Rtau = 0;
		//if (iTau->p() > 0) leadTrk->p()/iTau->p();
		float Rtau = iTau->tauID("HChTauIDtauPolarizationCont");
		hRtau->Fill(Rtau, fEventWeight.getWeight());

		if(Rtau < fRtauCut) continue;
		increment(fRtauSubCount);
		++RtauCutPassed;

		float DeltaE = iTau->tauID("HChTauIDDeltaECont");
      		hDeltaE->Fill(DeltaE, fEventWeight.getWeight());

      		float flightPathSignif = iTau->tauID("HChTauIDFlightPathSignifCont");
      		hFlightPathSignif->Fill(flightPathSignif, fEventWeight.getWeight());

      		// Fill Histos after Tau Selection Cuts
      		hPtAfterTauSelCuts->Fill(iTau->pt(), fEventWeight.getWeight());
      		hEtaAfterTauSelCuts->Fill(iTau->eta(), fEventWeight.getWeight());

      		fSelectedTaus.push_back(iTau);
		float InvMass = iTau->tauID("HChTauIDInvMassCont");
		hInvMass->Fill(InvMass, fEventWeight.getWeight());
	}

    	if(ptCutPassed == 0) return false;
    	increment(fPtCutCount);

    	if(etaCutPassed == 0) return false;
    	increment(fEtaCutCount);

    	if(againstMuonCutPassed == 0) return false;
    	increment(fagainstMuonCount);

    	if(againstElectronCutPassed == 0) return false;
    	increment(fagainstElectronCount);

    	if(leadTrkPtCutPassed == 0) return false;
    	increment(fLeadTrkPtCount);

	if(byTaNCCutPassed == 0) return false;
	increment(fTaNCCount);

	if(nProngsCutPassed == 0) return false;
	increment(fnProngsCount);

	if(HChTauIDchargeCutPassed == 0) return false;
	increment(fHChTauIDchargeCount);       

    	if(RtauCutPassed == 0) return false;
    	increment(fRtauCount);

	return true;
  }

  bool TauSelection::selectionByHPSTau(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus){
        fSelectedTaus.clear();
        fSelectedTaus.reserve(taus.size());

        size_t ptCutPassed = 0;
        size_t etaCutPassed = 0;
	size_t leadTrkPtCutPassed = 0;
	size_t nProngsCutPassed = 0;
	size_t HChTauIDchargeCutPassed = 0;
        size_t againstElectronCutPassed = 0;
        size_t againstMuonCutPassed = 0;
	size_t byTightIsolationPassed = 0;
	size_t RtauCutPassed = 0;
	size_t InvMassCutPassed = 0;

        // Fill initial histograms and do the first selection
        for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
                edm::Ptr<pat::Tau> iTau = *iter;

                increment(fAllSubCount);
                hPt->Fill(iTau->pt(), fEventWeight.getWeight());
                hEta->Fill(iTau->eta(), fEventWeight.getWeight());
		reco::PFCandidateRef leadTrk = iTau->leadPFChargedHadrCand(); // HPS is constructed from PF

                if(!(iTau->pt() > fPtCut)) continue;
                increment(fPtCutSubCount);
                ++ptCutPassed;

                if(!(std::abs(iTau->eta()) < fEtaCut)) continue;
                increment(fEtaCutSubCount);
                ++etaCutPassed;

                //////////////////////////////////////////////////////////////////////

                if(iTau->tauID("againstMuon") < 0.5 ) continue;
                increment(fagainstMuonSubCount);
                ++againstMuonCutPassed;

                if(iTau->tauID("againstElectron") < 0.5 ) continue;
                increment(fagainstElectronSubCount);
                ++againstElectronCutPassed;


		if(leadTrk.isNonnull())
		  hLeadTrkPt->Fill(leadTrk->pt(), fEventWeight.getWeight());

		if(leadTrk.isNull() || !(leadTrk->pt() > fLeadTrkPtCut)) continue;
		increment(fLeadTrkPtSubCount);
		++leadTrkPtCutPassed;

		if(iTau->tauID("byTightIsolation") < 0.5 ) continue;
		increment(fbyHPSIsolationSubCount);
		++byTightIsolationPassed;

		uint16_t nSigTracks        =  iTau->signalPFChargedHadrCands().size();
		hnProngs->Fill(iTau->signalTracks().size(), fEventWeight.getWeight());
		if(nSigTracks != 1 ) continue;
		increment(fnProngsSubCount);
		++nProngsCutPassed;


		float Rtau = 0;
		if (iTau->p() > 0) Rtau =  leadTrk->p()/iTau->p();
		//		float Rtau = iTau->tauID("HChTauIDtauPolarizationCont");
		if (Rtau > 1 ) {
		  hEtaRtau->Fill(iTau->eta());
		}
		hRtau->Fill(Rtau);
    
		if(Rtau < fRtauCut) continue; 
		increment(fRtauSubCount);
		++RtauCutPassed;

/* ONLY HPS discriminators available, please do not uncomment unless sure the are included!
		hnProngs->Fill(iTau->signalTracks().size(), fEventWeight.getWeight());
		if(iTau->tauID("HChTauID1Prong") < 0.5 && iTau->tauID("HChTauID3Prongs") < 0.5) continue;
		increment(fnProngsSubCount);
		++nProngsCutPassed;

		if(iTau->tauID("HChTauIDcharge") < 0.5) continue; 
		increment(fHChTauIDchargeSubCount);
		++HChTauIDchargeCutPassed;

		//float Rtau = 0;
		//if (iTau->p() > 0) leadTrk->p()/iTau->p();
		float Rtau = iTau->tauID("HChTauIDtauPolarizationCont");
		if (Rtau > 1 ) {
		  hEtaRtau->Fill(iTau->eta(), fEventWeight.getWeight());
		}
		hRtau->Fill(Rtau, fEventWeight.getWeight());
    
		if(Rtau < fRtauCut) continue; 
		increment(fRtauSubCount);
		++RtauCutPassed;

		float DeltaE = iTau->tauID("HChTauIDDeltaECont");
		hDeltaE->Fill(DeltaE, fEventWeight.getWeight());

		float flightPathSignif = iTau->tauID("HChTauIDFlightPathSignifCont");
		hFlightPathSignif->Fill(flightPathSignif, fEventWeight.getWeight());

		// DeltaE and flight path are not applied - why?
		// They should be applied for 3-prongs only

		float InvMass = iTau->tauID("HChTauIDInvMassCont");
		hInvMass->Fill(InvMass, fEventWeight.getWeight());

		if(InvMass > fInvMassCut) continue;
		increment(fInvMassSubCount);
		++InvMassCutPassed;
*/
                // Fill Histos after Tau Selection Cuts
                hPtAfterTauSelCuts->Fill(iTau->pt(), fEventWeight.getWeight());
                hEtaAfterTauSelCuts->Fill(iTau->eta(), fEventWeight.getWeight());

                fSelectedTaus.push_back(iTau);
        }

        if(ptCutPassed == 0) return false;
        increment(fPtCutCount);

        if(etaCutPassed == 0) return false;
        increment(fEtaCutCount);

        if(againstMuonCutPassed == 0) return false;
        increment(fagainstMuonCount);

        if(againstElectronCutPassed == 0) return false;
        increment(fagainstElectronCount);


	if(leadTrkPtCutPassed == 0) return false;
	increment(fLeadTrkPtCount); 

	if(byTightIsolationPassed == 0) return false;
	increment(fHPSIsolationCount);

	if(nProngsCutPassed == 0) return false;
	increment(fnProngsCount);

	//	if(HChTauIDchargeCutPassed == 0) return false;
	//	increment(fHChTauIDchargeCount);       

	if(RtauCutPassed == 0) return false;
	increment(fRtauCount);

	//	if(InvMassCutPassed == 0) return false;
	//	increment(fInvMassCount);

        return true;
  }

  bool TauSelection::selectionByTCTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus){
    	fSelectedTaus.clear();
    	fSelectedTaus.reserve(taus.size());

    	size_t ptCutPassed = 0;
    	size_t etaCutPassed = 0;
    	size_t leadTrkPtCutPassed = 0;
    	size_t nProngsCutPassed = 0;
    	size_t HChTauIDchargeCutPassed = 0;
    	size_t byIsolationCutPassed = 0;
    	size_t againstElectronCutPassed = 0;
    	size_t againstMuonCutPassed = 0;
    	size_t RtauCutPassed = 0;
    	size_t InvMassCutPassed = 0;

    	// Fill initial histograms and do the first selection
    	for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      		edm::Ptr<pat::Tau> iTau = *iter;

                increment(fAllSubCount);
                hPt->Fill(iTau->pt(), fEventWeight.getWeight());
                hEta->Fill(iTau->eta(), fEventWeight.getWeight());

                if(!(iTau->pt() > fPtCut)) continue;
                increment(fPtCutSubCount);
                ++ptCutPassed;

                if(!(std::abs(iTau->eta()) < fEtaCut)) continue;
                increment(fEtaCutSubCount);
                ++etaCutPassed;

                //////////////////////////////////////////////////////////////////////

                if(iTau->tauID("againstMuon") < 0.5 ) continue;
                increment(fagainstMuonSubCount);
                ++againstMuonCutPassed;

                if(iTau->tauID("againstElectron") < 0.5 ) continue;
                increment(fagainstElectronSubCount);
                ++againstElectronCutPassed;

		if(iTau->tauID("HChTauIDleadingTrackPtCut") < 0.5 ) continue;
		increment(fLeadTrkPtSubCount);
		++leadTrkPtCutPassed;

      		if(iTau->tauID("HChTauID1Prong") < 0.5 && iTau->tauID("HChTauID3Prongs") < 0.5) continue;
      		increment(fnProngsSubCount);
      		++nProngsCutPassed;

      		if(iTau->tauID("HChTauIDcharge") < 0.5) continue;
      		increment(fHChTauIDchargeSubCount);
      		++HChTauIDchargeCutPassed;

      		if(iTau->tauID("byIsolation") < 0.5) continue;
      		increment(fbyIsolationSubCount);
      		++byIsolationCutPassed;

            	float Rtau = iTau->tauID("HChTauIDtauPolarizationCont");
      		hRtau->Fill(Rtau, fEventWeight.getWeight());
      		if(Rtau < fRtauCut) continue;
      		increment(fRtauSubCount);
      		++RtauCutPassed;

		float DeltaE = iTau->tauID("HChTauIDDeltaECont");
		hDeltaE->Fill(DeltaE, fEventWeight.getWeight());

		float flightPathSignif = iTau->tauID("HChTauIDFlightPathSignifCont");
		hFlightPathSignif->Fill(flightPathSignif, fEventWeight.getWeight());

		// DeltaE and flight path are not applied - why?
		// They should be applied for 3-prongs only

		float InvMass = iTau->tauID("HChTauIDInvMassCont");
		hInvMass->Fill(InvMass, fEventWeight.getWeight());
		if(InvMass > fInvMassCut) continue;
		increment(fInvMassSubCount);
		++InvMassCutPassed;

                // Fill Histos after Tau Selection Cuts
                hPtAfterTauSelCuts->Fill(iTau->pt(), fEventWeight.getWeight());
                hEtaAfterTauSelCuts->Fill(iTau->eta(), fEventWeight.getWeight());

                fSelectedTaus.push_back(iTau);
	}

        if(ptCutPassed == 0) return false;
        increment(fPtCutCount);

        if(etaCutPassed == 0) return false;
        increment(fEtaCutCount);

        if(againstMuonCutPassed == 0) return false;
        increment(fagainstMuonCount);

        if(againstElectronCutPassed == 0) return false;
        increment(fagainstElectronCount);

        if(leadTrkPtCutPassed == 0) return false;
        increment(fLeadTrkPtCount);

    	if(nProngsCutPassed == 0) return false;
    	increment(fnProngsCount);

    	if(HChTauIDchargeCutPassed == 0) return false;
    	increment(fHChTauIDchargeCount);

    	if(byIsolationCutPassed == 0) return false;
    	increment(fbyIsolationCount);

    	if(RtauCutPassed == 0) return false;
    	increment(fRtauCount);

	if(InvMassCutPassed == 0) return false;
	increment(fInvMassCount);

        return true;
  }

  TauSelection::Data TauSelection::setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passEvent) {
    fSelectedTaus.clear();
    fSelectedTaus.reserve(1);
    if (tau.isNonnull())
      fSelectedTaus.push_back(tau);
    return Data(this, passEvent);
  }
}
