#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "Math/GenVector/VectorUtil.h"

#include "TLorentzVector.h"
#include "TVector3.h"

namespace HPlus {
  GenParticleAnalysis::Data::Data():
    fTTBarDecayMode(kTT_invalid)
  {}

  GenParticleAnalysis::Data::~Data() {}
  void GenParticleAnalysis::Data::check() const {
    if(!isValid())
      throw cms::Exception("Assert") << "GenParticleAnalysis::Data: This Data object was constructed with the default constructor, not with GenParticleAnalysis::(silent)analyze(). There is something wrong in your code." << std::endl;
  }

  GenParticleAnalysis::GenParticleAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMetSrc(iConfig.getUntrackedParameter<edm::InputTag>("metSrc")),
    fOneProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneProngTauSrc")),
    fOneAndThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneAndThreeProngTauSrc")),
    fThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("threeProngTauSrc")),
    fEnabled(iConfig.getUntrackedParameter<bool>("enabled"))
  {
    init(histoWrapper);
  }

  GenParticleAnalysis::~GenParticleAnalysis() {}

  void GenParticleAnalysis::init(HPlus::HistoWrapper& histoWrapper){
    if(!fEnabled)
      return;

    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("GenParticleAnalysis");

    hRtau1pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genRtau1ProngHp", "genRtau1ProngHp", 100, 0., 1.2);
    hRtau13pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genRtau13ProngHp", "genRtau13ProngHp", 100, 0., 1.2);
    hRtau3pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genRtau3ProngHp", "genRtau3ProngHp", 100, 0., 1.2);
    hRtau1pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genRtau1ProngW", "genRtau1ProngW", 100, 0., 1.2);
    hRtau13pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genRtau13ProngW", "genRtau13ProngW", 100, 0., 1.2);
    hRtau3pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genRtau3ProngW", "genRtau3ProngW", 100, 0., 1.2);
    hptVisibleTau1pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genptVisibleTau1ProngHp", "ptVisibleTau1ProngHp", 100, 0., 200);
    hptVisibleTau13pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genptVisibleTau13ProngHp", "ptVisibleTau13ProngHp", 100, 0., 200);
    hptVisibleTau3pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genptVisibleTau3ProngHp", "ptVisibleTau3ProngHp", 100, 0., 200);
    hEtaVisibleTau1pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genEtaVisibleTau1ProngHp", "etaVisibleTau1ProngHp", 100, -5., 5);
    hLeadingTrack1pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genLeadingTrack1ProngHp", "LeadingTrack1ProngHp", 100, 0., 200);
    hptVisibleTau1pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genPtVisibleTau1ProngW", "ptVisibleTau1ProngW", 100, 0., 200);
    hptVisibleTau13pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genPtVisibleTau13ProngW", "ptVisibleTau13ProngW", 100, 0., 200);
    hptVisibleTau3pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genPtVisibleTau3ProngW", "ptVisibleTau3ProngW", 100, 0., 200);
    hEtaVisibleTau1pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genEtaVisibleTau1ProngW", "etaVisibleTau1ProngW", 100, -5., 5);
    hLeadingTrack1pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genLeadingTrack1ProngW", "LeadingTrack1ProngW", 100, 0., 200);
    hTauMass1pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genTauMass1pHp", "genTauMass1pHp", 100, 0., 2.);
    hTauMass1pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genTauMass1pW", "genTauMass1pW", 100, 0., 2.);
    hThetaCM1pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genThetaCM1pHp", "genThetaCMs1pHp", 100, 0., 3.);
    hThetaCM1pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genThetaCM1pW", "genThetaCMs1pW", 100, 0., 3.);
    hMagCM1pHp = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genMagCM1pHp", "genMagCMs1pHp", 100, 0.95, 1.);
    hMagCM1pW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genMagCM1pW", "genMagCMs1pW", 100, 0.95, 1.);
    hHpMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HpMass", "HpMass", 100, 100, 200.);
    hBquarkMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_Multiplicity", "genBquark_Multiplicity", 20, -0.5, 19.5);
    hBquarkStatus2Multiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_Status2_Multiplicity", "genBquark_Status2_Multiplicity", 20, -0.5, 19.5);
    hBquarkStatus3Multiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_Status3_Multiplicity", "genBquark_Status3_Multiplicity", 20, -0.5, 19.5);
    hBquarkFromTopEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTop_Eta", "genBquark_FromTop_Eta", 300, -6.0, 6.0);
    hBquarkNotFromTopEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_NotFromTop_Eta", "genBquark_NotFromTop_Eta", 300, -6.0, 6.0);
    hBquarkFromTopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTop_Pt", "genBquark_FromTop_Pt", 250, 0., 500.);
    hBquarkNotFromTopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_NotFromTop_Pt", "genBquark_NotFromTop_Pt", 250, 0., 500.);
    hBquarkFromTopEtaPtCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTop_Eta_ptcut", "genBquark_FromTop_Eta_ptcut", 300, -6.0, 6.0);
    hBquarkNotFromTopEtaPtCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_NotFromTop_Eta_ptcut", "genBquark_NotFromTop_Eta_ptcut", 300, -6.0, 6.0);
    hBquarkFromTopPtEtaCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTop_Pt_etacut", "genBquark_FromTop_Pt_etacut", 250, 0., 500.);
    hBquarkNotFromTopPtEtaCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_NotFromTop_Pt_etacut", "genBquark_NotFromTop_Pt_etacut", 250, 0., 500.);
    hBquarkFromTopDeltaRTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTop_DeltaRTau", "genBquark_FromTop_DeltaRTau", 300, 0., 8.);
    hBquarkNotFromTopDeltaRTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_NotFromTop_DeltaRTau", "genBquark_NotFromTop_DeltaRTau", 400, 0., 8.);
    hGenDeltaRHiggsSide= histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromHiggsSide_DeltaRTau", "genBquark_FromHiggsSide_DeltaRTau", 350, 0., 7.);
    hGenBquarkFromHiggsSideEta= histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromHiggsSide_Eta", "genBquark_FromHiggsSide_Eta", 250, -5.0, 5.0);
    hGenBquarkFromHiggsSidePt= histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromHiggsSide_Pt", "genBquark_FromHiggsSide_Pt", 200, 0., 400.);
    hGenDeltaRTopSide= histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTopSide_DeltaRTau", "genBquark_FromTopSide_DeltaRTau", 350, 0., 7.);
    hGenBquarkFromTopSideEta= histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTopSide_Eta", "genBquark_FromTopSide_Eta", 250, -5.0, 5.0);
    hGenBquarkFromTopSidePt= histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genBquark_FromTopSide_Pt", "genBquark_FromTopSide_Pt", 200, 0., 400.);

    hTopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genTopPt", "genTopPt", 300, 0., 600);
    hTopPt_wrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genTopPt_wrongB", "genTopPt_wrongB", 300, 0., 600);
    hTopToChHiggsMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "genTopToChHiggsMass", "genTopToChHiggsMass", 300, 0., 600);
    hTopToWBosonMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "genTopToWBosonMass", "genTopToWBosonMass", 300, 0., 600);
    hFullHiggsMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "genFullHiggsMass", "genFullHiggsMass", 300, 0., 600);
    hTopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "genTopPt", "genTopPt", 300, 0., 600);
    hGenMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genMET", "genMET", 40, 0., 400);
    hWPt  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genWPt", "genWPt", 120, 0., 600);
    hWEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genWEta", "genWEta", 100, -5., 5.);    
    hWPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genWPhi", "genWPhi", 64, -3.2, 3.2);    
  }

  WrappedTH1 *GenParticleAnalysis::bookTTBarDecayModeHistogram(HistoWrapper& histoWrapper, HistoWrapper::HistoLevel histoLevel, TFileDirectory& dir, const std::string& name) {
    WrappedTH1 *h = histoWrapper.makeTH<TH1F>(histoLevel, dir, name.c_str(), "TTBar decay mode", kTT_bbtautau, 1, kTT_bbtautau+1);
    if(h->isActive()) {
      TAxis *axis = h->GetXaxis();
      axis->SetBinLabel(kTT_noTT,     "not t#bar{t}");
      axis->SetBinLabel(kTT_unknown,  "unknown");
      axis->SetBinLabel(kTT_bbqqqq,   "t#bar{T}#rightarrowbbqqqq");     // 46 %
      axis->SetBinLabel(kTT_bbqqe,    "t#bar{T}#rightarrowbbqqe");      // 15 %
      axis->SetBinLabel(kTT_bbqqmu,   "t#bar{T}#rightarrowbbqq#mu");    // 15 %
      axis->SetBinLabel(kTT_bbqqtau,  "t#bar{T}#rightarrowbbqq#tau");   // 15 %
      axis->SetBinLabel(kTT_bbee,     "t#bar{T}#rightarrowbbee");       //  1 %
      axis->SetBinLabel(kTT_bbemu,    "t#bar{T}#rightarrowbbe#mu");     //  2 %
      axis->SetBinLabel(kTT_bbetau,   "t#bar{T}#rightarrowbbe#tau");    //  2 %
      axis->SetBinLabel(kTT_bbmumu,   "t#bar{T}#rightarrowbb#mu#mu");   //  1 %
      axis->SetBinLabel(kTT_bbmutau,  "t#bar{T}#rightarrowbb#mu#tau");  //  2 %
      axis->SetBinLabel(kTT_bbtautau, "t#bar{T}#rightarrowbb#tau#tau"); //  1 %
    }
    return h;
  }

  GenParticleAnalysis::Data GenParticleAnalysis::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup ){
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup);
  }

  GenParticleAnalysis::Data GenParticleAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup ){
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup);
  }

  GenParticleAnalysis::Data GenParticleAnalysis::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup ){
    Data output;
    
    if (iEvent.isRealData() || !fEnabled) return output;

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel(fSrc, genParticles);

    typedef math::XYZTLorentzVectorD LorentzVector;
    typedef std::vector<LorentzVector> LorentzVectorCollection;


    edm::Handle <std::vector<LorentzVector> > oneProngTaus;
    iEvent.getByLabel(fOneProngTauSrc, oneProngTaus);

    edm::Handle <std::vector<LorentzVector> > oneAndThreeProngTaus;
    iEvent.getByLabel(fOneAndThreeProngTauSrc,oneAndThreeProngTaus);	  

    edm::Handle <std::vector<LorentzVector> > threeProngTaus;
    iEvent.getByLabel(fThreeProngTauSrc, threeProngTaus);	  

    edm::Handle<edm::View<reco::GenMET> > hmet;
    iEvent.getByLabel(fMetSrc, hmet);
    output.fGenMet = hmet->ptrAt(0);

    hGenMET->Fill(output.fGenMet->et());

    output.fTTBarDecayMode = findTTBarDecayMode(*genParticles);

    // loop over all genParticles
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if ( abs(id) != 24 ) continue;
      bool hasDaughter = false;
      // Check whether the genParticle decays to itself. If yes do not consider in counting
      if ( p.numberOfDaughters() != 0 ){
        // Loop over all 1st daughters of genParticle
        for(size_t j = 0; j < p.numberOfDaughters() ; ++ j) {
          const reco::Candidate *d = p.daughter( j );
          if( p.pdgId() == d->pdgId() ) hasDaughter = true;
        }
      }
      if(hasDaughter) continue;
      hWPt->Fill(p.pt());
      hWEta->Fill(p.eta());
      hWPhi->Fill(p.phi());
    }


    // One-prong tau jets
    double Rtau = -1;
    for( LorentzVectorCollection::const_iterator tau = oneProngTaus->begin();tau!=oneProngTaus->end();++tau) {
  
      double ptmax = 0;
      bool tauFromHiggs = false;
      bool tauFromW = false;

      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	double mass = p.mass();
	int id = p.pdgId();
	if ( abs(id) == 37) {
	  hHpMass->Fill(mass);
	}
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR > 0.2) continue;
	if ( abs(id) == 15 ) {
	  int numberOfTauMothers = p.numberOfMothers(); 
	  for (int im=0; im < numberOfTauMothers; ++im){  
	    const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	    if ( !dparticle) continue;
	    int idmother = dparticle->pdgId();
	    if ( abs(idmother) == 37 ) {
	      tauFromHiggs = true;
	    }
	    if ( abs(idmother) == 24 ) {
	      tauFromW = true;
	    }
	  }
	}
      }


      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	
	if ( abs(id) != 211 ) continue;      
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR < 0.1) {
	  if ( p.pt() > ptmax ){
	    ptmax = p.pt();
	    if (  tau->E() > 0 ) 
	      Rtau = p.p4().P() / tau->E() ;
	  }
	}
	
      }
      
      double thetaCM = tau->BoostToCM().Theta();
      double magCM = tau->BoostToCM().mag2();
      
      if (tauFromHiggs ) {
	hptVisibleTau1pHp->Fill(tau->pt());
	hEtaVisibleTau1pHp->Fill(tau->eta());
	if ( tau->pt() > 40 && ptmax > 20 && fabs(tau->eta()) < 2.3 ) {
	  hRtau1pHp->Fill(Rtau);
	  hLeadingTrack1pHp->Fill(ptmax);
	  hThetaCM1pHp->Fill(thetaCM); 
	  hTauMass1pHp->Fill(tau->mass());
	  hMagCM1pHp->Fill(magCM);
	}
      }
      if (tauFromW) {
	hptVisibleTau1pW->Fill(tau->pt());
	hEtaVisibleTau1pW->Fill(tau->eta());
	if ( tau->pt() > 40 && ptmax > 20 && fabs(tau->eta()) < 2.3 ) {
	  hRtau1pW->Fill(Rtau);
	  hLeadingTrack1pW->Fill(ptmax);
	  hThetaCM1pW->Fill(thetaCM); 
	  hTauMass1pW->Fill(tau->mass());
	  hMagCM1pW->Fill(magCM);
	}
      }
    }
    


   // One-and-three prong tau jets
    Rtau = -1;
    for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
  
      double ptmax = 0;   
      bool tauFromHiggs = false;
      bool tauFromW = false;

      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) == 15 ) {
	  int numberOfTauMothers = p.numberOfMothers(); 
	  for (int im=0; im < numberOfTauMothers; ++im){  
	    const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	    if ( !dparticle) continue;
	    int idmother = dparticle->pdgId();
	    if ( abs(idmother) == 37 ) {
	      tauFromHiggs = true;
	    }
	    if ( abs(idmother) == 24 ) {
	      tauFromW = true;
	    }
	  }
	}
      }



      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	
	if ( abs(id) != 211 ) continue;
	
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR < 0.1) {
	  if ( p.pt() > ptmax ){
	    ptmax = p.pt();
	    if (  tau->E() > 0 ) 
	      Rtau = p.p4().P() / tau->E() ;
	  }
	}
      }

      if (tauFromHiggs ) {
	if ( tau->pt() > 40 && ptmax > 20 && fabs(tau->eta()) < 2.3 ) {
	  hRtau13pHp->Fill(Rtau);
	  hptVisibleTau13pHp->Fill(tau->pt());
	}
      }
      if (tauFromW) {
	if ( tau->pt() > 40 && ptmax > 20 && fabs(tau->eta()) < 2.3 ) {
	  hRtau13pW->Fill(Rtau);
	  hptVisibleTau13pW->Fill(tau->pt());
	}
      }
    }
    
   // Three-prong tau jets
    Rtau = -1;
    for( LorentzVectorCollection::const_iterator tau = threeProngTaus->begin();tau!=threeProngTaus->end();++tau) {  
      //const reco::GenParticle* matchingPion;
      double ptmax = 0;
      bool tauFromHiggs = false;
      bool tauFromW = false;
      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) == 15 ) {
	  //	  bool tauFromHiggs = false;
	  int numberOfTauMothers = p.numberOfMothers(); 
	  for (int im=0; im < numberOfTauMothers; ++im){  
	    const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	    if ( !dparticle) continue;
	    int idmother = dparticle->pdgId();
	    if ( abs(idmother) == 37  ) {
	      tauFromHiggs = true;
	    }
	    if ( abs(idmother) == 24 ) {
	      tauFromW = true;
	    }
	  }
	}
      }


      for (size_t i=0; i < genParticles->size(); ++i){  
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) != 211 ) continue;
	double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	if ( deltaR < 0.1) {
	  if ( p.pt() > ptmax ){
	    ptmax = p.pt();
	    if (  tau->E() > 0 ) 
	      Rtau = p.p4().P() / tau->E() ;
	    //matchingPion  =  dynamic_cast<const reco::GenParticle*>(&p);
	  }
	}
      }
      
      //     std::cout << " pion 1/3 prong " <<  ptmax << " Rtau  " <<  Rtau << std::endl;
      
      if (tauFromHiggs ) {
	if ( tau->pt() > 40 && ptmax > 20 && fabs(tau->eta()) < 2.3 ) {
	  hRtau3pHp->Fill(Rtau);
	  hptVisibleTau3pHp->Fill(tau->pt());
	}
      }
      if (tauFromW) {
	if ( tau->pt() > 40 && ptmax > 20 && fabs(tau->eta()) < 2.3 ) {
	  hRtau3pW->Fill(Rtau);
	  hptVisibleTau3pW->Fill(tau->pt());
	}
      }
    }


    /////////////////////////////////////////////////////////////////////
    // correlations in the signal event

    int tauFromHiggsId = 0;
    int ntaus = 0;
    bool tauHiggsSideFound = false;
    // Generate a vector of all taus from H+
    std::vector<LorentzVector> tausFromHp;
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if ( abs(id) != 15 || hasImmediateMother(p,15) || hasImmediateMother(p,-15) ) continue;
      if( hasImmediateMother(p,37) || hasImmediateMother(p,-37) ) {
	tausFromHp.push_back(p.p4());
	tauFromHiggsId = id;
	ntaus++;
	tauHiggsSideFound = true;	  
      }
    }

    // t(6) -> H+(37) -> tau(-15) 
 
  
    double bPt, bEta;
    if (tauHiggsSideFound && ntaus == 1) {
    
      for (size_t i=0; i < genParticles->size(); ++i){
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	// b from Higgs side
	if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	bEta = p.eta();
	bPt = p.pt();
	
	if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {

	  for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
	    bool tauFromHp = false;
	    for(size_t itau=0; itau<tausFromHp.size(); ++itau) {
	      if(ROOT::Math::VectorUtil::DeltaR(*tau, tausFromHp[itau]) < 0.4){
		tauFromHp=true;
		break;
	      }
	    }
	    if(tauFromHp) {
	      double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	      if ( id * tauFromHiggsId  < 0 ) {
		//		std::cout << " H+ side  " << id <<  " tauFromHiggsId " <<   tauFromHiggsId << " deltaR " << deltaR << " pT " << bPt << std::endl;
		hGenDeltaRHiggsSide->Fill(deltaR);
		hGenBquarkFromHiggsSideEta->Fill(bEta);
		hGenBquarkFromHiggsSidePt->Fill(bPt);
       
	      }
	      if ( id * tauFromHiggsId  > 0 ) {
		//		std::cout << " Top side  " << id <<  " tauFromHiggsId " <<   tauFromHiggsId << " deltaR " << deltaR << " pT " << bPt <<std::endl;
		hGenDeltaRTopSide->Fill(deltaR);
		hGenBquarkFromTopSideEta->Fill(bEta);
		hGenBquarkFromTopSidePt->Fill(bPt);
	      }
	    }
	  }
	}
      }
      
    }





    // b-quark analysis for gg -> tbH+
   
    //    std::vector<LorentzVector> tausFromHp;
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if(abs(id) == 15 && (hasImmediateMother(p,37) || hasImmediateMother(p,-37))) tausFromHp.push_back(p.p4());
    }



    int nBquarks = 0;
    // loop over all genParticles
    for (size_t i=0; i < genParticles->size(); ++i){  
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if ( abs(id) != 5 ) continue;    
      bool bHasBquarkDaughter = false;
      // Check whether the genParticle decays to itself. If yes do not consider in counting
      if ( p.numberOfDaughters() != 0 ){
      	// Loop over all 1st daughters of genParticle    
      	for(size_t j = 0; j < p.numberOfDaughters() ; ++ j) {
      	  const reco::Candidate *d = p.daughter( j );
      	  if( p.pdgId() == d->pdgId() ) bHasBquarkDaughter = true; 
      	}
      }
      if(bHasBquarkDaughter) continue;
      nBquarks++;      
    }
    hBquarkMultiplicity->Fill(nBquarks);
    
    
    //    double bPt, bEta;

    // loop over all genParticles
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      // Only choose beauties
      if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
      bEta = p.eta();
      bPt = p.pt();
      // Plot eta, pt and deltaR in different histos based on whether there was a t mother or not
      if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
        hBquarkFromTopEta->Fill(bEta);
        hBquarkFromTopPt->Fill(bPt);
	if (bPt > 20) hBquarkFromTopEtaPtCut->Fill(bEta);
        if (fabs(bEta) < 2.4) hBquarkFromTopPtEtaCut->Fill(bPt);
        for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
          // Check that the tau comes from H+
          bool tauFromHp = false;
          for(size_t itau=0; itau<tausFromHp.size(); ++itau) {
            if(ROOT::Math::VectorUtil::DeltaR(*tau, tausFromHp[itau]) < 0.4){
              tauFromHp=true;
              break;
            }
          }
          if(tauFromHp) {
            double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
            hBquarkFromTopDeltaRTau->Fill(deltaR);
          }
        }
      }
      else {
        if (bPt > 20) hBquarkNotFromTopEtaPtCut->Fill(bEta);
        if (fabs(bEta) < 2.4) hBquarkNotFromTopPtEtaCut->Fill(bPt);
        for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
          // Check that the tau comes from H+
          bool tauFromHp = false;
          for(size_t itau=0; itau<tausFromHp.size(); ++itau) {
            if(ROOT::Math::VectorUtil::DeltaR(*tau, tausFromHp[itau]) < 0.4){
              tauFromHp=true;
              break;
            }
          }
          if(tauFromHp) {
            double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
            hBquarkNotFromTopDeltaRTau->Fill(deltaR);
          }
        }
      }
    }
        
    // loop over all genParticles, search tops that decay to u and d and calculate pt
    // also calculate the "wrong" pt, by picking the b quark that does not come from the t
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if ( abs(id) != 6 || hasImmediateMother(p,id)) continue;
      std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
      int daughterId=9999;
      double px = 0, py = 0;
      double px_wrong = 0, py_wrong = 0;
      bool decaysHadronically = false;
      for(size_t d=0; d<daughters.size(); ++d) {
        const reco::GenParticle& dparticle = *daughters[d];
        daughterId = dparticle.pdgId();
        if( abs(daughterId) == 24 ) {
          px += dparticle.px();
          py += dparticle.py();
          px_wrong += dparticle.px();
          py_wrong += dparticle.py();
          if(hasDaughter(dparticle,1) || hasDaughter(dparticle,-1) || 
               hasDaughter(dparticle,2) || hasDaughter(dparticle,-2) || 
               hasDaughter(dparticle,3) || hasDaughter(dparticle,-3) || 
               hasDaughter(dparticle,4) || hasDaughter(dparticle,-4) )
          {
      	    decaysHadronically = true;
          }
        }
        if( abs(daughterId) == 5 ) {
          px += dparticle.px();
          py += dparticle.py();
        }
      }
      // Look for other b quarks
      for (size_t j=0; j < genParticles->size(); ++j){
        const reco::Candidate & b = (*genParticles)[j];
        int bId = b.pdgId();
        if ( abs(bId) != 5 || hasImmediateMother(b,bId)) continue;
        if ( hasImmediateMother(b,6) || hasImmediateMother(b,-6)) continue;
        px_wrong += b.px();
        py_wrong += b.py();
        // Stop at the first found b quark that does not come from top
        break;
      }
      if(decaysHadronically) {
        hTopPt->Fill(sqrt(px*px+py*py));
        hTopPt_wrongB->Fill(sqrt(px_wrong*px_wrong+py_wrong*py_wrong));
      }
    }

    // Loop over all gen particles, find tops that decay via t -> Wb and t -> Hb
    // and add their masses to different histograms
    for (size_t i=0; i < genParticles->size(); ++i){
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      if ( abs(id) != 6 || hasImmediateMother(p,id)) continue;
      std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
      int daughterId=9999;
      double px = 0, py = 0, pz = 0, E = 0;
      bool decaysToChHiggs = false;
      bool decaysToWBoson = false;
      for(size_t d=0; d<daughters.size(); ++d) {
        const reco::GenParticle& dparticle = *daughters[d];
        daughterId = dparticle.pdgId();
	// If top decays to W boson (and b quark):
        if( abs(daughterId) == 24 ) {
          px += dparticle.px();
          py += dparticle.py();
	  pz += dparticle.pz();
	  E  += dparticle.energy();
	  decaysToWBoson = true;
        }
	// If top decays to charged Higgs boson (and b quark):
        if( abs(daughterId) == 37 ) {
          px += dparticle.px();
          py += dparticle.py();
	  pz += dparticle.pz();
	  E  += dparticle.energy();
	  decaysToChHiggs = true;
        }
	// In either case (t -> Wb || t -> Hb), add four momentum of b quark
        if( abs(daughterId) == 5 ) {
          px += dparticle.px();
          py += dparticle.py();
	  pz += dparticle.pz();
	  E  += dparticle.energy();
        }
      }
      if(decaysToWBoson) {
        hTopToWBosonMass->Fill(sqrt(E*E - px*px - py*py - pz*pz));
      }
      if(decaysToChHiggs) {
        hTopToChHiggsMass->Fill(sqrt(E*E - px*px - py*py - pz*pz));
      }
    }

    // Loop over all gen particles, find charged Higgs bosons decaying to tau+nu and put their full mass
    // in a histogram (i.e. norm of four-momentum)
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      // If charged Higgs
      if ( abs(id) != 37 || hasImmediateMother(p,id)) continue;
      std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
      int daughterId=9999;
      double px = 0, py = 0, pz = 0, E = 0;
      bool tauFound = false;
      bool neutrinoFound = false;
      for(size_t d=0; d<daughters.size(); ++d) {
        const reco::GenParticle& dparticle = *daughters[d];
        daughterId = dparticle.pdgId();
	// If tau among immediate daughters
        if( abs(daughterId) == 15 ) {
          px += dparticle.px();
          py += dparticle.py();
	  pz += dparticle.pz();
	  E  += dparticle.energy();
	  //	  std::cout << "Tau found." << std::endl;
	  tauFound = true;
        }
	// If tau neutrino among immediate daughters
        if( abs(daughterId) == 16 ) {
          px += dparticle.px();
          py += dparticle.py();
	  pz += dparticle.pz();
	  E  += dparticle.energy();
	  neutrinoFound = true;
        }
      } // end of loop over daughters of charged Higgs
      // If both tau and tau neutrino found among immediate daughters, add mass to histogram
      if( tauFound && neutrinoFound) {
	hFullHiggsMass->Fill(sqrt(E*E - px*px - py*py - pz*pz));
	//	  std::cout << "Mass put in histogram" << std::endl;
      }
      else {
	//	  std::cout << "Charged Higgs boson NOT decaying to tauNu found" << std::endl;
      }
    }    

    return output;
  }
   //eof: void GenParticleAnalysis::analyze()

  GenParticleAnalysis::TTBarDecayMode GenParticleAnalysis::findTTBarDecayMode(const std::vector<reco::GenParticle>& genParticles) const {
    // First find ttbar
    const reco::GenParticle *top = 0;
    const reco::GenParticle *antitop = 0;
    for(std::vector<reco::GenParticle>::const_iterator iGen = genParticles.begin(); iGen != genParticles.end(); ++iGen) {
      const reco::GenParticle *gen = &(*iGen);
      if(std::abs(gen->pdgId()) != 6)
        continue;

      if(gen->pdgId() == 6) {
        if(top) {
          //std::cout << "Top already found" << std::endl;
          return kTT_noTT;
        }
        top = gen;
      }
      else {
        if(antitop) {
          //std::cout << "Anti-top already found" << std::endl;
          return kTT_noTT;
        }
        antitop = gen;
      }

      if(top && antitop) break;
    }
    if(!top || !antitop) {
      //std::cout << "Either top (" << top << ") or anti-top (" << antitop << ") not found" << std::endl;
      return kTT_noTT;
    }

    top = GenParticleTools::rewindChainDown(top);
    antitop = GenParticleTools::rewindChainDown(antitop);

    const reco::GenParticle *topW = GenParticleTools::findMaxNonNeutrinoDaughter(top);
    const reco::GenParticle *antitopW = GenParticleTools::findMaxNonNeutrinoDaughter(antitop);

    if(std::abs(topW->pdgId()) != 24 || std::abs(antitopW->pdgId()) != 24) {
      //std::cout << "Daughter of top (" << topW->pdgId() << ") or anti-top (" << antitopW->pdgId() << " not W (24)" << std::endl;
      return kTT_noTT;
    }

    int n_q = 0;
    int n_e = 0;
    int n_mu = 0;
    int n_tau = 0;

    /*
    std::cout << "topW numberOfDaughters " << topW->numberOfDaughters()
              << " anti-topW numberOfDaughters " << antitopW->numberOfDaughters()
              << std::endl;
    */

    size_t n = topW->numberOfDaughters();
    for(size_t i=0; i<n; ++i) {
      switch(std::abs(topW->daughter(i)->pdgId())) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
      case 6:
        ++n_q; break;
      case 11: ++n_e; break;
      case 13: ++n_mu; break;
      case 15: ++n_tau; break;
      default:
        //std::cout << "Daughter of top->W " << topW->daughter(i)->pdgId() << std::endl;
        break;
      };
    }
    n = antitopW->numberOfDaughters();
    for(size_t i=0; i<n; ++i) {
      switch(std::abs(antitopW->daughter(i)->pdgId())) {
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
      case 6:
        ++n_q; break;
      case 11: ++n_e; break;
      case 13: ++n_mu; break;
      case 15: ++n_tau; break;
      default:
        //std::cout << "Daughter of anti-top->W " << topW->daughter(i)->pdgId() << std::endl;
        break;
      };
    }
    if(!(n_q == 0 || n_q == 2 || n_q == 4))
      throw cms::Exception("Assert") << __FILE__ << ":" << __LINE__ << ": Something weird is going on, got " << n_q << " quarks";
    n_q = n_q/2;

    if(n_q + n_e + n_mu + n_tau != 2)
      throw cms::Exception("Assert") << __FILE__ << ":" << __LINE__ << ": Something weird is going on, got " << n_q << " quark pairs, " << n_e << " electrons, " << n_mu << " muons, and " << n_tau << " taus.";

    if(n_q == 2)
      return kTT_bbqqqq;
    if(n_e == 2)
      return kTT_bbee;
    if(n_mu == 2)
      return kTT_bbmumu;
    if(n_tau == 2)
      return kTT_bbtautau;
    if(n_q == 1) {
      if(n_e == 1)
        return kTT_bbqqe;
      if(n_mu == 1)
        return kTT_bbqqmu;
      if(n_tau == 1)
        return kTT_bbqqtau;
    }
    if(n_e == 1) {
      if(n_mu == 1)
        return kTT_bbemu;
      if(n_tau == 1)
        return kTT_bbetau;
    }
    if(n_mu == 1)
      if(n_tau == 1)
        return kTT_bbmutau;

    return kTT_unknown;
  }


  /*

  std::vector<const reco::GenParticle*> GenParticleAnalysis::getImmediateMothers(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> mothers;
    for (size_t im=0; im < p.numberOfMothers(); ++im){
      const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
      if (mparticle) mothers.push_back(mparticle);
    }
    return mothers;
  }

  std::vector<const reco::GenParticle*> GenParticleAnalysis::getMothers(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> mothers;
    for (size_t im=0; im < p.numberOfMothers(); ++im){
      const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
      if (mparticle) { 
        mothers.push_back(mparticle);
        std::vector<const reco::GenParticle*> mmothers = getMothers( * (dynamic_cast<const reco::Candidate*> (mparticle)) );
        mothers.insert(mothers.end(), mmothers.begin(), mmothers.end()); 
      }
    }
    return mothers;
  }
  
  bool GenParticleAnalysis::hasImmediateMother(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
    for (size_t im=0; im < mothers.size(); ++im){
      if (mothers[im]->pdgId() == id) return true;
    }
    return false;
  }  
  
  bool GenParticleAnalysis::hasMother(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> mothers = getMothers(p);
    for (size_t im=0; im < mothers.size(); ++im){
      if (mothers[im]->pdgId() == id) return true;
    }
    return false;
  }  

  void GenParticleAnalysis::printImmediateMothers(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
    std::cout << "Immediate mothers of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < mothers.size(); ++im){
      std::cout << "  " << mothers[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  

  void GenParticleAnalysis::printMothers(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> mothers = getMothers(p);
    std::cout << "Mothers of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < mothers.size(); ++im){
      std::cout << "  " << mothers[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  

  std::vector<const reco::GenParticle*> GenParticleAnalysis::getImmediateDaughters(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> daughters;
    for (size_t im=0; im < p.numberOfDaughters(); ++im){
      const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.daughter(im));
      if (dparticle) daughters.push_back(dparticle);
    }
    return daughters;
  }

  std::vector<const reco::GenParticle*> GenParticleAnalysis::getDaughters(const reco::Candidate& p){ 
    std::vector<const reco::GenParticle*> daughters;
    for (size_t im=0; im < p.numberOfDaughters(); ++im){
      const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.daughter(im));
      if (dparticle) {
        daughters.push_back(dparticle);
        std::vector<const reco::GenParticle*> ddaughters = getDaughters( * (dynamic_cast<const reco::Candidate*> (dparticle)) );
        daughters.insert(daughters.end(), ddaughters.begin(), ddaughters.end()); 
      }
    }
    return daughters;
  }
  
    bool GenParticleAnalysis::hasImmediateDaughter(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
    for (size_t im=0; im < daughters.size(); ++im){
      if (daughters[im]->pdgId() == id) return true;
    }
    return false;
  }
  
  bool GenParticleAnalysis::hasDaughter(const reco::Candidate& p, int id){
    std::vector<const reco::GenParticle*> daughters = getDaughters(p);
    for (size_t im=0; im < daughters.size(); ++im){
      if (daughters[im]->pdgId() == id) return true;
    }
    return false;
  }
  
  void GenParticleAnalysis::printImmediateDaughters(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
    std::cout << "Immediate daughters of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < daughters.size(); ++im){
      std::cout << "  " << daughters[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  
  
  void GenParticleAnalysis::printDaughters(const reco::Candidate& p){
    std::vector<const reco::GenParticle*> daughters = getDaughters(p);
    std::cout << "Daughters of " << p.pdgId() << ":" << std::endl;
    for (size_t im=0; im < daughters.size(); ++im){
      std::cout << "  " << daughters[im]->pdgId() << std::endl;
    }
    std::cout << std::endl;
  }  


  std::vector<const reco::Candidate*> GenParticleAnalysis::doQCDmAnalysis(const edm::Event& iEvent, const edm::EventSetup& iSetup ){

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    std::vector<const reco::Candidate*> genBquarks;
  
    // b-quark analysis
    int nBquarks = 0;
    int nStatus2Bquarks = 0;
    int nStatus3Bquarks = 0;

    /// Loop over all genParticles
    for (size_t i=0; i < genParticles->size(); ++i){  
      const reco::Candidate & p = (*genParticles)[i];
      int id = p.pdgId();
      
      if ( abs(id) != 5 ) continue;
      nBquarks++;
      if (p.status() == 2) nStatus2Bquarks++;
      if (p.status() == 3) nStatus3Bquarks++;
      
      genBquarks.push_back(&p);
      
    } //eof:  for 
    hBquarkMultiplicity->Fill(nBquarks);
    hBquarkStatus2Multiplicity ->Fill(nStatus2Bquarks);
    hBquarkStatus3Multiplicity ->Fill(nStatus3Bquarks);
    
    return genBquarks;
  }
  */
  
}
