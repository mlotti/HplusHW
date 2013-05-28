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

    double dataEfficiency() const;
    double dataEfficiencyRelativeUncertainty() const;
    double dataEfficiencyAbsoluteUncertainty() const;

    double dataAverageEfficiency() const;
    double dataAverageEfficiencyRelativeUncertainty() const;
    double dataAverageEfficiencyAbsoluteUncertainty() const;

    double mcEfficiency() const;
    double mcEfficiencyRelativeUncertainty() const;
    double mcEfficiencyAbsoluteUncertainty() const;

    double scaleFactor() const;
    double scaleFactorRelativeUncertainty() const;
    double scaleFactorAbsoluteUncertainty() const;

    Data getEventWeight(bool isData) const;

  private:
    EfficiencyScaleFactorData<double> fData;
  };
}

#endif
