#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/ServiceRegistry/interface/Service.h"

#include <sstream>

namespace HPlus {
  ScaleFactorUncertaintyManager::ScaleFactorUncertaintyManager(HPlus::HistoWrapper& histoWrapper, const std::string& name, const std::string& directory) {
    edm::Service<TFileService> fs;

    // Book histograms
    std::stringstream s;
    if (directory.size())
      s << directory <<"/";
    s << "ScaleFactorUncertainties";
    TFileDirectory myDir = fs->mkdir(s.str().c_str());

    // Tau trigger SF
    s.str("");
    s << "TauTriggerScaleFactor_" << name;
    hTauTriggerSF = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "TauTriggerScaleFactorAbsUncert_" << name;
    hTauTriggerSFAbsUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "TauTriggerScaleFactorAbsUncertCounts_" << name;
    hTauTriggerSFAbsUncertaintyCounts = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

    // MET trigger SF
    s.str("");
    s << "METTriggerScaleFactor_" << name;
    hMETTriggerSF = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "METTriggerScaleFactorAbsUncert_" << name;
    hMETTriggerSFAbsUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "METTriggerScaleFactorAbsUncertCounts_" << name;
    hMETTriggerSFAbsUncertaintyCounts = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

    // Fake tau SF / systematics
    s.str("");
    s << "FakeTauScaleFactor_" << name;
    hFakeTauSF = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "FakeTauAbsUncert_" << name;
    hFakeTauAbsUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "FakeTauAbsUncertCounts_" << name;
    hFakeTauAbsUncertaintyCounts = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

    // btag SF
    s.str("");
    s << "BtagScaleFactor_" << name;
    hBtagSF = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "BtagScaleFactorAbsUncert_" << name;
    hBtagSFAbsUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "BtagScaleFactorAbsUncertCounts_" << name;
    hBtagSFAbsUncertaintyCounts = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

    // Embedding muon efficiency
    s.str("");
    s << "EmbeddingMuonEfficiency_" << name;
    hEmbeddingMuonEff = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "EmbeddingMuonEfficiencyAbsUncert_" << name;
    hEmbeddingMuonEffAbsUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "EmbeddingMuonEfficiencyAbsUncertCounts_" << name;
    hEmbeddingMuonEffAbsUncertaintyCounts = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

  }

  ScaleFactorUncertaintyManager::~ScaleFactorUncertaintyManager() {}

  void ScaleFactorUncertaintyManager::setScaleFactorUncertainties(bool isFakeTau, double eventWeight,
                                                                  double fakeTauSF, double fakeTauAbsUncertainty,
                                                                  double btagSF, double btagSFAbsUncertainty) {
    // To calculate relative uncertainty, use
    //   sqrt(sum_i((N_i * abs_uncert_i)^2)) / sum_i (N_i*w_i)
    //   i.e. sqrt(sum_i((getBinContent(i) * getBinCenter(i))^2) / AbsUncertaintyCounts->GetBinContent(0);
    // Fake tau SF and systematics
    if (isFakeTau) {
      hFakeTauSF->Fill(fakeTauSF);
      hFakeTauAbsUncertainty->Fill(fakeTauAbsUncertainty, eventWeight / fakeTauSF);
      hFakeTauAbsUncertaintyCounts->Fill(0.0, eventWeight);
    }
    // btag SF
    hBtagSF->Fill(btagSF);
    hBtagSFAbsUncertainty->Fill(btagSFAbsUncertainty, eventWeight / btagSF);
    hBtagSFAbsUncertaintyCounts->Fill(0.0, eventWeight); // weight should include also trg SF
  }

  void ScaleFactorUncertaintyManager::setTauTriggerScaleFactorUncertainty(double eventWeight, double triggerSF, double triggerSFAbsUncertainty) {
    // TauTrigger SF
    hTauTriggerSF->Fill(triggerSF);
    hTauTriggerSFAbsUncertainty->Fill(triggerSFAbsUncertainty, eventWeight / triggerSF);
    hTauTriggerSFAbsUncertaintyCounts->Fill(0.0, eventWeight); // weight should include also trg SF
  }

  void ScaleFactorUncertaintyManager::setMETTriggerScaleFactorUncertainty(double eventWeight, double triggerSF, double triggerSFAbsUncertainty) {
    // METTrigger SF
    hMETTriggerSF->Fill(triggerSF);
    hMETTriggerSFAbsUncertainty->Fill(triggerSFAbsUncertainty, eventWeight / triggerSF);
    hMETTriggerSFAbsUncertaintyCounts->Fill(0.0, eventWeight); // weight should include also trg SF
  }

  void ScaleFactorUncertaintyManager::setEmbeddingMuonEfficiencyUncertainty(double eventWeight, double muonEff, double muonEffAbsUncertainty) {
    hEmbeddingMuonEff->Fill(muonEff);
    hEmbeddingMuonEffAbsUncertainty->Fill(muonEffAbsUncertainty, eventWeight / muonEff);
    hEmbeddingMuonEffAbsUncertaintyCounts->Fill(0.0, eventWeight); // weight should include also eff
  }

}
