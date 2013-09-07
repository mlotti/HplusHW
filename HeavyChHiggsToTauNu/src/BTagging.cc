/*
  PURPOSE
  Loop over jets in event and apply a b-tagging discriminator. If an event contains at least one b-tagged jet, it will be flagged as having passed.
  If the event is MC, its current weight is multiplied by a b-tagging scale factor (SF). See also BTaggingScaleFactorFromDB.cc.
*/
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingScaleFactorFromDB.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TMath.h"
#include<vector>
#include<algorithm>

std::vector<const reco::GenParticle*>   getImmediateMothers(const reco::Candidate&);
std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);
bool  hasImmediateMother(const reco::Candidate& p, int id);
bool  hasMother(const reco::Candidate& p, int id);
void  printImmediateMothers(const reco::Candidate& p);
void  printMothers(const reco::Candidate& p);
std::vector<const reco::GenParticle*>  getImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*>   getDaughters(const reco::Candidate& p);
bool  hasImmediateDaughter(const reco::Candidate& p, int id);
bool  hasDaughter(const reco::Candidate& p, int id);
void  printImmediateDaughters(const reco::Candidate& p);
void printDaughters(const reco::Candidate& p);

namespace {
  // The below things are contained in an anonymous namespace to prevent them from being accessed from outside this file.
  // Set this to true to enable printing output for debugging/checking calculations:
  bool printValidationOutput = true;
  // Tool to convert SF and efficiency tables from C-type table to std::vector.
  template <int N>
  std::vector<double> toVector(double (&input)[N]) {
    std::vector<double> ret;
    ret.reserve(N);
    std::copy(input, input+N, std::back_inserter(ret));
    return ret;
  }
}

namespace HPlus {
  // ===== Look-up tables and parametrized functions for scale factors and tagging efficiencies =====

  namespace SFBins {
    double ptmin[] = {30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500};
  }
  namespace CSVL {
    // B-tagging scale factors
    // Source:    https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFb-mujet_payload.txt
    // Retrieved: 2013-09-04
    const char* SFb = "1.02658*((1.+(0.0195388*x))/(1.+(0.0209145*x)))";
    double SFb_error[] = {
      0.0188743,
      0.0161816,
      0.0139824,
      0.0152644,
      0.0161226,
      0.0157396,
      0.0161619,
      0.0168747,
      0.0257175,
      0.026424,
      0.0264928,
      0.0315127,
      0.030734,
      0.0438259 };
    // Mistagging scale factors
    // Source:    https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs.C
    // Row:       Atagger == "CSVL" && sEtamin == "0.0" && sEtamax == "2.4"
    // Retrieved: 2013-09-04
    TF1 *SFl     = new TF1("SFlight","((1.0344+(0.000962994*x))+(-3.65392e-06*(x*x)))+(3.23525e-09*(x*(x*x)))", 20.,670.);
    TF1 *SFl_min = new TF1("SFlightMin","((0.956023+(0.000825106*x))+(-3.18828e-06*(x*x)))+(2.81787e-09*(x*(x*x)))", 20.,670.);
    TF1 *SFl_max = new TF1("SFlightMax","((1.11272+(0.00110104*x))+(-4.11956e-06*(x*x)))+(3.65263e-09*(x*(x*x)))", 20.,670.);
    // B->B efficiencies
    double ptBinLowEdges_BtoB[] = {20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 200, 250, 300, 350, 400};
    double eff_BtoB[] = {0.821023, 0.844312, 0.841045, 0.849044, 0.848066, 0.853467, 0.847721, 0.848242, 0.849008, 0.852407, 0.852413, 0.843951, 0.820661, 0.826063, 0.773984, 0.756426, 0.633727};
    double effUncertainty_BtoB[] = {0.005739, 0.004294, 0.004514, 0.004737, 0.005098, 0.005450, 0.006033, 0.006512, 0.005161, 0.006037, 0.007169, 0.006949, 0.010137, 0.015885, 0.027706, 0.040550, 0.045388};
    // C->B efficiencies

    // UDS->B efficiencies

    // G->B efficiencies
    double eff_GtoB[] = {0.259164, 0.240507, 0.151367, 0.125611, 0.116589, 0.121143, 0.107907, 0.090414, 0.082867, 0.080655, 0.081918, 0.094026, 0.101960, 0.100259, 0.077350, 0.072080, 0.094000};
    double effUncertainty_GtoB[] = {0.004679, 0.005317, 0.005481, 0.005952, 0.006675, 0.007612, 0.008025, 0.008179, 0.006400, 0.007538, 0.008682, 0.008497, 0.011539, 0.015783, 0.017536, 0.025889, 0.025597};
  }
  namespace CSVM {
    // B-tagging scale factors
    // Source:    https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFb-mujet_payload.txt
    // Retrieved: 2013-09-04
    const char* SFb = "0.6981*((1.+(0.414063*x))/(1.+(0.300155*x)))";
    double SFb_error[] = {
      0.0295675,
      0.0295095,
      0.0210867,
      0.0219349,
      0.0227033,
      0.0204062,
      0.0185857,
      0.0256242,
      0.0383341,
      0.0409675,
      0.0420284,
      0.0541299,
      0.0578761,
      0.0655432 };
    // Mistagging scale factors
    // Source:    https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs.C
    // Row:       Atagger == "CSVM" && sEtamin == "0.0" && sEtamax == "2.4"
    // Retrieved: 2013-09-04
    TF1 *SFl     = new TF1("SFlight","((1.04318+(0.000848162*x))+(-2.5795e-06*(x*x)))+(1.64156e-09*(x*(x*x)))", 20.,670.);
    TF1 *SFl_min = new TF1("SFlightMin","((0.962627+(0.000448344*x))+(-1.25579e-06*(x*x)))+(4.82283e-10*(x*(x*x)))", 20.,670.);
    TF1 *SFl_max = new TF1("SFlightMax","((1.12368+(0.00124806*x))+(-3.9032e-06*(x*x)))+(2.80083e-09*(x*(x*x)))", 20.,670.);
    // B->B efficiencies
    double ptBinLowEdges_BtoB[] = {20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 200, 250, 300, 350, 400};
    double eff_BtoB[] = {0.821023, 0.844312, 0.841045, 0.849044, 0.848066, 0.853467, 0.847721, 0.848242, 0.849008, 0.852407, 0.852413, 0.843951, 0.820661, 0.826063, 0.773984, 0.756426, 0.633727};
    double effUncertainty_BtoB[] = {0.005739, 0.004294, 0.004514, 0.004737, 0.005098, 0.005450, 0.006033, 0.006512, 0.005161, 0.006037, 0.007169, 0.006949, 0.010137, 0.015885, 0.027706, 0.040550, 0.045388};
    // C->B efficiencies

    // UDS->B efficiencies

    // G->B efficiencies
    double eff_GtoB[] = {0.259164, 0.240507, 0.151367, 0.125611, 0.116589, 0.121143, 0.107907, 0.090414, 0.082867, 0.080655, 0.081918, 0.094026, 0.101960, 0.100259, 0.077350, 0.072080, 0.094000};
    double effUncertainty_GtoB[] = {0.004679, 0.005317, 0.005481, 0.005952, 0.006675, 0.007612, 0.008025, 0.008179, 0.006400, 0.007538, 0.008682, 0.008497, 0.011539, 0.015783, 0.017536, 0.025889, 0.025597};
  }
  namespace CSVT {
    // B-tagging scale factors
    // Source:    https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFb-mujet_payload.txt
    // Retrieved: 2013-09-04
    const char* SFb = "0.901615*((1.+(0.552628*x))/(1.+(0.547195*x)))";
    double SFb_error[] = {
      0.0364717,
      0.0362281,
      0.0232876,
      0.0249618,
      0.0261482,
      0.0290466,
      0.0300033,
      0.0453252,
      0.0685143,
      0.0653621,
      0.0712586,
      0.094589,
      0.0777011,
      0.0866563 };
    // Mistagging scale factors
    // Source:    https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs.C
    // Row:       Atagger == "CSVT" && sEtamin == "0.0" && sEtamax == "2.4"
    // Retrieved: 2013-09-04
    TF1 *SFl     = new TF1("SFlight","((0.948463+(0.00288102*x))+(-7.98091e-06*(x*x)))+(5.50157e-09*(x*(x*x)))", 20.,670.);
    TF1 *SFl_min = new TF1("SFlightMin","((0.899715+(0.00102278*x))+(-2.46335e-06*(x*x)))+(9.71143e-10*(x*(x*x)))", 20.,670.);
    TF1 *SFl_max = new TF1("SFlightMax","((0.997077+(0.00473953*x))+(-1.34985e-05*(x*x)))+(1.0032e-08*(x*(x*x)))", 20.,670.);
    // B->B efficiencies
    double ptBinLowEdges_BtoB[] = {20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 200, 250, 300, 350, 400};
    double eff_BtoB[] = {0.821023, 0.844312, 0.841045, 0.849044, 0.848066, 0.853467, 0.847721, 0.848242, 0.849008, 0.852407, 0.852413, 0.843951, 0.820661, 0.826063, 0.773984, 0.756426, 0.633727};
    double effUncertainty_BtoB[] = {0.005739, 0.004294, 0.004514, 0.004737, 0.005098, 0.005450, 0.006033, 0.006512, 0.005161, 0.006037, 0.007169, 0.006949, 0.010137, 0.015885, 0.027706, 0.040550, 0.045388};
    // C->B efficiencies

    // UDS->B efficiencies

    // G->B efficiencies
    double eff_GtoB[] = {0.259164, 0.240507, 0.151367, 0.125611, 0.116589, 0.121143, 0.107907, 0.090414, 0.082867, 0.080655, 0.081918, 0.094026, 0.101960, 0.100259, 0.077350, 0.072080, 0.094000};
    double effUncertainty_GtoB[] = {0.004679, 0.005317, 0.005481, 0.005952, 0.006675, 0.007612, 0.008025, 0.008179, 0.006400, 0.007538, 0.008682, 0.008497, 0.011539, 0.015783, 0.017536, 0.025889, 0.025597};
  }


  // ================================== class Data ==================================
  BTagging::Data::Data():
    fPassedEvent(false),
    iNBtags(-1),
    fMaxDiscriminatorValue(-999.0),
    fEventScaleFactor(1.0),
    fEventScaleFactorAbsoluteUncertainty(0.0),
    fEventScaleFactorRelativeUncertainty(0.0)
    { }
  BTagging::Data::~Data() {}

  const bool BTagging::Data::hasGenuineBJets() const {
    for (edm::PtrVector<pat::Jet>::const_iterator iter = fSelectedJets.begin(); iter != fSelectedJets.end(); ++iter) {
      int myFlavor = std::abs((*iter)->partonFlavour());
      if (myFlavor == 5) return true;
    }
    return false;
  }

