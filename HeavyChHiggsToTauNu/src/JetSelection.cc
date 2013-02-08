#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "Math/GenVector/VectorUtil.h"
#include <cmath>

#include<algorithm>

namespace {
  bool ptGreaterThan(const edm::Ptr<pat::Jet>& a, const edm::Ptr<pat::Jet>& b) {
    return a->pt() > b->pt();
  }
}

namespace HPlus {
  JetSelection::Data::Data():
    fPassedEvent(false),
    iNHadronicJets(-1),
    iNHadronicJetsInFwdDir(-1),
    fMinDeltaRToOppositeDirectionOfTau(999.),
    bEMFraction08Veto(false),
    bEMFraction07Veto(false),
    fMinEtaOfSelectedJetToGap(999),
    fEtaSpreadOfSelectedJets(999),
    fAverageEtaOfSelectedJets(999),
    fAverageSelectedJetsEtaDistanceToTauEta(999),
    fDeltaPtJetTau(999),
    fDeltaPhiMHTJet1(-1),
    fDeltaPhiMHTJet2(-1),
    fDeltaPhiMHTJet3(-1),
    fDeltaPhiMHTJet4(-1),
    fDeltaPhiMHTTau(-1),
    fReferenceJetToTauDeltaPt(999),
    fReferenceJetToTauPtRatio(999) {}
  JetSelection::Data::~Data() {}
  
  const int JetSelection::Data::getReferenceJetToTauPartonFlavour() const {
    if (fReferenceJetToTau.isNull())
      return -999;
    return std::abs(fReferenceJetToTau->partonFlavour());
  }

