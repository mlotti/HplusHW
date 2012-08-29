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

    // Trigger SF
    s.str("");
    s << "TriggerScaleFactor_" << name;
    hTriggerSF = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "TriggerScaleFactorAbsUncert_" << name;
    hTriggerSFAbsUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "TriggerScaleFactorAbsUncertCounts_" << name;
    hTriggerSFAbsUncertaintyCounts = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

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

  }

  ScaleFactorUncertaintyManager::~ScaleFactorUncertaintyManager() {}

  void ScaleFactorUncertaintyManager::setScaleFactorUncertainties(bool isFakeTau, double eventWeight,
                                                                  double triggerSF, double triggerSFAbsUncertainty,
                                                                  double fakeTauSF, double fakeTauAbsUncertainty,
                                                                  double btagSF, double btagSFAbsUncertainty) {
    // To calculate relative uncertainty, use
    //   sqrt(sum_i((N_i * abs_uncert_i)^2)) / sum_i (N_i*w_i)
    //   i.e. sqrt(sum_i((getBinContent(i) * getBinCenter(i))^2) / AbsUncertaintyCounts->GetBinContent(0);
    // Trigger SF
    hTriggerSF->Fill(triggerSF);
    hTriggerSFAbsUncertainty->Fill(triggerSFAbsUncertainty, eventWeight / triggerSF);
    hTriggerSFAbsUncertaintyCounts->Fill(0.0, eventWeight); // weight should include also trg SF
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
}
