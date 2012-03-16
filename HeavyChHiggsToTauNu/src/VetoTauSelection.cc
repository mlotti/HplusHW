#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TMath.h"
#include "TH1.h"
#include "TLorentzVector.h"

namespace HPlus {
  VetoTauSelection::Data::Data(const VetoTauSelection *vetoTauSelection, bool passedEvent) :
  fVetoTauSelection(vetoTauSelection), fPassedEvent(passedEvent) { }

  VetoTauSelection::Data::~Data() { }
  
  VetoTauSelection::VetoTauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight) :
    fZMass(iConfig.getUntrackedParameter<double>("Zmass")),
    fZMassWindow(iConfig.getUntrackedParameter<double>("ZmassWindow")),
    fTauSource(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection").getUntrackedParameter<edm::InputTag>("src")),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, "TauVeto"),
    fFakeTauIdentifier(eventWeight, "VetoTauSelection"),
    fEventWeight(eventWeight),
    fAllEventsCounter(eventCounter.addSubCounter("VetoTauSelection","All events")),
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
    hSelectedGenuineTauByPt = makeTH<TH1F>(myDir, "SelectedGenuineTauByPt", "SelectedGenuineTauByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedGenuineTauByEta = makeTH<TH1F>(myDir, "SelectedGenuineTauByEta", "SelectedGenuineTauByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hSelectedGenuineTauByPhi = makeTH<TH1F>(myDir, "SelectedGenuineTauByPhi", "SelectedGenuineTauByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hSelectedFakeTauByPt = makeTH<TH1F>(myDir, "SelectedFakeTauByPt", "SelectedFakeTauByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hSelectedFakeTauByEta = makeTH<TH1F>(myDir, "SelectedFakeTauByEta", "SelectedFakeTauByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hSelectedFakeTauByPhi = makeTH<TH1F>(myDir, "SelectedFakeTauByPhi", "SelectedFakeTauByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hSelectedGenuineTauDiTauMass = makeTH<TH1F>(myDir, "SelectedGenuineTauDitauMass", "SelectedGenuineTauDitauMass;M_{#tau#tau}, GeV/c^{2};Events / 5 GeV/c^{2}", 50, 0, 250);
    hSelectedFakeTauDiTauMass = makeTH<TH1F>(myDir, "SelectedFakeTauDitauMass", "SelectedFakeTauDitauMass;M_{#tau#tau}, GeV/c^{2};Events / 5 GeV/c^{2}", 50, 0, 250);
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
    // Count how many taus (excluding the selected tau) are available in the event
    for (edm::PtrVector<pat::Tau>::iterator it = myVetoTauCandidates.begin(); it != myVetoTauCandidates.end(); ++it) {
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
    if (myTauData.passedEvent())
      increment(fVetoTausSelectedCounter);
    
    // Loop over the selected veto taus
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
      if (TMath::Abs(myDitauMass - fZMass) < fZMassWindow) {
        myVetoStatus = true;
      }
      if (isGenuineTau) {
          hSelectedGenuineTauDiTauMass->Fill(myDitauMass, fEventWeight.getWeight());
        } else {
          hSelectedFakeTauDiTauMass->Fill(myDitauMass, fEventWeight.getWeight());
      }
    }
    // Return the end result
    if (myVetoStatus)
      increment(fEventsCompatibleWithZMassCounter);
    else
      increment(fSelectedEventsCounter);
    return Data(this, myVetoStatus);
  }
}
