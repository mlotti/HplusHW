#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingHistos.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaPhi.h"


#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "TH1F.h"
#include "TH2F.h"

namespace hplus {
  namespace te {
    Histo::Histo(): hPt(0), hEta(0), hPhi(0) {}
    Histo::~Histo() {}
    void Histo::init(TFileDirectory& dir, const std::string& name, const std::string& title) {
      hPt = dir.make<TH1F>((name+"_Pt").c_str(), (title+" pt").c_str(), 200, 0., 200.);
      hEta = dir.make<TH1F>((name+"_Eta").c_str(), (title+" eta").c_str(), 600, -3, 3.);
      hPhi = dir.make<TH1F>((name+"_Phi").c_str(), (title+" phi").c_str(), 700, -3.5, 3.5);
    }

    void Histo::fill(const reco::Candidate& cand) {
      hPt->Fill(cand.pt());
      hEta->Fill(cand.eta());
      hPhi->Fill(cand.phi());
    }

    ////////////////////////////////////////

    Histo2::Histo2():  hPt(0), hEta(0), hPhi(0) {}
    Histo2::~Histo2() {}

    void Histo2::init(TFileDirectory& dir, const std::string& name, const std::string& title) {
      hPt = dir.make<TH2F>((name+"_Pt").c_str(), (title+" pt").c_str(), 200,0,200, 200,0,200);
      hEta = dir.make<TH2F>((name+"_Eta").c_str(), (title+" eta").c_str(), 600,-3,3, 600,-3,3);
      hPhi = dir.make<TH2F>((name+"_Phi").c_str(), (title+" phi").c_str(), 700,-3.5,3.5, 700,-3.5, 3.5);

      std::string name2 = name;
      size_t pos = name.find_first_of('_');
      if(pos != std::string::npos)
        name2[pos] = ',';
      hDPt = dir.make<TH1F>((name2+"_DPt").c_str(), (title+" pt diff").c_str(), 400,-200,200);
      hDR = dir.make<TH1F>((name2+"_DR").c_str(), (title+" #Delta R").c_str(), 700,0,7);
      hDPhi = dir.make<TH1F>((name2+"_DPhi").c_str(), (title+" #Delta#phi").c_str(), 700,-3.5,3.5);
      hDEta = dir.make<TH1F>((name2+"_DEta").c_str(), (title+" #Delta#eta").c_str(), 600,-3,3);
    }

    void Histo2::fill(const reco::Candidate& x, const reco::Candidate& y) {
      hPt->Fill(x.pt(), y.pt());
      hEta->Fill(x.eta(), y.eta());
      hPhi->Fill(x.phi(), y.phi());

      hDPt->Fill(y.pt()-x.pt());
      hDR->Fill(reco::deltaR(y, x));
      hDPhi->Fill(reco::deltaPhi(y.phi(), x.phi()));
      hDEta->Fill(y.eta() - x.eta());
    }

    ////////////////////////////////////////

    HistoMet::HistoMet(const edm::InputTag src): src_(src) {}
    HistoMet::HistoMet() {}
    HistoMet::~HistoMet() {}

    void HistoMet::init(TFileDirectory& dir, const std::string& name, const std::string& title, const std::string& candName, const std::string& nuName) {
      hMet = dir.make<TH1F>((name+"_Et").c_str(), (title+" MET").c_str(), 400, 0., 400.);
      hMetX = dir.make<TH1F>((name+"_X").c_str(), (title+" MET X").c_str(), 400, -200., 200.);
      hMetY = dir.make<TH1F>((name+"_Y").c_str(), (title+" MET Y").c_str(), 400, -200., 200.);
      hMetPhi = dir.make<TH1F>((name+"_Phi").c_str(), (title+" MET phi").c_str(), 60, -3, 3.);

      hCandMetDPhi = dir.make<TH1F>((candName+","+name+"_DPhi").c_str(), ("DPhi("+candName+", MET)").c_str(), 700, -3.5, 3.5);

      hNuMetDPhi = dir.make<TH1F>(("Gen"+nuName+"Nu,"+name+"_DPhi").c_str(), ("DPhi(nu_"+nuName+", MET)").c_str(), 700, -3.5, 3.5);
    }

    const math::XYZTLorentzVector HistoMet::fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const edm::Event& iEvent) {
      edm::Handle<edm::View<reco::MET> > hmet;
      iEvent.getByLabel(src_, hmet);
      const math::XYZTLorentzVector& met = hmet->at(0).p4();
      fill(cand, candNu, met);
      return met;
    }

    void HistoMet::fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const math::XYZTLorentzVector& met) {
      hMet->Fill(met.Et());
      hMetX->Fill(met.px());
      hMetY->Fill(met.py());
      hMetPhi->Fill(met.phi());

      hCandMetDPhi->Fill(reco::deltaPhi(cand, met));

      if(candNu) {
        hNuMetDPhi->Fill(reco::deltaPhi(*candNu, met));
      }
    }

    ////////////////////////////////////////

    HistoMet2::HistoMet2(const edm::ParameterSet& pset, double metCut):
      metCut_(metCut),
      hMet(pset.getUntrackedParameter<edm::InputTag>("embeddedSrc")),
      hOrigMet(pset.getUntrackedParameter<edm::InputTag>("originalSrc"))
    {}

    HistoMet2::HistoMet2(double metCut):
      metCut_(metCut)
    {}
    HistoMet2::~HistoMet2() {}

    void HistoMet2::init(TFileDirectory& dir, const std::string& name) {
      hMet.init(dir, name, "Tau+jets", "Tau", "Tau");
      hOrigMet.init(dir, name+"Original", "Muon+jets", "Muon", "W");

      hOrigMetAfterCut = dir.make<TH1F>((name+"Original_Et_AfterCut").c_str(), "Tau+jets MET", 400, 0., 400.);

      std::string metmet = name+"Original_"+name+"_";
      hMetMet = dir.make<TH2F>((metmet+"Et").c_str(), "Muon vs. Tau+jets MET", 400,0.,400., 400,0.,400.);
      hMetMetX = dir.make<TH2F>((metmet+"X").c_str(), "Muon vs. Tau+jets MET x", 400,-200,200, 400,-200,200);
      hMetMetY = dir.make<TH2F>((metmet+"Y").c_str(), "Muon vs. Tau+jets MET y", 400,-200,200, 400,-200,200);
      hMetMetPhi = dir.make<TH2F>((metmet+"Phi").c_str(), "Muon vs. Tau+jets MET phi", 700,-3.5,3.5, 700,-3.5,3.5);

      hMuonMetDPhi = dir.make<TH1F>(("Muon,"+name+"_DPhi").c_str(), "DPhi(muon, MET)", 700, -3.5, 3.5);
      hTauOrigMetDPhi = dir.make<TH1F>(("Tau,"+name+"Original_DPhi").c_str(), "DPhi(tau, MET)", 700, -3.5, 3.5);

      hMuonOrigMetTauMetDPhi = dir.make<TH2F>(("Muon,"+name+"Original_Tau,"+name+"_DPhi").c_str(),
                                              "DPhi(muon, MET) vs. DPhi(tau, MET)",
                                              700,-3.5,3.5, 700,-3.5,3.5);

      hWTauNuMetDPhi = dir.make<TH1F>(("GenWTauNu,"+name+"_DPhi").c_str(), "DPhi(nu_W+nu_tau, MET)", 700, -3.5, 3.5);
      hWNuOrigMetMuonTauNuMetDPhi = dir.make<TH2F>(("GenWNu,"+name+"Original_GenWTauNu,"+name+"_DPhi").c_str(),
                                                      "DPhi(nu_muon, MET) vs. DPhi(nu_muon+nu_tau, MET)",
                                                      700,-3.5,3.5, 700,-3.5,3.5);

      std::string metdiff = name+","+name+"Original_";
      hMetOrigDiff = dir.make<TH1F>((metdiff+"DEt").c_str(), "MET_{#tau} - MET_{#mu}", 800,-400,400);
      hMetOrigDPhi = dir.make<TH1F>((metdiff+"DPhi").c_str(), "DPhi(MET_{#tau}, MET_{#mu}", 700,-3.5,3.5);
      hMuonOrigMetDPhiMetOrigDiff = dir.make<TH2F>(("Muon,"+name+"Original_DPhi_"+metdiff+"DEt").c_str(),
                                                   "DPhi(muon, MET_{#mu}) vs. MET_{#tau} - MET_{#mu}",
                                                   700,-3.5,3.5, 800,-400,400);
    }

    void HistoMet2::fill(const pat::Muon& muon, const reco::BaseTau& tau,
                        const reco::GenParticle *wNu, const reco::GenParticle *tauNu,
                        const edm::Event& iEvent) {
      math::XYZTLorentzVector metOrig = hOrigMet.fill(muon, wNu, iEvent);
      math::XYZTLorentzVector met = hMet.fill(tau, tauNu, iEvent);
      fillInternal(muon, tau, wNu, tauNu, metOrig, met);
    }

    void HistoMet2::fill(const reco::Candidate& muon, const reco::Candidate& tau,
                         const reco::GenParticle *wNu, const reco::GenParticle *tauNu,
                         const math::XYZTLorentzVector& metOrig, const math::XYZTLorentzVector& met) {
      hOrigMet.fill(muon, wNu, metOrig);
      hMet.fill(tau, tauNu, met);
      fillInternal(muon, tau, wNu, tauNu, metOrig, met);
    }

    void HistoMet2::fillInternal(const reco::Candidate& muon, const reco::Candidate& tau,
                                 const reco::GenParticle *wNu, const reco::GenParticle *tauNu,
                                 const math::XYZTLorentzVector& metOrig, const math::XYZTLorentzVector& met) {

      if(met.Et() > metCut_)
        hOrigMetAfterCut->Fill(metOrig.Et());

      hMetMet->Fill(metOrig.Et(), met.Et());
      hMetMetX->Fill(metOrig.px(), met.px());
      hMetMetY->Fill(metOrig.py(), met.py());
      hMetMetPhi->Fill(metOrig.phi(), met.phi());


      hMuonMetDPhi->Fill(reco::deltaPhi(muon.phi(), met.phi()));
      hTauOrigMetDPhi->Fill(reco::deltaPhi(tau.phi(), metOrig.phi()));

      double muonOrigMetDphi = reco::deltaPhi(muon.phi(), metOrig.phi());
      hMuonOrigMetTauMetDPhi->Fill(muonOrigMetDphi,
                                   reco::deltaPhi(tau.phi(), met.phi()));

      if(wNu && tauNu) {
        reco::GenParticle::LorentzVector wTauNu = wNu->p4()+tauNu->p4();
        double wTauNuMetDphi = reco::deltaPhi(wTauNu.phi(), met.phi());
        hWTauNuMetDPhi->Fill(wTauNuMetDphi);
        hWNuOrigMetMuonTauNuMetDPhi->Fill(reco::deltaPhi(wNu->phi(), metOrig.phi()),
                                          wTauNuMetDphi);
        /*
        std::cout << "Orig. met phi " << metOrig.phi() << " embedded met phi " << met.phi()
                  << " nu_mu phi " << wNu->phi() << " nu_tau phi " << tauNu->phi() << " nu_mu+nu_tau phi " << muonTauNu.phi()
                  << std::endl;
        */
      }

      double diff = met.Et() - metOrig.Et();
      hMetOrigDiff->Fill(diff);
      hMetOrigDPhi->Fill(reco::deltaPhi(met.phi(), metOrig.phi()));
      hMuonOrigMetDPhiMetOrigDiff->Fill(muonOrigMetDphi, diff);
    }
  }
}
