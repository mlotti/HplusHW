#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TH1F.h"

namespace HPlus {

  TauSelection::TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSelection(iConfig.getUntrackedParameter<std::string>("selection")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fLeadTrkPtCut(iConfig.getUntrackedParameter<double>("leadingTrackPtCut")),
    fRtauCut(iConfig.getUntrackedParameter<double>("rtauCut")),
    fInvMassCut(iConfig.getUntrackedParameter<double>("invMassCut")),
    fPtCutCount(eventCounter.addCounter("Tau pt cut")),
    fEtaCutCount(eventCounter.addCounter("Tau eta cut")),
    fagainstMuonCount(eventCounter.addCounter("Tau againstMuon discriminator")),
    fagainstElectronCount(eventCounter.addCounter("Tau againstElectron discriminator")),
    fLeadTrkPtCount(eventCounter.addCounter("Tau leading track pt cut")),
    fTaNCCount(eventCounter.addCounter("Tau TaNC cut")),
    fbyIsolationCount(eventCounter.addCounter("Tau byIsolation discriminator")),
    fbyTrackIsolationCount(eventCounter.addCounter("Tau byTrackIsolation cut")),
    fecalIsolationCount(eventCounter.addCounter("Tau ecalIsolation discriminator")),
    fnProngsCount(eventCounter.addCounter("Tau number of prongs cut")),
    fHChTauIDchargeCount(eventCounter.addCounter("Tau charge cut")),
    fRtauCount(eventCounter.addCounter("Tau Rtau cut")),
    fInvMassCount(eventCounter.addCounter("Tau InvMass cut")),
    fAllSubCount(eventCounter.addSubCounter("Tau identification", "all tau candidates")),
    fPtCutSubCount(eventCounter.addSubCounter("Tau identification", "pt cut")),
    fEtaCutSubCount(eventCounter.addSubCounter("Tau identification", "eta cut")),
    fagainstMuonSubCount(eventCounter.addSubCounter("Tau identification","againstMuon discriminator")),
    fagainstElectronSubCount(eventCounter.addSubCounter("Tau identification","againstElectron discriminator")),
    fLeadTrkPtSubCount(eventCounter.addSubCounter("Tau identification", "leading track pt cut")),

      fbyTaNCSubCount(eventCounter.addSubCounter("Tau identification","Tau TaNC cut")),

    fbyIsolationSubCount(eventCounter.addSubCounter("Tau identification", "byIsolation discriminator")),
    fbyTrackIsolationSubCount(eventCounter.addSubCounter("Tau identification", "byTrackIsolation cut")),
    fnProngsSubCount(eventCounter.addSubCounter("Tau identification", "number of prongs cut")),
    fHChTauIDchargeSubCount(eventCounter.addSubCounter("Tau identification", "Tau charge cut")),
    fecalIsolationSubCount(eventCounter.addSubCounter("Tau identification", "ecalIsolation discriminator")),
    fRtauSubCount(eventCounter.addSubCounter("Tau identification","Tau Rtau cut")),
    fInvMassSubCount(eventCounter.addSubCounter("Tau identification","Tau InvMass cut"))
  {
    edm::Service<TFileService> fs;
    hPt = fs->make<TH1F>("tau_pt", "tau_pt", 100, 0., 100.);
    hEta = fs->make<TH1F>("tau_eta", "tau_eta", 60, -3., 3.);
    hPtAfterTauSelCuts = fs->make<TH1F>("tau_pt_afterTauSelCuts", "tau_pt_afterTauSelCuts", 100, 0., 100.);
    hEtaAfterTauSelCuts = fs->make<TH1F>("tau_eta_afterTauSelCuts", "tau_eta_afterTauSelCuts", 60, -3., 3.);
    hEtaRtau = fs->make<TH1F>("tau_eta_Rtau", "tau_eta_Rtau", 60, -3., 3.);
    hLeadTrkPt = fs->make<TH1F>("tau_leadtrk_pt", "tau_leadtrk_pt", 100, 0., 100.);
    hIsolTrkPt = fs->make<TH1F>("tau_isoltrk_pt", "tau_isoltrk_pt", 100, 0., 20.);
    hIsolTrkPtSum = fs->make<TH1F>("tau_isoltrk_ptsum", "tau_isoltrk_ptsum", 100, 0., 20.);
    hIsolTrkPtSumVsPtCut = fs->make<TH2F>("tau_isoltrk_ptsum_vs_ptcut", "tau_isoltrk_ptsum_vs_ptcut", 6, 0.45, 1.05, 100, 0., 20.);
    hNIsolTrksVsPtCut = fs->make<TH2F>("tau_ntrks_vs_ptcut", "tau_ntrks_vs_ptcut", 6, 0.45, 1.05,10,0.,10.);
    hIsolMaxTrkPt = fs->make<TH1F>("tau_isomaxltrk_pt", "tau_isolmaxtrk_pt", 100, 0., 20.);
    hnProngs = fs->make<TH1F>("tau_nProngs", "tau_nProngs", 10, 0., 10.);
    hRtau = fs->make<TH1F>("tau_Rtau", "tau_Rtau", 100, 0., 1.2);
    hDeltaE = fs->make<TH1F>("tau_DeltaE", "tau_DeltaE", 100, 0., 0.01);
    hlightPathSignif = fs->make<TH1F>("tau_lightPathSignif", "tau_lightPathSignif", 100, 0., 0.01);
    hInvMass = fs->make<TH1F>("tau_InvMass", "tau_InvMass", 100, 0., 5.);
    hbyTaNC = fs->make<TH1F>("tau_TaNC", "tau_TaNC", 100, -1., 1.);
  }

  TauSelection::~TauSelection() {}

  bool TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
	if(fSelection == "CaloTauCutBased")             return selectionByTCTauCuts(iEvent,iSetup);
	if(fSelection == "ShrinkingConePFTauCutBased")  return selectionByPFTauCuts(iEvent,iSetup);
	if(fSelection == "ShrinkingConePFTauTaNCBased") return selectionByPFTauTaNC(iEvent,iSetup);
	if(fSelection == "HPSTauBased")                 return selectionByHPSTau(iEvent,iSetup);
	std::cout << "WARNING, no tau selection used!" << std::endl;
	return false;
  }

