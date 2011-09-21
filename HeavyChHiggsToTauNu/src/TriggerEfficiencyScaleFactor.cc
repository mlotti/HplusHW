#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "TH1F.h"


#include<cmath>
#include<algorithm>

namespace HPlus {
  TriggerEfficiencyScaleFactor::Data::Data(const TriggerEfficiencyScaleFactor *tesf): fTesf(tesf) {}
  TriggerEfficiencyScaleFactor::Data::~Data() {}
  
  TriggerEfficiencyScaleFactor::TriggerEfficiencyScaleFactor(const edm::ParameterSet& iConfig, EventWeight& eventWeight):
    fEventWeight(eventWeight) {
    std::vector<edm::ParameterSet> bins = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("parameters");
    for(size_t i=0; i<bins.size(); ++i) {
      double bin = bins[i].getParameter<double>("pt");
      if(!fPtBinLowEdges.empty() && bin <= fPtBinLowEdges.back())
        throw cms::Exception("Configuration") << "Bins must be in an ascending order of lowEdges (new "
                                              << bin << " previous " << fPtBinLowEdges.back() << ")"
                                              << std::endl;

      fPtBinLowEdges.push_back(bin);
      fEffDataValues.push_back(bins[i].getParameter<double>("dataEff"));
      fEffDataUncertainties.push_back(bins[i].getParameter<double>("dataUncertainty"));
      fEffMCValues.push_back(bins[i].getParameter<double>("mcEff"));
      fEffMCUncertainties.push_back(bins[i].getParameter<double>("mcUncertainty"));
    }

    std::string mode = iConfig.getUntrackedParameter<std::string>("mode");
    if(mode == "dataEfficiency")
      fMode = kDataEfficiency;
    else if(mode == "scaleFactor")
      fMode = kScaleFactor;
    else if(mode == "disabled")
      fMode = kDisabled;
    else
      throw cms::Exception("Configuration") << "Unsupported value for parameter 'mode' " << mode << ", should be 'efficiency', 'scaleFactor', or 'disabled'" << std::endl;

    edm::Service<TFileService> fs;
    TFileDirectory dir = fs->mkdir("TriggerScaleFactor");
    hScaleFactor = makeTH<TH1F>(dir, "TriggerScaleFactor", "TriggerScaleFactor;TriggerScaleFactor;N_{events}/0.01", 200., 0., 2.0);
    hScaleFactorRelativeUncertainty = makeTH<TH1F>(dir, "TriggerScaleFactorRelativeUncertainty", "TriggerScaleFactorRelativeUncertainty;TriggerScaleFactorRelativeUncertainty;N_{events}/0.001", 2000., 0., 2.0);
    hScaleFactorAbsoluteUncertainty = makeTH<TH1F>(dir, "TriggerScaleFactorAbsoluteUncertainty", "TriggerScaleFactorAbsoluteUncertainty;TriggerScaleFactorAbsoluteUncertainty;N_{events}/0.001", 2000., 0., 2.0);

  }
  TriggerEfficiencyScaleFactor::~TriggerEfficiencyScaleFactor() {}

  size_t TriggerEfficiencyScaleFactor::index(double pt) const {
    // find the first bin for which fPtBinLowEdges[bin] >= pt
    std::vector<double>::const_iterator found = std::lower_bound(fPtBinLowEdges.begin(), fPtBinLowEdges.end(), pt);
    if(found == fPtBinLowEdges.begin())
      throw cms::Exception("LogicError") << "Got tau pt " << pt << " which is less than the first bin in the given efficiencies " << fPtBinLowEdges.front();
    // pick the previous bin
    --found;
    return found-fPtBinLowEdges.begin();
  }

  double TriggerEfficiencyScaleFactor::dataEfficiency(const pat::Tau& tau) const {
    return fEffDataValues[index(tau.pt())];
  }

  double TriggerEfficiencyScaleFactor::dataEfficiencyRelativeUncertainty(const pat::Tau& tau) const {
    size_t i = index(tau.pt());
    return fEffDataUncertainties[i] / fEffDataValues[i];
  }
  double TriggerEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const {
    return fEffDataUncertainties[index(tau.pt())];
  }

  double TriggerEfficiencyScaleFactor::scaleFactor(const pat::Tau& tau) const {
    size_t i = index(tau.pt());
    return fEffDataValues[i] / fEffMCValues[i];
  }
  double TriggerEfficiencyScaleFactor::scaleFactorRelativeUncertainty(const pat::Tau& tau) const {
    size_t i = index(tau.pt());
    double data = fEffDataUncertainties[i] / fEffDataValues[i];
    double mc = fEffMCUncertainties[i] / fEffMCValues[i];
    return std::sqrt(data*data + mc*mc);
  }
  double TriggerEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty(const pat::Tau& tau) const {
    return scaleFactor(tau) * scaleFactorRelativeUncertainty(tau);
  }

  TriggerEfficiencyScaleFactor::Data TriggerEfficiencyScaleFactor::applyEventWeight(const pat::Tau& tau) {
    fWeight = 1.0;
    if(fMode == kScaleFactor) {
      fWeight = scaleFactor(tau);
      hScaleFactor->Fill(fWeight, fEventWeight.getWeight());
      hScaleFactorRelativeUncertainty->Fill(scaleFactorRelativeUncertainty(tau), fEventWeight.getWeight());
      hScaleFactorAbsoluteUncertainty->Fill(scaleFactorAbsoluteUncertainty(tau), fEventWeight.getWeight());

      fEventWeight.multiplyWeight(fWeight);
    }
    else if(fMode == kDataEfficiency) {
      fWeight = dataEfficiency(tau);
      fEventWeight.multiplyWeight(fWeight);
    }
    return Data(this);
  }
}
