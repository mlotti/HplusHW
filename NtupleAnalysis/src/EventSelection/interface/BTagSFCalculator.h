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
  BTagSFInputItem(float ptMin, float ptMax, const std::string formula);
  BTagSFInputItem(float ptMin, float ptMax, float eff);
  ~BTagSFInputItem();
  
  /// Returns true if the jet pt is in the range of this input item
  bool matchesPtRange(float pt) const;
  /// Returns true if the jet pt is higher than the range of this input item
  bool isGreaterThanPtRange(float pt) const { return pt > fPtMax; }
  /// Returns the input value
  float getValueByPt(float pt) const;
  /// Returns ptmax
  float getPtMax() const { return fPtMax; }
  /// Set as overflow bin
  void setAsOverflowBinPt() { bIsOverflowBinPt = true; }
  
private:
  float fPtMin;
  float fPtMax;
  bool bIsOverflowBinPt;
  TFormula fFormula;
};

class BTagSFCalculator {
public:
  enum BTagJetFlavorType {
    kBJet,
    kCJet,
    kGJet,
    kUDSJet,
    kUDSGJet,
  };

  /// Constructor
  explicit BTagSFCalculator(const ParameterSet& config);
  /// Destructor
  virtual ~BTagSFCalculator();
  /// Book histograms
  void bookHistograms(TDirectory* dir, HistoWrapper& histoWrapper);
  /// Calculate scale factor for the event
  float calculateSF(const std::vector<Jet>& selectedJets, const std::vector<Jet>& selectedBJets);
  /// Returns the size of the efficiency config items
  size_t sizeOfEfficiencyList(BTagJetFlavorType flavor) const;
  /// Returns the size of the SF config items
  size_t sizeOfSFList(BTagJetFlavorType flavor) const;
  
private:
  /// Method for handling the efficiency input
  void handleEfficiencyInput(boost::optional<std::vector<ParameterSet>> psets);
  /// Method for handling the SF input
  void handleSFInput(boost::optional<std::vector<ParameterSet>> psets);
  /// Method for converting flavor string to flavor type
  BTagJetFlavorType getFlavorTypeForEfficiency(std::string str) const;
  /// Method for converting flavor string to flavor type
  BTagJetFlavorType getFlavorTypeForSF(int i) const;
  /// Set overflow bin
  void setOverflowBin(std::vector<BTagSFInputItem>& container);
  /// Find input value
  float getInputValueByPt(std::vector<BTagSFInputItem>& container, float pt);
  
  
  /// parton->b jet efficiencies from config
  std::vector<BTagSFInputItem> fBToBEfficiency;
  std::vector<BTagSFInputItem> fCToBEfficiency;
  std::vector<BTagSFInputItem> fGToBEfficiency;
  std::vector<BTagSFInputItem> fUdsToBEfficiency;
  /// parton->b jet data/MC scalefactors from config
  std::vector<BTagSFInputItem> fBToBSF;
  std::vector<BTagSFInputItem> fCToBSF;
  std::vector<BTagSFInputItem> fGToBSF;
  std::vector<BTagSFInputItem> fUdsToBSF;
  // Validity of input
  bool isActive;
  // Histograms
  WrappedTH1* hBTagSF;
};

#endif
