// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EfficiencyScaleFactorBase_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EfficiencyScaleFactorBase_h


namespace edm {
  class ParameterSet;
}

namespace HPlus {
  class EfficiencyScaleFactorBase {
  public:
    enum Mode {
      kEfficiency,
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
        return fWeightRelUnc;
      }

    protected:
      double fWeight;
      double fWeightAbsUnc;
      double fWeightRelUnc;
    };

    explicit EfficiencyScaleFactorBase(const edm::ParameterSet& iConfig);
    ~EfficiencyScaleFactorBase();

    Mode getMode() const { return fMode; }
  private:
    Mode fMode;
  };
}


#endif
