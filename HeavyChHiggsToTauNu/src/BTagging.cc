/*
  PURPOSE
  Loop over jets in event and apply a b-tagging discriminator. If an event contains at least one b-tagged jet, it will be flagged as having passed.
  If the event is MC, an event scale factor is calculated using per-jet scale factors and MC tagging efficiencies. The scale factors come from a
  database maintained by the B-tagging & Vertexing POG and the efficiencies are measured by us (see BTaggingEfficiencyInMC.cc). Both are hard-coded
  into this file. The event weight is multiplied with the event scale factor (in the main analysis file, e.g. SignalAnalysis.cc).
*/
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
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
  bool printValidationOutput = false;
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
  namespace EffBins {
    double bins_B[] = {20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 200, 250, 300, 350, 400};
    double bins_C[] = {20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 200, 250, 300, 350, 400};
    double bins_G[] = {20, 30, 60, 100, 150, 250};
    double bins_UDS[] = {20, 30, 60, 100, 150, 250};
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
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_BtoB_byPt[] = {0.000000, 0.843692, 0.841796, 0.847828, 0.848339, 0.851303, 0.848301, 0.847911, 0.849353, 0.853927, 0.849528, 0.844153, 0.819833, 0.827717, 0.776372, 0.758767, 0.631211};
    double effUncertUp_BtoB_byPt[] = {0.000000, 0.004269, 0.004465, 0.004706, 0.005054, 0.005428, 0.005960, 0.006454, 0.005105, 0.005941, 0.007159, 0.006879, 0.010042, 0.015658, 0.027454, 0.040231, 0.045057};
    double effUncertDown_BtoB_byPt[] = {0.000000, 0.004269, 0.004465, 0.004706, 0.005054, 0.005428, 0.005960, 0.006454, 0.005105, 0.005941, 0.007159, 0.006879, 0.010042, 0.015658, 0.027454, 0.040231, 0.045057};
    // C->B efficiencies
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_CtoB_byPt[] = {0.000000, 0.512153, 0.435582, 0.431783, 0.437036, 0.401122, 0.398187, 0.387372, 0.405418, 0.403269, 0.365568, 0.394243, 0.429448, 0.358584, 0.301526, 0.313177, 0.299944};
    double effUncertUp_CtoB_byPt[] = {0.000000, 0.012331, 0.013119, 0.013576, 0.014845, 0.015599, 0.016915, 0.018294, 0.014104, 0.016224, 0.019251, 0.017779, 0.024536, 0.034436, 0.048572, 0.059639, 0.055166};
    double effUncertDown_CtoB_byPt[] = {0.000000, 0.012331, 0.013119, 0.013576, 0.014845, 0.015599, 0.016915, 0.018294, 0.014104, 0.016224, 0.019251, 0.017779, 0.024536, 0.034436, 0.048572, 0.059639, 0.055166};
    // G->B efficiencies
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_GtoB_byPt[] = {0.000000, 0.188206, 0.110660, 0.081346, 0.095621, 0.088693};
    double effUncertUp_GtoB_byPt[] = {0.000000, 0.003294, 0.003748, 0.004439, 0.006072, 0.009871};
    double effUncertDown_GtoB_byPt[] = {0.000000, 0.003294, 0.003748, 0.004439, 0.006072, 0.009871};
    // UDS->B efficiencies
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_UDStoB_byPt[] = {0.000000, 0.166084, 0.097383, 0.087873, 0.111919, 0.121946};
    double effUncertUp_UDStoB_byPt[] = {0.000000, 0.003238, 0.003002, 0.003560, 0.004863, 0.008440};
    double effUncertDown_UDStoB_byPt[] = {0.000000, 0.003238, 0.003002, 0.003560, 0.004863, 0.008440};
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
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_BtoB_byPt[] = {0.000000, 0.605497, 0.660818, 0.696156, 0.717718, 0.721635, 0.725644, 0.733542, 0.742611, 0.754529, 0.733295, 0.720926, 0.693444, 0.666824, 0.606797, 0.570024, 0.427823};
    double effUncertUp_BtoB_byPt[] = {0.000000, 0.005743, 0.005794, 0.006011, 0.006346, 0.006841, 0.007410, 0.007930, 0.006243, 0.007234, 0.008858, 0.008525, 0.012013, 0.019713, 0.032342, 0.046238, 0.046291};
    double effUncertDown_BtoB_byPt[] = {0.000000, 0.005743, 0.005794, 0.006011, 0.006346, 0.006841, 0.007410, 0.007930, 0.006243, 0.007234, 0.008858, 0.008525, 0.012013, 0.019713, 0.032342, 0.046238, 0.046291};
    // C->B efficiencies
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_CtoB_byPt[] = {0.000000, 0.176809, 0.172700, 0.175568, 0.202081, 0.198587, 0.187493, 0.215256, 0.203682, 0.214922, 0.214593, 0.216126, 0.214556, 0.193903, 0.122043, 0.143678, 0.126606};
    double effUncertUp_CtoB_byPt[] = {0.000000, 0.009417, 0.009991, 0.010394, 0.012058, 0.012682, 0.013441, 0.015478, 0.011531, 0.013545, 0.016377, 0.015065, 0.020521, 0.028282, 0.034813, 0.044718, 0.040161};
    double effUncertDown_CtoB_byPt[] = {0.000000, 0.009417, 0.009991, 0.010394, 0.012058, 0.012682, 0.013441, 0.015478, 0.011531, 0.013545, 0.016377, 0.015065, 0.020521, 0.028282, 0.034813, 0.044718, 0.040161};
    // G->B efficiencies
    // From W+jets (WJets) sample with Rtau cut deactivated
    double eff_GtoB_byPt[] = {0.000000, 0.016194, 0.017898, 0.014332, 0.016984, 0.021557};
    double effUncertUp_GtoB_byPt[] = {0.000000, 0.001065, 0.001611, 0.001938, 0.002675, 0.004955};
    double effUncertDown_GtoB_byPt[] = {0.000000, 0.001065, 0.001611, 0.001938, 0.002675, 0.004955};
    // UDS->B efficiencies
    // From W+jets (WJets) sample with Rtau cut deactivated
    double eff_UDStoB_byPt[] = {0.000000, 0.011731, 0.012522, 0.011719, 0.013914, 0.020363};
    double effUncertUp_UDStoB_byPt[] = {0.000000, 0.000935, 0.001128, 0.001334, 0.001789, 0.003645};
    double effUncertDown_UDStoB_byPt[] = {0.000000, 0.000935, 0.001128, 0.001334, 0.001789, 0.003645};
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
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_BtoB_byPt[] = {0.000000, 0.458483, 0.518979, 0.553481, 0.571330, 0.579789, 0.577360, 0.560711, 0.559940, 0.580829, 0.526322, 0.464904, 0.426719, 0.352917, 0.275715, 0.266566, 0.168526};
    double effUncertUp_BtoB_byPt[] = {0.000000, 0.005856, 0.006119, 0.006500, 0.006984, 0.007535, 0.008196, 0.008910, 0.007097, 0.008298, 0.009980, 0.009487, 0.012849, 0.019915, 0.029559, 0.041264, 0.035311};
    double effUncertDown_BtoB_byPt[] = {0.000000, 0.005856, 0.006119, 0.006500, 0.006984, 0.007535, 0.008196, 0.008910, 0.007097, 0.008298, 0.009980, 0.009487, 0.012849, 0.019915, 0.029559, 0.041264, 0.035311};
    // C->B efficiencies
    // From ttbar (TTJets) sample with Rtau cut deactivated
    double eff_CtoB_byPt[] = {0.000000, 0.059786, 0.053019, 0.068237, 0.058548, 0.059453, 0.063899, 0.048850, 0.047686, 0.056202, 0.047481, 0.040659, 0.042219, 0.027147, 0.000000, 0.031319, 0.028526};
    double effUncertUp_CtoB_byPt[] = {0.000000, 0.005852, 0.005966, 0.006897, 0.007087, 0.007513, 0.008420, 0.008020, 0.006123, 0.007539, 0.008558, 0.007140, 0.009909, 0.011899, 0.000000, 0.021816, 0.019897};
    double effUncertDown_CtoB_byPt[] = {0.000000, 0.005852, 0.005966, 0.006897, 0.007087, 0.007513, 0.008420, 0.008020, 0.006123, 0.007539, 0.008558, 0.007140, 0.009909, 0.011899, 0.000000, 0.021816, 0.019897};
    // G->B efficiencies
    // From W+jets (WJets) sample with Rtau cut deactivated
    double eff_GtoB_byPt[] = {0.000000, 0.003232, 0.001569, 0.000304, 0.001146, 0.002640};
    double effUncertUp_GtoB_byPt[] = {0.000000, 0.000491, 0.000478, 0.000244, 0.000673, 0.001866};
    double effUncertDown_GtoB_byPt[] = {0.000000, 0.000491, 0.000478, 0.000244, 0.000673, 0.001866};
    // UDS->B efficiencies
    // From W+jets (WJets) sample with Rtau cut deactivated
    double eff_UDStoB_byPt[] = {0.000000, 0.002185, 0.001140, 0.001492, 0.000834, 0.001265};
    double effUncertUp_UDStoB_byPt[] = {0.000000, 0.000415, 0.000354, 0.000498, 0.000441, 0.000895};
    double effUncertDown_UDStoB_byPt[] = {0.000000, 0.000415, 0.000354, 0.000498, 0.000441, 0.000895};
  }


  // ================================== class Data ==================================
  BTagging::Data::Data():
    fPassedEvent(false),
    iNBtags(-1),
    fMaxDiscriminatorValue(-999.0),
    fEventScaleFactor(1.0),
    fEventSFAbsUncert_up(0.0),
    fEventSFAbsUncert_down(0.0),
    fEventSFRelUncert_up(0.0),
    fEventSFRelUncert_down(0.0),
    fEventSFAbsUncert_max(0.0)
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
  BTagging::ScaleFactorTable::ScaleFactorTable() :
    fScaleFactorFunction(0), fScaleFactorUncertUpFunction(0), fScaleFactorUncertDownFunction(0)
  {}

  BTagging::ScaleFactorTable::~ScaleFactorTable() {
    delete fScaleFactorFunction;
    delete fScaleFactorUncertUpFunction;
    delete fScaleFactorUncertDownFunction;
  }
  
  void BTagging::ScaleFactorTable::setScaleFactorTable(const std::vector<double>& ptBinTable, const char* SFFunctionExpression, const std::vector<double>& uncertaintyTable) {
    fPtBins = ptBinTable;
    setScaleFactorFunction(SFFunctionExpression);
    fScaleFactorUncertainty = uncertaintyTable;
    size_t NBins = fPtBins.size();
    fPerBinUncertaintyUp.reserve(NBins);
    fPerBinUncertaintyDown.reserve(NBins);
    size_t i = 0;
    while (i < NBins) {
      fPerBinUncertaintyUp.push_back(0.0);
      fPerBinUncertaintyDown.push_back(0.0);
      i++;
    }
  }

  void BTagging::ScaleFactorTable::setScaleFactorTable(TF1* scaleFactorFunction, TF1* sfUncertUpFunction, TF1* sfUncertDownFunction) {
    fScaleFactorFunction = new TF1(*scaleFactorFunction);
    fScaleFactorUncertUpFunction = new TF1(*sfUncertUpFunction);
    fScaleFactorUncertDownFunction = new TF1(*sfUncertDownFunction);
  }

  void BTagging::ScaleFactorTable::resetJetTable() {
    size_t i = 0;
    while (i < fPtBins.size()) {
      fPerBinUncertaintyUp[i] = 0.0;
      fPerBinUncertaintyDown[i] = 0.0;
      i++;
    }
    fUnbinnedUncertaintyUp.clear();
    fUnbinnedUncertaintyDown.clear();
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
      sfUncertUp = fScaleFactorUncertUpFunction->Eval(pT); // Careful, this is a relative uncertainty!
      sfUncertDown = fScaleFactorUncertDownFunction->Eval(pT); // Careful, this is a relative uncertainty!
      if (isBTagged) {
	fUnbinnedUncertaintyUp.push_back(factor * sfUncertUp);
	fUnbinnedUncertaintyDown.push_back(factor * sfUncertDown);
      } else {
	fUnbinnedUncertaintyUp.push_back(-(factor * eff * SF * sfUncertUp) / (1.0 - eff * SF));
	fUnbinnedUncertaintyDown.push_back(-factor * (eff * SF * sfUncertDown) / (1.0 - eff * SF));
      }
    }
    // BINNED UNCERTAINTIES:
    else if (fScaleFactorUncertainty.size() > 0) { // one vector of binned uncertainties given (lower and upper are equal)
      sfUncertUp = getScaleFactorUncertaintyBinned(pT);
      sfUncertDown = getScaleFactorUncertaintyBinned(pT);
      size_t i = obtainIndex(fPtBins, pT);
      if (isBTagged) {
	fPerBinUncertaintyUp[i] += factor * sfUncertUp;
	fPerBinUncertaintyDown[i] += factor * sfUncertDown;
      } else {
	fPerBinUncertaintyUp[i] += -(factor * eff * SF * sfUncertUp) / (1.0 - eff * SF);
	fPerBinUncertaintyDown[i] += -(factor * eff * SF * sfUncertDown) / (1.0 - eff * SF);
      }
    }
    else throw cms::Exception("LogicError")  << "Please provide two functions OR one vector of b-tagging SF upper and lower uncertainties! (Or implement using a different combination.)";
  }
  
  void BTagging::ScaleFactorTable::addJetSFUncertaintyTerm(double pT, bool isBTagged, EfficiencyTable& effTable) {
    addJetSFUncertaintyTerm(pT, isBTagged, effTable, 1.0);
  }
  
  size_t BTagging::ScaleFactorTable::obtainIndex(const std::vector<double>& table, double pT) {
    size_t myEnd = table.size();
    size_t myPos = 0;
    while (myPos < myEnd) {
      if (pT < table[myPos]) {
        if (myPos == 0)
          return 0; // should never happen
        else
          return myPos-1;
      }
      ++myPos;
    }
    return myEnd-1; // return last bin
  }

  double BTagging::ScaleFactorTable::getScaleFactor(double pT) const {
    if (fScaleFactorFunction) {
      return fScaleFactorFunction->Eval(pT);
    }
    else if (fScaleFactor.size() > 0) return fScaleFactor[obtainIndex(fPtBins, pT)];
    else throw cms::Exception("LogicError")  << "Neither parametrized function nor look-up table for b-tagging scale factor found! Either one must be given.";
  }

  double BTagging::ScaleFactorTable::getScaleFactorUncertaintyBinned(double pT) const {
    return fScaleFactorUncertainty[obtainIndex(fPtBins, pT)];
  }

  double BTagging::ScaleFactorTable::getMaximumUncertainty(double pT) const {
    if (fScaleFactorUncertUpFunction && fScaleFactorUncertDownFunction)
      return TMath::Max(fScaleFactorUncertUpFunction->Eval(pT), fScaleFactorUncertDownFunction->Eval(pT));
    else 
      return getScaleFactorUncertaintyBinned(pT);
  }

  double BTagging::ScaleFactorTable::calculateRelativeUncertaintySquared(bool up) {
    double relUncertSquared = 0.0;
    size_t i = 0;
    // Sum binned uncertainties:
    while (i < fPtBins.size()) {
      if (up) relUncertSquared += TMath::Power(fPerBinUncertaintyUp[i], 2);
      else  relUncertSquared += TMath::Power(fPerBinUncertaintyDown[i], 2);
      i++;
    }
    // Sum unbinned uncertainties:
    if (up) {
      for(std::vector<double>::const_iterator iterUncert = fUnbinnedUncertaintyUp.begin(); iterUncert != fUnbinnedUncertaintyUp.end(); ++iterUncert) {
	relUncertSquared += TMath::Power(*iterUncert, 2);
      }
    }
    else {
      for(std::vector<double>::const_iterator iterUncert = fUnbinnedUncertaintyDown.begin(); iterUncert != fUnbinnedUncertaintyDown.end(); ++iterUncert) {
	relUncertSquared += TMath::Power(*iterUncert, 2);
      }
    }
    return relUncertSquared;
  }

  void BTagging::ScaleFactorTable::printJetTableForValidation() {
    std::cout << "  fPerBinUncertaintyUp: {";
    size_t i = 0;
    while (i < fPtBins.size()) {
      std::cout << fPerBinUncertaintyUp[i] << ", ";
      i++;
    }
    std::cout << "}" << std::endl;
    std::cout << "  fPerBinUncertaintyDown: {";
    i = 0;
    while (i < fPtBins.size()) {
      std::cout << fPerBinUncertaintyDown[i] << ", ";
      i++;
    }
    std::cout << "}" << std::endl;
    std::cout << "  fUnbinnedUncertaintyUp: {";
    for(std::vector<double>::const_iterator iterUncert = fUnbinnedUncertaintyUp.begin(); iterUncert != fUnbinnedUncertaintyUp.end(); ++iterUncert) {
      std::cout << *iterUncert << ", ";
    }
    std::cout << "}" << std::endl;
    std::cout << "  fUnbinnedUncertaintyDown: {";
    for(std::vector<double>::const_iterator iterUncert = fUnbinnedUncertaintyDown.begin(); iterUncert != fUnbinnedUncertaintyDown.end(); ++iterUncert) {
      std::cout << *iterUncert << ", ";
    }
    std::cout << "}" << std::endl;
  }


  // ================================== class EfficiencyTable ==================================
  BTagging::EfficiencyTable::EfficiencyTable() { }

  BTagging::EfficiencyTable::~EfficiencyTable() { }

  void BTagging::EfficiencyTable::setEfficiencyTable(const std::vector<double>& ptBinTable, const std::vector<double>& efficiencyTable, const std::vector<double>& uncertaintyUpTable, const std::vector<double>& uncertaintyDownTable) {
    fPtBins = ptBinTable;
    fEfficiency = efficiencyTable;
    fEffUncertUp = uncertaintyUpTable;
    fEffUncertDown = uncertaintyDownTable;
    size_t NBins = fPtBins.size();
    fPerBinUncertaintyUp.reserve(NBins);
    fPerBinUncertaintyDown.reserve(NBins);
    size_t i = 0;
    while (i < NBins) {
      fPerBinUncertaintyUp.push_back(0.0);
      fPerBinUncertaintyDown.push_back(0.0);
      i++;
    }
  }

  void BTagging::EfficiencyTable::resetJetTable() {
    size_t i = 0;
    while (i < fPtBins.size()) {
      fPerBinUncertaintyUp[i] = 0.0;
      fPerBinUncertaintyDown[i] = 0.0;
      i++;
    }
  }

  void BTagging::EfficiencyTable::addJetSFUncertaintyTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable) {
    if (isBTagged) return; // The uncertainty term due to the efficiency uncertainty for tagged jets is zero
    size_t i = obtainIndex(fPtBins, pT);
    double SF = sfTable.getScaleFactor(pT);
    double eff = fEfficiency[i];
    // Careful, relative uncertainties have to be converted to absolute uncertainties!
    fPerBinUncertaintyUp[i] += ((1.0 - SF) * eff * fEffUncertUp[i]) / ((1.0 - SF * eff) * (1.0 - eff));
    fPerBinUncertaintyDown[i] += ((1.0 - SF) * eff * fEffUncertDown[i]) / ((1.0 - SF * eff) * (1.0 - eff));
  }

  size_t BTagging::EfficiencyTable::obtainIndex(const std::vector<double>& table, double pT) {
    size_t myEnd = table.size();
    size_t myPos = 0;
    while (myPos < myEnd) {
      if (pT < table[myPos]) {
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

  double BTagging::EfficiencyTable::getMaximumUncertainty(double pT) const {
    return TMath::Max(fEffUncertUp[obtainIndex(fPtBins, pT)], fEffUncertDown[obtainIndex(fPtBins, pT)]);
  }

  double BTagging::EfficiencyTable::calculateRelativeUncertaintySquared(bool up) {
    double relUncertSquared = 0.0;
    size_t i = 0;
    while (i < fPtBins.size()) {
      if (up) relUncertSquared += TMath::Power(fPerBinUncertaintyUp[i], 2);
      else  relUncertSquared += TMath::Power(fPerBinUncertaintyDown[i], 2);
      i++;
    }
    return relUncertSquared;
  }

  // ================================== struct EventSFTerms ==================================
  void BTagging::EventSFTerms::addJetSFTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable, EfficiencyTable& effTable) {
    double term = 1.0;
    if (isBTagged) {
      term = sfTable.getScaleFactor(pT);
    } else {
      term = (1.-sfTable.getScaleFactor(pT)*effTable.getEfficiency(pT)) / (1.-effTable.getEfficiency(pT));
    }
    if (printValidationOutput) std::cout << "  Event scale factor term: " << term << std::endl;
    SFTerms.push_back(term);
  }

  double BTagging::EventSFTerms::calculateEventScaleFactor() {
    double SF = 1.0;
    size_t i = 0;
    while (i < SFTerms.size()) {
      SF *= SFTerms[i];
      i++;
    }
    return SF;
  }

  // ================================== class BTagging ==================================
  BTagging::BTagging(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fDiscriminator(iConfig.getUntrackedParameter<std::string>("discriminator")),
    fLeadingDiscrCut(iConfig.getUntrackedParameter<double>("leadingDiscriminatorCut")),
    fSubLeadingDiscrCut(iConfig.getUntrackedParameter<double>("leadingDiscriminatorCut")),// Force subleading cut to be the same as leading cut, i.e. no asymmetry allowed
    //fSubLeadingDiscrCut(iConfig.getUntrackedParameter<double>("subleadingDiscriminatorCut")),
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
    TFileDirectory myDir = histoWrapper.mkdir(HistoWrapper::kInformative, *fs, "Btagging");
    hDiscriminator = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_bdiscriminator", ("b discriminator "+fDiscriminator).c_str(), 100, -10, 10);
    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet_pt", "bjet_pt", 100, 0., 500.);
    hPtBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_pt", "realbjetCSVM_pt", 100, 0., 500.);
    hEtaBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_eta", "realbjetCSVM_eta", 100, -5., 5.);
    hPtBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_pt", "realbjetCSVT_pt", 100, 0., 500.);
    hEtaBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_eta", "realbjetCSVT_eta", 100, -5., 5.);
    hPtBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_pt", "realbjetNotag_pt", 100, 0., 500.);
    hEtaBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_eta", "realbjetNotag_eta", 100, -5., 5.);
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
    TFileDirectory myMCEffDir = histoWrapper.mkdir(HistoWrapper::kInformative, myDir, "MCEfficiency");
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
      fMistagSFTable.setScaleFactorTable(CSVL::SFl, CSVL::SFl_max, CSVL::SFl_min);
      fTagEffTable.setEfficiencyTable(toVector(EffBins::bins_B), toVector(CSVL::eff_BtoB_byPt), toVector(CSVL::effUncertUp_BtoB_byPt), toVector(CSVL::effUncertDown_BtoB_byPt));
      fCMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_C), toVector(CSVL::eff_CtoB_byPt), toVector(CSVL::effUncertUp_CtoB_byPt), toVector(CSVL::effUncertDown_CtoB_byPt));
      fGMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_G), toVector(CSVL::eff_GtoB_byPt), toVector(CSVL::effUncertUp_GtoB_byPt), toVector(CSVL::effUncertDown_GtoB_byPt));
      fUDSMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_UDS), toVector(CSVL::eff_UDStoB_byPt), toVector(CSVL::effUncertUp_UDStoB_byPt), toVector(CSVL::effUncertDown_UDStoB_byPt));
    } else if (fLeadingDiscrCut > 0.678 && fLeadingDiscrCut < 0.680) { // CSVM (Combined Secondary Vertex b-tagging method, Medium working point)
      fTagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVM::SFb, toVector(CSVM::SFb_error));
      fMistagSFTable.setScaleFactorTable(CSVM::SFl, CSVM::SFl_max, CSVM::SFl_min);
      fTagEffTable.setEfficiencyTable(toVector(EffBins::bins_B), toVector(CSVM::eff_BtoB_byPt), toVector(CSVM::effUncertUp_BtoB_byPt), toVector(CSVM::effUncertDown_BtoB_byPt));
      fCMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_C), toVector(CSVM::eff_CtoB_byPt), toVector(CSVM::effUncertUp_CtoB_byPt), toVector(CSVM::effUncertDown_CtoB_byPt));
      fGMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_G), toVector(CSVM::eff_GtoB_byPt), toVector(CSVM::effUncertUp_GtoB_byPt), toVector(CSVM::effUncertDown_GtoB_byPt));
      fUDSMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_UDS), toVector(CSVM::eff_UDStoB_byPt), toVector(CSVM::effUncertUp_UDStoB_byPt), toVector(CSVM::effUncertDown_UDStoB_byPt));
    } else if (fLeadingDiscrCut > 0.897 && fLeadingDiscrCut < 0.899) { // CSVT (Combined Secondary Vertex b-tagging method, Tight working point)
      fTagSFTable.setScaleFactorTable(toVector(SFBins::ptmin), CSVT::SFb, toVector(CSVT::SFb_error));
      fMistagSFTable.setScaleFactorTable(CSVT::SFl, CSVT::SFl_max, CSVT::SFl_min);
      fTagEffTable.setEfficiencyTable(toVector(EffBins::bins_B), toVector(CSVT::eff_BtoB_byPt), toVector(CSVT::effUncertUp_BtoB_byPt), toVector(CSVT::effUncertDown_BtoB_byPt));
      fCMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_C), toVector(CSVT::eff_CtoB_byPt), toVector(CSVT::effUncertUp_CtoB_byPt), toVector(CSVT::effUncertDown_CtoB_byPt));
      fGMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_G), toVector(CSVT::eff_GtoB_byPt), toVector(CSVT::effUncertUp_GtoB_byPt), toVector(CSVT::effUncertDown_GtoB_byPt));
      fUDSMistagEffTable.setEfficiencyTable(toVector(EffBins::bins_UDS), toVector(CSVT::eff_UDStoB_byPt), toVector(CSVT::effUncertUp_UDStoB_byPt), toVector(CSVT::effUncertDown_UDStoB_byPt));
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
    if (printValidationOutput) std::cout << std::endl << "Start processing next event..." << std::endl;
    
    // Initialize output data object
    Data output;
    output.fDiscriminatorName = fDiscriminator;
    output.fSelectedJets.reserve(jets.size());
    output.fSelectedSubLeadingJets.reserve(jets.size());
    // Initialize structure for collecting event SF term of each jet
    EventSFTerms eventSFTerms;
    eventSFTerms.reserve(jets.size());
    // Initialize tables of per-jet SF uncertainties in look-up table objects
    fTagSFTable.resetJetTable();
    fMistagSFTable.resetJetTable();
    fTagEffTable.resetJetTable();
    fCMistagEffTable.resetJetTable();
    fGMistagEffTable.resetJetTable();
    fUDSMistagEffTable.resetJetTable();

    // Loop over all jets in event
    if (printValidationOutput) std::cout << "*** Begin looping over jets ***" << std::endl;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      if (printValidationOutput) std::cout << "Jet number " << iter - jets.begin() + 1 << " found. Flavour = " << std::abs(iJet->partonFlavour()) << ", pT = " << iJet->pt();

      // Initialize flags
      bool isGenuineB = false;
      bool isBTagged = false;

      increment(fAllSubCount);

      // In MC, check if the jet is from a b-quark
      if (!iEvent.isRealData()) {
	if (std::abs(iJet->partonFlavour()) == 5) {
	    isGenuineB = true;
	    increment(fTaggedAllRealBJetsSubCount);
	}
      }

      // Apply transverse momentum cut
      //if(iJet->pt() < fPtCut) continue; // disabled, jet pT is chosen in jet selection
      increment(fTaggedPtCutSubCount);

      // Apply pseudorapidity cut
      //if(fabs(iJet->eta()) > fEtaCut) continue; // disabled, jet eta is chosen in jet selection
      increment(fTaggedEtaCutSubCount);

      // Do b-tagging using the chosen discriminator and working point
      float discr = iJet->bDiscriminator(fDiscriminator);
      hDiscriminator->Fill(discr);
      if (discr > fLeadingDiscrCut) {
        output.fSelectedJets.push_back(iJet);
	isBTagged = true;
	if (printValidationOutput) std::cout << ", b-tagged" << std::endl;
	increment(fTaggedSubCount);
	if (isGenuineB) increment(fTaggedTaggedRealBJetsSubCount);
	hPt->Fill(iJet->pt());
	hEta->Fill(iJet->eta());
      } else if (discr > fSubLeadingDiscrCut) {
        output.fSelectedSubLeadingJets.push_back(iJet);
      }
      if (discr > output.fMaxDiscriminatorValue) output.fMaxDiscriminatorValue = discr;

      if (printValidationOutput && !isBTagged) std::cout << ", not b-tagged" << std::endl;

      // If MC, calculate the jet's contribution to the event scale factor
      if (!iEvent.isRealData()) {
	calculateJetSFAndUncertaintyTerm(iJet, isBTagged, eventSFTerms, fTagSFTable, fMistagSFTable, fTagEffTable, fCMistagEffTable, fGMistagEffTable, fUDSMistagEffTable);
// 	fBTaggingInfo.fTagged.push_back(isBTagged);
// 	fBTaggingInfo.fGenuine.push_back(isGenuineB);
      }
    } // End of jet loop
    if (printValidationOutput) std::cout << "*** Jet loop ended ***" << std::endl;

    if (printValidationOutput) {
      std::cout << "Uncertainty terms stored in the look-up table objects:" << std::endl;
      std::cout << "Tagging scale factor table" << std::endl;
      fTagSFTable.printJetTableForValidation();
      std::cout << "Mistagging scale factor table" << std::endl;
      fMistagSFTable.printJetTableForValidation();
    }

    // Calculate scale factor and its uncertainty for MC events
    if (!iEvent.isRealData()) setEventScaleFactorInfo(eventSFTerms, fTagSFTable, fMistagSFTable, fTagEffTable, fCMistagEffTable, fGMistagEffTable, fUDSMistagEffTable, output);

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

    // Calculate probability to pass b tagging
    double myProbabilitySum = 0.0;
    if (!iEvent.isRealData()) {
      size_t nJets = jets.size();
      std::vector<bool> myPassedStatus;
      for (size_t j = 0; j < jets.size(); ++j) {
        myPassedStatus.push_back(false); // initialize
      }
      size_t nPermutations = TMath::Power(2, nJets);
      for (size_t i = 0; i < nPermutations; ++i) {
        // Set status vector according to the permutation
        std::cout << "permutation " << i << ":";
        size_t nPassed = 0;
        for (size_t j = 0; j < jets.size(); ++j) {
          bool myStatus = (static_cast<int>(i) % static_cast<int>(TMath::Power(2,j)) == 0);
          myPassedStatus[j] = myStatus;
          if (myStatus) ++nPassed;
          std::cout << "," << myPassedStatus[j];
        }
        // Sum probability only if the number of passed jets would match to the cut criteria
        if (fNumberOfBJets.passedCut(nPassed)) {
          double myProbability = 1.0;
          for (size_t j = 0; j < jets.size(); ++j) {
            // Obtain correct efficiency table depending on jet flavor
            EfficiencyTable* myTable = 0;
            int myJetFlavor = std::abs(jets[j]->partonFlavour());
            if (myJetFlavor >= 1 && myJetFlavor <= 3 ) { // uds jet
              myTable = &fUDSMistagEffTable;
            } else if (myJetFlavor == 4) { // c jet
              myTable = &fCMistagEffTable;
            } else if (myJetFlavor == 5) { // b jet
              myTable = &fTagEffTable;
            } else { // gluon jet or unknown; assume unknown is rather a gluon than uds jet (mistag rate is higher)
              myTable = &fGMistagEffTable;
            }
            if (myPassedStatus[j]) {
              myProbability *= myTable->getEfficiency(jets[j]->pt());
              std::cout << "," << myTable->getEfficiency(jets[j]->pt());
            } else {
              myProbability *= 1.0 - myTable->getEfficiency(jets[j]->pt());
              std::cout << "," << 1.0 - myTable->getEfficiency(jets[j]->pt());
            }
          }
          myProbabilitySum += myProbability;
          std::cout << ",prob=," << myProbability << std::endl;
        }
      }
    }
    std::cout << "Overall prob:," << myProbabilitySum << std::endl;
    output.fProbabilityToPassBtagging = myProbabilitySum;

    return output;
  }

  void BTagging::calculateJetSFAndUncertaintyTerm(edm::Ptr<pat::Jet>& iJet, bool isBTagged, EventSFTerms& terms, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) const {
    // Get jet information
    int flavour = std::abs(iJet->partonFlavour());
    double pT = iJet->pt();
    
    // Set flags
    bool isGenuineB = false, isGenuineC = false, isGenuineG = false, isGenuineUDS = false;
    if      (flavour == 5) isGenuineB = true;
    else if (flavour == 4) isGenuineC = true;
    else if (flavour == 21) isGenuineG = true;
    else    isGenuineUDS = true;

    // Calculate the jet weight according to the properties (flavour, momentum, etc.) of the jet and the tagging status
    if (isGenuineB) {
      terms.addJetSFTerm(pT, isBTagged, sfTag, effTag);
      sfTag.addJetSFUncertaintyTerm(pT, isBTagged, effTag);
      effTag.addJetSFUncertaintyTerm(pT, isBTagged, sfTag);
    }
    else if (isGenuineC) {
      terms.addJetSFTerm(pT, isBTagged, sfTag, effCMistag);
      sfTag.addJetSFUncertaintyTerm(pT, isBTagged, effCMistag, 2.0); // c-jets use b-jet scale factors with double uncertainty
      effCMistag.addJetSFUncertaintyTerm(pT, isBTagged, sfTag);
    }
    else if (isGenuineG) {
      terms.addJetSFTerm(pT, isBTagged, sfMistag, effGMistag);
      sfMistag.addJetSFUncertaintyTerm(pT, isBTagged, effGMistag);
      effGMistag.addJetSFUncertaintyTerm(pT, isBTagged, sfMistag);
    }
    else if (isGenuineUDS) {
      terms.addJetSFTerm(pT, isBTagged, sfMistag, effUDSMistag);
      sfMistag.addJetSFUncertaintyTerm(pT, isBTagged, effUDSMistag);
      effUDSMistag.addJetSFUncertaintyTerm(pT, isBTagged, sfMistag);
    }
  }

  double BTagging::calculateRelativeEventScaleFactorUncertainty(bool up, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) {
    double relUncertSquared = 0.0;
    relUncertSquared += sfTag.calculateRelativeUncertaintySquared(up);
    relUncertSquared += sfMistag.calculateRelativeUncertaintySquared(up);
    relUncertSquared += effTag.calculateRelativeUncertaintySquared(up);
    relUncertSquared += effCMistag.calculateRelativeUncertaintySquared(up);
    relUncertSquared += effGMistag.calculateRelativeUncertaintySquared(up);
    relUncertSquared += effUDSMistag.calculateRelativeUncertaintySquared(up);
    return TMath::Sqrt(relUncertSquared);
  }

  void BTagging::setEventScaleFactorInfo(EventSFTerms& terms, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag, BTagging::Data& output) {
    output.fEventScaleFactor = terms.calculateEventScaleFactor();
    output.fEventSFRelUncert_up = calculateRelativeEventScaleFactorUncertainty(true, sfTag, sfMistag, effTag, effCMistag, effGMistag, effUDSMistag);
    output.fEventSFAbsUncert_up = output.fEventSFRelUncert_up * output.fEventScaleFactor;
    output.fEventSFRelUncert_down = calculateRelativeEventScaleFactorUncertainty(false, sfTag, sfMistag, effTag, effCMistag, effGMistag, effUDSMistag);
    output.fEventSFAbsUncert_down = output.fEventSFRelUncert_down * output.fEventScaleFactor;

    output.fEventSFAbsUncert_max = TMath::Max(output.fEventSFAbsUncert_up, output.fEventSFAbsUncert_down);
    
    if (printValidationOutput) {
      std::cout << "Event weight: " << output.fEventScaleFactor << " (+" << output.fEventSFAbsUncert_up << ", -" << output.fEventSFAbsUncert_down << ")" << std::endl;
      std::cout << "  Corresponding to relative uncertainty (+" << output.fEventSFRelUncert_up << ", -" << output.fEventSFRelUncert_down<< ")" << std::endl;;
    }

    // Do the variation, if asked
    if(fVariationEnabled) {
      if (fVariationShiftBy > 0) output.fEventScaleFactor += fVariationShiftBy * output.fEventSFAbsUncert_up;
      else output.fEventScaleFactor += fVariationShiftBy * output.fEventSFAbsUncert_down;
      // These are meaningless after the variation:
      output.fEventSFAbsUncert_up = 0;
      output.fEventSFAbsUncert_down = 0;
      output.fEventSFRelUncert_up = 0;
      output.fEventSFRelUncert_down = 0;
    }
  }

  // Method called from SignalAnalysis.cc:
  void BTagging::fillScaleFactorHistograms(BTagging::Data& data) {
    hScaleFactor->Fill(data.getScaleFactor());
    hBTagAbsoluteUncertainty->Fill(data.getScaleFactorMaxAbsUncertainty());
    hBTagRelativeUncertainty->Fill(data.getScaleFactorMaxAbsUncertainty() / data.fEventScaleFactor);
  }

  // Method called from HPlusBTaggingSelectorFilter.cc;
  BTagging::PerJetInfo BTagging::getPerJetInfo(edm::PtrVector<pat::Jet> jetCollection, BTagging::Data& bTagData, bool isRealData) const {
    PerJetInfo info;
    info.reserve(jetCollection.size());
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jetCollection.begin(); iter != jetCollection.end(); ++iter) {
      bool tagged = false;
      double scaleFactor = 1.0;
      double uncertainty = 0.0;
      bool genuine = false;

      edm::Ptr<pat::Jet> jet = *iter;
      // Find out if jet is b-tagged
      for (edm::PtrVector<pat::Jet>::iterator bjet = bTagData.getSelectedJets().begin(); bjet != bTagData.getSelectedJets().end(); ++bjet) {
	if (jet == *bjet) {
	  tagged = true;
	  break;
	}
      }
      // If MC, calculate the following things:
      if (! isRealData) {
	int flavour = std::abs(jet->partonFlavour());
	const BTagging::ScaleFactorTable *sfTable;
	const BTagging::EfficiencyTable *effTable;
	double SFUncertaintyFactor = 1.0;
	// Find out if jet is genuine b-jet and choose the correct look-up tables
	if (flavour == 5) {
	  genuine = true;
	  sfTable = &fTagSFTable;
	  effTable = &fTagEffTable;
	} else if (flavour == 4) {
	  sfTable = &fTagSFTable;
          effTable = &fCMistagEffTable;
	  SFUncertaintyFactor = 2.0;
	} else if (flavour == 21) {
          sfTable = &fMistagSFTable;
          effTable = &fGMistagEffTable;
	} else {
          sfTable = &fMistagSFTable;
          effTable = &fUDSMistagEffTable;
	}
	// Get event scale factor term due to current jet
	scaleFactor = calculateJetSFTerm(jet->pt(), tagged, *sfTable, *effTable);
	// Get event scale factor uncertainty term due to current jet
	uncertainty = calculateJetSFUncertaintyTerm(jet->pt(), tagged, *sfTable, *effTable, SFUncertaintyFactor);
      }
      // Set output
      info.scaleFactor.push_back(scaleFactor);
      info.uncertainty.push_back(uncertainty);
      info.tagged.push_back(tagged);
      info.genuine.push_back(genuine);
    }
    return info;
  }

  double BTagging::calculateJetSFTerm(double pT, bool isBTagged, const ScaleFactorTable& sfTable, const EfficiencyTable& effTable) const {
    double sf = 1.0;
    if (isBTagged) {
      sf = sfTable.getScaleFactor(pT);
    } else {
      sf = (1.-sfTable.getScaleFactor(pT)*effTable.getEfficiency(pT)) / (1.-effTable.getEfficiency(pT));
    }
    return sf;
  }

  double BTagging::calculateJetSFUncertaintyTerm(double pT, bool isBTagged, const ScaleFactorTable& sfTable, const EfficiencyTable& effTable, double SFUncertaintyFactor) const {
    double uncertainty = 0.0;
    if (isBTagged)
      uncertainty = SFUncertaintyFactor * sfTable.getMaximumUncertainty(pT);
    else {
      double uncertainty2 = TMath::Power((-(SFUncertaintyFactor * effTable.getEfficiency(pT) * sfTable.getScaleFactor(pT) * sfTable.getMaximumUncertainty(pT))
					  / (1.0 - effTable.getEfficiency(pT) * sfTable.getScaleFactor(pT))), 2)
	+ TMath::Power(((1.0 - sfTable.getScaleFactor(pT)) * effTable.getEfficiency(pT) * effTable.getMaximumUncertainty(pT))
		       / ((1.0 - sfTable.getScaleFactor(pT) * effTable.getEfficiency(pT)) * (1.0 - effTable.getEfficiency(pT))), 2);
      uncertainty = TMath::Sqrt(uncertainty2);
    }
    return uncertainty;
  }
}