  // ================================== class ScaleFactorTable ==================================
  BTagging::ScaleFactorTable::ScaleFactorTable() : fScaleFactorFunction(0) {}

  BTagging::ScaleFactorTable::~ScaleFactorTable() {
    //std::cout << "Destructor called!" << std::endl;
    delete fScaleFactorFunction; fScaleFactorFunction = 0;
  }

  void BTagging::ScaleFactorTable::setScaleFactorTable(const std::vector<double>& ptBinTable, const char* SFFunctionExpression, const std::vector<double>& uncertaintyTable) {
    fPtBins = ptBinTable;
    setScaleFactorFunction(SFFunctionExpression);
    fScaleFactorUncertainty = uncertaintyTable;
    initializeJetTable();
  }

  void BTagging::ScaleFactorTable::initializeJetTable() {
    if (fPtBins.size() == 0) throw cms::Exception("LogicError")  << "Call BTagging::ScaleFactorTable::initializeJetTable() AFTER adding data to the lookup-table!";
    size_t i = 0;
    while (i < fPtBins.size()) {
      fPerBinUncertaintyUp.push_back(0.0);
      fPerBinUncertaintyDown.push_back(0.0);
      i++;
    }
  }

  void BTagging::ScaleFactorTable::setScaleFactorFunction(const char* expression) {
    fScaleFactorFunction = new TF1("scaleFactor", expression, 30.0, 670.0); // currently defined for jets with 30 < pT < 670 GeV (2013-09-04)
  }

  void BTagging::ScaleFactorTable::setScaleFactorUncertaintyFunctions(const char* expressionUp, const char* expressionDown) {
    fScaleFactorUncertUpFunction = new TF1("scaleFactorUncertUp", expressionUp, 30.0, 670.0);
    fScaleFactorUncertDownFunction = new TF1("scaleFactorUncertDown", expressionDown, 30.0, 670.0);
  }

  void BTagging::ScaleFactorTable::addJetSFUncertaintyTerm(double pT, bool isBTagged, EfficiencyTable& effTable, double factor) {
    double sfUncertUp = 0.0; double sfUncertDown = 0.0;
    double eff = effTable.getEfficiency(pT);
    double SF = getScaleFactor(pT);
    // UNBINNED UNCERTAINTIES:
    if (fScaleFactorUncertUpFunction && fScaleFactorUncertDownFunction) { // two functions given (one for lower, one for upper uncertainty)
      sfUncertUp = fScaleFactorUncertUpFunction->Eval(pT);
      sfUncertDown = fScaleFactorUncertDownFunction->Eval(pT);
      if (isBTagged) {
	fUnbinnedUncertaintyUp.push_back(factor * sfUncertUp / SF);
	fUnbinnedUncertaintyDown.push_back(factor * sfUncertDown / SF);
      } else {
	fUnbinnedUncertaintyUp.push_back(-factor * (eff * sfUncertUp) / (1.0 - eff * SF));
	fUnbinnedUncertaintyDown.push_back(-factor * (eff * sfUncertDown) / (1.0 - eff * SF));
      }
    }
    // BINNED UNCERTAINTIES:
    else if (fScaleFactorUncertainty.size() > 0) { // one vector of binned uncertainties given (lower and upper are equal)
      sfUncertUp = getScaleFactorUncertaintyBinned(pT);
      sfUncertDown = getScaleFactorUncertaintyBinned(pT);
      size_t i = obtainIndex(fPtBins, pT);
      if (isBTagged) {
	fPerBinUncertaintyUp[i] += factor * sfUncertUp / SF;
	fPerBinUncertaintyDown[i] += factor * sfUncertDown / SF;
      } else {
	fPerBinUncertaintyUp[i] += -factor * (eff * sfUncertUp) / (1.0 - eff * SF);
	fPerBinUncertaintyDown[i] += -factor * (eff * sfUncertDown) / (1.0 - eff * SF);
      }
    }
    else throw cms::Exception("LogicError")  << "Please provide two functions OR one vector of b-tagging SF upper and lower uncertainties! (Or implement using a different combination.)";
  }
  
  void BTagging::ScaleFactorTable::addJetSFUncertaintyTerm(double pT, bool isBTagged, EfficiencyTable& effTable) {
    addJetSFUncertaintyTerm(pT, isBTagged, effTable, 1.0);
  }
  
  size_t BTagging::ScaleFactorTable::obtainIndex(const std::vector<double>& table, double pt) {
    size_t myEnd = table.size();
    size_t myPos = 0;
    while (myPos < myEnd) {
      if (pt < table[myPos]) {
        if (myPos == 0)
          return 0; // should never happen
        else
          return myPos-1;
      }
      ++myPos;
    }
    return myEnd-1; // return last bin
  }

  double BTagging::ScaleFactorTable::getScaleFactor(double pt) const {
    if (fScaleFactorFunction) {
      //std::cout << "In getScaleFactor: fScaleFactorFunction exists! Evaluating..." << fScaleFactorFunction->Eval(pt) << std::endl;
      return fScaleFactorFunction->Eval(pt);
    }
    else if (fScaleFactor.size() > 0) return fScaleFactor[obtainIndex(fPtBins, pt)];
    else throw cms::Exception("LogicError")  << "Neither parametrized function nor look-up table for b-tagging scale factor found! Either one must be given.";
  }

