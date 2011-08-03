#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingHistos.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "TH1F.h"
#include "TH2F.h"

namespace hplus {
  namespace te {
    Histo::Histo(const HPlus::EventWeight& eventWeight): fEventWeight(eventWeight), hPt(0), hEta(0), hPhi(0) {}
    Histo::~Histo() {}
    void Histo::init(TFileDirectory& dir, const std::string& name, const std::string& title) {
      hPt = HPlus::makeTH<TH1F>(dir, (name+"_Pt").c_str(), (title+" pt").c_str(), 200, 0., 200.);
      hEta = HPlus::makeTH<TH1F>(dir, (name+"_Eta").c_str(), (title+" eta").c_str(), 600, -3, 3.);
      hPhi = HPlus::makeTH<TH1F>(dir, (name+"_Phi").c_str(), (title+" phi").c_str(), 700, -3.5, 3.5);
    }

    //void Histo::fill(const reco::Candidate& cand) {
    void Histo::fill(const math::XYZTLorentzVector& cand) {
      hPt->Fill(cand.pt(), fEventWeight.getWeight());
      hEta->Fill(cand.eta(), fEventWeight.getWeight());
      hPhi->Fill(cand.phi(), fEventWeight.getWeight());
    }

    ////////////////////////////////////////
    HistoTrack::HistoTrack(const HPlus::EventWeight& eventWeight): fEventWeight(eventWeight), hNhits(0), hChi2Norm(0), hDxy(0), hDz(0) {}
    HistoTrack::~HistoTrack() {}
    void HistoTrack::init(TFileDirectory& dir, const std::string& name, const std::string& title) {
      hNhits = HPlus::makeTH<TH1F>(dir, (name+"_TrackNhits").c_str(), (title+" track N hits").c_str(), 80, 0, 80);
      hChi2Norm = HPlus::makeTH<TH1F>(dir, (name+"_TrackChi2Norm").c_str(), (title+" track chi2/ndof").c_str(), 200, 0, 20);
      hDxy = HPlus::makeTH<TH1F>(dir, (name+"_TrackDxy").c_str(), (title+" track dxy").c_str(), 200, 0, 0.2);
      hDz = HPlus::makeTH<TH1F>(dir, (name+"_TrackDz").c_str(), (title+" track dz").c_str(), 100, 0, 1.0);
    }

    void HistoTrack::fill(const reco::Track& track, const math::XYZPoint& vertex) {
      hNhits->Fill(track.numberOfValidHits(), fEventWeight.getWeight());
      hChi2Norm->Fill(track.normalizedChi2(), fEventWeight.getWeight());
      hDxy->Fill(std::abs(track.dxy(vertex)), fEventWeight.getWeight());
      hDz->Fill(std::abs(track.dz(vertex)), fEventWeight.getWeight());
    }


    ////////////////////////////////////////

    Histo2::Histo2(const HPlus::EventWeight& eventWeight): fEventWeight(eventWeight), hPt(0), hEta(0), hPhi(0) {}
    Histo2::~Histo2() {}

    void Histo2::init(TFileDirectory& dir, const std::string& name, const std::string& title) {
      hPt = HPlus::makeTH<TH2F>(dir, (name+"_Pt").c_str(), (title+" pt").c_str(), 200,0,200, 200,0,200);
      hEta = HPlus::makeTH<TH2F>(dir, (name+"_Eta").c_str(), (title+" eta").c_str(), 600,-3,3, 600,-3,3);
      hPhi = HPlus::makeTH<TH2F>(dir, (name+"_Phi").c_str(), (title+" phi").c_str(), 700,-3.5,3.5, 700,-3.5, 3.5);

      std::string name2 = name;
      size_t pos = name.find_first_of('_');
      if(pos != std::string::npos)
        name2[pos] = ',';
      hDPt = HPlus::makeTH<TH1F>(dir, (name2+"_DPt").c_str(), (title+" pt diff").c_str(), 400,-200,200);
      hDR = HPlus::makeTH<TH1F>(dir, (name2+"_DR").c_str(), (title+" #Delta R").c_str(), 700,0,7);
      hDPhi = HPlus::makeTH<TH1F>(dir, (name2+"_DPhi").c_str(), (title+" #Delta#phi").c_str(), 700,-3.5,3.5);
      hDEta = HPlus::makeTH<TH1F>(dir, (name2+"_DEta").c_str(), (title+" #Delta#eta").c_str(), 600,-3,3);
    }

