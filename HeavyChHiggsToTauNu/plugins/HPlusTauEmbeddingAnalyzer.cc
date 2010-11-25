#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TH2F.h"

class HPlusTauEmbeddingAnalyzer: public edm::EDAnalyzer {
 public:

  explicit HPlusTauEmbeddingAnalyzer(const edm::ParameterSet&);
  ~HPlusTauEmbeddingAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  typedef std::pair<const reco::GenParticle *, const reco::GenParticle *> GenParticlePair;
  template <typename I>
  GenParticlePair findTauNu(I begin, I end) const;


  edm::InputTag muonSrc_;
  edm::InputTag tauSrc_;
  edm::InputTag metSrc_;
  edm::InputTag origMetSrc_;
  edm::InputTag genMetSrc_;
  edm::InputTag origGenMetSrc_;
  edm::InputTag nuMetSrc_;
  edm::InputTag origNuMetSrc_;
  edm::InputTag genParticleSrc_;

  double muonTauCone_;

  struct Histo {
    Histo(): hPt(0), hEta(0), hPhi(0) {}

    void init(TFileDirectory& dir, const std::string& name, const std::string& title) {
      hPt = dir.make<TH1F>((name+"Pt").c_str(), (title+" pt").c_str(), 200, 0., 200.);
      hEta = dir.make<TH1F>((name+"Eta").c_str(), (title+" eta").c_str(), 60, -3, 3.);
      hPhi = dir.make<TH1F>((name+"Phi").c_str(), (title+" phi").c_str(), 70, -3.5, 3.5);
    }

    void fill(const reco::Candidate& cand) {
      hPt->Fill(cand.pt());
      hEta->Fill(cand.eta());
      hPhi->Fill(cand.phi());
    }

    TH1 *hPt;
    TH1 *hEta;
    TH1 *hPhi;
  };

  struct Histo2 {
    Histo2():  hPt(0), hEta(0), hPhi(0) {}

    void init(TFileDirectory& dir, const std::string& name, const std::string& title) {
      hPt = dir.make<TH2F>((name+"Pt").c_str(), (title+" pt").c_str(), 200,0,200, 200,0,200);
      hEta = dir.make<TH2F>((name+"Eta").c_str(), (title+" eta").c_str(), 60,-3,3, 60,-3,3);
      hPhi = dir.make<TH2F>((name+"Phi").c_str(), (title+" phi").c_str(), 70,-3.5,3.5, 70,-3.5, 3.5);
    }

    void fill(const reco::Candidate& ref, const reco::Candidate& cand) {
      hPt->Fill(ref.pt(), cand.pt());
      hEta->Fill(ref.eta(), cand.eta());
      hPhi->Fill(ref.phi(), cand.phi());
    }

    TH2 *hPt;
    TH2 *hEta;
    TH2 *hPhi;
  };

  struct HistoMet {
    HistoMet(double metCut): metCut_(metCut),
                             hMet(0), hMetX(0), hMetY(0),
                             hOrigMet(0), hOrigMetX(0), hOrigMetY(0),
                             hOrigMetAfterCut(0),
                             hMetMet(0), hMetMetX(0), hMetMetY(0)
    {}

    void init(TFileDirectory& dir, const std::string& name) {
      hMet = dir.make<TH1F>((name+"Met").c_str(), "Tau+jets MET", 400, 0., 400.);
      hMetX = dir.make<TH1F>((name+"Met_x").c_str(), "Tau+jets MET", 400, -200., 200.);
      hMetY = dir.make<TH1F>((name+"Met_y").c_str(), "Tau+jets MET", 400, -200., 200.);

      hOrigMet = dir.make<TH1F>((name+"MetOriginal").c_str(), "Mu+jets MET", 400, 0., 400.);
      hOrigMetX = dir.make<TH1F>((name+"MetOriginal_x").c_str(), "Mu+jets MET", 400, -200., 200.);
      hOrigMetY = dir.make<TH1F>((name+"MetOriginal_y").c_str(), "Mu+jets MET", 400, -200., 200.);

      hOrigMetAfterCut = dir.make<TH1F>((name+"MetOriginalAfterCut").c_str(), "Tau+jets MET", 400, 0., 400.);

      hMetMet = dir.make<TH2F>((name+"MetMet").c_str(), "Mu vs. tau+jets MET", 400,0.,400., 400,0.,400.);
      hMetMetX = dir.make<TH2F>((name+"MetMet_x").c_str(), "Mu. vs. tau+jets MET x", 400,-200,200, 400,-200,200);
      hMetMetY = dir.make<TH2F>((name+"MetMet_y").c_str(), "Mu. vs. tau+jets MET y", 400,-200,200, 400,-200,200);
    }

    void fill(const reco::MET& met, const reco::MET& metOrig) {
      hMet->Fill(met.et());
      hMetX->Fill(met.px());
      hMetY->Fill(met.py());

      hOrigMet->Fill(metOrig.et());
      hOrigMetX->Fill(metOrig.px());
      hOrigMetY->Fill(metOrig.py());

      if(met.et() > metCut_)
        hOrigMetAfterCut->Fill(metOrig.et());

      hMetMet->Fill(metOrig.et(), met.et());
      hMetMetX->Fill(metOrig.px(), met.px());
      hMetMetY->Fill(metOrig.py(), met.py());

    }

    double metCut_;

    TH1 *hMet;
    TH1 *hMetX;
    TH1 *hMetY;

    TH1 *hOrigMet;
    TH1 *hOrigMetX;
    TH1 *hOrigMetY;

    TH1 *hOrigMetAfterCut;

    TH2 *hMetMet;
    TH2 *hMetMetX;
    TH2 *hMetMetY;
  };

  struct HistoAll {
    HistoAll(double metCut): hMet(metCut), hGenMet(metCut), hNuMet(metCut) {}

    void init(TFileDirectory& dir) {
      hMet.init(dir, "");
      hGenMet.init(dir, "Gen");
      hNuMet.init(dir, "Nu");

      hMuon.init(dir, "muon", "Muon");
      hTau.init(dir, "tau", "Tau");
      hTauGen.init(dir, "tauGen", "Tau gen");
      hNuGen.init(dir, "nuGen", "Nu gen");

      hMuonTau.init(dir, "muonTau", "Mu vs. tau");

      hMuonTauDR = dir.make<TH1F>("muonTauDR", "DR(muon, tau)", 700, 0, 7);
      hTauNuGenDR = dir.make<TH1F>("tauNuGenDR", "DR(tau, nu) gen", 700, 0, 7);
      hTauNuGenDEta = dir.make<TH1F>("tauNuGenDEta", "DEta(tau, nu) gen", 700, 0, 7);
      hTauNuGenDPhi = dir.make<TH1F>("tauNuGenDPhi", "DPhi(tau, nu) gen", 350, 0, 3.5);
    }

    HistoMet hMet;
    HistoMet hGenMet;
    HistoMet hNuMet;
    Histo hMuon;
    Histo hTau;
    Histo hTauGen;
    Histo hNuGen;

    Histo2 hMuonTau;

    TH1 *hMuonTauDR;
    TH1 *hTauNuGenDR;
    TH1 *hTauNuGenDEta;
    TH1 *hTauNuGenDPhi;
  };

  HistoAll histos;
  HistoAll histosMatched;

};

HPlusTauEmbeddingAnalyzer::HPlusTauEmbeddingAnalyzer(const edm::ParameterSet& iConfig):
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  tauSrc_(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  metSrc_(iConfig.getUntrackedParameter<edm::InputTag>("metSrc")),
  origMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("origMetSrc")),
  genMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genMetSrc")),
  origGenMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("origGenMetSrc")),
  nuMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("nuMetSrc")),
  origNuMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("origNuMetSrc")),
  genParticleSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
  muonTauCone_(iConfig.getUntrackedParameter<double>("muonTauMatchingCone")),
  histos(iConfig.getUntrackedParameter<double>("metCut")),
  histosMatched(iConfig.getUntrackedParameter<double>("metCut"))
{
  edm::Service<TFileService> fs;

  histos.init(*fs);
  TFileDirectory mdir = fs->mkdir("matched");
  histosMatched.init(mdir);
}
HPlusTauEmbeddingAnalyzer::~HPlusTauEmbeddingAnalyzer() {}

void HPlusTauEmbeddingAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Muon> > hmuon;
  iEvent.getByLabel(muonSrc_, hmuon);
  if(hmuon->size() != 1)
    throw cms::Exception("LogicError") << "Expected muon size 1, got " << hmuon->size() << " from collection " << muonSrc_.encode() << std::endl;
  edm::Ptr<reco::Muon> muon = hmuon->ptrAt(0);

  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(tauSrc_, htaus);
  if(htaus->empty())
    return;

  edm::Ptr<pat::Tau> tau;
  double minDR = 99999;
  for(size_t i=0; i<htaus->size(); ++i) {
    double dR = reco::deltaR(*muon, htaus->at(i));
    if(dR < minDR) {
      minDR = dR;
      tau = htaus->ptrAt(i);
    }
  }

  edm::Handle<edm::View<reco::MET> > hmet;
  iEvent.getByLabel(metSrc_, hmet);
  edm::Ptr<reco::MET> met = hmet->ptrAt(0);

  edm::Handle<edm::View<reco::MET> > horigMet;
  iEvent.getByLabel(origMetSrc_, horigMet);
  edm::Ptr<reco::MET> origMet = horigMet->ptrAt(0);

  edm::Handle<edm::View<reco::MET> > hgenMet;
  iEvent.getByLabel(genMetSrc_, hgenMet);
  edm::Ptr<reco::MET> genMet = hgenMet->ptrAt(0);

  edm::Handle<edm::View<reco::MET> > horigGenMet;
  iEvent.getByLabel(origGenMetSrc_, horigGenMet);
  edm::Ptr<reco::MET> origGenMet = horigGenMet->ptrAt(0);

  edm::Handle<edm::View<reco::MET> > hnuMet;
  iEvent.getByLabel(nuMetSrc_, hnuMet);
  edm::Ptr<reco::MET> nuMet = hnuMet->ptrAt(0);

  edm::Handle<edm::View<reco::MET> > horigNuMet;
  iEvent.getByLabel(origNuMetSrc_, horigNuMet);
  edm::Ptr<reco::MET> origNuMet = horigNuMet->ptrAt(0);

  edm::Handle<edm::View<reco::GenParticle> > hgen;
  iEvent.getByLabel(genParticleSrc_, hgen);

  GenParticlePair nuTau = findTauNu(hgen->begin(), hgen->end());

  histos.hMet.fill(*met, *origMet);
  histos.hGenMet.fill(*genMet, *origGenMet);
  histos.hNuMet.fill(*nuMet, *origNuMet);

  histos.hMuon.fill(*muon);
  histos.hMuonTauDR->Fill(minDR);
  histos.hTau.fill(*tau);
  histos.hMuonTau.fill(*muon, *tau);

  histos.hTauGen.fill(*nuTau.second);
  histos.hNuGen.fill(*nuTau.first);

  histos.hTauNuGenDR->Fill(reco::deltaR(*nuTau.first, *nuTau.second));
  histos.hTauNuGenDPhi->Fill(reco::deltaPhi(nuTau.first->phi(), nuTau.second->phi()));
  histos.hTauNuGenDEta->Fill(std::abs(nuTau.first->eta()-nuTau.second->eta()));
                    
  if(minDR < muonTauCone_) {
    histosMatched.hMet.fill(*met, *origMet);
    histosMatched.hGenMet.fill(*genMet, *origGenMet);
    histosMatched.hNuMet.fill(*nuMet, *origNuMet);

    histosMatched.hMuon.fill(*muon);
    histosMatched.hMuonTauDR->Fill(minDR);
    histosMatched.hTau.fill(*tau);
    histosMatched.hMuonTau.fill(*muon, *tau);

    histosMatched.hTauGen.fill(*nuTau.second);
    histosMatched.hNuGen.fill(*nuTau.first);

    histosMatched.hTauNuGenDR->Fill(reco::deltaR(*nuTau.first, *nuTau.second));
    histosMatched.hTauNuGenDPhi->Fill(reco::deltaPhi(nuTau.first->phi(), nuTau.second->phi()));
    histosMatched.hTauNuGenDEta->Fill(std::abs(nuTau.first->eta()-nuTau.second->eta()));
  }

}

template <typename I>
HPlusTauEmbeddingAnalyzer::GenParticlePair HPlusTauEmbeddingAnalyzer::findTauNu(I begin, I end) const {
  for(I iGen = begin; iGen != end; ++iGen) {
    int pdgId = std::abs(iGen->pdgId());
    if(pdgId == 12 || pdgId == 14 || pdgId == 16) {
      const reco::GenParticle *particle = &(*(iGen));
      bool isFromTau = false;
      while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(particle->mother())) {
        particle = mother;
        if(std::abs(particle->pdgId()) == 15) {
          isFromTau = true;
          break;
        }
      }
      if(isFromTau)
        return std::make_pair(&(*iGen), particle); // neutrino, tau
    }
  }
  return GenParticlePair(0, 0);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauEmbeddingAnalyzer);
