// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionHistoComparison_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionHistoComparison_h

#include<string>

class TH1;

namespace HPlus {
  class ExpressionHistoComparison {
  public:
    ExpressionHistoComparison();
    virtual ~ExpressionHistoComparison();

    virtual void fillEfficiency(TH1 *histo, double value, double weight) = 0;
    virtual bool compare(double a, double b) const = 0;

    static ExpressionHistoComparison *create(const std::string& cmp);

    class Wrapper {
    public:
      Wrapper(const ExpressionHistoComparison *cmp): ptr(cmp) {}

      bool operator()(double a, double b) const {
        // The comparison needs to be inverted in order to have the
        // vector of values sorted in the corred direction
        return !ptr->compare(a, b);
      }

    private:
      const ExpressionHistoComparison *ptr;
    };
  };
}

#endif
