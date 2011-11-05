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

    s.str("");
    s << "AbsoluteUncertainty_" << name;
    hCumulativeUncertainties = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 3, 0, 3);
    hCumulativeUncertainties->GetXaxis()->SetBinLabel(1+kSFOrderTotalCount,"TotalCount"); // cumulative weight
    hCumulativeUncertainties->GetXaxis()->SetBinLabel(1+kSFOrderTriggerSF,"abs. #delta_{TriggerSF}^{2}"); // cumulative absolute uncertainty squared
    hCumulativeUncertainties->GetXaxis()->SetBinLabel(1+kSFOrderBtagSF,"abs. #delta_{btagSF}^{2}"); // cumulative absolute uncertainty squared
    // To obtain the relative uncertainty, calculate sqrt(abs uncertainty) / cumulative weight
    
    // Trigger SF
    s.str("");
    s << "TriggerScaleFactor_" << name;
    hTriggerSF = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);
    // btag SF
    s.str("");
    s << "BtagScaleFactor_" << name;
    hBtagSF = makeTH<TH1F>(myDir, s.str().c_str(), s.str().c_str(), 200., 0., 2.0);

  }

  ScaleFactorUncertaintyManager::~ScaleFactorUncertaintyManager() {}

  void ScaleFactorUncertaintyManager::setScaleFactorUncertainties(double eventWeight, double triggerSF, double triggerSFAbsUncertainty, double btagSF, double btagSFAbsUncertainty) {
    // weight
    hCumulativeUncertainties->Fill(kSFOrderTotalCount, eventWeight);

    // Absolute uncertainty is given by weight / SF * delta(SF), weight is the event weight at the point what one is observing

    // Trigger SF
    hCumulativeUncertainties->Fill(kSFOrderTriggerSF, eventWeight / triggerSF * triggerSFAbsUncertainty);
    hTriggerSF->Fill(triggerSF);
    // btag SF
    hCumulativeUncertainties->Fill(kSFOrderBtagSF, eventWeight / btagSF * btagSFAbsUncertainty);
    hBtagSF->Fill(btagSF);
  }
}
