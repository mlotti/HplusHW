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



namespace HPlus {
  // ================================== class Data ==================================
  BTagging::Data::Data():
    fPassedEvent(false),
    iNBtags(-1),
    fMaxDiscriminatorValue(-999.0),
    fScaleFactor(1.0),
    fScaleFactorAbsoluteUncertainty(0.0),
    fScaleFactorRelativeUncertainty(0.0)
    { }
  BTagging::Data::~Data() {}

  const bool BTagging::Data::hasGenuineBJets() const {
    for (edm::PtrVector<pat::Jet>::const_iterator iter = fSelectedJets.begin(); iter != fSelectedJets.end(); ++iter) {
      int myFlavor = std::abs((*iter)->partonFlavour());
      if (myFlavor == 5) return true;
    }
    return false;
  }

  // ================================== class BTaggingScaleFactor ==================================
  BTagging::BTaggingScaleFactor::BTaggingScaleFactor() {
    btagdb = 0;
  }

  BTagging::BTaggingScaleFactor::~BTaggingScaleFactor() {}

  void BTagging::BTaggingScaleFactor::UseDB(BTaggingScaleFactorFromDB* db){btagdb = db;}  
  
  void BTagging::BTaggingScaleFactor::addBFlavorData(double pT, double scaleFactorB, double scaleFactorUncertaintyB, double epsilonMCB) {
    fPtBinsB.push_back(pT);
    fScaleFactorB.push_back(scaleFactorB);
    fScaleFactorUncertaintyB.push_back(scaleFactorUncertaintyB);
    fEpsilonMCB.push_back(epsilonMCB);
  }
  
  void BTagging::BTaggingScaleFactor::addNonBFlavorData(double pT, double scaleFactorL, double scaleFactorUncertaintyL, double epsilonMCL) {
    fPtBinsL.push_back(pT);
    fScaleFactorL.push_back(scaleFactorL);
    fScaleFactorUncertaintyL.push_back(scaleFactorUncertaintyL);
    fEpsilonMCL.push_back(epsilonMCL);
  }

