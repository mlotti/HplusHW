#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetDetailHistograms.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "Math/GenVector/VectorUtil.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

std::vector<const reco::GenParticle*> getMothers(const reco::Candidate& p);

namespace HPlus {
  JetDetailHistograms::JetDetailHistograms(HistoWrapper& histoWrapper, TFileDirectory& myDir, std::string prefix, bool enableExtraHistograms) :
    bEnableExtraHistograms(enableExtraHistograms) {
    // Create subdirectory for containting the histograms, but only if there are any histograms to put
    TFileDirectory mySubDir = histoWrapper.mkdir(HistoWrapper::kInformative, myDir, prefix);
    // Create histograms
    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_pt", "jet_pt", 40, 0., 400.);
    hEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_eta", "jet_eta", 50, -2.5, 2.5);
    hPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_phi", "jet_phi", 72, -3.14159, 3.41459);
    hNeutralEmEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_NeutralEmEnergyFraction", "jet_NeutralEmEnergyFraction", 100, 0., 1.);
    hNeutralMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_EmEnergyFraction", "jet_EmEnergyFraction", 100, 0., 1.);
    hNeutralHadronEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_NeutralHadronEnergyFraction", "jet_NeutralHadronEnergyFraction", 100, 0., 1.);
    hNeutralHadronMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hPhotonEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_PhotonEnergyFraction", "jet_PhotonEnergyFraction", 100, 0., 1.);
    hPhotonMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_PhotonMultiplicity", "jet_PhotonMultiplicity", 100, 0., 100.);
    hMuonEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_MuonEnergyFraction", "jet_MuonEnergyFraction", 100, 0., 1.);
    hMuonMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_MuonMultiplicity", "jet_MuonMultiplicity", 100, 0., 100.);
    hChargedHadronEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_ChargedHadronEnergyFraction", "jet_ChargedHadronEnergyFraction", 100, 0., 1.);
    hChargedEmEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_ChargedEmEnergyFraction", "jet_ChargedEmEnergyFraction", 100, 0., 1.);
    hChargedMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_ChargedMultiplicity", "jet_ChargedMultiplicity", 100, 0., 100.);
    hPartonFlavour = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_PartonFlavour", "jet_PartonFlavour", 30, 0., 30.);
    hJECFactor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_JECFactor", "jet_JECFactor", 200, 0., 2.);
    hN60 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_N60", "jet_MultiplicityCarrying60PercentOfEnergy", 100, 0., 100.);
    hTowersArea = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_TowersArea", "jet_TowersArea", 100, 0., 10.);
    hJetCharge = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_charge", "jet_charge", 10, -5., 5.);
    hPtDiffToGenJet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "jet_PtDiffToGenJet", "jet_PtDiffToGenJet", 150, 0., 3.);
    if (bEnableExtraHistograms) {
      hDataDrivenLeptonOverlaps = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "Extra_DataDrivenLeptonOverlaps", "Extra_DataDrivenLeptonOverlaps", 5, 0., 5.);
      if (hDataDrivenLeptonOverlaps->isActive()) {
        hDataDrivenLeptonOverlaps->GetXaxis()->SetBinLabel(1, "No lepton overlap");
        hDataDrivenLeptonOverlaps->GetXaxis()->SetBinLabel(2, "Overlaps non-isol. e");
        hDataDrivenLeptonOverlaps->GetXaxis()->SetBinLabel(3, "Overlaps non-isol. mu");
        hDataDrivenLeptonOverlaps->GetXaxis()->SetBinLabel(4, "Overlaps isol. e");
        hDataDrivenLeptonOverlaps->GetXaxis()->SetBinLabel(5, "Overlaps isol. mu");
      }
      hMCBJetOverlaps = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "Extra_MCOverlapsWithBjet", "Extra_MCOverlapsWithBjet", 5,0.,5.);
      if (hMCBJetOverlaps->isActive()) {
        hMCBJetOverlaps->GetXaxis()->SetBinLabel(1, "No MC b jet or lepton overlap");
        hMCBJetOverlaps->GetXaxis()->SetBinLabel(2, "Overlaps with MC b jet with lepton");
        hMCBJetOverlaps->GetXaxis()->SetBinLabel(3, "Overlaps with MC b jet and lepton");
        hMCBJetOverlaps->GetXaxis()->SetBinLabel(4, "Overlaps with with lepton");
        hMCBJetOverlaps->GetXaxis()->SetBinLabel(5, "Overlaps with lepton from other b jet");
      }
      hMCLeptonOverlaps = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySubDir, "Extra_MCOverlapsWithLepton", "Extra_MCOverlapsWithLepton", 5,0.,5.);
      if (hMCLeptonOverlaps->isActive()) {
        hMCLeptonOverlaps->GetXaxis()->SetBinLabel(1, "No MC lepton overlap");
        hMCLeptonOverlaps->GetXaxis()->SetBinLabel(2, "Overlaps with MC e");
        hMCLeptonOverlaps->GetXaxis()->SetBinLabel(3, "Overlaps with MC mu");
        hMCLeptonOverlaps->GetXaxis()->SetBinLabel(4, "Overlaps with MC e from b jet");
        hMCLeptonOverlaps->GetXaxis()->SetBinLabel(5, "Overlaps with MC mu from b jet");
      }
    }

  }

  JetDetailHistograms::~JetDetailHistograms() { }

  void JetDetailHistograms::fill(const edm::Ptr<pat::Jet>& jet, const bool isRealData) {
    hPt->Fill(jet->pt());
    hEta->Fill(jet->eta());
    hPhi->Fill(jet->phi());
    hNeutralEmEnergyFraction->Fill(jet->neutralEmEnergyFraction());
    hNeutralMultiplicity->Fill(jet->neutralMultiplicity());
    hNeutralHadronEnergyFraction->Fill(jet->neutralHadronEnergyFraction());
    hNeutralHadronMultiplicity->Fill(jet->neutralHadronMultiplicity());
    hPhotonEnergyFraction->Fill(jet->photonEnergyFraction());
    hPhotonMultiplicity->Fill(jet->photonMultiplicity());
    hMuonEnergyFraction->Fill(jet->muonEnergyFraction());
    hMuonMultiplicity->Fill(jet->muonMultiplicity());
    hChargedHadronEnergyFraction->Fill(jet->chargedHadronEnergyFraction());
    hChargedEmEnergyFraction->Fill(jet->chargedEmEnergyFraction());
    hChargedMultiplicity->Fill(jet->chargedMultiplicity());
    //hJECFactor->Fill(jet->jecFactor());
    //hN60->Fill(jet->n60());
    //hTowersArea->Fill(jet->towersArea());
    hJetCharge->Fill(jet->jetCharge());
    if (!isRealData) {
      hPartonFlavour->Fill(jet->partonFlavour());
      if (jet->genJet())
        hPtDiffToGenJet->Fill(jet->pt() / jet->genJet()->pt());
    }
  }

  void JetDetailHistograms::fillLeptonDetails(const edm::Event& iEvent, const edm::Ptr<pat::Jet>& jet, const ElectronSelection::Data& eData, const MuonSelection::Data& muData, const bool isRealData) {
    if (!bEnableExtraHistograms) return;

    // Data-driven values
    bool isOverlappingWithElectron = false;
    for (edm::PtrVector<pat::Electron>::const_iterator it = eData.getNonIsolatedElectrons().begin(); it != eData.getNonIsolatedElectrons().end(); ++it) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(jet->p4(), (*it)->p4());
      if (myDeltaR < 0.4) isOverlappingWithElectron = true;
    }
    bool isOverlappingWithMuon = false;
    for (edm::PtrVector<pat::Muon>::const_iterator it = muData.getNonIsolatedMuons().begin(); it != muData.getNonIsolatedMuons().end(); ++it) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(jet->p4(), (*it)->p4());
      if (myDeltaR < 0.4) isOverlappingWithMuon = true;
    }
    bool isOverlappingWithIsolatedElectron = false;
    for (edm::PtrVector<pat::Electron>::const_iterator it = eData.getSelectedElectronsVeto().begin(); it != eData.getSelectedElectronsVeto().end(); ++it) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(jet->p4(), (*it)->p4());
      if (myDeltaR < 0.4) isOverlappingWithIsolatedElectron = true;
    }
    bool isOverlappingWithIsolatedMuon = false;
    for (edm::PtrVector<pat::Muon>::const_iterator it = muData.getSelectedLooseMuons().begin(); it != muData.getSelectedLooseMuons().end(); ++it) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(jet->p4(), (*it)->p4());
      if (myDeltaR < 0.4) isOverlappingWithIsolatedMuon = true;
    }
    if (isOverlappingWithElectron) {
      hDataDrivenLeptonOverlaps->Fill(1);
    } else if (isOverlappingWithMuon) {
      hDataDrivenLeptonOverlaps->Fill(2);
    } else if (isOverlappingWithIsolatedElectron) {
      hDataDrivenLeptonOverlaps->Fill(3);
    } else if (isOverlappingWithIsolatedMuon) {
      hDataDrivenLeptonOverlaps->Fill(4);
    } else {
      hDataDrivenLeptonOverlaps->Fill(0);
    }
    if (isRealData) return;

    // MC-based values
    edm::Handle <edm::View<reco::GenParticle> > genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Jet matching categories
    bool isOverlappingWithMCbjet = false;
    bool isOverlappingWithMCbjetWithLepton = false;
    bool isOverlappingWithMCbjetAndLepton = false;
    bool isOverlappingWithMCLepton = false;
    bool isOverlappingWithMCLeptonFromOtherBjet = false;
    // Lepton matching categories
    bool isOverlappingWithMCelectron = false;
    bool isOverlappingWithMCmuon = false;
    bool isOverlappingWithMCelectronFromBjet = false;
    bool isOverlappingWithMCmuonFromBjet = false;

    for (size_t i=0; i < genParticles->size(); ++i){
      if ((*genParticles)[i].status() != 1) continue;
      int myPid = std::abs((*genParticles)[i].pdgId());      
      if (myPid == 5) { // is bjet
        double myDeltaR = ROOT::Math::VectorUtil::DeltaR(jet->p4(), (*genParticles)[i].p4());
        if (myDeltaR < 0.4) isOverlappingWithMCbjet = true;
      }
      if (myPid == 11 || myPid == 13) { // is e or mu
        double myDeltaR = ROOT::Math::VectorUtil::DeltaR(jet->p4(), (*genParticles)[i].p4());
        if (myDeltaR > 0.4) continue;
        bool isOffspringFromBjet = false;
        std::vector<const reco::GenParticle*> mothers = getMothers((*genParticles)[i]);
        for (size_t d=0; d<mothers.size(); ++d) {
          const reco::GenParticle dparticle = *mothers[d];
          if (abs(dparticle.pdgId()) == 5) {
            isOffspringFromBjet = true;
          }
        }
        if (myPid == 11) {
          if (isOffspringFromBjet) {
            isOverlappingWithMCelectronFromBjet = true;
          } else {
            isOverlappingWithMCelectron = true;
          }
        } else if (myPid == 13) {
          if (isOffspringFromBjet) {
            isOverlappingWithMCmuonFromBjet = true;
          } else {
            isOverlappingWithMCmuon = true;
          }
        }
      }
    }
    if (isOverlappingWithMCbjet) {
      if (isOverlappingWithMCelectronFromBjet || isOverlappingWithMCmuonFromBjet)
        isOverlappingWithMCbjetAndLepton = true;
      if (isOverlappingWithMCelectron || isOverlappingWithMCmuon)
        isOverlappingWithMCbjetWithLepton = true;
    } else {
      if (isOverlappingWithMCelectron || isOverlappingWithMCmuon)
        isOverlappingWithMCLepton = true;
      if (isOverlappingWithMCelectronFromBjet || isOverlappingWithMCmuonFromBjet)
        isOverlappingWithMCLeptonFromOtherBjet = true;
    }
    // Fill histograms
    if (isOverlappingWithMCbjetWithLepton) {
      hMCBJetOverlaps->Fill(1);
    } else if (isOverlappingWithMCbjetAndLepton) {
      hMCBJetOverlaps->Fill(2);
    } else if (isOverlappingWithMCLepton) {
      hMCBJetOverlaps->Fill(3);
    } else if (isOverlappingWithMCLeptonFromOtherBjet) {
      hMCBJetOverlaps->Fill(4);
    } else {
      hMCBJetOverlaps->Fill(0);
    }
    if (isOverlappingWithMCelectron) {
      hMCLeptonOverlaps->Fill(1);
    } else if (isOverlappingWithMCmuon) {
      hMCLeptonOverlaps->Fill(2);
    } else if (isOverlappingWithMCelectronFromBjet) {
      hMCLeptonOverlaps->Fill(3);
    } else if (isOverlappingWithMCmuonFromBjet) {
      hMCLeptonOverlaps->Fill(4);
    } else {
      hMCLeptonOverlaps->Fill(0);
    }
  }
}
