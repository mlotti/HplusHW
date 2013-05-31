#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Math/interface/Vector3D.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  METPhiOscillationCorrection::METPhiOscillationCorrection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix) {
    edm::Service<TFileService> fs;
    std::string myDirStr = "METPhiOscillationCorrection"+prefix;
    TFileDirectory myDir = fs->mkdir(myDirStr.c_str());
    // Histograms for determining corrections
    hNVerticesVsMetX = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETX", "NverticesVsMETX;N_{vertices};MET_{x}, GeV", 60, 0., 60., 1000, -500, 500);
    hNVerticesVsMetY = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETY", "NverticesVsMETY;N_{vertices};MET_{y}, GeV", 60, 0., 60., 1000, -500, 500);
  }

  METPhiOscillationCorrection::METPhiOscillationCorrection(EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix) {
    edm::Service<TFileService> fs;
    std::string myDirStr = "METPhiOscillationCorrection"+prefix;
    TFileDirectory myDir = fs->mkdir(myDirStr.c_str());
    // Histograms for determining corrections
    hNVerticesVsMetX = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETX", "NverticesVsMETX;N_{vertices};MET_{x}, GeV", 60, 0., 60., 1000, -500, 500);
    hNVerticesVsMetY = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETY", "NverticesVsMETY;N_{vertices};MET_{y}, GeV", 60, 0., 60., 1000, -500, 500);
  }

  METPhiOscillationCorrection::~METPhiOscillationCorrection() {}

  double METPhiOscillationCorrection::getCorrectedMET(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met) {
    double metX = getCorrectedMETX(isRealData, nVertices, met);
    double metY = getCorrectedMETY(isRealData, nVertices, met);
    return std::sqrt(metX*metX + metY*metY);
  }

  double METPhiOscillationCorrection::getCorrectedMETphi(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met) {
    double metX = getCorrectedMETX(isRealData, nVertices, met);
    double metY = getCorrectedMETY(isRealData, nVertices, met);
    math::XYZVector v(metX, metY, 0.0);
    return v.phi();
  }

  double METPhiOscillationCorrection::getCorrectedMETX(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met) {
    if (isRealData) {
      // 2012ABCD, tau+MET
      return met->px() - (0.594 * static_cast<double>(nVertices) - 1.361);
    } else {
      // 2012ABCD, from Christian
      return met->px() - (-0.02004 * static_cast<double>(nVertices) + 0.1143);
    }
  }

  double METPhiOscillationCorrection::getCorrectedMETY(const bool isRealData, int nVertices, const edm::Ptr<reco::MET>& met) {
    if (isRealData) {
      // 2012ABCD, tau+MET
      return met->py() - (-0.1554 * static_cast<double>(nVertices) - 4.028);
    } else {
      // 2012ABCD, from Christian
      return met->py() - (-0.1979 * static_cast<double>(nVertices) - 0.2135);
    }
  }

  void METPhiOscillationCorrection::analyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData) {
    privateAnalyze(iEvent, nVertices, metData.getSelectedMET());
  }

  void METPhiOscillationCorrection::analyze(const edm::Event& iEvent, int nVertices, const edm::Ptr<reco::MET>& met) {
    privateAnalyze(iEvent, nVertices, met);
  }

  void METPhiOscillationCorrection::privateAnalyze(const edm::Event& iEvent, int nVertices, const edm::Ptr<reco::MET>& met) {
    // Fill histograms for determining correction factors
    hNVerticesVsMetX->Fill(nVertices, met->px());
    hNVerticesVsMetY->Fill(nVertices, met->py());
  }
}
