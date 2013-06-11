#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METPhiOscillationCorrection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Math/interface/Vector3D.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  METPhiOscillationCorrection::METPhiOscillationCorrection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix) {
    initializeHistograms(histoWrapper, prefix);
  }

  METPhiOscillationCorrection::METPhiOscillationCorrection(EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string prefix) {
    initializeHistograms(histoWrapper, prefix);
  }

  METPhiOscillationCorrection::~METPhiOscillationCorrection() {}

  void METPhiOscillationCorrection::analyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData) {
    privateAnalyze(iEvent, nVertices, metData);
  }

  void METPhiOscillationCorrection::privateAnalyze(const edm::Event& iEvent, int nVertices, const METSelection::Data& metData) {
    const edm::Ptr<reco::MET> myUncorrectedMET = metData.getPhiUncorrectedSelectedMET();
    // Fill uncorrected histograms
    hMETPhiUncorrected->Fill(myUncorrectedMET->phi());
    hMETUncorrected->Fill(myUncorrectedMET->pt());
    // Fill histograms for determining correction factors
    hNVerticesVsMetX->Fill(nVertices, myUncorrectedMET->px());
    hNVerticesVsMetY->Fill(nVertices, myUncorrectedMET->py());
    // Fill corrected histograms
    const edm::Ptr<reco::MET> myCorrectedMET = metData.getPhiCorrectedSelectedMET();
    hMETPhiCorrected->Fill(myCorrectedMET->phi());
    hMETCorrected->Fill(myCorrectedMET->pt());
    // Fill histograms for validating correction factors
    hNVerticesVsMetXCorrected->Fill(nVertices, myCorrectedMET->px());
    hNVerticesVsMetYCorrected->Fill(nVertices, myCorrectedMET->py());
}

  void METPhiOscillationCorrection::initializeHistograms(HistoWrapper& histoWrapper, std::string prefix) {
    edm::Service<TFileService> fs;
    std::string myDirStr = "METPhiOscillationCorrection"+prefix;
    TFileDirectory myDir = fs->mkdir(myDirStr.c_str());
    // Histograms for determining corrections
    hNVerticesVsMetX = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETX", "NverticesVsMETX;N_{vertices};MET_{x}, GeV", 60, 0., 60., 2000, -500, 500);
    hNVerticesVsMetY = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETY", "NverticesVsMETY;N_{vertices};MET_{y}, GeV", 60, 0., 60., 2000, -500, 500);
    // Diagnostic histograms
    hMETPhiUncorrected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "METPhiUncorrected", "METPhiUncorrected;Type I MET #phi;N_{events}", 72, -3.1415927, 3.1415927);
    hMETPhiCorrected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "METPhiCorrected", "METPhiCorrected;Type I MET #phi;N_{events}", 72, -3.1415927, 3.1415927);    
    hMETUncorrected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "METUncorrected", "METUncorrected;Type I MET, GeV;N_{events}", 100., 0., 500.);
    hMETCorrected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "METCorrected", "METCorrected;Type I MET, GeV;N_{events}", 100., 0., 500.);
    // Histograms for validating corrections
    hNVerticesVsMetXCorrected = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETXCorrected", "NverticesVsMETXCorrected;N_{vertices};MET_{x}, GeV", 60, 0., 60., 2000, -500, 500);
    hNVerticesVsMetYCorrected = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "NverticesVsMETYCorrected", "NverticesVsMETYCorrected;N_{vertices};MET_{y}, GeV", 60, 0., 60., 2000, -500, 500);
  }
}
