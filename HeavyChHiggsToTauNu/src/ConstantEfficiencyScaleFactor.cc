#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ConstantEfficiencyScaleFactor.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include<cmath>
#include<algorithm>
#include<iostream>

namespace HPlus {
  ConstantEfficiencyScaleFactor::Data::Data() {}
  ConstantEfficiencyScaleFactor::Data::~Data() {}

  ConstantEfficiencyScaleFactor::ConstantEfficiencyScaleFactor(const edm::ParameterSet& iConfig):
    EfficiencyScaleFactorBase(iConfig) {

    if(getMode() == kDisabled)
      return;

    edm::ParameterSet dataParameters = iConfig.getParameter<edm::ParameterSet>("dataParameters");
    edm::ParameterSet mcParameters = iConfig.getParameter<edm::ParameterSet>("mcParameters");

    std::vector<std::string> dataSelects = iConfig.getParameter<std::vector<std::string> >("dataSelect");
    std::string mcSelect = iConfig.getParameter<std::string>("mcSelect");

    if(dataSelects.empty()) {
      throw cms::Exception("Configuration") << "ConstantEfficiencyScaleFactor: Must select at least one data run period in dataSelect" << std::endl;
    }

    // Get MC efficiencies for the given MC era
    edm::ParameterSet pset = mcParameters.getParameter<edm::ParameterSet>(mcSelect);
    fData.fEffMCValues = pset.getParameter<double>("efficiency");
    fData.fEffMCUncertainties = pset.getParameter<double>("uncertainty");

    // Get data efficiencies for the given run periods, calculate the
    // total luminosity of those periods for the weighted average of
    // scale factors
    double totalLuminosity = 0;
    for(std::vector<std::string>::const_iterator iSelect = dataSelects.begin(); iSelect != dataSelects.end(); ++iSelect) {
      edm::ParameterSet pset = dataParameters.getParameter<edm::ParameterSet>(*iSelect);
      EfficiencyScaleFactorData<double>::DataValue dv;
      dv.firstRun = pset.getParameter<unsigned>("firstRun");
      dv.lastRun = pset.getParameter<unsigned>("lastRun");
      dv.luminosity = pset.getParameter<double>("luminosity");
      totalLuminosity += dv.luminosity;

      dv.values = pset.getParameter<double>("efficiency");
      dv.uncertainties = pset.getParameter<double>("uncertainty");

      fData.fDataValues.push_back(dv);
    }

    // Calculate the scale factor in tau pt bins as data/MC, where
    // data is the luminosity weighted average.
    bool print = iConfig.getUntrackedParameter<bool>("printScaleFactors", false);
    if(print)
      std::cout << "Scale factor uncertainties:" << std::endl;
    double dataValue = 0;
    double dataUncertaintySquared = 0;
    if(fData.fDataValues.size() == 1) {
      dataValue = fData.fDataValues[0].values;
      dataUncertaintySquared = fData.fDataValues[0].uncertainties;
      dataUncertaintySquared = dataUncertaintySquared*dataUncertaintySquared;
    }
    else {
      for(size_t iPeriod = 0; iPeriod != fData.fDataValues.size(); ++iPeriod) {
        double lumi = fData.fDataValues[iPeriod].luminosity;
        dataValue += lumi*fData.fDataValues[iPeriod].values;
        double unc = lumi*fData.fDataValues[iPeriod].uncertainties;
        dataUncertaintySquared += unc*unc;
      }
      dataValue = dataValue / totalLuminosity;
      dataUncertaintySquared = dataUncertaintySquared / (totalLuminosity*totalLuminosity);
    }
    fData.fEffDataAverageValues = dataValue;
    fData.fEffDataAverageUncertainties = std::sqrt(dataUncertaintySquared);

    double dataRelativeUncertainty = std::sqrt(dataUncertaintySquared)/dataValue;

    double mcValue = fData.fEffMCValues;
    double mcRelativeUncertainty = fData.fEffMCUncertainties/mcValue;

    double scaleFactor = dataValue/mcValue;
    double scaleFactorRelativeUncertainty = std::sqrt(dataRelativeUncertainty*dataRelativeUncertainty + mcRelativeUncertainty*mcRelativeUncertainty);
    double scaleFactorAbsoluteUncertainty = scaleFactor * scaleFactorRelativeUncertainty;

    //std::cout << "Bin " << fBinLowEdges[i] << " data / mc = " << dataValue << " / " << mcValue << " = " << scaleFactor << " +- " << scaleFactorAbsoluteUncertainty << std::endl;

    fData.fScaleValues = scaleFactor;
    fData.fScaleUncertainties = scaleFactorAbsoluteUncertainty;

    if(print)
      std::cout << "SF: scale factor " << scaleFactor << " +- " << scaleFactorAbsoluteUncertainty << std::endl;
  }