    //void Histo2::fill(const reco::Candidate& x, const reco::Candidate& y) {
    void Histo2::fill(const math::XYZTLorentzVector& x, const math::XYZTLorentzVector& y) {
      hPt->Fill(x.pt(), y.pt(), fEventWeight.getWeight());
      hEta->Fill(x.eta(), y.eta(), fEventWeight.getWeight());
      hPhi->Fill(x.phi(), y.phi(), fEventWeight.getWeight());

      hDPt->Fill(y.pt()-x.pt(), fEventWeight.getWeight());
      hDR->Fill(reco::deltaR(y, x), fEventWeight.getWeight());
      hDPhi->Fill(reco::deltaPhi(y.phi(), x.phi()), fEventWeight.getWeight());
      hDEta->Fill(y.eta() - x.eta(), fEventWeight.getWeight());
    }

    ////////////////////////////////////////

    HistoMet::HistoMet(const edm::InputTag src, const HPlus::EventWeight& eventWeight): src_(src), fEventWeight(eventWeight) {}
    HistoMet::HistoMet(const HPlus::EventWeight& eventWeight): fEventWeight(eventWeight) {}
    HistoMet::~HistoMet() {}

    void HistoMet::init(TFileDirectory& dir, const std::string& name, const std::string& title, const std::string& candName, const std::string& nuName) {
      hMet = HPlus::makeTH<TH1F>(dir, (name+"_Et").c_str(), (title+" MET").c_str(), 400, 0., 400.);
      hMetX = HPlus::makeTH<TH1F>(dir, (name+"_X").c_str(), (title+" MET X").c_str(), 400, -200., 200.);
      hMetY = HPlus::makeTH<TH1F>(dir, (name+"_Y").c_str(), (title+" MET Y").c_str(), 400, -200., 200.);
      hMetPhi = HPlus::makeTH<TH1F>(dir, (name+"_Phi").c_str(), (title+" MET phi").c_str(), 60, -3, 3.);

      hCandMetDPhi = HPlus::makeTH<TH1F>(dir, (candName+","+name+"_DPhi").c_str(), ("DPhi("+candName+", MET)").c_str(), 700, -3.5, 3.5);

      hNuMetDPhi = HPlus::makeTH<TH1F>(dir, ("Gen"+nuName+"Nu,"+name+"_DPhi").c_str(), ("DPhi(nu_"+nuName+", MET)").c_str(), 700, -3.5, 3.5);
    }

    const math::XYZTLorentzVector HistoMet::fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const edm::Event& iEvent) {
      edm::Handle<edm::View<reco::MET> > hmet;
      iEvent.getByLabel(src_, hmet);
      const math::XYZTLorentzVector& met = hmet->at(0).p4();
      fill(cand, candNu, met);
      return met;
    }

    void HistoMet::fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const math::XYZTLorentzVector& met) {
      hMet->Fill(met.Et(), fEventWeight.getWeight());
      hMetX->Fill(met.px(), fEventWeight.getWeight());
      hMetY->Fill(met.py(), fEventWeight.getWeight());
      hMetPhi->Fill(met.phi(), fEventWeight.getWeight());

      hCandMetDPhi->Fill(reco::deltaPhi(cand, met), fEventWeight.getWeight());

      if(candNu) {
        hNuMetDPhi->Fill(reco::deltaPhi(*candNu, met), fEventWeight.getWeight());
      }
    }

    ////////////////////////////////////////

    HistoMet2::HistoMet2(const edm::ParameterSet& pset, double metCut, const HPlus::EventWeight& eventWeight):
      metCut_(metCut),
      fEventWeight(eventWeight),
      hMet(pset.getUntrackedParameter<edm::InputTag>("embeddedSrc"), fEventWeight),
      hOrigMet(pset.getUntrackedParameter<edm::InputTag>("originalSrc"), fEventWeight)
    {}

    HistoMet2::HistoMet2(double metCut, const HPlus::EventWeight& eventWeight):
      metCut_(metCut),
      fEventWeight(eventWeight),
      hMet(fEventWeight),
      hOrigMet(fEventWeight)
    {}
    HistoMet2::~HistoMet2() {}

    void HistoMet2::init(TFileDirectory& dir, const std::string& name) {
      hMet.init(dir, name, "Tau+jets", "Tau", "Tau");
      hOrigMet.init(dir, name+"Original", "Muon+jets", "Muon", "W");

      hOrigMetAfterCut = HPlus::makeTH<TH1F>(dir, (name+"Original_Et_AfterCut").c_str(), "Tau+jets MET", 400, 0., 400.);

      std::string metmet = name+"Original_"+name+"_";
      hMetMet = HPlus::makeTH<TH2F>(dir, (metmet+"Et").c_str(), "Muon vs. Tau+jets MET", 400,0.,400., 400,0.,400.);
      hMetMetX = HPlus::makeTH<TH2F>(dir, (metmet+"X").c_str(), "Muon vs. Tau+jets MET x", 400,-200,200, 400,-200,200);
      hMetMetY = HPlus::makeTH<TH2F>(dir, (metmet+"Y").c_str(), "Muon vs. Tau+jets MET y", 400,-200,200, 400,-200,200);
      hMetMetPhi = HPlus::makeTH<TH2F>(dir, (metmet+"Phi").c_str(), "Muon vs. Tau+jets MET phi", 700,-3.5,3.5, 700,-3.5,3.5);

      hMuonMetDPhi = HPlus::makeTH<TH1F>(dir, ("Muon,"+name+"_DPhi").c_str(), "DPhi(muon, MET)", 700, -3.5, 3.5);
      hTauOrigMetDPhi = HPlus::makeTH<TH1F>(dir, ("Tau,"+name+"Original_DPhi").c_str(), "DPhi(tau, MET)", 700, -3.5, 3.5);

      hMuonOrigMetTauMetDPhi = HPlus::makeTH<TH2F>(dir, ("Muon,"+name+"Original_Tau,"+name+"_DPhi").c_str(),
                                              "DPhi(muon, MET) vs. DPhi(tau, MET)",
                                              700,-3.5,3.5, 700,-3.5,3.5);

      hMuonOrigMetMt = HPlus::makeTH<TH1F>(dir, ("Muon,"+name+"Original_Mt").c_str(), "Mt(muon, MET)", 200, 0, 200);
      hTauMetMt = HPlus::makeTH<TH1F>(dir, ("Tau,"+name+"_Mt").c_str(), "Mt(tau, MET)", 200, 0, 200);

      hWTauNuMetDPhi = HPlus::makeTH<TH1F>(dir, ("GenWTauNu,"+name+"_DPhi").c_str(), "DPhi(nu_W+nu_tau, MET)", 700, -3.5, 3.5);
      hWNuOrigMetMuonTauNuMetDPhi = HPlus::makeTH<TH2F>(dir, ("GenWNu,"+name+"Original_GenWTauNu,"+name+"_DPhi").c_str(),
                                                      "DPhi(nu_muon, MET) vs. DPhi(nu_muon+nu_tau, MET)",
                                                      700,-3.5,3.5, 700,-3.5,3.5);

      std::string metdiff = name+","+name+"Original_";
      hMetOrigDiff = HPlus::makeTH<TH1F>(dir, (metdiff+"DEt").c_str(), "MET_{#tau} - MET_{#mu}", 800,-400,400);
      hMetOrigDPhi = HPlus::makeTH<TH1F>(dir, (metdiff+"DPhi").c_str(), "DPhi(MET_{#tau}, MET_{#mu}", 700,-3.5,3.5);
      hMuonOrigMetDPhiMetOrigDiff = HPlus::makeTH<TH2F>(dir, ("Muon,"+name+"Original_DPhi_"+metdiff+"DEt").c_str(),
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
        hOrigMetAfterCut->Fill(metOrig.Et(), fEventWeight.getWeight());

      hMetMet->Fill(metOrig.Et(), met.Et(), fEventWeight.getWeight());
      hMetMetX->Fill(metOrig.px(), met.px(), fEventWeight.getWeight());
      hMetMetY->Fill(metOrig.py(), met.py(), fEventWeight.getWeight());
      hMetMetPhi->Fill(metOrig.phi(), met.phi(), fEventWeight.getWeight());


      hMuonMetDPhi->Fill(reco::deltaPhi(muon.phi(), met.phi()), fEventWeight.getWeight());
      hTauOrigMetDPhi->Fill(reco::deltaPhi(tau.phi(), metOrig.phi()), fEventWeight.getWeight());

      double origMt = std::sqrt(2 * muon.pt() * metOrig.Et() * (1 - cos(muon.phi() - metOrig.phi())));
      double embMt = std::sqrt(2 * tau.pt() * met.Et() * (1 - cos(tau.phi() - met.phi())));
      hMuonOrigMetMt->Fill(origMt, fEventWeight.getWeight());
      hTauMetMt->Fill(embMt, fEventWeight.getWeight());
        
      double muonOrigMetDphi = reco::deltaPhi(muon.phi(), metOrig.phi());
      hMuonOrigMetTauMetDPhi->Fill(muonOrigMetDphi,
                                   reco::deltaPhi(tau.phi(), met.phi()), fEventWeight.getWeight());

      if(wNu && tauNu) {
        reco::GenParticle::LorentzVector wTauNu = wNu->p4()+tauNu->p4();
        double wTauNuMetDphi = reco::deltaPhi(wTauNu.phi(), met.phi());
        hWTauNuMetDPhi->Fill(wTauNuMetDphi, fEventWeight.getWeight());
        hWNuOrigMetMuonTauNuMetDPhi->Fill(reco::deltaPhi(wNu->phi(), metOrig.phi()),
                                          wTauNuMetDphi, fEventWeight.getWeight());
        /*
        std::cout << "Orig. met phi " << metOrig.phi() << " embedded met phi " << met.phi()
                  << " nu_mu phi " << wNu->phi() << " nu_tau phi " << tauNu->phi() << " nu_mu+nu_tau phi " << muonTauNu.phi()
                  << std::endl;
        */
      }

      double diff = met.Et() - metOrig.Et();
      hMetOrigDiff->Fill(diff, fEventWeight.getWeight());
      hMetOrigDPhi->Fill(reco::deltaPhi(met.phi(), metOrig.phi()), fEventWeight.getWeight());
      hMuonOrigMetDPhiMetOrigDiff->Fill(muonOrigMetDphi, diff, fEventWeight.getWeight());
    }

    ////////////////////////////////////////

    HistoIso::HistoIso(const HPlus::EventWeight& eventWeight): fEventWeight(eventWeight), hSumPt(0), hOccupancy(0) {}
    HistoIso::~HistoIso() {}
    void HistoIso::init(TFileDirectory& dir, const std::string& name) {
      hSumPt = HPlus::makeTH<TH1F>(dir, (name+"SumPt").c_str(), (name+" sum pt").c_str(), 200, 0, 100);
      hMaxPt = HPlus::makeTH<TH1F>(dir, (name+"MaxPt").c_str(), (name+" max pt").c_str(), 200, 0, 100);
      hOccupancy = HPlus::makeTH<TH1F>(dir, (name+"Occupancy").c_str(), (name+" occupancy").c_str(), 20, 0, 20);
    }
    void HistoIso::fill(double sumPt, double maxPt, size_t occupancy) {
      hSumPt->Fill(sumPt, fEventWeight.getWeight());
      hMaxPt->Fill(maxPt, fEventWeight.getWeight());
      hOccupancy->Fill(occupancy, fEventWeight.getWeight());
    }

    HistoIso2::HistoIso2(const HPlus::EventWeight& eventWeight): fEventWeight(eventWeight), hSumPt(0), hOccupancy(0) {}
    HistoIso2::~HistoIso2() {}
    void HistoIso2::init(TFileDirectory& dir, const std::string& muonName, const std::string& tauName) {
      hSumPt = HPlus::makeTH<TH2F>(dir, ("Muon_"+muonName+"_Tau_"+tauName+"SumPt").c_str(),
                              ("Muon "+muonName+" vs. tau "+tauName+ " sum pt").c_str(),
                              100,0,0.5, 100,0,100);
      hMaxPt = HPlus::makeTH<TH2F>(dir, ("Muon_"+muonName+"_Tau_"+tauName+"MaxPt").c_str(),
                              ("Muon "+muonName+" vs. tau "+tauName+ " max pt").c_str(),
                              100,0,0.5, 100,0,100);
      hOccupancy = HPlus::makeTH<TH2F>(dir, ("Muon_"+muonName+"_Tau_"+tauName+"Occupancy").c_str(),
                                  ("Muon "+muonName+" vs. tau "+tauName+ " occupancy").c_str(),
                                  100,0,0.5, 100,0,100);
    }
    void HistoIso2::fill(double muonIso, double tauSumPt, double tauMaxPt, size_t tauOccupancy) {
      hSumPt->Fill(muonIso, tauSumPt, fEventWeight.getWeight());
      hMaxPt->Fill(muonIso, tauMaxPt, fEventWeight.getWeight());
      hOccupancy->Fill(muonIso, tauOccupancy, fEventWeight.getWeight());
    }
  }
}
