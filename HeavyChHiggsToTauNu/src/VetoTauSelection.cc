#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TMath.h"
#include "TH1.h"
#include "TLorentzVector.h"



std::vector<const reco::GenParticle*>   getImmediateMothers(const reco::Candidate&);
std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);
bool  hasImmediateMother(const reco::Candidate& p, int id);
bool  hasMother(const reco::Candidate& p, int id);
void  printImmediateMothers(const reco::Candidate& p);
void  printMothers(const reco::Candidate& p);
std::vector<const reco::GenParticle*>  getImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*>   getDaughters(const reco::Candidate& p);
bool  hasImmediateDaughter(const reco::Candidate& p, int id);
bool  hasDaughter(const reco::Candidate& p, int id);
void  printImmediateDaughters(const reco::Candidate& p);
void printDaughters(const reco::Candidate& p);


namespace HPlus {
  VetoTauSelection::Data::Data(const VetoTauSelection *vetoTauSelection, bool passedEvent) :
  fVetoTauSelection(vetoTauSelection), fPassedEvent(passedEvent) { }

  VetoTauSelection::Data::~Data() { }
  
  VetoTauSelection::VetoTauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight) :
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fOneProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneProngTauSrc")),
    fOneAndThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneAndThreeProngTauSrc")),
    fThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("threeProngTauSrc")),
    fZMass(iConfig.getUntrackedParameter<double>("Zmass")),
    fZMassWindow(iConfig.getUntrackedParameter<double>("ZmassWindow")),
    fTauSource(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection").getUntrackedParameter<edm::InputTag>("src")),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, "TauVeto"),
    fFakeTauIdentifier(eventWeight, "VetoTauSelection"),
    fEventWeight(eventWeight),
    fAllEventsCounter(eventCounter.addSubCounter("VetoTauSelection","All events")),
    //    fVetoTauCandidatesCounter(eventCounter.addSubCounter("VetoTauSelection","Veto tau candidates"));
    fVetoTausSelectedCounter(eventCounter.addSubCounter("VetoTauSelection","Veto taus found")),
    fEventsCompatibleWithZMassCounter(eventCounter.addSubCounter("VetoTauSelection","Z mass compatible ditau found")),
    fSelectedEventsCounter(eventCounter.addSubCounter("VetoTauSelection","Selected events")) {
    // Initialise histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("VetoTauSelection");
    hCandidateTauNumber = makeTH<TH1F>(myDir, "CandidateTauNumber", "CandidateTauNumber;Number of veto #tau candidates;Jets", 4, 0, 4);
    hCandidateTauNumber->GetXaxis()->SetBinLabel(1, "Genuine #tau");
    hCandidateTauNumber->GetXaxis()->SetBinLabel(2, "e#rightarrow#tau");
    hCandidateTauNumber->GetXaxis()->SetBinLabel(3, "#mu#rightarrow#tau");
    hCandidateTauNumber->GetXaxis()->SetBinLabel(4, "jet#rightarrow#tau");
    hSelectedTauNumber = makeTH<TH1F>(myDir, "SelectedTauNumber", "SelectedTauNumber;Number of selected veto #tau jets;Jets", 4, 0, 4);
    for (int i = 1; i <= hCandidateTauNumber->GetNbinsX(); ++i)
      hSelectedTauNumber->GetXaxis()->SetBinLabel(i, hCandidateTauNumber->GetXaxis()->GetBinLabel(i));
    hTauCandFromWPt = makeTH<TH1F>(myDir, "TauCandFromWPt", "TauCandFromWPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hTauCandAllPt = makeTH<TH1F>(myDir, "TauCandAllPt", "TauCandAllPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedGenuineTauByPt = makeTH<TH1F>(myDir, "SelectedGenuineTauByPt", "SelectedGenuineTauByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedGenuineTauByEta = makeTH<TH1F>(myDir, "SelectedGenuineTauByEta", "SelectedGenuineTauByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hSelectedGenuineTauByPhi = makeTH<TH1F>(myDir, "SelectedGenuineTauByPhi", "SelectedGenuineTauByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hSelectedFakeTauByPt = makeTH<TH1F>(myDir, "SelectedFakeTauByPt", "SelectedFakeTauByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedFakeTauByEta = makeTH<TH1F>(myDir, "SelectedFakeTauByEta", "SelectedFakeTauByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hSelectedFakeTauByPhi = makeTH<TH1F>(myDir, "SelectedFakeTauByPhi", "SelectedFakeTauByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hSelectedGenuineTauDiTauMass = makeTH<TH1F>(myDir, "SelectedGenuineTauDitauMass", "SelectedGenuineTauDitauMass;M_{#tau#tau}, GeV/c^{2};Events / 5 GeV/c^{2}", 50, 0, 250);
    hSelectedFakeTauDiTauMass = makeTH<TH1F>(myDir, "SelectedFakeTauDitauMass", "SelectedFakeTauDitauMass;M_{#tau#tau}, GeV/c^{2};Events / 5 GeV/c^{2}", 50, 0, 250);
    hSelectedTaus= makeTH<TH1F>(myDir, "SelectedTausPerEvent", "SelectedTausPerEvent", 20, 0, 20);
  }

  VetoTauSelection::~VetoTauSelection() {}

  VetoTauSelection::Data VetoTauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, edm::Ptr<reco::Candidate> selectedTau) {
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
	      hTauCandFromWPt->Fill((*it)->pt(), fEventWeight.getWeight()); 
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
      hTauCandAllPt->Fill((*it)->pt(), fEventWeight.getWeight()); 
      //      double ptLead = (*it)->leadTrack()->pt();
      //      double emfrac = (*it)->emFraction();
      //      double isolSum = (*it)->isolationTracksPtSum();
      //      double myValue = (*it)->userFloat("byTightChargedMaxPt");
      //      double myLdgTrackPt = (*it)->leadPFChargedHadrCand()->pt();
      /*
      double minTrackPt = 0.8;
      int minPixelHits = 0;
      int minTrackHits = 3;
      double maxIP = 0.03;
      double maxChi2 = 100;
      double maxDeltaZ = 0.2;
      double minGammaEt = 0.8;
      *sumPt = 0;
      *maxPt = 0;
      *occupancy = 0;
      reco::PFCandidateRefVector allCands = (*it)->isolationPFChargedHadrCands();
      if(allCands.isNonnull()) {
        reco::PFCandidateRefVector chargedCands = TauTagTools::filteredPFChargedHadrCands(allCands,
                                                                                          minTrackPt,
                                                                                          minPixelHits,
                                                                                          minTrackHits,
                                                                                          maxIP,
                                                                                          maxChi2,
                                                                                          maxDeltaZ,
                                                                                          *thePV_,
                                                                                          thePV_->position().z());
        *occupancy = *occupancy + chargedCands.size();
        for(size_t i=0; i<chargedCands.size(); ++i) {
          double pt = chargedCands[i]->pt();
          *sumPt = *sumPt + pt;
          *maxPt = std::max(*maxPt, pt);
        }
     
	std::cout << " allCands " << allCands << " sumPt  " << *sumPt << std::endl;
      
      }
      */
      FakeTauIdentifier::MCSelectedTauMatchType myMatch = fFakeTauIdentifier.matchTauToMC(iEvent, **it);
      if (myMatch == FakeTauIdentifier::kkTauToTau || FakeTauIdentifier::kkTauToTauAndTauOutsideAcceptance)
        hCandidateTauNumber->Fill(0., fEventWeight.getWeight());
      else if (myMatch == FakeTauIdentifier::kkElectronToTau || FakeTauIdentifier::kkElectronToTauAndTauOutsideAcceptance)
        hCandidateTauNumber->Fill(1, fEventWeight.getWeight());
      else if (myMatch == FakeTauIdentifier::kkMuonToTau || FakeTauIdentifier::kkMuonToTauAndTauOutsideAcceptance)
        hCandidateTauNumber->Fill(2, fEventWeight.getWeight());
      else if (myMatch == FakeTauIdentifier::kkJetToTau || FakeTauIdentifier::kkJetToTauAndTauOutsideAcceptance)
        hCandidateTauNumber->Fill(3, fEventWeight.getWeight());
    }
    // Do tau selection on the veto tau candidates
    TauSelection::Data myTauData = fTauSelection.analyze(iEvent, iSetup, myVetoTauCandidates);
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
      fSelectedVetoTaus.push_back(*it);
      // Count how many selected veto taus are genuine taus
      FakeTauIdentifier::MCSelectedTauMatchType myMatch = fFakeTauIdentifier.matchTauToMC(iEvent, **it);
      if (myMatch == FakeTauIdentifier::kkTauToTau || FakeTauIdentifier::kkTauToTauAndTauOutsideAcceptance)
        hSelectedTauNumber->Fill(0., fEventWeight.getWeight());
      else if (myMatch == FakeTauIdentifier::kkElectronToTau || FakeTauIdentifier::kkElectronToTauAndTauOutsideAcceptance)
        hSelectedTauNumber->Fill(1, fEventWeight.getWeight());
      else if (myMatch == FakeTauIdentifier::kkMuonToTau || FakeTauIdentifier::kkMuonToTauAndTauOutsideAcceptance)
        hSelectedTauNumber->Fill(2, fEventWeight.getWeight());
      else if (myMatch == FakeTauIdentifier::kkJetToTau || FakeTauIdentifier::kkJetToTauAndTauOutsideAcceptance)
        hSelectedTauNumber->Fill(3, fEventWeight.getWeight());

      bool isGenuineTau = !(fFakeTauIdentifier.isFakeTau(myMatch));
      if (isGenuineTau) {
        // Genuine tau
        hSelectedGenuineTauByPt->Fill((*it)->pt(), fEventWeight.getWeight());
        hSelectedGenuineTauByEta->Fill((*it)->eta(), fEventWeight.getWeight());
        hSelectedGenuineTauByPhi->Fill((*it)->phi(), fEventWeight.getWeight());
      } else {
        // Fake tau
        hSelectedFakeTauByPt->Fill((*it)->pt(), fEventWeight.getWeight());
        hSelectedFakeTauByEta->Fill((*it)->eta(), fEventWeight.getWeight());
        hSelectedFakeTauByPhi->Fill((*it)->phi(), fEventWeight.getWeight());
      }
      // Add the taus up and get the ditau mass
      TLorentzVector myVetoTauMomentum;
      myVetoTauMomentum.SetXYZM((*it)->px(), (*it)->py(), (*it)->pz(), 1.777);  
      myVetoTauMomentum += mySelectedTauMomentum;
      double myDitauMass = myVetoTauMomentum.M();
      // Check if ditau mass is compatible with Z mass
      if (myDitauMass <  100 ) 	{
	myVetoStatus = true;
	numberOfTaus++;
      }
      
      /*
      if (TMath::Abs(myDitauMass - fZMass) < fZMassWindow) {
	myVetoStatus = true;
      }
      */
      if (isGenuineTau) {
          hSelectedGenuineTauDiTauMass->Fill(myDitauMass, fEventWeight.getWeight());
        } else {
          hSelectedFakeTauDiTauMass->Fill(myDitauMass, fEventWeight.getWeight());
      }
    }
    //    if (myTauData.passedEvent()) myVetoStatus = true;
    hSelectedTaus->Fill(numberOfTaus, fEventWeight.getWeight());
    // Return the end result
    if (myVetoStatus)
      increment(fEventsCompatibleWithZMassCounter);
    else
      increment(fSelectedEventsCounter);
    return Data(this, myVetoStatus);
  }
}
