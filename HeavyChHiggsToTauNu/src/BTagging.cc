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

  size_t BTagging::BTaggingScaleFactor::obtainIndex(std::vector<double>& table, double pt) {
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

////  double BTagging::BTaggingScaleFactor::getWeight(std::vector<double>& fPassedBpT, std::vector<double>& fPassedLpT, std::vector<double>& nFailedBpT, std::vector<double>& nFailedLpT) {
  double BTagging::BTaggingScaleFactor::getWeight(edm::PtrVector<pat::Jet> fPassedBpT,
                                                  edm::PtrVector<pat::Jet> fPassedLpT,
                                                  edm::PtrVector<pat::Jet> fFailedBpT,
                                                  edm::PtrVector<pat::Jet> fFailedLpT) {
    double myValue = 1.0;
    // b-flavor jets that have passed b-tagging
////    myValue *= std::pow(fScaleFactorB[0], nPassedB);
    for(edm::PtrVector<pat::Jet>::const_iterator it = fPassedBpT.begin(); it != fPassedBpT.end(); ++it) {
      myValue *= getBtagScaleFactor((*it)->pt(),(*it)->eta());
    }    
    // b-flavor jets that have not passed b-tagging
    for(edm::PtrVector<pat::Jet>::const_iterator it = fFailedBpT.begin(); it != fFailedBpT.end(); ++it) {
      // obtain index for pT table)
////      int myIndex = obtainIndex(fPtBinsB, *it);
////      myValue *= (1.-fScaleFactorB[myIndex]*fEpsilonMCB[myIndex]) / (1.-fEpsilonMCB[myIndex]);
      myValue *= (1.-getBtagScaleFactor((*it)->pt(),(*it)->eta())*getMCBtagEfficiency((*it)->pt(),(*it)->eta())) / (1.-getMCBtagEfficiency((*it)->pt(),(*it)->eta()));
    }
    // non-b-flavor jets that have passed b-tagging
    for(edm::PtrVector<pat::Jet>::const_iterator it = fPassedLpT.begin(); it != fPassedLpT.end(); ++it) {
      myValue *= getMistagScaleFactor((*it)->pt(),(*it)->eta());
    }
////    myValue *= std::pow(fScaleFactorL[0], nPassedL);
    // non-b-flavor jets that have not passed b-tagging
    for(edm::PtrVector<pat::Jet>::const_iterator it = fFailedLpT.begin(); it != fFailedLpT.end(); ++it) {
      // obtain index for pT table
////      int myIndex = obtainIndex(fPtBinsL, *it);
////      myValue *= (1.-fScaleFactorL[myIndex]*fEpsilonMCL[myIndex]) / (1.-fEpsilonMCL[myIndex]);
      myValue *= (1.-getMistagScaleFactor((*it)->pt(),(*it)->eta())*getMCMistagEfficiency((*it)->pt(),(*it)->eta())) / (1.-getMCMistagEfficiency((*it)->pt(),(*it)->eta()));
    }
    // Return calculated value
    return myValue;
  }
  
//  double BTagging::BTaggingScaleFactor::getRelativeUncertainty(std::vector<double>& fPassedBpT, std::vector<double>& fPassedLpT, std::vector<double>& nFailedBpT, std::vector<double>& nFailedLpT) {
  double BTagging::BTaggingScaleFactor::getRelativeUncertainty(edm::PtrVector<pat::Jet> fPassedBpT,
                                                               edm::PtrVector<pat::Jet> fPassedLpT,
                                                               edm::PtrVector<pat::Jet> fFailedBpT,
                                                               edm::PtrVector<pat::Jet> fFailedLpT) {

    // b-flavor jets and non-b-flavor jets are uncorrelated --> error propagation with F=F(scalefactorB, scalefactorL)
    // Notice the nice anti-correlation between the passed and failed components
/*
    // b-flavor jets
////    double myBTerm = static_cast<double>(nPassedB)/fScaleFactorB[0];
    double myBTerm = 0;
    for(std::vector<double>::iterator it = fPassedBpT.begin(); it != fPassedBpT.end(); ++it) {
      myBTerm += 1/getBtagScaleFactor(*it,0);
    }
    for(std::vector<double>::iterator it = nFailedBpT.begin(); it != nFailedBpT.end(); ++it) {
      // obtain index for pT table
////      int myIndex = obtainIndex(fPtBinsB, *it);
////      myBTerm -= fEpsilonMCB[myIndex]/(1.-fScaleFactorB[myIndex]*fEpsilonMCB[myIndex]);
	myBTerm -= getMCBtagEfficiency(*it,0)/(1.-getBtagScaleFactor(*it,0)*getMCBtagEfficiency(*it,0));
    }
    myBTerm *= fScaleFactorUncertaintyB[0];
    // l-flavor jets
////    double myLTerm = static_cast<double>(nPassedL)/fScaleFactorL[0];
    for(std::vector<double>::iterator it = fPassedLpT.begin(); it != fPassedLpT.end(); ++it) {
      myLTerm += getMistagScaleFactor(*it,0);
    }
    for(std::vector<double>::iterator it = nFailedLpT.begin(); it != nFailedLpT.end(); ++it) {
      // obtain index for pT table
////      int myIndex = obtainIndex(fPtBinsL, *it);
////      myLTerm -= fEpsilonMCL[myIndex]/(1.-fScaleFactorL[myIndex]*fEpsilonMCL[myIndex]);
	myLTerm -= getMCMistagEfficiency(*it,0)/(1.-getMistagScaleFactor(*it,0)*getMCMistagEfficiency(*it,0));
    }
    myLTerm *= fScaleFactorUncertaintyL[0];
    // Return result
    return std::sqrt(std::pow(myBTerm,2) + std::pow(myLTerm,2));
*/
	
	// b-jets
	double berror = 0;
	for(edm::PtrVector<pat::Jet>::const_iterator it = fPassedBpT.begin(); it != fPassedBpT.end(); ++it) {
		berror += getBtagScaleFactorError((*it)->pt(),(*it)->eta())/getBtagScaleFactor((*it)->pt(),(*it)->eta());
	}
        for(edm::PtrVector<pat::Jet>::const_iterator it = fFailedBpT.begin(); it != fFailedBpT.end(); ++it) {
		berror -= getBtagScaleFactorError((*it)->pt(),(*it)->eta())*getMCBtagEfficiency((*it)->pt(),(*it)->eta())/(1-getBtagScaleFactor((*it)->pt(),(*it)->eta())*getMCBtagEfficiency((*it)->pt(),(*it)->eta()));
	}

	// light q/g jets
	double lerror = 0;
        for(edm::PtrVector<pat::Jet>::const_iterator it = fPassedLpT.begin(); it != fPassedLpT.end(); ++it) {
                berror += getMistagScaleFactorError((*it)->pt(),(*it)->eta())/getMistagScaleFactor((*it)->pt(),(*it)->eta());
        }                                                                                                                                              
        for(edm::PtrVector<pat::Jet>::const_iterator it = fFailedLpT.begin(); it != fFailedLpT.end(); ++it) {
                berror -= getMistagScaleFactorError((*it)->pt(),(*it)->eta())*getMCMistagEfficiency((*it)->pt(),(*it)->eta())/(1-getMistagScaleFactor((*it)->pt(),(*it)->eta())*getMCMistagEfficiency((*it)->pt(),(*it)->eta()));
        }
	return std::sqrt(std::pow(berror,2) + std::pow(lerror,2));
  }

  double BTagging::BTaggingScaleFactor::getAbsoluteUncertainty(edm::PtrVector<pat::Jet> fPassedBpT,
                                                               edm::PtrVector<pat::Jet> fPassedLpT,
                                                               edm::PtrVector<pat::Jet> fFailedBpT,
                                                               edm::PtrVector<pat::Jet> fFailedLpT) {

////  double BTagging::BTaggingScaleFactor::getAbsoluteUncertainty(std::vector<double>& fPassedBpT, std::vector<double>& fPassedLpT, std::vector<double>& fFailedBpT, std::vector<double>& fFailedLpT) {
    return getWeight(fPassedBpT, fPassedLpT, fFailedBpT, fFailedLpT) * getRelativeUncertainty(fPassedBpT, fPassedLpT, fFailedBpT, fFailedLpT);
  }

  double BTagging::BTaggingScaleFactor::getBtagScaleFactor(double pt,double eta){
        if(btagdb==0){
                int myIndex = obtainIndex(fPtBinsB, pt);
                return fScaleFactorB[myIndex];
        }else{
                return btagdb->getScaleFactors(pt,eta).btagScaleFactor();
        }
  }
  double BTagging::BTaggingScaleFactor::getBtagScaleFactorError(double pt,double eta){
        if(btagdb==0){
                return fScaleFactorUncertaintyB[0];
        }else{
                return btagdb->getScaleFactors(pt,eta).btagScaleFactorError();
        }
  }
  double BTagging::BTaggingScaleFactor::getMistagScaleFactor(double pt,double eta){
        if(btagdb==0){
                int myIndex = obtainIndex(fPtBinsB, pt);
                return fScaleFactorL[myIndex];
        }else{
                return btagdb->getScaleFactors(pt,eta).mistagScaleFactor();
        }
  }
  double BTagging::BTaggingScaleFactor::getMistagScaleFactorError(double pt,double eta){
        if(btagdb==0){   
                return fScaleFactorUncertaintyL[0];      
        }else{
                return btagdb->getScaleFactors(pt,eta).mistagScaleFactorError();
        }                                                                                                
  }
  double BTagging::BTaggingScaleFactor::getMCBtagEfficiency(double pt,double eta){
        if(btagdb==0){
                int myIndex = obtainIndex(fPtBinsB, pt);
                return fEpsilonMCB[myIndex];
        }else{
		return btagdb->getScaleFactors(pt,eta).btagEfficiency();
        }
  }
  double BTagging::BTaggingScaleFactor::getMCMistagEfficiency(double pt,double eta){
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
    hDiscr = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "jet_bdiscriminator", ("b discriminator "+fDiscriminator).c_str(), 100, -10, 10);
    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "bjet_pt", "bjet_pt", 100, 0., 500.);
    hDiscrB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "RealBjet_discrim", ("realm b discrimi. "+fDiscriminator).c_str(), 100, -10, 10);
    hPtBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_pt", "realbjetCSVM_pt", 100, 0., 500.);
    hEtaBCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVM_eta", "realbjetCSVM_eta", 100, -5., 5.);
    hPtBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_pt", "realbjetCSVT_pt", 100, 0., 500.);
    hEtaBCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetCSVT_eta", "realbjetCSVT_eta", 100, -5., 5.);
    hPtBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_pt", "realbjetNotag_pt", 100, 0., 500.);
    hEtaBnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realbjetNotag_eta", "realbjetNotag_eta", 100, -5., 5.);
    hDiscrQ = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "RealBjet_discrim", ("realm b discrimi. "+fDiscriminator).c_str(), 100, -10, 10);
    hPtQCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVM_pt", "realqjetCSVM_pt", 100, 0., 500.);
    hEtaQCSVM = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVM_eta", "realqjetCSVM_pt", 100, -5., 5.);
    hPtQCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVT_pt", "realqjetCSVT_pt", 100, 0., 500.);
    hEtaQCSVT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetCSVT_eta", "realqjetCSVT_pt", 100, -5., 5.);
    hPtQnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetNotag_pt", "realqjetNotag_pt", 100, 0., 500.);
    hEtaQnoTag = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "realqjetNotag_eta", "realqjetNotag_pt", 100, -5., 5.);
    hPt1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet1_pt", "bjet1_pt", 100, 0., 500.);
    hPt2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet2_pt", "bjet2_pt", 100, 0., 500.);
    hEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "bjet_eta", "bjet_pt", 100, -5., 5.);
    hEta1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet1_eta", "bjet1_pt", 100, -5., 5.);
    hEta2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjet2_eta", "bjet2_pt", 100, -5., 5.);
    hNumberOfBtaggedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "NumberOfBtaggedJets", "NumberOfBtaggedJets", 10, 0., 10.);
    hNumberOfBtaggedJetsIncludingSubLeading = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "NumberOfBtaggedJetsIncludingSubLeading", "NumberOfBtaggedJetsIncludingSubLeading", 10, 0., 10.);
    hMCMatchForPassedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "MCMatchForPassedJets", "MCMatchForPassedJets;;N_{jets}", 3, 0., 3.);
    if (hMCMatchForPassedJets->isActive()) {
      hMCMatchForPassedJets->GetXaxis()->SetBinLabel(1, "b jet");
      hMCMatchForPassedJets->GetXaxis()->SetBinLabel(2, "light jet");
      hMCMatchForPassedJets->GetXaxis()->SetBinLabel(3, "no match");
    }

    // Scale factor histograms (needed for evaluating syst. uncertainty of btagging in datacard generator)
    hScaleFactor = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "scaleFactor", "scaleFactor;b-tag/mistag scale factor;N_{events}/0.05", 100, 0., 5.);
    hBTagRelativeUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "BTagRelativeUncertainty", "BTagRelativeUncertainty;Relative Uncertainty;N_{events}", 3000, 0., 3.);
    hBTagAbsoluteUncertainty = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "BTagAbsoluteUncertainty", "BTagAbsoluteUncertainty;Absolute Uncertainty;N_{events}", 3000, 0., 3.);

    // BTagging scale factors from DB
    if(FactorsFromDB) {
      btagDB = new BTaggingScaleFactorFromDB(iConfig);
      fBTaggingScaleFactor.UseDB(btagDB);
    }
    else
      btagDB = 0;

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
    bool bmatchedJet = false;
    bool qmatchedJet = false;
    bool bMatch = false;
    bool qMatch = false;

    if(btagDB) btagDB->setup(iSetup);

    // Calculate 
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      increment(fAllSubCount);

      if (!iEvent.isRealData()) {
	edm::Handle <reco::GenParticleCollection> genParticles;
	iEvent.getByLabel("genParticles", genParticles);

	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();
	  if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	  //	  printImmediateMothers(p);
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(iJet->p4(),p.p4() );
	  if ( deltaR < 0.2) bMatch = true;
	  //	  std::cout << "  bmatch   "  <<  p.pdgId()   << std::endl;
	} 

	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();
	  if ( abs(id) > 4 &&  p.pdgId() != 21 )continue;
	  if ( hasImmediateMother(p,1) || hasImmediateMother(p,-1) )continue;
	  if ( hasImmediateMother(p,2) || hasImmediateMother(p,-2) )continue;
	  if ( hasImmediateMother(p,3) || hasImmediateMother(p,-3) )continue;
	  if ( hasImmediateMother(p,4) || hasImmediateMother(p,-4) )continue;
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(iJet->p4(),p.p4() );
	  if ( deltaR < 0.2) qMatch = true;
	  //	  std::cout << "  qmatch   "  <<  p.pdgId()   << std::endl;

	}
	//////////////////////////////////////////////
        int myFlavor = std::abs(iJet->partonFlavour());
        if (myFlavor == 5) {
          bmatchedJet = true;
        } else {
          qmatchedJet = true;
        }
      }
      if( bmatchedJet )   increment(fTaggedAllRealBJetsSubCount);

      float discr = iJet->bDiscriminator(fDiscriminator);
      //      if (bmatchedJet ) {
      if (bMatch ) {
	hPtBnoTag->Fill(iJet->pt());
	hEtaBnoTag->Fill(iJet->eta());
	//	std::cout << " discr. b-matched   "  << discr << " discr cut   "  << fDiscrCut  << std::endl;	
	//	if(discr > fDiscrCut ) {
	if(discr > 0.898) {
	  hPtBCSVT->Fill(iJet->pt());
	  hEtaBCSVT->Fill(iJet->eta());
	}
	if(discr > 0.679) {
	  hPtBCSVM->Fill(iJet->pt());
	  hEtaBCSVM->Fill(iJet->eta());
	}
	hDiscrB->Fill(discr);
      }
      //      if (qmatchedJet ) {
      if (qMatch ) {
	hPtQnoTag->Fill(iJet->pt());
	hEtaQnoTag->Fill(iJet->eta());
	//	std::cout << " discr. q-matched  "  << discr <<  discr << " discr cut   "  << fDiscrCut << std::endl;
	//	if(discr > fDiscrCut ) {
	if(discr > 0.898) {
	  hPtQCSVT->Fill(iJet->pt());
	  hEtaQCSVT->Fill(iJet->eta());
	}
	if(discr > 0.679) {
	  hPtQCSVM->Fill(iJet->pt());
	  hEtaQCSVM->Fill(iJet->eta());
	}
	hDiscrQ->Fill(discr);
      }

      // pt cut
      if(iJet->pt() < fPtCut ) continue;
      increment(fTaggedPtCutSubCount);
      // eta cut
      if(fabs(iJet->eta()) > fEtaCut ) continue;
      increment(fTaggedEtaCutSubCount);
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
      if( bmatchedJet )   increment(fTaggedTaggedRealBJetsSubCount);

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

  void BTagging::calculateScaleFactor(const edm::PtrVector<pat::Jet>& jets, BTagging::Data& btagData) {
    // Count number of b jets and light jets
////    int nBJetsPassed = 0;
////    std::vector<double> fBJetsPassedPt;
////    std::vector<double> fBJetsFailedPt;
////    int nLightJetsPassed = 0;
////    std::vector<double> fLightJetsPassedPt;
////    std::vector<double> fLightJetsFailedPt;

    edm::PtrVector<pat::Jet> fBJetsPassedPt;
    edm::PtrVector<pat::Jet> fBJetsFailedPt;
    edm::PtrVector<pat::Jet> fLightJetsPassedPt;
    edm::PtrVector<pat::Jet> fLightJetsFailedPt;

    // Loop over jets
    for (edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      bool myJetTaggedStatus = false;
      for (edm::PtrVector<pat::Jet>::const_iterator iBjet = btagData.fSelectedJets.begin(); iBjet != btagData.fSelectedJets.end(); ++iBjet) {
	if (iJet == *iBjet) myJetTaggedStatus = true;
      }
      if (myJetTaggedStatus) continue; // no double counting
      // analyze jet flavor
      int myFlavor = std::abs(iJet->partonFlavour());
      if (myFlavor == 5) {
        fBJetsFailedPt.push_back(iJet);
      } else {
        fLightJetsFailedPt.push_back(iJet);
      }
    }
    // Loop over b-tagged jets
    for (edm::PtrVector<pat::Jet>::const_iterator iter = btagData.fSelectedJets.begin(); iter != btagData.fSelectedJets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      // analyze jet flavor
      int myFlavor = std::abs(iJet->partonFlavour());
      if (myFlavor == 5) {
        fBJetsPassedPt.push_back(iJet);
        hMCMatchForPassedJets->Fill(1, 1.0);
      } else {
        fLightJetsPassedPt.push_back(iJet);
        hMCMatchForPassedJets->Fill(2, 1.0);
      }
    }
    // Calculate scalefactor
    // FIXME this is a dirty hack, numbers are from BTV-11-004 (see accompanying AN's)

    double mySF = 1.0;
    double mySFuncert = 0.0;
    for (edm::PtrVector<pat::Jet>::const_iterator iter = fBJetsPassedPt.begin(); iter != fBJetsPassedPt.end(); ++iter) {
      // This is independent of pT
      mySF *= 0.96;
      mySFuncert += 0.04*0.04;
    }
    for (edm::PtrVector<pat::Jet>::const_iterator iter = fLightJetsPassedPt.begin(); iter != fLightJetsPassedPt.end(); ++iter) {
      mySF *= 1.17;
      mySFuncert += 0.21*0.21;
    }

    btagData.fScaleFactor = mySF;
    btagData.fScaleFactorAbsoluteUncertainty = TMath::Sqrt(mySFuncert);
    btagData.fScaleFactorRelativeUncertainty = btagData.fScaleFactorAbsoluteUncertainty / mySF;
    // FIXME end of dirty hack

    /* this is the old code
    fScaleFactor = fBTaggingScaleFactor.getWeight(fBJetsPassedPt, fLightJetsPassedPt, fBJetsFailedPt, fLightJetsFailedPt);
    fScaleFactorRelativeUncertainty = fBTaggingScaleFactor.getRelativeUncertainty(fBJetsPassedPt, fLightJetsPassedPt, fBJetsFailedPt, fLightJetsFailedPt);
    fScaleFactorAbsoluteUncertainty = fBTaggingScaleFactor.getAbsoluteUncertainty(fBJetsPassedPt, fLightJetsPassedPt, fBJetsFailedPt, fLightJetsFailedPt);
    */

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
