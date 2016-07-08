#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METTriggerEfficiencyScaleFactor.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/METReco/interface/MET.h"

namespace HPlus {
  METTriggerEfficiencyScaleFactor::METTriggerEfficiencyScaleFactor(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper):
    fBinned(iConfig, "pt") {
  
    edm::Service<TFileService> fs;
    TFileDirectory dir = fs->mkdir("METTriggerScaleFactor");
    hScaleFactor = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, dir, "TriggerScaleFactor", "TriggerScaleFactor;TriggerScaleFactor;N_{events}/0.01", 200., 0., 2.0);

    const size_t NBUF = 10;
    char buf[NBUF];

    WrappedTH1 *hsf = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, dir, "ScaleFactor", "Scale factor;MET bin;Scale factor", fBinned.nbins()+1, 0, fBinned.nbins()+1);
    WrappedTH1 *hsfu = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, dir, "ScaleFactorUncertainty", "Scale factor;MET bin;Scale factor uncertainty", fBinned.nbins()+1, 0, fBinned.nbins()+1);
    if(hsf->getHisto()) {
      hsf->getHisto()->SetBinContent(1, 1); hsf->GetXaxis()->SetBinLabel(1, "control");
      hsfu->getHisto()->SetBinContent(1, 1); hsfu->GetXaxis()->SetBinLabel(1, "control");
      for(size_t i=0; i<fBinned.nbins(); ++i) {
        size_t bin = i+2;
        snprintf(buf, NBUF, "%.0f", fBinned.binLowEdge(i));

        hsf->getHisto()->SetBinContent(bin, fBinned.binScaleFactor(i));
        hsfu->getHisto()->SetBinContent(bin, fBinned.binScaleFactorAbsoluteUncertainty(i));
        hsf->GetXaxis()->SetBinLabel(bin, buf);
        hsfu->GetXaxis()->SetBinLabel(bin, buf);
      }
    }
  }
  METTriggerEfficiencyScaleFactor::~METTriggerEfficiencyScaleFactor() {}

  METTriggerEfficiencyScaleFactor::Data METTriggerEfficiencyScaleFactor::applyEventWeight(const reco::MET& met, bool isData, EventWeight& eventWeight) {
    Data output = fBinned.getEventWeight(met.et(), isData);

    if(fBinned.getMode() == BinnedEfficiencyScaleFactor::kScaleFactor) {
      hScaleFactor->Fill(output.getEventWeight());
    }
    eventWeight.multiplyWeight(output.getEventWeight());
    return output;
  }

  double METTriggerEfficiencyScaleFactor::getEventWeight(const reco::MET& met) {
    return fBinned.getEventWeight(met.et(), false).getEventWeight();
  }
}
