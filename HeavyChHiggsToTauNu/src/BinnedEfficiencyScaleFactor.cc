#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BinnedEfficiencyScaleFactor.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"

#include<cmath>
#include<algorithm>
#include<iostream>

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
  BinnedEfficiencyScaleFactor::Data::Data():
    fWeight(1.0),
    fWeightAbsUnc(0.0),
    fWeightRelUnc(0.0) {}
  BinnedEfficiencyScaleFactor::Data::~Data() {}

  BinnedEfficiencyScaleFactor::BinnedEfficiencyScaleFactor(const edm::ParameterSet& iConfig):
    fCurrentRunData(0) {

    std::string mode = iConfig.getUntrackedParameter<std::string>("mode");
    if(mode == "efficiency")
      fMode = kEfficiency;
    else if(mode == "scaleFactor")
      fMode = kScaleFactor;
    else if(mode == "disabled")
      fMode = kDisabled;
    else
      throw cms::Exception("Configuration") << "BinnedEfficiencyScaleFactor: Unsupported value for parameter 'mode' " << mode << ", should be 'efficiency', 'scaleFactor', or 'disabled'" << std::endl;

    if(fMode == kDisabled)
      return;

    edm::ParameterSet dataParameters = iConfig.getParameter<edm::ParameterSet>("dataParameters");
    edm::ParameterSet mcParameters = iConfig.getParameter<edm::ParameterSet>("mcParameters");

    std::vector<std::string> dataSelects = iConfig.getParameter<std::vector<std::string> >("dataSelect");
    std::string mcSelect = iConfig.getParameter<std::string>("mcSelect");

    if(dataSelects.empty()) {
      throw cms::Exception("Configuration") << "BinnedEfficiencyScaleFactor: Must select at least one data run period in dataSelect" << std::endl;
    }

    // Get MC efficiencies for the given MC era
    edm::ParameterSet pset = mcParameters.getParameter<edm::ParameterSet>(mcSelect);
    std::vector<edm::ParameterSet> mcBins = pset.getParameter<std::vector<edm::ParameterSet> >("bins");
    for(size_t i=0; i<mcBins.size(); ++i) {
      double bin = mcBins[i].getParameter<double>("pt");
      if(!fBinLowEdges.empty() && bin <= fBinLowEdges.back())
        throw cms::Exception("Configuration") << "BinnedEfficiencyScaleFactor:  Bins must be in an ascending order of lowEdges (new "
                                              << bin << " previous " << fBinLowEdges.back() << ")"
                                              << " in mcParameters." << mcSelect
                                              << std::endl;

      fBinLowEdges.push_back(bin);
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
      if(dataBins.size() != fBinLowEdges.size())
        throw cms::Exception("Configuration") << "TauTriggerEfficiencyScaleFactor: dataParameters." << *iSelect << " must have same number of bins as mcParameters." << *iSelect << ", now data has " << dataBins.size() << " while mc has " << fBinLowEdges.size() << std::endl;

      DataValue dv;
      dv.firstRun = pset.getParameter<unsigned>("firstRun");
      dv.lastRun = pset.getParameter<unsigned>("lastRun");
      dv.luminosity = pset.getParameter<double>("luminosity");
      totalLuminosity += dv.luminosity;

      for(size_t i=0; i<dataBins.size(); ++i) {
        double bin = dataBins[i].getParameter<double>("pt");

        if(!doubleEqual(bin, fBinLowEdges[i]))
          throw cms::Exception("Configuration") << "TauTriggerEfficiencyScaleFactor: Bin " << i << " in dataParameters." << *iSelect << " must have same low edge as mcParameters" << *iSelect << ", now data hs " << bin << " while mc has " << fBinLowEdges[i] << std::endl;

        dv.values.push_back(dataBins[i].getParameter<double>("efficiency"));
        dv.uncertainties.push_back(dataBins[i].getParameter<double>("uncertainty"));
      }
      fDataValues.push_back(dv);
    }

    // Calculate the scale factor in tau pt bins as data/MC, where
    // data is the luminosity weighted average.
    std::cout << "Scale factor uncertainties:" << std::endl;
    for(size_t i=0; i<fBinLowEdges.size(); ++i) {
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

      //std::cout << "Bin " << fBinLowEdges[i] << " data / mc = " << dataValue << " / " << mcValue << " = " << scaleFactor << " +- " << scaleFactorAbsoluteUncertainty << std::endl;

      fScaleValues.push_back(scaleFactor);
      fScaleUncertainties.push_back(scaleFactorAbsoluteUncertainty);

      std::cout << "SF for bin " << fBinLowEdges[i] << ": scale factor " << scaleFactor << " +- " << scaleFactorAbsoluteUncertainty << std::endl;
    }
  }

  BinnedEfficiencyScaleFactor::~BinnedEfficiencyScaleFactor() {}


  void BinnedEfficiencyScaleFactor::setRun(unsigned run) {
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

    throw cms::Exception("LogicError") << "BinnedEfficiencyScaleFactor: No data efficiency definitions found for run " << run << ", specified run regions are " << ss.str() << std::endl;
  }

  size_t BinnedEfficiencyScaleFactor::index(double value) const {
    // find the first bin for which fBinLowEdges[bin] >= value
    std::vector<double>::const_iterator found = std::lower_bound(fBinLowEdges.begin(), fBinLowEdges.end(), value);
    if(found == fBinLowEdges.begin())
      throw cms::Exception("LogicError") << "BinnedEfficiencyScaleFactor: Got value " << value << " which is less than the first bin in the given efficiencies " << fBinLowEdges.front();
    // pick the previous bin
    --found;
    return found-fBinLowEdges.begin();
  }


  double BinnedEfficiencyScaleFactor::dataEfficiency(double value) const {
    if(!fCurrentRunData) throw cms::Exception("Assert") << "BinnedEfficiencyScaleFactor: Must call BinnedEfficiencyScaleFactor::setRun() before dataEfficiency()" << std::endl;
    return fCurrentRunData->values[index(value)];
  }
  double BinnedEfficiencyScaleFactor::dataEfficiencyRelativeUncertainty(double value) const {
    if(!fCurrentRunData) throw cms::Exception("Assert") << "BinnedEfficiencyScaleFactor: Must call BinnedEfficiencyScaleFactor::setRun() before dataEfficiencyRelativeUncertainty()" << std::endl;
    size_t i = index(value);
    return fCurrentRunData->uncertainties[i] / fCurrentRunData->values[i];
  }
  double BinnedEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertainty(double value) const {
    if(!fCurrentRunData) throw cms::Exception("Assert") << "BinnedEfficiencyScaleFactor: Must call BinnedEfficiencyScaleFactor::setRun() before dataEfficiencyAbsoluteUncertainty()" << std::endl;
    return fCurrentRunData->uncertainties[index(value)];
  }

  double BinnedEfficiencyScaleFactor::dataAverageEfficiency(double value) const {
    return fEffDataAverageValues[index(value)];
  }
  double BinnedEfficiencyScaleFactor::dataAverageEfficiencyRelativeUncertainty(double value) const {
    size_t i = index(value);
    return fEffDataAverageUncertainties[i] / fEffDataAverageValues[i];
  }
  double BinnedEfficiencyScaleFactor::dataAverageEfficiencyAbsoluteUncertainty(double value) const {
    return fEffDataAverageUncertainties[index(value)];
  }

  double BinnedEfficiencyScaleFactor::mcEfficiency(double value) const {
    return fEffMCValues[index(value)];
  }
  double BinnedEfficiencyScaleFactor::mcEfficiencyRelativeUncertainty(double value) const {
    size_t i = index(value);
    return fEffMCUncertainties[i] / fEffMCValues[i];
  }
  double BinnedEfficiencyScaleFactor::mcEfficiencyAbsoluteUncertainty(double value) const {
    return fEffMCUncertainties[index(value)];
  }


  double BinnedEfficiencyScaleFactor::scaleFactor(double value) const {
    return fScaleValues[index(value)];
  }
  double BinnedEfficiencyScaleFactor::scaleFactorRelativeUncertainty(double value) const {
    size_t i = index(value);
    return fScaleUncertainties[i] / fScaleValues[i];
  }
  double BinnedEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty(double value) const {
    return fScaleUncertainties[index(value)];
  }


  BinnedEfficiencyScaleFactor::Data BinnedEfficiencyScaleFactor::getEventWeight(double value, bool isData) const {
    Data output;

    if(fMode == kScaleFactor) {
      output.fWeight = scaleFactor(value);
      output.fWeightAbsUnc = scaleFactorAbsoluteUncertainty(value);
      output.fWeightRelUnc = scaleFactorRelativeUncertainty(value);
    }
    else if(fMode == kEfficiency) {
      if(isData) {
        if(!fCurrentRunData)
          throw cms::Exception("LogicError") << "TBinnedEfficiencyScaleFactor: With efficiency mode and data input, must call setRun() before getEventWeight()" << std::endl;
        output.fWeight = dataEfficiency(value);
        output.fWeightAbsUnc = dataEfficiencyAbsoluteUncertainty(value);
        output.fWeightRelUnc = dataEfficiencyRelativeUncertainty(value);
      }
      else {
        // Efficiency mode is needed only for embedding, and in there
        // for MC using the luminosity-averaged efficiency from data
        // makes more sense than the efficiency of MC, because the
        // comparison will always be with respect to the efficiency of
        // data.
        output.fWeight = dataAverageEfficiency(value);
        output.fWeightAbsUnc = dataAverageEfficiencyAbsoluteUncertainty(value);
        output.fWeightRelUnc = dataAverageEfficiencyRelativeUncertainty(value);
        /*
        output.fWeight = mcEfficiency(value);
        output.fWeightAbsUnc = mcEfficiencyAbsoluteUncertainty(value);
        output.fWeightRelUnc = mcEfficiencyRelativeUncertainty(value);
        */
      }
    }
    return output;
  }
  
}
