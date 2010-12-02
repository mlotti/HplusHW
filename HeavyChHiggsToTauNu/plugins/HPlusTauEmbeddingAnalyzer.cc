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

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingHistos.h"

#include "TH1F.h"
#include "TH2F.h"

using hplus::te::Histo;
using hplus::te::Histo2;
using hplus::te::HistoMet2;

class HPlusTauEmbeddingAnalyzer: public edm::EDAnalyzer {
 public:

  explicit HPlusTauEmbeddingAnalyzer(const edm::ParameterSet&);
  ~HPlusTauEmbeddingAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  typedef std::pair<const reco::GenParticle *, const reco::GenParticle *> GenParticlePair;
  template <typename I>
  GenParticlePair findTauNu(I begin, I end) const;
  template <typename I>
  GenParticlePair findMuNuFromW(const reco::Candidate& recoMu, I begin, I end) const;

  edm::InputTag muonSrc_;
  edm::InputTag tauSrc_;
  edm::InputTag genParticleOriginalSrc_;
  edm::InputTag genParticleEmbeddedSrc_;

  double muonTauCone_;

  struct HistoAll {
    HistoAll(double metCut): metCut_(metCut), hMetNu(metCut) {}
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
        HistoMet2 *met = new HistoMet2(pset.getUntrackedParameter<edm::ParameterSet>(*iName), metCut_);
        met->init(dir, *iName);
        hMets.push_back(met);
      }
      hMetNu.init(dir, "GenMetNu");      

      hMuon.init(dir, "Muon", "Muon");
      hMuonTrkIso = dir.make<TH1F>("Muon_IsoTrk", "Muon track isolation", 100, 0, 100);
      hMuonTrkRelIso = dir.make<TH1F>("Muon_IsoTrkRel", "Muon track relative isolation", 100, 0, 1);
      hMuonCaloIso = dir.make<TH1F>("Muon_IsoCalo", "Muon calo isolation", 100, 0, 100);
      hMuonCaloRelIso = dir.make<TH1F>("Muon_IsoCaloRel", "Muon calo relative isolation", 100, 0, 1);
      hMuonIso = dir.make<TH1F>("Muon_IsoTotal", "Muon total isolation", 50, 0, 50);
      hMuonRelIso = dir.make<TH1F>("Muon_IsoTotalRel", "Muon total relative isolation", 100, 0, 1);

      hTau.init(dir, "Tau", "Tau");
      hTauR = dir.make<TH1F>("Tau_Rtau", "Rtau", 120, 0., 1.2);
      hTauIsoChargedHadrPtSum = dir.make<TH1F>("Tau_IsoChargedHadrPtSum", "Tau isolation charged hadr cand pt sum", 100, 0, 100);
      hTauIsoChargedHadrPtSumRel = dir.make<TH1F>("Tau_IsoChargedHadrPtSumRel", "Tau isolation charged hadr cand relative pt sum", 200, 0, 20);
      hTauIsoChargedHadrPtMax = dir.make<TH1F>("Tau_IsoChargedHadrPtMax", "Tau isolation charged hadr cand pt max", 100, 0, 100);
      hTauIsoChargedHadrPtMaxRel = dir.make<TH1F>("Tau_IsoChargedHadrPtMaxRel", "Tau isolation charged hadr cand relative pt max", 200, 0, 20);

      hMuonTrkTauPtSumIso = dir.make<TH2F>("Muon_IsoTrk_Tau_IsoChargedHadrPtSum", "Muon trk vs. tau ptsum isolation", 100,0,100, 100,0,100);
      hMuonTrkTauPtSumIsoRel = dir.make<TH2F>("Muon_IsoTrkRel_Tau_IsoChargedHadrPtSumRel", "Muon trk vs. tau ptsum relative isolation", 200,0,1, 200,0,20);
      hMuonTauPtSumIso = dir.make<TH2F>("Muon_IsoTotal_Tau_IsoChargedHadrPtSum", "Muon total vs. tau ptsum isolation", 100,0,100, 200,0,20);
      hMuonTauPtSumIsoRel = dir.make<TH2F>("Muon_IsoTotal_Tau_IsoChargedHadrPtSumRel", "Muon total vs. tau ptsum relative isolation", 200,0,1, 200,0,20);

      hTauGen.init(dir, "GenTau", "Tau gen");
      hNuGen.init(dir, "GenTauNu", "Nu gen");
      hTauNuGen.init(dir, "GenTau_GenTauNu", "Gen tau vs. nu");

      hTauGenMass = dir.make<TH1F>("GenTau_Mass", "Tau mass at generator level", 100, 1.7, 1.9);
      hTauGenDecayMass = dir.make<TH1F>("GenTauDecay_Mass", "Tau mass from decay products at generator level", 100, 1.7, 1.9);

      hMuonTau.init(dir, "Muon_Tau", "Mu vs. tau");
      hMuonTauLdg.init(dir, "Muon_TauLdg", "Mu vs. tau ldg cand");

      hMuonTauDR = dir.make<TH1F>("Muon,Tau_DR", "DR(muon, tau)", 700, 0, 7);
      hMuonTauLdgDR = dir.make<TH1F>("Muon,TauLdg_DR", "DR(muon, tau ldg cand)", 700, 0, 7);
      hTauNuGenDR = dir.make<TH1F>("GenTau,GenTauNu_DR", "DR(tau, nu) gen", 700, 0, 7);
      hTauNuGenDEta = dir.make<TH1F>("GenTau,GenTauNu_DEta", "DEta(tau, nu) gen", 600, -3, 3);
      hTauNuGenDPhi = dir.make<TH1F>("GenTau,GenTauNu_DPhi", "DPhi(tau, nu) gen", 700, -3.5, 3.5);
    }

    void fillMets(const reco::Muon& muon, const reco::BaseTau& tau,
                  const reco::GenParticle *muonNu, const reco::GenParticle *tauNu,
                  const edm::Event& iEvent) {
      for(size_t i=0; i<hMets.size(); ++i) {
        hMets[i]->fill(muon, tau, muonNu, tauNu, iEvent);
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
    std::vector<HistoMet2 *> hMets;
    HistoMet2 hMetNu;

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
    TH1 *hTauR;

    TH2 *hMuonTrkTauPtSumIso;
    TH2 *hMuonTrkTauPtSumIsoRel;
    TH2 *hMuonTauPtSumIso;
    TH2 *hMuonTauPtSumIsoRel;

    Histo hTauGen;
    Histo hNuGen;
    Histo2 hTauNuGen;

    TH1 *hTauGenMass;
    TH1 *hTauGenDecayMass;

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
  genParticleOriginalSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleOriginalSrc")),
  genParticleEmbeddedSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleEmbeddedSrc")),
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

  edm::Handle<edm::View<reco::GenParticle> > hgenOriginal;
  iEvent.getByLabel(genParticleOriginalSrc_, hgenOriginal);
  GenParticlePair nuW = findMuNuFromW(*muon, hgenOriginal->begin(), hgenOriginal->end());

  edm::Handle<edm::View<reco::GenParticle> > hgenEmbedded;
  iEvent.getByLabel(genParticleEmbeddedSrc_, hgenEmbedded);
  GenParticlePair nuTau = findTauNu(hgenEmbedded->begin(), hgenEmbedded->end());

  reco::GenParticle::LorentzVector tauDecaySum;
  for(reco::GenParticle::const_iterator iDaughter = nuTau.second->begin(); iDaughter != nuTau.second->end(); ++iDaughter) {
    tauDecaySum += iDaughter->p4();
  }
  double tauDecayMass = tauDecaySum.M();

  histos.fillMets(*muon, *tau, nuW.first, nuTau.first, iEvent);
  reco::GenParticle::LorentzVector nuWTauSum;
  if(nuW.first && nuTau.first) {
    nuWTauSum = nuW.first->p4()+nuTau.first->p4();
    histos.hMetNu.fill(*muon, *tau, nuW.first, nuTau.first, nuW.first->p4(), nuWTauSum);
  }

  histos.hMuon.fill(*muon);
  histos.hMuonTauDR->Fill(minDR);
  histos.hTau.fill(*tau);
  histos.hMuonTau.fill(*muon, *tau);

  const reco::PFCandidateRef leadCand = tau->leadPFChargedHadrCand();
  if(leadCand.isNonnull()) {
    if(tau->p() > 0)
      histos.hTauR->Fill(leadCand->p()/tau->p());
    histos.hMuonTauLdgDR->Fill(reco::deltaR(*muon, *leadCand));
    histos.hMuonTauLdg.fill(*muon, *leadCand);
  }
                            

  histos.fillMuonTauIso(*muon, *tau);

  histos.hTauGen.fill(*nuTau.second);
  histos.hNuGen.fill(*nuTau.first);
  histos.hTauNuGen.fill(*nuTau.second, *nuTau.first);

  histos.hTauGenMass->Fill(nuTau.second->p4().M());
  histos.hTauGenDecayMass->Fill(tauDecayMass);

  histos.hTauNuGenDR->Fill(reco::deltaR(*nuTau.first, *nuTau.second));
  histos.hTauNuGenDPhi->Fill(reco::deltaPhi(nuTau.first->phi(), nuTau.second->phi()));
  histos.hTauNuGenDEta->Fill(nuTau.second->eta() - nuTau.first->eta());
                    
  if(minDR < muonTauCone_) {
    histosMatched.fillMets(*muon, *tau, nuW.first, nuTau.first, iEvent);
    if(nuW.first && nuTau.first) {
      histosMatched.hMetNu.fill(*muon, *tau, nuW.first, nuTau.first, nuW.first->p4(), nuWTauSum);
    }

    histosMatched.hMuon.fill(*muon);
    histosMatched.hMuonTauDR->Fill(minDR);
    histosMatched.hTau.fill(*tau);
    histosMatched.hMuonTau.fill(*muon, *tau);
    if(leadCand.isNonnull()) {
      if(tau->p() > 0)
        histosMatched.hTauR->Fill(leadCand->p()/tau->p());
      histosMatched.hMuonTauLdgDR->Fill(reco::deltaR(*muon, *leadCand));
      histosMatched.hMuonTauLdg.fill(*muon, *leadCand);
    }

    histosMatched.fillMuonTauIso(*muon, *tau);

    histosMatched.hTauGen.fill(*nuTau.second);
    histosMatched.hNuGen.fill(*nuTau.first);
    histosMatched.hTauNuGen.fill(*nuTau.second, *nuTau.first);

    histosMatched.hTauGenMass->Fill(nuTau.second->p4().M());
    histosMatched.hTauGenDecayMass->Fill(tauDecayMass);
  
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

template <typename I>
HPlusTauEmbeddingAnalyzer::GenParticlePair HPlusTauEmbeddingAnalyzer::findMuNuFromW(const reco::Candidate& recoMu, I begin, I end) const {

  GenParticlePair nearest(0, 0);
  double maxDR = 9999;
  for(I iGen = begin; iGen != end; ++iGen) {
    int pdgId = std::abs(iGen->pdgId());
    if(pdgId == 12 || pdgId == 14 || pdgId == 16) {
      const reco::GenParticle *particle = &(*(iGen));
      bool isFromMu = false;
      while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(particle->mother())) {
        particle = mother;
        if(std::abs(particle->pdgId()) == 24) {
          for(reco::GenParticle::const_iterator iDaughter = particle->begin(); iDaughter != particle->end(); ++iDaughter) {
            if(std::abs(iDaughter->pdgId()) == 13) {
              isFromMu = true;
              break;
            }
          }
          if(isFromMu)
            break;
        }
      }
      double deltaR = reco::deltaR(recoMu, *particle);
      if(isFromMu &&  deltaR < maxDR) {
        nearest = std::make_pair(&(*iGen), particle); // neutrino, mu
        maxDR = deltaR;
      }
    }
  }
  return nearest;
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauEmbeddingAnalyzer);
