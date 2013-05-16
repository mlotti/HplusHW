// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BinnedEfficiencyScaleFactor_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BinnedEfficiencyScaleFactor_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EfficiencyScaleFactorBase.h"
#include<cstddef>

#include<vector>
#include<string>

namespace HPlus {
  class BinnedEfficiencyScaleFactor: public EfficiencyScaleFactorBase {
  public:
    class Data: public EfficiencyScaleFactorBase::Data {
    public:
      Data();
      ~Data();

      friend class BinnedEfficiencyScaleFactor;
    };

    explicit BinnedEfficiencyScaleFactor(const edm::ParameterSet& iConfig, const std::string& quantity);
    ~BinnedEfficiencyScaleFactor();

    void setRun(unsigned run);

    double dataEfficiency(double value) const;
    double dataEfficiencyRelativeUncertainty(double value) const;
    double dataEfficiencyAbsoluteUncertainty(double value) const;

    double dataAverageEfficiency(double value) const;
    double dataAverageEfficiencyRelativeUncertainty(double value) const;
    double dataAverageEfficiencyAbsoluteUncertainty(double value) const;

    double mcEfficiency(double value) const;
    double mcEfficiencyRelativeUncertainty(double value) const;
    double mcEfficiencyAbsoluteUncertainty(double value) const;

    double scaleFactor(double value) const;
    double scaleFactorRelativeUncertainty(double value) const;
    double scaleFactorAbsoluteUncertainty(double value) const;

    size_t nbins() const { return fBinLowEdges.size(); }
    double binLowEdge(size_t bin) const { return fBinLowEdges[bin]; }
    double binScaleFactor(size_t bin) const { return fData.fScaleValues[bin]; }
    double binScaleFactorAbsoluteUncertainty(size_t bin) const { return fData.fScaleUncertainties[bin]; }

    Data getEventWeight(double value, bool isData) const;

  private:
    typedef EfficiencyScaleFactorData<std::vector<double> > EffData;

    EffData fData;

    size_t index(double value) const;

    std::vector<double> fBinLowEdges;
  };
}

#endif
