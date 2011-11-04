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

    const size_t NBUF = 10;
    char buf[NBUF];
    TH1 *hsf = makeTH<TH1F>(dir, "ScaleFactor", "Scale factor;Tau p_{T} bin;Scale factor", bins.size()+1, 0, bins.size()+1);
    TH1 *hsfu = makeTH<TH1F>(dir, "ScaleFactorUncertainty", "Scale factor;Tau p_{T} bin;Scale factor uncertainty", bins.size()+1, 0, bins.size()+1);
    TH1 *hde = makeTH<TH1F>(dir, "DataEfficiency", "Efficiency from data;Tau p_{T} bin;Efficiency", bins.size()+1, 0, bins.size()+1);
    TH1 *hdeu = makeTH<TH1F>(dir, "DataEfficiencyUncertainty", "Efficiency from data;Tau p_{T} bin;Efficiency uncertainty", bins.size()+1, 0, bins.size()+1);
    hsf->SetBinContent(1, 1); hsf->GetXaxis()->SetBinLabel(1, "control");
    hsfu->SetBinContent(1, 1); hsf->GetXaxis()->SetBinLabel(1, "control");
    hde->SetBinContent(1, 1); hde->GetXaxis()->SetBinLabel(1, "control");
    hdeu->SetBinContent(1, 1); hde->GetXaxis()->SetBinLabel(1, "control");
    for(size_t i=0; i<bins.size(); ++i) {
      size_t bin = i+2;
      snprintf(buf, NBUF, "%.0f", fPtBinLowEdges[i]);

      hsf->SetBinContent(bin, scaleFactor(i));
      hsfu->SetBinContent(bin, scaleFactorAbsoluteUncertainty(i));
      hsf->GetXaxis()->SetBinLabel(bin, buf);
      hsfu->GetXaxis()->SetBinLabel(bin, buf);

      hde->SetBinContent(bin, dataEfficiency(i));
      hdeu->SetBinContent(bin, dataEfficiencyAbsoluteUncertainty(i));
      hde->GetXaxis()->SetBinLabel(bin, buf);
      hdeu->GetXaxis()->SetBinLabel(bin, buf);
    }
  }
  TriggerEfficiencyScaleFactor::~TriggerEfficiencyScaleFactor() {}

  size_t TriggerEfficiencyScaleFactor::index(const pat::Tau& tau) const {
    return index(tau.pt());
  }
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
    return dataEfficiency(index(tau));
  }
  double TriggerEfficiencyScaleFactor::dataEfficiency(size_t i) const {
    return fEffDataValues[i];
  }

  double TriggerEfficiencyScaleFactor::dataEfficiencyRelativeUncertainty(const pat::Tau& tau) const {
    size_t i = index(tau);
    return fEffDataUncertainties[i] / fEffDataValues[i];
  }
  double TriggerEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const {
    return dataEfficiencyAbsoluteUncertainty(index(tau.pt()));
  }
  double TriggerEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertainty(size_t i) const {
    return fEffDataUncertainties[i];
  }

  double TriggerEfficiencyScaleFactor::scaleFactor(const pat::Tau& tau) const {
    return scaleFactor(index(tau));
  }
  double TriggerEfficiencyScaleFactor::scaleFactor(size_t i) const {
    return fEffDataValues[i] / fEffMCValues[i];
  }
  double TriggerEfficiencyScaleFactor::scaleFactorRelativeUncertainty(const pat::Tau& tau) const {
    return scaleFactorRelativeUncertainty(index(tau));
  }
  double TriggerEfficiencyScaleFactor::scaleFactorRelativeUncertainty(size_t i) const {
    double data = fEffDataUncertainties[i] / fEffDataValues[i];
    double mc = fEffMCUncertainties[i] / fEffMCValues[i];
    return std::sqrt(data*data + mc*mc);
  }
  double TriggerEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty(const pat::Tau& tau) const {
    return scaleFactor(tau) * scaleFactorRelativeUncertainty(tau);
  }
  double TriggerEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty(size_t i) const {
    return scaleFactor(i) * scaleFactorRelativeUncertainty(i);
  }

  TriggerEfficiencyScaleFactor::Data TriggerEfficiencyScaleFactor::applyEventWeight(const pat::Tau& tau) {
    fWeight = 1.0;
    if(fMode == kScaleFactor) {
      fWeight = scaleFactor(tau);
      fRelativeUncertainty = scaleFactorRelativeUncertainty(tau);
      fAbsoluteUncertainty = scaleFactorAbsoluteUncertainty(tau);

      fEventWeight.multiplyWeight(fWeight);
    }
    else if(fMode == kDataEfficiency) {
      fWeight = dataEfficiency(tau);
      fEventWeight.multiplyWeight(fWeight);
    }
    return Data(this);
  }
}
