// -*- c++ -*-
#include "EventSelection/interface/BTagSFCalculator.h"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"

#include "TMath.h"

// --- BTagSFInputitem ---


// Constructor using formula string
BTagSFInputItem::BTagSFInputItem(float ptMin, float ptMax, const std::string& formula)
: fPtMin(ptMin),
  fPtMax(ptMax),
  bIsOverflowBinPt(false) {
  int v = fFormula.Compile(formula.c_str());
  if (v) {
    throw hplus::Exception("config") << "BTag SF formula '" << formula << "' does not compile for TFormula!";
  }
}

// Constructor using efficiency number
BTagSFInputItem::BTagSFInputItem(float ptMin, float ptMax, float eff)
: fPtMin(ptMin),
  fPtMax(ptMax),
  bIsOverflowBinPt(false) {
  std::stringstream s;
  s << eff;
  int v = fFormula.Compile(s.str().c_str());
  if (v) {
    throw hplus::Exception("config") << "BTag SF formula '" << eff << "' does not compile for TFormula!";
  }
}

// Destructor
BTagSFInputItem::~BTagSFInputItem() { }

const bool BTagSFInputItem::matchesPtRange(float pt) const { 
  if (pt > fPtMin) {
    if (bIsOverflowBinPt || pt <= fPtMax) {
      return true;
    }
  }
  return false;
}

// Evaluate SF for given pT
const float BTagSFInputItem::getValueByPt(float pt) const {
  if (!matchesPtRange(pt)) {
    throw hplus::Exception("assert") << "The requested pt (" << pt << ") is out of range!";
  }
  // For jet pt's above the maximum pt value, use the maximum value (otherwise the SF's become anomalously large)
  if (pt > fPtMax) {
    return fFormula.Eval(fPtMax);
  }
  return fFormula.Eval(pt);
}

void BTagSFInputItem::setAsOverflowBinPt() { bIsOverflowBinPt = true; }

// Print debug information
void BTagSFInputItem::debug() const {
  std::cout << "ptmin=" << fPtMin << " ptmax=" << fPtMax 
            << " overflow=" << bIsOverflowBinPt 
            << " formula=" << fFormula.GetExpFormula() << std::endl;
}


// --- BTagSFInputStash ---


// Constructor
BTagSFInputStash::BTagSFInputStash() { }

// Destructor
BTagSFInputStash::~BTagSFInputStash() {
  std::vector<std::vector<BTagSFInputItem*>> collections = { fBToB, fCToB, fGToB, fUdsToB };
  for (auto& container: collections) {
    for (size_t i = 0; i < container.size(); ++i) {
      delete container[i];
    }
    container.clear();
  }
}

// Create new input item corresponding to certain flavor and pT range (using formula string)
void BTagSFInputStash::addInput(BTagJetFlavorType flavor, float ptMin, float ptMax, const std::string& formula) {
  getCollection(flavor).push_back(new BTagSFInputItem(ptMin, ptMax, formula));
}

// Create new input item corresponding to certain flavor and pT range (using eff)
void BTagSFInputStash::addInput(BTagJetFlavorType flavor, float ptMin, float ptMax, float eff) {
  getCollection(flavor).push_back(new BTagSFInputItem(ptMin, ptMax, eff));
}

// Per-jet SF (by pT)
const float BTagSFInputStash::getInputValueByPt(BTagJetFlavorType flavor, float pt) const {
  for (auto &p: getConstCollection(flavor)) {
    if (p->matchesPtRange(pt)) {
      return p->getValueByPt(pt);
    }
  }
  //std::cout << "***" << getConstCollection(flavor).size() << std::endl;
  throw hplus::Exception("Logic") << "Jet pt " << pt << " flavor " << flavor << " is out of range for btag SF calculation!";
  return 1.0;
}

// Define overflow bin
void BTagSFInputStash::setOverflowBinByPt(const std::string& label) {
  std::vector<std::vector<BTagSFInputItem*>> collections = { fBToB, fCToB, fGToB, fUdsToB };
  size_t i = 0;
  for (auto& container: collections) {
    if (!container.size()) {
      std::cout << "Warning: Btag SF: empty collection for " << label << " flavor=" << i << std::endl;
      continue;
    }
    float maxValue = -1.0;
    int index = -1;
    int i = 0;
    for (auto p: container) {
      if (p->getPtMax() > maxValue) {
        maxValue = p->getPtMax();
        index = i;
      }
      ++i;
    }
    if (index >= 0) {
      container[index]->setAsOverflowBinPt();
    }
    //std::cout << "overflow " << label << " index " << index << std::endl;
    //container[index]->debug();
    ++i;
  }
}

// Get const vector of input items (according to flavor)
const std::vector<BTagSFInputItem*>& BTagSFInputStash::getConstCollection(BTagJetFlavorType flavor) const {
  if (flavor == kBJet)
    return fBToB;
  else if (flavor == kCJet)
    return fCToB;
  else if (flavor == kGJet)
    return fGToB;
  else if (flavor == kUDSJet)
    return fUdsToB;
  throw hplus::Exception("Logic") << "Unknown flavor requested! " << flavor;
}

// Get vector of input items (according to flavor)
std::vector<BTagSFInputItem*>& BTagSFInputStash::getCollection(BTagJetFlavorType flavor) {
  if (flavor == kBJet)
    return fBToB;
  else if (flavor == kCJet)
    return fCToB;
  else if (flavor == kGJet)
    return fGToB;
  else if (flavor == kUDSJet)
    return fUdsToB;
  throw hplus::Exception("Logic") << "Unknown flavor requested! " << flavor;
}

// Debug prints
void BTagSFInputStash::debug() const {
  std::vector<std::vector<BTagSFInputItem*>> collections = { fBToB, fCToB, fGToB, fUdsToB };
  for (auto p: collections) {
    for (auto pp: p) {
      pp->debug();
    }
  }
}


// --- BTagSFCalculator ---

// Constructor
BTagSFCalculator::BTagSFCalculator(const ParameterSet& config)
: fVariationInfo(parseVariationType(config)),
  isActive(true),
  hBTagSF(nullptr),
  hBTagSFRelUncert(nullptr) {
  // Import efficiencies
  handleEfficiencyInput(config.getParameterOptional<std::vector<ParameterSet>>("btagEfficiency"));
  fEfficiencies.setOverflowBinByPt("EfficiencyNominal");
  fEfficienciesUp.setOverflowBinByPt("EfficiencyUp");
  fEfficienciesDown.setOverflowBinByPt("EfficiencyDown");
  // Import scale factors
  handleSFInput(config.getParameterOptional<std::vector<ParameterSet>>("btagSF"));
  fSF.setOverflowBinByPt("SFnominal");
  fSFUp.setOverflowBinByPt("SFup");
  fSFDown.setOverflowBinByPt("SFdown");
  // Debug prints
  //fEfficiencies.debug();
  //fEfficienciesUp.debug();
  //fEfficienciesDown.debug();
  //fSF.debug();
  //fSFUp.debug();
  //fSFDown.debug();
  // Check validity of input
  if (!sizeOfEfficiencyList(BTagSFInputStash::kBJet, "nominal") || !sizeOfSFList(BTagSFInputStash::kBJet, "nominal")) {
    isActive = false;
    std::cout << "WARNING: Disabling Btag SF because btag SF's and efficiencies are not provided!" << std::endl;
  }
}

// Destructor
BTagSFCalculator::~BTagSFCalculator() {
  if (hBTagSF) delete hBTagSF;
  if (hBTagSFRelUncert) delete hBTagSFRelUncert;
}

// Book histograms
void BTagSFCalculator::bookHistograms(TDirectory* dir, HistoWrapper& histoWrapper) {
  hBTagSF = histoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "btagSF", "btag SF", 500, 0., 5.);
  hBTagSFRelUncert = histoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "btagSFRelUncert", "Relative btagSF uncert.", 100, 0., 1.);
}