  size_t BTagging::BTaggingScaleFactor::obtainIndex(const std::vector<double>& table, double pt) {
    // REMARK: An identical function exists in class BTagging::EfficiencyTable!
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

  double BTagging::BTaggingScaleFactor::calculateScaleFactor(const PerJetInfo& info) {
    double scaleFactor = 1.0;
    for(size_t i=0; i<info.size(); ++i) {
      scaleFactor *= info.scaleFactor[i];
    }
    return scaleFactor;
  }

  double BTagging::BTaggingScaleFactor::calculateAbsoluteUncertainty(const PerJetInfo& info) {
    // FIXME this is a dirty hack, numbers are from BTV-11-004 (see accompanying AN's)
    double uncert = 0.0;
    for(size_t i=0; i<info.size(); ++i) {
      double tmp = info.uncertainty[i];
      uncert += tmp*tmp;
    }
    return std::sqrt(uncert);
    // FIXME end of dirty hack
    // old numbers
    /*
    return calculateScaleFactor(info)*calculateRelativeUncertainty(info);
    */
  }

  double BTagging::BTaggingScaleFactor::calculateRelativeUncertainty(const PerJetInfo& info) {
    // FIXME this is a dirty hack, numbers are from BTV-11-004 (see accompanying AN's)
    return calculateAbsoluteUncertainty(info) / calculateScaleFactor(info);
    // FIXME end of dirty hack
  }

  double BTagging::BTaggingScaleFactor::getBtagScaleFactor(double pt,double eta) const {
    return fScaleFactorB[obtainIndex(fPtBinsB, pt)];
  }

  double BTagging::BTaggingScaleFactor::getBtagScaleFactorError(double pt,double eta) const {
    return fScaleFactorUncertaintyB[obtainIndex(fPtBinsB, pt)];
  }

  double BTagging::BTaggingScaleFactor::calculateMistagScaleFactor(double pt) const {
    // The scale factor is given by a four-degree polynomial function of the transverse momentum.
    // Source: https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs.C
    return ((0.948463+(0.00288102*pt))+(-7.98091*TMath::Power(10.0,-6.0)*(pt*pt)))+(5.50157*TMath::Power(10.0,-9.0)*(pt*(pt*pt)));
  }

  double BTagging::BTaggingScaleFactor::getMistagScaleFactor(double pt, double eta) const {
    return fScaleFactorL[obtainIndex(fPtBinsB, pt)];
  }

  double BTagging::BTaggingScaleFactor::getMistagScaleFactorError(double pt, double eta) const {
    return fScaleFactorUncertaintyL[obtainIndex(fPtBinsB, pt)];
  }

  // ================================== class EfficiencyTable ==================================
  BTagging::EfficiencyTable::EfficiencyTable() { }

  BTagging::EfficiencyTable::~EfficiencyTable() { }

  void BTagging::EfficiencyTable::addTagEfficiencyData(double pT, double efficiency, double effUncertainty) {
    fPtBinsTag.push_back(pT);
    fEfficiencyTag.push_back(efficiency);
    fEffUncertaintyTag.push_back(effUncertainty);
  }
  
  void BTagging::EfficiencyTable::addGMistagEfficiencyData(double pT, double efficiency, double effUncertainty) {
    fPtBinsGMistag.push_back(pT);
    fEfficiencyGMistag.push_back(efficiency);
    fEffUncertaintyGMistag.push_back(effUncertainty);
  }

  void BTagging::EfficiencyTable::addUDSMistagEfficiencyData(double pT, double efficiency, double effUncertainty) {
    fPtBinsUDSMistag.push_back(pT);
    fEfficiencyUDSMistag.push_back(efficiency);
    fEffUncertaintyUDSMistag.push_back(effUncertainty);
  }

  size_t BTagging::EfficiencyTable::obtainIndex(const std::vector<double>& table, double pt) {
    // REMARK: An identical function exists in class BTagging::BTaggingScaleFactor!
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

  double BTagging::EfficiencyTable::getTagEfficiency(double pT) const {
    return fEfficiencyTag[obtainIndex(fPtBinsTag, pT)];
  }

  double BTagging::EfficiencyTable::getGMistagEfficiency(double pT) const {
    return fEfficiencyGMistag[obtainIndex(fPtBinsGMistag, pT)];
  }

  double BTagging::EfficiencyTable::getUDSMistagEfficiency(double pT) const {
    return fEfficiencyUDSMistag[obtainIndex(fPtBinsUDSMistag, pT)];
  }

  double BTagging::EfficiencyTable::getTagEffUncertainty(double pT) const {
    return fEffUncertaintyTag[obtainIndex(fPtBinsTag, pT)];
  }

  double BTagging::EfficiencyTable::getGMistagEffUncertainty(double pT) const {
    return fEffUncertaintyGMistag[obtainIndex(fPtBinsGMistag, pT)];
  }

  double BTagging::EfficiencyTable::getUDSMistagEffUncertainty(double pT) const {
    return fEffUncertaintyUDSMistag[obtainIndex(fPtBinsUDSMistag, pT)];
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
    FactorsFromDB(iConfig.getUntrackedParameter<bool>("UseBTagDB",false)),
    fTaggedCount(eventCounter.addSubCounter("b-tagging main","b-tagging")),
    fAllSubCount(eventCounter.addSubCounter("b-tagging", "all jets")),
    fTaggedSubCount(eventCounter.addSubCounter("b-tagging", "tagged")),
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

    // BTagging scale factors from DB
    if(FactorsFromDB) {
      btagDB = new BTaggingScaleFactorFromDB(iConfig);
      fBTaggingScaleFactor.UseDB(btagDB);
    }
    else
      btagDB = 0;
    
    // B-tagged-as-b scale factors for 2011 analysis (assumed no eta dependence)
    // Source : BTV-12-001
    // Remarks: The pT bin 0-30 GeV has the scale factor of the 500+ GeV bin with twice the uncertainty.
    //          The scale factor is calculated as 0.901615*((1.+(0.552628*pT))/(1.+(0.547195*pT)))
    fBTaggingScaleFactor.addBFlavorData(0.,   .9105344, .1733126, .671); // TODO: update MC b-tagging efficiencies!
    fBTaggingScaleFactor.addBFlavorData(30.,  .9100530, .0364717, .671);
    fBTaggingScaleFactor.addBFlavorData(40.,  .9101758, .0362281, .741);
    fBTaggingScaleFactor.addBFlavorData(50.,  .9102513, .0232876, .779);
    fBTaggingScaleFactor.addBFlavorData(60.,  .9103024, .0249618, .802);
    fBTaggingScaleFactor.addBFlavorData(70.,  .9103392, .0261482, .826);
    fBTaggingScaleFactor.addBFlavorData(80.,  .9103670, .0290466, .840);
    fBTaggingScaleFactor.addBFlavorData(100., .9104327, .0300033, .840);
    fBTaggingScaleFactor.addBFlavorData(120., .9104516, .0453252, .856);
    fBTaggingScaleFactor.addBFlavorData(160., .9104659, .0685143, .671);
    fBTaggingScaleFactor.addBFlavorData(210., .9104897, .0653621, .671);
    fBTaggingScaleFactor.addBFlavorData(260., .9105045, .0712586, .671);
    fBTaggingScaleFactor.addBFlavorData(320., .9105161, .0945890, .671);
    fBTaggingScaleFactor.addBFlavorData(400., .9105263, .0777011, .671);
    fBTaggingScaleFactor.addBFlavorData(500., .9105344, .0866563, .671);

    // Tagging and mistagging efficiencies in MC
    // Source: Own measurement
    fEfficiencyTable.addTagEfficiencyData(0.,   .8, .1); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fEfficiencyTable.addTagEfficiencyData(100., .9, .05); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fEfficiencyTable.addGMistagEfficiencyData(0.,   .05, .03); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fEfficiencyTable.addGMistagEfficiencyData(100., .02, .005); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fEfficiencyTable.addUDSMistagEfficiencyData(0.,   .08, .01); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fEfficiencyTable.addUDSMistagEfficiencyData(100., .09, .06); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
  }

  BTagging::~BTagging() {
    if(btagDB) delete btagDB;
  }

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
    // Initialise output data object
    Data output;
    output.fSelectedJets.reserve(jets.size());
    output.fSelectedSubLeadingJets.reserve(jets.size());
    // Initialise internal variables
    bool isGenuineB = false;
    bool isGenuineC = false;
    bool isGenuineG = false;
    bool isGenuineUDS = false;

    if(btagDB) btagDB->setup(iSetup);

    // Loop over all jets in event
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      
      // Initialize structure for collecting information (scale factor & uncertainty, tagging status, etc.) of each jet.
      fBTaggingInfo.reserve(jets.size());

      // Initialize flags
      bool isBTagged = false;

      increment(fAllSubCount);

      // In MC, check the true flavour of the parton that produced the jet
      if (!iEvent.isRealData()) {
	int jetFlavour = std::abs(iJet->partonFlavour());
	if      (jetFlavour == 5) isGenuineB = true;
	else if (jetFlavour == 4) isGenuineC = true;
	else if (jetFlavour == 21) isGenuineG = true;
	else    isGenuineUDS = true;
      }
      if (isGenuineB) increment(fTaggedAllRealBJetsSubCount); // STR: why "Tagged"? No tagging has been done yet!

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
      } else if (discr > fSubLeadingDiscrCut) {
        output.fSelectedSubLeadingJets.push_back(iJet);
      } else {
        continue;
      }
      increment(fTaggedSubCount);
      hPt->Fill(iJet->pt());
      hEta->Fill(iJet->eta());
      if (discr > output.fMaxDiscriminatorValue) output.fMaxDiscriminatorValue = discr;
      if (isGenuineB) increment(fTaggedTaggedRealBJetsSubCount); // STR: "TaggedTagged"?!

      // If MC, calculate and store the contribution to the event weight for each jet.
      if (!iEvent.isRealData()) {
	BTagging::WeightWithUncertainty jetWeightData;
	jetWeightData = calculateJetWeight(iJet, isBTagged, fBTaggingScaleFactor, fEfficiencyTable);
	fBTaggingInfo.tagged.push_back(isBTagged);
	fBTaggingInfo.genuine.push_back(isGenuineB);
	fBTaggingInfo.scaleFactor.push_back(jetWeightData.weight);
	fBTaggingInfo.uncertainty.push_back(jetWeightData.uncert);
      }
    } // End of jet loop

    if (!iEvent.isRealData()) calculateScaleFactorInfo(fBTaggingInfo, output); // Calculate scale factor and its uncertainty for MC events

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

  BTagging::WeightWithUncertainty BTagging::calculateJetWeight(edm::Ptr<pat::Jet>& iJet, bool isBTagged, BTaggingScaleFactor& sf, EfficiencyTable& eff) const {
    BTagging::WeightWithUncertainty weightData;
    weightData.weight = 1.0;
    weightData.uncert = 0.0;
    
    // Get jet information
    int flavour = iJet->partonFlavour();
    double pt = iJet->pt();
    double eta = iJet->eta();
    
    // Set flags
    bool isGenuineB = false, isGenuineC = false, isGenuineG = false, isGenuineUDS = false;
    if      (flavour == 5) isGenuineB = true;
    else if (flavour == 4) isGenuineC = true;
    else if (flavour == 21) isGenuineG = true;
    else    isGenuineUDS = true;
    
    // Calculate the jet weight according to the properties (flavour, momentum, etc.) of the jet and the tagging status
    if (isBTagged) {
      if (isGenuineB) {
	weightData.weight = sf.getBtagScaleFactor(pt, eta); // ok
	weightData.uncert = sf.getBtagScaleFactorError(pt, eta) / weightData.weight;
      }
      if (isGenuineC) {
	weightData.weight = sf.getBtagScaleFactor(pt, eta); // ok
	weightData.uncert = 2 * sf.getBtagScaleFactorError(pt, eta) / weightData.weight; // uncertainty doubled w.r.t. genuine b
      }
      if (isGenuineG) {
	weightData.weight = sf.calculateMistagScaleFactor(pt); // ok
	  }
      if (isGenuineUDS) {
	weightData.weight = sf.calculateMistagScaleFactor(pt); // ok
	  }
    } else {
      if (isGenuineB) {
	weightData.weight = (1.-sf.getBtagScaleFactor(pt, eta)*eff.getTagEfficiency(pt)) / (1.-eff.getTagEfficiency(pt)); // ok
	  }
      if (isGenuineC) {
	weightData.weight = (1.-sf.getBtagScaleFactor(pt, eta)*eff.getTagEfficiency(pt)) / (1.-eff.getTagEfficiency(pt)); // ok
	  }
      if (isGenuineG) {
	weightData.weight = (1.-sf.calculateMistagScaleFactor(pt)*eff.getGMistagEfficiency(pt)) / (1.-eff.getGMistagEfficiency(pt)); // ok
      }
      if (isGenuineUDS) {
	weightData.weight = (1.-sf.calculateMistagScaleFactor(pt)*eff.getUDSMistagEfficiency(pt)) / (1.-eff.getUDSMistagEfficiency(pt)); // ok
      }
    }
    return weightData;
  }

  BTagging::PerJetInfo BTagging::getPerJetInfo(const edm::PtrVector<pat::Jet>& jets, const Data& btagData, bool isData) const {
    BTagging::PerJetInfo dummy;
    return dummy;
//     return fBTaggingScaleFactor.getPerJetInfo(jets, btagData, isData);
  }

  void BTagging::calculateScaleFactorInfo(PerJetInfo& bTaggingInfo, BTagging::Data& output) {
    output.fScaleFactor = fBTaggingScaleFactor.calculateScaleFactor(bTaggingInfo);
    output.fScaleFactorAbsoluteUncertainty = fBTaggingScaleFactor.calculateAbsoluteUncertainty(bTaggingInfo);
    output.fScaleFactorRelativeUncertainty = fBTaggingScaleFactor.calculateRelativeUncertainty(bTaggingInfo);

    // Do the variation, if asked
    if(fVariationEnabled) {
      output.fScaleFactor += fVariationShiftBy * output.fScaleFactorAbsoluteUncertainty;
      // These are meaningless after the variation:
      output.fScaleFactorAbsoluteUncertainty = 0;
      output.fScaleFactorRelativeUncertainty = 0;
    }
  }

  void BTagging::fillScaleFactorHistograms(BTagging::Data& input) {
    hScaleFactor->Fill(input.getScaleFactor());
    hBTagAbsoluteUncertainty->Fill(input.getScaleFactorAbsoluteUncertainty());
    hBTagRelativeUncertainty->Fill(input.getScaleFactorRelativeUncertainty());
  }
}
