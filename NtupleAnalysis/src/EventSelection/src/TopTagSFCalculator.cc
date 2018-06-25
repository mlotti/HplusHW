// -*- c++ -*-
#include "EventSelection/interface/TopTagSFCalculator.h"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"

#include "TMath.h"

// --- TopTagSFInputitem ---


// Constructor using formula string
TopTagSFInputItem::TopTagSFInputItem(float ptMin, float ptMax, const std::string& formula)
: fPtMin(ptMin),
  fPtMax(ptMax),
  bIsOverflowBinPt(false) {
  int v = fFormula.Compile(formula.c_str());
  if (v) 
    {
      throw hplus::Exception("config") << "TopTag SF formula '" << formula << "' does not compile for TFormula!";
    }
}

// Constructor using efficiency number
TopTagSFInputItem::TopTagSFInputItem(float ptMin, float ptMax, float eff)
: fPtMin(ptMin),
  fPtMax(ptMax),
  bIsOverflowBinPt(false) {
  std::stringstream s;
  s << eff;
  int v = fFormula.Compile(s.str().c_str());
  if (v) {
    throw hplus::Exception("config") << "TopTag SF formula '" << eff << "' does not compile for TFormula!";
  }
}

// Destructor
TopTagSFInputItem::~TopTagSFInputItem() { }

const bool TopTagSFInputItem::matchesPtRange(float pt) const { 
  if (pt >= fPtMin) {
    if (bIsOverflowBinPt || pt <= fPtMax) {
      return true;
    }
  }
  return false;
}

// Evaluate SF for given pT
const float TopTagSFInputItem::getValueByPt(float pt) const {
  if (!matchesPtRange(pt)) {
    throw hplus::Exception("assert") << "The requested pt (" << pt << ") is out of range!";
  }
  // For jet pt's above the maximum pt value, use the maximum value (otherwise the SF's become anomalously large)
  if (pt > fPtMax) 
    {
      return fFormula.Eval(fPtMax);
    }

  return fFormula.Eval(pt);
}

void TopTagSFInputItem::setAsOverflowBinPt() 
{ 
  bIsOverflowBinPt = true; 

  return;
}

void TopTagSFInputItem::debug() const 
{
  // Print debug information
  std::cout << " ptmin = "    << fPtMin 
	    << " ptmax = "    << fPtMax 
            << " overflow = " << bIsOverflowBinPt 
            << " formula = "  << fFormula.GetExpFormula() 
	    << std::endl;
  
  return;
}


// --- TopTagSFInputStash ---

// Constructor
TopTagSFInputStash::TopTagSFInputStash() { }

// Destructor
TopTagSFInputStash::~TopTagSFInputStash() {
  std::vector<std::vector<TopTagSFInputItem*>> collections = { fGenuineTop, fFakeTop };

  for (auto& container: collections) {
    for (size_t i = 0; i < container.size(); ++i) {
      delete container[i];
    }
    container.clear();
  }

}

// Create new input item corresponding to certain pT range (using formula string)
void TopTagSFInputStash::addInput(TopTagJetFlavorType flavor, float ptMin, float ptMax, const std::string& formula) 
{
  getCollection(flavor).push_back(new TopTagSFInputItem(ptMin, ptMax, formula));

  return; 
}

// Create new input item corresponding to certain pT range (using eff)
void TopTagSFInputStash::addInput(TopTagJetFlavorType flavor, float ptMin, float ptMax, float eff) 
{
  getCollection(flavor).push_back(new TopTagSFInputItem(ptMin, ptMax, eff));
  return;
}

// Per-jet SF (by pT)
const float TopTagSFInputStash::getInputValueByPt(TopTagJetFlavorType flavor, float pt) const 
{
  for (auto &p: getConstCollection(flavor)) {
    if (p->matchesPtRange(pt)) {
      return p->getValueByPt(pt);
    }
  }
  std::cout << "=== TopTagSFCalculator::addInput() Jet pt " << pt << " flavor " << flavor << " is out of range for top-tag SF calculation!";
  return 1.0;
}

// Define overflow bin
void TopTagSFInputStash::setOverflowBinByPt(const std::string& label) 
{
  std::vector<std::vector<TopTagSFInputItem*>> collections = { fGenuineTop, fFakeTop};
  size_t i = 0;
  
  
  for (auto& container: collections) {
    if (!container.size()) {
      std::cout << "=== TopTagSFCalculator::setOverflowBinByPt() Empty collection for " << label << " flavor =" << i << std::endl;
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
  
  return;
}

 // Get const vector of input items
 const std::vector<TopTagSFInputItem*>& TopTagSFInputStash::getConstCollection(TopTagJetFlavorType flavor) const 
 {
   if (flavor == kInclusiveTop) return fInclusiveTop;
   else if (flavor == kGenuineTop) return fGenuineTop;
   else if (flavor == kFakeTop) return fFakeTop;
   throw hplus::Exception("Logic") << "Unknown flavor requested! " << flavor;
 }

// Get vector of input items
 std::vector<TopTagSFInputItem*>& TopTagSFInputStash::getCollection(TopTagJetFlavorType flavor) 
 {
   if (flavor == kInclusiveTop)  return fInclusiveTop;
   else if (flavor == kGenuineTop)  return fGenuineTop;
   else if (flavor == kFakeTop)  return fFakeTop;
   throw hplus::Exception("Logic") << "Unknown flavor requested! " << flavor;
 }

// Debug prints
void TopTagSFInputStash::debug() const {
  std::vector<std::vector<TopTagSFInputItem*>> collections = { fGenuineTop, fFakeTop};
  for (auto p: collections) {
    for (auto pp: p) {
      pp->debug();
    }
  }

  return;
}


// --- TopTagSFCalculator ---

// Constructor
TopTagSFCalculator::TopTagSFCalculator(const ParameterSet& config)
: fVariationInfo(parseVariationType(config)),
  isActive(true),
  hTopTagSF(nullptr),
  hTopTagSFRelUncert(nullptr) {
  // Import efficiencies
  handleEfficiencyInput(config.getParameterOptional<std::vector<ParameterSet>>("topTagEfficiency"));
  // fEfficiencies.setOverflowBinByPt("EfficiencyNominal"); //fixme
  // fEfficienciesUp.setOverflowBinByPt("EfficiencyUp");
  // fEfficienciesDown.setOverflowBinByPt("EfficiencyDown");
  // fEfficienciesSF.setOverflowBinByPt("EfficienciesSFnominal");
  // fEfficienciesSFUp.setOverflowBinByPt("EfficienciesSFup");
  // fEfficienciesSFDown.setOverflowBinByPt("EfficienciesSFdown");

  // Import misidefication rates
  handleMisidInput(config.getParameterOptional<std::vector<ParameterSet>>("topTagMisid"));
  // fMisid.setOverflowBinByPt("MisidNominal"); //fixme
  // fMisidUp.setOverflowBinByPt("MisidUp");
  // fMisidDown.setOverflowBinByPt("MisidDown");
  // fMisidSF.setOverflowBinByPt("MisidSFnominal");
  // fMisidSFUp.setOverflowBinByPt("MisidSFup");
  // fMisidSFDown.setOverflowBinByPt("MisidSFdown");

  // Import scale factors
  // handleSFInput(config.getParameterOptional<std::vector<ParameterSet>>("toptagSF"));
  // fEfficienciesSF.setOverflowBinByPt("SFnominal");
  // fEfficienciesSFUp.setOverflowBinByPt("SFup");
  // fEfficienciesSFDown.setOverflowBinByPt("SFdown");
  
  // Debug prints
  if (0)
    {
      std::cout << "\n=== TopTagSFCalculator::TopTagSFCalculator() - DEBUG" << std::endl;
      fEfficiencies.debug();
      fEfficienciesUp.debug();
      fEfficienciesDown.debug();
      fSF.debug();
      fSFUp.debug();
      fSFDown.debug();
    }
  
  // Check validity of input
  const size_t effSize   = sizeOfEfficiencyList(TopTagSFInputStash::kGenuineTop, "nominal");
  const size_t misidSize = sizeOfEfficiencyList(TopTagSFInputStash::kFakeTop, "nominal");
  if (!effSize)
    {
      isActive = false;
      std::cout << "=== TopTagSFCalculator::TopTagSFCalculator() Disabling topTag SF because top-tagging efficiencies and SFs are not provided!" << std::endl;
    }
  if (!misidSize)
    {
      isActive = false;
      std::cout << "=== TopTagSFCalculator::TopTagSFCalculator() Disabling topTag SF because top-tagging misidentification rates and SFs are not provided!" << std::endl;
    }

  return;    
}

// Destructor
TopTagSFCalculator::~TopTagSFCalculator() 
{
  if (hTopTagSF) delete hTopTagSF;
  if (hTopTagSFRelUncert) delete hTopTagSFRelUncert;
  if (hTopEff_Vs_TopPt_Inclusive) delete hTopEff_Vs_TopPt_Inclusive;
  if (hTopEff_Vs_TopPt_Fake) delete hTopEff_Vs_TopPt_Fake;
  if (hTopEff_Vs_TopPt_Genuine) delete hTopEff_Vs_TopPt_Genuine;
}


// Book the histograms
void TopTagSFCalculator::bookHistograms(TDirectory* dir, HistoWrapper& histoWrapper) {

  hTopTagSF = histoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "topTagSF", "topTag SF", 500, 0.0, 5.0);
  hTopTagSFRelUncert = histoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "topTagSFRelUncert", "Relative topTagSF uncert.", 100, 0.0, 1.0);
  hTopEff_Vs_TopPt_Inclusive = histoWrapper.makeTH<TH2F>(HistoLevel::kInformative, dir, "topEff_Vs_TopPt_Inclusive", ";Efficiency;p_{T}", 100, 0.0, 1.0, 400, 0, 2000);
  hTopEff_Vs_TopPt_Fake = histoWrapper.makeTH<TH2F>(HistoLevel::kInformative, dir, "topEff_Vs_TopPt_Fake", ";Efficiency;p_{T}", 100, 0.0, 1.0, 400, 0, 2000);
  hTopEff_Vs_TopPt_Genuine = histoWrapper.makeTH<TH2F>(HistoLevel::kInformative, dir, "topEff_Vs_TopPt_Genuine", ";Efficiency;p_{T}", 100, 0.0, 1.0, 400, 0, 2000);
  
  return;

}

// Calculate scale factors
const float TopTagSFCalculator::calculateSF(const std::vector<math::XYZTLorentzVector> cleanTopP4, 
					    const std::vector<double> cleanTopMVA, 
					    const std::vector<bool> cleanTopIsTagged, 
					    const std::vector<bool> cleanTopIsGenuine)
{
  if (!isActive) return 1.0;
  
  // Define the totalSF (the final number to be returned)
  float totalSF = 1.0;
  bool debug = false;

  // For loop: All cleaned top-candidates
  for (size_t i = 0; i < cleanTopP4.size(); i++)
    {
      float pt   = cleanTopP4.at(i).pt();
      float mass = cleanTopP4.at(i).M();
      float mva  = cleanTopMVA.at(i);
      bool isGen = cleanTopIsGenuine.at(i);
      bool isTag = cleanTopIsTagged.at(i);
      TopTagSFInputStash::TopTagJetFlavorType flavor;
      
      // Calculate the SF
      float sf  = 0.0;
      
      // Top candidate is tagged (t|?)
      if (isTag)
	{
	  // Top candidate is also truth-matched  (t|gen-t)
	  if (isGen)
	    {
	      flavor = TopTagSFInputStash::kGenuineTop;
	    }
	  else // Top candidate is not truth-matched  (t|!gen-t)
	    {
	      flavor = TopTagSFInputStash::kFakeTop;
	    }
	     
	  // sf = just apply the SF or SF+deltaSF
	  float eff = fEfficiencies.getInputValueByPt(flavor, pt);	  

	  // nominal
	  sf = fSF.getInputValueByPt(flavor, pt);
	  
          hTopEff_Vs_TopPt_Inclusive          -> Fill(eff, pt);
          if (isGen) hTopEff_Vs_TopPt_Genuine -> Fill(eff, pt);
          else hTopEff_Vs_TopPt_Fake          -> Fill(eff, pt);

	  // up variation
	  // sf = fSFUp.getInputValueByPt(flavor, pt); //fixme
	  
	  // down variation
	  // sf = fSFDown.getInputValueByPt(flavor, pt); /fixme
	  
	} 
      else // Top candidate is not tagged (!t|?)
	{
	  // Top candidate is nevertheless truth-matched  (!t|gen-t)
	  if (isGen)
	    {
	      flavor = TopTagSFInputStash::kGenuineTop;
	    }
	  else // Top candidate is not truth-matched  (!t|!gen-t)
	    {
	      flavor = TopTagSFInputStash::kFakeTop;
	    }
	  
	  // sf = (1-eff*SF)/(1-eff) where eff = MC efficiency, SF = (Data efficiency) / (MC efficiency)
	  float sf_value   = fSF.getInputValueByPt(flavor, pt);	
	  float eff        = fEfficiencies.getInputValueByPt(flavor, pt);
	  float sf_nominal = std::abs((1.0-eff*sf_value) / (1.0-eff));
	  
	  // nominal
	  sf = sf_nominal;

          hTopEff_Vs_TopPt_Inclusive          -> Fill(eff, pt);
          if (isGen) hTopEff_Vs_TopPt_Genuine -> Fill(eff, pt);
          else hTopEff_Vs_TopPt_Fake          -> Fill(eff, pt);
	
	  // Protect against div by zero
	  if (std::abs(eff-1.0) < 0.00001 || sf_nominal > 2.0) 
	    {
	      std::cout << "=== TopTagSFCalculator::calculateSF(): Anomalously high SF."
			<< " Using SF=1 for this top-canidate with flavor = " << flavor 
			<< " pt = " << pt << " isTag = " << isTag 
			<< " isGen = " << isGen << " eff = " << eff << " SF = " << sf << std::endl;
	      sf = 1.0;
	    }
	}
      
      // Event weight to correct simulations is a product of SFs and MC tagging effiencies
      totalSF *= sf;
      if (debug) std::cout << i+1 << "/" << cleanTopP4.size() << ": pT = " << pt << " m(jjb) = " << mass << " MVA " << mva	       
		       << " isTag = " << isTag << " isGen = " << isGen 
		       << " flavor = " << flavor << " eff = " << fEfficiencies.getInputValueByPt(flavor, pt)
		       << " SF = " << sf << " totalSF = " << totalSF << std::endl;

    }
  if (debug) std::cout << "\n" << std::endl;

  // Fill histograms
  hTopTagSF->Fill(totalSF);
  
  if (0) std::cout << "totalSF = " << totalSF << std::endl;
  return totalSF;
}


// Get size of const list
const size_t TopTagSFCalculator::sizeOfEfficiencyList(TopTagSFInputStash::TopTagJetFlavorType flavor, const std::string& direction) const {

  if (direction == "nominal") return fEfficiencies.sizeOfList(flavor);
  if (direction == "up") return fEfficienciesUp.sizeOfList(flavor);
  if (direction == "down") return fEfficienciesDown.sizeOfList(flavor);
  return 0;
}

// Get list size
const size_t TopTagSFCalculator::sizeOfSFList(TopTagSFInputStash::TopTagJetFlavorType flavor, const std::string& direction) const {
  if (direction == "nominal") return fSF.sizeOfList(flavor);
  if (direction == "up") return fSFUp.sizeOfList(flavor);
  if (direction == "down") return fSFDown.sizeOfList(flavor);
  return 0;
}

// Import efficiencies
void TopTagSFCalculator::handleEfficiencyInput(boost::optional<std::vector<ParameterSet>> psets) {

  // Sanity check
  if (!psets) 
    {
      std::cout << "=== TopTagSFCalculator::handleEfficiencyInput() No Psets found! Return." << std::endl;
      return;
    }

  // For-loop: All PSets
  for (auto &p: *psets) 
    {

    // Obtain variables
    float ptMin        = p.getParameter<float>("ptMin");
    float ptMax        = p.getParameter<float>("ptMax");
    float effData      = p.getParameter<float>("effData");
    float effDataUp    = p.getParameter<float>("effDataUp");
    float effDataDown  = p.getParameter<float>("effDataDown");
    float effMC        = p.getParameter<float>("effMC");
    float effMCUp      = p.getParameter<float>("effMCUp");
    float effMCDown    = p.getParameter<float>("effMCDown");
    float sfMC         = p.getParameter<float>("sf");
    float sfMCUp       = p.getParameter<float>("sfUp");
    float sfMCDown     = p.getParameter<float>("sfDown");
    TopTagSFInputStash::TopTagJetFlavorType flavor = getFlavorTypeForEfficiency("Genuine"); // fixme
    // TopTagSFInputStash::TopTagJetFlavorType flavor = getFlavorTypeForEfficiency(p.getParameter<std::string>("jetFlavor")); 

    // Store items
    fEfficiencies.addInput(flavor, ptMin, ptMax, effMC);
    fEfficienciesUp.addInput(flavor, ptMin, ptMax, effMCUp);
    fEfficienciesDown.addInput(flavor, ptMin, ptMax, effMCDown);
    fSF.addInput(flavor, ptMin, ptMax, sfMC);
    fSFUp.addInput(flavor, ptMin, ptMax, sfMCUp);
    fSFDown.addInput(flavor, ptMin, ptMax, sfMCDown);

    // Debug?
    if (0)
      {
	std::cout << "ptmin = " << ptMin << " ptmax = " << ptMax 
		  << " effData = " << effData << " effDataUp = " << effDataUp
		  << " effDataDown = " << effDataDown << " effMC = " << effMC
		  << " effMCUp = " << effMCUp  << " effMCDown = " << effMCDown
		  << " sfMC = " << sfMC << " sfMCUp = " << sfMCUp
		  << " sfMCDown = " << sfMCDown << std::endl;
      }
    
    }

  return;
}


// Import misidentification rates
void TopTagSFCalculator::handleMisidInput(boost::optional<std::vector<ParameterSet>> psets) {

  // Sanity check
  if (!psets) 
    {
      std::cout << "TopTagSFCalculator::handleEfficiencyInput() No Psets found! Return." << std::endl;
      return;
    }

  // For-loop: All PSets
  for (auto &p: *psets) 
    {

    // Obtain variables
    float ptMin         = p.getParameter<float>("ptMin");
    float ptMax         = p.getParameter<float>("ptMax");
    float misidData     = p.getParameter<float>("misidData");
    float misidDataUp   = p.getParameter<float>("misidDataUp");
    float misidDataDown = p.getParameter<float>("misidDataDown");
    float misidMC       = p.getParameter<float>("misidMC");
    float misidMCUp     = p.getParameter<float>("misidMCUp");
    float misidMCDown   = p.getParameter<float>("misidMCDown");
    float sfMC          = p.getParameter<float>("sf");
    float sfMCUp        = p.getParameter<float>("sfUp");
    float sfMCDown      = p.getParameter<float>("sfDown");
    TopTagSFInputStash::TopTagJetFlavorType flavor = getFlavorTypeForEfficiency("Fake");//tmp: fixme
    // TopTagSFInputStash::TopTagJetFlavorType flavor = getFlavorTypeForEfficiency(p.getParameter<std::string>("jetFlavor")); 

    // Store items
    fEfficiencies.addInput(flavor, ptMin, ptMax, misidMC);
    fEfficienciesUp.addInput(flavor, ptMin, ptMax, misidMCUp);
    fEfficienciesDown.addInput(flavor, ptMin, ptMax, misidMCDown);
    fSF.addInput(flavor, ptMin, ptMax, sfMC);
    fSFUp.addInput(flavor, ptMin, ptMax, sfMCUp);
    fSFDown.addInput(flavor, ptMin, ptMax, sfMCDown);

    // Debug?
    if (0)
      {
	std::cout << "ptmin = " << ptMin << " ptmax = " << ptMax 
		  << " misidData = " << misidData << " misidDataUp = " << misidDataUp 
		  << " misidDataDown = " << misidDataDown << " misidMC = " << misidMC
		  << " misidMCUp = " << misidMCUp   << " misidMCDown = "   << misidMCDown
		  << " sfMC = "  << sfMC << " sfMCUp = " << sfMCUp 
		  << " sfMCDown = " << sfMCDown << std::endl;
      }
    }
  
  return;
}

