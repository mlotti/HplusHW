#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexAssignmentAnalysis.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TMath.h"

namespace HPlus {
  VertexAssignmentAnalysis::VertexAssignmentAnalysis(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), histoWrapper, "VertexAssignment"),
    fAllEventsWithGenuineTaus(eventCounter.addSubCounter("VtxAssignment","genuine tau/all events")),
    fGenuineTausWithCorrectPV(eventCounter.addSubCounter("VtxAssignment","genuine tau/passed events")),
    fAllEventsWithFakeTaus(eventCounter.addSubCounter("VtxAssignment","fake tau/all events")),
    fFakeTausWithCorrectPV(eventCounter.addSubCounter("VtxAssignment","fake tau/passed events")) {
    // Initialise histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("PVAssignment");
    hGenuineTauAllEventsByTauZ = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauAllEventsByTauZ", "GenuineTauAllEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hGenuineTauPassedEventsByTauZ = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauPassedEventsByTauZ", "GenuineTauPassedEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hGenuineTauAllEventsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauAllEventsByPt", "GenuineTauAllEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hGenuineTauPassedEventsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauPassedEventsByPt", "GenuineTauPassedEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hGenuineTauAllEventsByEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauAllEventsByEta", "GenuineTauAllEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hGenuineTauPassedEventsByEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauPassedEventsByEta", "GenuineTauPassedEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hGenuineTauAllEventsByPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauAllEventsByPhi", "GenuineTauAllEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hGenuineTauPassedEventsByPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GenuineTauPassedEventsByPhi", "GenuineTauPassedEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hFakeTauAllEventsByTauZ = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauAllEventsByTauZ", "FakeTauAllEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hFakeTauPassedEventsByTauZ = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauPassedEventsByTauZ", "FakeTauPassedEventsByTauZ;PV z associated to #tau, mm;Events / 1 mm", 100, -50, 50);
    hFakeTauAllEventsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauAllEventsByPt", "FakeTauAllEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hFakeTauPassedEventsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauPassedEventsByPt", "FakeTauPassedEventsByPt;#tau p_{T}, GeV/c;Events / 10 GeV/c", 40, 0, 400);
    hFakeTauAllEventsByEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauAllEventsByEta", "FakeTauAllEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hFakeTauPassedEventsByEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauPassedEventsByEta", "FakeTauPassedEventsByEta;#tau #eta;Events / 0.1", 50, -2.5, 2.5);
    hFakeTauAllEventsByPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauAllEventsByPhi", "FakeTauAllEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
    hFakeTauPassedEventsByPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "FakeTauPassedEventsByPhi", "FakeTauPassedEventsByEta;#tau #eta;Events / 5^{o}", 72, -3.14159265, 3.14159265);
  }

  VertexAssignmentAnalysis::~VertexAssignmentAnalysis() {}

  void VertexAssignmentAnalysis::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, isData, vtx, tau, mcmatch);
  }

  void VertexAssignmentAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, isData, vtx, tau, mcmatch);
  }

  void VertexAssignmentAnalysis::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool isData, edm::Ptr<reco::Vertex> vtx, edm::Ptr<pat::Tau> tau, FakeTauIdentifier::MCSelectedTauMatchType mcmatch) {
    // Analysis is only possible for MC events
    if (isData) return;
    // Fill counters and histograms for all events
    if (fFakeTauIdentifier.isFakeTau(mcmatch)) {
      hFakeTauAllEventsByTauZ->Fill(tau->vz());
      hFakeTauAllEventsByPt->Fill(tau->pt());
      hFakeTauAllEventsByEta->Fill(tau->eta());
      hFakeTauAllEventsByPhi->Fill(tau->phi());
      increment(fAllEventsWithFakeTaus);
    } else {
      hGenuineTauAllEventsByTauZ->Fill(tau->vz());
      hGenuineTauAllEventsByPt->Fill(tau->pt());
      hGenuineTauAllEventsByEta->Fill(tau->eta());
      hGenuineTauAllEventsByPhi->Fill(tau->phi());
      increment(fAllEventsWithGenuineTaus);
    }
    // Check if selected tau and PV do match
    double myDelta = TMath::Abs(tau->vz() - vtx->z());
    //std::cout << myDelta << " tau z=" << tau->vz() << " vtx z=" << vtx->z() << std::endl;
    if (myDelta > 2.0) return;

    // Fill counters for events where match was positive
    if (fFakeTauIdentifier.isFakeTau(mcmatch)) {
      hFakeTauPassedEventsByTauZ->Fill(tau->vz());
      hFakeTauPassedEventsByPt->Fill(tau->pt());
      hFakeTauPassedEventsByEta->Fill(tau->eta());
      hFakeTauPassedEventsByPhi->Fill(tau->phi());
      increment(fGenuineTausWithCorrectPV);
    } else {
      hGenuineTauPassedEventsByTauZ->Fill(tau->vz());
      hGenuineTauPassedEventsByPt->Fill(tau->pt());
      hGenuineTauPassedEventsByEta->Fill(tau->eta());
      hGenuineTauPassedEventsByPhi->Fill(tau->phi());
      increment(fFakeTausWithCorrectPV);
    }
  }
}
