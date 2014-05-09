#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TMath.h"
#include "TLorentzVector.h"

namespace HPlus {
  VetoTauSelection::Data::Data() :
  fPassedEvent(false) { }

  VetoTauSelection::Data::~Data() { }
  
  VetoTauSelection::VetoTauSelection(const edm::ParameterSet& iConfig, const edm::ParameterSet& fakeTauSFandSystematicsConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper) :
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fOneProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneProngTauSrc")),
    fOneAndThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneAndThreeProngTauSrc")),
    fThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("threeProngTauSrc")),
    fZMass(iConfig.getUntrackedParameter<double>("Zmass")),
    fZMassWindow(iConfig.getUntrackedParameter<double>("ZmassWindow")),
    fTauSource(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection").getUntrackedParameter<edm::InputTag>("src")),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, histoWrapper, "TauVeto"),
    fFakeTauIdentifier(fakeTauSFandSystematicsConfig, iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), histoWrapper, "VetoTauSelection"),
    fAllEventsCounter(eventCounter.addSubCounter("VetoTauSelection","All events")),
    //    fVetoTauCandidatesCounter(eventCounter.addSubCounter("VetoTauSelection","Veto tau candidates"));
    fVetoTausSelectedCounter(eventCounter.addSubCounter("VetoTauSelection","Veto taus found")),
    fEventsCompatibleWithZMassCounter(eventCounter.addSubCounter("VetoTauSelection","Z mass compatible ditau found")),
    fSelectedEventsCounter(eventCounter.addSubCounter("VetoTauSelection","Selected events")) {
    // Initialise histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("VetoTauSelection");

    hCandidateTauNumber = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "CandidateTauNumber", "CandidateTauNumber;Number of veto #tau candidates;Jets", 4, 0, 4);
    if (hCandidateTauNumber->isActive()) {
      hCandidateTauNumber->GetXaxis()->SetBinLabel(1, "Genuine #tau");
      hCandidateTauNumber->GetXaxis()->SetBinLabel(2, "e#rightarrow#tau");
      hCandidateTauNumber->GetXaxis()->SetBinLabel(3, "#mu#rightarrow#tau");
      hCandidateTauNumber->GetXaxis()->SetBinLabel(4, "jet#rightarrow#tau");
    }
    hSelectedTauNumber = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedTauNumber", "SelectedTauNumber;Number of selected veto #tau jets;Jets", 4, 0, 4);
    if (hSelectedTauNumber->isActive()) {
      for (int i = 1; i <= hCandidateTauNumber->getHisto()->GetNbinsX(); ++i)
        hSelectedTauNumber->GetXaxis()->SetBinLabel(i, hCandidateTauNumber->GetXaxis()->GetBinLabel(i));
    }
    hTauCandFromWPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauCandFromWPt", "TauCandFromWPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hTauCandAllPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauCandAllPt", "TauCandAllPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedGenuineTauByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedGenuineTauByPt", "SelectedGenuineTauByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedGenuineTauByEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedGenuineTauByEta", "SelectedGenuineTauByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hSelectedGenuineTauByPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedGenuineTauByPhi", "SelectedGenuineTauByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hSelectedFakeTauByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedFakeTauByPt", "SelectedFakeTauByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedFakeTauByEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedFakeTauByEta", "SelectedFakeTauByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hSelectedFakeTauByPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedFakeTauByPhi", "SelectedFakeTauByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hSelectedGenuineTauDiTauMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedGenuineTauDitauMass", "SelectedGenuineTauDitauMass;M_{#tau#tau}, GeV/c^{2};Events / 5 GeV/c^{2}", 50, 0, 250);
    hSelectedFakeTauDiTauMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedFakeTauDitauMass", "SelectedFakeTauDitauMass;M_{#tau#tau}, GeV/c^{2};Events / 5 GeV/c^{2}", 50, 0, 250);
    hSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "SelectedTausPerEvent", "SelectedTausPerEvent", 10, 0, 10);
  }

  VetoTauSelection::~VetoTauSelection() {}

  VetoTauSelection::Data VetoTauSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau, double vertexZ) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, selectedTau, vertexZ);
  }

  VetoTauSelection::Data VetoTauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau, double vertexZ) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, selectedTau, vertexZ);
  }

  VetoTauSelection::Data VetoTauSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau, double vertexZ) {
    Data output;

    increment(fAllEventsCounter);

    // Obtain tau collection as the veto tau candidates and take out selected tauSelection
    edm::Handle<edm::View<pat::Tau> > myTaus;
    iEvent.getByLabel(fTauSource, myTaus);
    edm::PtrVector<pat::Tau> myVetoTauCandidates;
    for (edm::PtrVector<pat::Tau>::iterator it = myTaus->ptrVector().begin(); it != myTaus->ptrVector().end(); ++it) {
      if (reco::deltaR(*selectedTau, **it) > 0.2)
        myVetoTauCandidates.push_back(*it);
    }


  
// Obtain tau collection as the veto tau candidates and take out selected tauSelection
    if (!iEvent.isRealData()) {

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

      //      edm::Handle<edm::View<reco::Vertex> > hvertex;
      //     iEvent.getByLabel(pvSrc_, hvertex);
      //     thePV_ = hvertex->ptrAt(0); 
      
      //     std::cout << " hadronic taus  " << oneAndThreeProngTaus.size() << std::endl;	       
      for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {  
	bool tauFromHiggs = false;
	bool tauFromW = false;
	bool tauCandFromW = false;	
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
	  
	  for (edm::PtrVector<pat::Tau>::iterator it = myVetoTauCandidates.begin(); it != myVetoTauCandidates.end(); ++it) {
	    double deltaR = reco::deltaR( *tau, **it);
	    if ( deltaR < 0.2 && tauFromW) {
	      tauCandFromW = true;
	      hTauCandFromWPt->Fill((*it)->pt()); 
	    }
	  }
	}
      }

      
 
      /*           
      for (edm::PtrVector<pat::Tau>::iterator it = myTaus->ptrVector().begin(); it != myTaus->ptrVector().end(); ++it) {
	if (reco::deltaR(*selectedTau, **it) < 0.4 ) continue;        
	bool tauCandFromW = false;	
	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();
	  if ( abs(id) != 15 || hasImmediateMother(p,15) || hasImmediateMother(p,-15) )continue;
	  //	  if(hasImmediateMother(p,24) || hasImmediateMother(p,-24)) {
	  printImmediateMothers(p);
	  //	  std::cout << " b quarks " << id <<  " idHiggsSide " <<   idHiggsSide << std::endl;
	  //	       double deltaR = ROOT::Math::VectorUtil::DeltaR(Jetb->p4(),p.p4() );
	  double deltaR = reco::deltaR(p.p4(), **it);	
	  if ( deltaR < 0.4) tauCandFromW = true;
	  // }
	} 
    std::cout << " tauCandFromW " << tauCandFromW << std::endl; 
      }
      */          
    }



    // Count how many taus (excluding the selected tau) are available in the event
    for (edm::PtrVector<pat::Tau>::iterator it = myVetoTauCandidates.begin(); it != myVetoTauCandidates.end(); ++it) {
      //     increment(fVetoTauCandidatesCounter);
      hTauCandAllPt->Fill((*it)->pt()); 
      //      double ptLead = (*it)->leadTrack()->pt();
      //      double emfrac = (*it)->emFraction();
      //      double isolSum = (*it)->isolationTracksPtSum();
      //      double myValue = (*it)->userFloat("byTightChargedMaxPt");
      //      double myLdgTrackPt = (*it)->leadPFChargedHadrCand()->pt();
    
     
     
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, **it);
      if (tauMatchData.isGenuineTau())
        hCandidateTauNumber->Fill(0.);
      else if (tauMatchData.isElectronToTau())
        hCandidateTauNumber->Fill(1);
      else if (tauMatchData.isMuonToTau())
        hCandidateTauNumber->Fill(2);
      else if (tauMatchData.isJetToTau())
        hCandidateTauNumber->Fill(3);
    }
    // Do tau selection on the veto tau candidates
    TauSelection::Data myTauData = fTauSelection.analyze(iEvent, iSetup, myVetoTauCandidates, vertexZ);
    //    std::cout << " myVetoTauCandidates   " << myVetoTauCandidates.size() << std::endl;
    if (myTauData.passedEvent())
      increment(fVetoTausSelectedCounter);
    //    std::cout << " myTauData.passedEvent())  " << myTauData.passedEvent()  << std::endl;
    
    // Loop over the selected veto taus
    double numberOfTaus = 0;
    bool myVetoStatus = false;
    TLorentzVector mySelectedTauMomentum;
    mySelectedTauMomentum.SetXYZM(selectedTau->px(), selectedTau->py(), selectedTau->pz(), 1.777);
    for (edm::PtrVector<pat::Tau>::iterator it = myTauData.getSelectedTaus().begin(); it != myTauData.getSelectedTaus().end(); ++it) {
      // Store to result vector

      output.fSelectedVetoTaus.push_back(*it);
      // Count how many selected veto taus are genuine taus
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, **it);
      if (tauMatchData.isGenuineTau())
        hSelectedTauNumber->Fill(0.);
      else if (tauMatchData.isElectronToTau())
        hSelectedTauNumber->Fill(1);
      else if (tauMatchData.isMuonToTau())
        hSelectedTauNumber->Fill(2);
      else if (tauMatchData.isJetToTau())
        hSelectedTauNumber->Fill(3);

      bool isGenuineTau = !(fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()));
      if (isGenuineTau) {
        // Genuine tau
        hSelectedGenuineTauByPt->Fill((*it)->pt());
        hSelectedGenuineTauByEta->Fill((*it)->eta());
        hSelectedGenuineTauByPhi->Fill((*it)->phi());
      } else {
        // Fake tau
        hSelectedFakeTauByPt->Fill((*it)->pt());
        hSelectedFakeTauByEta->Fill((*it)->eta());
        hSelectedFakeTauByPhi->Fill((*it)->phi());
      }
      // Add the taus up and get the ditau mass
      TLorentzVector myVetoTauMomentum;
      myVetoTauMomentum.SetXYZM((*it)->px(), (*it)->py(), (*it)->pz(), 1.777);  
      myVetoTauMomentum += mySelectedTauMomentum;
      double myDitauMass = myVetoTauMomentum.M();
      // Check if ditau mass is compatible with Z mass
      if (myDitauMass <  1000 ) {
	myVetoStatus = true;
	numberOfTaus++;
      }
      
      /*
      if (TMath::Abs(myDitauMass - fZMass) < fZMassWindow) {
	myVetoStatus = true;
      }
      */
      if (isGenuineTau) {
          hSelectedGenuineTauDiTauMass->Fill(myDitauMass);
        } else {
          hSelectedFakeTauDiTauMass->Fill(myDitauMass);
      }
    }
    //    if (myTauData.passedEvent()) myVetoStatus = true;
    hSelectedTaus->Fill(numberOfTaus);
    // Return the end result
    if (myVetoStatus)
      increment(fEventsCompatibleWithZMassCounter);
    else
      increment(fSelectedEventsCounter);
    output.fPassedEvent = !myVetoStatus;
    return output;
  }
}
