#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetDetailHistograms.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

namespace HPlus {
  JetDetailHistograms::JetDetailHistograms(HistoWrapper& histoWrapper, TFileDirectory& myDir, std::string prefix) {
    // Create subdirectory for containting the histograms
    TFileDirectory mySubDir = myDir.mkdir(prefix.c_str());
    // Create histograms
    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_pt", "jet_pt", 40, 0., 400.);
    hEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_eta", "jet_eta", 50, -2.5, 2.5);
    hPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_phi", "jet_phi", 72, -3.14159, 3.41459);
    hNeutralEmEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_NeutralEmEnergyFraction", "jet_NeutralEmEnergyFraction", 100, 0., 1.);
    hNeutralMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_EmEnergyFraction", "jet_EmEnergyFraction", 100, 0., 1.);
    hNeutralHadronEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_NeutralHadronFraction", "jet_NeutralHadronEnergyFraction", 100, 0., 1.);
    hNeutralHadronMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hPhotonEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_PhotonEnergyFraction", "jet_PhotonEnergyFraction", 100, 0., 1.);
    hPhotonMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_PhotonMultiplicity", "jet_PhotonMultiplicity", 100, 0., 100.);
    hMuonEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_MuonEnergyFraction", "jet_MuonEnergyFraction", 100, 0., 1.);
    hMuonMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hChargedHadronEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_ChargedHadronEnergyFraction", "jet_ChargedHadronEnergyFraction", 100, 0., 1.);
    hChargedEmEnergyFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_ChargedEmEnergyFraction", "jet_ChargedEmEnergyFraction", 100, 0., 1.);
    hChargedMultiplicity = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_ChargedMultiplicity", "jet_ChargedMultiplicity", 100, 0., 100.);
    hPartonFlavour = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_PartonFlavour", "jet_PartonFlavour", 30, 0., 30.);
    hJECFactor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_JECFactor", "jet_JECFactor", 100, 0., 10.);
    hN60 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_N60", "jet_MultiplicityCarrying60PercentOfEnergy", 100, 0., 100.);
    hTowersArea = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_TowersArea", "jet_TowersArea", 100, 0., 10.);
    hJetCharge = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_JECFactor", "jet_JECFactor", 10, -5., 5.);
    hPtDiffToGenJet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_PtDiffToGenJet", "jet_PtDiffToGenJet", 100, 0., 10.);
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

}