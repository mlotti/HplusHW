#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ScaleFactorUncertaintyManager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"

#include "TH1F.h"

#include <sstream>

namespace HPlus {
  ScaleFactorUncertaintyManager::ScaleFactorUncertaintyManager(const std::string& name, const std::string& directory) {
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
    hTriggerSF = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "TriggerScaleFactorAbsUncert_" << name;
    hTriggerSFAbsUncertainty = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "TriggerScaleFactorAbsUncertCounts_" << name;
    hTriggerSFAbsUncertaintyCounts = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

    // btag SF
    s.str("");
    s << "BtagScaleFactor_" << name;
    hBtagSF = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    s.str("");
    s << "BtagScaleFactorAbsUncert_" << name;
    hBtagSFAbsUncertainty = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 20000., 0., 2);
    s.str("");
    s << "BtagScaleFactorAbsUncertCounts_" << name;
    hBtagSFAbsUncertaintyCounts = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 1, 0., 1);

  }

  ScaleFactorUncertaintyManager::~ScaleFactorUncertaintyManager() {}

  void ScaleFactorUncertaintyManager::setScaleFactorUncertainties(double eventWeight, double triggerSF, double triggerSFAbsUncertainty, double btagSF, double btagSFAbsUncertainty) {
    // To calculate relative uncertainty, use
    //   sqrt(sum_i((N_i * abs_uncert_i)^2)) / sum_i (N_i*w_i)
    //   i.e. sqrt(sum_i((getBinContent(i) * getBinCenter(i))^2) / AbsUncertaintyCounts->GetBinContent(0);
    // Trigger SF
    hTriggerSF->Fill(triggerSF);
    hTriggerSFAbsUncertainty->Fill(triggerSFAbsUncertainty, eventWeight / triggerSF);
    hTriggerSFAbsUncertaintyCounts->Fill(0.0, eventWeight); // weight should include also trg SF
    // btag SF
    hBtagSF->Fill(btagSF);
    hTriggerSFAbsUncertainty->Fill(btagSFAbsUncertainty, eventWeight / btagSF);
    hTriggerSFAbsUncertaintyCounts->Fill(0.0, eventWeight); // weight should include also trg SF
  }
}
