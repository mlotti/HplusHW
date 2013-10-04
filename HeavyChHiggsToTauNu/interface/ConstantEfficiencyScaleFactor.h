// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ConstantEfficiencyScaleFactor_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ConstantEfficiencyScaleFactor_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EfficiencyScaleFactorBase.h"

#include<vector>
#include<string>

namespace HPlus {
  class ConstantEfficiencyScaleFactor: public EfficiencyScaleFactorBase {
  public:
    class Data: public EfficiencyScaleFactorBase::Data {
    public:
      Data();
      ~Data();

      friend class ConstantEfficiencyScaleFactor;
    };

    explicit ConstantEfficiencyScaleFactor(const edm::ParameterSet& iConfig);
    ~ConstantEfficiencyScaleFactor();

    void setRun(unsigned run);

    Data getEventWeight(bool isData) const;

  private:
    double dataEfficiency() const;
    double dataEfficiencyAbsoluteUncertaintyPlus() const;
    double dataEfficiencyAbsoluteUncertaintyMinus() const;

    double dataAverageEfficiency() const;
    double dataAverageEfficiencyAbsoluteUncertaintyPlus() const;
    double dataAverageEfficiencyAbsoluteUncertaintyMinus() const;

    double mcEfficiency() const;
    double mcEfficiencyAbsoluteUncertainty() const;
    double mcEfficiencyAbsoluteUncertaintyPlus() const;
    double mcEfficiencyAbsoluteUncertaintyMinus() const;

    double scaleFactor() const;
    double scaleFactorAbsoluteUncertainty() const;

    EfficiencyScaleFactorData<double> fData;
  };
}

#endif
