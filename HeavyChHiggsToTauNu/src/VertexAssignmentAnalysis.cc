#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"

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

namespace HPlus {
  VertexAssignmentAnalysis::VertexAssignmentAnalysis(EventCounter& eventCounter, EventWeight& eventWeight):
    fFakeTauIdentifier(eventWeight, "VertexAssignment"),
    fEventWeight(eventWeight),
    fAllEventsWithGenuineTaus(eventCounter.addSubCounter("VtxAssignment","genuine tau/all events")),
    fGenuineTausWithCorrectPV(eventCounter.addSubCounter("VtxAssignment","genuine tau/passed events")),
    fAllEventsWithFakeTaus(eventCounter.addSubCounter("VtxAssignment","fake tau/all events")),
    fFakeTausWithCorrectPV(eventCounter.addSubCounter("VtxAssignment","fake tau/passed events")) {
    // Initialise histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("PVAssignment");
    hGenuineTauAllEventsByTauZ = makeTH<TH1F>(myDir, "GenuineTauAllEventsByTauZ", "GenuineTauAllEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hGenuineTauPassedEventsByTauZ = makeTH<TH1F>(myDir, "GenuineTauPassedEventsByTauZ", "GenuineTauPassedEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hGenuineTauAllEventsByPt = makeTH<TH1F>(myDir, "GenuineTauAllEventsByPt", "GenuineTauAllEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hGenuineTauPassedEventsByPt = makeTH<TH1F>(myDir, "GenuineTauPassedEventsByPt", "GenuineTauPassedEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hGenuineTauAllEventsByEta = makeTH<TH1F>(myDir, "GenuineTauAllEventsByEta", "GenuineTauAllEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hGenuineTauPassedEventsByEta = makeTH<TH1F>(myDir, "GenuineTauPassedEventsByEta", "GenuineTauPassedEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hGenuineTauAllEventsByPhi = makeTH<TH1F>(myDir, "GenuineTauAllEventsByPhi", "GenuineTauAllEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hGenuineTauPassedEventsByPhi = makeTH<TH1F>(myDir, "GenuineTauPassedEventsByPhi", "GenuineTauPassedEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hFakeTauAllEventsByTauZ = makeTH<TH1F>(myDir, "FakeTauAllEventsByTauZ", "FakeTauAllEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hFakeTauPassedEventsByTauZ = makeTH<TH1F>(myDir, "FakeTauAllEventsByTauZ", "FakeTauAllEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hFakeTauAllEventsByPt = makeTH<TH1F>(myDir, "FakeTauPassedEventsByPt", "FakeTauPassedEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hFakeTauPassedEventsByPt = makeTH<TH1F>(myDir, "FakeTauPassedEventsByPt", "FakeTauPassedEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hFakeTauAllEventsByEta = makeTH<TH1F>(myDir, "FakeTauAllEventsByEta", "FakeTauAllEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hFakeTauPassedEventsByEta = makeTH<TH1F>(myDir, "FakeTauPassedEventsByEta", "FakeTauPassedEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hFakeTauAllEventsByPhi = makeTH<TH1F>(myDir, "FakeTauAllEventsByPhi", "FakeTauAllEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hFakeTauPassedEventsByPhi = makeTH<TH1F>(myDir, "FakeTauPassedEventsByPhi", "FakeTauPassedEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
  }

  VertexAssignmentAnalysis::~VertexAssignmentAnalysis() {}

  void VertexAssignmentAnalysis::analyze(bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch) {
    // Analysis is only possible for MC events
    if (isData) return;
    // Fill counters and histograms for all events
    if (fFakeTauIdentifier.isFakeTau(mcmatch)) {
      hFakeTauAllEventsByTauZ->Fill(tau->vz(), fEventWeight.getWeight());
      hFakeTauAllEventsByPt->Fill(tau->pt(), fEventWeight.getWeight());
      hFakeTauAllEventsByEta->Fill(tau->eta(), fEventWeight.getWeight());
      hFakeTauAllEventsByPhi->Fill(tau->phi(), fEventWeight.getWeight());
      increment(fAllEventsWithFakeTaus);
    } else {
      hGenuineTauAllEventsByTauZ->Fill(tau->vz(), fEventWeight.getWeight());
      hGenuineTauAllEventsByPt->Fill(tau->pt(), fEventWeight.getWeight());
      hGenuineTauAllEventsByEta->Fill(tau->eta(), fEventWeight.getWeight());
      hGenuineTauAllEventsByPhi->Fill(tau->phi(), fEventWeight.getWeight());
      increment(fAllEventsWithGenuineTaus);
    }
    // Check if selected tau and PV do match
    double myDelta = TMath::Abs(tau->vz() - vtx->z());
    //std::cout << myDelta << " tau z=" << tau->vz() << " vtx z=" << vtx->z() << std::endl;
    if (myDelta > 2.0) return;
    
    // Fill counters for events where match was positive
    if (fFakeTauIdentifier.isFakeTau(mcmatch)) {
      hFakeTauPassedEventsByTauZ->Fill(tau->vz(), fEventWeight.getWeight());
      hFakeTauPassedEventsByPt->Fill(tau->pt(), fEventWeight.getWeight());
      hFakeTauPassedEventsByEta->Fill(tau->eta(), fEventWeight.getWeight());
      hFakeTauPassedEventsByPhi->Fill(tau->phi(), fEventWeight.getWeight());
      increment(fGenuineTausWithCorrectPV);
    } else {
      hGenuineTauPassedEventsByTauZ->Fill(tau->vz(), fEventWeight.getWeight());
      hGenuineTauPassedEventsByPt->Fill(tau->pt(), fEventWeight.getWeight());
      hGenuineTauPassedEventsByEta->Fill(tau->eta(), fEventWeight.getWeight());
      hGenuineTauPassedEventsByPhi->Fill(tau->phi(), fEventWeight.getWeight());
      increment(fFakeTausWithCorrectPV);
    }    
  }
}
