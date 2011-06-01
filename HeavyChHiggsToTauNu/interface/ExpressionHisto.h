// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionHisto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ExpressionHisto_h

// Took ExpressionHisto as a basis

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "TFile.h"
#include "TH1F.h"

#include<vector>
#include<limits>
#include<algorithm>

namespace HPlus {
  class ExpressionHistoVeryBase {
  protected:
    // prevent construction
    ExpressionHistoVeryBase(const edm::ParameterSet& iConfig);
    ~ExpressionHistoVeryBase();

    const std::string& getName() const { return name; }
    const std::string& getDescription() const { return description; }
    double getMin() { return min; }
    double getMax() { return max; }
    int getNbins() { return nbins; }

    TH1 *histo;

  private:
    double min, max;
    int nbins;
    std::string name, description;
  };

  template <typename T>
  class ExpressionHistoBase: public ExpressionHistoVeryBase {
  public:
    void initialize(TFileDirectory& fs);

  protected:
    // Prevent construction
    ExpressionHistoBase(const edm::ParameterSet& iConfig);
    ~ExpressionHistoBase();

    /**
     * For efficiency mode, we don't actually need the total, because
     * we can store the number of total fills to to the number of
     * entries in passed!
     */
    StringObjectFunction<T> function;
  };

  template<typename T>
  ExpressionHistoBase<T>::ExpressionHistoBase(const edm::ParameterSet& iConfig):
    ExpressionHistoVeryBase(iConfig),
    function(iConfig.template getUntrackedParameter<std::string>("plotquantity"), 
             iConfig.template getUntrackedParameter<bool>("lazyParsing", false))
  {}

  template<typename T>
  ExpressionHistoBase<T>::~ExpressionHistoBase() {
  }

  template<typename T>
  void ExpressionHistoBase<T>::initialize(TFileDirectory& fs) 
  {
    histo = makeTH<TH1F>(fs, this->getName().c_str(), this->getDescription().c_str(), this->getNbins(), this->getMin(), this->getMax());
  }

  template <typename T>
  class ExpressionHisto: public ExpressionHistoBase<T> {
    typedef ExpressionHistoBase<T> Base;
  public:
    ExpressionHisto(const edm::ParameterSet& iConfig);
    ~ExpressionHisto();

    /** Plot the quantity for the specified element and index.
        Returns true if the quantity has been plotted, false otherwise.
        A return value of "false" means "please don't send any more elements".
        The default "i = 0" is to keep backwards compatibility with usages outside
        HistoAnalyzer */
    bool fill(const T& element, double weight=1.0, uint32_t i=0);
  };

  template <typename T>
  ExpressionHisto<T>::ExpressionHisto(const edm::ParameterSet& iConfig): Base(iConfig) {}

  template <typename T>
  ExpressionHisto<T>::~ExpressionHisto(){}

  template <typename T>
  bool ExpressionHisto<T>::fill(const T& element, double weight, uint32_t i) {
    this->histo->Fill(this->function(element), weight);
    return true;
  }


}

#endif
