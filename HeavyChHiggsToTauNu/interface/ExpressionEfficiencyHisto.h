// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionEfficiencyHisto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionEfficiencyHisto_h

// Took ExpressionHisto as a basis

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionEfficiencyHistoComparison.h"

#include "TFile.h"
#include "TH1F.h"

#include<vector>
#include<limits>
#include<algorithm>

template<typename T>
class ExpressionEfficiencyHisto {
 public:
  ExpressionEfficiencyHisto(const edm::ParameterSet& iConfig);
  ~ExpressionEfficiencyHisto();
  
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
  std::auto_ptr<ExpressionEfficiencyHistoComparison> cmp;
};

template<typename T>
ExpressionEfficiencyHisto<T>::ExpressionEfficiencyHisto(const edm::ParameterSet& iConfig):
  min(iConfig.template getUntrackedParameter<double>("min")),
  max(iConfig.template getUntrackedParameter<double>("max")),
  nbins(iConfig.template getUntrackedParameter<int>("nbins")),
  name(iConfig.template getUntrackedParameter<std::string>("name")),
  description(iConfig.template getUntrackedParameter<std::string>("description")),
  passed(0),
  function(iConfig.template getUntrackedParameter<std::string>("plotquantity"), 
           iConfig.template getUntrackedParameter<bool>("lazyParsing", false)),
  cmp(ExpressionEfficiencyHistoComparison::create(iConfig.template getUntrackedParameter<std::string>("cuttype"))) {

  if(cmp.get() == 0)
    throw cms::Exception("Configuration") << "Unsupported cut type '" << iConfig.template getUntrackedParameter<std::string>("cuttype")
                                          << "' for variable " << name << "; supported types are '<', '<=', '>', '>='";
}

template<typename T>
ExpressionEfficiencyHisto<T>::~ExpressionEfficiencyHisto() {
}

template<typename T>
void ExpressionEfficiencyHisto<T>::initialize(TFileDirectory& fs) 
{
  passed = fs.make<TH1F>((name+"_passed").c_str(),description.c_str(),nbins,min,max);
}



template <typename T>
class ExpressionEfficiencyHistoPerObject: public ExpressionEfficiencyHisto<T> {
  typedef ExpressionEfficiencyHisto<T> Base;
public:
  ExpressionEfficiencyHistoPerObject(const edm::ParameterSet& iConfig);
  ~ExpressionEfficiencyHistoPerObject();

  /** Plot the quantity for the specified element and index.
    Returns true if the quantity has been plotted, false otherwise.
    A return value of "false" means "please don't send any more elements".
    The default "i = 0" is to keep backwards compatibility with usages outside
    HistoAnalyzer */
  bool fill(const T& element, double weight=1.0, uint32_t i=0);
};
template <typename T>
ExpressionEfficiencyHistoPerObject<T>::ExpressionEfficiencyHistoPerObject(const edm::ParameterSet& iConfig): Base(iConfig) {}
template <typename T>
ExpressionEfficiencyHistoPerObject<T>::~ExpressionEfficiencyHistoPerObject() {}
template <typename T>
bool ExpressionEfficiencyHistoPerObject<T>::fill(const T& element, double weight, uint32_t i) {
  double entries = this->passed->GetEntries();
  this->cmp->fill(this->passed, this->function(element), weight);
  this->passed->SetEntries(entries+1);
  return true;
}



template <typename T>
class ExpressionEfficiencyHistoPerEvent: public ExpressionEfficiencyHisto<T> {
  typedef ExpressionEfficiencyHisto<T> Base;
public:
  ExpressionEfficiencyHistoPerEvent(const edm::ParameterSet& iConfig);
  ~ExpressionEfficiencyHistoPerEvent();

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
ExpressionEfficiencyHistoPerEvent<T>::ExpressionEfficiencyHistoPerEvent(const edm::ParameterSet& iConfig):
  Base(iConfig),
  minObjects_(iConfig.template getUntrackedParameter<uint32_t>("minObjects", 1)) {
  values_.reserve(minObjects_);
  if(minObjects_ < 1)
    throw cms::Exception("Configuration") << "minObjects must be at least 1! (was " << minObjects_ << ")";
}
template <typename T>
ExpressionEfficiencyHistoPerEvent<T>::~ExpressionEfficiencyHistoPerEvent() {}
template <typename T>
bool ExpressionEfficiencyHistoPerEvent<T>::fill(const T& element, double weight, uint32_t i) {
  weight_ = weight;

  double value = this->function(element);
  std::vector<double>::iterator pos = std::lower_bound(values_.begin(), values_.end(), value, ExpressionEfficiencyHistoComparison::Wrapper(this->cmp.get()));
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
void ExpressionEfficiencyHistoPerEvent<T>::endEvent() {
  double entries = this->passed->GetEntries();

  if(values_.size() >= minObjects_) {
    this->cmp->fill(this->passed, values_.front(), weight_);
  }
  this->passed->SetEntries(entries+1);

  values_.clear();
  weight_ = 0;
}

template <template <class> class H> struct MultiHistoAnalyzerTraits;

template <>
struct MultiHistoAnalyzerTraits<ExpressionEfficiencyHistoPerEvent> {
  template <typename T>
  static void endEvent(ExpressionEfficiencyHistoPerEvent<T> *histo) {
    histo->endEvent();
  }
};



#endif
