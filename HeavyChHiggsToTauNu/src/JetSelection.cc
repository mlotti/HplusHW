#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"

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
    fReferenceJetToTauDeltaR(-1),
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
    fJetPileUpMVAValuesSrc(iConfig.getUntrackedParameter<edm::InputTag>("jetPileUpMVAValues")),
    fJetPileUpIdFlagSrc(iConfig.getUntrackedParameter<edm::InputTag>("jetPileUpIdFlag")),
    fApplyVetoForDeadECALCells(iConfig.getUntrackedParameter<bool>("applyVetoForDeadECALCells")),
    fDeadECALCellsVetoDeltaR(iConfig.getUntrackedParameter<double>("deadECALCellsVetoDeltaR")),
    fAllCount(eventCounter.addSubCounter("Jet main","All events")),
    fDeadECALCellVetoCount(eventCounter.addSubCounter("Jet main","Dead ECAL cells veto")),
    fCleanCutCount(eventCounter.addSubCounter("Jet main","Jet cleaning")),
    fJetIdCount(eventCounter.addSubCounter("Jet main", "Jet ID")),
    fJetPUIDCount(eventCounter.addSubCounter("Jet main","Jet PU ID")),
    fEMfractionCutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac ")),
    fEtaCutCount(eventCounter.addSubCounter("Jet main","Jet eta cut")),
    fPtCutCount(eventCounter.addSubCounter("Jet main","Jet pt cut")),
    fAllSubCount(eventCounter.addSubCounter("Jet selection", "all jets")),
    fEMfraction08CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.8")),
    fEMfraction07CutCount(eventCounter.addSubCounter("Jet main","Jet EMfrac < 0.7")),
    fEventKilledByJetPUIDCount(eventCounter.addSubCounter("Jet main","Event killed by jet PU ID")),
    fCleanCutSubCount(eventCounter.addSubCounter("Jet selection", "cleaning")),
    fneutralHadronEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "neutralHadronEnergyFractionCut")),
    fneutralEmEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "neutralEmEnergyFractionCut")),
    fnumberOfDaughtersCutSubCount(eventCounter.addSubCounter("Jet selection", "numberOfDaughtersCut")),
    fchargedHadronEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "chargedHadronEnergyFractionCut")),
    fchargedMultiplicityCutSubCount(eventCounter.addSubCounter("Jet selection", "fchargedMultiplicityCut")),
    fchargedEmEnergyFractionCutSubCount(eventCounter.addSubCounter("Jet selection", "chargedEmEnergyFractionCut")),
    fJetIdSubCount(eventCounter.addSubCounter("Jet selection", "Jet ID")),
    fEMfractionCutSubCount(eventCounter.addSubCounter("Jet selection", "EMfraction")),
    fJetPUIDSubCount(eventCounter.addSubCounter("Jet selection", "Jet PU ID")),
    fEtaCutSubCount(eventCounter.addSubCounter("Jet selection", "eta cut")),
    fPtCutSubCount(eventCounter.addSubCounter("Jet selection", "pt cut")),
    fJetToTauReferenceJetNotIdentifiedCount(eventCounter.addSubCounter("Jet selection", "jet->tau ref.jet not identified"))
  {
    // Check input for jet PU ID
    if (fJetPileUpMVAValuesSrc.label() == "")
      throw cms::Exception("Config") << "JetSelection: Jet PU ID MVA values inputtag is empty! Check that it gets set automatically!";
    if (fJetPileUpIdFlagSrc.label() == "")
      throw cms::Exception("Config") << "JetSelection: Jet PU ID decision flags values inputtag is empty! Check that it gets set automatically!";
    // Remaining jet PU ID options are checked at config creation level, now parse working point
    std::string myPUIDWP = iConfig.getUntrackedParameter<std::string>("jetPileUpWorkingPoint");
    if (myPUIDWP == "loose")
      fJetPileUpWorkingPoint = PileupJetIdentifier::kLoose;
    else if (myPUIDWP == "medium")
      fJetPileUpWorkingPoint = PileupJetIdentifier::kMedium;
    else if (myPUIDWP == "tight")
      fJetPileUpWorkingPoint = PileupJetIdentifier::kTight;
    else
      throw cms::Exception("Config") << "JetSelection: Jet PU ID working point '" << myPUIDWP << "' is not valide! Check your config!";

    // Create histograms
    edm::Service<TFileService> fs;
    // Create directory only if histo level is at most kInformative, which is the highest level within JetSelection
    TFileDirectory myDir = histoWrapper.mkdir(HistoWrapper::kInformative, *fs, "JetSelection");

    hPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_pt", "identified jet_pt", 120, 0., 600.);
    hPtCentral = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_pt_central", "identified jet_pt_central", 120, 0., 600.);
    hEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_eta", "identified jet_eta", 100, -5., 5.);
    hPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_phi", "identified jet_phi", 72, -3.1415926, 3.1415926);
    hPtIncludingTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_pt_including_tau", "jet_pt_including_tau", 120, 0., 600.);
    hEtaIncludingTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_eta_including_tau", "jet_eta_including_tau", 100, -5., 5.);
    hPhiIncludingTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_phi_including_tau", "jet_phi_including_tau", 72, -3.1415926, 3.1415926);
    hNumberOfSelectedJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfSelectedJets", "NumberOfSelectedJets", 30, 0., 30.);
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

    hDeltaPtJetTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "deltaPtTauJet", "deltaPtTauJet ", 200, -100., 100.);
    hDeltaRJetTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "deltaRTauJet", "deltaRTauJet ", 120, 0., 6.);
    // Histograms for PU analysis
    hJetPUIDMvaResult = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jet_PUIDmva", "jet_PUIDmva;MVA value;N_{Events}", 100, -1.0, 1.0);

    // Histograms for excluded jets (i.e. matching in DeltaR to tau jet)
    fExcludedJetsDetailHistograms = new JetDetailHistograms(fHistoWrapper, myDir, "ExcludedJets");

    // Histograms for selected jets
    fSelectedJetsDetailHistograms = new JetDetailHistograms(fHistoWrapper, myDir, "SelectedJets");

    // MHT related
    TFileDirectory myMHTDir = histoWrapper.mkdir(HistoWrapper::kInformative, myDir, "MHT");
    hMHT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "MHT", "MHT;MHT, GeV;N_{events}", 100, 0., 500.);
    hMHTphi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "MHTphi", "MHTphi;MHT #phi;N_{events}", 72, -3.14159265, -3.14159265);
    hDeltaPhiMHTJet1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet1", "DeltaPhiMHTJet1;#Delta#phi(MHT,jet1), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTJet2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet2", "DeltaPhiMHTJet2;#Delta#phi(MHT,jet2), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTJet3 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet3", "DeltaPhiMHTJet3;#Delta#phi(MHT,jet3), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTJet4 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTJet4", "DeltaPhiMHTJet4;#Delta#phi(MHT,jet4), ^{o};N_{events}", 36, 0., 180.);
    hDeltaPhiMHTTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myMHTDir, "DeltaPhiMHTTau", "DeltaPhiMHTTau;#Delta#phi(MHT,tau), ^{o};N_{events}", 36, 0., 180.);

    // Reference tau related
    TFileDirectory myRefDir = histoWrapper.mkdir(HistoWrapper::kInformative, myDir, "ReferenceJetToTau");
    hReferenceJetToTauMatchingDeltaR = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "MatchingDeltaR", "MatchingDeltaR;Matching #DeltaR;N_{events}", 30, 0., 1.);
    hReferenceJetToTauPartonFlavour = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "PartonFlavour", "ReferenceJetToTauPartonFlavour;ReferenceJetToTauPartonFlavour;N_{events}", 30, 0., 30.);
    hReferenceJetToTauDeltaPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "DeltaPt", "ReferenceJetToTauDeltaPt;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);
    hReferenceJetToTauPtRatio = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myRefDir, "PtRatio", "ReferenceJetToTauPtRatio;#tau p_{T} / ref.jet p_{T}, GeV/c;N_{events}", 120, 0., 1.2);

 }

  JetSelection::~JetSelection() {}

  JetSelection::Data JetSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, edm::Ptr<pat::Tau>(), nVertices);
  }

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
    if (tau.isNull())
      throw cms::Exception("LogicError") << "JetSelection::analyze was called with tau == zero pointer. Make sure a tau is found before calling JetSelection::analyze()" << std::endl;
    return privateAnalyze(iEvent, iSetup, tau, nVertices);
  }

  JetSelection::Data JetSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr< reco::Candidate >& tau, int nVertices) {
    Data output;

    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fSrc, hjets);

    edm::Handle<edm::ValueMap<float> > myJetPUIDMVA;
    if (fJetPileUpMVAValuesSrc.label() != "None")
      iEvent.getByLabel(fJetPileUpMVAValuesSrc, myJetPUIDMVA);

    edm::Handle<edm::ValueMap<int> > myJetPUIDFlag;
    if (fJetPileUpMVAValuesSrc.label() != "None")
      iEvent.getByLabel(fJetPileUpIdFlagSrc, myJetPUIDFlag);

    const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());

    size_t cleanPassed = 0;
    size_t jetIdPassed = 0;
    size_t killedByJetPUIDCut = 0;
    size_t jetPUIDPassed = 0;
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

      // Jet PU ID
      if (fJetPileUpMVAValuesSrc.label() != "None") {
        float myPUIDMVAValue = (*myJetPUIDMVA)[iJet];
        int myPUIDFlag = (*myJetPUIDFlag)[iJet];
        hJetPUIDMvaResult->Fill(myPUIDMVAValue);
        if (!PileupJetIdentifier::passJetId(myPUIDFlag, fJetPileUpWorkingPoint)) {
          // Count how many jets, that otherwise would have been selected, are killed by jet PU ID
          if (std::abs(iJet->eta()) < fEtaCut && iJet->pt() > fPtCut)
            ++killedByJetPUIDCut;
          continue;
        }
      }
      increment(fJetPUIDSubCount);
      ++jetPUIDPassed;
      hPtIncludingTau->Fill(iJet->pt());
      hEtaIncludingTau->Fill(iJet->eta());
      hPhiIncludingTau->Fill(iJet->phi());

      // Jet identification and jet PU ID cuts done, store jet to list of all jets
      output.fAllIdentifiedJets.push_back(iJet);
      if (iJet->pt() > fPtCut && (std::abs(iJet->eta()) < fEtaCut)) {
        output.fSelectedJetsIncludingTau.push_back(iJet);
      }

      // remove jets too close to tau jet
      if (tau.isNonnull()) {
        hDeltaRJetTau->Fill(ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJet->p4()));
        bool match = false;
        if(!(ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJet->p4()) > fMaxDR)) {
          match = true;
          output.fDeltaPtJetTau = iJet->pt() - (tau)->pt();
          hDeltaPtJetTau->Fill(iJet->pt() - (tau)->pt());
        }
        if(match) {
          if (iJet->pt() > fPtCut && (std::abs(iJet->eta()) < fEtaCut)) {
            fExcludedJetsDetailHistograms->fill(iJet, iEvent.isRealData());
          }
          continue;
        }
      }
      increment(fCleanCutSubCount);
      ++cleanPassed;
      hPt->Fill(iJet->pt());
      hEta->Fill(iJet->eta());
      hPhi->Fill(iJet->phi());

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
      fSelectedJetsDetailHistograms->fill(iJet, iEvent.isRealData());

      // Min DeltaR reversed to tau
      math::XYZTLorentzVectorD myReversedTau;
      if (tau.isNonnull()) {
        myReversedTau = -tau->p4();
      }
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

    if (fNumberOfJets.passedCut(output.fSelectedJets.size()+killedByJetPUIDCut)) {
      increment(fEventKilledByJetPUIDCount);
    }

    if (fNumberOfJets.passedCut(cleanPassed))
      increment(fCleanCutCount);

	  //    if(maxEMfraction < fEMfractionCut+ 0.1 )increment(fEMfraction08CutCount);
    //    if(maxEMfraction < fEMfractionCut )increment(fEMfraction07CutCount);

    // Set veto flags for event with high EM fraction of a selected jet
    if (fNumberOfJets.passedCut(jetIdPassed))
      increment(fJetIdCount);

    if (fNumberOfJets.passedCut(jetPUIDPassed))
      increment(fJetPUIDCount);

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
      if (tau.isNonnull())
        output.fAverageSelectedJetsEtaDistanceToTauEta = std::abs(myMegaJet.eta() - tau->eta());
    }

    // Analyze reference jet of selected tau
    obtainReferenceJetToTau(output.fAllJets, tau, output);

    // Calculate MHT on jets
    calculateMHT(output, tau);

    // Everything has been done now return
    return output;
  }

  void JetSelection::obtainReferenceJetToTau(const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::Candidate>& tau, JetSelection::Data& output) {
    if (tau.isNull()) {
      increment(fJetToTauReferenceJetNotIdentifiedCount);
      return;
    }
    const pat::Tau *tauObject = dynamic_cast<const pat::Tau *>(tau.get());
    if (!tauObject) {
      increment(fJetToTauReferenceJetNotIdentifiedCount);
      return;
    }
    double myMinDeltaR = 999.;
    for (edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      double myDeltaR = reco::deltaR(tauObject->p4Jet(), **iter);
      if (myDeltaR < myMinDeltaR) {
        myMinDeltaR = myDeltaR;
        if (myDeltaR < 0.4) {
          output.fReferenceJetToTau = *iter;
        }
      }
    }
    hReferenceJetToTauMatchingDeltaR->Fill(myMinDeltaR);
    output.fReferenceJetToTauDeltaR = myMinDeltaR;
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
    // Calculate angles between MHT and the jets (overlap with tau not considered)
    int njets = 0;
    for (size_t i = 0; i < output.fAllIdentifiedJets.size(); ++i) {
      if (!(output.fAllIdentifiedJets[i]->pt() > fPtCut && (std::abs(output.fAllIdentifiedJets[i]->eta()) < fEtaCut))) continue;
      double myDeltaPhi = reco::deltaPhi(output.fMHT, *(output.fAllIdentifiedJets[i])) * 57.3;
      if (njets == 0) {
        output.fDeltaPhiMHTJet1 = myDeltaPhi;
        hDeltaPhiMHTJet1->Fill(myDeltaPhi);
      } else if (njets == 1) {
        output.fDeltaPhiMHTJet2 = myDeltaPhi;
        hDeltaPhiMHTJet2->Fill(myDeltaPhi);
      } else if (njets == 2) {
        output.fDeltaPhiMHTJet3 = myDeltaPhi;
        hDeltaPhiMHTJet3->Fill(myDeltaPhi);
      } else if (njets == 3) {
        output.fDeltaPhiMHTJet4 = myDeltaPhi;
        hDeltaPhiMHTJet4->Fill(myDeltaPhi);
      }
      ++njets;
    }
    if (tau.isNonnull()) {
      output.fDeltaPhiMHTTau = reco::deltaPhi(output.fMHT, *tau) * 57.3;
      hDeltaPhiMHTTau->Fill(output.fDeltaPhiMHTTau);
    }
  }

}
