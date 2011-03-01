#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/Candidate/interface/Candidate.h"

namespace HPlus {
  TauEmbeddingAnalysis::Histograms::Histograms():
    hOriginalMet(0)
  {}
  TauEmbeddingAnalysis::Histograms::~Histograms() {}

  void TauEmbeddingAnalysis::Histograms::book(TFileDirectory& fd, const std::string& prefix) {
    hOriginalMet = makeTH<TH1F>(fd, (prefix+"_originalMet").c_str(), "Original MET", 400, 0, 400);
  }

  void TauEmbeddingAnalysis::Histograms::fill(double weight, const reco::Candidate& originalMet) {
    hOriginalMet->Fill(originalMet.et(), weight);
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

    fBegin.fill(fEventWeight.getWeight(), *fOriginalMet);    
  }

  void TauEmbeddingAnalysis::fillAfterTauId() {
    if(!fEnabled) return;
    fAfterTauId.fill(fEventWeight.getWeight(), *fOriginalMet);
  }
  void TauEmbeddingAnalysis::fillAfterMetCut() {
    if(!fEnabled) return;
    fAfterMetCut.fill(fEventWeight.getWeight(), *fOriginalMet);
  }
  void TauEmbeddingAnalysis::fillEnd() {
    if(!fEnabled) return;
    fEnd.fill(fEventWeight.getWeight(), *fOriginalMet);
  }
}
