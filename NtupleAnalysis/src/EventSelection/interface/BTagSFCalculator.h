// -*- c++ -*-
#ifndef EventSelection_BTagSFCalculator_h
#define EventSelection_BTagSFCalculator_h

#include "EventSelection/interface/BaseSelection.h"
#include "EventSelection/interface/JetSelection.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"

#include <string>
#include <vector>
#include "TFormula.h"
#include "boost/optional.hpp"

class ParameterSet;
class HistoWrapper;
class WrappedTH1;

class BTagSFInputItem {
public:
  BTagSFInputItem(float ptMin, float ptMax, const std::string& formula);
  BTagSFInputItem(float ptMin, float ptMax, float eff);
  ~BTagSFInputItem();
  
  /// Returns true if the jet pt is in the range of this input item
  const bool matchesPtRange(float pt) const;
  /// Returns true if the jet pt is higher than the range of this input item
  const bool isGreaterThanPtRange(float pt) const { return pt > fPtMax; }
  /// Returns the input value
  const float getValueByPt(float pt) const;
  /// Returns ptmax
  const float getPtMax() const { return fPtMax; }
  /// Set as overflow bin
  void setAsOverflowBinPt();
  /// Debug
  void debug() const;
  
private:
  float fPtMin;
  float fPtMax;
  bool bIsOverflowBinPt;
  TFormula fFormula;
};

/// Mediator class between individual BTagSFInputItem and BTagSFCalculator
class BTagSFInputStash {
public:
  enum BTagJetFlavorType { 
    // README: https://hypernews.cern.ch/HyperNews/CMS/get/btag/1482/1/1/1/1/1.html
    kBJet,
    kCJet,
    // kGJet,   // obsolete (see README)
    // kUDSJet, // obsolete (see README)
    kUDSGJet,
  };
  BTagSFInputStash();
  ~BTagSFInputStash();
  
  /// Add input 
  void addInput(BTagJetFlavorType flavor, float ptMin, float ptMax, const std::string& formula);
  void addInput(BTagJetFlavorType flavor, float ptMin, float ptMax, float eff);
  /// Returns the size of the collection
  const size_t sizeOfList(BTagJetFlavorType flavor) const { return getConstCollection(flavor).size(); }
  /// Returns value by pt
  const float getInputValueByPt(BTagJetFlavorType flavor, float pt) const;
  /// Set maximum bins as overflow bins
  void setOverflowBinByPt(const std::string& label);
  /// Debug
  void debug() const;
  
private:
  const std::vector<BTagSFInputItem*>& getConstCollection(BTagJetFlavorType flavor) const;
  std::vector<BTagSFInputItem*>& getCollection(BTagJetFlavorType flavor);
  
  std::vector<BTagSFInputItem*> fBToB;
  std::vector<BTagSFInputItem*> fCToB;
  // std::vector<BTagSFInputItem*> fGToB;
  std::vector<BTagSFInputItem*> fUdsgToB;
};

class BTagSFCalculator {
public:
  enum BTagSFVariationType {
    kNominal,
    kVariationTagUp,
    kVariationMistagUp,
    kVariationTagDown,
    kVariationMistagDown,
  };

  /// Constructor
  explicit BTagSFCalculator(const ParameterSet& config);
  /// Destructor
  virtual ~BTagSFCalculator();
  /// Book histograms
  void bookHistograms(TDirectory* dir, HistoWrapper& histoWrapper);
  /// Calculate scale factor for the event
  const float calculateSF(const std::vector<Jet>& selectedJets, const std::vector<Jet>& selectedBJets);
  /// Returns the size of the efficiency config items
  const size_t sizeOfEfficiencyList(BTagSFInputStash::BTagJetFlavorType flavor, const std::string& direction) const;
  /// Returns the size of the SF config items
  const size_t sizeOfSFList(BTagSFInputStash::BTagJetFlavorType flavor, const std::string& direction) const;
  
private:
  /// Method for handling the efficiency input
  void handleEfficiencyInput(boost::optional<std::vector<ParameterSet>> psets);
  /// Method for handling the SF input
  void handleSFInput(boost::optional<std::vector<ParameterSet>> psets);
  /// Method for converting flavor string to flavor type
  BTagSFInputStash::BTagJetFlavorType getFlavorTypeForEfficiency(const std::string& str) const;
  /// Method for converting flavor string to flavor type
  BTagSFInputStash::BTagJetFlavorType getFlavorTypeForSF(int i) const;
  /// Find input value
  float getInputValueByPt(std::vector<BTagSFInputItem>& container, float pt);

  /// Disentangle variation info type from config
  const BTagSFVariationType parseVariationType(const ParameterSet& config) const;
  
  /// Systematic variation type
  const BTagSFVariationType fVariationInfo;
  /// parton->b jet efficiencies from config
  BTagSFInputStash fEfficiencies;
  BTagSFInputStash fEfficienciesUp;
  BTagSFInputStash fEfficienciesDown;
  /// parton->b jet data/MC scalefactors from config
  BTagSFInputStash fSF;
  BTagSFInputStash fSFUp;
  BTagSFInputStash fSFDown;
  /// Validity of input
  bool isActive;
  // Histograms
  WrappedTH1* hBTagSF;
  WrappedTH1* hBTagSFRelUncert;
};

#endif
