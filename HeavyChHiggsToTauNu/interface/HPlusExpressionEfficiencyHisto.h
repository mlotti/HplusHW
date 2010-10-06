// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_HPlusExpressionEfficiencyHisto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_HPlusExpressionEfficiencyHisto_h

// Took ExpressionHisto as a basis

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionHistoComparison.h"

#include "TFile.h"
#include "TH1F.h"

#include<vector>
#include<limits>
#include<algorithm>

template<typename T>
class HPlusExpressionEfficiencyHisto {
 public:
  HPlusExpressionEfficiencyHisto(const edm::ParameterSet& iConfig);
  ~HPlusExpressionEfficiencyHisto();
  
  void initialize(TFileDirectory& fs);
  
private:
  double min, max;
  int nbins;
  std::string name, description;

protected:
  /**
   * We don't actually need the total, because we can store the number
   * of total fills to to the number of entries in passed!
   */
  //TH1 *total;
  TH1 *passed;
  StringObjectFunction<T> function;
  //FillFunction fillFunction;
  std::auto_ptr<HPlus::ExpressionHistoComparison> cmp;
};

template<typename T>
HPlusExpressionEfficiencyHisto<T>::HPlusExpressionEfficiencyHisto(const edm::ParameterSet& iConfig):
  min(iConfig.template getUntrackedParameter<double>("min")),
  max(iConfig.template getUntrackedParameter<double>("max")),
  nbins(iConfig.template getUntrackedParameter<int>("nbins")),
  name(iConfig.template getUntrackedParameter<std::string>("name")),
  description(iConfig.template getUntrackedParameter<std::string>("description")),
  passed(0),
  function(iConfig.template getUntrackedParameter<std::string>("plotquantity"), 
           iConfig.template getUntrackedParameter<bool>("lazyParsing", false)),
  cmp(HPlus::ExpressionHistoComparison::create(iConfig.template getUntrackedParameter<std::string>("cuttype"))) {

  if(cmp.get() == 0)
    throw cms::Exception("Configuration") << "Unsupported cut type '" << iConfig.template getUntrackedParameter<std::string>("cuttype")
                                          << "' for variable " << name << "; supported types are '<', '<=', '>', '>='";
}

template<typename T>
HPlusExpressionEfficiencyHisto<T>::~HPlusExpressionEfficiencyHisto() {
}

template<typename T>
void HPlusExpressionEfficiencyHisto<T>::initialize(TFileDirectory& fs) 
{
  passed = fs.make<TH1F>((name+"_passed").c_str(),description.c_str(),nbins,min,max);
}



template <typename T>
class HPlusExpressionEfficiencyHistoPerObject: public HPlusExpressionEfficiencyHisto<T> {
  typedef HPlusExpressionEfficiencyHisto<T> Base;
public:
  HPlusExpressionEfficiencyHistoPerObject(const edm::ParameterSet& iConfig);
  ~HPlusExpressionEfficiencyHistoPerObject();

  /** Plot the quantity for the specified element and index.
    Returns true if the quantity has been plotted, false otherwise.
    A return value of "false" means "please don't send any more elements".
    The default "i = 0" is to keep backwards compatibility with usages outside
    HistoAnalyzer */
  bool fill(const T& element, double weight=1.0, uint32_t i=0);
};
template <typename T>
HPlusExpressionEfficiencyHistoPerObject<T>::HPlusExpressionEfficiencyHistoPerObject(const edm::ParameterSet& iConfig): Base(iConfig) {}
template <typename T>
HPlusExpressionEfficiencyHistoPerObject<T>::~HPlusExpressionEfficiencyHistoPerObject() {}
template <typename T>
bool HPlusExpressionEfficiencyHistoPerObject<T>::fill(const T& element, double weight, uint32_t i) {
  double entries = this->passed->GetEntries();
  this->cmp->fillEfficiency(this->passed, this->function(element), weight);
  this->passed->SetEntries(entries+1);
  return true;
}



template <typename T>
class HPlusExpressionEfficiencyHistoPerEvent: public HPlusExpressionEfficiencyHisto<T> {
  typedef HPlusExpressionEfficiencyHisto<T> Base;
public:
  HPlusExpressionEfficiencyHistoPerEvent(const edm::ParameterSet& iConfig);
  ~HPlusExpressionEfficiencyHistoPerEvent();

  /** Plot the quantity for the specified element and index.
    Returns true if the quantity has been plotted, false otherwise.
    A return value of "false" means "please don't send any more elements".
    The default "i = 0" is to keep backwards compatibility with usages outside
    HistoAnalyzer */
  bool fill(const T& element, double weight=1.0, uint32_t i=0);

  void endEvent();

protected:
  const uint32_t minObjects_;
private:
  std::vector<double> values_;
  double weight_;
};
template <typename T>
HPlusExpressionEfficiencyHistoPerEvent<T>::HPlusExpressionEfficiencyHistoPerEvent(const edm::ParameterSet& iConfig):
  Base(iConfig),
  minObjects_(iConfig.template getUntrackedParameter<uint32_t>("minObjects", 1)) {
  values_.reserve(minObjects_);
  if(minObjects_ < 1)
    throw cms::Exception("Configuration") << "minObjects must be at least 1! (was " << minObjects_ << ")";
}
template <typename T>
HPlusExpressionEfficiencyHistoPerEvent<T>::~HPlusExpressionEfficiencyHistoPerEvent() {}
template <typename T>
bool HPlusExpressionEfficiencyHistoPerEvent<T>::fill(const T& element, double weight, uint32_t i) {
  weight_ = weight;

  double value = this->function(element);
  std::vector<double>::iterator pos = std::lower_bound(values_.begin(), values_.end(), value, HPlus::ExpressionHistoComparison::Wrapper(this->cmp.get()));
  if(values_.size() >= minObjects_) {
    if(pos != values_.begin()) {
      std::copy(values_.begin()+1, pos, values_.begin());
      values_[pos - values_.begin() - 1] = value;
    }
  }
  else {
    values_.insert(pos, value);
  }

  return true;
}
template <typename T>
void HPlusExpressionEfficiencyHistoPerEvent<T>::endEvent() {
  double entries = this->passed->GetEntries();

  if(values_.size() >= minObjects_) {
    this->cmp->fillEfficiency(this->passed, values_.front(), weight_);
  }
  this->passed->SetEntries(entries+1);

  values_.clear();
  weight_ = 0;
}

template <template <class> class H> struct MultiHistoAnalyzerTraits;

template <>
struct MultiHistoAnalyzerTraits<HPlusExpressionEfficiencyHistoPerEvent> {
  template <typename T>
  static void endEvent(HPlusExpressionEfficiencyHistoPerEvent<T> *histo) {
    histo->endEvent();
  }
};



#endif
