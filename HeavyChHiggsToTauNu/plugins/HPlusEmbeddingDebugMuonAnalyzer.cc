#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

class HPlusEmbeddingDebugMuonAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusEmbeddingDebugMuonAnalyzer(const edm::ParameterSet& iConfig);
  /// Default EDAnalyzer destructor
  ~HPlusEmbeddingDebugMuonAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endJob();


  HPlus::EventWeight fEventWeight;
  HPlus::HistoWrapper fHistoWrapper;
  HPlus::EventCounter eventCounter;
  HPlus::EmbeddingMuonEfficiency fEmbeddingMuonEfficiency;

  edm::InputTag muonSrc_;
  edm::InputTag jetSrc_;
  edm::InputTag genSrc_;

  HPlus::WeightReader pileupWeight_;

  const double muonPtCut_;
  const double muonEtaCut_;

  bool recoMuon_;
  bool recoJets_;

  HPlus::Count cAllEvents;
  HPlus::Count cPUReweight;
  HPlus::Count cGenMuons;
  HPlus::Count cGenMuonsAcceptance;
  HPlus::Count cOneGenMuon;
  HPlus::Count cRecoMuonFound;
  HPlus::Count cThreeJets;
  HPlus::Count cMuonEfficiency;

  HPlus::WrappedTH1 *hGenMuonPt;
  HPlus::WrappedTH1 *hGenMuonEta;
  HPlus::WrappedTH1 *hGenMuonPhi;

  HPlus::WrappedTH1 *hGenMuonPt2;
  HPlus::WrappedTH1 *hGenMuonEta2;
  HPlus::WrappedTH1 *hGenMuonPhi2;

  HPlus::WrappedTH1 *hGenMuonMatchMinDR;
  HPlus::WrappedTH1 *hGenMuonMatchCount;

  HPlus::WrappedTH1 *hGenMuonPt_AfterId;
  HPlus::WrappedTH1 *hGenMuonEta_AfterId;
  HPlus::WrappedTH1 *hGenMuonPhi_AfterId;

  HPlus::WrappedTH1 *hGenMuonPt_AfterJets;
  HPlus::WrappedTH1 *hGenMuonEta_AfterJets;
  HPlus::WrappedTH1 *hGenMuonPhi_AfterJets;

  HPlus::WrappedTH1 *hRecoMuonPt_AfterId;
  HPlus::WrappedTH1 *hRecoMuonEta_AfterId;
  HPlus::WrappedTH1 *hRecoMuonPhi_AfterId;

  HPlus::WrappedTH1 *hRecoMuonPt_AfterJets;
  HPlus::WrappedTH1 *hRecoMuonEta_AfterJets;
  HPlus::WrappedTH1 *hRecoMuonPhi_AfterJets;
};

HPlusEmbeddingDebugMuonAnalyzer::HPlusEmbeddingDebugMuonAnalyzer(const edm::ParameterSet& iConfig):
  fEventWeight(iConfig),
  fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, fEventWeight, fHistoWrapper),
  fEmbeddingMuonEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingMuonEfficiency")),
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  jetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("jetSrc")),
  genSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genSrc")),
  pileupWeight_(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
  muonPtCut_(iConfig.getUntrackedParameter<double>("muonPtCut")),
  muonEtaCut_(iConfig.getUntrackedParameter<double>("muonEtaCut")),
  recoMuon_(iConfig.getUntrackedParameter<bool>("recoMuon", true)),
  recoJets_(iConfig.getUntrackedParameter<bool>("recoJets", true)),
  cAllEvents(eventCounter.addCounter("All events")),
  cPUReweight(eventCounter.addCounter("PU reweighting")),
  cGenMuons(eventCounter.addCounter(">= 1 gen muon")),
  cGenMuonsAcceptance(eventCounter.addCounter(">= 1 gen muon in acceptance")),
  cOneGenMuon(eventCounter.addCounter("= 1 gen muon")),
  cRecoMuonFound(eventCounter.addCounter("reco muon found")),
  cThreeJets(eventCounter.addCounter("3 jets")),
  cMuonEfficiency(eventCounter.addCounter("muon eff. weight"))
{
  edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
  fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

  hGenMuonPt = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_pt", "Pt", 400, 0, 400);
  hGenMuonEta = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_eta", "Eta", 44, -2.1, 2.1);
  hGenMuonPhi = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_phi", "Phi", 128, -3.2, 3.2);

  hGenMuonPt2 = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon2_pt", "Pt", 400, 0, 400);
  hGenMuonEta2 = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon2_eta", "Eta", 44, -2.1, 2.1);
  hGenMuonPhi2 = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon2_phi", "Phi", 128, -3.2, 3.2);

  if(recoMuon_) {
    hGenMuonMatchMinDR = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kInformative, *fs, "genmuonmatch_mindr", "DR", 50, 0., 0.5);
    hGenMuonMatchCount = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kInformative, *fs, "genmuonmatch_count", "Count", 10, 0, 10);

    hGenMuonPt_AfterId = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_afterid_pt", "Pt", 400, 0, 400);
    hGenMuonEta_AfterId = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_afterid_eta", "Eta", 44, -2.1, 2.1);
    hGenMuonPhi_AfterId = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_afterid_phi", "Phi", 128, -3.2, 3.2);

    hRecoMuonPt_AfterId = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "recomuon_afterid_pt", "Pt", 400, 0, 400);
    hRecoMuonEta_AfterId = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "recomuon_afterid_eta", "eta", 44, -2.1, 2.1);
    hRecoMuonPhi_AfterId = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "recomuon_afterid_phi", "phi", 128, -3.2, 3.2);

    hGenMuonPt_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_afterjet_pt", "Pt", 400, 0, 400);
    hGenMuonEta_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_afterjet_eta", "eta", 44, -2.1, 2.1);
    hGenMuonPhi_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "genmuon_afterjet_phi", "phi", 128, -3.2, 3.2);

    hRecoMuonPt_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "recomuon_afterjet_pt", "Pt", 400, 0, 400);
    hRecoMuonEta_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "recomuon_afterjet_eta", "eta", 44, -2.1, 2.1);
    hRecoMuonPhi_AfterJets = fHistoWrapper.makeTH<TH1F>(HPlus::HistoWrapper::kVital, *fs, "recomuon_afterjet_phi", "phi", 128, -3.2, 3.2);
  }
}

HPlusEmbeddingDebugMuonAnalyzer::~HPlusEmbeddingDebugMuonAnalyzer() {}

void HPlusEmbeddingDebugMuonAnalyzer::endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}
void HPlusEmbeddingDebugMuonAnalyzer::endJob() {
  eventCounter.endJob();
}

void HPlusEmbeddingDebugMuonAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventWeight.beginEvent();
  increment(cAllEvents);

  const double myPileupWeight = pileupWeight_.getWeight(iEvent, iSetup);
  fEventWeight.multiplyWeight(myPileupWeight);
  increment(cPUReweight);

  edm::Handle<edm::View<pat::Muon> > hmuons;
  iEvent.getByLabel(muonSrc_, hmuons);

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(jetSrc_, hjets);

  edm::Handle<edm::View<reco::GenParticle> > hgenparticles;
  iEvent.getByLabel(genSrc_, hgenparticles);

  // Find W's
  typedef std::vector<const reco::GenParticle *> GenVector;
  GenVector wmuons;
  GenVector tmp = HPlus::GenParticleTools::findTTBarWdecays(hgenparticles->ptrVector());
  for(GenVector::const_iterator iGen = tmp.begin(); iGen != tmp.end(); ++iGen) {
    if(std::abs((*iGen)->pdgId()) == 13)
      wmuons.push_back(*iGen);
  }
  tmp.clear();
  if(wmuons.size() == 0)
    return;
  increment(cGenMuons);

  for(GenVector::const_iterator iGen = wmuons.begin(); iGen != wmuons.end(); ++iGen) {
    if(!((*iGen)->pt() > muonPtCut_ && std::abs((*iGen)->eta()) < muonEtaCut_))
      continue;
    tmp.push_back(*iGen);
  }
  wmuons.swap(tmp);
  tmp.clear();
  if(wmuons.size() == 0)
    return;
  increment(cGenMuonsAcceptance);

  if(wmuons.size() == 2) {
    for(size_t i=0; i<wmuons.size(); ++i) {
      const reco::GenParticle *genMuon = wmuons[0];
      hGenMuonPt2->Fill(genMuon->pt());
      hGenMuonEta2->Fill(genMuon->eta());
      hGenMuonPhi2->Fill(genMuon->phi());
    }
  }

  if(wmuons.size() != 1)
    return;
  increment(cOneGenMuon);

  const reco::GenParticle *genMuon = wmuons[0];

  hGenMuonPt->Fill(genMuon->pt());
  hGenMuonEta->Fill(genMuon->eta());
  hGenMuonPhi->Fill(genMuon->phi());

  if(recoMuon_) {
    edm::Ptr<pat::Muon> recoMuon;
    double minDR = 0.5;
    unsigned count = 0;
    for(edm::View<pat::Muon>::const_iterator iMuon = hmuons->begin(); iMuon != hmuons->end(); ++iMuon) {
      double DR = reco::deltaR(*iMuon, *genMuon);
      if(DR < minDR) {
        minDR = DR;
        recoMuon = hmuons->ptrAt(iMuon-hmuons->begin());
      }
      if(DR < 0.5) {
        ++count;
        /*
        std::cout << "gen    muon pt " << genMuon->pt() << " eta " << genMuon->eta() << " phi " << genMuon->phi() << std::endl
                  << "  reco muon pt " << recoMuon->pt() << " eta " << recoMuon->eta() << " phi " << recoMuon->phi() << " DR " << DR << std::endl;
        */
      }
    }
    hGenMuonMatchCount->Fill(count);
    if(recoMuon.isNull())
      return;
    increment(cRecoMuonFound);

    hGenMuonMatchMinDR->Fill(minDR);

    hGenMuonPt_AfterId->Fill(genMuon->pt());
    hGenMuonEta_AfterId->Fill(genMuon->eta());
    hGenMuonPhi_AfterId->Fill(genMuon->phi());

    hRecoMuonPt_AfterId->Fill(recoMuon->pt());
    hRecoMuonEta_AfterId->Fill(recoMuon->eta());
    hRecoMuonPhi_AfterId->Fill(recoMuon->phi());

    if(recoJets_) {
      edm::PtrVector<pat::Jet> jets;
      for(edm::View<pat::Jet>::const_iterator iJet = hjets->begin(); iJet != hjets->end(); ++iJet) {
        double DR = reco::deltaR(*recoMuon, *iJet);
        if(DR < 0.5)
          continue;

        jets.push_back(hjets->ptrAt(iJet-hjets->begin()));
      }
      if(jets.size() < 3)
        return;
      increment(cThreeJets);
    }

    HPlus::EmbeddingMuonEfficiency::Data embeddingMuonData = fEmbeddingMuonEfficiency.getEventWeight(recoMuon, iEvent.isRealData());
    fEventWeight.multiplyWeight(embeddingMuonData.getEventWeight());
    increment(cMuonEfficiency);

    hGenMuonPt_AfterJets->Fill(genMuon->pt());
    hGenMuonEta_AfterJets->Fill(genMuon->eta());
    hGenMuonPhi_AfterJets->Fill(genMuon->phi());

    hRecoMuonPt_AfterJets->Fill(recoMuon->pt());
    hRecoMuonEta_AfterJets->Fill(recoMuon->eta());
    hRecoMuonPhi_AfterJets->Fill(recoMuon->phi());
  }
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEmbeddingDebugMuonAnalyzer);
