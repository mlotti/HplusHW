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
  BTagging::BTaggingScaleFactor::BTaggingScaleFactor() {}

  BTagging::BTaggingScaleFactor::~BTaggingScaleFactor() {}

  void BTagging::BTaggingScaleFactor::addScaleFactorData(double pT, double scaleFactor, double scaleFactorUncertainty) {
    fPtBins.push_back(pT);
    fScaleFactor.push_back(scaleFactor);
    fScaleFactorUncertainty.push_back(scaleFactorUncertainty);
  }

  void BTagging::BTaggingScaleFactor::initializeJetTable() {
    size_t i = 0;
    while (i < fPtBins.size()) {
      fNTagged.push_back(0);
      fNNotTagged.push_back(0);
      fPerBinUncertaintyTagged.push_back(0);
      fPerBinUncertaintyNotTagged.push_back(0);
      i++;
    }
  }

  void BTagging::BTaggingScaleFactor::addTaggedJet(double pT) {
    fNTagged[obtainIndex(pT)]++;
  }

  void BTagging::BTaggingScaleFactor::addUntaggedJet(double pT) {
    fNNotTagged[obtainIndex(pT)]++;
  }

  void BTagging::BTaggingScaleFactor::addUncertaintyTagged(double pT) {
    size_t i = obtainIndex(fPtBins, pT);
    fPerBinUncertaintyTagged[i] += fScaleFactorUncertainty[i] / fScaleFactor[i];
  }

  void BTagging::BTaggingScaleFactor::addUncertaintyTagged(double pT, double uncertaintyFactor) {
    size_t i = obtainIndex(fPtBins, pT);
    fPerBinUncertaintyTagged[i] += uncertaintyFactor * fScaleFactorUncertainty[i] / fScaleFactor[i];
  }

  void BTagging::BTaggingScaleFactor::addUncertaintyUntagged(double pT, EfficiencyTable& efficiencyTable) {
    size_t i = obtainIndex(fPtBins, pT);
    double efficiency = efficiencyTable.getEfficiency(pT);
    fPerBinUncertaintyNotTagged[i] += - (efficiency * fScaleFactorUncertainty[i]) / (1.0 - efficiency * fScaleFactor[i]);
  }

  void BTagging::BTaggingScaleFactor::addUncertaintyUntagged(double pT, EfficiencyTable& efficiencyTable, double uncertaintyFactor) {
    size_t i = obtainIndex(fPtBins, pT);
    double efficiency = efficiencyTable.getEfficiency(pT);
    fPerBinUncertaintyNotTagged[i] += - uncertaintyFactor * (efficiency * fScaleFactorUncertainty[i]) / (1.0 - efficiency * fScaleFactor[i]);
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

  double BTagging::BTaggingScaleFactor::getScaleFactor(double pt) const {
    return fScaleFactor[obtainIndex(fPtBins, pt)];
  }

  double BTagging::BTaggingScaleFactor::getScaleFactorUncertainty(double pt) const {
    return fScaleFactorUncertainty[obtainIndex(fPtBins, pt)];
  }

  double BTagging::BTaggingScaleFactor::calculateMistagScaleFactor(double pt) const {
    // The scale factor is given by a four-degree polynomial function of the transverse momentum.
    // Source: https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFlightFuncs.C
    return ((0.948463+(0.00288102*pt))+(-7.98091*TMath::Power(10.0,-6.0)*(pt*pt)))+(5.50157*TMath::Power(10.0,-9.0)*(pt*(pt*pt)));
  }

  double BTagging::BTaggingScaleFactor::getNTagged(double pT) const {
    return fNTagged[obtainIndex(fPtBins, pT)];
  }

  double BTagging::BTaggingScaleFactor::getNUntagged(double pT) const {
    return fNNotTagged[obtainIndex(fPtBins, pT)];
  }

  double BTagging::BTaggingScaleFactor::calculateRelativeUncertaintySquared() {
    double relUncertSquared = 0.0;
    size_t i = 0;
    while (i < fPtBins.size()) {
      relUncertSquared += TMath::Power(fPerBinUncertaintyTagged[i] + fPerBinUncertaintyNotTagged[i], 2);
      i++;
    }
    return relUncertSquared;
  }



  // ================================== class EfficiencyTable ==================================
  BTagging::EfficiencyTable::EfficiencyTable() { }

  BTagging::EfficiencyTable::~EfficiencyTable() { }

  void BTagging::EfficiencyTable::addEfficiencyData(double pT, double efficiency, double effUncertainty) {
    fPtBins.push_back(pT);
    fEfficiency.push_back(efficiency);
    fEffUncertainty.push_back(effUncertainty);
  }

  void BTagging::EfficiencyTable::initializeJetTable() {
    size_t i = 0;
    while (i < fPtBins.size()) {
      fNTagged.push_back(0);
      fNNotTagged.push_back(0);
      fPerBinUncertaintyNotTagged.push_back(0);
      i++;
    }
  }

  void BTagging::EfficiencyTable::addTaggedJet(double pT) {
    fNTagged[obtainIndex(pT)]++;
  }

  void BTagging::EfficiencyTable::addUntaggedJet(double pT) {
    fNNotTagged[obtainIndex(pT)]++;
  }

  void BTagging::EfficiencyTable::addUncertaintyUntagged(double pT, BTaggingScaleFactor& scaleFactorTable) {
    size_t i = obtainIndex(fPtBins, pT);
    double scaleFactor = scaleFactorTable.getScaleFactor(pT);
    fPerBinUncertaintyNotTagged[i] += ((1.0 - scaleFactor) * fEffUncertainty[i]) / ((1.0 - scaleFactor * fEfficiency[i]) * (1.0 - fEfficiency[i]));
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

  double BTagging::EfficiencyTable::getEfficiency(double pT) const {
    return fEfficiency[obtainIndex(fPtBins, pT)];
  }

  double BTagging::EfficiencyTable::getEffUncertainty(double pT) const {
    return fEffUncertainty[obtainIndex(fPtBins, pT)];
  }

  double BTagging::EfficiencyTable::getNTagged(double pT) const {
    return fNTagged[obtainIndex(fPtBins, pT)];
  }

  double BTagging::EfficiencyTable::getNUntagged(double pT) const {
    return fNNotTagged[obtainIndex(fPtBins, pT)];
  }

  double BTagging::EfficiencyTable::calculateRelativeUncertaintySquared() {
    double relUncertSquared = 0.0;
    size_t i = 0;
    while (i < fPtBins.size()) {
      relUncertSquared += TMath::Power(fPerBinUncertaintyNotTagged[i], 2);
      i++;
    }
    return relUncertSquared;
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

    // B-tagged-as-b scale factors for 2011 analysis (assumed no eta dependence)
    // Source : BTV-12-001
    // Remarks: The pT bin 0-30 GeV has the scale factor of the 500+ GeV bin with twice the uncertainty.
    //          The scale factor is calculated as 0.901615*((1.+(0.552628*pT))/(1.+(0.547195*pT)))
    ////fTagSFTable, fMistagSFTable
    fTagSFTable.addScaleFactorData(0.,   .9105344, .1733126);
    fTagSFTable.addScaleFactorData(30.,  .9100530, .0364717);
    fTagSFTable.addScaleFactorData(40.,  .9101758, .0362281);
    fTagSFTable.addScaleFactorData(50.,  .9102513, .0232876);
    fTagSFTable.addScaleFactorData(60.,  .9103024, .0249618);
    fTagSFTable.addScaleFactorData(70.,  .9103392, .0261482);
    fTagSFTable.addScaleFactorData(80.,  .9103670, .0290466);
    fTagSFTable.addScaleFactorData(100., .9104327, .0300033);
    fTagSFTable.addScaleFactorData(120., .9104516, .0453252);
    fTagSFTable.addScaleFactorData(160., .9104659, .0685143);
    fTagSFTable.addScaleFactorData(210., .9104897, .0653621);
    fTagSFTable.addScaleFactorData(260., .9105045, .0712586);
    fTagSFTable.addScaleFactorData(320., .9105161, .0945890);
    fTagSFTable.addScaleFactorData(400., .9105263, .0777011);
    fTagSFTable.addScaleFactorData(500., .9105344, .0866563);
    fTagSFTable.initializeJetTable();

    fMistagSFTable.addScaleFactorData(0.,   .9105344, .1733126);
    fMistagSFTable.addScaleFactorData(30.,  .9100530, .0364717);
    fMistagSFTable.initializeJetTable();

    // Tagging and mistagging efficiencies in MC
    // Source: Own measurement
    ////fTagEfficiencyTable, fGMistagEfficiencyTable, fUDSMistagEfficiencyTable
    fTagEffTable.addEfficiencyData(0.,   .8, .1); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fTagEffTable.addEfficiencyData(100., .9, .05); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fTagEffTable.initializeJetTable();

    fGMistagEffTable.addEfficiencyData(0.,   .8, .1); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fGMistagEffTable.addEfficiencyData(100., .9, .05); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fGMistagEffTable.initializeJetTable();

    fUDSMistagEffTable.addEfficiencyData(0.,   .8, .1); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fUDSMistagEffTable.addEfficiencyData(100., .9, .05); // THESE ARE COMPLETE DUMMY VALUES FOR TESTING PURPOSES!!!
    fUDSMistagEffTable.initializeJetTable();
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
    // Initialize output data object
    Data output;
    output.fSelectedJets.reserve(jets.size());
    output.fSelectedSubLeadingJets.reserve(jets.size());
    // Initialize internal variables
    bool isGenuineB = false;
    bool isGenuineC = false;
    bool isGenuineG = false;
    bool isGenuineUDS = false;

    // Loop over all jets in event
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      
      // Initialize structures for collecting information (scale factor & uncertainty, tagging status, etc.) of each jet.
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
	jetWeightData = calculateJetWeight(iJet, isBTagged, fTagSFTable, fMistagSFTable, fTagEffTable, fGMistagEffTable, fUDSMistagEffTable);
	fJetsPerSFBin = jetWeightData.jetsPerSFBin;
	fJetsPerEffBin = jetWeightData.jetsPerEffBin;
	fBTaggingInfo.tagged.push_back(isBTagged);
	fBTaggingInfo.genuine.push_back(isGenuineB);
	fBTaggingInfo.scaleFactor.push_back(jetWeightData.weight);
	//fBTaggingInfo.uncertainty.push_back(jetWeightData.uncert);
      }
    } // End of jet loop

    // Calculate scale factor and its uncertainty for MC events
    if (!iEvent.isRealData()) calculateScaleFactorInfo(fBTaggingInfo, fTagSFTable, fMistagSFTable, fTagEffTable, fGMistagEffTable, fUDSMistagEffTable, output);

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

  BTagging::WeightWithUncertainty BTagging::calculateJetWeight(edm::Ptr<pat::Jet>& iJet, bool isBTagged, BTaggingScaleFactor& sfTag, BTaggingScaleFactor& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) const {
    // In the future, will take arguments bSF, lSF, bEff, gEff, udsEff
    BTagging::WeightWithUncertainty weightData;
    weightData.weight = 1.0;
    weightData.jetsPerSFBin.initialize(sfTag.getNumberOfBins());
    weightData.jetsPerEffBin.initialize(effTag.getNumberOfBins());
    //weightData.uncert = 0.0;
    
    // Get jet information
    int flavour = iJet->partonFlavour();
    double pt = iJet->pt();
    
    // Set flags
    bool isGenuineB = false, isGenuineC = false, isGenuineG = false, isGenuineUDS = false;
    if      (flavour == 5) isGenuineB = true;
    else if (flavour == 4) isGenuineC = true;
    else if (flavour == 21) isGenuineG = true;
    else    isGenuineUDS = true;
    
    // Calculate the jet weight according to the properties (flavour, momentum, etc.) of the jet and the tagging status
    if (isBTagged) {
      if (isGenuineB) {
	weightData.weight = sfTag.getScaleFactor(pt);
	sfTag.addTaggedJet(pt);
	effTag.addTaggedJet(pt);
	sfTag.addUncertaintyTagged(pt);
      }
      if (isGenuineC) {
	weightData.weight = sfTag.getScaleFactor(pt);
	sfTag.addTaggedJet(pt);
        effTag.addTaggedJet(pt);
	sfTag.addUncertaintyTagged(pt, 2.0); // c-jets use b-jet scale factors with double uncertainty
      }
      if (isGenuineG) {
	weightData.weight = sfMistag.calculateMistagScaleFactor(pt);
	sfMistag.addTaggedJet(pt);
	effGMistag.addTaggedJet(pt);
	sfMistag.addUncertaintyTagged(pt);
      }
      if (isGenuineUDS) {
	weightData.weight = sfMistag.calculateMistagScaleFactor(pt);
	sfMistag.addTaggedJet(pt);
	effUDSMistag.addTaggedJet(pt);
	sfMistag.addUncertaintyTagged(pt);
      }
    } else {
      if (isGenuineB) {
	weightData.weight = (1.-sfTag.getScaleFactor(pt)*effTag.getEfficiency(pt)) / (1.-effTag.getEfficiency(pt));
	sfTag.addUntaggedJet(pt);
	effTag.addUntaggedJet(pt);
	sfTag.addUncertaintyUntagged(pt, effTag);
	effTag.addUncertaintyUntagged(pt, sfTag);
      }
      if (isGenuineC) {
	weightData.weight = (1.-sfTag.getScaleFactor(pt)*effTag.getEfficiency(pt)) / (1.-effTag.getEfficiency(pt));
	sfTag.addUntaggedJet(pt); // should have weight 4 for twice the uncertainty
	effTag.addUntaggedJet(pt);
	sfTag.addUncertaintyUntagged(pt, effTag, 2.0);
	effTag.addUncertaintyUntagged(pt, sfTag);
      }
      if (isGenuineG) {
	weightData.weight = (1.-sfMistag.calculateMistagScaleFactor(pt)*effGMistag.getEfficiency(pt)) / (1.-effGMistag.getEfficiency(pt));
	sfMistag.addUntaggedJet(pt);
	effGMistag.addUntaggedJet(pt);
	sfMistag.addUncertaintyUntagged(pt, effTag);
	effGMistag.addUncertaintyUntagged(pt, sfTag);
      }
      if (isGenuineUDS) {
	weightData.weight = (1.-sfMistag.calculateMistagScaleFactor(pt)*effUDSMistag.getEfficiency(pt)) / (1.-effUDSMistag.getEfficiency(pt));
	sfMistag.addUntaggedJet(pt);
	effUDSMistag.addUntaggedJet(pt);
	sfMistag.addUncertaintyUntagged(pt, effTag);
	effUDSMistag.addUncertaintyUntagged(pt, sfTag);
      }
    }
    return weightData;
  }

  double BTagging::calculateEventWeight(PerJetInfo& fBTaggingInfo) {
    double eventWeight = 1.0;
    size_t i = 0;
    while (i < fBTaggingInfo.scaleFactor.size()) {
      eventWeight *= fBTaggingInfo.scaleFactor[i];
      i++;
    }
    return eventWeight;
  }

  double BTagging::calculateRelativeEventWeightUncertainty(BTaggingScaleFactor& sfTag, BTaggingScaleFactor& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) {
    double relUncertSquared = 0.0;
    relUncertSquared += sfTag.calculateRelativeUncertaintySquared();
    relUncertSquared += sfMistag.calculateRelativeUncertaintySquared();
    relUncertSquared += effTag.calculateRelativeUncertaintySquared();
    relUncertSquared += effGMistag.calculateRelativeUncertaintySquared();
    relUncertSquared += effUDSMistag.calculateRelativeUncertaintySquared();
    return TMath::Sqrt(relUncertSquared);
  }

  void BTagging::calculateScaleFactorInfo(PerJetInfo& bTaggingInfo, BTaggingScaleFactor& sfTag, BTaggingScaleFactor& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag, BTagging::Data& output) {
    output.fScaleFactor = calculateEventWeight(bTaggingInfo);
    output.fScaleFactorRelativeUncertainty = calculateRelativeEventWeightUncertainty(sfTag, sfMistag, effTag, effGMistag, effUDSMistag);
    output.fScaleFactorAbsoluteUncertainty = output.fScaleFactorRelativeUncertainty * output.fScaleFactor;

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
