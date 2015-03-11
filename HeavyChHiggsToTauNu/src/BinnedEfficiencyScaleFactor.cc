#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BinnedEfficiencyScaleFactor.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"

#include<cmath>
#include<algorithm>
#include<iostream>

#include "boost/property_tree/ptree.hpp"
#include "boost/property_tree/json_parser.hpp"
#include "boost/foreach.hpp"

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

  template <typename T>
  T square(T x) {
    return x*x;
  }
}

namespace HPlus {
  BinnedEfficiencyScaleFactor::Data::Data() {}
  BinnedEfficiencyScaleFactor::Data::~Data() {}

  BinnedEfficiencyScaleFactor::BinnedEfficiencyScaleFactor(const edm::ParameterSet& iConfig, const std::string& quantity):
    EfficiencyScaleFactorBase(iConfig) {

    if(getMode() == kDisabled)
      return;

    std::vector<std::string> dataSelects = iConfig.getParameter<std::vector<std::string> >("dataSelect");
    std::string mcSelect = iConfig.getParameter<std::string>("mcSelect");

    if(dataSelects.empty()) {
      throw cms::Exception("Configuration") << "BinnedEfficiencyScaleFactor: Must select at least one data run period in dataSelect" << std::endl;
    }

    // Read the efficiency data
    edm::FileInPath dataPath = iConfig.getParameter<edm::FileInPath>("data");
    double totalLuminosity = 0;
    try {
      using boost::property_tree::ptree;
      ptree data;
      boost::property_tree::read_json(dataPath.fullPath(), data);

      // Get MC efficiencies for the given MC era
      ptree& mcParameters = data.get_child("mcParameters").get_child(mcSelect);
      BOOST_FOREACH(ptree::value_type& v, mcParameters.get_child("bins")) {
        double bin = v.second.get<double>(quantity);
        if(!fBinLowEdges.empty() && bin <= fBinLowEdges.back())
          throw cms::Exception("Configuration") << "BinnedEfficiencyScaleFactor:  Bins must be in an ascending order of lowEdges (new "
                                                << bin << " previous " << fBinLowEdges.back() << ")"
                                                << " in mcParameters." << mcSelect
                                                << std::endl;
        fBinLowEdges.push_back(bin);
        fData.fEffMCValues.push_back(v.second.get<double>("efficiency"));
        std::pair<double, double> uncPlusMinus = parseUncertainty(v.second);
        fData.fEffMCUncertaintiesPlus.push_back(uncPlusMinus.first);
        fData.fEffMCUncertaintiesMinus.push_back(uncPlusMinus.second);
      }

      // Get data efficiencies for the given run periods, calculate the
      // total luminosity of those periods for the weighted average of
      // scale factors
      for(std::vector<std::string>::const_iterator iSelect = dataSelects.begin(); iSelect != dataSelects.end(); ++iSelect) {
        ptree& pset = data.get_child("dataParameters").get_child(*iSelect);
        ptree& dataBins = pset.get_child("bins");
        if(dataBins.size() != fBinLowEdges.size())
          throw cms::Exception("Configuration") << "TauTriggerEfficiencyScaleFactor: dataParameters." << *iSelect << " must have same number of bins as mcParameters." << mcSelect << ", now data has " << dataBins.size() << " while mc has " << fBinLowEdges.size() << std::endl;

        EffData::DataValue dv;
        dv.firstRun = pset.get<unsigned>("firstRun");
        dv.lastRun = pset.get<unsigned>("lastRun");
        dv.luminosity = pset.get<double>("luminosity");
        totalLuminosity += dv.luminosity;

        int i=0;
        BOOST_FOREACH(ptree::value_type& v, dataBins) {
          double bin = v.second.get<double>(quantity);

          if(!doubleEqual(bin, fBinLowEdges[i]))
            throw cms::Exception("Configuration") << "TauTriggerEfficiencyScaleFactor: Bin " << i << " in dataParameters." << *iSelect << " must have same low edge as mcParameters" << mcSelect << ", now data hs " << bin << " while mc has " << fBinLowEdges[i] << std::endl;

          dv.values.push_back(v.second.get<double>("efficiency"));
          std::pair<double, double> uncPlusMinus = parseUncertainty(v.second);
          dv.uncertaintiesPlus.push_back(uncPlusMinus.first);
          dv.uncertaintiesMinus.push_back(uncPlusMinus.second);
          ++i;
        }
        fData.fDataValues.push_back(dv);
      }
    } catch(const std::exception& e) {
      throw cms::Exception("Configuration") << "Error in parsing efficiency JSON " << dataPath.fullPath()
                                            << ":\n" << e.what();
    }

    // Calculate the scale factor in tau pt bins as data/MC, where
    // data is the luminosity weighted average.
    bool print = iConfig.getUntrackedParameter<bool>("printScaleFactors", false);
    if(print)
      std::cout << "Scale factor uncertainties:" << std::endl;
    for(size_t i=0; i<fBinLowEdges.size(); ++i) {
      double dataValue = 0;
      double dataUncertaintySquaredPlus = 0;
      double dataUncertaintySquaredMinus = 0;
      if(fData.fDataValues.size() == 1) {
        dataValue = fData.fDataValues[0].values[i];
        dataUncertaintySquaredPlus = square(fData.fDataValues[0].uncertaintiesPlus[i]);
        dataUncertaintySquaredMinus = square(fData.fDataValues[0].uncertaintiesMinus[i]);
      }
      else {
        for(size_t iPeriod = 0; iPeriod != fData.fDataValues.size(); ++iPeriod) {
          double lumi = fData.fDataValues[iPeriod].luminosity;
          dataValue += lumi*fData.fDataValues[iPeriod].values[i];
          dataUncertaintySquaredPlus += square(lumi*fData.fDataValues[iPeriod].uncertaintiesPlus[i]);
          dataUncertaintySquaredMinus += square(lumi*fData.fDataValues[iPeriod].uncertaintiesMinus[i]);
        }
        dataValue = dataValue / totalLuminosity;
        dataUncertaintySquaredPlus = dataUncertaintySquaredPlus / square(totalLuminosity);
        dataUncertaintySquaredMinus = dataUncertaintySquaredMinus / square(totalLuminosity);
      }
      fData.fEffDataAverageValues.push_back(dataValue);
      fData.fEffDataAverageUncertaintiesPlus.push_back(std::sqrt(dataUncertaintySquaredPlus));
      fData.fEffDataAverageUncertaintiesMinus.push_back(std::sqrt(dataUncertaintySquaredMinus));

      // Vary data and MC efficiencies, if enabled
      for(size_t iPeriod = 0; iPeriod != fData.fDataValues.size(); ++iPeriod) {
        varyData(&fData.fDataValues[iPeriod].values[i], &fData.fDataValues[iPeriod].uncertaintiesPlus[i], &fData.fDataValues[iPeriod].uncertaintiesMinus[i]);
      }
      varyData(&fData.fEffDataAverageValues.back(), &fData.fEffDataAverageUncertaintiesPlus.back(), &fData.fEffDataAverageUncertaintiesMinus.back());
      dataValue = fData.fEffDataAverageValues.back();
      varyMC(&fData.fEffMCValues[i], &fData.fEffMCUncertaintiesPlus[i], &fData.fEffMCUncertaintiesMinus[i]);

      // Take max of plus and minus for SF
      double dataRelativeUncertainty = std::sqrt(std::max(dataUncertaintySquaredPlus, dataUncertaintySquaredMinus))/dataValue;

      double mcValue = fData.fEffMCValues[i];
      double mcRelativeUncertainty = std::max(fData.fEffMCUncertaintiesPlus[i], fData.fEffMCUncertaintiesMinus[i])/mcValue;

      double scaleFactor = dataValue/mcValue;
      double scaleFactorRelativeUncertainty = std::sqrt(dataRelativeUncertainty*dataRelativeUncertainty + mcRelativeUncertainty*mcRelativeUncertainty);
      double scaleFactorAbsoluteUncertainty = scaleFactor * scaleFactorRelativeUncertainty;

      //std::cout << "Bin " << fBinLowEdges[i] << " data / mc = " << dataValue << " / " << mcValue << " = " << scaleFactor << " +- " << scaleFactorAbsoluteUncertainty << std::endl;

      // Vary SF, if enabled;
      varySF(&scaleFactor, &scaleFactorAbsoluteUncertainty);

      fData.fScaleValues.push_back(scaleFactor);
      fData.fScaleUncertainties.push_back(scaleFactorAbsoluteUncertainty);

      if(print)
        std::cout << "SF for bin " << fBinLowEdges[i] << ": scale factor " << scaleFactor << " +- " << scaleFactorAbsoluteUncertainty << std::endl;
    }
  }

  BinnedEfficiencyScaleFactor::~BinnedEfficiencyScaleFactor() {}


  void BinnedEfficiencyScaleFactor::setRun(unsigned run) {
    if(getMode() == kDisabled)
      return;

    fData.setRun(run);
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
    if(!fData.fCurrentRunData) throw cms::Exception("Assert") << "BinnedEfficiencyScaleFactor: Must call BinnedEfficiencyScaleFactor::setRun() before dataEfficiency()" << std::endl;
    return fData.fCurrentRunData->values[index(value)];
  }
  double BinnedEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertaintyPlus(double value) const {
    if(!fData.fCurrentRunData) throw cms::Exception("Assert") << "BinnedEfficiencyScaleFactor: Must call BinnedEfficiencyScaleFactor::setRun() before dataEfficiencyAbsoluteUncertaintyPlus()" << std::endl;
    return fData.fCurrentRunData->uncertaintiesPlus[index(value)];
  }
  double BinnedEfficiencyScaleFactor::dataEfficiencyAbsoluteUncertaintyMinus(double value) const {
    if(!fData.fCurrentRunData) throw cms::Exception("Assert") << "BinnedEfficiencyScaleFactor: Must call BinnedEfficiencyScaleFactor::setRun() before dataEfficiencyAbsoluteUncertaintyMinus()" << std::endl;
    return fData.fCurrentRunData->uncertaintiesMinus[index(value)];
  }

  double BinnedEfficiencyScaleFactor::dataAverageEfficiency(double value) const {
    return fData.fEffDataAverageValues[index(value)];
  }
  double BinnedEfficiencyScaleFactor::dataAverageEfficiencyAbsoluteUncertaintyPlus(double value) const {
    return fData.fEffDataAverageUncertaintiesPlus[index(value)];
  }
  double BinnedEfficiencyScaleFactor::dataAverageEfficiencyAbsoluteUncertaintyMinus(double value) const {
    return fData.fEffDataAverageUncertaintiesMinus[index(value)];
  }

  double BinnedEfficiencyScaleFactor::mcEfficiency(double value) const {
    return fData.fEffMCValues[index(value)];
  }
  double BinnedEfficiencyScaleFactor::mcEfficiencyAbsoluteUncertaintyPlus(double value) const {
    return fData.fEffMCUncertaintiesPlus[index(value)];
  }
  double BinnedEfficiencyScaleFactor::mcEfficiencyAbsoluteUncertaintyMinus(double value) const {
    return fData.fEffMCUncertaintiesMinus[index(value)];
  }

  double BinnedEfficiencyScaleFactor::scaleFactor(double value) const {
    return fData.fScaleValues[index(value)];
  }
  double BinnedEfficiencyScaleFactor::scaleFactorAbsoluteUncertainty(double value) const {
    return fData.fScaleUncertainties[index(value)];
  }


  BinnedEfficiencyScaleFactor::Data BinnedEfficiencyScaleFactor::getEventWeight(double value, bool isData) const {
    Data output;

    if(getMode() == kScaleFactor) {
      output.fWeight = scaleFactor(value);
      output.fWeightAbsUncPlus = scaleFactorAbsoluteUncertainty(value);
      output.fWeightAbsUncMinus = output.fWeightAbsUncPlus;
    }
    else if(getMode() == kDataEfficiency) {
      if(isData) {
        if(!fData.fCurrentRunData)
          throw cms::Exception("LogicError") << "TBinnedEfficiencyScaleFactor: With efficiency mode and data input, must call setRun() before getEventWeight()" << std::endl;
        output.fWeight = dataEfficiency(value);
        output.fWeightAbsUncPlus = dataEfficiencyAbsoluteUncertaintyPlus(value);
        output.fWeightAbsUncMinus = dataEfficiencyAbsoluteUncertaintyMinus(value);
      }
      else {
        // Efficiency mode is needed only for embedding, and in there
        // for MC using the luminosity-averaged efficiency from data
        // makes more sense than the efficiency of MC, because the
        // comparison will always be with respect to the efficiency of
        // data.
        output.fWeight = dataAverageEfficiency(value);
        output.fWeightAbsUncPlus = dataAverageEfficiencyAbsoluteUncertaintyPlus(value);
        output.fWeightAbsUncMinus = dataAverageEfficiencyAbsoluteUncertaintyMinus(value);
        /*
        output.fWeight = mcEfficiency(value);
        output.fWeightAbsUnc = mcEfficiencyAbsoluteUncertainty(value);
        output.fWeightRelUnc = mcEfficiencyRelativeUncertainty(value);
        */
      }
    }
    else if(getMode() == kMCEfficiency) {
      output.fWeight = mcEfficiency(value);
      output.fWeightAbsUncPlus = mcEfficiencyAbsoluteUncertaintyPlus(value);
      output.fWeightAbsUncMinus = mcEfficiencyAbsoluteUncertaintyMinus(value);
    }

    return output;
  }
}
