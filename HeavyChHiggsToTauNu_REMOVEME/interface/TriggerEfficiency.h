// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerEfficiency_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerEfficiency_h

#include<vector>

namespace edm {
  class ParameterSet;
}
namespace reco {
  class MET;
}
namespace pat {
  class Tau;
}

namespace HPlus {
  class TriggerEfficiency {
  public:
    class EfficiencyCalculatorBase {
    public:
      EfficiencyCalculatorBase();
      virtual ~EfficiencyCalculatorBase();

      virtual double efficiency(const pat::Tau& tau, const reco::MET& met) const = 0;
    };

  private:
    class WeightedEfficiencyCalculator {
    public:
      WeightedEfficiencyCalculator();
      ~WeightedEfficiencyCalculator();

      double efficiency(const pat::Tau& tau, const reco::MET& met) const;
      void addCalculator(double lumi, EfficiencyCalculatorBase *effcalc);
    private:
      std::vector<EfficiencyCalculatorBase *> fCalculators;
      std::vector<double> fLumis;
      double fTotalLumi;
    };


  public:
    TriggerEfficiency(const edm::ParameterSet& iConfig);
    ~TriggerEfficiency();

    double efficiency(const pat::Tau& tau, const reco::MET& met) const;
  private:
    WeightedEfficiencyCalculator fTrueTaus;
    WeightedEfficiencyCalculator fFakeTaus;
  };

}


#endif
