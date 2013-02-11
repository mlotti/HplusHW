// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerEfficiencyScaleFactor_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerEfficiencyScaleFactor_h

#include <vector>
#include <cstring>

namespace edm {
  class ParameterSet;
}
namespace pat {
  class Tau;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class EventWeight;

  class TriggerEfficiencyScaleFactor {
    enum Mode {
      kEfficiency,
      kScaleFactor,
      kDisabled
    };

  public:
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

      friend class TriggerEfficiencyScaleFactor;

    private:
      double fWeight;
      double fWeightAbsUnc;
      double fWeightRelUnc;

    };

    TriggerEfficiencyScaleFactor(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper);
    ~TriggerEfficiencyScaleFactor();

    void setRun(unsigned run);

    double dataEfficiency(const pat::Tau& tau) const;
    double dataEfficiencyRelativeUncertainty(const pat::Tau& tau) const;
    double dataEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const;

    double dataAverageEfficiency(const pat::Tau& tau) const;
    double dataAverageEfficiencyRelativeUncertainty(const pat::Tau& tau) const;
    double dataAverageEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const;

    double mcEfficiency(const pat::Tau& tau) const;
    double mcEfficiencyRelativeUncertainty(const pat::Tau& tau) const;
    double mcEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const;

    double scaleFactor(const pat::Tau& tau) const;
    double scaleFactorRelativeUncertainty(const pat::Tau& tau) const;
    double scaleFactorAbsoluteUncertainty(const pat::Tau& tau) const;

    Data applyEventWeight(const pat::Tau& tau, bool isData, HPlus::EventWeight& eventWeight);

  private:
    struct DataValue {
      unsigned firstRun;
      unsigned lastRun;
      double luminosity;
      std::vector<double> values;
      std::vector<double> uncertainties;
    };

    size_t index(const pat::Tau& tau) const;
    size_t index(double pt) const;

    double dataEfficiency(size_t i) const;
    double dataEfficiencyAbsoluteUncertainty(size_t i) const;

    double dataAverageEfficiency(size_t i) const;
    double dataAverageEfficiencyAbsoluteUncertainty(size_t i) const;

    double mcEfficiency(size_t i) const;
    double mcEfficiencyAbsoluteUncertainty(size_t i) const;

    double scaleFactor(size_t i) const;
    double scaleFactorAbsoluteUncertainty(size_t i) const;

    std::vector<double> fPtBinLowEdges;
    std::vector<DataValue> fDataValues;

    std::vector<double> fEffDataAverageValues;
    std::vector<double> fEffDataAverageUncertainties;
    std::vector<double> fEffMCValues;
    std::vector<double> fEffMCUncertainties;

    std::vector<double> fScaleValues;
    std::vector<double> fScaleUncertainties;

    const DataValue *fCurrentRunData;

    WrappedTH1 *hScaleFactor;
    WrappedTH1 *hScaleFactorRelativeUncertainty;
    WrappedTH1 *hScaleFactorAbsoluteUncertainty;

    Mode fMode;
  };
}


#endif
