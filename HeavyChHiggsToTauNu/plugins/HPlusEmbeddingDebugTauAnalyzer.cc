#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

class HPlusEmbeddingDebugTauAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusEmbeddingDebugTauAnalyzer(const edm::ParameterSet& iConfig);
  /// Default EDAnalyzer destructor
  ~HPlusEmbeddingDebugTauAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endJob();


  HPlus::EventWeight fEventWeight;
  HPlus::HistoWrapper fHistoWrapper;
  HPlus::EventCounter eventCounter;

  edm::InputTag jetSrc_;
  edm::InputTag genSrc_;

  HPlus::WeightReader pileupWeight_;

  const double tauPtCut_;
  const double tauEtaCut_;

  HPlus::Count cAllEvents;
  HPlus::Count cPUReweight;
  HPlus::Count cGenTaus;
  HPlus::Count cGenTausAcceptance;
  HPlus::Count cOneGenTau;
  HPlus::Count cThreeJets;

  HPlus::WrappedTH1 *hGenTauPt;
  HPlus::WrappedTH1 *hGenTauPtVisible;
  HPlus::WrappedTH1 *hGenTauEta;
  HPlus::WrappedTH1 *hGenTauPhi;

  HPlus::WrappedTH1 *hGenTauPt2;
  HPlus::WrappedTH1 *hGenTauPtVisible2;
  HPlus::WrappedTH1 *hGenTauEta2;
  HPlus::WrappedTH1 *hGenTauPhi2;

  HPlus::WrappedTH1 *hGenTauPt_AfterJets;
  HPlus::WrappedTH1 *hGenTauPtVisible_AfterJets;
  HPlus::WrappedTH1 *hGenTauEta_AfterJets;
  HPlus::WrappedTH1 *hGenTauPhi_AfterJets;
};

HPlusEmbeddingDebugTauAnalyzer::HPlusEmbeddingDebugTauAnalyzer(const edm::ParameterSet& iConfig):
  fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, fEventWeight, fHistoWrapper),
  jetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("jetSrc")),
  genSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genSrc")),
  pileupWeight_(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
  tauPtCut_(iConfig.getUntrackedParameter<double>("tauPtCut")),
  tauEtaCut_(iConfig.getUntrackedParameter<double>("tauEtaCut")),
  cAllEvents(eventCounter.addCounter("All events")),
  cPUReweight(eventCounter.addCounter("PU reweighting")),
  cGenTaus(eventCounter.addCounter(">= 1 gen tau")),
  cGenTausAcceptance(eventCounter.addCounter(">= 1 gen tau in acceptance")),
  cOneGenTau(eventCounter.addCounter("= 1 gen tau")),
  cThreeJets(eventCounter.addCounter("3 jets"))
{
  edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
  fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

  hGenTauPt = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_pt", "Pt", 400, 0, 400);
  hGenTauPtVisible = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_pt_visible", "Visible pt", 400, 0, 400);
  hGenTauEta = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_eta", "Eta", 44, -2.1, 2.1);
  hGenTauPhi = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_phi", "Phi", 128, -3.2, 3.2);

  hGenTauPt2 = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau2_pt", "Pt", 400, 0, 400);
  hGenTauPtVisible2 = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau2_pt_visible", "Visible pt", 400, 0, 400);
  hGenTauEta2 = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau2_eta", "Eta", 44, -2.1, 2.1);
  hGenTauPhi2 = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau2_phi", "Phi", 128, -3.2, 3.2);

  hGenTauPt_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_afterjet_pt", "Pt", 400, 0, 400);
  hGenTauPtVisible_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_afterjet_pt_visible", "Visible pt", 400, 0, 400);
  hGenTauEta_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_afterjet_eta", "eta", 44, -2.1, 2.1);
  hGenTauPhi_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "gentau_afterjet_phi", "phi", 128, -3.2, 3.2);
}

HPlusEmbeddingDebugTauAnalyzer::~HPlusEmbeddingDebugTauAnalyzer() {}

void HPlusEmbeddingDebugTauAnalyzer::endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}
void HPlusEmbeddingDebugTauAnalyzer::endJob() {
  eventCounter.endJob();
}

void HPlusEmbeddingDebugTauAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventWeight.beginEvent();
  increment(cAllEvents);

  const double myPileupWeight = pileupWeight_.getWeight(iEvent, iSetup);
  fEventWeight.multiplyWeight(myPileupWeight);
  increment(cPUReweight);

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(jetSrc_, hjets);

  edm::Handle<edm::View<reco::GenParticle> > hgenparticles;
  iEvent.getByLabel(genSrc_, hgenparticles);

  // Find W's
  const reco::GenParticle *W1 = 0;
  const reco::GenParticle *W2 = 0;

  for(edm::View<reco::GenParticle>::const_iterator iGen = hgenparticles->begin(); iGen != hgenparticles->end(); ++iGen) {
    const reco::GenParticle *gen = &(*iGen);
    if(std::abs(gen->pdgId()) != 24)
      continue;

    if(gen->mother() && std::abs(gen->mother()->pdgId()) != 6)
      continue;

    if(!W1)
      W1 = gen;
    else if(!W2)
      W2 = gen;
    else
      throw cms::Exception("Assert") << "Third W from top? at " << __FILE__ << ":" << __LINE__ << std::endl;
  }
  if(!W1)
    throw cms::Exception("Assert") << "W1 not found at " << __FILE__ << ":" << __LINE__  << std::endl;
  if(!W2)
    throw cms::Exception("Assert") << "W2 not found at " << __FILE__ << ":" << __LINE__  << std::endl;

  const reco::GenParticle *W1daughter = HPlus::GenParticleTools::findMaxNonNeutrinoDaughter(W1);
  const reco::GenParticle *W2daughter = HPlus::GenParticleTools::findMaxNonNeutrinoDaughter(W2);
  if(!W1daughter)
    throw cms::Exception("Assert") << "W1daughter not found at " << __FILE__ << ":" << __LINE__ << std::endl;
  if(!W2daughter)
    throw cms::Exception("Assert") << "W2daughter not found at " << __FILE__ << ":" << __LINE__ << std::endl;

  typedef std::vector<const reco::GenParticle *> GenVector;
  GenVector wtaus;
  GenVector tmp;
  if(std::abs(W1daughter->pdgId()) == 15)
    wtaus.push_back(W1daughter);
  if(std::abs(W2daughter->pdgId()) == 15)
    wtaus.push_back(W2daughter);

  if(wtaus.size() == 0)
    return;
  increment(cGenTaus);

  for(GenVector::const_iterator iGen = wtaus.begin(); iGen != wtaus.end(); ++iGen) {
    if(!((*iGen)->pt() > tauPtCut_ && std::abs((*iGen)->eta()) < tauEtaCut_))
      continue;
    tmp.push_back(*iGen);
  }
  wtaus.swap(tmp);
  tmp.clear();
  if(wtaus.size() == 0)
    return;
  increment(cGenTausAcceptance);

  if(wtaus.size() == 2) {
    for(size_t i=0; i<wtaus.size(); ++i) {
      const reco::GenParticle *genTau2 = wtaus[i];
      math::XYZTLorentzVector genTauVisible2 = HPlus::GenParticleTools::calculateVisibleTau(genTau2);

      hGenTauPt2->Fill(genTau2->pt());
      hGenTauEta2->Fill(genTau2->eta());
      hGenTauPhi2->Fill(genTau2->phi());
      hGenTauPtVisible2->Fill(genTauVisible2.Pt());
    }
  }

  if(wtaus.size() != 1)
    return;
  increment(cOneGenTau);

  const reco::GenParticle *genTau = wtaus[0];
  math::XYZTLorentzVector genTauVisible = HPlus::GenParticleTools::calculateVisibleTau(genTau);

  hGenTauPt->Fill(genTau->pt());
  hGenTauEta->Fill(genTau->eta());
  hGenTauPhi->Fill(genTau->phi());
  hGenTauPtVisible->Fill(genTauVisible.Pt());

  edm::PtrVector<pat::Jet> jets;
  for(edm::View<pat::Jet>::const_iterator iJet = hjets->begin(); iJet != hjets->end(); ++iJet) {
    double DR = reco::deltaR(genTauVisible, *iJet);
    if(DR < 0.5)
      continue;

    jets.push_back(hjets->ptrAt(iJet-hjets->begin()));
  }
  if(jets.size() < 3)
    return;
  increment(cThreeJets);

  hGenTauPt_AfterJets->Fill(genTau->pt());
  hGenTauEta_AfterJets->Fill(genTau->eta());
  hGenTauPhi_AfterJets->Fill(genTau->phi());
  hGenTauPtVisible_AfterJets->Fill(genTauVisible.Pt());
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEmbeddingDebugTauAnalyzer);
