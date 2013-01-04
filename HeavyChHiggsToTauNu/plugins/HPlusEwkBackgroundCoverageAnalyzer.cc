#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"


#include "TNamed.h"
#include "TH2F.h"

namespace {
  enum TauIDPassed {
    kTauNone,
    kTauTau1,
    kTauTau1OtherCorrect,
    kTauTau1OtherWrong,
    kTauObj2,
    kTauObj2Other,
    kTauOther,
    kTauSize
  };

  enum LeptonVetoPassed {
    kLeptonNone,
    kLeptonTau1,
    kLeptonObj2,
    kLeptonOther,
    kLeptonSize
  };

  enum Obj2Type {
    kObj2None,
    kObj2Electron,
    kObj2Muon,
    kObj2MuonEmb,
    kObj2Quark,
    kObj2TauNotInAcceptance,
    kObj2Tauh,
    kObj2Taue,
    kObj2Taumu,
    kObj2TaumuEmb
  };

  class MCMatcher {
  public:
    MCMatcher(const edm::PtrVector<pat::Tau>& taus_,
               const edm::PtrVector<pat::Electron>& electrons_,
               const edm::PtrVector<pat::Muon>& muons_,
               const edm::PtrVector<pat::Muon>& embMuons_):
      fSelectedTaus(taus_),
      fIdentifiedElectrons(electrons_),
      fIdentifiedMuons(muons_),
      fEmbeddingIdentifiedMuons(embMuons_),
      fMatchDR(0.1),
      fTauIDPassed(kTauNone),
      fLeptonVetoIdentified(kLeptonNone)
    {}

    const double getMatchDR() const { return fMatchDR; }

    TauIDPassed getTauIDStatus() const { return fTauIDPassed; }
    LeptonVetoPassed getLeptonVetoStatus() const { return fLeptonVetoIdentified; }

    void match(const reco::GenParticle *w1daughter, const reco::GenParticle *w2daughter1, const reco::GenParticle *w2daughter2=0) {
      // TauID
      
      // First try W1daughter
      for(size_t i=0; i<fSelectedTaus.size(); ++i) {
        if(reco::deltaR(*fSelectedTaus[i], *w1daughter) < fMatchDR) {
          fTauIDPassed = kTauTau1;
          break;
        }
      }
      if(fTauIDPassed == kTauTau1) {
        if(fSelectedTaus.size() > 1) {
          // The 0th element of fSelectedTaus is *the* selected tau
          if(reco::deltaR(*fSelectedTaus[0], *w1daughter) < fMatchDR)
            fTauIDPassed = kTauTau1OtherCorrect;
          else
            fTauIDPassed = kTauTau1OtherWrong;
        }
      }
      else {
        // If W1daughter not matched, try W2daughter
        for(size_t i=0; i<fSelectedTaus.size(); ++i) {
          if(reco::deltaR(*fSelectedTaus[i], *w2daughter1) < fMatchDR ||
             (w2daughter2 && reco::deltaR(*fSelectedTaus[i], *w2daughter2) < fMatchDR)) {
            fTauIDPassed = kTauObj2;
            break;
          }
        }
        if(fTauIDPassed == kTauObj2 && fSelectedTaus.size() > 1)
          fTauIDPassed = kTauObj2Other;
      }
      if(fTauIDPassed == kTauNone && !fSelectedTaus.empty())
        fTauIDPassed = kTauOther;


      // Lepton veto
      for(size_t i=0; i<fIdentifiedElectrons.size(); ++i) {
        if(fLeptonVetoIdentified == kLeptonNone) {
          if(reco::deltaR(*fIdentifiedElectrons[i], *w1daughter) < fMatchDR)
            fLeptonVetoIdentified = kLeptonTau1;
          else if(reco::deltaR(*fIdentifiedElectrons[i], *w2daughter1) < fMatchDR ||
                  (w2daughter2 && reco::deltaR(*fIdentifiedElectrons[i], *w2daughter2) < fMatchDR))
            fLeptonVetoIdentified = kLeptonObj2;
        }
        // Non-W1-daughter and non-W2-daughter object identified in lepton veto
        if(fLeptonVetoIdentified == kLeptonNone)
          fLeptonVetoIdentified = kLeptonOther;
      }
      for(size_t i=0; i<fIdentifiedMuons.size(); ++i) {
        if(fLeptonVetoIdentified == kLeptonNone) {
          if(reco::deltaR(*fIdentifiedMuons[i], *w1daughter) < fMatchDR)
            fLeptonVetoIdentified = kLeptonTau1;
          else if(reco::deltaR(*fIdentifiedMuons[i], *w2daughter1) < fMatchDR ||
                  (w2daughter2 && reco::deltaR(*fIdentifiedMuons[i], *w2daughter2) < fMatchDR))
            fLeptonVetoIdentified = kLeptonObj2;
        }
        // Non-W1-daughter and non-W2-daughter object identified in lepton veto
        if(fLeptonVetoIdentified == kLeptonNone)
          fLeptonVetoIdentified = kLeptonOther;
      }
    }


  private:
    const edm::PtrVector<pat::Tau>& fSelectedTaus;
    const edm::PtrVector<pat::Electron>& fIdentifiedElectrons;
    const edm::PtrVector<pat::Muon>& fIdentifiedMuons;
    const edm::PtrVector<pat::Muon>& fEmbeddingIdentifiedMuons;

    const double fMatchDR;
    TauIDPassed fTauIDPassed;
    LeptonVetoPassed fLeptonVetoIdentified;
  };


  TH2 *createHisto(TFileService& fs, const std::string& name, const std::string& obj2Name) {
    TH2 *histo = fs.make<TH2F>(name.c_str(), name.c_str(), kTauSize,0,kTauSize, kLeptonSize,0,kLeptonSize);
  
    histo->GetXaxis()->SetBinLabel(1+kTauNone, "None");
    histo->GetXaxis()->SetBinLabel(1+kTauTau1, "#tau_{1}");
    histo->GetXaxis()->SetBinLabel(1+kTauTau1OtherCorrect, "#tau_{1}+other (corr. sel.)");
    histo->GetXaxis()->SetBinLabel(1+kTauTau1OtherWrong, "#tau_{1}+other (wrong sel.)");
    histo->GetXaxis()->SetBinLabel(1+kTauObj2, obj2Name.c_str());
    histo->GetXaxis()->SetBinLabel(1+kTauObj2Other, (obj2Name+"+other").c_str());
    histo->GetXaxis()->SetBinLabel(1+kTauOther, "Other");
    histo->GetXaxis()->SetTitle("Tau ID");

    histo->GetYaxis()->SetBinLabel(1+kLeptonNone, "None");
    histo->GetYaxis()->SetBinLabel(1+kLeptonTau1, "#tau_{1}");
    histo->GetYaxis()->SetBinLabel(1+kLeptonObj2, obj2Name.c_str());
    histo->GetYaxis()->SetBinLabel(1+kLeptonOther, "Other");
    histo->GetYaxis()->SetTitle("ID in lepton veto");

    return histo;
  }
}

class HPlusEwkBackgroundCoverageAnalyzer: public edm::EDAnalyzer {
 public:


  explicit HPlusEwkBackgroundCoverageAnalyzer(const edm::ParameterSet& iConfig);
  ~HPlusEwkBackgroundCoverageAnalyzer();

 private:
  virtual void beginJob();
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual void endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight fEventWeight;
  HPlus::HistoWrapper fHistoWrapper;

  edm::InputTag fGenParticleSrc;
  edm::InputTag fEmbeddingMuonSrc;

  const double fTauPtCut;
  const double fTauEtaCut;
  const double fDeltaPhiCutValue;

