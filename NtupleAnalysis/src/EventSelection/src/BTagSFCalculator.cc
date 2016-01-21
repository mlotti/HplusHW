// -*- c++ -*-
#include "EventSelection/interface/BTagSFCalculator.h"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"

BTagSFInputItem::BTagSFInputItem(float ptMin, float ptMax, const std::string formula)
: fPtMin(ptMin),
  fPtMax(ptMax),
  bIsOverflowBinPt(false) {
  int v = fFormula.Compile(formula.c_str());
  if (v) {
    throw hplus::Exception("config") << "BTag SF formula '" << formula << "' does not compile for TFormula!";
  }
}

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

BTagSFInputItem::~BTagSFInputItem() { }

bool BTagSFInputItem::matchesPtRange(float pt) const { 
  if (pt > fPtMin) {
    if (bIsOverflowBinPt || pt <= fPtMax) {
      return true;
    }
  }
  return false;
}

float BTagSFInputItem::getValueByPt(float pt) const {
  if (!matchesPtRange(pt)) {
    throw hplus::Exception("assert") << "The requested pt (" << pt << ") is out of range!";
  }
  return fFormula.Eval(pt);
}

BTagSFCalculator::BTagSFCalculator(const ParameterSet& config)
: isActive(true) {
  handleEfficiencyInput(config.getParameterOptional<std::vector<ParameterSet>>("btagEfficiency"));
  setOverflowBin(fBToBEfficiency);
  setOverflowBin(fCToBEfficiency);
  setOverflowBin(fGToBEfficiency);
  setOverflowBin(fUdsToBEfficiency);
  handleSFInput(config.getParameterOptional<std::vector<ParameterSet>>("btagSF"));
  setOverflowBin(fBToBSF);
  setOverflowBin(fCToBSF);
  setOverflowBin(fGToBSF);
  setOverflowBin(fUdsToBSF);
  // Check validity of input
  if (!fBToBEfficiency.size() || !fBToBSF.size()) {
    isActive = false;
    std::cout << "WARNING: Disabling Btag SF because btag SF's and efficiencies are not provided!" << std::endl;
  }
}

BTagSFCalculator::~BTagSFCalculator() {
  fBToBEfficiency.clear();
  fCToBEfficiency.clear();
  fGToBEfficiency.clear();
  fUdsToBEfficiency.clear();
  fBToBSF.clear();
  fCToBSF.clear();
  fGToBSF.clear();
  fUdsToBSF.clear();
}

void BTagSFCalculator::bookHistograms(TDirectory* dir, HistoWrapper& histoWrapper) {
  hBTagSF = histoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "btagSF", "btag SF", 500, 0., 5.);
}

float BTagSFCalculator::calculateSF(const std::vector<Jet>& selectedJets, const std::vector<Jet>& selectedBJets) {
  if (!isActive) return 1.0;

  double totalSF = 1.0;
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
    // Calculate SF
    float sf = 0.;
    float eff = 0.;
    if (flavor == 5) { // b jet
      sf = getInputValueByPt(fBToBSF, jet.pt());
      eff = getInputValueByPt(fBToBEfficiency, jet.pt());
    } else if (flavor == 4) { // c jet
      sf = getInputValueByPt(fCToBSF, jet.pt());
      eff = getInputValueByPt(fCToBEfficiency, jet.pt());
    } else if (flavor == 21) { // g jet
      sf = getInputValueByPt(fGToBSF, jet.pt());
      eff = getInputValueByPt(fGToBEfficiency, jet.pt());
    } else if (flavor == 1 || flavor == 2 || flavor == 3) { // uds jet
      sf = getInputValueByPt(fUdsToBSF, jet.pt());
      eff = getInputValueByPt(fUdsToBEfficiency, jet.pt());
    }
    if (passedBJetSelection) {
      totalSF *= sf;
    } else {
      totalSF *= (1.0 - eff * sf) / (1 - eff);
    }
    //std::cout << totalSF << std::endl;
  }
  hBTagSF->Fill(totalSF);
  return totalSF;
}

size_t BTagSFCalculator::sizeOfEfficiencyList(BTagJetFlavorType flavor) const {
  if (flavor == kBJet)
    return fBToBEfficiency.size();
  if (flavor == kCJet)
    return fCToBEfficiency.size();
  if (flavor == kGJet)
    return fGToBEfficiency.size();
  if (flavor == kUDSJet)
    return fUdsToBEfficiency.size();
  return 0;
}

