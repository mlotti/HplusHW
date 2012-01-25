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

namespace {
  bool doubleEqual(double a, double b) {
    const double epsilon = 0.0001;
    if(a != 0)
      return std::abs( (a-b)/a ) < epsilon;
    else if(b != 0)
      return std::abs( (a-b)/b ) < epsilon;
    else
      return true;
  }
}

namespace HPlus {
  TriggerEfficiencyScaleFactor::Data::Data(const TriggerEfficiencyScaleFactor *tesf): fTesf(tesf) {}
  TriggerEfficiencyScaleFactor::Data::~Data() {}
  
  TriggerEfficiencyScaleFactor::TriggerEfficiencyScaleFactor(const edm::ParameterSet& iConfig, EventWeight& eventWeight):
    fEventWeight(eventWeight), fCurrentRunData(0) {

    std::string mode = iConfig.getUntrackedParameter<std::string>("mode");
    if(mode == "efficiency")
      fMode = kEfficiency;
    else if(mode == "scaleFactor")
      fMode = kScaleFactor;
    else if(mode == "disabled")
      fMode = kDisabled;
    else
      throw cms::Exception("Configuration") << "TriggerEfficiencyScaleFactor: Unsupported value for parameter 'mode' " << mode << ", should be 'efficiency', 'scaleFactor', or 'disabled'" << std::endl;

    if(fMode == kDisabled)
      return;

    edm::ParameterSet dataParameters = iConfig.getParameter<edm::ParameterSet>("dataParameters");
    edm::ParameterSet mcParameters = iConfig.getParameter<edm::ParameterSet>("mcParameters");

    std::vector<std::string> dataSelects = iConfig.getParameter<std::vector<std::string> >("dataSelect");
    std::string mcSelect = iConfig.getParameter<std::string>("mcSelect");

    if(dataSelects.empty()) {
      throw cms::Exception("Configuration") << "TriggerEfficiencyScaleFactor: Must select at least one data run period in dataSelect" << std::endl;
    }

    // Get MC efficiencies for the given MC era
    edm::ParameterSet pset = mcParameters.getParameter<edm::ParameterSet>(mcSelect);
    std::vector<edm::ParameterSet> mcBins = pset.getParameter<std::vector<edm::ParameterSet> >("bins");
    for(size_t i=0; i<mcBins.size(); ++i) {
      double bin = mcBins[i].getParameter<double>("pt");
      if(!fPtBinLowEdges.empty() && bin <= fPtBinLowEdges.back())
        throw cms::Exception("Configuration") << "TriggerEfficiencyScaleFactor:  Bins must be in an ascending order of lowEdges (new "
                                              << bin << " previous " << fPtBinLowEdges.back() << ")"
                                              << " in mcParameters." << mcSelect
                                              << std::endl;

      fPtBinLowEdges.push_back(bin);
      fEffMCValues.push_back(mcBins[i].getParameter<double>("efficiency"));
      fEffMCUncertainties.push_back(mcBins[i].getParameter<double>("uncertainty"));
    }

    // Get data efficiencies for the given run periods, calculate the
    // total luminosity of those periods for the weighted average of
    // scale factors
    double totalLuminosity = 0;
    for(std::vector<std::string>::const_iterator iSelect = dataSelects.begin(); iSelect != dataSelects.end(); ++iSelect) {
      edm::ParameterSet pset = dataParameters.getParameter<edm::ParameterSet>(*iSelect);

      std::vector<edm::ParameterSet> dataBins = pset.getParameter<std::vector<edm::ParameterSet> >("bins");
      if(dataBins.size() != fPtBinLowEdges.size())
        throw cms::Exception("Configuration") << "TriggerEfficiencyScaleFactor: dataParameters." << *iSelect << " must have same number of bins as mcParameters." << *iSelect << ", now data has " << dataBins.size() << " while mc has " << fPtBinLowEdges.size() << std::endl;

      DataValue dv;
      dv.firstRun = pset.getParameter<unsigned>("firstRun");
      dv.lastRun = pset.getParameter<unsigned>("lastRun");
      dv.luminosity = pset.getParameter<double>("luminosity");
      totalLuminosity += dv.luminosity;

      for(size_t i=0; i<dataBins.size(); ++i) {
        double bin = dataBins[i].getParameter<double>("pt");

        if(!doubleEqual(bin, fPtBinLowEdges[i]))
          throw cms::Exception("Configuration") << "TriggerEfficiencyScaleFactor: Bin " << i << " in dataParameters." << *iSelect << " must have same low edge as mcParameters" << *iSelect << ", now data hs " << bin << " while mc has " << fPtBinLowEdges[i] << std::endl;

        dv.values.push_back(dataBins[i].getParameter<double>("efficiency"));
        dv.uncertainties.push_back(dataBins[i].getParameter<double>("uncertainty"));
      }
      fDataValues.push_back(dv);
    }

    // Calculate the scale factor in tau pt bins as data/MC, where
    // data is the luminosity weighted average.
    for(size_t i=0; i<fPtBinLowEdges.size(); ++i) {
      double dataValue = 0;
      double dataUncertaintySquared = 0;
      if(fDataValues.size() == 1) {
        dataValue = fDataValues[0].values[i];
        dataUncertaintySquared = fDataValues[0].uncertainties[i];
        dataUncertaintySquared = dataUncertaintySquared*dataUncertaintySquared;
      }
      else {
        for(size_t iPeriod = 0; iPeriod != fDataValues.size(); ++iPeriod) {
          double lumi = fDataValues[iPeriod].luminosity;
          dataValue += lumi*fDataValues[iPeriod].values[i];
          double unc = lumi*fDataValues[iPeriod].uncertainties[i];
          dataUncertaintySquared = unc*unc;
        }
        dataValue = dataValue / totalLuminosity;
        dataUncertaintySquared = dataUncertaintySquared / (totalLuminosity*totalLuminosity);
      }
      fEffDataAverageValues.push_back(dataValue);
      fEffDataAverageUncertainties.push_back(std::sqrt(dataUncertaintySquared));

      double dataRelativeUncertainty = std::sqrt(dataUncertaintySquared)/dataValue;

      double mcValue = fEffMCValues[i];
      double mcRelativeUncertainty = fEffMCUncertainties[i]/mcValue;

      double scaleFactor = dataValue/mcValue;
      double scaleFactorRelativeUncertainty = std::sqrt(dataRelativeUncertainty*dataRelativeUncertainty + mcRelativeUncertainty*mcRelativeUncertainty);
      double scaleFactorAbsoluteUncertainty = scaleFactor * scaleFactorRelativeUncertainty;

      //std::cout << "Bin " << fPtBinLowEdges[i] << " data / mc = " << dataValue << " / " << mcValue << " = " << scaleFactor << " +- " << scaleFactorAbsoluteUncertainty << std::endl;

      fScaleValues.push_back(scaleFactor);
      fScaleUncertainties.push_back(scaleFactorAbsoluteUncertainty);
    }
  
    edm::Service<TFileService> fs;
    TFileDirectory dir = fs->mkdir("TriggerScaleFactor");
    hScaleFactor = makeTH<TH1F>(dir, "TriggerScaleFactor", "TriggerScaleFactor;TriggerScaleFactor;N_{events}/0.01", 200., 0., 2.0);

    const size_t NBUF = 10;
    char buf[NBUF];
    TH1 *hsf = makeTH<TH1F>(dir, "ScaleFactor", "Scale factor;Tau p_{T} bin;Scale factor", fPtBinLowEdges.size()+1, 0, fPtBinLowEdges.size()+1);
    TH1 *hsfu = makeTH<TH1F>(dir, "ScaleFactorUncertainty", "Scale factor;Tau p_{T} bin;Scale factor uncertainty", fPtBinLowEdges.size()+1, 0, fPtBinLowEdges.size()+1);
    hsf->SetBinContent(1, 1); hsf->GetXaxis()->SetBinLabel(1, "control");
    hsfu->SetBinContent(1, 1); hsf->GetXaxis()->SetBinLabel(1, "control");
    for(size_t i=0; i<fPtBinLowEdges.size(); ++i) {
      size_t bin = i+2;
      snprintf(buf, NBUF, "%.0f", fPtBinLowEdges[i]);

      hsf->SetBinContent(bin, scaleFactor(i));
      hsfu->SetBinContent(bin, scaleFactorAbsoluteUncertainty(i));
      hsf->GetXaxis()->SetBinLabel(bin, buf);
      hsfu->GetXaxis()->SetBinLabel(bin, buf);
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
      throw cms::Exception("LogicError") << "TriggerEfficiencyScaleFactor: Got tau pt " << pt << " which is less than the first bin in the given efficiencies " << fPtBinLowEdges.front();
    // pick the previous bin
    --found;
    return found-fPtBinLowEdges.begin();
  }

  void TriggerEfficiencyScaleFactor::setRun(unsigned run) {
    if(fMode == kDisabled)
      return;

    //std::cout << fDataValues.size() << fScaleValues.size() << std::endl;
    for(size_t i=0; i<fDataValues.size(); ++i) {
      //std::cout << "Period " << i << " " << fDataValues[i].firstRun << "-" << fDataValues[i].lastRun << ", run " << run << std::endl;
      if(fDataValues[i].firstRun <= run && run <= fDataValues[i].lastRun) {
        fCurrentRunData = &(fDataValues[i]);
        return;
      }
    }
    // Not found, throw exception
    std::stringstream ss;
    for(size_t i=0; i<fDataValues.size(); ++i) {
      ss << fDataValues[i].firstRun << "-" << fDataValues[i].lastRun << " ";
    }

    throw cms::Exception("LogicError") << "TriggerEfficiencyScaleFactor: No data efficiency definitions found for run " << run << ", specified run regions are " << ss.str() << std::endl;
  }

  double TriggerEfficiencyScaleFactor::dataEfficiency(const pat::Tau& tau) const {
    return dataEfficiency(index(tau));
  }
  double TriggerEfficiencyScaleFactor::dataEfficiency(size_t i) const {
    if(!fCurrentRunData) throw cms::Exception("Assert") << "TriggerEfficiencyScaleFactor: Must call TriggerEfficiencyScaleFactor::setRun() before dataEfficiency()" << std::endl;
    return fCurrentRunData->values[i];
  }
  double TriggerEfficiencyScaleFactor::dataEfficiencyRelativeUncertainty(const pat::Tau& tau) const {
    if(!fCurrentRunData) throw cms::Exception("Assert") << "TriggerEfficiencyScaleFactor: Must call TriggerEfficiencyScaleFactor::setRun() before dataEfficiencyRelativeUncertainty()" << std::endl;
    size_t i = index(tau);
    return fCurrentRunData->uncertainties[i] / fCurrentRunData->values[i];
  }
  double TriggerEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const {
    return dataEfficiencyAbsoluteUncertainty(index(tau.pt()));
  }
  double TriggerEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertainty(size_t i) const {
    if(!fCurrentRunData) throw cms::Exception("Assert") << "TriggerEfficiencyScaleFactor: Must call TriggerEfficiencyScaleFactor::setRun() before dataEfficiencyAbsoluteUncertainty()" << std::endl;
    return fCurrentRunData->uncertainties[i];
  }

  double TriggerEfficiencyScaleFactor::dataAverageEfficiency(const pat::Tau& tau) const {
    return dataAverageEfficiency(index(tau));
  }
  double TriggerEfficiencyScaleFactor::dataAverageEfficiency(size_t i) const {
    return fEffDataAverageValues[i];
  }
  double TriggerEfficiencyScaleFactor::dataAverageEfficiencyRelativeUncertainty(const pat::Tau& tau) const {
    size_t i = index(tau);
    return fEffDataAverageUncertainties[i] / fEffDataAverageValues[i];
  }
  double TriggerEfficiencyScaleFactor::dataAverageEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const {
    return dataAverageEfficiencyAbsoluteUncertainty(index(tau.pt()));
  }
  double TriggerEfficiencyScaleFactor::dataAverageEfficiencyAbsoluteUncertainty(size_t i) const {
    return fEffDataAverageUncertainties[i];
  }


  double TriggerEfficiencyScaleFactor::mcEfficiency(const pat::Tau& tau) const {
    return mcEfficiency(index(tau));
  }
  double TriggerEfficiencyScaleFactor::mcEfficiency(size_t i) const {
    return fEffMCValues[i];
  }
  double TriggerEfficiencyScaleFactor::mcEfficiencyRelativeUncertainty(const pat::Tau& tau) const {
    size_t i = index(tau);
    return fEffMCUncertainties[i] / fEffMCValues[i];
  }
  double TriggerEfficiencyScaleFactor::mcEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const {
    return mcEfficiencyAbsoluteUncertainty(index(tau.pt()));
  }
  double TriggerEfficiencyScaleFactor::mcEfficiencyAbsoluteUncertainty(size_t i) const {
    return fEffMCUncertainties[i];
  }

  double TriggerEfficiencyScaleFactor::scaleFactor(const pat::Tau& tau) const {
    return scaleFactor(index(tau));
  }
  double TriggerEfficiencyScaleFactor::scaleFactor(size_t i) const {
    return fScaleValues[i];
  }
  double TriggerEfficiencyScaleFactor::scaleFactorRelativeUncertainty(const pat::Tau& tau) const {
    size_t i = index(tau);
    return fScaleUncertainties[i] / fScaleValues[i];
  }
  double TriggerEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty(const pat::Tau& tau) const {
    return scaleFactorAbsoluteUncertainty(index(tau));
  }
  double TriggerEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty(size_t i) const {
    return fScaleUncertainties[i];
  }

  TriggerEfficiencyScaleFactor::Data TriggerEfficiencyScaleFactor::applyEventWeight(const pat::Tau& tau, bool isData) {
    fWeight = 1.0;
    fWeightAbsUnc = 0.0;
    fWeightRelUnc = 0.0;
    if(fMode == kScaleFactor) {
      fWeight = scaleFactor(tau);
      fWeightAbsUnc = scaleFactorAbsoluteUncertainty(tau);
      fWeightRelUnc = scaleFactorRelativeUncertainty(tau);

      hScaleFactor->Fill(fWeight, fEventWeight.getWeight());
    }
    else if(fMode == kEfficiency) {
      if(isData) {
        if(!fCurrentRunData)
          throw cms::Exception("LogicError") << "TriggerEfficiencyScaleFactor: With efficiency mode and data input, must call setRun() before applyEventWeight()" << std::endl;
        fWeight = dataEfficiency(tau);
        fWeightAbsUnc = dataEfficiencyAbsoluteUncertainty(tau);
        fWeightRelUnc = dataEfficiencyRelativeUncertainty(tau);
      }
      else {
        // Efficiency mode is needed only for embedding, and in there
        // for MC using the luminosity-averaged efficiency from data
        // makes more sense than the efficiency of MC, because the
        // comparison will always be with respect to the efficiency of
        // data.
        fWeight = dataAverageEfficiency(tau);
        fWeightAbsUnc = dataAverageEfficiencyAbsoluteUncertainty(tau);
        fWeightRelUnc = dataAverageEfficiencyRelativeUncertainty(tau);
        /*
        fWeight = mcEfficiency(tau);
        fWeightAbsUnc = mcEfficiencyAbsoluteUncertainty(tau);
        fWeightRelUnc = mcEfficiencyRelativeUncertainty(tau);
        */
      }
    }
    fEventWeight.multiplyWeight(fWeight);
    return Data(this);
  }
}
