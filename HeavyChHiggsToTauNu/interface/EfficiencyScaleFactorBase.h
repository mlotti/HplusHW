// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EfficiencyScaleFactorBase_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EfficiencyScaleFactorBase_h

#include "FWCore/Utilities/interface/Exception.h"

#include "boost/property_tree/ptree.hpp"

#include<vector>
#include<sstream>
#include<algorithm>
#include<utility>

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  class EfficiencyScaleFactorBase {
  public:
    enum Mode {
      kDataEfficiency,
      kMCEfficiency,
      kScaleFactor,
      kDisabled
    };

    class Data {
    public:
      Data();
      ~Data();

      const double getEventWeight() const {
        return fWeight;
      }
      const double getEventWeightAbsoluteUncertaintyPlus() const {
        return fWeightAbsUncPlus;
      }
      const double getEventWeightAbsoluteUncertaintyMinus() const {
        return fWeightAbsUncMinus;
      }
      const double getEventWeightAbsoluteUncertainty() const {
        return std::max(fWeightAbsUncPlus, fWeightAbsUncMinus);
      }
      const double getEventWeightRelativeUncertainty() const {
        if(fWeight == 0.0) return 0.0;
        else return getEventWeightAbsoluteUncertainty() / fWeight;
      }

    protected:
      double fWeight;
      double fWeightAbsUncPlus;
      double fWeightAbsUncMinus;
    };

    explicit EfficiencyScaleFactorBase(const edm::ParameterSet& iConfig);
    virtual ~EfficiencyScaleFactorBase();

    Mode getMode() const { return fMode; }

    virtual void setRun(unsigned run) = 0;

    std::pair<double, double> parseUncertainty(const edm::ParameterSet& pset);
    std::pair<double, double> parseUncertainty(const boost::property_tree::ptree& pset);

  protected:
    void varyData(double *eff, double *uncPlus, double *uncMinus) const;
    void varyMC(double *eff, double *uncPlus, double *uncMinus) const;
    void varySF(double *sf, double *unc) const;

    const bool fUseMaxUncertainty;
    const bool fVariationEnabled;

  private:
    Mode fMode;
    double fVariationSFShiftBy;
    double fVariationDataShiftBy;
    double fVariationMCShiftBy;
  };

  template <typename T>
  struct EfficiencyScaleFactorData {
    EfficiencyScaleFactorData(): fCurrentRunData(0) {}
    ~EfficiencyScaleFactorData() {}

    void setRun(unsigned run) {
      fCurrentRunData = 0;
      for(size_t i=0; i<fDataValues.size(); ++i) {
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

      throw cms::Exception("LogicError") << "EfficiencyScaleFactorData: No data efficiency definitions found for run " << run << ", specified run regions are " << ss.str();
    }

    struct DataValue {
      unsigned firstRun;
      unsigned lastRun;
      double luminosity;
      T values;
      T uncertaintiesPlus;
      T uncertaintiesMinus;
    };
    std::vector<DataValue> fDataValues;
    const DataValue *fCurrentRunData;

    T fEffDataAverageValues;
    T fEffDataAverageUncertaintiesPlus;
    T fEffDataAverageUncertaintiesMinus;
    T fEffMCValues;
    T fEffMCUncertaintiesPlus;
    T fEffMCUncertaintiesMinus;

    T fScaleValues;
    T fScaleUncertainties;
  };
}


#endif
