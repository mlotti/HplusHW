#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MCAnalysisOfSelectedEvents.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

#include <limits>

namespace HPlus {
  MCAnalysisOfSelectedEvents::Data::Data() { }
  
  MCAnalysisOfSelectedEvents::Data::~Data() {}

  MCAnalysisOfSelectedEvents::MCAnalysisOfSelectedEvents(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fOneProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneProngTauSrc")),
    fOneAndThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneAndThreeProngTauSrc")),
 
  
    fElectronNotInTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Electron not in tau")),
    fElectronNotInTauFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "W->Electron not in tau")),
    fElectronNotInTauFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Bottom->Electron not in tau")),
    fElectronNotInTauFromTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau->Electron not in tau")),

    fMuonNotInTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Muon not in tau")),
    fMuonNotInTauFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "W->Muon not in tau")),
    fMuonNotInTauFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Bottom->Muon not in tau")),
    fMuonNotInTauFromTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau->Muon not in tau")),

    fTauNotInTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau not in tau")),
    fTauNotInTauFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "W->Tau not in tau")),
    fTauNotInTauFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Bottom->Tau not in tau")),
    fTauNotInTauFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Hplus->tau not in tau")),

    fElectronOrMuonFoundCounter(eventCounter.addSubCounter("MCinfo for selected events", "Electron or muon found")),
    fNoElectronOrMuonFoundCounter(eventCounter.addSubCounter("MCinfo for selected events", "No electron or muon found")),
    fNoElectronOrMuonFoundRealTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "No electron or muon found, real tau")),

    fLeptonFoundCounter(eventCounter.addSubCounter("MCinfo for selected events", "Electron, muon or tau found")),
    fNoLeptonFoundCounter(eventCounter.addSubCounter("MCinfo for selected events", "No electron, muon or tau found")),
    fNoLeptonFoundRealTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "No electron, muon, tau found, real tau")),   

    fObservableMuonsCounter(eventCounter.addSubCounter("MCinfo for selected events", "Observable associated muons")),
    fObservableElectronsCounter(eventCounter.addSubCounter("MCinfo for selected events", "Observable associated electrons")),
    fObservableTausCounter(eventCounter.addSubCounter("MCinfo for selected events", "Observable associated taus")),

    fTauIsHadronFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->hadrons")),
    fTauIsElectronFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->electron")),
    fTauIsMuonFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->muon")),
    fTauIsQuarkFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->qq")),
    fTauIsQuarkFromZCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->qq")),
    fTauIsElectronFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->e")),
    fTauIsElectronFromZCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->e")),
    fTauIsMuonFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->mu")),
    fTauIsHadronFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->hadrons")),
    fTauIsElectronFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->e")),
    fTauIsMuonFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->mu")),
    fTauIsMuonFromZCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->mu")),
    fTauIsHadronFromZTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->tau->hadrons")),
    fTauIsElectronFromZTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->tau->e")),
    fTauIsMuonFromZTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->tau->mu")),
    fTauIsElectronFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->e")),
    fTauIsMuonFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->mu")),
    fTauIsHadronFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->hadron")),
    fTauIsElectronFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->e")),
    fTauIsMuonFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->mu")),
    fTauIsHadronFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->hadron"))
  {

    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("MCAnalysisOfSelectedEvents");
    hGenMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genMET", "genMET", 200, 0., 400.);
    hdeltaPhiMetGenMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir , "deltaPhiMetGenMet", "deltaPhiMetGenMet", 180, 0., 180.); 
    hdeltaEtMetGenMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "deltaEtMetGenMet", "deltaEtMetGenMet", 200, -1., 1.);
    hgenWmass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "genWmass", "genWmass", 200, 0.,400.); 
    htransverseMassAll = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassAll", "transverseMassAll;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassMuonNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassMuonNotInTau", "transverseMassMuonNotInTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassElectronNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassElectronNotInTau", "transverseMassElectronNotInTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassElectronFromW = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassElectronFromW", "transverseMassElectronFromW;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassElectronFromBottom = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassElectronFromBottom", "transverseMassElectronFromBottom0;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassElectronFromTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "transverseMassElectronFromTau", "transverseMassElectronFromTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassMuonFromW = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassMuomFromW", "transverseMassMuonFromW;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassMuonFromBottom = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassMuomFromBottom", "transverseMassMuonFromBottom;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassMuonFromTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassMuomFromTau", "transverseMassMuonFromTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassTauNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassTauNotInTau", "transverseMassTauNotInTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassMetReso02 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassMetReso02", "transverseMassMetReso02;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 100, 0., 500.);
    htransverseMassLeptonNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassLeptonNotInTau", "transverseMassLeptonNotInTau", 100, 0., 500.);
    htransverseMassNoLeptonNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassNoLeptonNotInTau", "transverseMassNoLeptonNotInTau", 100, 0., 500.);
    htransverseMassLeptonRealSignalTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "transverseMassLeptonRealSignalTau", "transverseMassLeptonRealSignalTau", 100, 0., 500.);
    htransverseMassNoLeptonRealSignalTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassNoLeptonRealSignalTau", "transverseMassNoLeptonRealSignalTau", 100, 0., 500.);
    htransverseMassElMuNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassElMuNotInTau", "transverseMassElMuNotInTau", 100, 0., 500.);
    htransverseMassNoElMuNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassNoElMuNotInTau", "transverseMassNoElMuNotInTau", 100, 0., 500.);
    htransverseMassNoElMuRealSignalTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassNoElMuRealSignalTau", "transverseMassNoElMuRealSignalTau", 100, 0., 500.);
    htransverseMassLeptonFakeSignalTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassLeptonFakeSignalTau", "transverseMassLeptonFakeSignalTau", 100, 0., 500.);
    htransverseMassNoLeptonGoodMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassNoLeptonGoodMet", "transverseMassNoLeptonGoodMet", 100, 0., 500.);
    htransverseMassNoLeptonGoodMetGoodTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassNoLeptonGoodMetGoodTau", "transverseMassNoLeptonGoodMetGoodTau", 100, 0., 500.);
    htransverseMassNoObservableLeptons= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseNoMassObservableLeptons", "transverseMassNoObservableLeptons", 100, 0., 500.);
    htransverseMassObservableLeptons= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,  myDir, "transverseMassObservableLeptons", "transverseMassObservableLeptons", 100, 0., 500.);
    

  }

  MCAnalysisOfSelectedEvents::~MCAnalysisOfSelectedEvents() {}

  void MCAnalysisOfSelectedEvents::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData ) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    
    return privateAnalyze(iEvent, iSetup, tauData, metData, genData);
  }
  
  void MCAnalysisOfSelectedEvents::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData ) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, tauData, metData, genData);
  }
  
  
  
  void MCAnalysisOfSelectedEvents::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData ) {
    
    //    if (iEvent.isRealData()) continue;
    
    // Origin and type of selected tau
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);

    typedef math::XYZTLorentzVectorD LorentzVector;
    typedef std::vector<LorentzVector> LorentzVectorCollection;


    edm::Handle <std::vector<LorentzVector> > oneProngTaus;
    iEvent.getByLabel(fOneProngTauSrc, oneProngTaus); 

    edm::Handle <std::vector<LorentzVector> > oneAndThreeProngTaus;
    iEvent.getByLabel(fOneAndThreeProngTauSrc,oneAndThreeProngTaus);

  

    bool myTauFoundStatus = false;
    bool myLeptonVetoStatus = false;
    bool otherTauFound = false;
    bool otherHadronicTauFound = false;
    bool tauFromWFound = false;
    bool tauFromBottomFound = false;
    bool electronFound = false;
    bool electronFromWFound = false;
    bool electronFromBottomFound = false;
    bool electronFromTauFound = false;
    bool muonFound = false;
    bool muonFromWFound = false;
    bool muonFromBottomFound = false;
    bool muonFromTauFound = false;
    bool observableOtherTauFound = false;
    bool observableOtherHadronicTauFound = false;
    bool observableElectronFound = false;
    bool observableMuonFound = false;

    hGenMET->Fill(genData.getGenMET()->pt());
    double deltaPhiMetGenMet = DeltaPhi::reconstruct(*(genData.getGenMET()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hdeltaPhiMetGenMet->Fill(deltaPhiMetGenMet);
    hdeltaEtMetGenMet->Fill((genData.getGenMET()->pt() - metData.getSelectedMET()->pt())/genData.getGenMET()->pt());

    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    if ((fabs(genData.getGenMET()->pt() - metData.getSelectedMET()->pt())/genData.getGenMET()->pt()) > 0.2) {
      htransverseMassMetReso02->Fill(transverseMass);
    }

    
    reco::GenParticle parton;
    reco::GenParticle otherTau;
    reco::GenParticle electron;
    reco::GenParticle muon;

    double minDeltaR = 99999;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (p.pt() > 5 && p.pdgId()!= std::abs(p.pdgId()) ) {
     
        if (reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4()) < 0.3) {
	  if ((hasImmediateMother(p,15) || hasImmediateMother(p,-15)) && (std::abs(p.pdgId()) != 11 || std::abs(p.pdgId()) != 13 )) {
	    myTauFoundStatus = true;
	  }
	}

	if (reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4()) > 0.5 ) {
	  
	  // non-signal taus
	  if ((hasImmediateMother(p,15) || hasImmediateMother(p,-15)) && (std::abs(p.pdgId()) != 11 || std::abs(p.pdgId()) != 13 )) 
	    //if (std::abs(p.pdgId()) == 15 && !hasImmediateMother(p,15) && !hasImmediateMother(p,-15) ) {
	    // hadronic taus
	    for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
	      double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	      if ( deltaR > 0.3) continue;
	      // if (hasImmediateDaughter(p,11) || !hasImmediateDaughter(p,-13) ) continue;	
	      //	      increment(fTauNotInTauCounter);
	      otherTau = (*genParticles)[i]; 
	      otherTauFound = true;
	      //if (hasImmediateMother(p,24) || hasImmediateMother(p,-24) )   tauFromWFound = true;
	      std::vector<const reco::GenParticle*> tauMothers = getMothers(otherTau); 
	      for(size_t d=0; d< tauMothers.size(); ++d) {
		const reco::GenParticle dparticle = *tauMothers[d];
		if( abs(dparticle.pdgId()) == 24 ) tauFromWFound = true; 
		//		if( abs(dparticle.pdgId()) == 24 ) std::cout << " W mass " << dparticle.mass() << std::endl;
		if( abs(dparticle.pdgId()) == 24 ) hgenWmass->Fill(dparticle.mass());
		if( abs(dparticle.pdgId()) == 5 ) tauFromBottomFound = true;
		if( abs(dparticle.pdgId()) == 37 ) increment(fTauNotInTauFromHplusCounter); 	
	      }
	      if ( tau->pt() < 15 || fabs(tau->eta()) > 2.4 ) continue;
	      //increment(fObservableTausCounter);
	      observableOtherTauFound = true;
	    }
	}
	
	
	// electrons 
	if (std::abs(p.pdgId()) == 11 && !hasImmediateMother(p,11) && !hasImmediateMother(p,-11)) {
	  //	  increment(fElectronNotInTauCounter);
	  electronFound = true;
	  electron = (*genParticles)[i]; 
	  if (hasImmediateMother(p,24) || hasImmediateMother(p,-24) )  electronFromWFound = true;
	  if (hasImmediateMother(p,15) || hasImmediateMother(p,-15) )  electronFromTauFound = true;

	  std::vector<const reco::GenParticle*> electronMothers = getMothers(electron); 
	  for(size_t d=0; d<electronMothers.size(); ++d) {
	    const reco::GenParticle dparticle = *electronMothers[d];
	    if( abs(dparticle.pdgId()) == 24 ) {
	      //  increment(fElectronNotInTauFromWCounter);
	      //   electronFromWFound = true;
	    }
	    if( abs(dparticle.pdgId()) == 5 ) {
	      //increment(fElectronNotInTauFromBottomCounter);
	      electronFromBottomFound = true;
	    }
	    if( abs(dparticle.pdgId()) == 15 ) {
	      //increment(fElectronNotInTauFromTauCounter); 	
	      //electronFromTauFound = true;
	    }
	  }
	  if ( p.pt() < 15 || fabs(p.eta()) > 2.4 ) continue;
	  //increment(fObservableElectronsCounter);
	  observableElectronFound = true;
	}
	
	// muons
	if (std::abs(p.pdgId()) == 13 && !hasImmediateMother(p,13) && !hasImmediateMother(p,-13) ) {
	  //increment(fMuonNotInTauCounter);
	   muonFound = true;
	  muon = (*genParticles)[i];
	  if (hasImmediateMother(p,24) || hasImmediateMother(p,-24) )  muonFromWFound = true;
	  if (hasImmediateMother(p,15) || hasImmediateMother(p,-15) )  muonFromTauFound = true;

	  std::vector<const reco::GenParticle*> muonMothers = getMothers(muon);
	  
	  for(size_t d=0; d< muonMothers.size(); ++d) {
	    const reco::GenParticle dparticle = *muonMothers[d];
	    if( abs(dparticle.pdgId()) == 24 ) {
	      //increment(fMuonNotInTauFromWCounter);
	      // muonFromWFound = true;
	    }
	    if( abs(dparticle.pdgId()) == 5 ) {
	      //increment(fMuonNotInTauFromBottomCounter);
	      muonFromBottomFound = true;
	    }
	    if( abs(dparticle.pdgId()) == 15 ) {
	      //muonFromTauFound = true;
	      //increment(fMuonNotInTauFromTauCounter);
	    }
	  }
	  if ( p.pt() < 15 || fabs(p.eta()) > 2.4 ) continue;
	  //increment(fObservableMuonsCounter);
	  observableMuonFound = true;
	}
      }
      
      double deltaR = reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4());
      if (deltaR < minDeltaR) {
	minDeltaR = deltaR;
	parton = (*genParticles)[i];
      }
    }
  
    if ( otherTauFound && !muonFromTauFound && !electronFromTauFound) otherHadronicTauFound = true;
    if ( observableOtherTauFound && !muonFromTauFound && !electronFromTauFound) observableOtherHadronicTauFound = true;


    htransverseMassAll->Fill(transverseMass); 
    // origin of leptons (not in tau)
    if (electronFound) {
      if (transverseMass>100) increment(fElectronNotInTauCounter);
      htransverseMassElectronNotInTau->Fill(transverseMass);
    }
    if (electronFromWFound && !electronFromBottomFound) {
      if (transverseMass>100) increment(fElectronNotInTauFromWCounter);
      htransverseMassElectronFromW->Fill(transverseMass);
    }
    if (electronFromBottomFound ) {
      if (transverseMass>100) increment(fElectronNotInTauFromBottomCounter);
      htransverseMassElectronFromBottom->Fill(transverseMass);
    }
    if (electronFromTauFound) {
      if (transverseMass>100) increment(fElectronNotInTauFromTauCounter);
      htransverseMassElectronFromTau->Fill(transverseMass);
    }
    if (muonFound) {
      if (transverseMass>100) increment(fMuonNotInTauCounter);
      htransverseMassMuonNotInTau->Fill(transverseMass);
    }
    if (muonFromWFound && !muonFromBottomFound) {
      if (transverseMass>100) increment(fMuonNotInTauFromWCounter);
      htransverseMassMuonFromW->Fill(transverseMass);
    }
    if (muonFromBottomFound) {
      if (transverseMass>100) increment(fMuonNotInTauFromBottomCounter);
      htransverseMassMuonFromBottom->Fill(transverseMass);
    }
    if (muonFromTauFound) {
      if (transverseMass>100) increment(fMuonNotInTauFromTauCounter);
      htransverseMassMuonFromTau->Fill(transverseMass);
    }

    if (otherHadronicTauFound ) {
      if (transverseMass>100) increment(fTauNotInTauCounter);
      if (transverseMass>100 && tauFromWFound) increment(fTauNotInTauFromWCounter);
      if (transverseMass>100 && tauFromBottomFound) increment(fTauNotInTauFromBottomCounter);
      htransverseMassTauNotInTau->Fill(transverseMass);
    }

    if (otherTauFound || electronFound || muonFound ) {
      if (transverseMass>100) increment(fLeptonFoundCounter);
      htransverseMassLeptonNotInTau->Fill(transverseMass);
      if (myTauFoundStatus ) htransverseMassLeptonRealSignalTau->Fill(transverseMass);
      if (!myTauFoundStatus ) htransverseMassLeptonFakeSignalTau->Fill(transverseMass); 
    }

    if (electronFound || muonFound ) {
      if (transverseMass>100) increment(fElectronOrMuonFoundCounter);
      htransverseMassElMuNotInTau->Fill(transverseMass);
    }


    if (!otherTauFound && !electronFound && !muonFound ) {
      if (transverseMass>100) increment(fNoLeptonFoundCounter);
      htransverseMassNoLeptonNotInTau->Fill(transverseMass);
    }
   
    if (!electronFound && !muonFound ) {
      if (transverseMass>100) increment(fNoElectronOrMuonFoundCounter);
      htransverseMassNoElMuNotInTau->Fill(transverseMass);
    }

    if (!otherTauFound && !electronFound && !muonFound && myTauFoundStatus ) {
     if (transverseMass>100) increment(fNoLeptonFoundRealTauCounter);
      htransverseMassNoLeptonRealSignalTau->Fill(transverseMass);
    }
   
   if (!electronFound && !muonFound && myTauFoundStatus ) {
     if (transverseMass>100) increment(fNoElectronOrMuonFoundRealTauCounter);
      htransverseMassNoElMuRealSignalTau->Fill(transverseMass);
    }

   if (transverseMass > 100) {
     if (observableMuonFound ) increment(fObservableMuonsCounter);
     if (observableElectronFound ) increment(fObservableElectronsCounter);
     if ( observableOtherHadronicTauFound ) increment(fObservableTausCounter);
   }

    if ( observableOtherHadronicTauFound || observableElectronFound || observableMuonFound ) {
      htransverseMassObservableLeptons->Fill(transverseMass);
    }

    if (!observableOtherHadronicTauFound  && !observableElectronFound && !observableMuonFound ) {                                                                                                          
      htransverseMassNoObservableLeptons->Fill(transverseMass);
    }

    if ((fabs(genData.getGenMET()->pt() - metData.getSelectedMET()->pt())/genData.getGenMET()->pt()) < 0.2) {
      if (!otherTauFound && !electronFound && !muonFound ) {
	htransverseMassNoLeptonGoodMet->Fill(transverseMass);
	if (myTauFoundStatus ) {
	  htransverseMassNoLeptonGoodMetGoodTau->Fill(transverseMass);
	}
      }
    }

    std::vector<const reco::GenParticle*> mothers = getMothers(parton);
    int motherId=9999;      
    bool wInMothers = false;
    bool zInMothers = false;
    bool topInMothers = false;
    bool bottomInMothers = false;
    bool tauInMothers = false;
    bool hplusInMothers = false;

    for(size_t d=0; d<mothers.size(); ++d) {
      const reco::GenParticle dparticle = *mothers[d];
      motherId = dparticle.pdgId();
      if( abs(motherId) == 24 ) wInMothers = true; 
      if( abs(motherId) == 23 ) zInMothers = true; 
      if( abs(motherId) == 6 ) topInMothers = true;
      if( abs(motherId) == 5 ) bottomInMothers = true;
      if( abs(motherId) == 15 ) tauInMothers = true;
      if( abs(motherId) == 37 ) hplusInMothers = true;
            
    }

    bool FromBottom = false;
    bool FromJet = false;    
    bool FromHplusTau = false;
    bool FromWTau = false;
    bool FromW = false;
    bool FromZTau = false;
    bool FromZ = false;
    
    if (bottomInMothers && !wInMothers && !zInMothers  ) FromBottom = true;
    if (!bottomInMothers && !wInMothers && !hplusInMothers && !zInMothers ) FromJet = true;
    if (hplusInMothers && tauInMothers ) FromHplusTau = true;
    if (wInMothers && tauInMothers ) FromWTau = true;
    if (zInMothers && tauInMothers ) FromZTau = true;
    if (wInMothers && !tauInMothers ) FromW = true;
    if (zInMothers && !tauInMothers ) FromZ = true;

    if (FromBottom && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromBottomCounter);
    if (FromBottom && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromBottomCounter);
    if (FromBottom && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromBottomCounter);
    

    if (FromJet && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromJetCounter); 
    if (FromJet && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromJetCounter);
    if (FromJet && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11)  increment(fTauIsHadronFromJetCounter);

    //      if (hplusInMothers && std::abs(parton.pdgId()) == 15 ) tauFromHplus = true;
    if (hplusInMothers && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromHplusCounter);
    if (hplusInMothers && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromHplusCounter);
    if (hplusInMothers && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromHplusCounter);

    if (FromW && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromWCounter);
    if (FromW && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromWCounter);
    if (FromW && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsQuarkFromWCounter);

    if (FromWTau && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromWTauCounter);
    if (FromWTau && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromWTauCounter);
    if (FromWTau && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromWTauCounter);

    if (FromZ && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromZCounter);
    if (FromZ && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromZCounter);
    if (FromZ && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsQuarkFromZCounter);

    if (FromZTau && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromZTauCounter);
    if (FromZTau && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromZTauCounter);
    if (FromZTau && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromZTauCounter);

 
 
  }

}