  bool TauSelection::selectionByPFTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);

    const edm::PtrVector<pat::Tau>& taus(htaus->ptrVector());

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

      hPt->Fill(iTau->pt());
      hEta->Fill(iTau->eta());
      reco::PFCandidateRef  leadTrk = iTau->leadPFChargedHadrCand(); 
      //      reco::TrackRef leadTrk = iTau->leadTrack();
      //      if(leadTrk.isNonnull())
      //        hLeadTrkPt->Fill(leadTrk->pt());

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
        hLeadTrkPt->Fill(leadTrk->pt());

      if(leadTrk.isNull() || !(leadTrk->pt() > fLeadTrkPtCut)) continue;
      increment(fLeadTrkPtSubCount);
      ++leadTrkPtCutPassed;

      if(iTau->tauID("HChTauIDcharge") < 0.5) continue; 
      increment(fHChTauIDchargeSubCount);
      ++HChTauIDchargeCutPassed;
     
     
      float ptmax = 0;
      float ptsum = 0;

      const reco::PFCandidateRefVector& isolCands = iTau->isolationPFChargedHadrCands();
      reco::PFCandidateRefVector::const_iterator iCand = isolCands.begin();
      //      const reco::TrackRefVector& isolCands = iTau->isolationTracks();
      //      reco::TrackRefVector::const_iterator iCand = isolCands.begin();
      //      std::cout << " isol cands " << isolCands.size() << std::endl;
      for(; iCand != isolCands.end(); ++iCand) {
	float pt = (*iCand)->pt();
	ptsum += pt; 
	if (pt > ptmax) ptmax = pt;
	hIsolTrkPt->Fill(pt);
	//	std::cout << " isol track pt " << pt << std::endl;
	//iCand->pt()
      }
      hIsolMaxTrkPt->Fill(ptmax);
      hIsolTrkPtSum->Fill(ptsum);

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
	hIsolTrkPtSumVsPtCut->Fill(cut,sum);
	hNIsolTrksVsPtCut->Fill(cut,float(nTracks));
      } 

      
      if(iTau->tauID("byIsolation") < 0.5) continue; 
      increment(fbyIsolationSubCount);
      ++byIsolationCutPassed;

      if(iTau->tauID("ecalIsolation") < 0.5) continue; 
      increment(fecalIsolationSubCount);
      ++ecalIsolationCutPassed;

        
      hnProngs->Fill(iTau->signalTracks().size());    
      if(iTau->tauID("HChTauID1Prong") < 0.5 && iTau->tauID("HChTauID3Prongs") < 0.5) continue;
      //      if(iTau->tauID("HChTauID3Prongs") < 0.5) continue; 
      increment(fnProngsSubCount);
      ++nProngsCutPassed;
 
      if(iTau->tauID("HChTauIDcharge") < 0.5) continue; 
      increment(fHChTauIDchargeSubCount);
      ++HChTauIDchargeCutPassed;
  
      float Rtau = leadTrk->p()/iTau->p();
      //      Rtau = leadTrk->p()/iTau->p();
      hRtau->Fill(Rtau);
    
      if(Rtau < fRtauCut) continue; 
      increment(fRtauSubCount);
      ++RtauCutPassed;
      
      float DeltaE = iTau->tauID("HChTauIDDeltaECont");
      hDeltaE->Fill(DeltaE);

      float lightPathSignif = iTau->tauID("HChTauIDFlightPathSignifCont");
      hlightPathSignif->Fill(lightPathSignif);

      float InvMass = iTau->tauID("HChTauIDInvMassCont");
      hInvMass->Fill(InvMass);
      //      continue;
     
      if(InvMass > fInvMassCut) continue;
      increment(fInvMassSubCount);
      ++InvMassCutPassed;


      // Fill Histos after Tau Selection Cuts
      hPtAfterTauSelCuts->Fill(iTau->pt());
      hEtaAfterTauSelCuts->Fill(iTau->eta());

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

  bool TauSelection::selectionByPFTauTaNC(const edm::Event& iEvent, const edm::EventSetup& iSetup){

	// NC input corresponds to isolation and mass 

	edm::Handle<edm::View<pat::Tau> > htaus;
	iEvent.getByLabel(fSrc, htaus);

	const edm::PtrVector<pat::Tau>& taus(htaus->ptrVector());

	fSelectedTaus.clear();
	fSelectedTaus.reserve(taus.size());

	size_t againstElectronCutPassed = 0;
	size_t againstMuonCutPassed = 0;
	size_t ptCutPassed = 0;
    	size_t etaCutPassed = 0;
    	size_t leadTrkPtCutPassed = 0;
	size_t byTaNCCutPassed = 0;
	size_t RtauCutPassed = 0;

	for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
		edm::Ptr<pat::Tau> iTau = *iter;
		
		increment(fAllSubCount);
      		hPt->Fill(iTau->pt());
      		hEta->Fill(iTau->eta());

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
      		if(leadTrk.isNonnull()) hLeadTrkPt->Fill(leadTrk->pt());

      		if(leadTrk.isNull() || !(leadTrk->pt() > fLeadTrkPtCut)) continue;
      		increment(fLeadTrkPtSubCount);
      		++leadTrkPtCutPassed;

		hbyTaNC->Fill(iTau->tauID("byTaNC"));
//		if(iTau->tauID("byTaNC") < 0.6) continue;
//		if(iTau->tauID("byTaNCfrQuarterPercent") < 0.5) continue;
		if(iTau->tauID("byTaNCfrTenthPercent") < 0.5) continue;
		//		if(iTau->tauID("byTaNCfrOnePercent") < 0.5) continue;
//		if(iTau->tauID("byTaNCfrHalfPercent") < 0.5) continue;
		increment(fbyTaNCSubCount);
		++byTaNCCutPassed;

		float Rtau = leadTrk->p()/iTau->p();
		hRtau->Fill(Rtau);

		if(Rtau < fRtauCut) continue;
		increment(fRtauSubCount);
		++RtauCutPassed;

		float DeltaE = iTau->tauID("HChTauIDDeltaECont");
      		hDeltaE->Fill(DeltaE);

      		float lightPathSignif = iTau->tauID("HChTauIDFlightPathSignifCont");
      		hlightPathSignif->Fill(lightPathSignif);

      		// Fill Histos after Tau Selection Cuts
      		hPtAfterTauSelCuts->Fill(iTau->pt());
      		hEtaAfterTauSelCuts->Fill(iTau->eta());

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

	if(byTaNCCutPassed == 0) return false;
	increment(fTaNCCount);

    	if(RtauCutPassed == 0) return false;
    	increment(fRtauCount);

	return true;
  }

  bool TauSelection::selectionByHPSTau(const edm::Event& iEvent, const edm::EventSetup& iSetup){

        edm::Handle<edm::View<pat::Tau> > htaus;
        iEvent.getByLabel(fSrc, htaus);

        const edm::PtrVector<pat::Tau>& taus(htaus->ptrVector());

        fSelectedTaus.clear();
        fSelectedTaus.reserve(taus.size());

        size_t ptCutPassed = 0;
        size_t etaCutPassed = 0;
	//        size_t leadTrkPtCutPassed = 0;
	//        size_t nProngsCutPassed = 0;
	//        size_t HChTauIDchargeCutPassed = 0;
	//        size_t byIsolationCutPassed = 0;
        size_t againstElectronCutPassed = 0;
        size_t againstMuonCutPassed = 0;
	//        size_t RtauCutPassed = 0;
	//        size_t InvMassCutPassed = 0;

        // Fill initial histograms and do the first selection
        for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
                edm::Ptr<pat::Tau> iTau = *iter;

                increment(fAllSubCount);
                hPt->Fill(iTau->pt());
                hEta->Fill(iTau->eta());

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

                // Fill Histos after Tau Selection Cuts
                hPtAfterTauSelCuts->Fill(iTau->pt());
                hEtaAfterTauSelCuts->Fill(iTau->eta());

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
/*
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
*/
        return true;
  }

  bool TauSelection::selectionByTCTauCuts(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    	edm::Handle<edm::View<pat::Tau> > htaus;
    	iEvent.getByLabel(fSrc, htaus);

     	const edm::PtrVector<pat::Tau>& taus(htaus->ptrVector());

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
                hPt->Fill(iTau->pt());
                hEta->Fill(iTau->eta());

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
      		hRtau->Fill(Rtau);
      		if(Rtau < fRtauCut) continue;
      		increment(fRtauSubCount);
      		++RtauCutPassed;

                // Fill Histos after Tau Selection Cuts
                hPtAfterTauSelCuts->Fill(iTau->pt());
                hEtaAfterTauSelCuts->Fill(iTau->eta());

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

        return true;
  }
}
