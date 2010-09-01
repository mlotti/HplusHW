// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_HPlusExpressionEfficiencyHistoComparison_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_HPlusExpressionEfficiencyHistoComparison_h

#include<string>

class TH1;

class HPlusExpressionEfficiencyHistoComparison {
public:
  HPlusExpressionEfficiencyHistoComparison();
  virtual ~HPlusExpressionEfficiencyHistoComparison();

  virtual void fill(TH1 *histo, double value, double weight) = 0;
  virtual bool compare(double a, double b) const = 0;

  static HPlusExpressionEfficiencyHistoComparison *create(const std::string& cmp);

  class Wrapper {
  public:
    Wrapper(const HPlusExpressionEfficiencyHistoComparison *cmp): ptr(cmp) {}

    bool operator()(double a, double b) const {
      // The comparison needs to be inverted in order to have the
      // vector of values sorted in the corred direction
      return !ptr->compare(a, b);
    }

  private:
    const HPlusExpressionEfficiencyHistoComparison *ptr;
  };
};

#endif
