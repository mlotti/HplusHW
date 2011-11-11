// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerEfficiencyScaleFactor_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerEfficiencyScaleFactor_h

#include<vector>

namespace edm {
  class ParameterSet;
}
namespace pat {
  class Tau;
}

class TH1;

namespace HPlus {
  class EventWeight;

  class TriggerEfficiencyScaleFactor {
    enum Mode {
      kDataEfficiency,
      kScaleFactor,
      kDisabled
    };

  public:
    class Data {
    public:
      Data(const TriggerEfficiencyScaleFactor *tesf);
      ~Data();

      double getEventWeight() const {
        return fTesf->fWeight;
      }

      double getEventWeightAbsoluteUncertainty() const {
        return fTesf->fWeightAbsUnc;
      }

    private:
      const TriggerEfficiencyScaleFactor *fTesf;
    };

    TriggerEfficiencyScaleFactor(const edm::ParameterSet& iConfig, EventWeight& eventWeight);
    ~TriggerEfficiencyScaleFactor();

    double dataEfficiency(const pat::Tau& tau) const;
    double dataEfficiencyRelativeUncertainty(const pat::Tau& tau) const;
    double dataEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const;

    double scaleFactor(const pat::Tau& tau) const;
    double scaleFactorRelativeUncertainty(const pat::Tau& tau) const;
    double scaleFactorAbsoluteUncertainty(const pat::Tau& tau) const;

    Data applyEventWeight(const pat::Tau& tau);

  private:
    size_t index(const pat::Tau& tau) const;
    size_t index(double pt) const;

    double dataEfficiency(size_t i) const;
    double dataEfficiencyAbsoluteUncertainty(size_t i) const;

    double scaleFactor(size_t i) const;
    double scaleFactorRelativeUncertainty(size_t i) const;
    double scaleFactorAbsoluteUncertainty(size_t i) const;

    std::vector<double> fPtBinLowEdges;
    std::vector<double> fEffDataValues;
    std::vector<double> fEffDataUncertainties;
    std::vector<double> fEffMCValues;
    std::vector<double> fEffMCUncertainties;

    EventWeight& fEventWeight;

    TH1 *hScaleFactor;
    TH1 *hScaleFactorRelativeUncertainty;
    TH1 *hScaleFactorAbsoluteUncertainty;

    Mode fMode;
    double fWeight;
    double fWeightAbsUnc;
  };
}


#endif
