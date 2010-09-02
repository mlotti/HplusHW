#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TH1F.h"

namespace HPlus {

  TauSelection::TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fLeadTrkPtCut(iConfig.getUntrackedParameter<double>("leadingTrackPtCut")),
    fPtCutCount(eventCounter.addCounter("Tau pt cut")),
    fEtaCutCount(eventCounter.addCounter("Tau eta cut")),
    fLeadTrkPtCount(eventCounter.addCounter("Tau leading track pt cut")),
    fAllSubCount(eventCounter.addSubCounter("Tau identification", "all tau candidates")),
    fPtCutSubCount(eventCounter.addSubCounter("Tau identification", "pt cut")),
    fEtaCutSubCount(eventCounter.addSubCounter("Tau identification", "eta cut")),
    fLeadTrkPtSubCount(eventCounter.addSubCounter("Tau identification", "leading track pt cut"))
  {
    edm::Service<TFileService> fs;
    hPt = fs->make<TH1F>("tau_pt", "tau_pt", 100, 0., 100.);
    hEta = fs->make<TH1F>("tau_eta", "tau_eta", 60, -3., 3.);
    hLeadTrkPt = fs->make<TH1F>("tau_leadtrk_pt", "tau_leadtrk_pt", 100, 0., 100.);
  }

  TauSelection::~TauSelection() {}

  bool TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);

    const edm::PtrVector<pat::Tau>& taus(htaus->ptrVector());

    edm::PtrVector<pat::Tau> selectedTaus;
    selectedTaus.reserve(taus.size());

    size_t ptCutPassed = 0;
    size_t etaCutPassed = 0;
    size_t leadTrkPtCutPassed = 0;

    // Fill initial histograms and do the first selection
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      edm::Ptr<pat::Tau> iTau = *iter;

      increment(fAllSubCount);

      hPt->Fill(iTau->pt());
      hEta->Fill(iTau->eta());
      reco::TrackRef leadTrk = iTau->leadTrack();
      if(leadTrk.isNonnull())
        hLeadTrkPt->Fill(leadTrk->pt());

      if(!(iTau->pt() > fPtCut)) continue;
      increment(fPtCutSubCount);
      ++ptCutPassed;

      if(!(std::abs(iTau->eta()) < fEtaCut)) continue;
      increment(fEtaCutSubCount);
      ++etaCutPassed;

      if(leadTrk.isNull() || !(leadTrk->pt() > fLeadTrkPtCut)) continue;
      increment(fLeadTrkPtSubCount);
      ++leadTrkPtCutPassed;

      selectedTaus.push_back(iTau);
    }

    if(ptCutPassed == 0) return false;
    increment(fPtCutCount);

    if(etaCutPassed == 0) return false;      
    increment(fEtaCutCount);

    if(leadTrkPtCutPassed == 0) return false;
    increment(fLeadTrkPtCount);      

    if(selectedTaus.size() > 1)
      // do something!
      return false;

    fSelectedTau = selectedTaus[0];
    return true;
  }
}