  HPlus::TriggerSelection fTriggerSelection;
  HPlus::VertexSelection fPrimaryVertexSelection;
  HPlus::TauSelection fTauSelection;
  HPlus::GlobalElectronVeto fGlobalElectronVeto;
  HPlus::GlobalMuonVeto fGlobalMuonVeto;
  HPlus::JetSelection fJetSelection;
  HPlus::METSelection fMETSelection;
  HPlus::BTagging fBTagging;

  HPlus::Count fAllCounter;
  HPlus::Count fTriggerCounter;
  HPlus::Count fPrimaryVertexCounter;

  HPlus::Count fGenuineTauCounter;

  HPlus::Count fTauIDCounter;
  HPlus::Count fJetSelectionCounter;
  HPlus::Count fMETCounter;
  HPlus::Count fBTaggingCounter;
  HPlus::Count fDeltaPhiTauMETCounter;

  struct Result {
    Result(HPlus::EventCounter& eventCounter, const std::string& postfix):
      fTauElectronCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + electron2")),
      fTauMuonCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + muon2 (not embedding-identified)")),
      fTauMuonEmbCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + muon2 (embedding-identified)")),
      fTauTauNotInAcceptanceCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + tau2 (not in acceptance)")),
      fTauQuarkCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + quark2")),
      fTauTauHCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + tau_h2")),
      fTauTauECounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + tau_e2")),
      fTauTauMuNonEmbCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + tau_mu2 (not embedding-identified)")),
      fTauTauMuEmbCounter(eventCounter.addSubCounter("Classification"+postfix, "tau1 + tau_mu2 (embedding-identified)")),
      fHistoPostfix(postfix)
    {}

    void bookHistos(TFileService& fs) {
      hTauElectron    = createHisto(fs, "tau1_electron2_"+fHistoPostfix,     "e_{2}");
      hTauQuark       = createHisto(fs, "tau1_quark2_"+fHistoPostfix,        "q_{2}");
      hTauMuNonEmb    = createHisto(fs, "tau1_muon2_nonEmb_"+fHistoPostfix,  "#mu_{2}");
      hTauMuEmb       = createHisto(fs, "tau1_muon2_Emb_"+fHistoPostfix,     "#mu_{2}");

      hTauTauH        = createHisto(fs, "tau1_tauh2_"+fHistoPostfix,         "#tau_{h,2}");
      hTauTauE        = createHisto(fs, "tau1_taue2_"+fHistoPostfix,         "#tau_{e,2}");
      hTauTauMuEmb    = createHisto(fs, "tau1_taumu2_nonEmb_"+fHistoPostfix, "#tau_{#mu,2}");
      hTauTauMuNonEmb = createHisto(fs, "tau1_taumu2_Emb_"+fHistoPostfix,    "#tau_{#mu,2}");
    }

    void fill(Obj2Type obj2Type, TauIDPassed tauIDPassed, LeptonVetoPassed leptonVetoIdentified) {
      TH2 *theHisto = 0;
      switch(obj2Type) {
      case kObj2Electron:
        theHisto = hTauElectron;
        increment(fTauElectronCounter);
        break;
      case kObj2MuonEmb:
        theHisto = hTauMuEmb;
        increment(fTauMuonEmbCounter);
        break;
      case  kObj2Muon:
        theHisto = hTauMuNonEmb;
        increment(fTauMuonCounter);
        break;
      case kObj2TauNotInAcceptance:
        increment(fTauTauNotInAcceptanceCounter);
        break;
      case kObj2Quark:
        theHisto = hTauQuark;
        increment(fTauQuarkCounter);
        break;
      case kObj2Taue:
        theHisto = hTauTauE;
        increment(fTauTauECounter);
        break;
      case kObj2TaumuEmb:
        theHisto = hTauTauMuEmb;
        increment(fTauTauMuEmbCounter);
        break;
      case kObj2Taumu:
        theHisto = hTauTauMuNonEmb;
        increment(fTauTauMuNonEmbCounter);
        break;
      case kObj2Tauh:
        theHisto = hTauTauH;
        increment(fTauTauHCounter);
        break;
      default:
        throw cms::Exception("Assert") << "This should never happen at " << __FILE__ << ":" << __LINE__ << std::endl;
      }

      if(theHisto)
        theHisto->Fill(tauIDPassed+1, leptonVetoIdentified+1);

    }

    HPlus::Count fTauElectronCounter;
    HPlus::Count fTauMuonCounter;
    HPlus::Count fTauMuonEmbCounter;
    HPlus::Count fTauTauNotInAcceptanceCounter;
    HPlus::Count fTauQuarkCounter;

    HPlus::Count fTauTauHCounter;
    HPlus::Count fTauTauECounter;
    HPlus::Count fTauTauMuNonEmbCounter;
    HPlus::Count fTauTauMuEmbCounter;

    const std::string fHistoPostfix;

    TH2 *hTauElectron;
    TH2 *hTauQuark;
    TH2 *hTauMuNonEmb;
    TH2 *hTauMuEmb;
    
    TH2 *hTauTauH;
    TH2 *hTauTauE;
    TH2 *hTauTauMuNonEmb;
    TH2 *hTauTauMuEmb;
  };

  Result fResult;
  Result fResultAfterAllSelections;
};

HPlusEwkBackgroundCoverageAnalyzer::HPlusEwkBackgroundCoverageAnalyzer(const edm::ParameterSet& iConfig):
  eventCounter(iConfig), fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  fGenParticleSrc(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
  fEmbeddingMuonSrc(iConfig.getUntrackedParameter<edm::InputTag>("embeddingMuonSrc")),
  fTauPtCut(iConfig.getUntrackedParameter<double>("tauPtCut")),
  fTauEtaCut(iConfig.getUntrackedParameter<double>("tauEtaCut")),
  fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
  fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
  fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
  fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
  fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), fPrimaryVertexSelection.getSrc(), eventCounter, fHistoWrapper),
  fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, fHistoWrapper),
  fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
  fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET"),
  fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
  fAllCounter(eventCounter.addCounter("Offline selection begins")),
  fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
  fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
  fGenuineTauCounter(eventCounter.addCounter(">= 1 genuine tau in acceptance")),
  fTauIDCounter(eventCounter.addCounter("taus > 1")),
  fJetSelectionCounter(eventCounter.addCounter("njets")),
  fMETCounter(eventCounter.addCounter("MET")),
  fBTaggingCounter(eventCounter.addCounter("btagging")),
  fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhi(Tau MET) upper limit")),
  fResult(eventCounter, "Before"),
  fResultAfterAllSelections(eventCounter, "AfterAllSelections")
{
  eventCounter.setWeightPointer(fEventWeight.getWeightPtr());


  edm::Service<TFileService> fs;
  // Save the module configuration to the output ROOT file as a TNamed object
  fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

  fResult.bookHistos(*fs);
  fResultAfterAllSelections.bookHistos(*fs);
}

HPlusEwkBackgroundCoverageAnalyzer::~HPlusEwkBackgroundCoverageAnalyzer() {}
void HPlusEwkBackgroundCoverageAnalyzer::beginJob() {}

void HPlusEwkBackgroundCoverageAnalyzer::endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}

void HPlusEwkBackgroundCoverageAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventWeight.updatePrescale(iEvent); // set prescale

  increment(fAllCounter);

//------ Apply trigger and HLT_MET cut or trigger parametrisation
  HPlus::TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
  if (!triggerData.passedEvent()) return;
  increment(fTriggerCounter);

//------ Primary vertex
  HPlus::VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
  if(!pvData.passedEvent()) return;
  increment(fPrimaryVertexCounter);

//------ TauID
  HPlus::TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
 
//------ Global electron veto
  HPlus::GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);

//------ Global muon veto
  HPlus::GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());

  // Embedding-identified muons
  edm::Handle<edm::View<pat::Muon> > hembeddingmuons;
  iEvent.getByLabel(fEmbeddingMuonSrc, hembeddingmuons);

  // Get GenParticles
  edm::Handle<edm::View<reco::GenParticle> > hgenparticle;
  iEvent.getByLabel(fGenParticleSrc, hgenparticle);


  const edm::PtrVector<pat::Tau>& selectedTaus = tauData.getSelectedTaus();
  const edm::PtrVector<pat::Electron>& identifiedElectrons = electronVetoData.getSelectedElectrons();
  const edm::PtrVector<pat::Muon>& identifiedMuons = muonVetoData.getSelectedMuons();
  const edm::PtrVector<pat::Muon>& embeddingIdentifiedMuons = hembeddingmuons->ptrVector();

  MCMatcher mcMatcher(selectedTaus,
                      identifiedElectrons,
                      identifiedMuons,
                      embeddingIdentifiedMuons);

  const reco::GenParticle *W1 = 0; // from (t->)W->tau
  const reco::GenParticle *W2 = 0;

  for(edm::View<reco::GenParticle>::const_iterator iGen = hgenparticle->begin(); iGen != hgenparticle->end(); ++iGen) {
    const reco::GenParticle *particle = &(*iGen);
    unsigned pdgId = std::abs(particle->pdgId());
    if(pdgId == 24) { // W
      // Ensure that this W has no other W as a mother
      const reco::GenParticle *Wmother = HPlus::GenParticleTools::hasMother(particle, 24);
      if(Wmother)
        continue;

      if(!W1)
        W1 = particle;
      else if(!W2) {
        W2 = particle;
        break; // Not interested in further W's
      }
    }
  }

  // Inspect W1
  bool W1decaysTau = false;
  bool W2decaysTau = false;
  const reco::GenParticle *W1daughter = 0;
  const reco::GenParticle *W2daughter1 = 0;
  const reco::GenParticle *W2daughter2 = 0;
  if(W1) {
    //W1 = HPlus::GenParticleTools::rewindChainDown(W1);
    W1daughter = HPlus::GenParticleTools::findMaxNonNeutrinoDaughter(W1);
    if(!W1daughter)
      throw cms::Exception("Assert") << "Did not find daughter for W1 at " << __FILE__ << ":" << __LINE__ << std::endl;

    //std::cout << "W1 " << W1daughter->pdgId() << std::endl;

    if(std::abs(W1daughter->pdgId()) == 15 && W1daughter->pt() > fTauPtCut && std::abs(W1daughter->eta()) < fTauEtaCut)
      W1decaysTau = true;
  }
  if(W2) {
    //W2 = HPlus::GenParticleTools::rewindChainDown(W1);
    W2daughter1 = HPlus::GenParticleTools::findMaxNonNeutrinoDaughter(W2);
    if(!W2daughter1)
      throw cms::Exception("Assert") << "Did not find daughter for W2 at " << __FILE__ << ":" << __LINE__ << std::endl;

    //std::cout << "W2 " << W2daughter->pdgId() << std::endl;

    if(std::abs(W2daughter1->pdgId()) == 15 && W2daughter1->pt() > fTauPtCut && std::abs(W2daughter1->eta()) < fTauEtaCut)
      W2decaysTau = true;
  }

  // Neither W decays to tau
  if(!W1decaysTau && !W2decaysTau) {
    return;
  }
  increment(fGenuineTauCounter);

  // If W1 decays non-tau, and W2 decays tau, switch them
  // For single-tau W1 is the one decaying to tau
  if(!W1decaysTau && W2decaysTau) {
    const reco::GenParticle *tmp = W1;
    W1 = W2;
    W2 = tmp;

    tmp = W1daughter;
    W1daughter = W2daughter1;
    W2daughter1 = tmp;

    W1decaysTau = true;
    W2decaysTau = false;
  }

  mcMatcher.match(W1daughter, W2daughter1);

  // Now W1 decays to tau, W2 to anything (could be tau)

  Obj2Type obj2Type = kObj2None;

  // Single tau
  if(W1decaysTau && !W2decaysTau) {
    unsigned daughterId = std::abs(W2daughter1->pdgId());
    if(daughterId == 11) { // W2 -> electron
      obj2Type = kObj2Electron;
    }
    else if(daughterId == 13) { // W2 -> muon
      bool embeddingIdentified = false;
      for(size_t i=0; i<embeddingIdentifiedMuons.size(); ++i) {
        if(reco::deltaR(*embeddingIdentifiedMuons[i], *W2daughter1) < mcMatcher.getMatchDR()) {
          embeddingIdentified = true;
          break;
        }
      }

      if(embeddingIdentified)
        obj2Type = kObj2MuonEmb;
      else
        obj2Type = kObj2Muon;
    }
    else if(daughterId == 15) { //  W2 -> tau (shouldn't happen)
      // happens with tau outside acceptance
      //throw cms::Exception("Assert") << "This shouldn't happen at " << __FILE__ << ":" << __LINE__ << std::endl;

      obj2Type = kObj2TauNotInAcceptance;
    }
    else if(daughterId == 1 || daughterId == 2 || daughterId == 3 ||
            daughterId == 4 || daughterId == 5 || daughterId == 6) {// W -> qq'
      for(size_t i=0; i<W2->numberOfDaughters(); ++i) {
        const reco::GenParticle *tmp = dynamic_cast<const reco::GenParticle *>(W2->daughter(i));
        if(tmp == W2daughter1)
          continue;
        if(tmp->pdgId() == W2->pdgId())
          continue;
        W2daughter2 = tmp;
        break;
      }

      // Redo the matching with both quarks given as the W2 daughters
      mcMatcher.match(W1daughter, W2daughter1, W2daughter2);

      obj2Type = kObj2Quark;
    }
    else {
      throw cms::Exception("Assert") << "Got daughter " << daughterId << " from W2 at " << __FILE__ << ":" << __LINE__ << std::endl;
    }
  }
  else if(W1decaysTau && W2decaysTau) {
    const reco::GenParticle *tauDaughter = HPlus::GenParticleTools::findTauDaughter(W2daughter1);
    unsigned tauDaughterId = std::abs(tauDaughter->pdgId());
    if(tauDaughterId == 11) { // W2 -> tau -> electron
      obj2Type = kObj2Taue;
    }
    else if(tauDaughterId == 13) { // W2 -> tau -> muon
      bool embeddingIdentified = false;
      for(size_t i=0; i<embeddingIdentifiedMuons.size(); ++i) {
        if(reco::deltaR(*embeddingIdentifiedMuons[i], *tauDaughter) < mcMatcher.getMatchDR()) {
          embeddingIdentified = true;
          break;
        }
      }

      if(embeddingIdentified)
        obj2Type = kObj2TaumuEmb;
      else
        obj2Type = kObj2Taumu;
    }
    else { // W2 -> tau -> hadrons
      obj2Type = kObj2Tauh;
    }
  }

  fResult.fill(obj2Type, mcMatcher.getTauIDStatus(), mcMatcher.getLeptonVetoStatus());

  // Remaining selections

  // Consider only events where some object has passed tau ID
  if(!tauData.passedEvent()) return;
  increment(fTauIDCounter);

  // Hadronic jet selection
  int nVertices = 0; // dummy value
  HPlus::JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), nVertices);
  if(!jetData.passedEvent()) return;
  increment(fJetSelectionCounter);

  // MET
  HPlus::METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
  if(!metData.passedEvent()) return;
  increment(fMETCounter);

  // B tagging
  HPlus::BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
  if(!btagData.passedEvent()) return;
  increment(fBTaggingCounter);

  // Delta phi(tau, MET)
  double deltaPhi = HPlus::DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
  if (deltaPhi > fDeltaPhiCutValue) return;
  increment(fDeltaPhiTauMETCounter);

  fResultAfterAllSelections.fill(obj2Type, mcMatcher.getTauIDStatus(), mcMatcher.getLeptonVetoStatus());
  
}

void HPlusEwkBackgroundCoverageAnalyzer::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEwkBackgroundCoverageAnalyzer);
