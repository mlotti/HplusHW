#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
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
    HistoMet(const edm::ParameterSet& pset, double metCut):
      embeddedSrc_(pset.getUntrackedParameter<edm::InputTag>("embeddedSrc")),
      originalSrc_(pset.getUntrackedParameter<edm::InputTag>("originalSrc")),
      metCut_(metCut),
      hMet(0), hMetX(0), hMetY(0),
      hOrigMet(0), hOrigMetX(0), hOrigMetY(0),
      hOrigMetAfterCut(0),
      hMetMet(0), hMetMetX(0), hMetMetY(0),
      hMuonMetDPhi(0), hMuonOrigMetDPhi(0), hTauMetDPhi(0), hTauOrigMetDPhi(0), hMuonOrigMetTauMetDPhi(0)
    {}

    void init(TFileDirectory& dir, const std::string& name) {
      hMet = dir.make<TH1F>(name.c_str(), "Tau+jets MET", 400, 0., 400.);
      hMetX = dir.make<TH1F>((name+"_x").c_str(), "Tau+jets MET", 400, -200., 200.);
      hMetY = dir.make<TH1F>((name+"_y").c_str(), "Tau+jets MET", 400, -200., 200.);

      hOrigMet = dir.make<TH1F>((name+"Original").c_str(), "Mu+jets MET", 400, 0., 400.);
      hOrigMetX = dir.make<TH1F>((name+"Original_x").c_str(), "Mu+jets MET", 400, -200., 200.);
      hOrigMetY = dir.make<TH1F>((name+"Original_y").c_str(), "Mu+jets MET", 400, -200., 200.);

      hOrigMetAfterCut = dir.make<TH1F>((name+"OriginalAfterCut").c_str(), "Tau+jets MET", 400, 0., 400.);

      hMetMet = dir.make<TH2F>((name+"Met").c_str(), "Mu vs. tau+jets MET", 400,0.,400., 400,0.,400.);
      hMetMetX = dir.make<TH2F>((name+"Met_x").c_str(), "Mu. vs. tau+jets MET x", 400,-200,200, 400,-200,200);
      hMetMetY = dir.make<TH2F>((name+"Met_y").c_str(), "Mu. vs. tau+jets MET y", 400,-200,200, 400,-200,200);

      hMuonMetDPhi = dir.make<TH1F>(("muon"+name+"DPhi").c_str(), "DPhi(muon, MET)", 700, -3.5, 3.5);
      hMuonOrigMetDPhi = dir.make<TH1F>(("muon"+name+"OriginalDPhi").c_str(), "DPhi(muon, MET)", 700, -3.5, 3.5);
      hTauMetDPhi = dir.make<TH1F>(("tau"+name+"DPhi").c_str(), "DPhi(tau, MET)", 700, -3.5, 3.5);
      hTauOrigMetDPhi = dir.make<TH1F>(("tau"+name+"OriginalDPhi").c_str(), "DPhi(tau, MET)", 700, -3.5, 3.5);

      hMuonOrigMetTauMetDPhi = dir.make<TH2F>(("muon"+name+"OriginalTau"+name+"DPhi").c_str(), "DPhi(muon, MET) vs. DPhi(tau, MET)", 700,-3.5,3.5, 700,-3.5,3.5);

      hMetOrigDiff = dir.make<TH1F>((name+"OriginalDiff").c_str(), "MET_{#tau} - MET_{#mu}", 800,-400,400);
      hMuonOrigMetDPhiMetOrigDiff = dir.make<TH2F>(("muon"+name+"OriginalDPhi"+name+"OriginalDiff").c_str(), "DPhi(muon, MET) vs. MET_{#tau} - MET_{#mu}", 700,-3.5,3.5, 800,-400,400);
    }

    void fill(const pat::Muon& muon, const reco::BaseTau& tau, const edm::Event& iEvent) {
      edm::Handle<edm::View<reco::MET> > hmet;
      iEvent.getByLabel(embeddedSrc_, hmet);
      const reco::MET& met = hmet->at(0);

      edm::Handle<edm::View<reco::MET> > horigMet;
      iEvent.getByLabel(originalSrc_, horigMet);
      const reco::MET& metOrig = horigMet->at(0);

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


      double muonOrigMetDphi = reco::deltaPhi(muon, metOrig);
      double tauMetDphi = reco::deltaPhi(tau, met);
      hMuonMetDPhi->Fill(reco::deltaPhi(muon, met));
      hMuonOrigMetDPhi->Fill(muonOrigMetDphi);
      hTauMetDPhi->Fill(tauMetDphi);
      hTauOrigMetDPhi->Fill(reco::deltaPhi(tau, metOrig));
      hMuonOrigMetTauMetDPhi->Fill(muonOrigMetDphi, tauMetDphi);

      double diff = met.et() - metOrig.et();
      hMetOrigDiff->Fill(diff);
      hMuonOrigMetDPhiMetOrigDiff->Fill(muonOrigMetDphi, diff);
    }

    edm::InputTag embeddedSrc_;
    edm::InputTag originalSrc_;

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

    TH1 *hMuonMetDPhi;
    TH1 *hMuonOrigMetDPhi;
    TH1 *hTauMetDPhi;
    TH1 *hTauOrigMetDPhi;
    TH2 *hMuonOrigMetTauMetDPhi;

    TH1 *hMetOrigDiff;
    TH2 *hMuonOrigMetDPhiMetOrigDiff;
  };

  struct HistoAll {
    HistoAll(double metCut): metCut_(metCut) {}
    ~HistoAll() {
      for(size_t i=0; i<hMets.size(); ++i) {
        delete hMets[i];
      }
    }

    void init(const edm::ParameterSet& pset, TFileDirectory& dir) {
      std::vector<std::string> metNames = pset.getParameterNames();
      for(std::vector<std::string>::const_iterator iName = metNames.begin(); iName != metNames.end(); ++iName) {
        HistoMet *met = new HistoMet(pset.getUntrackedParameter<edm::ParameterSet>(*iName), metCut_);
        met->init(dir, *iName);
        hMets.push_back(met);
      }

      hMuon.init(dir, "muon", "Muon");
      hMuonTrkIso = dir.make<TH1F>("muonIsoTrk", "Muon track isolation", 100, 0, 100);
      hMuonTrkRelIso = dir.make<TH1F>("muonIsoTrkRel", "Muon track relative isolation", 100, 0, 1);
      hMuonCaloIso = dir.make<TH1F>("muonIsoCalo", "Muon calo isolation", 100, 0, 100);
      hMuonCaloRelIso = dir.make<TH1F>("muonIsoCaloRel", "Muon calo relative isolation", 100, 0, 1);
      hMuonIso = dir.make<TH1F>("muonIsoTotal", "Muon total isolation", 50, 0, 50);
      hMuonRelIso = dir.make<TH1F>("muonIsoTotalRel", "Muon total relative isolation", 100, 0, 1);

      hTau.init(dir, "tau", "Tau");
      hTauIsoChargedHadrPtSum = dir.make<TH1F>("tauIsoChargedHadrPtSum", "Tau isolation charged hadr cand pt sum", 100, 0, 100);
      hTauIsoChargedHadrPtSumRel = dir.make<TH1F>("tauIsoChargedHadrPtSumRel", "Tau isolation charged hadr cand relative pt sum", 200, 0, 20);
      hTauIsoChargedHadrPtMax = dir.make<TH1F>("tauIsoChargedHadrPtMax", "Tau isolation charged hadr cand pt max", 100, 0, 100);
      hTauIsoChargedHadrPtMaxRel = dir.make<TH1F>("tauIsoChargedHadrPtMaxRel", "Tau isolation charged hadr cand relative pt max", 200, 0, 20);

      hMuonTrkTauPtSumIso = dir.make<TH2F>("muonIsoTrkTauPtSum", "Muon trk vs. tau ptsum isolation", 100,0,100, 100,0,100);
      hMuonTrkTauPtSumIsoRel = dir.make<TH2F>("muonIsoTrkTauPtSumRel", "Muon trk vs. tau ptsum relative isolation", 200,0,1, 200,0,20);
      hMuonTauPtSumIso = dir.make<TH2F>("muonIsoTauPtSum", "Muon total vs. tau ptsum isolation", 100,0,100, 200,0,20);
      hMuonTauPtSumIsoRel = dir.make<TH2F>("muonIsoTauPtSumRel", "Muon total vs. tau ptsum relative isolation", 200,0,1, 200,0,20);

      hTauGen.init(dir, "tauGen", "Tau gen");
      hNuGen.init(dir, "nuGen", "Nu gen");

      hMuonTau.init(dir, "muonTau", "Mu vs. tau");
      hMuonTauLdg.init(dir, "muonTauLdg", "Mu vs. tau ldg cand");

      hMuonTauDR = dir.make<TH1F>("muonTauDR", "DR(muon, tau)", 700, 0, 7);
      hMuonTauLdgDR = dir.make<TH1F>("muonTauLdgDR", "DR(muon, tau ldg cand)", 700, 0, 7);
      hTauNuGenDR = dir.make<TH1F>("tauNuGenDR", "DR(tau, nu) gen", 700, 0, 7);
      hTauNuGenDEta = dir.make<TH1F>("tauNuGenDEta", "DEta(tau, nu) gen", 600, -3, 3);
      hTauNuGenDPhi = dir.make<TH1F>("tauNuGenDPhi", "DPhi(tau, nu) gen", 700, -3.5, 3.5);
    }

    void fillMets(const reco::Muon& muon, const reco::BaseTau& tau, const edm::Event& iEvent) {
      for(size_t i=0; i<hMets.size(); ++i) {
        hMets[i]->fill(muon, tau, iEvent);
      }
    }

    void fillMuonTauIso(const pat::Muon& muon, const pat::Tau& tau) {
      const reco::MuonIsolation& iso = muon.isolationR03();
      double caloIso = iso.emEt+iso.hadEt;
      double totalIso = caloIso+iso.sumPt;

      hMuonTrkIso->Fill(iso.sumPt);
      hMuonTrkRelIso->Fill(iso.sumPt/muon.pt());
      hMuonCaloIso->Fill(caloIso);
      hMuonCaloRelIso->Fill(caloIso/muon.pt());
      hMuonIso->Fill(totalIso);
      hMuonRelIso->Fill(totalIso/muon.pt());

      double ptSum = tau.isolationPFChargedHadrCandsPtSum();
      double ptMax = 0;
      const reco::PFCandidateRefVector& isoCands = tau.isolationPFChargedHadrCands();
      if(isoCands.isNonnull()) {
        for(reco::PFCandidateRefVector::const_iterator iCand = isoCands.begin(); iCand != isoCands.end(); ++iCand) {
          ptMax = std::max(ptMax, (*iCand)->pt());
        }
      }
      hTauIsoChargedHadrPtSum->Fill(ptSum);
      hTauIsoChargedHadrPtSumRel->Fill(ptSum/tau.pt());
      hTauIsoChargedHadrPtMax->Fill(ptMax);
      hTauIsoChargedHadrPtMaxRel->Fill(ptMax/tau.pt());
      

      hMuonTrkTauPtSumIso->Fill(iso.sumPt, ptSum);
      hMuonTrkTauPtSumIsoRel->Fill(iso.sumPt/muon.pt(), ptSum/tau.pt());
      hMuonTauPtSumIso->Fill(totalIso, ptSum);
      hMuonTauPtSumIsoRel->Fill(totalIso/muon.pt(), ptSum/tau.pt());
    }

    double metCut_;
    std::vector<HistoMet *> hMets;

    Histo hMuon;
    TH1 *hMuonTrkIso;
    TH1 *hMuonTrkRelIso;
    TH1 *hMuonCaloIso;
    TH1 *hMuonCaloRelIso;
    TH1 *hMuonIso;
    TH1 *hMuonRelIso;

    Histo hTau;
    TH1 *hTauIsoChargedHadrPtSum;
    TH1 *hTauIsoChargedHadrPtSumRel;
    TH1 *hTauIsoChargedHadrPtMax;
    TH1 *hTauIsoChargedHadrPtMaxRel;

    TH2 *hMuonTrkTauPtSumIso;
    TH2 *hMuonTrkTauPtSumIsoRel;
    TH2 *hMuonTauPtSumIso;
    TH2 *hMuonTauPtSumIsoRel;

    Histo hTauGen;
    Histo hNuGen;

    Histo2 hMuonTau;
    Histo2 hMuonTauLdg;

    TH1 *hMuonTauDR;
    TH1 *hMuonTauLdgDR;
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
  genParticleSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
  muonTauCone_(iConfig.getUntrackedParameter<double>("muonTauMatchingCone")),
  histos(iConfig.getUntrackedParameter<double>("metCut")),
  histosMatched(iConfig.getUntrackedParameter<double>("metCut"))
{
  edm::Service<TFileService> fs;

  const edm::ParameterSet& pset = iConfig.getUntrackedParameter<edm::ParameterSet>("mets");

  histos.init(pset, *fs);
  TFileDirectory mdir = fs->mkdir("matched");
  histosMatched.init(pset, mdir);
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

  edm::Handle<edm::View<reco::GenParticle> > hgen;
  iEvent.getByLabel(genParticleSrc_, hgen);

  GenParticlePair nuTau = findTauNu(hgen->begin(), hgen->end());

  histos.fillMets(*muon, *tau, iEvent);

  histos.hMuon.fill(*muon);
  histos.hMuonTauDR->Fill(minDR);
  histos.hTau.fill(*tau);
  histos.hMuonTau.fill(*muon, *tau);

  const reco::PFCandidateRef leadCand = tau->leadPFChargedHadrCand();
  if(leadCand.isNonnull()) {
    histos.hMuonTauLdgDR->Fill(reco::deltaR(*muon, *leadCand));
    histos.hMuonTauLdg.fill(*muon, *leadCand);
  }
                            

  histos.fillMuonTauIso(*muon, *tau);

  histos.hTauGen.fill(*nuTau.second);
  histos.hNuGen.fill(*nuTau.first);

  histos.hTauNuGenDR->Fill(reco::deltaR(*nuTau.first, *nuTau.second));
  histos.hTauNuGenDPhi->Fill(reco::deltaPhi(nuTau.first->phi(), nuTau.second->phi()));
  histos.hTauNuGenDEta->Fill(nuTau.second->eta() - nuTau.first->eta());
                    
  if(minDR < muonTauCone_) {
    histosMatched.fillMets(*muon, *tau, iEvent);

    histosMatched.hMuon.fill(*muon);
    histosMatched.hMuonTauDR->Fill(minDR);
    histosMatched.hTau.fill(*tau);
    histosMatched.hMuonTau.fill(*muon, *tau);
    if(leadCand.isNonnull()) {
      histosMatched.hMuonTauLdgDR->Fill(reco::deltaR(*muon, *leadCand));
      histosMatched.hMuonTauLdg.fill(*muon, *leadCand);
    }

    histosMatched.fillMuonTauIso(*muon, *tau);

    histosMatched.hTauGen.fill(*nuTau.second);
    histosMatched.hNuGen.fill(*nuTau.first);

    histosMatched.hTauNuGenDR->Fill(reco::deltaR(*nuTau.first, *nuTau.second));
    histosMatched.hTauNuGenDPhi->Fill(reco::deltaPhi(nuTau.first->phi(), nuTau.second->phi()));
    histosMatched.hTauNuGenDEta->Fill(nuTau.second->eta() - nuTau.first->eta());
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
