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

  size_t BTagging::BTaggingScaleFactor::obtainIndex(const std::vector<double>& table, double pt) {    //STR consider renaming to getIndexOfSFEntryByPt
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

  BTagging::Info BTagging::BTaggingScaleFactor::getPerJetInfo(const edm::PtrVector<pat::Jet>& jets, const Data& btagData, bool isData) const {
    Info ret;
    ret.reserve(jets.size());

    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jets.begin(); iJet != jets.end(); ++iJet) {
      bool tagged = false;
      for (edm::PtrVector<pat::Jet>::const_iterator iBjet = btagData.fSelectedJets.begin(); iBjet != btagData.fSelectedJets.end(); ++iBjet) {
	if (*iJet == *iBjet) tagged = true;
      }
      bool genuine = std::abs((*iJet)->partonFlavour()) == 5;

      // To see how per-jet scale factor and uncertainty are used, see calculateScaleFactor(), calculateAbsoluteUncertainty(), and  calculateRelativeUncertainty()
      double scaleFactor = 1.0;
      double uncertainty = 0.0;
      if(!isData) {
        // FIXME this is a dirty hack, numbers are from BTV-11-004 (see accompanying AN's)
        if(tagged) {
          // This is independent of pT
          if(genuine) { scaleFactor = 0.96; uncertainty = 0.04; }
          else        { scaleFactor = 1.17; uncertainty = 0.21; }
        }
        // FIXME end of dirty hack

        // Old numbers
        /*
        const double pt = (*iJet)->pt();
        const double eta = (*iJet)->eta();
        if(tagged) {
          if(genuine) {
            scaleFactor = getBtagScaleFactor(pt, eta);
            uncertainty = getBtagScaleFactorError(pt, eta) / scaleFactor;
          }
          else {
            scaleFactor = getMistagScaleFactor(pt, eta);
            uncertainty = getMistagScaleFactorError(pt, eta) / scaleFactor;
          }
        }
        else {
          if(genuine) {
            scaleFactor = (1.-getBtagScaleFactor(pt, eta)*getMCBtagEfficiency(pt, eta)) / (1.-getMCBtagEfficiency(pt, eta));
            uncertainty = -1. * getBtagScaleFactorError(pt, eta)*getMCBtagEfficiency(pt, eta) / (1.-getBtagScaleFactor(pt, eta)*getMCBtagEfficiency(pt, eta));
          }
          else {
            scaleFactor = (1.-getMistagScaleFactor(pt, eta)*getMCMistagEfficiency(pt, eta)) / (1.-getMCMistagEfficiency(pt, eta));
            uncertainty = -1. * getMistagScaleFactorError(pt, eta)*getMCMistagEfficiency(pt, eta) / (1.-getMistagScaleFactor(pt, eta)*getMCMistagEfficiency(pt, eta));
          }
        }
        */
      }
      ret.tagged.push_back(tagged);
      ret.genuine.push_back(genuine);
      ret.scaleFactor.push_back(scaleFactor);
      ret.uncertainty.push_back(uncertainty);

    }
    return ret;
  }

  double BTagging::BTaggingScaleFactor::calculateScaleFactor(const Info& info) {
    double scaleFactor = 1.0;
    for(size_t i=0; i<info.size(); ++i) {
      scaleFactor *= info.scaleFactor[i];
    }
    return scaleFactor;
  }

  double BTagging::BTaggingScaleFactor::calculateAbsoluteUncertainty(const Info& info) {
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

  double BTagging::BTaggingScaleFactor::calculateRelativeUncertainty(const Info& info) {
    // FIXME this is a dirty hack, numbers are from BTV-11-004 (see accompanying AN's)
    return calculateAbsoluteUncertainty(info) / calculateScaleFactor(info);
    // FIXME end of dirty hack
    // old numbers
    /*
    double berror = 0; // b-jets
    double lerror = 0; // light q/g jets

    for(size_t i=0; i<info.size(); ++i) {
      if(info.genuine[i])
        berror += info.uncertainty[i];
      else
        lerror += info.uncertainty[i];
    }

    return std::sqrt(berror*berror + lerror*lerror);
    */
  }


  double BTagging::BTaggingScaleFactor::getBtagScaleFactor(double pt,double eta) const {
        if(btagdb==0){
                int myIndex = obtainIndex(fPtBinsB, pt);
                return fScaleFactorB[myIndex];
        }else{
                return btagdb->getScaleFactors(pt,eta).btagScaleFactor();
        }
  }
  double BTagging::BTaggingScaleFactor::getBtagScaleFactorError(double pt,double eta) const {
        if(btagdb==0){
                return fScaleFactorUncertaintyB[0];
        }else{
                return btagdb->getScaleFactors(pt,eta).btagScaleFactorError();
        }
  }
  double BTagging::BTaggingScaleFactor::getMistagScaleFactor(double pt,double eta) const {
        if(btagdb==0){
                int myIndex = obtainIndex(fPtBinsB, pt);
                return fScaleFactorL[myIndex];
        }else{
                return btagdb->getScaleFactors(pt,eta).mistagScaleFactor();
        }
  }
  double BTagging::BTaggingScaleFactor::getMistagScaleFactorError(double pt,double eta) const {
        if(btagdb==0){   
                return fScaleFactorUncertaintyL[0];      
        }else{
                return btagdb->getScaleFactors(pt,eta).mistagScaleFactorError();
        }                                                                                                
  }
  double BTagging::BTaggingScaleFactor::getMCBtagEfficiency(double pt,double eta) const {
        if(btagdb==0){
                int myIndex = obtainIndex(fPtBinsB, pt);
                return fEpsilonMCB[myIndex];
        }else{
		return btagdb->getScaleFactors(pt,eta).btagEfficiency();
        }
  }
  double BTagging::BTaggingScaleFactor::getMCMistagEfficiency(double pt,double eta) const {
        if(btagdb==0){
                int myIndex = obtainIndex(fPtBinsB, pt);
                return fEpsilonMCL[myIndex];
        }else{
                return btagdb->getScaleFactors(pt,eta).mistagEfficiency();
        }
  }


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
    fTaggedTwoTaggedJets(eventCounter.addSubCounter("b-tagging", "two b-tagged jets"))
    //    fTaggedEtaCutSubCount(eventCounter.addSubCounter("b-tagging", "eta  cut")),
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("Btagging");
    hDiscr = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_bdiscriminator", ("b discriminator "+fDiscriminator).c_str(), 100, -10, 10);
    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet_pt", "bjet_pt", 100, 0., 500.);
    hDiscrB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "RealBjet_discrim", ("realm b discrimi. "+fDiscriminator).c_str(), 100, -10, 10);
    hPtBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_pt", "realbjetCSVM_pt", 100, 0., 500.);
    hEtaBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_eta", "realbjetCSVM_eta", 100, -5., 5.);
    hPtBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_pt", "realbjetCSVT_pt", 100, 0., 500.);
    hEtaBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_eta", "realbjetCSVT_eta", 100, -5., 5.);
    hPtBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_pt", "realbjetNotag_pt", 100, 0., 500.);
    hEtaBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_eta", "realbjetNotag_eta", 100, -5., 5.);
    hDiscrQ = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "RealQjet_discrim", ("realm b discrimi. "+fDiscriminator).c_str(), 100, -10, 10);
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

    // OBSOLETE
    // BTagging scale factors for b-flavor jets (source: BTV-11-001)
    double fScaleFactorBFlavor = 0.95;
    double fScaleFactorBFlavorUncertainty = 0.05;
    fBTaggingScaleFactor.addBFlavorData(30., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .671);
    fBTaggingScaleFactor.addBFlavorData(40., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .741);
    fBTaggingScaleFactor.addBFlavorData(50., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .779);
    fBTaggingScaleFactor.addBFlavorData(60., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .802);
    fBTaggingScaleFactor.addBFlavorData(70., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .826);
    fBTaggingScaleFactor.addBFlavorData(80., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .840);
    fBTaggingScaleFactor.addBFlavorData(100., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .840);
    fBTaggingScaleFactor.addBFlavorData(120., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .856);
    // BTagging scale factors for non-b-flavor jets (source: BTV-11-001)
    double fScaleFactorLightFlavor = 1.10;
    double fScaleFactorLightFlavorUncertainty = 0.12;
    fBTaggingScaleFactor.addNonBFlavorData(30., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.055);
    fBTaggingScaleFactor.addNonBFlavorData(40., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.076);
    fBTaggingScaleFactor.addNonBFlavorData(50., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.095);
    fBTaggingScaleFactor.addNonBFlavorData(60., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.116);
    fBTaggingScaleFactor.addNonBFlavorData(70., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.128);
    fBTaggingScaleFactor.addNonBFlavorData(80., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.151);
    fBTaggingScaleFactor.addNonBFlavorData(90., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.170);
    fBTaggingScaleFactor.addNonBFlavorData(100., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.186);
    fBTaggingScaleFactor.addNonBFlavorData(110., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.202);
    fBTaggingScaleFactor.addNonBFlavorData(120., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.213);
    fBTaggingScaleFactor.addNonBFlavorData(130., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.226);
    fBTaggingScaleFactor.addNonBFlavorData(140., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.238);
    fBTaggingScaleFactor.addNonBFlavorData(150., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.248);
    fBTaggingScaleFactor.addNonBFlavorData(160., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.260);
    fBTaggingScaleFactor.addNonBFlavorData(170., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.271);
    fBTaggingScaleFactor.addNonBFlavorData(180., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.279);
    fBTaggingScaleFactor.addNonBFlavorData(190., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.286);
    fBTaggingScaleFactor.addNonBFlavorData(200., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.294);
    fBTaggingScaleFactor.addNonBFlavorData(210., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.303);
    fBTaggingScaleFactor.addNonBFlavorData(220., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.311);
    fBTaggingScaleFactor.addNonBFlavorData(230., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.319);
    fBTaggingScaleFactor.addNonBFlavorData(240., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.321);
    fBTaggingScaleFactor.addNonBFlavorData(250., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.329);
    fBTaggingScaleFactor.addNonBFlavorData(260., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.335);
    fBTaggingScaleFactor.addNonBFlavorData(270., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.338);
    fBTaggingScaleFactor.addNonBFlavorData(280., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.347);
    fBTaggingScaleFactor.addNonBFlavorData(290., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.355);
    fBTaggingScaleFactor.addNonBFlavorData(300., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.358);
    fBTaggingScaleFactor.addNonBFlavorData(310., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.361);
    fBTaggingScaleFactor.addNonBFlavorData(320., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.367);
    fBTaggingScaleFactor.addNonBFlavorData(330., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.365);
    fBTaggingScaleFactor.addNonBFlavorData(340., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.371);
    fBTaggingScaleFactor.addNonBFlavorData(350., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.373);
    fBTaggingScaleFactor.addNonBFlavorData(360., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.374);
    fBTaggingScaleFactor.addNonBFlavorData(370., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.377);
    fBTaggingScaleFactor.addNonBFlavorData(380., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.376);
    fBTaggingScaleFactor.addNonBFlavorData(390., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.380);
    fBTaggingScaleFactor.addNonBFlavorData(400., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.385);
    fBTaggingScaleFactor.addNonBFlavorData(410., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.387);
    fBTaggingScaleFactor.addNonBFlavorData(420., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.391);
    fBTaggingScaleFactor.addNonBFlavorData(430., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.392);
    fBTaggingScaleFactor.addNonBFlavorData(440., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.389);
    fBTaggingScaleFactor.addNonBFlavorData(450., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.396);
    fBTaggingScaleFactor.addNonBFlavorData(460., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.396);
    fBTaggingScaleFactor.addNonBFlavorData(470., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.402);
    fBTaggingScaleFactor.addNonBFlavorData(480., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.396);
    fBTaggingScaleFactor.addNonBFlavorData(490., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.402);

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
    bool bJetIsMCb = false;
    bool bJetIsMCc = false;
    bool bJetIsMCLightQuark = false;
    bool bMatch = false;
    bool qMatch = false;

    if(btagDB) btagDB->setup(iSetup);

    // Calculate 
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      increment(fAllSubCount);

//       if (!iEvent.isRealData()) {
// 	edm::Handle <reco::GenParticleCollection> genParticles;
// 	iEvent.getByLabel("genParticles", genParticles);
// 
// 	for (size_t i=0; i < genParticles->size(); ++i){
// 	  const reco::Candidate & p = (*genParticles)[i];
// 	  int id = p.pdgId();
// 	  if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
// 	  //	  printImmediateMothers(p);
// 	  double deltaR = ROOT::Math::VectorUtil::DeltaR(iJet->p4(),p.p4() );
// 	  if ( deltaR < 0.2) bMatch = true;
// 	  //	  std::cout << "  bmatch   "  <<  p.pdgId()   << std::endl;
// 	} 
// 
// 	for (size_t i=0; i < genParticles->size(); ++i){
// 	  const reco::Candidate & p = (*genParticles)[i];
// 	  int id = p.pdgId();
// 	  if ( abs(id) > 4 &&  p.pdgId() != 21 )continue;
// 	  if ( hasImmediateMother(p,1) || hasImmediateMother(p,-1) )continue;
// 	  if ( hasImmediateMother(p,2) || hasImmediateMother(p,-2) )continue;
// 	  if ( hasImmediateMother(p,3) || hasImmediateMother(p,-3) )continue;
// 	  if ( hasImmediateMother(p,4) || hasImmediateMother(p,-4) )continue;
// 	  double deltaR = ROOT::Math::VectorUtil::DeltaR(iJet->p4(),p.p4() );
// 	  if ( deltaR < 0.2) qMatch = true;
// 	  //	  std::cout << "  qmatch   "  <<  p.pdgId()   << std::endl;
// 
// 	}

      if (!iEvent.isRealData()) {
        int myFlavor = std::abs(iJet->partonFlavour());
        if (myFlavor == 5) {
          bJetIsMCb = true;
        } else if (myFlavor == 4) {
          bJetIsMCc = true;
        } else {
          bJetIsMCLightQuark = true;
        }
      }

      if (bJetIsMCb)   increment(fTaggedAllRealBJetsSubCount);

      float discr = iJet->bDiscriminator(fDiscriminator);
      //      if (bmatchedJet ) {
//       if (bMatch ) {
// 	hPtBnoTag->Fill(iJet->pt());
// 	hEtaBnoTag->Fill(iJet->eta());
// 	//	std::cout << " discr. b-matched   "  << discr << " discr cut   "  << fDiscrCut  << std::endl;	
// 	//	if(discr > fDiscrCut ) {
// 	if(discr > 0.898) {
// 	  hPtBCSVT->Fill(iJet->pt());
// 	  hEtaBCSVT->Fill(iJet->eta());
// 	}
// 	if(discr > 0.679) {
// 	  hPtBCSVM->Fill(iJet->pt());
// 	  hEtaBCSVM->Fill(iJet->eta());
// 	}
// 	hDiscrB->Fill(discr);
//       }
//       //      if (qmatchedJet ) {
//       if (qMatch ) {
// 	hPtQnoTag->Fill(iJet->pt());
// 	hEtaQnoTag->Fill(iJet->eta());
// 	//	std::cout << " discr. q-matched  "  << discr <<  discr << " discr cut   "  << fDiscrCut << std::endl;
// 	//	if(discr > fDiscrCut ) {
// 	if(discr > 0.898) {
// 	  hPtQCSVT->Fill(iJet->pt());
// 	  hEtaQCSVT->Fill(iJet->eta());
// 	}
// 	if(discr > 0.679) {
// 	  hPtQCSVM->Fill(iJet->pt());
// 	  hEtaQCSVM->Fill(iJet->eta());
// 	}
// 	hDiscrQ->Fill(discr);
//       }

      // pt cut
      if(iJet->pt() < fPtCut ) continue;
      increment(fTaggedPtCutSubCount);

      // eta cut
      if(fabs(iJet->eta()) > fEtaCut ) continue;
      increment(fTaggedEtaCutSubCount);

      // Analyze MC tag / mistag efficiencies
      analyzeMCTagEfficiencyByJetFlavour(iJet, bJetIsMCb, bJetIsMCc, bJetIsMCLightQuark);

      // discriminator cut
      hDiscr->Fill(discr);
      if (discr > fLeadingDiscrCut) {
        output.fSelectedJets.push_back(iJet);
      } else if (discr > fSubLeadingDiscrCut){
        output.fSelectedSubLeadingJets.push_back(iJet);
      } else {
        continue;
      }
      increment(fTaggedSubCount);

      hPt->Fill(iJet->pt());
      hEta->Fill(iJet->eta());

      if (discr > output.fMaxDiscriminatorValue)
        output.fMaxDiscriminatorValue = discr;

      //++passed;
      if (bJetIsMCb) increment(fTaggedTaggedRealBJetsSubCount);

    } // end of jet loop

    // Calculate scale factor for MC events
    if (!iEvent.isRealData())
      calculateScaleFactor(jets, output);

    // Fill histograms
    hNumberOfBtaggedJets->Fill(output.fSelectedJets.size());
    hNumberOfBtaggedJetsIncludingSubLeading->Fill(output.fSelectedJets.size()+output.fSelectedSubLeadingJets.size());
    output.iNBtags = output.fSelectedJets.size();

    ////////////////////////////////
    if(output.fSelectedJets.size() > 0) {
      hPt1->Fill(output.fSelectedJets[0]->pt());
      hEta1->Fill(output.fSelectedJets[0]->eta());
    }
    if(output.fSelectedJets.size() > 1) {
      hPt2->Fill(output.fSelectedJets[1]->pt());
      hEta2->Fill(output.fSelectedJets[1]->eta());
    }
       // plot deltaPhi(bjet,tau jet)
    //      double deltaPhi = -999;    
	//      if ( met->et()>  fMetCut) {
      //	  deltaPhi = DeltaPhi::reconstruct(*(iJet), *(met));
      //	  hDeltaPhiJetMet->Fill(deltaPhi*57.3);
      //      }
    if(output.fSelectedJets.size() == 0)   increment(fTaggedNoTaggedJet);
    else if(output.fSelectedJets.size() == 1)   increment(fTaggedOneTaggedJet);
    else if(output.fSelectedJets.size() == 2)   increment(fTaggedTwoTaggedJets);

    output.fPassedEvent= fNumberOfBJets.passedCut(output.fSelectedJets.size());
    if (output.fPassedEvent)
      increment(fTaggedCount);

    return output;
  }

  void BTagging::analyzeMCTagEfficiencyByJetFlavour(const edm::Ptr<pat::Jet>& jet, const bool isBJet, const bool isCJet, const bool isLightJet) {
    // Plot histograms for leading discriminator
    if (isBJet) {
      hMCAllBJetsByPt->Fill(jet->pt());
      hMCAllBJetsByPtAndEta->Fill(jet->pt(),jet->eta());
    } else if (isCJet) {
      hMCAllCJetsByPt->Fill(jet->pt());
      hMCAllCJetsByPtAndEta->Fill(jet->pt(),jet->eta());
    } else if (isLightJet) {
      hMCAllLightJetsByPt->Fill(jet->pt());
      hMCAllLightJetsByPtAndEta->Fill(jet->pt(),jet->eta());
    }
    bool myPassedLeadingDiscriminator = jet->bDiscriminator(fDiscriminator) > fLeadingDiscrCut;
    if (myPassedLeadingDiscriminator) {
      // jet passed b tag
      if (isBJet) {
        hMCBtaggedBJetsByPt->Fill(jet->pt());
        hMCBtaggedBJetsByPtAndEta->Fill(jet->pt(),jet->eta());
      } else if (isCJet) {
        hMCBtaggedCJetsByPt->Fill(jet->pt());
        hMCBtaggedCJetsByPtAndEta->Fill(jet->pt(),jet->eta());
      } else if (isLightJet) {
        hMCBtaggedLightJetsByPt->Fill(jet->pt());
        hMCBtaggedLightJetsByPtAndEta->Fill(jet->pt(),jet->eta());
      }
    } else {
      // jet did not pass b tag
      if (isBJet) {
        hMCBmistaggedBJetsByPt->Fill(jet->pt());
        hMCBmistaggedBJetsByPtAndEta->Fill(jet->pt(),jet->eta());
      } else if (isCJet) {
        hMCBmistaggedCJetsByPt->Fill(jet->pt());
        hMCBmistaggedCJetsByPtAndEta->Fill(jet->pt(),jet->eta());
      } else if (isLightJet) {
        hMCBmistaggedLightJetsByPt->Fill(jet->pt());
        hMCBmistaggedLightJetsByPtAndEta->Fill(jet->pt(),jet->eta());
      }
    }
  }

  BTagging::Info BTagging::getPerJetInfo(const edm::PtrVector<pat::Jet>& jets, const Data& btagData, bool isData) const {
    return fBTaggingScaleFactor.getPerJetInfo(jets, btagData, isData);
  }
  
  void BTagging::calculateScaleFactor(const edm::PtrVector<pat::Jet>& jets, BTagging::Data& btagData) {
    Info jetInfos = fBTaggingScaleFactor.getPerJetInfo(jets, btagData, false); // assume this method is called only for MC!
    btagData.fScaleFactor = fBTaggingScaleFactor.calculateScaleFactor(jetInfos);
    btagData.fScaleFactorAbsoluteUncertainty = fBTaggingScaleFactor.calculateAbsoluteUncertainty(jetInfos);
    btagData.fScaleFactorRelativeUncertainty = fBTaggingScaleFactor.calculateRelativeUncertainty(jetInfos);

    // Do the variation, if asked
    if(fVariationEnabled) {
      btagData.fScaleFactor += fVariationShiftBy*btagData.fScaleFactorAbsoluteUncertainty;
      // these are meaningless after the variation
      btagData.fScaleFactorAbsoluteUncertainty = 0;
      btagData.fScaleFactorRelativeUncertainty = 0;
    }

    /*std::cout << "btagSF debug: jets=" << jets.size() << " bjets=" << bjets.size() << " nb=" << nBJetsPassed << ", nbf pT=";
    for (std::vector<double>::iterator it = fBJetsFailedPt.begin(); it != fBJetsFailedPt.end(); ++it) { std::cout << " " << *it; }
    std::cout << " nl=" << nLightJetsPassed << ", nlf pT=";
    for (std::vector<double>::iterator it = fLightJetsFailedPt.begin(); it != fLightJetsFailedPt.end(); ++it) { std::cout << " " << *it; }
    std::cout << " scalefactor= " << fScaleFactor << ", rel.syst.=" << fBTaggingScaleFactor.getRelativeUncertainty(nBJetsPassed, nLightJetsPassed, fBJetsFailedPt, fLightJetsFailedPt) << std::endl;*/

    //std::cout << "bjets=" << nBJets << ", light jets=" << nLightJets << ", scale factor=" << fScaleFactor << std::endl;
  }

  void BTagging::fillScaleFactorHistograms(BTagging::Data& input) {
    hScaleFactor->Fill(input.getScaleFactor());
    hBTagAbsoluteUncertainty->Fill(input.getScaleFactorAbsoluteUncertainty());
    hBTagRelativeUncertainty->Fill(input.getScaleFactorRelativeUncertainty());
  }

}
