#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

#include<algorithm>

namespace {
  bool ptGreaterThan(const edm::Ptr<pat::Jet>& a, const edm::Ptr<pat::Jet>& b) {
    return a->pt() > b->pt();
  }
}

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
    fEMfractionCut(iConfig.getUntrackedParameter<double>("EMfractionCut")),
    fMaxDR(iConfig.getUntrackedParameter<double>("cleanTauDR")),
    fMin(iConfig.getUntrackedParameter<uint32_t>("minNumber")),
    fCleanCutCount(eventCounter.addSubCounter("Jet main","Jet cleaning")),
    fPtCutCount(eventCounter.addSubCounter("Jet main","Jet pt cut")),
    fEtaCutCount(eventCounter.addSubCounter("Jet main","Jet eta cut")),
    fEMfraction08CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.8")),
    fEMfraction07CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.7")),
    fEMfractionCutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac ")),
    fAllSubCount(eventCounter.addSubCounter("Jet selection", "all jets")),
    fCleanCutSubCount(eventCounter.addSubCounter("Jet selection", "cleaning")),
    fPtCutSubCount(eventCounter.addSubCounter("Jet selection", "pt cut")),
    fEtaCutSubCount(eventCounter.addSubCounter("Jet selection", "eta cut")),
    fEMfractionCutSubCount(eventCounter.addSubCounter("Jet selection", "EMfraction")),
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
    hjetEMFraction = makeTH<TH1F>(myDir, "jetEMFraction", "jetEMFraction", 400, 0., 1.0);
    hjetMaxEMFraction = makeTH<TH1F>(myDir, "jetMaxEMFraction", "jetMaxEMFraction", 400, 0., 1.0);  
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
    fNotSelectedJets.clear();
    fNotSelectedJets.reserve(jets.size());

    size_t cleanPassed = 0;
    size_t ptCutPassed = 0;
    size_t etaCutPassed = 0;
    double maxEMfraction = 0;
    size_t EMfractionCutPassed = 0;
    
    std::vector<edm::Ptr<pat::Jet> > tmpSelectedJets;
    tmpSelectedJets.reserve(jets.size());

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

    
      if(!(iJet->chargedEmEnergyFraction() < 0.99)) continue;
      increment(fchargedEmEnergyFractionCutSubCount);

   
      if(!(iJet->neutralHadronEnergyFraction() < 0.99)) continue;
      increment(fneutralHadronEnergyFractionCutSubCount);

      if(!(iJet->neutralEmEnergyFraction() < 0.99)) continue;
      increment(fneutralEmEnergyFractionCutSubCount);

    
      if(fabs(iJet->eta()) < 2.4) {
	  if(!(iJet->chargedHadronEnergyFraction() > 0)) continue;
	  increment(fchargedHadronEnergyFractionCutSubCount);
	  if(!(iJet->chargedMultiplicity() > 0)) continue;
	  increment(fchargedMultiplicityCutSubCount);
	}

      double EMfrac = (iJet->chargedEmEnergy() +
                       iJet->neutralEmEnergy())/(
                       iJet->chargedHadronEnergy() +
                       iJet->neutralHadronEnergy() +
                       iJet->chargedEmEnergy() +
                       iJet->neutralEmEnergy());
      hjetEMFraction->Fill(EMfrac, fEventWeight.getWeight());
      if ( EMfrac > maxEMfraction ) maxEMfraction =  EMfrac;

      if (EMfrac > fEMfractionCut) continue;
      ++EMfractionCutPassed;
      increment(fEMfractionCutSubCount);
    
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


      tmpSelectedJets.push_back(iJet);
    }

    // Sort the selected jets in the (corrected) pt
    std::sort(tmpSelectedJets.begin(), tmpSelectedJets.end(), ptGreaterThan);
    fSelectedJets.reserve(tmpSelectedJets.size());
    for(size_t i=0; i<tmpSelectedJets.size(); ++i)
      fSelectedJets.push_back(tmpSelectedJets[i]);

    hNumberOfSelectedJets->Fill(fSelectedJets.size(), fEventWeight.getWeight());
    if (fSelectedJets.size() > 2 ) hjetMaxEMFraction->Fill(maxEMfraction, fEventWeight.getWeight());

    iNHadronicJets = fSelectedJets.size();
    iNHadronicJetsInFwdDir = fNotSelectedJets.size();
    passEvent = true;
    if(cleanPassed < fMin) passEvent = false;
    increment(fCleanCutCount);

    if(ptCutPassed < fMin) passEvent = false;
    if(ptCutPassed > fMin)    increment(fPtCutCount);

    if(etaCutPassed < fMin) passEvent = false;
    if(etaCutPassed > fMin)    increment(fEtaCutCount);

    //    if(maxEMfraction > 0.8 ) passEvent = false;
    if(maxEMfraction < 0.8 )increment(fEMfraction08CutCount);

    //    if(maxEMfraction > 0.7 ) passEvent = false;
    if(maxEMfraction < 0.7 )increment(fEMfraction07CutCount);

    if(EMfractionCutPassed < fMin) passEvent = false;
    if(EMfractionCutPassed > fMin )increment(fEMfractionCutCount);

    return Data(this, passEvent);
  }
}