  double BTagging::ScaleFactorTable::getScaleFactorUncertaintyBinned(double pt) const {
    return fScaleFactorUncertainty[obtainIndex(fPtBins, pt)];
  }

  double BTagging::ScaleFactorTable::calculateRelativeUncertaintySquared() { // FIXME! Up & Down, take into account also unbinned uncertainties!
    //std::cout << "Calculating rel uncert ^2 of SF table..." << std::endl;
    double relUncertSquared = 0.0;
    size_t i = 0;
    while (i < fPtBins.size()) {
      relUncertSquared += TMath::Power(fPerBinUncertaintyUp[i], 2);
      //std::cout << "   " << relUncertSquared << std::endl;
      i++;
    }
    return relUncertSquared;
  }



  // ================================== class EfficiencyTable ==================================
  BTagging::EfficiencyTable::EfficiencyTable() { }

  BTagging::EfficiencyTable::~EfficiencyTable() { }

  void BTagging::EfficiencyTable::setEfficiencyTable(const std::vector<double>& ptBinTable, const std::vector<double>& efficiencyTable, const std::vector<double>& uncertaintyUpTable, const std::vector<double>& uncertaintyDownTable) {
    fPtBins = ptBinTable;
    fEfficiency = efficiencyTable;
    fEffUncertUp = uncertaintyUpTable;
    fEffUncertDown = uncertaintyDownTable;
    initializeJetTable();
  }


  void BTagging::EfficiencyTable::initializeJetTable() {
    if (fPtBins.size() == 0) throw cms::Exception("LogicError")  << "Call BTagging::EfficiencyTable::initializeJetTable() AFTER adding data to the lookup-table!";
    size_t i = 0;
    while (i < fPtBins.size()) {
      fPerBinUncertaintyUp.push_back(0.0);
      fPerBinUncertaintyDown.push_back(0.0);
      i++;
    }
  }

  void BTagging::EfficiencyTable::addJetSFUncertaintyTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable) {
    if (isBTagged) return; // The uncertainty term due to the efficiency uncertainty for tagged jets is zero
    size_t i = obtainIndex(fPtBins, pT);
    double SF = sfTable.getScaleFactor(pT);
    fPerBinUncertaintyUp[i] += ((1.0 - SF) * fEffUncertUp[i]) / ((1.0 - SF * fEfficiency[i]) * (1.0 - fEfficiency[i]));
    fPerBinUncertaintyDown[i] += ((1.0 - SF) * fEffUncertDown[i]) / ((1.0 - SF * fEfficiency[i]) * (1.0 - fEfficiency[i]));
  }

  size_t BTagging::EfficiencyTable::obtainIndex(const std::vector<double>& table, double pt) {
    size_t myEnd = table.size();
    size_t myPos = 0;
    while (myPos < myEnd) {
      if (pt < table[myPos]) {
        if (myPos == 0)
          return 0; // should never happen
        else
          return myPos-1;
      }
      ++myPos;
    }
    return myEnd-1; // return last bin
  }

  double BTagging::EfficiencyTable::getEfficiency(double pT) const {
    return fEfficiency[obtainIndex(fPtBins, pT)];
  }

  double BTagging::EfficiencyTable::calculateRelativeUncertaintySquared() { // FIXME: up and down
    //std::cout << "Calculating rel uncert ^2 of efficiency table..." << std::endl;
    double relUncertSquared = 0.0;
    size_t i = 0;
    while (i < fPtBins.size()) {
      relUncertSquared += TMath::Power(fPerBinUncertaintyUp[i], 2);
      //std::cout << "   " << relUncertSquared << std::endl;
      i++;
    }
    return relUncertSquared;
  }

  // ================================== struct PerJetInfo ==================================
  void BTagging::PerJetInfo::addJetSFTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable, EfficiencyTable& effTable) {
    double eventScaleFactor = 1.0;
    if (isBTagged) {
      eventScaleFactor = sfTable.getScaleFactor(pT);
    } else {
      eventScaleFactor = (1.-sfTable.getScaleFactor(pT)*effTable.getEfficiency(pT)) / (1.-effTable.getEfficiency(pT));
    }
    fScaleFactor.push_back(eventScaleFactor);
  }
  


  // ================================== class BTagging ==================================
  BTagging::BTagging(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fDiscriminator(iConfig.getUntrackedParameter<std::string>("discriminator")),
    fLeadingDiscrCut(iConfig.getUntrackedParameter<double>("leadingDiscriminatorCut")),
    fSubLeadingDiscrCut(iConfig.getUntrackedParameter<double>("subleadingDiscriminatorCut")),
    fNumberOfBJets(iConfig.getUntrackedParameter<uint32_t>("jetNumber"),iConfig.getUntrackedParameter<std::string>("jetNumberCutDirection")),
    fVariationEnabled(iConfig.getUntrackedParameter<bool>("variationEnabled")),
    fVariationShiftBy(iConfig.getUntrackedParameter<double>("variationShiftBy")),
    fTaggedCount(eventCounter.addSubCounter("b-tagging main","b-tagging")),
    fAllSubCount(eventCounter.addSubCounter("b-tagging", "all jets")),
    fTaggedSubCount(eventCounter.addSubCounter("b-tagging", "tagged (leading discr. cut only)")),
    fTaggedPtCutSubCount(eventCounter.addSubCounter("b-tagging", "pt cut")),  
    fTaggedEtaCutSubCount(eventCounter.addSubCounter("b-tagging", "eta cut")),  
    fTaggedAllRealBJetsSubCount(eventCounter.addSubCounter("b-tagging", "All real b jets")),
    fTaggedTaggedRealBJetsSubCount(eventCounter.addSubCounter("b-tagging", "Btagged real b jets")),
    fTaggedNoTaggedJet(eventCounter.addSubCounter("b-tagging", "no b-tagged jet")),
    fTaggedOneTaggedJet(eventCounter.addSubCounter("b-tagging", "one b-tagged jet")),
    fTaggedTwoTaggedJets(eventCounter.addSubCounter("b-tagging", "two b-tagged jets")),
    allJetsCount2(eventCounter.addSubCounter("allJetsCount2", "All jets")),
    genuineBJetsCount2(eventCounter.addSubCounter("genuineBJetsCount2", "All b-jets")),
    genuineBJetsWithBTagCount2(eventCounter.addSubCounter("genuineBJetsWithBTagCount2", "All b-jets with b-tag"))
    //    fTaggedEtaCutSubCount(eventCounter.addSubCounter("b-tagging", "eta  cut")),
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("Btagging");
    hDiscriminator = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_bdiscriminator", ("b discriminator "+fDiscriminator).c_str(), 100, -10, 10);
    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet_pt", "bjet_pt", 100, 0., 500.);
    hDiscriminatorB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "RealBjet_discrim", ("realm b discrimi. "+fDiscriminator).c_str(), 100, -10, 10); // STR: Currently not used
    hPtBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_pt", "realbjetCSVM_pt", 100, 0., 500.);
    hEtaBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_eta", "realbjetCSVM_eta", 100, -5., 5.);
    hPtBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_pt", "realbjetCSVT_pt", 100, 0., 500.);
    hEtaBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_eta", "realbjetCSVT_eta", 100, -5., 5.);
    hPtBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_pt", "realbjetNotag_pt", 100, 0., 500.);
    hEtaBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_eta", "realbjetNotag_eta", 100, -5., 5.);
    hDiscriminatorQ = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "RealQjet_discrim", ("realm b discrimi. "+fDiscriminator).c_str(), 100, -10, 10); // STR: Currently not used
    hPtQCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVM_pt", "realqjetCSVM_pt", 100, 0., 500.);
    hEtaQCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVM_eta", "realqjetCSVM_pt", 100, -5., 5.);
    hPtQCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVT_pt", "realqjetCSVT_pt", 100, 0., 500.);
    hEtaQCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVT_eta", "realqjetCSVT_pt", 100, -5., 5.);
    hPtQnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetNotag_pt", "realqjetNotag_pt", 100, 0., 500.);
    hEtaQnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetNotag_eta", "realqjetNotag_pt", 100, -5., 5.);
    hPt1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet1_pt", "bjet1_pt", 100, 0., 500.);
    hPt2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet2_pt", "bjet2_pt", 100, 0., 500.);
    hEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet_eta", "bjet_pt", 100, -5., 5.);
    hEta1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet1_eta", "bjet1_pt", 100, -5., 5.);
    hEta2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet2_eta", "bjet2_pt", 100, -5., 5.);
    hNumberOfBtaggedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfBtaggedJets", "NumberOfBtaggedJets", 10, 0., 10.);
    hNumberOfBtaggedJetsIncludingSubLeading = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfBtaggedJetsIncludingSubLeading", "NumberOfBtaggedJetsIncludingSubLeading", 10, 0., 10.);
    hMCMatchForPassedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MCMatchForPassedJets", "MCMatchForPassedJets;;N_{jets}", 3, 0., 3.);
    if (hMCMatchForPassedJets->isActive()) {
      hMCMatchForPassedJets->GetXaxis()->SetBinLabel(1, "b jet");
      hMCMatchForPassedJets->GetXaxis()->SetBinLabel(2, "light jet");
      hMCMatchForPassedJets->GetXaxis()->SetBinLabel(3, "no match");
    }

    // MC btagging and mistagging efficiency
    TFileDirectory myMCEffDir = myDir.mkdir("MCEfficiency");
    hMCAllBJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "AllBJetsByPt", "AllBJetsByPt;b jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCAllCJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "AllCJetsByPt", "AllCJetsByPt;c jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCAllLightJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "AllLightJetsByPt", "AllLightJetsByPt;udsg jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCBtaggedBJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "TaggedBJetsByPt", "TaggedBJetsByPt;b jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCBtaggedCJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "TaggedCJetsByPt", "TaggedCJetsByPt;c jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCBtaggedLightJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "TaggedLightJetsByPt", "TaggedLightJetsByPt;udsg jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCBmistaggedBJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "MistaggedBJetsByPt", "MistaggedBJetsByPt;b jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCBmistaggedCJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "MistaggedCJetsByPt", "MistaggedCJetsByPt;c jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);
    hMCBmistaggedLightJetsByPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMCEffDir, "MistaggedLightJetsByPt", "MistaggedLightJetsByPt;udsg jets p_{T}, GeV/c;N_{jets}", 50, 0., 500.);

    hMCAllBJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "AllBJetsByPtAndEta", "AllBJetsByPtAndEta;b jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCAllCJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "AllCJetsByPtAndEta", "AllCJetsByPtAndEta;c jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCAllLightJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "AllLightJetsByPtAndEta", "AllLightJetsByPtAndEta;udsg jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCBtaggedBJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "TaggedBJetsByPtAndEta", "TaggedBJetsByPtAndEta;b jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCBtaggedCJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "TaggedCJetsByPtAndEta", "TaggedCJetsByPtAndEta;c jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCBtaggedLightJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "TaggedLightJetsByPtAndEta", "TaggedLightJetsByPtAndEta;udsg jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCBmistaggedBJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "MistaggedBJetsByPtAndEta", "MistaggedBJetsByPtAndEta;b jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCBmistaggedCJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "MistaggedCJetsByPtAndEta", "MistaggedCJetsByPtAndEta;c jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);
    hMCBmistaggedLightJetsByPtAndEta = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myMCEffDir, "MistaggedLightJetsByPtAndEta", "MistaggedLightJetsByPtAndEta;udsg jets p_{T}, GeV/c;jet #eta", 50, 0., 500., 10, -2.5, 2.5);

    // Scale factor histograms (needed for evaluating syst. uncertainty of btagging in datacard generator)
    hScaleFactor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "scaleFactor", "scaleFactor;b-tag/mistag scale factor;N_{events}/0.05", 100, 0., 5.);
    hBTagRelativeUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "BTagRelativeUncertainty", "BTagRelativeUncertainty;Relative Uncertainty;N_{events}", 3000, 0., 3.);
    hBTagAbsoluteUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "BTagAbsoluteUncertainty", "BTagAbsoluteUncertainty;Absolute Uncertainty;N_{events}", 3000, 0., 3.);

    // Set scale factor and efficiency look-up tables and functions
    if (fLeadingDiscrCut > 0.243 && fLeadingDiscrCut < 0.245) { // CSVL (Combined Secondary Vertex b-tagging method, Loose working point)
      fTagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVL::SFb, toVector(CSVL::SFb_error));
      fMistagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVL::SFb, toVector(CSVL::SFb_error));
      fTagEffTable.setEfficiencyTable(toVector(CSVL::ptBinLowEdges_BtoB), toVector(CSVL::eff_BtoB), toVector(CSVL::effUncertainty_BtoB), toVector(CSVL::effUncertainty_BtoB));
      fCMistagEffTable.setEfficiencyTable(toVector(CSVL::ptBinLowEdges_BtoB), toVector(CSVL::eff_GtoB), toVector(CSVL::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
      fGMistagEffTable.setEfficiencyTable(toVector(CSVL::ptBinLowEdges_BtoB), toVector(CSVL::eff_GtoB), toVector(CSVL::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
      fUDSMistagEffTable.setEfficiencyTable(toVector(CSVL::ptBinLowEdges_BtoB), toVector(CSVL::eff_GtoB), toVector(CSVL::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
    } else if (fLeadingDiscrCut > 0.678 && fLeadingDiscrCut < 0.680) { // CSVM (Combined Secondary Vertex b-tagging method, Medium working point)
      fTagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVM::SFb, toVector(CSVM::SFb_error));
      fMistagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVM::SFb, toVector(CSVM::SFb_error));
      fTagEffTable.setEfficiencyTable(toVector(CSVM::ptBinLowEdges_BtoB), toVector(CSVM::eff_BtoB), toVector(CSVM::effUncertainty_BtoB), toVector(CSVL::effUncertainty_BtoB));
      fCMistagEffTable.setEfficiencyTable(toVector(CSVM::ptBinLowEdges_BtoB), toVector(CSVM::eff_GtoB), toVector(CSVM::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
      fGMistagEffTable.setEfficiencyTable(toVector(CSVM::ptBinLowEdges_BtoB), toVector(CSVM::eff_GtoB), toVector(CSVM::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
      fUDSMistagEffTable.setEfficiencyTable(toVector(CSVM::ptBinLowEdges_BtoB), toVector(CSVM::eff_GtoB), toVector(CSVM::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
    } else if (fLeadingDiscrCut > 0.897 && fLeadingDiscrCut < 0.899) { // CSVT (Combined Secondary Vertex b-tagging method, Tight working point)
      fTagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVT::SFb, toVector(CSVT::SFb_error));
      fMistagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVT::SFb, toVector(CSVT::SFb_error));
      fTagEffTable.setEfficiencyTable(toVector(CSVT::ptBinLowEdges_BtoB), toVector(CSVT::eff_BtoB), toVector(CSVT::effUncertainty_BtoB), toVector(CSVL::effUncertainty_BtoB));
      fCMistagEffTable.setEfficiencyTable(toVector(CSVT::ptBinLowEdges_BtoB), toVector(CSVT::eff_GtoB), toVector(CSVT::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
      fGMistagEffTable.setEfficiencyTable(toVector(CSVT::ptBinLowEdges_BtoB), toVector(CSVT::eff_GtoB), toVector(CSVT::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
      fUDSMistagEffTable.setEfficiencyTable(toVector(CSVT::ptBinLowEdges_BtoB), toVector(CSVT::eff_GtoB), toVector(CSVT::effUncertainty_GtoB), toVector(CSVL::effUncertainty_GtoB));
    } else {
      throw cms::Exception("LogicError")  << "The given b-tagging discriminator value does not correspond to any known working point!";
    }
  }

  BTagging::~BTagging() {}

  BTagging::Data BTagging::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return privateAnalyze(iEvent, iSetup, jets);
  }

  BTagging::Data BTagging::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets);
  }

  BTagging::Data BTagging::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets) {
    //std::cout << "****************" << fTagSFTable.getNumberOfBins() << std::endl;
    
    // Initialize output data object
    Data output;
    output.fSelectedJets.reserve(jets.size());
    output.fSelectedSubLeadingJets.reserve(jets.size());
    // Initialize structure for collecting information (scale factor & uncertainty, tagging status, etc.) of each jet.
    PerJetInfo bTaggingInfo;
    bTaggingInfo.reserve(jets.size());

    // Loop over all jets in event
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      //std::cout << "Current jet flavour and pT: " << std::abs(iJet->partonFlavour()) << ", " << iJet->pt() << std::endl;

      // Initialize flags
      bool isGenuineB = false;
      bool isBTagged = false;

      increment(fAllSubCount);

      // In MC, check if the jet is from a b-quark
      if (!iEvent.isRealData()) {
	if (std::abs(iJet->partonFlavour()) == 5) {
	    isGenuineB = true;
	    increment(fTaggedAllRealBJetsSubCount); // STR: why "Tagged"? No tagging has been done yet!
	}
      }

      // Apply transverse momentum cut
      if(iJet->pt() < fPtCut) continue;
      increment(fTaggedPtCutSubCount); // STR: why "Tagged"? No tagging has been done yet!

      // Apply pseudorapidity cut
      if(fabs(iJet->eta()) > fEtaCut) continue;
      increment(fTaggedEtaCutSubCount); // STR: why "Tagged"? No tagging has been done yet!

      // Do b-tagging using the chosen discriminator and working point
      float discr = iJet->bDiscriminator(fDiscriminator);
      hDiscriminator->Fill(discr);
      if (discr > fLeadingDiscrCut) {
        output.fSelectedJets.push_back(iJet);
	isBTagged = true;
	increment(fTaggedSubCount);
	if (isGenuineB) increment(fTaggedTaggedRealBJetsSubCount); // STR: "TaggedTagged"?!
	hPt->Fill(iJet->pt());
	hEta->Fill(iJet->eta());
	//std::cout << "Jet is b-tagged" << std::endl;
      } else if (discr > fSubLeadingDiscrCut) {
        output.fSelectedSubLeadingJets.push_back(iJet);
      }
      if (discr > output.fMaxDiscriminatorValue) output.fMaxDiscriminatorValue = discr;

      // If MC, calculate the jet's contribution to the event scale factor
      if (!iEvent.isRealData()) {
	calculateJetSFAndUncertaintyTerm(iJet, isBTagged, bTaggingInfo, fTagSFTable, fMistagSFTable, fTagEffTable, fCMistagEffTable, fGMistagEffTable, fUDSMistagEffTable);
	bTaggingInfo.fTagged.push_back(isBTagged);
	bTaggingInfo.fGenuine.push_back(isGenuineB);
      }
    } // End of jet loop

    // Calculate scale factor and its uncertainty for MC events
    if (!iEvent.isRealData()) setEventScaleFactorInfo(bTaggingInfo, fTagSFTable, fMistagSFTable, fTagEffTable, fCMistagEffTable, fGMistagEffTable, fUDSMistagEffTable, output);

    // Do histogramming and set output
    hNumberOfBtaggedJets->Fill(output.fSelectedJets.size());
    hNumberOfBtaggedJetsIncludingSubLeading->Fill(output.fSelectedJets.size()+output.fSelectedSubLeadingJets.size());
    output.iNBtags = output.fSelectedJets.size();
    if(output.fSelectedJets.size() > 0) {
      hPt1->Fill(output.fSelectedJets[0]->pt());
      hEta1->Fill(output.fSelectedJets[0]->eta());
    }
    if(output.fSelectedJets.size() > 1) {
      hPt2->Fill(output.fSelectedJets[1]->pt());
      hEta2->Fill(output.fSelectedJets[1]->eta());
    }
    if(output.fSelectedJets.size() == 0) increment(fTaggedNoTaggedJet);
    else if(output.fSelectedJets.size() == 1) increment(fTaggedOneTaggedJet);
    else if(output.fSelectedJets.size() == 2) increment(fTaggedTwoTaggedJets);

    output.fPassedEvent= fNumberOfBJets.passedCut(output.fSelectedJets.size());
    if (output.fPassedEvent)
      increment(fTaggedCount);

    return output;
  }

  void BTagging::calculateJetSFAndUncertaintyTerm(edm::Ptr<pat::Jet>& iJet, bool isBTagged, PerJetInfo& info, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) const {
    // Get jet information
    int flavour = std::abs(iJet->partonFlavour());
    double pt = iJet->pt();
    
    //std::cout << "Weight calculation jet flavour and pT: " << flavour << ", " << pt << std::endl;

    // Set flags
    bool isGenuineB = false, isGenuineC = false, isGenuineG = false, isGenuineUDS = false;
    if      (flavour == 5) isGenuineB = true;
    else if (flavour == 4) isGenuineC = true;
    else if (flavour == 21) isGenuineG = true;
    else    isGenuineUDS = true;

    // Calculate the jet weight according to the properties (flavour, momentum, etc.) of the jet and the tagging status
    if (isGenuineB) {
      info.addJetSFTerm(pt, isBTagged, sfTag, effTag);
      sfTag.addJetSFUncertaintyTerm(pt, isBTagged, effTag);
      effTag.addJetSFUncertaintyTerm(pt, isBTagged, sfTag);
    }
    else if (isGenuineC) {
      info.addJetSFTerm(pt, isBTagged, sfTag, effCMistag);
      sfTag.addJetSFUncertaintyTerm(pt, isBTagged, effCMistag, 2.0); // c-jets use b-jet scale factors with double uncertainty
      effCMistag.addJetSFUncertaintyTerm(pt, isBTagged, sfTag);
    }
    else if (isGenuineG) {
      info.addJetSFTerm(pt, isBTagged, sfMistag, effGMistag);
      sfMistag.addJetSFUncertaintyTerm(pt, isBTagged, effGMistag);
      effGMistag.addJetSFUncertaintyTerm(pt, isBTagged, sfMistag);
    }
    else if (isGenuineUDS) {
      info.addJetSFTerm(pt, isBTagged, sfMistag, effUDSMistag);
      sfMistag.addJetSFUncertaintyTerm(pt, isBTagged, effUDSMistag);
      effUDSMistag.addJetSFUncertaintyTerm(pt, isBTagged, sfMistag);
    }
  }

  double BTagging::calculateEventScaleFactor(PerJetInfo& bTaggingInfo) {
    //std::cout << "Calculating event SF..." << std::endl;
    //std::cout << "   Number of entries in bTaggingInfo.fScaleFactor: " << bTaggingInfo.fScaleFactor.size() << std::endl;
    double eventScaleFactor = 1.0;
    size_t i = 0;
    while (i < bTaggingInfo.fScaleFactor.size()) {
      eventScaleFactor *= bTaggingInfo.fScaleFactor[i];
      //std::cout << "_" << bTaggingInfo.fScaleFactor[i] << std::endl;
      //std::cout << "   " << eventScaleFactor << std::endl;
      i++;
    }
    return eventScaleFactor;
  }

  double BTagging::calculateRelativeEventScaleFactorUncertainty(ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) {
    //std::cout << "Calculaing relative uncertainty of event scale factor... " << std::endl;
    double relUncertSquared = 0.0;
    relUncertSquared += sfTag.calculateRelativeUncertaintySquared();
    //std::cout << "sfTag.calculateRelativeUncertaintySquared() " << sfTag.calculateRelativeUncertaintySquared() << std::endl;
    relUncertSquared += sfMistag.calculateRelativeUncertaintySquared();
    //std::cout << "sfMistag.calculateRelativeUncertaintySquared() " << sfMistag.calculateRelativeUncertaintySquared() << std::endl;
    relUncertSquared += effTag.calculateRelativeUncertaintySquared();
    //std::cout << "effTag.calculateRelativeUncertaintySquared() " << effTag.calculateRelativeUncertaintySquared() << std::endl;
    relUncertSquared += effCMistag.calculateRelativeUncertaintySquared();
    //std::cout << "effCMistag.calculateRelativeUncertaintySquared() " << effCMistag.calculateRelativeUncertaintySquared() << std::endl; 
    relUncertSquared += effGMistag.calculateRelativeUncertaintySquared();
    //std::cout << "effGMistag.calculateRelativeUncertaintySquared() " << effGMistag.calculateRelativeUncertaintySquared() << std::endl; 
    relUncertSquared += effUDSMistag.calculateRelativeUncertaintySquared();
    //std::cout << "effUDSMistag.calculateRelativeUncertaintySquared() " << effUDSMistag.calculateRelativeUncertaintySquared() << std::endl;
    //std::cout << "Uncertainty squared is: " << relUncertSquared << std::endl;
    //std::cout << "UNCERTAINTY IS: " << TMath::Sqrt(relUncertSquared) << std::endl;
    return TMath::Sqrt(relUncertSquared);
  }

  void BTagging::setEventScaleFactorInfo(PerJetInfo& bTaggingInfo, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag, BTagging::Data& output) {
    output.fEventScaleFactor = calculateEventScaleFactor(bTaggingInfo);
    output.fEventScaleFactorRelativeUncertainty = calculateRelativeEventScaleFactorUncertainty(sfTag, sfMistag, effTag, effCMistag, effGMistag, effUDSMistag);
    output.fEventScaleFactorAbsoluteUncertainty = output.fEventScaleFactorRelativeUncertainty * output.fEventScaleFactor;

    //std::cout << "Event weight: " << output.fEventScaleFactor << std::endl;
    //std::cout << "Event weight rel uncert: " << output.fEventScaleFactorRelativeUncertainty << std::endl;
    //std::cout << "Event weight abs uncert: " << output.fEventScaleFactorAbsoluteUncertainty << std::endl;

    // Do the variation, if asked
    if(fVariationEnabled) {
      output.fEventScaleFactor += fVariationShiftBy * output.fEventScaleFactorAbsoluteUncertainty;
      // These are meaningless after the variation:
      output.fEventScaleFactorAbsoluteUncertainty = 0;
      output.fEventScaleFactorRelativeUncertainty = 0;
    }
  }

  // Method called from SignalAnalysis.cc:
  void BTagging::fillScaleFactorHistograms(BTagging::Data& data) {
    hScaleFactor->Fill(data.getScaleFactor());
    hBTagAbsoluteUncertainty->Fill(data.getScaleFactorAbsoluteUncertainty());
    hBTagRelativeUncertainty->Fill(data.getScaleFactorRelativeUncertainty());
  }
}
