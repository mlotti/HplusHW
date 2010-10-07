#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionHistoComparison.h"

#include "TH1.h"
#include "TAxis.h"

#include<iostream>

namespace {
  using HPlus::ExpressionHistoComparison;

  class Less: public ExpressionHistoComparison {
  public:
    Less();
    ~Less();
    void fillEfficiency(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class LessEqual: public ExpressionHistoComparison {
  public:
    LessEqual();
    ~LessEqual();
    void fillEfficiency(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class Greater: public ExpressionHistoComparison {
  public:
    Greater();
    ~Greater();
    void fillEfficiency(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  class GreaterEqual: public ExpressionHistoComparison {
  public:
    GreaterEqual();
    ~GreaterEqual();
    void fillEfficiency(TH1 *passed, double value, double weight);
    bool compare(double a, double b) const;
  };

  Less::Less():ExpressionHistoComparison() {}
  Less::~Less() {}
  void Less::fillEfficiency(TH1 *passed, double value, double weight) {
    //std::cout << "### Less::fill(), filling for value " << value << std::endl;
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

  LessEqual::LessEqual():ExpressionHistoComparison() {}
  LessEqual::~LessEqual() {}
  void LessEqual::fillEfficiency(TH1 *passed, double value, double weight) {
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

  Greater::Greater():ExpressionHistoComparison() {}
  Greater::~Greater() {}
  void Greater::fillEfficiency(TH1 *passed, double value, double weight) {
    //std::cout << "### Greater::fill(), filling for value " << value << std::endl;
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

  GreaterEqual::GreaterEqual():ExpressionHistoComparison() {}
  GreaterEqual::~GreaterEqual() {}
  void GreaterEqual::fillEfficiency(TH1 *passed, double value, double weight) {
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

namespace HPlus {
  ExpressionHistoComparison::ExpressionHistoComparison() {}
  ExpressionHistoComparison::~ExpressionHistoComparison() {}

  ExpressionHistoComparison *ExpressionHistoComparison::create(const std::string& cmp) {
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
}