// Import scale factors
void TopTagSFCalculator::handleSFInput(boost::optional<std::vector<ParameterSet>> psets) {
  // Sanity check
  if (!psets) 
    {
      std::cout << "TopTagSFCalculator::handleEfficiencyInput() No Psets found! Return" << std::endl;
      return;
    }

  // For-loop: All psets
  for (auto &p: *psets) {

    // Obtain variables
    float ptMin         = p.getParameter<float>("ptMin");
    float ptMax         = p.getParameter<float>("ptMax");
    std::string formula = p.getParameter<std::string>("formula");
    std::string sysType = p.getParameter<std::string>("sysType");
    // TopTagSFInputStash::TopTagJetFlavorType flavor = getFlavorTypeForEfficiency("Genuine");//tmp: fixme
    // TopTagSFInputStash::TopTagJetFlavorType flavor = getFlavorTypeForEfficiency(p.getParameter<std::string>("jetFlavor")); 
    std::vector<TopTagSFInputStash::TopTagJetFlavorType> flavorCollection;
    flavorCollection.push_back(TopTagSFInputStash::kInclusiveTop);

    // For-loop: All flavor collections
    for (auto pflavor: flavorCollection) 
      {
	if (sysType == " central")   fSF.addInput(pflavor, ptMin, ptMax, formula);
	else if (sysType == " up")   fSFUp.addInput(pflavor, ptMin, ptMax, formula);
	else if (sysType == " down") fSFDown.addInput(pflavor, ptMin, ptMax, formula);
	else 
	  {
	    throw hplus::Exception("config") << "Undefined value for sysType '" << sysType << "'!";
	  }
	std::cout << "sf " << pflavor << std::endl;
      }
  }

  return;
}

// Get flavor type for efficiency (from .json file evaluated with TopTagEfficiencyAnalysis)
TopTagSFInputStash::TopTagJetFlavorType TopTagSFCalculator::getFlavorTypeForEfficiency(const std::string& str) const {
  if (str == "Inclusive") return TopTagSFInputStash::kInclusiveTop;
  else if (str == "Genuine") return TopTagSFInputStash::kGenuineTop;
  else if (str == "Fake") return TopTagSFInputStash::kFakeTop;
  else throw hplus::Exception("config") << "Unknown flavor '" << str << "'!";
}

// Get flavor type for scale factor (from .csv file provided by TopTagging POG)
TopTagSFInputStash::TopTagJetFlavorType TopTagSFCalculator::getFlavorTypeForSF(int i) const {
  if (i == 0) return TopTagSFInputStash::kInclusiveTop;
  else if (i == 1) return TopTagSFInputStash::kGenuineTop;
  else if (i == 2) return TopTagSFInputStash::kFakeTop;
  else throw hplus::Exception("config") << "Unknown flavor '" << i << "'!";
}

// Parser
const TopTagSFCalculator::TopTagSFVariationType TopTagSFCalculator::parseVariationType(const ParameterSet& config) const {
  boost::optional<std::string> sDirection = config.getParameterOptional<std::string>("topTagSFVariationDirection");
  boost::optional<std::string> sVariationInfo = config.getParameterOptional<std::string>("topTagSFVariationInfo");
  if (!sDirection) return kNominal;
  // Nominal
  if (*sDirection == "nominal") return kNominal;
  // Variations
  if (!sVariationInfo) {
    throw hplus::Exception("config") << "Error: please specify in config field topTagSFVariationInfo!";
  }
  if (*sDirection == "up") {
    if (*sVariationInfo == "tag")
      return kVariationTagUp;
    if (*sVariationInfo == "mistag")
      return kVariationMistagUp;
    throw hplus::Exception("config") << "Error: Invalid value for field topTagSFVariationInfo!";
  }
  if (*sDirection == "down") {
    if (*sVariationInfo == "tag")
      return kVariationTagDown;
    if (*sVariationInfo == "mistag")
      return kVariationMistagDown;
    throw hplus::Exception("config") << "Error: Invalid value for field topTagSFVariationInfo!";
  }
  throw hplus::Exception("config") << "Error: Invalid value for field topTagSFVariationDirection!";
}
