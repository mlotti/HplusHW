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
    class EfficiencyCalculator {
    public:
      EfficiencyCalculator(const std::vector<double>& params);
      ~EfficiencyCalculator();

      double efficiency(const pat::Tau& tau, const reco::MET& met) const;
    private:
      std::vector<double> fParams;
    };

    class WeightedEfficiencyCalculator {
    public:
      WeightedEfficiencyCalculator();
      ~WeightedEfficiencyCalculator();

      double efficiency(const pat::Tau& tau, const reco::MET& met) const;
      void addCalculator(double lumi, const EfficiencyCalculator& effcalc);
    private:
      std::vector<EfficiencyCalculator> fCalculators;
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
