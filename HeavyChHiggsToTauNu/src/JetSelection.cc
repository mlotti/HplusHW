#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

namespace HPlus {

  JetSelection::JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fMaxDR(iConfig.getUntrackedParameter<double>("cleanTauDR")),
    fMin(iConfig.getUntrackedParameter<uint32_t>("minNumber")),
    fCleanCutCount(eventCounter.addCounter("Jet cleaning")),
    fPtCutCount(eventCounter.addCounter("Jet pt cut")),
    fEtaCutCount(eventCounter.addCounter("Jet eta cut")),
    fAllSubCount(eventCounter.addSubCounter("Jet selection", "all jets")),
    fCleanCutSubCount(eventCounter.addSubCounter("Jet selection", "cleaning")),
    fPtCutSubCount(eventCounter.addSubCounter("Jet selection", "pt cut")),
    fEtaCutSubCount(eventCounter.addSubCounter("Jet selection", "eta cut"))
  {
    edm::Service<TFileService> fs;
    hPt = fs->make<TH1F>("jet_pt", "het_pt", 100, 0., 100.);
    hEta = fs->make<TH1F>("jet_eta", "jet_eta", 60, -3., 3.);
  }

  JetSelection::~JetSelection() {}

  bool JetSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus) {
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fSrc, hjets);

    const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());

    fSelectedJets.clear();
    fSelectedJets.reserve(jets.size());

    size_t cleanPassed = 0;
    size_t ptCutPassed = 0;
    size_t etaCutPassed = 0;
    
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      increment(fAllSubCount);

      // remove tau jet
      bool match = false;
      for(edm::PtrVector<reco::Candidate>::const_iterator itertau = taus.begin(); itertau != taus.end(); ++itertau) {
        edm::Ptr<reco::Candidate> iTau = *itertau;
        if(!(ROOT::Math::VectorUtil::DeltaR(iTau->p4(), iJet->p4()) > fMaxDR)) {
          match = true;
          break;
        }
      }
      if(match) continue;
      increment(fCleanCutSubCount);
      ++cleanPassed;

      hPt->Fill(iJet->pt());
      hEta->Fill(iJet->eta());

      if(!(iJet->pt() > fPtCut)) continue;
      increment(fPtCutSubCount);
      ++ptCutPassed;

      if(!(std::abs(iJet->eta()) < fEtaCut)) continue;
      increment(fEtaCutSubCount);
      ++etaCutPassed;

      fSelectedJets.push_back(iJet);
    }

    if(cleanPassed < fMin) return false;
    increment(fCleanCutCount);

    if(ptCutPassed < fMin) return false;
    increment(fPtCutCount);

    if(etaCutPassed < fMin) return false;      
    increment(fEtaCutCount);
    return true;
  }
}
