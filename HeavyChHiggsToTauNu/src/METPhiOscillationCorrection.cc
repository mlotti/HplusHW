#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  METPhiOscillationCorrection::Data::Data():
    fCorrectionFactor(1.0) {}
  METPhiOscillationCorrection::Data::~Data() {}

  METPhiOscillationCorrection::METPhiOscillationCorrection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix):
    BaseSelection(eventCounter, histoWrapper) {
    edm::Service<TFileService> fs;
    std::string myDirStr = "METPhiOscillationCorrection"+prefix;
    TFileDirectory myDir = fs->mkdir(myDirStr.c_str());
    // Histograms for determining corrections
    hNVerticesVsMetX = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETX", "NverticesVsMETX;N_{vertices};MET_{x}, GeV", 60, 0., 60., 1000, -500, 500);
    hNVerticesVsMetY = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETY", "NverticesVsMETY;N_{vertices};MET_{y}, GeV", 60, 0., 60., 1000, -500, 500);
  }

  METPhiOscillationCorrection::METPhiOscillationCorrection(EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix):
    BaseSelection(eventCounter, histoWrapper) {
    edm::Service<TFileService> fs;
    std::string myDirStr = "METPhiOscillationCorrection"+prefix;
    TFileDirectory myDir = fs->mkdir(myDirStr.c_str());
    // Histograms for determining corrections
    hNVerticesVsMetX = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETX", "NverticesVsMETX;N_{vertices};MET_{x}, GeV", 60, 0., 60., 1000, -500, 500);
    hNVerticesVsMetY = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETY", "NverticesVsMETY;N_{vertices};MET_{y}, GeV", 60, 0., 60., 1000, -500, 500);
  }

  METPhiOscillationCorrection::~METPhiOscillationCorrection() {}

  METPhiOscillationCorrection::Data METPhiOscillationCorrection::silentAnalyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent,  nVertices, metData.getSelectedMET());
  }

  METPhiOscillationCorrection::Data METPhiOscillationCorrection::silentAnalyze(const edm::Event& iEvent, int nVertices, const edm::Ptr<reco::MET>& met) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, nVertices, met);
  }

  METPhiOscillationCorrection::Data METPhiOscillationCorrection::analyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, nVertices, metData.getSelectedMET());
  }

  METPhiOscillationCorrection::Data METPhiOscillationCorrection::analyze(const edm::Event& iEvent, int nVertices, const edm::Ptr<reco::MET>& met) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, nVertices, met);
  }

  METPhiOscillationCorrection::Data METPhiOscillationCorrection::privateAnalyze(const edm::Event& iEvent, int nVertices, const edm::Ptr<reco::MET>& met) {
    Data output;

    // Fill histograms for determining correction factors
    hNVerticesVsMetX->Fill(nVertices, met->px());
    hNVerticesVsMetY->Fill(nVertices, met->py());

    // Return result
    return output;
  }
}
