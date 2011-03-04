#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

namespace HPlus {
  TauEmbeddingAnalysis::Histograms::Histograms():
    hOriginalMet(0)
  {}
  TauEmbeddingAnalysis::Histograms::~Histograms() {}

  void TauEmbeddingAnalysis::Histograms::book(TFileDirectory& fd, const std::string& prefix) {
    hOriginalMet = makeTH<TH1F>(fd, (prefix+"_originalMet").c_str(), "Original MET", 400, 0, 400);
    hEmbeddingMet = makeTH<TH1F>(fd, (prefix+"_embeddingMet").c_str(), "Embedding MET", 400, 0, 400);
    hOriginalMuonPt = makeTH<TH1F>(fd, (prefix+"_originalMuonPt").c_str(), "OriginalMuon Pt", 400, 0, 400);
    hOriginalMuonEta = makeTH<TH1F>(fd, (prefix+"_originalMuonEta").c_str(), "OriginalMuon Eta", 300, -3,3);
    hOriginalMuonPhi = makeTH<TH1F>(fd, (prefix+"_originalMuonPhi").c_str(), "OriginalMuon Phi", 300, 0, 3.2);
    hSelectedTauPt = makeTH<TH1F>(fd, (prefix+"_selectedTauPt").c_str(), "SelectedTau Pt", 400, 0, 400);
    hSelectedTauEta = makeTH<TH1F>(fd, (prefix+"_selectedTauEta").c_str(), "SelectedTau Eta", 300, -3, 3);
    hSelectedTauPhi = makeTH<TH1F>(fd, (prefix+"_selectedTauPhi").c_str(), "SelectedTau Phi", 300, 0, 3.2);
    hleadPFChargedHadrPt = makeTH<TH1F>(fd, (prefix+"_leadPFChargedHadrPt").c_str(), "LeadPFChargedHadr Pt", 400, 0, 200);
    hRtau = makeTH<TH1F>(fd, (prefix+"_Rtau").c_str(), "Rtau", 400, 0, 1.2);
    hDeltaPhi = makeTH<TH1F>(fd, (prefix+"_DeltaPhi").c_str(), "DeltaPhi", 400, 0, 3.2);
    hTransverseMass = makeTH<TH1F>(fd, (prefix+"_TransverseMass").c_str(), "TransverseMass", 400, 0, 400);
    hDeltaPhiOriginal = makeTH<TH1F>(fd, (prefix+"_DeltaPhiOriginal").c_str(), "DeltaPhiOriginal", 400, 0, 3.2);
    hTransverseMassOriginal = makeTH<TH1F>(fd, (prefix+"_TransverseMassOriginal").c_str(), "TransverseMassOriginal", 400, 0, 400);
  }

  void TauEmbeddingAnalysis::Histograms::fill(double weight, const reco::MET& originalMet, const reco::MET& embeddingMet, const reco::Muon& originalMuon) {
    hOriginalMet->Fill(originalMet.et(), weight);
    hEmbeddingMet->Fill(embeddingMet.et(), weight);
    hOriginalMuonPt->Fill(originalMuon.pt(), weight);
    hOriginalMuonPt->Fill(originalMuon.pt(), weight);
    hOriginalMuonEta->Fill(originalMuon.eta(), weight);
    hOriginalMuonPhi->Fill(originalMuon.phi(), weight);
  }
  void TauEmbeddingAnalysis::Histograms::fill(double weight, const reco::MET& originalMet, const reco::MET& embeddingMet, const reco::Muon& originalMuon, const pat::Tau& selectedTau) {
    fill(weight, originalMet, embeddingMet, originalMuon);
    hSelectedTauPt->Fill(selectedTau.pt(), weight);
    hSelectedTauEta->Fill(selectedTau.eta(), weight);
    hSelectedTauPhi->Fill(selectedTau.phi(), weight);
    // Leading track and Rtau 
    if (!selectedTau.leadPFChargedHadrCand().isNull()) {
      double LdgTrackPt = selectedTau.leadPFChargedHadrCand()->p();
      hleadPFChargedHadrPt->Fill(LdgTrackPt, weight);
      if (selectedTau.energy() > 0) {
	double Rtau = selectedTau.leadPFChargedHadrCand()->p()/selectedTau.energy();
        hRtau->Fill(Rtau, weight);
      }
    }
 
    double deltaPhi = DeltaPhi::reconstruct(selectedTau, embeddingMet);
    hDeltaPhi->Fill(deltaPhi);
    double transverseMass = TransverseMass::reconstruct(selectedTau, embeddingMet );
    hTransverseMass->Fill(transverseMass);

    double deltaPhiOriginal = DeltaPhi::reconstruct(originalMuon, originalMet);
    hDeltaPhiOriginal->Fill(deltaPhiOriginal);
    double transverseMassOriginal = TransverseMass::reconstruct(originalMuon, originalMet );
    hTransverseMassOriginal->Fill(transverseMassOriginal);
   
  }

  //////////

  TauEmbeddingAnalysis::TauEmbeddingAnalysis(EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fEnabled(false)
  {}
  TauEmbeddingAnalysis::~TauEmbeddingAnalysis() {}

  void TauEmbeddingAnalysis::init(const edm::ParameterSet& iConfig) {
    fEnabled = true;
    fOriginalMetSrc = iConfig.getUntrackedParameter<edm::InputTag>("originalMetSrc");
    fEmbeddingMetSrc = iConfig.getUntrackedParameter<edm::InputTag>("embeddingMetSrc");
    fOriginalMuonSrc = iConfig.getUntrackedParameter<edm::InputTag>("originalMuon");
    fSelectedTauSrc = iConfig.getUntrackedParameter<edm::InputTag>("selectedTauSrc");

    edm::Service<TFileService> fs;
    std::string prefix("TauEmbeddingAnalysis_");

    fBegin.book(*fs, prefix+"begin");
    fAfterTauId.book(*fs, prefix+"afterTauId");
    fAfterMetCut.book(*fs, prefix+"afterMetCut");
    fEnd.book(*fs, prefix+"end");
  }

  void TauEmbeddingAnalysis::beginEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    if(!fEnabled) return;

    edm::Handle<edm::View<reco::MET> > hOriginalMet;
    iEvent.getByLabel(fOriginalMetSrc, hOriginalMet);
    fOriginalMet = hOriginalMet->ptrAt(0);

    edm::Handle<edm::View<reco::MET> > hEmbeddingMet;
    iEvent.getByLabel(fEmbeddingMetSrc, hEmbeddingMet);
    fEmbeddingMet = hEmbeddingMet->ptrAt(0);

    edm::Handle<edm::View<pat::Muon> > hOriginalMuon;
    iEvent.getByLabel(fOriginalMuonSrc, hOriginalMuon);
    fOriginalMuon = hOriginalMuon->ptrAt(0);

    fSelectedTau = edm::Ptr<pat::Tau>();

    fBegin.fill(fEventWeight.getWeight(), *fOriginalMet, *fEmbeddingMet, *fOriginalMuon);    
  }

  void TauEmbeddingAnalysis::setSelectedTau(const edm::Ptr<pat::Tau>& tau) {
    fSelectedTau = tau;
  }

  void TauEmbeddingAnalysis::fillAfterTauId() {
    if(!fEnabled) return;
    fAfterTauId.fill(fEventWeight.getWeight(), *fOriginalMet, *fEmbeddingMet, *fOriginalMuon, *fSelectedTau);
  }
  void TauEmbeddingAnalysis::fillAfterMetCut() {
    if(!fEnabled) return;
    fAfterMetCut.fill(fEventWeight.getWeight(), *fOriginalMet, *fEmbeddingMet, *fOriginalMuon, *fSelectedTau);
  }
  void TauEmbeddingAnalysis::fillEnd() {
    if(!fEnabled) return;
    fEnd.fill(fEventWeight.getWeight(), *fOriginalMet, *fEmbeddingMet, *fOriginalMuon, *fSelectedTau);
  }
}
