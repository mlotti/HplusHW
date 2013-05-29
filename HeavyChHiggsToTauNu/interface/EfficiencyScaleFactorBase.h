// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EfficiencyScaleFactorBase_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EfficiencyScaleFactorBase_h

#include "FWCore/Utilities/interface/Exception.h"

#include<vector>
#include<sstream>

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
      const double getEventWeightAbsoluteUncertainty() const {
        return fWeightAbsUnc;
      }
      const double getEventWeightRelativeUncertainty() const {
        if(fWeight == 0.0) return 0.0;
        else return fWeightAbsUnc / fWeight;
      }

    protected:
      double fWeight;
      double fWeightAbsUnc;
    };

    explicit EfficiencyScaleFactorBase(const edm::ParameterSet& iConfig);
    virtual ~EfficiencyScaleFactorBase();

    Mode getMode() const { return fMode; }

    virtual void setRun(unsigned run) = 0;

  protected:
    const bool fVariationEnabled;
    const double fVariationShiftBy;

  private:
    Mode fMode;
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
      T uncertainties;
    };
    std::vector<DataValue> fDataValues;
    const DataValue *fCurrentRunData;

    T fEffDataAverageValues;
    T fEffDataAverageUncertainties;
    T fEffMCValues;
    T fEffMCUncertainties;

    T fScaleValues;
    T fScaleUncertainties;
  };
}


#endif
