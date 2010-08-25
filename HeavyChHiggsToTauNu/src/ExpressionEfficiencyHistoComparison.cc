#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionEfficiencyHistoComparison.h"

#include "TH1.h"
#include "TAxis.h"

namespace {
  class Less: public ExpressionEfficiencyHistoComparison {
  public:
    Less();
    ~Less();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class LessEqual: public ExpressionEfficiencyHistoComparison {
  public:
    LessEqual();
    ~LessEqual();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class Greater: public ExpressionEfficiencyHistoComparison {
  public:
    Greater();
    ~Greater();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class GreaterEqual: public ExpressionEfficiencyHistoComparison {
  public:
    GreaterEqual();
    ~GreaterEqual();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  Less::Less():ExpressionEfficiencyHistoComparison() {}
  Less::~Less() {}
  void Less::fill(TH1 *passed, double value, double weight) {
    for(int bin=passed->GetNbinsX(); bin >= 1; --bin) {
      if(value < passed->GetXaxis()->GetBinCenter(bin))
        passed->AddBinContent(bin, weight);
      else
        break;
    }
  }
  bool Less::compare(double a, double b) const {
    return a < b;
  }

  LessEqual::LessEqual():ExpressionEfficiencyHistoComparison() {}
  LessEqual::~LessEqual() {}
  void LessEqual::fill(TH1 *passed, double value, double weight) {
    for(int bin=passed->GetNbinsX(); bin >= 1; --bin) {
      if(value <= passed->GetXaxis()->GetBinCenter(bin))
        passed->AddBinContent(bin, weight);
      else
        break;
    }
  }
  bool LessEqual::compare(double a, double b) const {
    return a <= b;
  }

  Greater::Greater():ExpressionEfficiencyHistoComparison() {}
  Greater::~Greater() {}
  void Greater::fill(TH1 *passed, double value, double weight) {
    for(int bin=1; bin <= passed->GetNbinsX(); ++bin) {
      if(value > passed->GetXaxis()->GetBinCenter(bin))
        passed->AddBinContent(bin, weight);
      else
        break;
    }
  }
  bool Greater::compare(double a, double b) const {
    return a > b;
  }

  GreaterEqual::GreaterEqual():ExpressionEfficiencyHistoComparison() {}
  GreaterEqual::~GreaterEqual() {}
  void GreaterEqual::fill(TH1 *passed, double value, double weight) {
    for(int bin=1; bin <= passed->GetNbinsX(); ++bin) {
      if(value >= passed->GetXaxis()->GetBinCenter(bin))
        passed->AddBinContent(bin, weight);
      else
        break;
    }
  }
  bool GreaterEqual::compare(double a, double b) const {
    return a >= b;
  }

}

ExpressionEfficiencyHistoComparison::ExpressionEfficiencyHistoComparison() {}
ExpressionEfficiencyHistoComparison::~ExpressionEfficiencyHistoComparison() {}

ExpressionEfficiencyHistoComparison *ExpressionEfficiencyHistoComparison::create(const std::string& cmp) {
  if(cmp == "<" || cmp == "lessThan")
    return new Less();
  else if(cmp == "<=" || cmp == "lessEqual")
    return new LessEqual();
  else if(cmp == ">" || cmp == "greaterThan")
    return new Greater();
  else if(cmp == ">=" || cmp == "greaterEqual")
    return new GreaterEqual();
  else
    return 0;
}