  JetSelection::JetSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fEMfractionCut(iConfig.getUntrackedParameter<double>("EMfractionCut")),
    fMaxDR(iConfig.getUntrackedParameter<double>("cleanTauDR")),
    fNumberOfJets(iConfig.getUntrackedParameter<uint32_t>("jetNumber"), iConfig.getUntrackedParameter<std::string>("jetNumberCutDirection")),
    fJetIdMaxNeutralHadronEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMaxNeutralHadronEnergyFraction")),
    fJetIdMaxNeutralEMEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMaxNeutralEMEnergyFraction")),
    fJetIdMinNumberOfDaughters(iConfig.getUntrackedParameter<uint32_t>("jetIdMinNumberOfDaughters")),
    fJetIdMinChargedHadronEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMinChargedHadronEnergyFraction")),
    fJetIdMinChargedMultiplicity(iConfig.getUntrackedParameter<uint32_t>("jetIdMinChargedMultiplicity")),
    fJetIdMaxChargedEMEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMaxChargedEMEnergyFraction")),
    fBetaCut(iConfig.getUntrackedParameter<double>("betaCut"), iConfig.getUntrackedParameter<std::string>("betaCutDirection")),
    fBetaSrc(iConfig.getUntrackedParameter<std::string>("betaCutSource")),
    fApplyVetoForDeadECALCells(iConfig.getUntrackedParameter<bool>("applyVetoForDeadECALCells")),
    fDeadECALCellsVetoDeltaR(iConfig.getUntrackedParameter<double>("deadECALCellsVetoDeltaR")),
    fAllCount(eventCounter.addSubCounter("Jet main","All events")),
    fDeadECALCellVetoCount(eventCounter.addSubCounter("Jet main","Dead ECAL cells veto")),
    fCleanCutCount(eventCounter.addSubCounter("Jet main","Jet cleaning")),
    fJetIdCount(eventCounter.addSubCounter("Jet main", "Jet ID")),
    fBetaCutCount(eventCounter.addSubCounter("Jet main","beta cut")),
    fEMfractionCutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac ")),
    fEtaCutCount(eventCounter.addSubCounter("Jet main","Jet eta cut")),
    fPtCutCount(eventCounter.addSubCounter("Jet main","Jet pt cut")),
    fAllSubCount(eventCounter.addSubCounter("Jet selection", "all jets")),
    fEMfraction08CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.8")),
    fEMfraction07CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.7")),
    fEventKilledByBetaCutCount(eventCounter.addSubCounter("Jet main","Event killed by beta cut")),
    fCleanCutSubCount(eventCounter.addSubCounter("Jet selection", "cleaning")),
    fneutralHadronEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "neutralHadronEnergyFractionCut")),
    fneutralEmEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "neutralEmEnergyFractionCut")),
    fnumberOfDaughtersCutSubCount(eventCounter.addSubCounter("Jet selection", "numberOfDaughtersCut")),
    fchargedHadronEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "chargedHadronEnergyFractionCut")),
    fchargedMultiplicityCutSubCount(eventCounter.addSubCounter("Jet selection", "fchargedMultiplicityCut")),
    fchargedEmEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "chargedEmEnergyFractionCut")),
    fJetIdSubCount(eventCounter.addSubCounter("Jet selection", "Jet ID")),
    fEMfractionCutSubCount(eventCounter.addSubCounter("Jet selection", "EMfraction")),
    fBetaCutSubCount(eventCounter.addSubCounter("Jet selection", "Beta cut")),
    fEtaCutSubCount(eventCounter.addSubCounter("Jet selection", "eta cut")),
    fPtCutSubCount(eventCounter.addSubCounter("Jet selection", "pt cut")),
    fJetToTauReferenceJetNotIdentifiedCount(eventCounter.addSubCounter("Jet selection", "jet->tau ref.jet not identified"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("JetSelection");

    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "jet_pt", "jet_pt", 120, 0., 600.);
    hPtCentral = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_pt_central", "jet_pt_central", 120, 0., 600.);
    hEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "jet_eta", "jet_eta", 100, -5., 5.);
    hPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "jet_phi", "jet_phi", 72, -3.1415926, 3.1415926);
    hNumberOfSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "NumberOfSelectedJets", "NumberOfSelectedJets", 30, 0., 30.);
    hjetEMFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jetEMFraction", "jetEMFraction", 100, 0., 1.0);
    hjetChargedEMFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "chargedJetEMFraction", "chargedJetEMFraction", 100, 0., 1.0);
    hjetMaxEMFraction = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jetMaxEMFraction", "jetMaxEMFraction", 100, 0., 1.0);
    hMinDeltaRToOppositeDirectionOfTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_MinDeltaRToOppositeDirectionOfTau", "jet_MinDeltaRToOppositeDirectionOfTau", 50, 0., 5.);

    hFirstJetPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "firstJet_pt", "firstJet_pt;p_{T} of first jet, GeV/c;Events", 120, 0., 600.);
    hFirstJetEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "firstJet_eta", "firstJet_eta;#eta of first jet;Events", 100, -5., 5.); 
    hFirstJetPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "firstJet_phi", "firstJet_phi;#phi of first jet;Events", 72, -3.14159, 3.14159); 
    hSecondJetPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "secondJet_pt", "secondJet_pt;p_{T} of second jet, GeV/c;Events", 120, 0., 600.);
    hSecondJetEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "secondJet_eta", "secondJet_eta;#eta of second jet;Events", 100, -5., 5.); 
    hSecondJetPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "secondJet_phi", "secondJet_phi;#phi of second jet;Events", 72, -3.14159, 3.14159); 
    hThirdJetPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "thirdJet_pt", "thirdJet_pt;p_{T} of third jet, GeV/c;Events", 120, 0., 600.);
    hThirdJetEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "thirdJet_eta", "thirdJet_eta;#eta of third jet;Events", 100, -5., 5.); 
    hThirdJetPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "thirdJet_phi", "thirdJet_phi;#phi of third jet;Events", 72, -3.14159, 3.14159); 
    hFourthJetPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fourthJet_pt", "fourthJet_pt;p_{T} of fourth jet, GeV/c;Events", 120, 0., 600.);
    hFourthJetEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fourthJet_eta", "fourthJet_eta;#eta of fourth jet;Events", 100, -5., 5.); 
    hFourthJetPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fourthJet_phi", "fourthJet_phi;#phi of fourth jet;Events", 72, -3.14159, 3.14159); 
    hMinEtaOfSelectedJetToGap = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "minEtaOfSelectedJetToGap", "minEtaOfSelectedJetToGap;abs(jet #eta - 1.5);Events", 60, 0, 3.0);

    // Histograms for PU analysis
    hBetaGenuine = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "betaGenuine", "betaGenuine;#beta variable, PV jets;Events", 100, 0., 1.);
    hBetaStarGenuine = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "betaStarGenuine", "betaStarGenuine;#beta* variable, PV jets;Events", 100, 0., 1.);
    hMeanDRgenuine = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "meanDRGenuine", "meanDRGenuine;Mean #DeltaR, PV jets;Events", 100, 0., 4.);
    hBetaFake = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "betaPU", "betaPU;#beta variable, PU jets;Events", 100, 0., 1.);
    hBetaStarFake = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "betaStarPU", "betaStarPU;#beta* variable, PU jets;Events", 100, 0., 1.);
    hMeanDRfake = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "meanDRPU", "meanDRPU;Mean #DeltaR, PU jets;Events", 100, 0., 4.);
    hBetaVsPUgenuine = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "betaVsPUGenuine", "betaVSPUGenuine;#beta variable, PV jets;Number of vertices", 100, 0., 1., 50, 0., 50.);
    hBetaStarVsPUgenuine = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "betaVsPUStarGenuine", "betaStarVsPUGenuine;#beta* variable, PV jets;Events", 100, 0., 1., 50, 0., 50.);
    hMeanDRVsPUgenuine = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "meanDRVsPUGenuine", "meanDRVsPUGenuine;Mean #DeltaR, PV jets;Events", 100, 0., 4., 50, 0., 50.);
    hBetaVsPUfake = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "betaVsPUFake", "betaVsPUFake;#beta variable, PU jets;Events", 100, 0., 1., 50, 0., 50.);
    hBetaStarVsPUfake = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "betaStarVsPUFake", "betaStarVsPUFake;#beta* variable, PU jets;Events", 100, 0., 1., 50, 0., 50.);
    hMeanDRVsPUfake = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "meanDRVsPUFake", "meanDRVsPUFake;Mean #DeltaR, PU jets;Events", 100, 0., 4., 50, 0., 50.);

    // Histograms for excluded jets (i.e. matching in DeltaR to tau jet)
    TFileDirectory myExcludedJetsDir = myDir.mkdir("ExcludedJets");
    hPtExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_pt", "jet_pt", 40, 0., 400.);
    hEtaExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_eta", "jet_eta", 50, -2.5, 2.5);
    hPhiExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_phi", "jet_phi", 72, -3.14159, 3.41459);
    hNeutralEmEnergyFractionExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_NeutralEmEnergyFraction", "jet_NeutralEmEnergyFraction", 100, 0., 1.);
    hNeutralMultiplicityExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_EmEnergyFraction", "jet_EmEnergyFraction", 100, 0., 1.);
    hNeutralHadronEnergyFractionExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_NeutralHadronFraction", "jet_NeutralHadronEnergyFraction", 100, 0., 1.);
    hNeutralHadronMultiplicityExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hPhotonEnergyFractionExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_PhotonEnergyFraction", "jet_PhotonEnergyFraction", 100, 0., 1.);
    hPhotonMultiplicityExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_PhotonMultiplicity", "jet_PhotonMultiplicity", 100, 0., 100.);
    hMuonEnergyFractionExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_MuonEnergyFraction", "jet_MuonEnergyFraction", 100, 0., 1.);
    hMuonMultiplicityExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hChargedHadronEnergyFractionExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_ChargedHadronEnergyFraction", "jet_ChargedHadronEnergyFraction", 100, 0., 1.);
    hChargedEmEnergyFractionExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_ChargedEmEnergyFraction", "jet_ChargedEmEnergyFraction", 100, 0., 1.);
    hChargedMultiplicityExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_ChargedMultiplicity", "jet_ChargedMultiplicity", 100, 0., 100.);
    hPartonFlavourExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_PartonFlavour", "jet_PartonFlavour", 30, 0., 30.);
    hJECFactorExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_JECFactor", "jet_JECFactor", 100, 0., 10.);
    hN60ExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_N60", "jet_MultiplicityCarrying60PercentOfEnergy", 100, 0., 100.);
    hTowersAreaExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_TowersArea", "jet_TowersArea", 100, 0., 10.);
    hJetChargeExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_JECFactor", "jet_JECFactor", 10, -5., 5.);
    hPtDiffToGenJetExcludedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myExcludedJetsDir, "jet_PtDiffToGenJet", "jet_PtDiffToGenJet", 100, 0., 10.);

    // Histograms for selected jets
    TFileDirectory mySelectedJetsDir = myDir.mkdir("SelectedJets");
    hPtSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_pt", "jet_pt", 40, 0., 400.);
    hEtaSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_eta", "jet_eta", 50, -2.5, 2.5);
    hPhiSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_phi", "jet_phi", 72, -3.14159, 3.41459);
    hNeutralEmEnergyFractionSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_NeutralEmEnergyFraction", "jet_NeutralEmEnergyFraction", 100, 0., 1.);
    hNeutralMultiplicitySelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_EmEnergyFraction", "jet_EmEnergyFraction", 100, 0., 1.);
    hNeutralHadronEnergyFractionSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_NeutralHadronFraction", "jet_NeutralHadronEnergyFraction", 100, 0., 1.);
    hNeutralHadronMultiplicitySelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hPhotonEnergyFractionSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_PhotonEnergyFraction", "jet_PhotonEnergyFraction", 100, 0., 1.);
    hPhotonMultiplicitySelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_PhotonMultiplicity", "jet_PhotonMultiplicity", 100, 0., 100.);
    hMuonEnergyFractionSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_MuonEnergyFraction", "jet_MuonEnergyFraction", 100, 0., 1.);
    hMuonMultiplicitySelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hChargedHadronEnergyFractionSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_ChargedHadronEnergyFraction", "jet_ChargedHadronEnergyFraction", 100, 0., 1.);
    hChargedEmEnergyFractionSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_ChargedEmEnergyFraction", "jet_ChargedEmEnergyFraction", 100, 0., 1.);
    hChargedMultiplicitySelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_ChargedMultiplicity", "jet_ChargedMultiplicity", 100, 0., 100.);
    hPartonFlavourSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_PartonFlavour", "jet_PartonFlavour", 30, 0., 30.);
    hJECFactorSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_JECFactor", "jet_JECFactor", 100, 0., 10.);
    hN60SelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_N60", "jet_MultiplicityCarrying60PercentOfEnergy", 100, 0., 100.);
    hTowersAreaSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_TowersArea", "jet_TowersArea", 100, 0., 10.);
    hJetChargeSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_JECFactor", "jet_JECFactor", 10, -5., 5.);
    hPtDiffToGenJetSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, mySelectedJetsDir, "jet_PtDiffToGenJet", "jet_PtDiffToGenJet", 100, 0., 10.);
    hDeltaPtJetTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, mySelectedJetsDir, "deltaPtTauJet", "deltaPtTauJet ", 200, -100., 100.);
    hDeltaRJetTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, mySelectedJetsDir, "deltaRTauJet", "deltaRTauJet ", 120, 0., 6.);

    // MHT related
    TFileDirectory myMHTDir = myDir.mkdir("MHT");
    hMHT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "MHT", "MHT;MHT, GeV;N_{events}", 100, 0., 500.);
    hMHTphi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "MHTphi", "MHTphi;MHT #phi;N_{events}", 72, -3.14159265, -3.14159265);
    hDeltaPhiMHTJet1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet1", "DeltaPhiMHTJet1;#Delta#phi(MHT,jet1), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTJet2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet2", "DeltaPhiMHTJet2;#Delta#phi(MHT,jet2), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTJet3 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet3", "DeltaPhiMHTJet3;#Delta#phi(MHT,jet3), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTJet4 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet4", "DeltaPhiMHTJet4;#Delta#phi(MHT,jet4), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTTau", "DeltaPhiMHTTau;#Delta#phi(MHT,tau), ^{o};N_{events}", 36, 0., 180.);

    // Reference tau related
    TFileDirectory myRefDir = myDir.mkdir("ReferenceJetToTau");
    hReferenceJetToTauMatchingDeltaR = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "MatchingDeltaR", "MatchingDeltaR;Matching #DeltaR;N_{events}", 30, 0., 1.);
    hReferenceJetToTauPartonFlavour = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "PartonFlavour", "ReferenceJetToTauPartonFlavour;ReferenceJetToTauPartonFlavour;N_{events}", 30, 0., 30.);
    hReferenceJetToTauDeltaPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "DeltaPt", "ReferenceJetToTauDeltaPt;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);
    hReferenceJetToTauPtRatio = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "PtRatio", "ReferenceJetToTauPtRatio;#tau p_{T} / ref.jet p_{T}, GeV/c;N_{events}", 120, 0., 1.2);

 }

  JetSelection::~JetSelection() {}

  JetSelection::Data JetSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr< reco::Candidate >& tau, int nVertices) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, tau, nVertices);
  }

  JetSelection::Data JetSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr< reco::Candidate >& tau, int nVertices) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, tau, nVertices);
  }

  JetSelection::Data JetSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr< reco::Candidate >& tau, int nVertices) {
    Data output;

    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fSrc, hjets);

    const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());

    size_t cleanPassed = 0;
    size_t jetIdPassed = 0;
    size_t killedByBetaCut = 0;
    size_t betaCutPassed = 0;
    size_t ptCutPassed = 0;
    size_t etaCutPassed = 0;
    double maxEMfraction = 0;
    size_t EMfractionCutPassed = 0;

    std::vector<edm::Ptr<pat::Jet> > tmpSelectedJets;
    tmpSelectedJets.reserve(jets.size());

    increment(fAllCount);
    // Check if any of the jets hits a dead ECAL cell
    if (fApplyVetoForDeadECALCells) {
      for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
        // Ignore jets too close to tau
	if(!(ROOT::Math::VectorUtil::DeltaR((tau)->p4(), (*iter)->p4()) > fMaxDR)) continue;
        if ((*iter)->pt() < 20.0) continue;
        bool myStatus = fDeadECALCells.ObjectHitsDeadECALCell(*iter, fDeadECALCellsVetoDeltaR);
        if (!myStatus) {
          output.fPassedEvent = false;
          return output;
        }
      }
    }
    increment(fDeadECALCellVetoCount);

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      output.fAllJets.push_back(iJet);
      increment(fAllSubCount);

      // jetID cuts 
      // This is loose jet ID. Even though the EM fraction can be
      // tightened later, we have here baseline cuts.
      if(!(iJet->numberOfDaughters() > fJetIdMinNumberOfDaughters)) continue;
      increment(fnumberOfDaughtersCutSubCount);

      if(!(iJet->chargedEmEnergyFraction() < fJetIdMaxChargedEMEnergyFraction)) continue;
      increment(fchargedEmEnergyFractionCutSubCount);

      if(!(iJet->neutralHadronEnergyFraction() < fJetIdMaxNeutralHadronEnergyFraction)) continue;
      increment(fneutralHadronEnergyFractionCutSubCount);

      if(!(iJet->neutralEmEnergyFraction() < fJetIdMaxNeutralEMEnergyFraction)) continue;
      increment(fneutralEmEnergyFractionCutSubCount);

      if(fabs(iJet->eta()) < 2.4) {
        if(!(iJet->chargedHadronEnergyFraction() > fJetIdMinChargedHadronEnergyFraction)) continue;
        increment(fchargedHadronEnergyFractionCutSubCount);
        if(!(static_cast<uint32_t>(iJet->chargedMultiplicity()) > fJetIdMinChargedMultiplicity)) continue;
        increment(fchargedMultiplicityCutSubCount);
      }
      increment(fJetIdSubCount);
      ++jetIdPassed;
      // jetID cuts end

      // The following methods return the energy fractions w.r.t. raw jet energy (as they should be)
      double EMfrac = iJet->chargedEmEnergyFraction() + iJet->neutralEmEnergyFraction();
      double chargedEMfrac = iJet->chargedEmEnergyFraction();
      hjetEMFraction->Fill(EMfrac);
      hjetChargedEMFraction->Fill(chargedEMfrac);
      if ( EMfrac > maxEMfraction ) maxEMfraction =  EMfrac;

      if (EMfrac > fEMfractionCut) continue;
      ++EMfractionCutPassed;
      increment(fEMfractionCutSubCount);

      // against PU cut (beta or betaStar)
      if (!passBetaCut(iJet, iEvent, nVertices)) {
        // Count how many jets, that otherwise would have been selected, are killed by beta cut
        if (std::abs(iJet->eta()) < fEtaCut && iJet->pt() > fPtCut)
          ++killedByBetaCut;
        continue;
      }
      increment(fBetaCutSubCount);
      ++betaCutPassed;
      hPt->Fill(iJet->pt());
      hEta->Fill(iJet->eta());
      hPhi->Fill(iJet->phi());

      // Jet identification and beta cuts done, store jet to list of all jets
      output.fAllIdentifiedJets.push_back(iJet);

      // remove jets too close to tau jet
      hDeltaRJetTau->Fill(ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJet->p4()));
      bool match = false;
      if(!(ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJet->p4()) > fMaxDR)) {
        match = true;
        output.fDeltaPtJetTau = iJet->pt()- (tau)->pt();
        hDeltaPtJetTau->Fill(iJet->pt()- (tau)->pt());
      }
      if(match) {
        if (iJet->pt() > fPtCut && (std::abs(iJet->eta()) < fEtaCut)) {
          plotExcludedJetHistograms(iJet, iEvent.isRealData());
        }
        continue;
      }
      increment(fCleanCutSubCount);
      ++cleanPassed;
      // eta cut
      if(!(std::abs(iJet->eta()) < fEtaCut)){
        output.fNotSelectedJets.push_back(*iter);
        continue;
      }
      increment(fEtaCutSubCount);
      ++etaCutPassed;

      hPtCentral->Fill(iJet->pt());

      // pt cut
      if (iJet->pt() > 20.0)
        output.fSelectedJetsPt20.push_back(iJet);

      if(!(iJet->pt() > fPtCut)) continue;
      increment(fPtCutSubCount);
      ++ptCutPassed;

      // Fill histograms for selected jets
      plotSelectedJetHistograms(iJet, iEvent.isRealData());

      // Min DeltaR reversed to tau
      math::XYZTLorentzVectorD myReversedTau = -tau->p4();
      //     math::XYZTLorentzVectorD myReversedTau = -tau.p4();
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(myReversedTau, iJet->p4());
      if (myDeltaR < output.fMinDeltaRToOppositeDirectionOfTau)
        output.fMinDeltaRToOppositeDirectionOfTau = myDeltaR;

      tmpSelectedJets.push_back(iJet);
    }

    // Sort the selected jets in the (corrected) pt
    std::sort(tmpSelectedJets.begin(), tmpSelectedJets.end(), ptGreaterThan);
    for(size_t i=0; i<tmpSelectedJets.size(); ++i)
      output.fSelectedJets.push_back(tmpSelectedJets[i]);

    hNumberOfSelectedJets->Fill(output.fSelectedJets.size());
    if (output.fSelectedJets.size() > 2 ) hjetMaxEMFraction->Fill(maxEMfraction);
    output.iNHadronicJets = output.fSelectedJets.size();
    output.iNHadronicJetsInFwdDir = output.fNotSelectedJets.size();

    output.fPassedEvent = fNumberOfJets.passedCut(output.fSelectedJets.size());

    if (fNumberOfJets.passedCut(output.fSelectedJets.size()+killedByBetaCut)) {
      increment(fEventKilledByBetaCutCount);
    }

    if (fNumberOfJets.passedCut(cleanPassed))
      increment(fCleanCutCount);

	  //    if(maxEMfraction < fEMfractionCut+ 0.1 )increment(fEMfraction08CutCount);
    //    if(maxEMfraction < fEMfractionCut )increment(fEMfraction07CutCount);

    // Set veto flags for event with high EM fraction of a selected jet
    if (fNumberOfJets.passedCut(jetIdPassed))
      increment(fJetIdCount);

    if (fNumberOfJets.passedCut(betaCutPassed))
      increment(fBetaCutCount);

    if(fNumberOfJets.passedCut(EMfractionCutPassed))
      increment(fEMfractionCutCount);

    if (fNumberOfJets.passedCut(ptCutPassed))
      increment(fPtCutCount);

    if (fNumberOfJets.passedCut(etaCutPassed))
      increment(fEtaCutCount);

    if (output.fPassedEvent && maxEMfraction >= 0.8 ) {
      increment(fEMfraction08CutCount);
      output.bEMFraction08Veto = true;
    }

    if (output.fPassedEvent && maxEMfraction < 0.7 ) {
      increment(fEMfraction07CutCount);
      output.bEMFraction07Veto = true;
    }


    // Plot pt, eta, and phi of jets if jet selection has been passed
    if (output.fPassedEvent && output.fSelectedJets.size() >= 3) {
      hFirstJetPt->Fill(output.fSelectedJets[0]->pt());
      hFirstJetEta->Fill(output.fSelectedJets[0]->eta());
      hFirstJetPhi->Fill(output.fSelectedJets[0]->phi());
      hSecondJetPt->Fill(output.fSelectedJets[1]->pt());
      hSecondJetEta->Fill(output.fSelectedJets[1]->eta());
      hSecondJetPhi->Fill(output.fSelectedJets[1]->phi());
      hThirdJetPt->Fill(output.fSelectedJets[2]->pt());
      hThirdJetEta->Fill(output.fSelectedJets[2]->eta());
      hThirdJetPhi->Fill(output.fSelectedJets[2]->phi());
      if (output.fSelectedJets.size() >= 4) {
        hFourthJetPt->Fill(output.fSelectedJets[3]->pt());
        hFourthJetEta->Fill(output.fSelectedJets[3]->eta());
        hFourthJetPhi->Fill(output.fSelectedJets[3]->phi());
      }
    }
    hMinDeltaRToOppositeDirectionOfTau->Fill(output.fMinDeltaRToOppositeDirectionOfTau);

    // Calculate minimum distance in eta of a selected jet and the gap between barrel and endcap
    double myMinEta = 999.0;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = output.fSelectedJets.begin(); iter != output.fSelectedJets.end(); ++iter) {
      double myValue = std::abs(std::abs((*iter)->eta()) - 1.5);
      if (myValue < myMinEta)
        myMinEta = myValue;
    }
    output.fMinEtaOfSelectedJetToGap = myMinEta;
    hMinEtaOfSelectedJetToGap->Fill(output.fMinEtaOfSelectedJetToGap);
    // Calculate the eta range over which the selected jets are spanned; and the average eta of the jets
    myMinEta = 999.0;
    double myMaxEta = -999.0;
    LorentzVector myMegaJet;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = output.fSelectedJets.begin(); iter != output.fSelectedJets.end(); ++iter) {
      if ((*iter)->eta() > myMaxEta)
        myMaxEta = (*iter)->eta();
      if ((*iter)->eta() < myMinEta)
        myMinEta = (*iter)->eta();
      myMegaJet += (*iter)->p4();
    }
    output.fEtaSpreadOfSelectedJets = myMaxEta - myMinEta;
    if (myMegaJet.pz() > 0.0) {
      output.fAverageEtaOfSelectedJets = myMegaJet.eta();
      output.fAverageSelectedJetsEtaDistanceToTauEta = std::abs(myMegaJet.eta() - tau->eta());
    }

    // Analyze reference jet of selected tau
    obtainReferenceJetToTau(output.fAllJets, tau, output);

    // Calculate MHT on jets
    calculateMHT(output, tau);

    // Everything has been done now return
    return output;
  }

  bool JetSelection::passBetaCut(const edm::Ptr<pat::Jet>& jet, const edm::Event& iEvent, int nVertices) {
    double myBeta = jet->userFloat("Beta");
    //double myBetaMax = jet->userFloat("BetaMax");
    double myBetaStar = jet->userFloat("BetaStar");
    double myMeanDR = jet->userFloat("DRMean");

    //bool myIsPVJetStatusByLdgTrack = (jet->userInt("LdgTrackBelongsToSelectedPV") == 1);
    // Do MC matching of jet to a quark or gluon
    //double minDeltaR = 99999;
    bool myIsPVJetStatusByMCMatching = false;
    if (!iEvent.isRealData()) {
      edm::Handle <reco::GenParticleCollection> genParticles;
      iEvent.getByLabel("genParticles", genParticles);
      for (size_t i=0; i < genParticles->size(); ++i) {
        const reco::Candidate & p = (*genParticles)[i];
        if ((std::abs(p.pdgId()) >= 1 && std::abs(p.pdgId()) <= 5) || std::abs(p.pdgId()) == 21) {
          // Particle is a quark (not a top quark) or a gluon
          if (p.pt() > 15) {
            // Quark or gluon momentum is at least 15 GeV
            if (reco::deltaR(p, *jet) < 0.3) {
              myIsPVJetStatusByMCMatching = true;
            }
          }
        }
      }
    }
    // Fill histograms after eta and pt cuts
    if (std::abs(jet->eta()) < fEtaCut && jet->pt() > fPtCut) {
      if (myIsPVJetStatusByMCMatching) {
        hBetaGenuine->Fill(myBeta);
        hBetaStarGenuine->Fill(myBetaStar);
        hMeanDRgenuine->Fill(myMeanDR);
        hBetaVsPUgenuine->Fill(myBeta, nVertices);
        hBetaStarVsPUgenuine->Fill(myBetaStar, nVertices);
        hMeanDRVsPUgenuine->Fill(myMeanDR, nVertices);
      } else {
        hBetaFake->Fill(myBeta);
        hBetaStarFake->Fill(myBetaStar);
        hMeanDRfake->Fill(myMeanDR);
        hBetaVsPUfake->Fill(myBeta, nVertices);
        hBetaStarVsPUfake->Fill(myBetaStar, nVertices);
        hMeanDRVsPUfake->Fill(myMeanDR, nVertices);
      }
    }
    return fBetaCut.passedCut(jet->userFloat(fBetaSrc));
  }

  void JetSelection::obtainReferenceJetToTau(const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::Candidate>& tau, JetSelection::Data& output) {
    double myMinDeltaR = 999.;
    for (edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      double myDeltaR = reco::deltaR(*tau, **iter);
      if (myDeltaR < myMinDeltaR) {
        myMinDeltaR = myDeltaR;
        if (myDeltaR < 0.1) {
          output.fReferenceJetToTau = *iter;
        }
      }
    }
    hReferenceJetToTauMatchingDeltaR->Fill(myMinDeltaR);
    if (output.fReferenceJetToTau.isNonnull()) {
      hReferenceJetToTauPartonFlavour->Fill(output.getReferenceJetToTauPartonFlavour());
      output.fReferenceJetToTauDeltaPt = tau->pt() - output.fReferenceJetToTau->pt();
      hReferenceJetToTauDeltaPt->Fill(output.fReferenceJetToTauDeltaPt);
      output.fReferenceJetToTauPtRatio = tau->pt() / output.fReferenceJetToTau->pt();
      hReferenceJetToTauPtRatio->Fill(output.fReferenceJetToTauPtRatio);
    } else {
      increment(fJetToTauReferenceJetNotIdentifiedCount);
    }
  }

  void JetSelection::calculateMHT(JetSelection::Data& output, const edm::Ptr<reco::Candidate>& tau) {
    output.fMHT.SetXYZT(0., 0., 0., 0.);
    for (edm::PtrVector<pat::Jet>::const_iterator iter = output.fAllIdentifiedJets.begin(); iter != output.fAllIdentifiedJets.end(); ++iter) {
      if ((*iter)->pt() > fPtCut && (std::abs((*iter)->eta()) < fEtaCut)) {
        output.fMHT -= (*iter)->p4();
      }
    }
    hMHT->Fill(output.fMHT.pt());
    hMHTphi->Fill(output.fMHT.phi());
    // Calculate angles between MHT and the jets
    for (size_t i = 0; i < output.fSelectedJets.size(); ++i) {
      double myDeltaPhi = reco::deltaPhi(output.fMHT, *(output.fSelectedJets[i])) * 57.3;
      if (i == 0) {
        output.fDeltaPhiMHTJet1 = myDeltaPhi;
        hDeltaPhiMHTJet1->Fill(myDeltaPhi);
      } else if (i == 1) {
        output.fDeltaPhiMHTJet2 = myDeltaPhi;
        hDeltaPhiMHTJet2->Fill(myDeltaPhi);
      } else if (i == 2) {
        output.fDeltaPhiMHTJet3 = myDeltaPhi;
        hDeltaPhiMHTJet3->Fill(myDeltaPhi);
      } else if (i == 3) {
        output.fDeltaPhiMHTJet4 = myDeltaPhi;
        hDeltaPhiMHTJet4->Fill(myDeltaPhi);
      }
    }
    output.fDeltaPhiMHTTau = reco::deltaPhi(output.fMHT, *tau) * 57.3;
    hDeltaPhiMHTTau->Fill(output.fDeltaPhiMHTTau);
  }

  void JetSelection::plotSelectedJetHistograms(const edm::Ptr<pat::Jet>& jet, const bool isRealData) {
    hPtSelectedJets->Fill(jet->pt());
    hEtaSelectedJets->Fill(jet->eta());
    hPhiSelectedJets->Fill(jet->phi());
    hNeutralEmEnergyFractionSelectedJets->Fill(jet->neutralEmEnergyFraction());
    hNeutralMultiplicitySelectedJets->Fill(jet->neutralMultiplicity());
    hNeutralHadronEnergyFractionSelectedJets->Fill(jet->neutralHadronEnergyFraction());
    hNeutralHadronMultiplicitySelectedJets->Fill(jet->neutralHadronMultiplicity());
    hPhotonEnergyFractionSelectedJets->Fill(jet->photonEnergyFraction());
    hPhotonMultiplicitySelectedJets->Fill(jet->photonMultiplicity());
    hMuonEnergyFractionSelectedJets->Fill(jet->muonEnergyFraction());
    hMuonMultiplicitySelectedJets->Fill(jet->muonMultiplicity());
    hChargedHadronEnergyFractionSelectedJets->Fill(jet->chargedHadronEnergyFraction());
    hChargedEmEnergyFractionSelectedJets->Fill(jet->chargedEmEnergyFraction());
    hChargedMultiplicitySelectedJets->Fill(jet->chargedMultiplicity());
    //hJECFactorSelectedJets->Fill(jet->jecFactor());
    //hN60SelectedJets->Fill(jet->n60());
    //hTowersAreaSelectedJets->Fill(jet->towersArea());
    hJetChargeSelectedJets->Fill(jet->jetCharge());
    if (!isRealData) {
      hPartonFlavourSelectedJets->Fill(jet->partonFlavour());
      if (jet->genJet())
        hPtDiffToGenJetSelectedJets->Fill(jet->pt() / jet->genJet()->pt());
      else
        hPtDiffToGenJetSelectedJets->Fill(0.);
    }
  }

  void JetSelection::plotExcludedJetHistograms(const edm::Ptr<pat::Jet>& jet, const bool isRealData) {
    // Fill histograms for excluded jets
    hPtExcludedJets->Fill(jet->pt());
    hEtaExcludedJets->Fill(jet->eta());
    hPhiExcludedJets->Fill(jet->phi());
    hNeutralEmEnergyFractionExcludedJets->Fill(jet->neutralEmEnergyFraction());
    hNeutralMultiplicityExcludedJets->Fill(jet->neutralMultiplicity());
    hNeutralHadronEnergyFractionExcludedJets->Fill(jet->neutralHadronEnergyFraction());
    hNeutralHadronMultiplicityExcludedJets->Fill(jet->neutralHadronMultiplicity());
    hPhotonEnergyFractionExcludedJets->Fill(jet->photonEnergyFraction());
    hPhotonMultiplicityExcludedJets->Fill(jet->photonMultiplicity());
    hMuonEnergyFractionExcludedJets->Fill(jet->muonEnergyFraction());
    hMuonMultiplicityExcludedJets->Fill(jet->muonMultiplicity());
    hChargedHadronEnergyFractionExcludedJets->Fill(jet->chargedHadronEnergyFraction());
    hChargedEmEnergyFractionExcludedJets->Fill(jet->chargedEmEnergyFraction());
    hChargedMultiplicityExcludedJets->Fill(jet->chargedMultiplicity());
    //hJECFactorExcludedJets->Fill(jet->jecFactor());
    //hN60ExcludedJets->Fill(jet->n60());
    //hTowersAreaExcludedJets->Fill(jet->towersArea());
    hJetChargeExcludedJets->Fill(jet->jetCharge());
    if (!isRealData) {
      hPartonFlavourExcludedJets->Fill(jet->partonFlavour());
      if (jet->genJet())
        hPtDiffToGenJetExcludedJets->Fill(jet->pt() / jet->genJet()->pt());
      else
        hPtDiffToGenJetExcludedJets->Fill(0.);
    }
  }

}