size_t BTagSFCalculator::sizeOfSFList(BTagJetFlavorType flavor) const {
  if (flavor == kBJet)
    return fBToBSF.size();
  if (flavor == kCJet)
    return fCToBSF.size();
  if (flavor == kGJet)
    return fGToBSF.size();
  if (flavor == kUDSJet)
    return fUdsToBSF.size();
  return 0; 
}

void BTagSFCalculator::handleEfficiencyInput(boost::optional<std::vector<ParameterSet>> psets) {
  if (!psets) return;
  for (auto &p: *psets) {
    // Obtain variables
    float ptMin = p.getParameter<float>("ptMin");
    float ptMax = p.getParameter<float>("ptMax");
    std::stringstream s;
    s << p.getParameter<float>("eff");
    BTagJetFlavorType flavor = getFlavorTypeForEfficiency(p.getParameter<std::string>("jetFlavor"));
    // Store item
    if (flavor == kBJet)
      fBToBEfficiency.push_back(BTagSFInputItem(ptMin, ptMax, s.str()));
    else if (flavor == kCJet)
      fCToBEfficiency.push_back(BTagSFInputItem(ptMin, ptMax, s.str()));
    else if (flavor == kGJet || flavor == kUDSGJet)
      fGToBEfficiency.push_back(BTagSFInputItem(ptMin, ptMax, s.str()));
    else if (flavor == kUDSJet || flavor == kUDSGJet)
      fUdsToBEfficiency.push_back(BTagSFInputItem(ptMin, ptMax, s.str()));
  }
  //std::cout << fBToBEfficiency.size() << " " << fCToBEfficiency.size() << " " << fGToBEfficiency.size() << " " << fUdsToBEfficiency.size() << std::endl;
}

void BTagSFCalculator::handleSFInput(boost::optional<std::vector<ParameterSet>> psets) {
  if (!psets) return;
  for (auto &p: *psets) {
    // Obtain variables
    float ptMin = p.getParameter<float>("ptMin");
    float ptMax = p.getParameter<float>("ptMax");
    std::string s = p.getParameter<std::string>("formula");
    BTagJetFlavorType flavor = getFlavorTypeForSF(p.getParameter<int>("jetFlavor"));
    // Store item
    if (flavor == kBJet)
      fBToBSF.push_back(BTagSFInputItem(ptMin, ptMax, s));
    if (flavor == kCJet)
      fCToBSF.push_back(BTagSFInputItem(ptMin, ptMax, s));
    if (flavor == kGJet || flavor == kUDSGJet)
      fGToBSF.push_back(BTagSFInputItem(ptMin, ptMax, s));
    if (flavor == kUDSJet || flavor == kUDSGJet)
      fUdsToBSF.push_back(BTagSFInputItem(ptMin, ptMax, s));
  }
  //std::cout << fBToBSF.size() << " " << fCToBSF.size() << " " << fGToBSF.size() << " " << fUdsToBSF.size() << std::endl;
}

BTagSFCalculator::BTagJetFlavorType BTagSFCalculator::getFlavorTypeForEfficiency(std::string str) const {
  if (str == "B") {
    return kBJet;
  } else if (str == "C") {
    return kCJet;
  } else if (str == "Light") {
    return kUDSJet;
  } else if (str == "G") {
    return kGJet;
  }
  throw hplus::Exception("config") << "Unknown flavor '" << str << "'!";
}

BTagSFCalculator::BTagJetFlavorType BTagSFCalculator::getFlavorTypeForSF(int i) const {
  if (i == 0) {
    return kBJet;
  } else if (i == 1) {
    return kCJet;
  } else if (i == 2) {
    return kUDSGJet;
  }
  throw hplus::Exception("config") << "Unknown flavor '" << i << "'!";
}

void BTagSFCalculator::setOverflowBin(std::vector<BTagSFInputItem>& container) {
  if (!container.size()) return;
  float maxValue = -1.0;
  int index = -1;
  int i = 0;
  for (auto &p: container) {
    if (maxValue > p.getPtMax()) {
      maxValue = p.getPtMax();
      index = i;
    }
    ++i;
  }
  if (index >= 0) {
    container[index].setAsOverflowBinPt();
  }
}

float BTagSFCalculator::getInputValueByPt(std::vector<BTagSFInputItem>& container, float pt) {
  for (auto &p: container) {
    if (p.matchesPtRange(pt)) {
      return p.getValueByPt(pt);
    }
  }
  return 1.0;
}
