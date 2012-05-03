#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"
#include "TH2F.h"
#include <cmath>

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
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fEMfractionCut(iConfig.getUntrackedParameter<double>("EMfractionCut")),
    fMaxDR(iConfig.getUntrackedParameter<double>("cleanTauDR")),
    fMinNumberOfJets(iConfig.getUntrackedParameter<uint32_t>("minNumber")),
    fJetIdMaxNeutralHadronEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMaxNeutralHadronEnergyFraction")),
    fJetIdMaxNeutralEMEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMaxNeutralEMEnergyFraction")),
    fJetIdMinNumberOfDaughters(iConfig.getUntrackedParameter<uint32_t>("jetIdMinNumberOfDaughters")),
    fJetIdMinChargedHadronEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMinChargedHadronEnergyFraction")),
    fJetIdMinChargedMultiplicity(iConfig.getUntrackedParameter<uint32_t>("jetIdMinChargedMultiplicity")),
    fJetIdMaxChargedEMEnergyFraction(iConfig.getUntrackedParameter<double>("jetIdMaxChargedEMEnergyFraction")),
    fBetaCut(iConfig.getUntrackedParameter<double>("betaCut")),
    fCleanCutCount(eventCounter.addSubCounter("Jet main","Jet cleaning")),
    fJetIdCount(eventCounter.addSubCounter("Jet main", "Jet ID")),
    fEMfractionCutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac ")),
    fEtaCutCount(eventCounter.addSubCounter("Jet main","Jet eta cut")),
    fPtCutCount(eventCounter.addSubCounter("Jet main","Jet pt cut")),
    fAllSubCount(eventCounter.addSubCounter("Jet selection", "all jets")),
    fEMfraction08CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.8")),
    fEMfraction07CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.7")),
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

    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("JetSelection");
    
    hPt = makeTH<TH1F>(myDir, "jet_pt", "het_pt", 300, 0., 600.);
    hPtCentral = makeTH<TH1F>(myDir, "jet_pt_central", "jet_pt_central", 300, 0., 600.);
    hEta = makeTH<TH1F>(myDir, "jet_eta", "jet_eta", 250, -5., 5.);
    hPhi = makeTH<TH1F>(myDir, "jet_phi", "jet_phi", 320, -3.2, 3.2);
    hNumberOfSelectedJets = makeTH<TH1F>(myDir, "NumberOfSelectedJets", "NumberOfSelectedJets", 15, 0., 15.);
    hjetEMFraction = makeTH<TH1F>(myDir, "jetEMFraction", "jetEMFraction", 400, 0., 1.0);
    hjetChargedEMFraction = makeTH<TH1F>(myDir, "chargedJetEMFraction", "chargedJetEMFraction", 400, 0., 1.0);
    hjetMaxEMFraction = makeTH<TH1F>(myDir, "jetMaxEMFraction", "jetMaxEMFraction", 400, 0., 1.0);  
    hMinDeltaRToOppositeDirectionOfTau = makeTH<TH1F>(myDir, "jet_MinDeltaRToOppositeDirectionOfTau", "jet_MinDeltaRToOppositeDirectionOfTau", 50, 0., 5.);

    hFirstJetPt = makeTH<TH1F>(myDir, "firstJet_pt", "firstJet_pt;p_{T} of first jet, GeV/c;Events", 300, 0., 600.);
    hFirstJetEta = makeTH<TH1F>(myDir, "firstJet_eta", "firstJet_eta;#eta of first jet;Events", 250, -5., 5.); 
    hFirstJetPhi = makeTH<TH1F>(myDir, "firstJet_phi", "firstJet_phi;#phi of first jet;Events", 72, -3.14159, 3.14159); 
    hSecondJetPt = makeTH<TH1F>(myDir, "secondJet_pt", "secondJet_pt;p_{T} of second jet, GeV/c;Events", 300, 0., 600.);
    hSecondJetEta = makeTH<TH1F>(myDir, "secondJet_eta", "secondJet_eta;#eta of second jet;Events", 250, -5., 5.); 
    hSecondJetPhi = makeTH<TH1F>(myDir, "secondJet_phi", "secondJet_phi;#phi of second jet;Events", 72, -3.14159, 3.14159); 
    hThirdJetPt = makeTH<TH1F>(myDir, "thirdJet_pt", "thirdJet_pt;p_{T} of third jet, GeV/c;Events", 300, 0., 600.);
    hThirdJetEta = makeTH<TH1F>(myDir, "thirdJet_eta", "thirdJet_eta;#eta of third jet;Events", 250, -5., 5.); 
    hThirdJetPhi = makeTH<TH1F>(myDir, "thirdJet_phi", "thirdJet_phi;#phi of third jet;Events", 72, -3.14159, 3.14159); 
    hFourthJetPt = makeTH<TH1F>(myDir, "fourthJet_pt", "fourthJet_pt;p_{T} of fourth jet, GeV/c;Events", 300, 0., 600.);
    hFourthJetEta = makeTH<TH1F>(myDir, "fourthJet_eta", "fourthJet_eta;#eta of fourth jet;Events", 250, -5., 5.); 
    hFourthJetPhi = makeTH<TH1F>(myDir, "fourthJet_phi", "fourthJet_phi;#phi of fourth jet;Events", 72, -3.14159, 3.14159); 

    // Histograms for PU analysis
    hBetaGenuine = makeTH<TH1F>(myDir, "betaGenuine", "betaGenuine;#beta variable, PV jets;Events", 100, 0., 1.);
    hBetaStarGenuine = makeTH<TH1F>(myDir, "betaStarGenuine", "betaStarGenuine;#beta* variable, PV jets;Events", 100, 0., 1.);
    hMeanDRgenuine = makeTH<TH1F>(myDir, "meanDRGenuine", "meanDRGenuine;Mean #DeltaR, PV jets;Events", 100, 0., 4.);
    hBetaFake = makeTH<TH1F>(myDir, "betaPU", "betaPU;#beta variable, PU jets;Events", 100, 0., 1.);
    hBetaStarFake = makeTH<TH1F>(myDir, "betaStarPU", "betaStarPU;#beta* variable, PU jets;Events", 100, 0., 1.);
    hMeanDRfake = makeTH<TH1F>(myDir, "meanDRPU", "meanDRPU;Mean #DeltaR, PU jets;Events", 100, 0., 4.);
    hBetaVsPUgenuine = makeTH<TH2F>(myDir, "betaVsPUGenuine", "betaVSPUGenuine;#beta variable, PV jets;Number of vertices", 100, 0., 1., 50, 0., 50.);
    hBetaStarVsPUgenuine = makeTH<TH2F>(myDir, "betaVsPUStarGenuine", "betaStarVsPUGenuine;#beta* variable, PV jets;Events", 100, 0., 1., 50, 0., 50.);
    hMeanDRVsPUgenuine = makeTH<TH2F>(myDir, "meanDRVsPUGenuine", "meanDRVsPUGenuine;Mean #DeltaR, PV jets;Events", 100, 0., 4., 50, 0., 50.);
    hBetaVsPUfake = makeTH<TH2F>(myDir, "betaVsPUFake", "betaVsPUFake;#beta variable, PU jets;Events", 100, 0., 1., 50, 0., 50.);
    hBetaStarVsPUfake = makeTH<TH2F>(myDir, "betaStarVsPUFake", "betaStarVsPUFake;#beta* variable, PU jets;Events", 100, 0., 1., 50, 0., 50.);
    hMeanDRVsPUfake = makeTH<TH2F>(myDir, "meanDRVsPUFake", "meanDRVsPUFake;Mean #DeltaR, PU jets;Events", 100, 0., 4., 50, 0., 50.);

    // Histograms for excluded jets (i.e. matching in DeltaR to tau jet)
    TFileDirectory myExcludedJetsDir = myDir.mkdir("ExcludedJets");
    hPtExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_pt", "jet_pt", 40, 0., 400.);
    hEtaExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_eta", "jet_eta", 50, -2.5, 2.5);
    hPhiExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_phi", "jet_phi", 72, -3.14159, 3.41459);
    hNeutralEmEnergyFractionExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_NeutralEmEnergyFraction", "jet_NeutralEmEnergyFraction", 100, 0., 1.);
    hNeutralMultiplicityExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_EmEnergyFraction", "jet_EmEnergyFraction", 100, 0., 1.);
    hNeutralHadronEnergyFractionExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_NeutralHadronFraction", "jet_NeutralHadronEnergyFraction", 100, 0., 1.);
    hNeutralHadronMultiplicityExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hPhotonEnergyFractionExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_PhotonEnergyFraction", "jet_PhotonEnergyFraction", 100, 0., 1.);
    hPhotonMultiplicityExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_PhotonMultiplicity", "jet_PhotonMultiplicity", 100, 0., 100.);
    hMuonEnergyFractionExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_MuonEnergyFraction", "jet_MuonEnergyFraction", 100, 0., 1.);
    hMuonMultiplicityExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hChargedHadronEnergyFractionExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_ChargedHadronEnergyFraction", "jet_ChargedHadronEnergyFraction", 100, 0., 1.);
    hChargedEmEnergyFractionExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_ChargedEmEnergyFraction", "jet_ChargedEmEnergyFraction", 100, 0., 1.);
    hChargedMultiplicityExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_ChargedMultiplicity", "jet_ChargedMultiplicity", 100, 0., 100.);
    hPartonFlavourExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_PartonFlavour", "jet_PartonFlavour", 30, 0., 30.);
    hJECFactorExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_JECFactor", "jet_JECFactor", 100, 0., 10.);
    hN60ExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_N60", "jet_MultiplicityCarrying60PercentOfEnergy", 100, 0., 100.);
    hTowersAreaExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_TowersArea", "jet_TowersArea", 100, 0., 10.);
    hJetChargeExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_JECFactor", "jet_JECFactor", 10, -5., 5.);
    hPtDiffToGenJetExcludedJets = makeTH<TH1F>(myExcludedJetsDir, "jet_PtDiffToGenJet", "jet_PtDiffToGenJet", 100, 0., 10.);

    // Histograms for selected jets
    TFileDirectory mySelectedJetsDir = myDir.mkdir("SelectedJets");
    hPtSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_pt", "jet_pt", 40, 0., 400.);
    hEtaSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_eta", "jet_eta", 50, -2.5, 2.5);
    hPhiSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_phi", "jet_phi", 72, -3.14159, 3.41459);
    hNeutralEmEnergyFractionSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_NeutralEmEnergyFraction", "jet_NeutralEmEnergyFraction", 100, 0., 1.);
    hNeutralMultiplicitySelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_EmEnergyFraction", "jet_EmEnergyFraction", 100, 0., 1.);
    hNeutralHadronEnergyFractionSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_NeutralHadronFraction", "jet_NeutralHadronEnergyFraction", 100, 0., 1.);
    hNeutralHadronMultiplicitySelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hPhotonEnergyFractionSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_PhotonEnergyFraction", "jet_PhotonEnergyFraction", 100, 0., 1.);
    hPhotonMultiplicitySelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_PhotonMultiplicity", "jet_PhotonMultiplicity", 100, 0., 100.);
    hMuonEnergyFractionSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_MuonEnergyFraction", "jet_MuonEnergyFraction", 100, 0., 1.);
    hMuonMultiplicitySelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_NeutralHadronMultiplicity", "jet_NeutralHadronMultiplicity", 100, 0., 100.);
    hChargedHadronEnergyFractionSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_ChargedHadronEnergyFraction", "jet_ChargedHadronEnergyFraction", 100, 0., 1.);
    hChargedEmEnergyFractionSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_ChargedEmEnergyFraction", "jet_ChargedEmEnergyFraction", 100, 0., 1.);
    hChargedMultiplicitySelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_ChargedMultiplicity", "jet_ChargedMultiplicity", 100, 0., 100.);
    hPartonFlavourSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_PartonFlavour", "jet_PartonFlavour", 30, 0., 30.);
    hJECFactorSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_JECFactor", "jet_JECFactor", 100, 0., 10.);
    hN60SelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_N60", "jet_MultiplicityCarrying60PercentOfEnergy", 100, 0., 100.);
    hTowersAreaSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_TowersArea", "jet_TowersArea", 100, 0., 10.);
    hJetChargeSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_JECFactor", "jet_JECFactor", 10, -5., 5.);
    hPtDiffToGenJetSelectedJets = makeTH<TH1F>(mySelectedJetsDir, "jet_PtDiffToGenJet", "jet_PtDiffToGenJet", 100, 0., 10.);

    fMinDeltaRToOppositeDirectionOfTau = 999.;
 }

  JetSelection::~JetSelection() {}

  JetSelection::Data JetSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr< reco::Candidate >& tau, int nVertices) {
    // Reset variables
    iNHadronicJets = -1;
    iNHadronicJetsInFwdDir = -1;
    fMinDeltaRToOppositeDirectionOfTau = 999.;
    bEMFraction08Veto = false;
    bEMFraction07Veto = false;

    bool passEvent = false;

    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fSrc, hjets);

    const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());
    fAllJets = hjets->ptrVector();

    fSelectedJets.clear();
    fNotSelectedJets.clear();
    fNotSelectedJets.reserve(jets.size());

    size_t cleanPassed = 0;
    size_t jetIdPassed = 0;
    size_t ptCutPassed = 0;
    size_t etaCutPassed = 0;
    double maxEMfraction = 0;
    size_t EMfractionCutPassed = 0;

    std::vector<edm::Ptr<pat::Jet> > tmpSelectedJets;
    tmpSelectedJets.reserve(jets.size());

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      increment(fAllSubCount);

      // remove jets too close to tau jet
      bool match = false;
      if(!(ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJet->p4()) > fMaxDR)) {
        match = true;
      }
      if(match) {
        if (iJet->pt() > fPtCut && (std::abs(iJet->eta()) < fEtaCut)) {
          // Fill histograms for excluded jets
          hPtExcludedJets->Fill(iJet->pt());
          hEtaExcludedJets->Fill(iJet->eta());
          hPhiExcludedJets->Fill(iJet->phi());
          hNeutralEmEnergyFractionExcludedJets->Fill(iJet->neutralEmEnergyFraction());
          hNeutralMultiplicityExcludedJets->Fill(iJet->neutralMultiplicity());
          hNeutralHadronEnergyFractionExcludedJets->Fill(iJet->neutralHadronEnergyFraction());
          hNeutralHadronMultiplicityExcludedJets->Fill(iJet->neutralHadronMultiplicity());
          hPhotonEnergyFractionExcludedJets->Fill(iJet->photonEnergyFraction());
          hPhotonMultiplicityExcludedJets->Fill(iJet->photonMultiplicity());
          hMuonEnergyFractionExcludedJets->Fill(iJet->muonEnergyFraction());
          hMuonMultiplicityExcludedJets->Fill(iJet->muonMultiplicity());
          hChargedHadronEnergyFractionExcludedJets->Fill(iJet->chargedHadronEnergyFraction());
          hChargedEmEnergyFractionExcludedJets->Fill(iJet->chargedEmEnergyFraction());
          hChargedMultiplicityExcludedJets->Fill(iJet->chargedMultiplicity());
          //hJECFactorExcludedJets->Fill(iJet->jecFactor());
          //hN60ExcludedJets->Fill(iJet->n60());
          //hTowersAreaExcludedJets->Fill(iJet->towersArea());
          hJetChargeExcludedJets->Fill(iJet->jetCharge());
          if (!iEvent.isRealData()) {
            hPartonFlavourExcludedJets->Fill(iJet->partonFlavour());
            if (iJet->genJet())
              hPtDiffToGenJetExcludedJets->Fill(iJet->pt() / iJet->genJet()->pt());
            else
              hPtDiffToGenJetExcludedJets->Fill(0.);
          }
        }
        continue;
      }
      increment(fCleanCutSubCount);
      ++cleanPassed;

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
      hjetEMFraction->Fill(EMfrac, fEventWeight.getWeight());
      hjetChargedEMFraction->Fill(chargedEMfrac, fEventWeight.getWeight());
      if ( EMfrac > maxEMfraction ) maxEMfraction =  EMfrac;

      if (EMfrac > fEMfractionCut) continue;
      ++EMfractionCutPassed;
      increment(fEMfractionCutSubCount);

      // against PU cut (beta or betaStar)
      double myBeta = iJet->userFloat("Beta");
      //double myBetaMax = iJet->userFloat("BetaMax");
      double myBetaStar = iJet->userFloat("BetaStar");
      double myMeanDR = iJet->userFloat("DRMean");
      bool myIsPVJetStatus = (iJet->userInt("LdgTrackBelongsToSelectedPV") == 1);
      //      std::cout << "mybeta " << myBeta << " myBetaStar " <<  myBetaStar  << " myIsPVJetStatus " << myIsPVJetStatus << std::endl;
 
      // Fill histograms after eta and pt cuts
      
      if (std::abs(iJet->eta()) < fEtaCut && iJet->pt() > fPtCut) {
        if (myIsPVJetStatus) {
          hBetaGenuine->Fill(myBeta, fEventWeight.getWeight());
          hBetaStarGenuine->Fill(myBetaStar, fEventWeight.getWeight());
          hMeanDRgenuine->Fill(myMeanDR, fEventWeight.getWeight());
          hBetaVsPUgenuine->Fill(myBeta, nVertices, fEventWeight.getWeight());
          hBetaStarVsPUgenuine->Fill(myBetaStar, nVertices, fEventWeight.getWeight());
          hMeanDRVsPUgenuine->Fill(myMeanDR, nVertices, fEventWeight.getWeight());
        } else {
          hBetaFake->Fill(myBeta, fEventWeight.getWeight());
          hBetaStarFake->Fill(myBetaStar, fEventWeight.getWeight());
          hMeanDRfake->Fill(myMeanDR, fEventWeight.getWeight());
          hBetaVsPUfake->Fill(myBeta, nVertices, fEventWeight.getWeight());
          hBetaStarVsPUfake->Fill(myBetaStar, nVertices, fEventWeight.getWeight());
          hMeanDRVsPUfake->Fill(myMeanDR, nVertices, fEventWeight.getWeight());
        }
      }
      //if(std::isnan(iJet->userFloat("BetaPV"))) continue;
      if(iJet->userFloat("Beta") < fBetaCut) continue;
      increment(fBetaCutSubCount);

      hPt->Fill(iJet->pt(), fEventWeight.getWeight());
      hEta->Fill(iJet->eta(), fEventWeight.getWeight());
      hPhi->Fill(iJet->phi(), fEventWeight.getWeight());

      // eta cut
      if(!(std::abs(iJet->eta()) < fEtaCut)){
	fNotSelectedJets.push_back(iJet);
	continue;
      }
      increment(fEtaCutSubCount);
      ++etaCutPassed;

      hPtCentral->Fill(iJet->pt(), fEventWeight.getWeight());

      // pt cut
      if(!(iJet->pt() > fPtCut)) continue;
      increment(fPtCutSubCount);
      ++ptCutPassed;
      

      // Fill histograms for selected jets
      hPtSelectedJets->Fill(iJet->pt());
      hEtaSelectedJets->Fill(iJet->eta());
      hPhiSelectedJets->Fill(iJet->phi());
      hNeutralEmEnergyFractionSelectedJets->Fill(iJet->neutralEmEnergyFraction());
      hNeutralMultiplicitySelectedJets->Fill(iJet->neutralMultiplicity());
      hNeutralHadronEnergyFractionSelectedJets->Fill(iJet->neutralHadronEnergyFraction());
      hNeutralHadronMultiplicitySelectedJets->Fill(iJet->neutralHadronMultiplicity());
      hPhotonEnergyFractionSelectedJets->Fill(iJet->photonEnergyFraction());
      hPhotonMultiplicitySelectedJets->Fill(iJet->photonMultiplicity());
      hMuonEnergyFractionSelectedJets->Fill(iJet->muonEnergyFraction());
      hMuonMultiplicitySelectedJets->Fill(iJet->muonMultiplicity());
      hChargedHadronEnergyFractionSelectedJets->Fill(iJet->chargedHadronEnergyFraction());
      hChargedEmEnergyFractionSelectedJets->Fill(iJet->chargedEmEnergyFraction());
      hChargedMultiplicitySelectedJets->Fill(iJet->chargedMultiplicity());
      //hJECFactorSelectedJets->Fill(iJet->jecFactor());
      //hN60SelectedJets->Fill(iJet->n60());
      //hTowersAreaSelectedJets->Fill(iJet->towersArea());
      hJetChargeSelectedJets->Fill(iJet->jetCharge());
      if (!iEvent.isRealData()) {
	hPartonFlavourSelectedJets->Fill(iJet->partonFlavour());
	if (iJet->genJet())
	  hPtDiffToGenJetSelectedJets->Fill(iJet->pt() / iJet->genJet()->pt());
	else
	  hPtDiffToGenJetSelectedJets->Fill(0.);
      }

      // Min DeltaR reversed to tau
      math::XYZTLorentzVectorD myReversedTau = -tau->p4();
      //     math::XYZTLorentzVectorD myReversedTau = -tau.p4();
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(myReversedTau, iJet->p4());
      if (myDeltaR < fMinDeltaRToOppositeDirectionOfTau)
	fMinDeltaRToOppositeDirectionOfTau = myDeltaR;

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
    
    passEvent = fSelectedJets.size() >= fMinNumberOfJets;
    
    if (cleanPassed >= fMinNumberOfJets) 
      increment(fCleanCutCount);

	  //    if(maxEMfraction < fEMfractionCut+ 0.1 )increment(fEMfraction08CutCount);
    //    if(maxEMfraction < fEMfractionCut )increment(fEMfraction07CutCount);

    // Set veto flags for event with high EM fraction of a selected jet
    if (jetIdPassed >= fMinNumberOfJets)
      increment(fJetIdCount);

    if(EMfractionCutPassed >= fMinNumberOfJets)
      increment(fEMfractionCutCount);

    if (ptCutPassed >= fMinNumberOfJets)
      increment(fPtCutCount);

    if (etaCutPassed >= fMinNumberOfJets)
      increment(fEtaCutCount);

    if (passEvent && maxEMfraction >= 0.8 ) {
      increment(fEMfraction08CutCount);
      bEMFraction08Veto = true;
    }
      
    if (passEvent && maxEMfraction < 0.7 ) {
      increment(fEMfraction07CutCount);
      bEMFraction07Veto = true;
    }


    // Plot pt, eta, and phi of jets if jet selection has been passed
    if (passEvent && fSelectedJets.size() >= 3) {
      hFirstJetPt->Fill(fSelectedJets[0]->pt());
      hFirstJetEta->Fill(fSelectedJets[0]->eta());
      hFirstJetPhi->Fill(fSelectedJets[0]->phi());
      hSecondJetPt->Fill(fSelectedJets[1]->pt());
      hSecondJetEta->Fill(fSelectedJets[1]->eta());
      hSecondJetPhi->Fill(fSelectedJets[1]->phi());
      hThirdJetPt->Fill(fSelectedJets[2]->pt());
      hThirdJetEta->Fill(fSelectedJets[2]->eta());
      hThirdJetPhi->Fill(fSelectedJets[2]->phi());
      if (fSelectedJets.size() >= 4) {
        hFourthJetPt->Fill(fSelectedJets[3]->pt());
        hFourthJetEta->Fill(fSelectedJets[3]->eta());
        hFourthJetPhi->Fill(fSelectedJets[3]->phi());
      }
    }
    hMinDeltaRToOppositeDirectionOfTau->Fill(fMinDeltaRToOppositeDirectionOfTau);

    return Data(this, passEvent);
  }
}
