#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HPlusExpressionEfficiencyHistoComparison.h"

#include "TH1.h"
#include "TAxis.h"

namespace {
  class Less: public HPlusExpressionEfficiencyHistoComparison {
  public:
    Less();
    ~Less();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class LessEqual: public HPlusExpressionEfficiencyHistoComparison {
  public:
    LessEqual();
    ~LessEqual();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class Greater: public HPlusExpressionEfficiencyHistoComparison {
  public:
    Greater();
    ~Greater();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class GreaterEqual: public HPlusExpressionEfficiencyHistoComparison {
  public:
    GreaterEqual();
    ~GreaterEqual();
    void fill(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  Less::Less():HPlusExpressionEfficiencyHistoComparison() {}
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

  LessEqual::LessEqual():HPlusExpressionEfficiencyHistoComparison() {}
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

  Greater::Greater():HPlusExpressionEfficiencyHistoComparison() {}
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

  GreaterEqual::GreaterEqual():HPlusExpressionEfficiencyHistoComparison() {}
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

HPlusExpressionEfficiencyHistoComparison::HPlusExpressionEfficiencyHistoComparison() {}
HPlusExpressionEfficiencyHistoComparison::~HPlusExpressionEfficiencyHistoComparison() {}

HPlusExpressionEfficiencyHistoComparison *HPlusExpressionEfficiencyHistoComparison::create(const std::string& cmp) {
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
