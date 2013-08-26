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
  TriggerEfficiency::EfficiencyCalculatorBase::EfficiencyCalculatorBase() {}
  TriggerEfficiency::EfficiencyCalculatorBase::~EfficiencyCalculatorBase() {}

}
namespace {
  class ParametrisedEfficiencyCalculator: public HPlus::TriggerEfficiency::EfficiencyCalculatorBase {
  public:
    ParametrisedEfficiencyCalculator(const std::vector<double>& tauParams, const std::vector<double>& metParams):
      HPlus::TriggerEfficiency::EfficiencyCalculatorBase(),
      fTauParams(tauParams),
      fMetParams(metParams)
    {
      if(fTauParams.size() != 3)
        throw cms::Exception("Configuration") << "EfficiencyCalculator needs exactly 3 tau parameters, got " << fTauParams.size() << std::endl;
      if(fMetParams.size() != 3)
        throw cms::Exception("Configuration") << "EfficiencyCalculator needs exactly 3 met parameters, got " << fMetParams.size() << std::endl;

    }
    ~ParametrisedEfficiencyCalculator() {}

    double efficiency(const pat::Tau& tau, const reco::MET& met) const {
      double tauEff = fTauParams[0]*(TMath::Freq((std::sqrt(tau.pt())-sqrt(fTauParams[1]))/(2*fTauParams[2])));
      double metEff = fMetParams[0]*(TMath::Freq((std::sqrt(met.et())-sqrt(fMetParams[1]))/(2*fMetParams[2])));

      return tauEff*metEff;
    }

  private:
    std::vector<double> fTauParams;
    std::vector<double> fMetParams;
  };


  class TauPtBinEfficiencyCalculator: public HPlus::TriggerEfficiency::EfficiencyCalculatorBase {
  public:
    explicit TauPtBinEfficiencyCalculator(const std::vector<edm::ParameterSet>& bins):
      HPlus::TriggerEfficiency::EfficiencyCalculatorBase()
    {
      fBinLowEdges.reserve(bins.size());
      fEfficiencies.reserve(bins.size());
      for(size_t i=0; i<bins.size(); ++i) {
        double lowEdge = bins[i].getParameter<double>("lowEdge");
        if(!fBinLowEdges.empty() && lowEdge <= fBinLowEdges.back())
          throw cms::Exception("Configuration") << "Bins must be in an ascending order of lowEdges (new "
                                                << lowEdge << " previous " << fBinLowEdges.back() << ")"
                                                << std::endl;
        fBinLowEdges.push_back(lowEdge);
        fEfficiencies.push_back(bins[i].getParameter<double>("efficiency"));
        //std::cout << "lowEdge " << lowEdge << " eff " << fEfficiencies.back() << std::endl;
      }
    }
    ~TauPtBinEfficiencyCalculator() {}

    double efficiency(const pat::Tau& tau, const reco::MET& met) const {
      for(size_t i=0; i<fBinLowEdges.size(); ++i) {
        //std::cout << "Tau pt " << tau.pt() << " i " << i << " low edge " << fBinLowEdges[i] << " eff " << fEfficiencies[i] << std::endl;
        if(tau.pt() < fBinLowEdges[i]) {
          if(i == 0)
            throw cms::Exception("LogicError") << "Encountered tau with pt() " << tau.pt() << " which is less than smallest efficiency bin lower edge " << fBinLowEdges.front() << std::endl;
          return fEfficiencies[i-1];
        }
      }
      return fEfficiencies.back();
    }

  private:
    std::vector<double> fBinLowEdges;
    std::vector<double> fEfficiencies;
  };
}
namespace HPlus {
  TriggerEfficiency::WeightedEfficiencyCalculator::WeightedEfficiencyCalculator(): fTotalLumi(0) {}
  TriggerEfficiency::WeightedEfficiencyCalculator::~WeightedEfficiencyCalculator() {
    for(size_t i=0; i<fCalculators.size(); ++i) {
      delete fCalculators[i];
    }
    fCalculators.clear();
  }
  double TriggerEfficiency::WeightedEfficiencyCalculator::efficiency(const pat::Tau& tau, const reco::MET& met) const {
    if(fCalculators.empty())
      return 0;
    if(fCalculators.size() == 1)
      return fCalculators[0]->efficiency(tau, met);

    double eff=0;
    for(size_t i=0; i<fLumis.size(); ++i) {
      eff += fLumis[i] * fCalculators[i]->efficiency(tau, met);
    }
    return eff/fTotalLumi;
  }
  void TriggerEfficiency::WeightedEfficiencyCalculator::addCalculator(double lumi, EfficiencyCalculatorBase *effcalc) {
    fLumis.push_back(lumi);
    fTotalLumi += lumi;
    fCalculators.push_back(effcalc);
  }


  TriggerEfficiency::TriggerEfficiency(const edm::ParameterSet& iConfig) {
    std::vector<edm::ParameterSet> selectTriggers = iConfig.getParameter<std::vector<edm::ParameterSet> >("selectTriggers");
    edm::ParameterSet parameters = iConfig.getParameter<edm::ParameterSet>("parameters");

    for(std::vector<edm::ParameterSet>::const_iterator iTrigger = selectTriggers.begin(); iTrigger != selectTriggers.end(); ++iTrigger) {
      edm::ParameterSet param = parameters.getParameter<edm::ParameterSet>(iTrigger->getParameter<std::string>("trigger"));
      double luminosity = iTrigger->getParameter<double>("luminosity");

      if(param.exists("trueTauParameters") ){
        std::vector<double> trueTauParameters = param.getParameter<std::vector<double> >("trueTauParameters");
        std::vector<double> fakeTauParameters = param.getParameter<std::vector<double> >("fakeTauParameters");
        std::vector<double> metParameters = param.getParameter<std::vector<double> >("metParameters");

        fTrueTaus.addCalculator(luminosity, new ParametrisedEfficiencyCalculator(trueTauParameters, metParameters));
        fFakeTaus.addCalculator(luminosity, new ParametrisedEfficiencyCalculator(fakeTauParameters, metParameters));
      }
      else {
        std::vector<edm::ParameterSet> bins = param.getParameter<std::vector<edm::ParameterSet> >("tauPtBins");
        fTrueTaus.addCalculator(luminosity, new TauPtBinEfficiencyCalculator(bins));
        fFakeTaus.addCalculator(luminosity, new TauPtBinEfficiencyCalculator(bins));
      }
    }
  }
  TriggerEfficiency::~TriggerEfficiency() {}

  double TriggerEfficiency::efficiency(const pat::Tau& tau, const reco::MET& met) const {
    double eff = 0;

    if(tau.genJet())
      eff = fTrueTaus.efficiency(tau, met);
    else
      eff = fFakeTaus.efficiency(tau, met);

    //std::cout << "Is true tau? " << (tau.genJet() != 0) << " tau pt " << tau.pt() << " met " << met.et() << " efficiency " << eff << std::endl;

    return eff;
  }
}
