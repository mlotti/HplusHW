#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

namespace HPlus {
  JetSelection::Data::Data(const JetSelection *jetSelection, bool passedEvent):
    fJetSelection(jetSelection), fPassedEvent(passedEvent) {}
  JetSelection::Data::~Data() {}
  
  JetSelection::JetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    //    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSrc_met(iConfig.getUntrackedParameter<edm::InputTag>("src_met")),
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fMaxDR(iConfig.getUntrackedParameter<double>("cleanTauDR")),
    fMin(iConfig.getUntrackedParameter<uint32_t>("minNumber")),
    fCleanCutCount(eventCounter.addSubCounter("Jet main","Jet cleaning")),
    fPtCutCount(eventCounter.addSubCounter("Jet main","Jet pt cut")),
    fEtaCutCount(eventCounter.addSubCounter("Jet main","Jet eta cut")),
    fAllSubCount(eventCounter.addSubCounter("Jet selection", "all jets")),
    fCleanCutSubCount(eventCounter.addSubCounter("Jet selection", "cleaning")),
    fPtCutSubCount(eventCounter.addSubCounter("Jet selection", "pt cut")),
    fEtaCutSubCount(eventCounter.addSubCounter("Jet selection", "eta cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    hPt = fs->make<TH1F>("jet_pt", "het_pt", 100, 0., 200.);
    hEta = fs->make<TH1F>("jet_eta", "jet_eta", 100, -5., 5.);
    hNumberOfSelectedJets = fs->make<TH1F>("NumberOfSelectedJets", "NumberOfSelectedJets", 15, 0., 15.);
    hDeltaPhiJetMet = fs->make<TH1F>("deltaPhiJetMet", "deltaPhiJetMet", 60, 0., 180.); 
 }

  JetSelection::~JetSelection() {}

  JetSelection::Data JetSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus) {
    // Reset variables
    iNHadronicJets = -1;
    iNHadronicJetsInFwdDir = -1;
    bool passEvent = false;
  
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fSrc, hjets);

    const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());

    fSelectedJets.clear();
    fSelectedJets.reserve(jets.size());
    fNotSelectedJets.clear();
    fNotSelectedJets.reserve(jets.size());

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

      hPt->Fill(iJet->pt(), fEventWeight.getWeight());
      hEta->Fill(iJet->eta(), fEventWeight.getWeight());

      if(!(iJet->pt() > fPtCut)) continue;
      increment(fPtCutSubCount);
      ++ptCutPassed;

      if(!(std::abs(iJet->eta()) < fEtaCut)){
	fNotSelectedJets.push_back(iJet);
	continue;
      }
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
	  hDeltaPhiJetMet->Fill(deltaPhi*57.3, fEventWeight.getWeight());
      }


      fSelectedJets.push_back(iJet);
    }

    hNumberOfSelectedJets->Fill(fSelectedJets.size(), fEventWeight.getWeight());
    iNHadronicJets = fSelectedJets.size();
    iNHadronicJetsInFwdDir = fNotSelectedJets.size();
    passEvent = true;
    if(cleanPassed < fMin) passEvent = false;
    increment(fCleanCutCount);

    if(ptCutPassed < fMin) passEvent = false;
    increment(fPtCutCount);

    if(etaCutPassed < fMin) passEvent = false;
    increment(fEtaCutCount);

    return Data(this, passEvent);
  }
}