  ConstantEfficiencyScaleFactor::~ConstantEfficiencyScaleFactor() {}


  void ConstantEfficiencyScaleFactor::setRun(unsigned run) {
    if(getMode() == kDisabled)
      return;
    fData.setRun(run);
  }

  double ConstantEfficiencyScaleFactor::dataEfficiency() const {
    if(!fData.fCurrentRunData) throw cms::Exception("Assert") << "ConstantEfficiencyScaleFactor: Must call ConstantEfficiencyScaleFactor::setRun() before dataEfficiency()" << std::endl;
    return fData.fCurrentRunData->values;
  }
  double ConstantEfficiencyScaleFactor::dataEfficiencyRelativeUncertainty() const {
    if(!fData.fCurrentRunData) throw cms::Exception("Assert") << "ConstantEfficiencyScaleFactor: Must call ConstantEfficiencyScaleFactor::setRun() before dataEfficiencyRelativeUncertainty()" << std::endl;
    return fData.fCurrentRunData->uncertainties / fData.fCurrentRunData->values;
  }
  double ConstantEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertainty() const {
    if(!fData.fCurrentRunData) throw cms::Exception("Assert") << "ConstantEfficiencyScaleFactor: Must call ConstantEfficiencyScaleFactor::setRun() before dataEfficiencyAbsoluteUncertainty()" << std::endl;
    return fData.fCurrentRunData->uncertainties;
  }

  double ConstantEfficiencyScaleFactor::dataAverageEfficiency() const {
    return fData.fEffDataAverageValues;
  }
  double ConstantEfficiencyScaleFactor::dataAverageEfficiencyRelativeUncertainty() const {
    return fData.fEffDataAverageUncertainties / fData.fEffDataAverageValues;
  }
  double ConstantEfficiencyScaleFactor::dataAverageEfficiencyAbsoluteUncertainty() const {
    return fData.fEffDataAverageUncertainties;
  }

  double ConstantEfficiencyScaleFactor::mcEfficiency() const {
    return fData.fEffMCValues;
  }
  double ConstantEfficiencyScaleFactor::mcEfficiencyRelativeUncertainty() const {
    return fData.fEffMCUncertainties / fData.fEffMCValues;
  }
  double ConstantEfficiencyScaleFactor::mcEfficiencyAbsoluteUncertainty() const {
    return fData.fEffMCUncertainties;
  }


  double ConstantEfficiencyScaleFactor::scaleFactor() const {
    return fData.fScaleValues;
  }
  double ConstantEfficiencyScaleFactor::scaleFactorRelativeUncertainty() const {
    return fData.fScaleUncertainties / fData.fScaleValues;
  }
  double ConstantEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty() const {
    return fData.fScaleUncertainties;
  }


  ConstantEfficiencyScaleFactor::Data ConstantEfficiencyScaleFactor::getEventWeight(bool isData) const {
    Data output;

    if(getMode() == kScaleFactor) {
      output.fWeight = scaleFactor();
      output.fWeightAbsUnc = scaleFactorAbsoluteUncertainty();
    }
    else if(getMode() == kDataEfficiency) {
      if(isData) {
        if(!fData.fCurrentRunData)
          throw cms::Exception("LogicError") << "ConstantEfficiencyScaleFactor: With efficiency mode and data input, must call setRun() before getEventWeight()" << std::endl;
        output.fWeight = dataEfficiency();
        output.fWeightAbsUnc = dataEfficiencyAbsoluteUncertainty();
      }
      else {
        // Efficiency mode is needed only for embedding, and in there
        // for MC using the luminosity-averaged efficiency from data
        // makes more sense than the efficiency of MC, because the
        // comparison will always be with respect to the efficiency of
        // data.
        output.fWeight = dataAverageEfficiency();
        output.fWeightAbsUnc = dataAverageEfficiencyAbsoluteUncertainty();
        /*
        output.fWeight = mcEfficiency(value);
        output.fWeightAbsUnc = mcEfficiencyAbsoluteUncertainty(value);
        output.fWeightRelUnc = mcEfficiencyRelativeUncertainty(value);
        */
      }
    }
    else if(getMode() == kMCEfficiency) {
      output.fWeight = mcEfficiency();
      output.fWeightAbsUnc = mcEfficiencyAbsoluteUncertainty();
    }
    return output;
  }
  
}
