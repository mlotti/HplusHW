#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
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

  TH1 *hMet;
  TH1 *hMetX;
  TH1 *hMetY;

  TH1 *hOrigMet;
  TH1 *hOrigMetX;
  TH1 *hOrigMetY;

  TH2 *hMetMet;

  Histo hMuon;
  Histo hTau;
  Histo hTauMatched;

  TH1 *hMuonTauDR;
};

HPlusTauEmbeddingAnalyzer::HPlusTauEmbeddingAnalyzer(const edm::ParameterSet& iConfig):
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  tauSrc_(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  metSrc_(iConfig.getUntrackedParameter<edm::InputTag>("metSrc")),
  origMetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("origMetSrc")),
  muonTauCone_(iConfig.getUntrackedParameter<double>("muonTauMatchingCone"))
{
  edm::Service<TFileService> fs;

  hMet = fs->make<TH1F>("met", "Tau+jets MET", 400, 0., 400.);
  hMetX = fs->make<TH1F>("met_x", "Tau+jets MET", 400, -200., 200.);
  hMetY = fs->make<TH1F>("met_y", "Tau+jets MET", 400, -200., 200.);

  hOrigMet = fs->make<TH1F>("metOriginal", "Mu+jets MET", 400, 0., 400.);
  hOrigMetX = fs->make<TH1F>("metOriginal_x", "Mu+jets MET", 400, -200., 200.);
  hOrigMetY = fs->make<TH1F>("metOriginal_y", "Mu+jets MET", 400, -200., 200.);

  hMetMet = fs->make<TH2F>("metMet", "Mu vs. tau+jets MET", 100,0.,500., 100,0.,500.);

  hMuon.init(*fs, "muon", "Muon");
  hTau.init(*fs, "tau", "Tau");
  hTauMatched.init(*fs, "tauMatched", "Tau");

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

  hMet->Fill(met->et());
  hMetX->Fill(met->px());
  hMetY->Fill(met->py());

  hOrigMet->Fill(origMet->et());
  hOrigMetX->Fill(origMet->px());
  hOrigMetY->Fill(origMet->py());

  hMetMet->Fill(origMet->et(), met->et());

  hMuon.fill(*muon);

  if(tau.isNonnull()) {
    hMuonTauDR->Fill(minDR);

    hTau.fill(*tau);

    if(minDR < muonTauCone_) {
      hTauMatched.fill(*tau);
    }
  }

}


//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauEmbeddingAnalyzer);
