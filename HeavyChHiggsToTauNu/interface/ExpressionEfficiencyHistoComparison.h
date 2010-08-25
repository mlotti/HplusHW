// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionEfficiencyHistoComparison_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionEfficiencyHistoComparison_h

#include<string>

class TH1;

class ExpressionEfficiencyHistoComparison {
public:
  ExpressionEfficiencyHistoComparison();
  virtual ~ExpressionEfficiencyHistoComparison();

  virtual void fill(TH1 *histo, double value, double weight) = 0;
  virtual bool compare(double a, double b) const = 0;

  static ExpressionEfficiencyHistoComparison *create(const std::string& cmp);

  class Wrapper {
  public:
    Wrapper(const ExpressionEfficiencyHistoComparison *cmp): ptr(cmp) {}

    bool operator()(double a, double b) const {
      return ptr->compare(a, b);
    }

  private:
    const ExpressionEfficiencyHistoComparison *ptr;
  };
};

#endif