// Calculate scale factors
const float BTagSFCalculator::calculateSF(const std::vector<Jet>& selectedJets, const std::vector<Jet>& selectedBJets) {
  if (!isActive) return 1.0;

  double totalSF = 1.0; // final number to be returned
  for (auto &jet: selectedJets) {
    // See if the jet passed the b jet selection
    bool passedBJetSelection = false;
    for (auto &bjet: selectedBJets) {
      if (std::abs(jet.bjetDiscriminator() - bjet.bjetDiscriminator()) < 0.0001) {
        passedBJetSelection = true;
      }
    }
    // Obtain jet flavor
    int flavor = std::abs(jet.pdgId());
    BTagSFInputStash::BTagJetFlavorType flavorType = BTagSFInputStash::kUDSJet; // Default value, used also for flavor == 0
    if (flavor == 5) { // b jet
      flavorType = BTagSFInputStash::kBJet;
    } else if (flavor == 4) { // c jet
      flavorType = BTagSFInputStash::kCJet;
    } else if (flavor == 21) { // g jet
      flavorType = BTagSFInputStash::kGJet;
    }
    // Calculate SF
    // Assuming that the SF's of the jets are independent (BTV POG recommendation)
    // Such approach simplifies notably the error propagation
    double sf = 0.;
    if (passedBJetSelection) {
    // x -> b jet; just apply the SF or SF+deltaSF
      if ((fVariationInfo == kVariationTagUp && flavor == 5) || (fVariationInfo == kVariationMistagUp && flavor != 5)) {
      // up variation
        sf = fSFUp.getInputValueByPt(flavorType, jet.pt());
      // down variation
      } else if ((fVariationInfo == kVariationTagDown && flavor == 5) || (fVariationInfo == kVariationMistagDown && flavor != 5)) {
        sf = fSFDown.getInputValueByPt(flavorType, jet.pt());
      // nominal
      } else {
        sf = fSF.getInputValueByPt(flavorType, jet.pt());
      }
    } else {
    // x -> not b; apply (1-eff*SF)/(1-eff) where eff = MC efficiency, SF = per-jet scale factor
      double eff = fEfficiencies.getInputValueByPt(flavorType, jet.pt());
      double sfvalue = fSF.getInputValueByPt(flavorType, jet.pt());
      // nominal
      double sfnominal = std::abs((1.0-eff*sfvalue) / (1.0-eff));
      // up variation
      if ((fVariationInfo == kVariationTagUp && flavor == 5) || (fVariationInfo == kVariationMistagUp && flavor != 5)) {
        double effDelta = fEfficienciesUp.getInputValueByPt(flavorType, jet.pt());
        double sfDelta = fSFUp.getInputValueByPt(flavorType, jet.pt()) - sfvalue;
        // error propagation
        double a = (1-sfvalue) / (1.0-eff) / (1.0-eff); // d/deff((1-eff*SF)/(1-eff))
        double b = -eff / (1.0-eff); // d/dsf((1-eff*SF)/(1-eff))
        // squared sum of eff and SF uncertainties
        double sfuncert = TMath::Sqrt(a*a*effDelta*effDelta + b*b*sfDelta*sfDelta);
        sf = std::abs(sfnominal + sfuncert);
        hBTagSFRelUncert->Fill(sfuncert/sfnominal);
      }
      // down variation
      else if ((fVariationInfo == kVariationTagDown && flavor == 5) || (fVariationInfo == kVariationMistagDown && flavor != 5)) {
        double effDelta = fEfficienciesDown.getInputValueByPt(flavorType, jet.pt());
        double sfDelta = fSFDown.getInputValueByPt(flavorType, jet.pt()) - sfvalue;
        // error propagation (as above)
        double a = (1-sfvalue) / (1.0-eff) / (1.0-eff); // d/deff((1-eff*SF)/(1-eff))
        double b = -eff / (1.0-eff); // d/dsf((1-eff*SF)/(1-eff))
        // squared sum of eff and SF uncertainties
        double sfuncert = TMath::Sqrt(a*a*effDelta*effDelta + b*b*sfDelta*sfDelta);
        sf = std::abs(sfnominal - sfuncert);
        hBTagSFRelUncert->Fill(sfuncert/sfnominal);
      } 
      // nominal
      else {
        sf = sfnominal;
      }
      // Protect against div by zero
      if (std::abs(eff-1.0) < 0.00001 || sfnominal > 2.0) {
        std::cout << "BtagSF: anomalously high sf, using sf=1 for this jet: flavor=" << flavor << " pt=" << jet.pt() << " pass btag=" << passedBJetSelection << " eff=" << eff << " sf=" << sf << std::endl;
        sf = 1.0;
      }
    }
    totalSF *= sf;
    //std::cout << "jet: flavor=" << flavor << " pt=" << jet.pt() << " pass=" << passedBJetSelection << " sf=" << sf << std::endl;
    //std::cout << totalSF << std::endl;
  }
  //std::cout << "SF=" << totalSF << std::endl;
  hBTagSF->Fill(totalSF);
  
  return totalSF;
}


// Get size of const list
const size_t BTagSFCalculator::sizeOfEfficiencyList(BTagSFInputStash::BTagJetFlavorType flavor, const std::string& direction) const {
  if (direction == "nominal")
    return fEfficiencies.sizeOfList(flavor);
  if (direction == "up")
    return fEfficienciesUp.sizeOfList(flavor);
  if (direction == "down")
    return fEfficienciesDown.sizeOfList(flavor);
  return 0;
}

// Get list size
const size_t BTagSFCalculator::sizeOfSFList(BTagSFInputStash::BTagJetFlavorType flavor, const std::string& direction) const {
  if (direction == "nominal")
    return fSF.sizeOfList(flavor);
  if (direction == "up")
    return fSFUp.sizeOfList(flavor);
  if (direction == "down")
    return fSFDown.sizeOfList(flavor);
  return 0;
}

// Import efficiencies
void BTagSFCalculator::handleEfficiencyInput(boost::optional<std::vector<ParameterSet>> psets) {
  if (!psets) return;
  for (auto &p: *psets) {
    // Obtain variables
    float ptMin = p.getParameter<float>("ptMin");
    float ptMax = p.getParameter<float>("ptMax");
    float eff = p.getParameter<float>("eff");
    float effUp = p.getParameter<float>("effUp");
    float effDown = p.getParameter<float>("effDown");
    BTagSFInputStash::BTagJetFlavorType flavor = getFlavorTypeForEfficiency(p.getParameter<std::string>("jetFlavor"));
    // Store item
    fEfficiencies.addInput(flavor, ptMin, ptMax, eff);
    fEfficienciesUp.addInput(flavor, ptMin, ptMax, effUp);
    fEfficienciesDown.addInput(flavor, ptMin, ptMax, effDown);
    //std::cout << "adding eff " << flavor << " ptmin=" << ptMin << " ptmax=" << ptMax << std::endl;
  }
}

// Import scale factors
void BTagSFCalculator::handleSFInput(boost::optional<std::vector<ParameterSet>> psets) {
  if (!psets) return;
  for (auto &p: *psets) {
    // Obtain variables
    float ptMin = p.getParameter<float>("ptMin");
    float ptMax = p.getParameter<float>("ptMax");
    std::string formula = p.getParameter<std::string>("formula");
    std::string sysType = p.getParameter<std::string>("sysType");
    BTagSFInputStash::BTagJetFlavorType flavor = getFlavorTypeForSF(p.getParameter<int>("jetFlavor"));
    std::vector<BTagSFInputStash::BTagJetFlavorType> flavorCollection;
    if (flavor == BTagSFInputStash::kUDSGJet) {
      flavorCollection.push_back(BTagSFInputStash::kUDSJet);
      flavorCollection.push_back(BTagSFInputStash::kGJet);
    } else {
      flavorCollection.push_back(flavor);
    }
    for (auto pflavor: flavorCollection) {
      if (sysType == " central") {
        fSF.addInput(pflavor, ptMin, ptMax, formula);
      } else if (sysType == " up") {
        fSFUp.addInput(pflavor, ptMin, ptMax, formula);
      } else if (sysType == " down") {
        fSFDown.addInput(pflavor, ptMin, ptMax, formula);
      } else {
        throw hplus::Exception("config") << "Undefined value for sysType '" << sysType << "'!";
      }
      //std::cout << "sf " << pflavor << std::endl;
    }
  }
  //std::cout << fBToBSF.size() << " " << fCToBSF.size() << " " << fGToBSF.size() << " " << fUdsToBSF.size() << std::endl;
}

// Get flavor type for efficiency
BTagSFInputStash::BTagJetFlavorType BTagSFCalculator::getFlavorTypeForEfficiency(const std::string& str) const {
  if (str == "B") {
    return BTagSFInputStash::kBJet;
  } else if (str == "C") {
    return BTagSFInputStash::kCJet;
  } else if (str == "Light") {
    return BTagSFInputStash::kUDSJet;
  } else if (str == "G") {
    return BTagSFInputStash::kGJet;
  }
  throw hplus::Exception("config") << "Unknown flavor '" << str << "'!";
}

// Get flavor type for scale factor
BTagSFInputStash::BTagJetFlavorType BTagSFCalculator::getFlavorTypeForSF(int i) const {
  if (i == 0) {
    return BTagSFInputStash::kBJet;
  } else if (i == 1) {
    return BTagSFInputStash::kCJet;
  } else if (i == 2) {
    return BTagSFInputStash::kUDSGJet;
  }
  throw hplus::Exception("config") << "Unknown flavor '" << i << "'!";
}

// Parser
const BTagSFCalculator::BTagSFVariationType BTagSFCalculator::parseVariationType(const ParameterSet& config) const {
  boost::optional<std::string> sDirection = config.getParameterOptional<std::string>("btagSFVariationDirection");
  boost::optional<std::string> sVariationInfo = config.getParameterOptional<std::string>("btagSFVariationInfo");
  if (!sDirection)
    return kNominal;
  // Nominal
  if (*sDirection == "nominal")
    return kNominal;
  // Variations
  if (!sVariationInfo) {
    throw hplus::Exception("config") << "Error: please specify in config field btagSFVariationInfo!";
  }
  if (*sDirection == "up") {
    if (*sVariationInfo == "tag")
      return kVariationTagUp;
    if (*sVariationInfo == "mistag")
      return kVariationMistagUp;
    throw hplus::Exception("config") << "Error: Invalid value for field btagSFVariationInfo!";
  }
  if (*sDirection == "down") {
    if (*sVariationInfo == "tag")
      return kVariationTagDown;
    if (*sVariationInfo == "mistag")
      return kVariationMistagDown;
    throw hplus::Exception("config") << "Error: Invalid value for field btagSFVariationInfo!";
  }
  throw hplus::Exception("config") << "Error: Invalid value for field btagSFVariationDirection!";
}
