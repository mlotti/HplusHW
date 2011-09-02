#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

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
    fnumberOfDaughtersCutSubCount(eventCounter.addSubCounter("Jet selection", "numberOfDaughtersCut")),
    fchargedEmEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "chargedEmEnergyFractionCut")),
    fneutralHadronEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "neutralHadronEnergyFractionCut")),
    fneutralEmEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "neutralEmEnergyFractionCut")),
    fchargedHadronEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "chargedHadronEnergyFractionCut")),
    fchargedMultiplicityCutSubCount(eventCounter.addSubCounter("Jet selection", "fchargedMultiplicityCut")),  
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("JetSelection");
    
    hPt = makeTH<TH1F>(myDir, "jet_pt", "het_pt", 400, 0., 400.);
    hPtCentral = makeTH<TH1F>(myDir, "jet_pt_central", "het_pt_central", 100, 0., 200.);
    hEta = makeTH<TH1F>(myDir, "jet_eta", "jet_eta", 400, -5., 5.);
    hPhi = makeTH<TH1F>(myDir, "jet_phi", "jet_phi", 400, -3.2, 3.2);
    hNumberOfSelectedJets = makeTH<TH1F>(myDir, "NumberOfSelectedJets", "NumberOfSelectedJets", 15, 0., 15.);
    hDeltaPhiJetMet = makeTH<TH1F>(myDir, "deltaPhiJetMet", "deltaPhiJetMet", 400, 0., 3.2); 
    hchargedEmEnergyFraction = makeTH<TH1F>(myDir, "chargedEmEnergyFraction", "chargedEmEnergyFraction", 400, 0., 1.0);
    hneutralHadronEnergyFraction = makeTH<TH1F>(myDir, "neutralHadronEnergyFraction", "neutralHadronEnergyFraction", 400, 0., 1.0); 
    hchargedHadronEnergyFraction = makeTH<TH1F>(myDir, "chargedHadronEnergyFraction", "chargedHadronEnergyFraction", 400, 0., 1.0);  
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
      if (fabs(iJet->eta()) < 2.4) hPtCentral->Fill(iJet->pt(), fEventWeight.getWeight());
      hEta->Fill(iJet->eta(), fEventWeight.getWeight());
      hPhi->Fill(iJet->phi(), fEventWeight.getWeight());

      if(!(iJet->pt() > fPtCut)) continue;
      increment(fPtCutSubCount);
      ++ptCutPassed;


      if(!(std::abs(iJet->eta()) < fEtaCut)){
	fNotSelectedJets.push_back(iJet);
	continue;
      }
      increment(fEtaCutSubCount);
      ++etaCutPassed;

      
    // jetID cuts 
      if(!(iJet->numberOfDaughters() > 1)) continue;
      increment(fnumberOfDaughtersCutSubCount);

      hchargedEmEnergyFraction->Fill(iJet->chargedEmEnergyFraction(), fEventWeight.getWeight());
      if(!(iJet->chargedEmEnergyFraction() < 0.99)) continue;
      increment(fchargedEmEnergyFractionCutSubCount);

      hneutralHadronEnergyFraction->Fill(iJet->neutralHadronEnergyFraction(), fEventWeight.getWeight());
      if(!(iJet->neutralHadronEnergyFraction() < 0.99)) continue;
      increment(fneutralHadronEnergyFractionCutSubCount);

      if(!(iJet->neutralEmEnergyFraction() < 0.99)) continue;
      increment(fneutralEmEnergyFractionCutSubCount);

      hchargedHadronEnergyFraction->Fill(iJet->chargedHadronEnergyFraction(), fEventWeight.getWeight());
      if(fabs(iJet->eta()) < 2.4) {
	  if(!(iJet->chargedHadronEnergyFraction() > 0)) continue;
	  increment(fchargedHadronEnergyFractionCutSubCount);
	  if(!(iJet->chargedMultiplicity() > 0)) continue;
	  increment(fchargedMultiplicityCutSubCount);
	}
     
      // plot deltaPhi(jet,met)
      double deltaPhi = -999;

      edm::Handle<edm::View<reco::MET> > hmet;
      iEvent.getByLabel(fSrc_met, hmet);
      edm::Ptr<reco::MET> met = hmet->ptrAt(0);

      if ( met->et()>  fMetCut) {
	//	  deltaPhi = DeltaPhi::reconstruct(*(iJet), *(fMETSelection.getSelectedMET()));
	  deltaPhi = DeltaPhi::reconstruct(*(iJet), *(met));
	  hDeltaPhiJetMet->Fill(deltaPhi*57.3, fEventWeight.getWeight());
	  //	  hDeltaPhiJetMet->Fill(deltaPhi, fEventWeight.getWeight());
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
