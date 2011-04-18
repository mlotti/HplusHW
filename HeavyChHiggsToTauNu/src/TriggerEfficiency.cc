#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerEfficiency.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/METReco/interface/MET.h"

#include "TMath.h"

#include<vector>
#include<algorithm>
#include<iostream>

namespace {
  struct TriggerEq: public std::binary_function<edm::ParameterSet, std::string, bool> {
    bool operator()(const edm::ParameterSet& iParam, const std::string& name) const {
      return iParam.getParameter<std::string>("trigger") == name;
    }
  };
}

namespace HPlus {
  TriggerEfficiency::EfficiencyCalculator::EfficiencyCalculator(const std::vector<double>& params): fParams(params) {
    if(fParams.size() != 6)
      throw cms::Exception("Configuration") << "EfficiencyCalculator needs exactly 6 parameters, got " << fParams.size() << std::endl;
  }
  TriggerEfficiency::EfficiencyCalculator::~EfficiencyCalculator() {}
  double TriggerEfficiency::EfficiencyCalculator::efficiency(const pat::Tau& tau, const reco::MET& met) const {
    double tauEff = fParams[0]*(TMath::Freq((std::sqrt(tau.pt())-sqrt(fParams[1]))/(2*fParams[2])));
    double metEff = fParams[3]*(TMath::Freq((std::sqrt(met.et())-sqrt(fParams[4]))/(2*fParams[5])));

    return tauEff*metEff;
  }


  TriggerEfficiency::WeightedEfficiencyCalculator::WeightedEfficiencyCalculator(): fTotalLumi(0) {}
  TriggerEfficiency::WeightedEfficiencyCalculator::~WeightedEfficiencyCalculator() {}
  double TriggerEfficiency::WeightedEfficiencyCalculator::efficiency(const pat::Tau& tau, const reco::MET& met) const {
    if(fCalculators.empty())
      return 0;
    if(fCalculators.size() == 1)
      return fCalculators[0].efficiency(tau, met);

    double eff=0;
    for(size_t i=0; i<fLumis.size(); ++i) {
      eff += fLumis[i] * fCalculators[i].efficiency(tau, met);
    }
    return eff/fTotalLumi;
  }
  void TriggerEfficiency::WeightedEfficiencyCalculator::addCalculator(double lumi, const EfficiencyCalculator& effcalc) {
    fLumis.push_back(lumi);
    fTotalLumi += lumi;
    fCalculators.push_back(effcalc);
  }


  TriggerEfficiency::TriggerEfficiency(const edm::ParameterSet& iConfig) {
    std::vector<edm::ParameterSet> selectTriggers = iConfig.getParameter<std::vector<edm::ParameterSet> >("selectTriggers");
    std::vector<edm::ParameterSet> parameters = iConfig.getParameter<std::vector<edm::ParameterSet> >("parameters");

    for(std::vector<edm::ParameterSet>::const_iterator iTrigger = selectTriggers.begin(); iTrigger != selectTriggers.end(); ++iTrigger) {
      std::string triggerName = iTrigger->getParameter<std::string>("trigger");
      double luminosity = iTrigger->getParameter<double>("luminosity");
      std::vector<edm::ParameterSet>::const_iterator iParam = std::find_if(parameters.begin(), parameters.end(), std::bind2nd(TriggerEq(), triggerName));
      if(iParam == parameters.end()) {
        throw cms::Exception("Configuration") << "No efficiency parameters for trigger " << triggerName << std::endl;
      }

      fTrueTaus.addCalculator(luminosity, EfficiencyCalculator(iParam->getParameter<std::vector<double> >("trueTauParameters")));
      fFakeTaus.addCalculator(luminosity, EfficiencyCalculator(iParam->getParameter<std::vector<double> >("fakeTauParameters")));
    }
  }
  TriggerEfficiency::~TriggerEfficiency() {}

  double TriggerEfficiency::efficiency(const pat::Tau& tau, const reco::MET& met) const {
    double eff = 0;

    if(tau.genJet())
      eff = fTrueTaus.efficiency(tau, met);
    else
      eff = fFakeTaus.efficiency(tau, met);

    std::cout << "Is true tau? " << (tau.genJet() != 0) << " tau pt " << tau.pt() << " met " << met.et() << " efficiency " << eff << std::endl;

    return eff;
  }
}
