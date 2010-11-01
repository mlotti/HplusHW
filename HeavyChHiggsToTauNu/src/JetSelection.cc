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
    //    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter),
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSrc_met(iConfig.getUntrackedParameter<edm::InputTag>("src_met")),
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
    hPt = fs->make<TH1F>("jet_pt", "het_pt", 100, 0., 200.);
    hEta = fs->make<TH1F>("jet_eta", "jet_eta", 100, -5., 5.);
    hNumberOfSelectedJets = fs->make<TH1F>("NumberOfSelectedJets", "NumberOfSelectedJets", 15, 0., 15.);
    hDeltaPhiJetMet = fs->make<TH1F>("deltaPhiJetMet", "deltaPhiJetMet", 60, 0., 180.); 
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


      // plot deltaPhi(jet,met)
      double deltaPhi = -999;

      edm::Handle<edm::View<reco::MET> > hmet;
      iEvent.getByLabel(fSrc_met, hmet);
      edm::Ptr<reco::MET> met = hmet->ptrAt(0);

      if ( met->et()>  fMetCut) {
	//	  deltaPhi = DeltaPhi::reconstruct(*(iJet), *(fMETSelection.getSelectedMET()));
	  deltaPhi = DeltaPhi::reconstruct(*(iJet), *(met));
	  hDeltaPhiJetMet->Fill(deltaPhi*57.3);
      }


      fSelectedJets.push_back(iJet);
    }

    hNumberOfSelectedJets->Fill(fSelectedJets.size());
    iNHadronicJets = fSelectedJets.size();

    if(cleanPassed < fMin) return false;
    increment(fCleanCutCount);

    if(ptCutPassed < fMin) return false;
    increment(fPtCutCount);

    if(etaCutPassed < fMin) return false;      
    increment(fEtaCutCount);
    return true;
  }
}
