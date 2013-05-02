#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"


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

  double tauPtCut_;
  double tauEtaCut_;

  HPlus::Count cAllEvents;
  HPlus::Count cGenTaus;
  HPlus::Count cGenTausAcceptance;
  HPlus::Count cOneGenTau;
  HPlus::Count cThreeJets;
};

HPlusEmbeddingDebugTauAnalyzer::HPlusEmbeddingDebugTauAnalyzer(const edm::ParameterSet& iConfig):
  fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, fEventWeight, fHistoWrapper),
  jetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("jetSrc")),
  genSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genSrc")),
  tauPtCut_(iConfig.getUntrackedParameter<double>("tauPtCut")),
  tauEtaCut_(iConfig.getUntrackedParameter<double>("tauEtaCut")),
  cAllEvents(eventCounter.addCounter("All events")),
  cGenTaus(eventCounter.addCounter(">= 1 gen tau")),
  cGenTausAcceptance(eventCounter.addCounter(">= 1 gen tau in acceptance")),
  cOneGenTau(eventCounter.addCounter("= 1 gen tau")),
  cThreeJets(eventCounter.addCounter("3 jets"))
{}

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

  if(wtaus.size() != 1)
    return;
  increment(cOneGenTau);

  const reco::GenParticle *genTau = wtaus[0];
  math::XYZTLorentzVector genTauVisible = HPlus::GenParticleTools::calculateVisibleTau(genTau);

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
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEmbeddingDebugTauAnalyzer);
