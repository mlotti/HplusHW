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

#include<limits>

namespace HPlus {
  TauEmbeddingAnalysis::Histograms::Histograms():
    hOriginalMet(0)
  {}
  TauEmbeddingAnalysis::Histograms::~Histograms() {}

  void TauEmbeddingAnalysis::Histograms::book(TFileDirectory& fd, const std::string& prefix) {
    hOriginalMet = makeTH<TH1F>(fd, (prefix+"_originalMet").c_str(), "Original MET", 400, 0, 400);
    hEmbeddingMet = makeTH<TH1F>(fd, (prefix+"_embeddingMet").c_str(), "Embedding MET", 400, 0, 400);
    hEmbVSOrigMet = makeTH<TH2F>(fd, (prefix+"_embVSOrigMet").c_str(), "EmbeddingVSoriginal MET", 100, 0, 400, 100, 0, 400);

    hOriginalMuonPt = makeTH<TH1F>(fd, (prefix+"_originalMuonPt").c_str(), "OriginalMuon Pt", 400, 0, 400);
    hOriginalMuonEta = makeTH<TH1F>(fd, (prefix+"_originalMuonEta").c_str(), "OriginalMuon Eta", 300, -3,3);
    hOriginalMuonPhi = makeTH<TH1F>(fd, (prefix+"_originalMuonPhi").c_str(), "OriginalMuon Phi", 300, 0, 3.2);

    hSelectedTauPt = makeTH<TH1F>(fd, (prefix+"_selectedTauPt").c_str(), "SelectedTau Pt", 400, 0, 400);
    hSelectedTauEta = makeTH<TH1F>(fd, (prefix+"_selectedTauEta").c_str(), "SelectedTau Eta", 300, -3, 3);
    hSelectedTauPhi = makeTH<TH1F>(fd, (prefix+"_selectedTauPhi").c_str(), "SelectedTau Phi", 300, 0, 3.2);
    hSelectedTauIsolation05 = makeTH<TH1F>(fd, (prefix+"_selectedTauIsolation05").c_str(), "Selected tau sum(iso_cand_pt) for iso_cand_pt > 0.5", 100, 0, 100);
    hSelectedTauIsolation10 = makeTH<TH1F>(fd, (prefix+"_selectedTauIsolation10").c_str(), "Selected tau sum(iso_cand_pt) for iso_cand_pt > 1.0", 100, 0, 100);
    hleadPFChargedHadrPt = makeTH<TH1F>(fd, (prefix+"_leadPFChargedHadrPt").c_str(), "LeadPFChargedHadr Pt", 400, 0, 200);
    hRtau = makeTH<TH1F>(fd, (prefix+"_Rtau").c_str(), "Rtau", 400, 0, 1.2);

    hDeltaPhi = makeTH<TH1F>(fd, (prefix+"_DeltaPhi").c_str(), "DeltaPhi", 400, 0, 3.2);
    hDeltaPhiEmbVSOrig = makeTH<TH2F>(fd, (prefix+"_DeltaPhiEmbVSOrig").c_str(), "DeltaPhiEmbVSOrig", 100, 0, 3.2, 100, 0, 3.2);
    hTransverseMass = makeTH<TH1F>(fd, (prefix+"_TransverseMass").c_str(), "TransverseMass", 400, 0, 400);
    hDeltaPhiOriginal = makeTH<TH1F>(fd, (prefix+"_DeltaPhiOriginal").c_str(), "DeltaPhiOriginal", 400, 0, 3.2);
    hTransverseMassOriginal = makeTH<TH1F>(fd, (prefix+"_TransverseMassOriginal").c_str(), "TransverseMassOriginal", 400, 0, 400);
    hMTEmbVSOrig = makeTH<TH2F>(fd, (prefix+"_MTEmbVSOrig").c_str(), "MTEmbVSOrig", 100, 0, 400, 100, 0, 400);
  }

  void TauEmbeddingAnalysis::Histograms::fill(double weight, const reco::MET *originalMet, const reco::MET *embeddingMet, const reco::Muon *originalMuon, const pat::Tau *selectedTau) {
    // Fill only PFTaus
    if(selectedTau && !selectedTau->isPFTau())
      return;

    if(originalMet) {
      hOriginalMet->Fill(originalMet->et(), weight);
      hEmbVSOrigMet->Fill(embeddingMet->et(),originalMet->et(), weight);
    }

    if(embeddingMet) {
      hEmbeddingMet->Fill(embeddingMet->et(), weight);
    }

    if(originalMuon) {
      hOriginalMuonPt->Fill(originalMuon->pt(), weight);
      hOriginalMuonPt->Fill(originalMuon->pt(), weight);
      hOriginalMuonEta->Fill(originalMuon->eta(), weight);
      hOriginalMuonPhi->Fill(originalMuon->phi(), weight);
    }

    if(selectedTau) {
      hSelectedTauPt->Fill(selectedTau->pt(), weight);
      hSelectedTauEta->Fill(selectedTau->eta(), weight);
      hSelectedTauPhi->Fill(selectedTau->phi(), weight);

      // Leading track and Rtau 
      if (!selectedTau->leadPFChargedHadrCand().isNull()) {
        double LdgTrackPt = selectedTau->leadPFChargedHadrCand()->pt();
        hleadPFChargedHadrPt->Fill(LdgTrackPt, weight);
        if (selectedTau->energy() > 0) {
          double Rtau = selectedTau->leadPFChargedHadrCand()->p()/selectedTau->energy();
          hRtau->Fill(Rtau, weight);
        }
      }

      // Isolation
      reco::PFCandidateRefVector isoCands = selectedTau->isolationPFChargedHadrCands();
      if(isoCands.isNonnull()) {
        double pt05 = 0;
        double pt10 = 0;
        for(reco::PFCandidateRefVector::const_iterator isoCand = isoCands.begin(); isoCand != isoCands.end(); ++isoCand) {
          double pt = (*isoCand)->pt();
          if(pt > 0.5) {
            pt05 += pt;
            if(pt > 1.0) {
              pt10 += pt;
            }
          }
        }

        hSelectedTauIsolation05->Fill(pt05, weight);
        hSelectedTauIsolation10->Fill(pt10, weight);
      }
    }

    double deltaPhi = std::numeric_limits<double>::quiet_NaN();
    double transverseMass = std::numeric_limits<double>::quiet_NaN();
    if(selectedTau && embeddingMet) {
      deltaPhi = DeltaPhi::reconstruct(*selectedTau, *embeddingMet);
      hDeltaPhi->Fill(deltaPhi, weight);
      transverseMass = TransverseMass::reconstruct(*selectedTau, *embeddingMet );
      hTransverseMass->Fill(transverseMass, weight);
    }

    if(originalMuon && originalMet) {
      double deltaPhiOriginal = DeltaPhi::reconstruct(*originalMuon, *originalMet);
      hDeltaPhiOriginal->Fill(deltaPhiOriginal, weight);
      double transverseMassOriginal = TransverseMass::reconstruct(*originalMuon, *originalMet);
      hTransverseMassOriginal->Fill(transverseMassOriginal, weight);
      hDeltaPhiEmbVSOrig->Fill(deltaPhi,deltaPhiOriginal, weight);
      hMTEmbVSOrig->Fill(transverseMass, transverseMassOriginal, weight);    
    }
  }

  //////////

  TauEmbeddingAnalysis::TauEmbeddingAnalysis(const edm::ParameterSet& iConfig, EventWeight& eventWeight):
    fEmbeddingMetSrc(iConfig.getUntrackedParameter<edm::InputTag>("embeddingMetSrc")),
    fEmbeddingMode(iConfig.getUntrackedParameter<bool>("embeddingMode")),
    fEventWeight(eventWeight)
  {
    if(fEmbeddingMode) {
      fOriginalMuonSrc = iConfig.getUntrackedParameter<edm::InputTag>("originalMuon");
      fOriginalMetSrc = iConfig.getUntrackedParameter<edm::InputTag>("originalMetSrc");
    }

    edm::Service<TFileService> fs;
    std::string prefix("TauEmbeddingAnalysis_");

    fBegin.book(*fs, prefix+"begin");
    fAfterTauId.book(*fs, prefix+"afterTauId");
    fAfterMetCut.book(*fs, prefix+"afterMetCut");
    fEnd.book(*fs, prefix+"end");

  }
  TauEmbeddingAnalysis::~TauEmbeddingAnalysis() {}

  void TauEmbeddingAnalysis::beginEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    if(fEmbeddingMode) {
      edm::Handle<edm::View<reco::MET> > hOriginalMet;
      iEvent.getByLabel(fOriginalMetSrc, hOriginalMet);
      fOriginalMet = hOriginalMet->ptrAt(0);

      edm::Handle<edm::View<pat::Muon> > hOriginalMuon;
      iEvent.getByLabel(fOriginalMuonSrc, hOriginalMuon);
      fOriginalMuon = hOriginalMuon->ptrAt(0);
    }
    else {
      fOriginalMet = edm::Ptr<reco::MET>();
      fOriginalMuon = edm::Ptr<reco::Muon>();
    }

    edm::Handle<edm::View<reco::MET> > hEmbeddingMet;
    iEvent.getByLabel(fEmbeddingMetSrc, hEmbeddingMet);
    fEmbeddingMet = hEmbeddingMet->ptrAt(0);

    fSelectedTau = edm::Ptr<pat::Tau>();

    fBegin.fill(fEventWeight.getWeight(), fOriginalMet.get(), fEmbeddingMet.get(), fOriginalMuon.get(), fSelectedTau.get());
  }

  void TauEmbeddingAnalysis::setSelectedTau(const edm::Ptr<pat::Tau>& tau) {
    fSelectedTau = tau;
  }

  void TauEmbeddingAnalysis::fillAfterTauId() {
    fAfterTauId.fill(fEventWeight.getWeight(), fOriginalMet.get(), fEmbeddingMet.get(), fOriginalMuon.get(), fSelectedTau.get());
  }
  void TauEmbeddingAnalysis::fillAfterMetCut() {
    fAfterMetCut.fill(fEventWeight.getWeight(), fOriginalMet.get(), fEmbeddingMet.get(), fOriginalMuon.get(), fSelectedTau.get());
  }
  void TauEmbeddingAnalysis::fillEnd() {
    fEnd.fill(fEventWeight.getWeight(), fOriginalMet.get(), fEmbeddingMet.get(), fOriginalMuon.get(), fSelectedTau.get());
  }
}
