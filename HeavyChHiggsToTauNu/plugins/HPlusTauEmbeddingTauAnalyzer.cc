#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
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

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingHistos.h"

#include "TH1F.h"
#include "TH2F.h"

#include<vector>

using hplus::te::Histo;
using hplus::te::Histo2;
using hplus::te::HistoMet;
using hplus::te::HistoMet2;

class HPlusTauEmbeddingTauAnalyzer: public edm::EDAnalyzer {
 public:

  explicit HPlusTauEmbeddingTauAnalyzer(const edm::ParameterSet&);
  ~HPlusTauEmbeddingTauAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  struct GenParticleTriple {
    GenParticleTriple(const reco::GenParticle *a, const reco::GenParticle *b, const reco::GenParticle *c):
      tau(a), wnu(b), taunu(c) {}

    const reco::GenParticle *tau;
    const reco::GenParticle *wnu;
    const reco::GenParticle *taunu;
  };

  template <typename I>
  void findTauNuFromW(I begin, I end, std::vector<GenParticleTriple>& results) const;

  edm::InputTag tauSrc_;
  edm::InputTag genParticleSrc_;

  double genTauMatch_;
  double genTauPt_;
  double genTauEta_;

  struct HistoAll {
    HistoAll(): hMetNu(0.0) {}
    ~HistoAll() {
      for(size_t i=0; i<hMets.size(); ++i) {
        delete hMets[i];
      }
    }

    void init(const edm::ParameterSet& pset, TFileDirectory& dir) {
      std::vector<std::string> metNames = pset.getParameterNames();
      for(std::vector<std::string>::const_iterator iName = metNames.begin(); iName != metNames.end(); ++iName) {
        if(*iName == "GenMetNu")
          throw cms::Exception("Configuration") << "GenMetNu is a reserved MET name" << std::endl;
        HistoMet *met = new HistoMet(pset.getUntrackedParameter<edm::InputTag>(*iName));
        met->init(dir, *iName, "Tau+jets", "tau", "tau");
        hMets.push_back(met);
      }
      hMetNu.init(dir, "GenMetNu");

      hTau.init(dir, "Tau", "Tau");
      hTauR = dir.make<TH1F>("Tau_Rtau", "R tau variable", 120, 0., 1.2);
      hTauIsoChargedHadrPtSum = dir.make<TH1F>("Tau_IsoChargedHadrPtSum", "Tau isolation charged hadr cand pt sum", 100, 0, 100);
      hTauIsoChargedHadrPtSumRel = dir.make<TH1F>("Tau_IsoChargedHadrPtSumRel", "Tau isolation charged hadr cand relative pt sum", 200, 0, 20);

      hTauGen.init(dir, "GenTau", "Tau gen");
      hNuGen.init(dir, "GenTauNu", "Nu gen");
      hTauNuGen.init(dir, "GenTau_GenTauNu", "Gen tau vs. nu");

      hTauGenDR = dir.make<TH1F>("Tau,GenTau_DR", "DR(tau, gen tau)", 700, 0, 7);
    }

    void fillMets(const reco::BaseTau& tau,
                  const reco::GenParticle *wNu, const reco::GenParticle *tauNu,
                  const edm::Event& iEvent) {
      for(size_t i=0; i<hMets.size(); ++i) {
        hMets[i]->fill(tau, tauNu, iEvent);
      }
    }

    void fillTauIso(const pat::Tau& tau) {
      double ptSum = tau.isolationPFChargedHadrCandsPtSum();
      hTauIsoChargedHadrPtSum->Fill(ptSum);
      hTauIsoChargedHadrPtSumRel->Fill(ptSum/tau.pt());
    }

    std::vector<HistoMet *> hMets;
    HistoMet2 hMetNu;

    Histo hTau;
    TH1 *hTauIsoChargedHadrPtSum;
    TH1 *hTauIsoChargedHadrPtSumRel;
    TH1 *hTauR;

    Histo hTauGen;
    Histo hNuGen;
    Histo2 hTauNuGen;

    TH1 *hTauGenDR;
  };

  HistoAll histos;
  HistoAll histosMatched;
};

HPlusTauEmbeddingTauAnalyzer::HPlusTauEmbeddingTauAnalyzer(const edm::ParameterSet& iConfig):
  tauSrc_(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  genParticleSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
  genTauMatch_(iConfig.getUntrackedParameter<double>("genTauMatchingCone")),
  genTauPt_(iConfig.getUntrackedParameter<double>("genTauPtCut")),
  genTauEta_(iConfig.getUntrackedParameter<double>("genTauEtaCut")),
  histos()
{
  edm::Service<TFileService> fs;

  const edm::ParameterSet& pset = iConfig.getUntrackedParameter<edm::ParameterSet>("mets");

  histos.init(pset, *fs);
  TFileDirectory mdir = fs->mkdir("matched");
  histosMatched.init(pset, mdir);
}

HPlusTauEmbeddingTauAnalyzer::~HPlusTauEmbeddingTauAnalyzer() {}

void HPlusTauEmbeddingTauAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::GenParticle> > hgen;
  iEvent.getByLabel(genParticleSrc_, hgen);

  std::vector<GenParticleTriple> tauNusAll;

  findTauNuFromW(hgen->begin(), hgen->end(), tauNusAll);
  if(tauNusAll.empty())
    return;

  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(tauSrc_, htaus);
  if(htaus->empty())
    return;

  for(size_t i=0; i<tauNusAll.size(); ++i) {
    const GenParticleTriple& tauNus = tauNusAll[i];
    if(genTauPt_ > 0 && tauNus.tau->pt() < genTauPt_)
      continue;
    if(genTauEta_ > 0 && std::abs(tauNus.tau->eta()) >= genTauEta_)
      continue;

    edm::Ptr<pat::Tau> tau;
    double minDR = 99999;
    for(size_t i=0; i<htaus->size(); ++i) {
      double dR = reco::deltaR(*tauNus.tau, htaus->at(i));
      if(dR < minDR) {
        minDR = dR;
        tau = htaus->ptrAt(i);
      }
    }

    histos.hTauGenDR->Fill(minDR);
    histos.fillMets(*tau, tauNus.wnu, tauNus.taunu, iEvent);

    reco::GenParticle::LorentzVector nuWTauSum = tauNus.wnu->p4() + tauNus.taunu->p4();
    histos.hMetNu.fill(*tau, *tau, tauNus.wnu, tauNus.taunu, tauNus.wnu->p4(), nuWTauSum);

    histos.hTau.fill(*tau);
    const reco::PFCandidateRef leadCand = tau->leadPFChargedHadrCand();
    if(leadCand.isNonnull() && tau->p() > 0)
      histos.hTauR->Fill(leadCand->p()/tau->p());

    histos.fillTauIso(*tau);
    histos.hTauGen.fill(*tauNus.tau);
    histos.hNuGen.fill(*tauNus.taunu);
    histos.hTauNuGen.fill(*tauNus.tau, *tauNus.taunu);

    if(minDR < genTauMatch_) {
      histosMatched.hTauGenDR->Fill(minDR);
      histosMatched.fillMets(*tau, tauNus.wnu, tauNus.taunu, iEvent);

      histosMatched.hMetNu.fill(*tau, *tau, tauNus.wnu, tauNus.taunu, tauNus.wnu->p4(), nuWTauSum);

      histosMatched.hTau.fill(*tau);
      if(leadCand.isNonnull() && tau->p() > 0)
        histosMatched.hTauR->Fill(leadCand->p()/tau->p());

      histosMatched.fillTauIso(*tau);
      histosMatched.hTauGen.fill(*tauNus.tau);
      histosMatched.hNuGen.fill(*tauNus.taunu);
      histosMatched.hTauNuGen.fill(*tauNus.tau, *tauNus.taunu);
    }
  }
}

namespace {
  const reco::Candidate *findLastDaughter(const reco::Candidate& particle, int pdgId) {
    for(reco::Candidate::const_iterator id = particle.begin(); id != particle.end(); ++id) {
      if(std::abs(id->pdgId()) == pdgId) {
        const reco::Candidate *daughter = findLastDaughter(*id, pdgId);
        if(daughter != 0)
          return daughter;
        else
          return &(*id);
      }
    }
    return &particle;
  }
}

template <typename I>
void HPlusTauEmbeddingTauAnalyzer::findTauNuFromW(I begin, I end, std::vector<GenParticleTriple>& result) const {
  for(I iGen = begin; iGen != end; ++iGen) {
    int pdgId = std::abs(iGen->pdgId());
    if(pdgId != 24)
      continue;

    const reco::GenParticle *w = &(*iGen);
    const reco::GenParticle *tau = 0;
    const reco::GenParticle *nu = 0;
    for(reco::GenParticle::const_iterator iwd = w->begin(); iwd != w->end(); ++iwd) {
      if(std::abs(iwd->pdgId()) == 15) { // tau
        tau = dynamic_cast<const reco::GenParticle *>(findLastDaughter(*iwd, 15));
      }
      else if(std::abs(iwd->pdgId()) == 16) { // tau neutrino
        nu = dynamic_cast<const reco::GenParticle *>(findLastDaughter(*iwd, 16));
      }
    }
    if(tau != 0 && nu != 0) {
      const reco::GenParticle *tauNu = dynamic_cast<const reco::GenParticle *>(findLastDaughter(*tau, 16));
      if(tauNu != 0) {
        result.push_back(GenParticleTriple(tau, nu, tauNu));
      }
    }
  }
}


//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauEmbeddingTauAnalyzer);
