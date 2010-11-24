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

#include "DataFormats/Math/interface/deltaR.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TH2F.h"

class HPlusTauEmbeddingAnalyzer: public edm::EDAnalyzer {
 public:

  explicit HPlusTauEmbeddingAnalyzer(const edm::ParameterSet&);
  ~HPlusTauEmbeddingAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag muonSrc_;
  edm::InputTag tauSrc_;
  edm::InputTag metSrc_;
  edm::InputTag origMetSrc_;
  edm::InputTag genMetSrc_;
  edm::InputTag origGenMetSrc_;

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
    HistoMet(): hMet(0), hMetX(0), hOrigMet(0), hOrigMetX(0), hOrigMetY(0), hMetMet(0), hMetMetX(0), hMetMetY(0) {}

    void init(TFileDirectory& dir, const std::string& name) {
      hMet = dir.make<TH1F>((name+"Met").c_str(), "Tau+jets MET", 400, 0., 400.);
      hMetX = dir.make<TH1F>((name+"Met_x").c_str(), "Tau+jets MET", 400, -200., 200.);
      hMetY = dir.make<TH1F>((name+"Met_y").c_str(), "Tau+jets MET", 400, -200., 200.);

      hOrigMet = dir.make<TH1F>((name+"MetOriginal").c_str(), "Mu+jets MET", 400, 0., 400.);
      hOrigMetX = dir.make<TH1F>((name+"MetOriginal_x").c_str(), "Mu+jets MET", 400, -200., 200.);
      hOrigMetY = dir.make<TH1F>((name+"MetOriginal_y").c_str(), "Mu+jets MET", 400, -200., 200.);

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

      hMetMet->Fill(metOrig.et(), met.et());
      hMetMetX->Fill(metOrig.px(), met.px());
      hMetMetY->Fill(metOrig.py(), met.py());

    }

    TH1 *hMet;
    TH1 *hMetX;
    TH1 *hMetY;

    TH1 *hOrigMet;
    TH1 *hOrigMetX;
    TH1 *hOrigMetY;

    TH2 *hMetMet;
    TH2 *hMetMetX;
    TH2 *hMetMetY;
  };

  HistoMet hMet;
  HistoMet hMetMatched;
  HistoMet hGenMet;
  HistoMet hGenMetMatched;

  Histo hMuon;
  Histo hTau;
  Histo hTauMatched;

  Histo2 hMuonTau;
  Histo2 hMuonTauMatched;

  TH1 *hMuonTauDR;
};

HPlusTauEmbeddingAnalyzer::HPlusTauEmbeddingAnalyzer(const edm::ParameterSet& iConfig):
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  tauSrc_(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  metSrc_(iConfig.getUntrackedParameter<edm::InputTag>("metSrc")),
  origMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("origMetSrc")),
  genMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genMetSrc")),
  origGenMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("origGenMetSrc")),
  muonTauCone_(iConfig.getUntrackedParameter<double>("muonTauMatchingCone"))
{
  edm::Service<TFileService> fs;

  hMet.init(*fs, "");
  hMetMatched.init(*fs, "tauMatched");

  hGenMet.init(*fs, "Gen");
  hGenMetMatched.init(*fs, "tauMatchedGen");

  hMuon.init(*fs, "muon", "Muon");
  hTau.init(*fs, "tau", "Tau");
  hTauMatched.init(*fs, "tauMatched", "Tau");

  hMuonTau.init(*fs, "muonTau", "Mu vs. tau");
  hMuonTauMatched.init(*fs, "muonTauMatched", "Mu vs. tau");

  hMuonTauDR = fs->make<TH1F>("muonTauDR", "DR(muon, tau)", 70, 0, 7);
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

  hMet.fill(*met, *origMet);
  hGenMet.fill(*genMet, *origGenMet);

  hMuon.fill(*muon);
  hMuonTauDR->Fill(minDR);
  hTau.fill(*tau);
  hMuonTau.fill(*muon, *tau);

  if(minDR < muonTauCone_) {
    hTauMatched.fill(*tau);
    hMuonTauMatched.fill(*muon, *tau);
    hMetMatched.fill(*met, *origMet);
    hGenMetMatched.fill(*genMet, *origGenMet);
  }

}


//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauEmbeddingAnalyzer);
