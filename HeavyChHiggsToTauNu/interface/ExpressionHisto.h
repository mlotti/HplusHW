// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionHisto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionHisto_h

// Took ExpressionHisto as a basis

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionHistoComparison.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "TFile.h"
#include "TH1F.h"

#include<vector>
#include<limits>
#include<algorithm>

namespace HPlus {
  template <typename T>
  class ExpressionHistoBase {
  public:
    ExpressionHistoBase(const edm::ParameterSet& iConfig);
    ~ExpressionHistoBase();
  
    void initialize(TFileDirectory& fs);

  private:
    double min, max;
    int nbins;
    std::string name, description;

  protected:
    /**
     * For efficiency mode, we don't actually need the total, because
     * we can store the number of total fills to to the number of
     * entries in passed!
     */
    TH1 *histo;
    StringObjectFunction<T> function;
    std::auto_ptr<ExpressionHistoComparison> cmp;
  };

  template<typename T>
  ExpressionHistoBase<T>::ExpressionHistoBase(const edm::ParameterSet& iConfig):
    min(iConfig.template getUntrackedParameter<double>("min")),
    max(iConfig.template getUntrackedParameter<double>("max")),
    nbins(iConfig.template getUntrackedParameter<int>("nbins")),
    name(iConfig.template getUntrackedParameter<std::string>("name")),
    description(iConfig.template getUntrackedParameter<std::string>("description")),
    histo(0),
    function(iConfig.template getUntrackedParameter<std::string>("plotquantity"), 
             iConfig.template getUntrackedParameter<bool>("lazyParsing", false)),
    cmp(ExpressionHistoComparison::create(iConfig.template getUntrackedParameter<std::string>("cuttype"))) {

    if(cmp.get() == 0)
      throw cms::Exception("Configuration") << "Unsupported cut type '" << iConfig.template getUntrackedParameter<std::string>("cuttype")
                                            << "' for variable " << name << "; supported types are '<', '<=', '>', '>='";
  }

  template<typename T>
  ExpressionHistoBase<T>::~ExpressionHistoBase() {
  }

  template<typename T>
  void ExpressionHistoBase<T>::initialize(TFileDirectory& fs) 
  {
    histo = makeTH<TH1F>(fs, name.c_str(), description.c_str(), nbins, min, max);
  }

  template <typename T>
  class ExpressionValueHisto: ExpressionHistoBase<T> {
    typedef ExpressionHistoBase<T> Base;
  public:
    ExpressionValueHisto(const edm::ParameterSet& iConfig);
    ~ExpressionValueHisto();

    /** Plot the quantity for the specified element and index.
        Returns true if the quantity has been plotted, false otherwise.
        A return value of "false" means "please don't send any more elements".
        The default "i = 0" is to keep backwards compatibility with usages outside
        HistoAnalyzer */
    bool fill(const T& element, double weight=1.0, uint32_t i=0);
  };

  template <typename T>
  ExpressionValueHisto<T>::ExpressionValueHisto(const edm::ParameterSet& iConfig): Base(iConfig) {}

  template <typename T>
  ExpressionValueHisto<T>::~ExpressionValueHisto(){}

  template <typename T>
  bool ExpressionValueHisto<T>::fill(const T& element, double weight, uint32_t i) {
    this->histo->Fill(this->function(element), weight);
    return true;
  }


}

#endif
