#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::XYZTLorentzVector LorentzVector;

namespace HPlus {
  FakeTauIdentifier::Data::Data(): fTauMatchType(kkNoMC), fTauOriginType(kkUnknownOrigin), fTauMatchGenParticle(0) {}
  FakeTauIdentifier::Data::~Data() {}
  
  FakeTauIdentifier::FakeTauIdentifier(const edm::ParameterSet& iConfig, const edm::ParameterSet& tauIDConfig, HPlus::HistoWrapper& histoWrapper, std::string label):
    fVisibleMCTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("visibleMCTauSrc")),
    fVisibleMCTauOneProngSrc(iConfig.getUntrackedParameter<edm::InputTag>("visibleMCTauOneProngSrc")),
    fMatchingConditionDeltaR(iConfig.getUntrackedParameter<double>("matchingConditionDeltaR")),
    // Scale factors for tau ID and X->tau fakes mis-ID
    fSFGenuineTauBarrel(iConfig.getUntrackedParameter<double>("scalefactorGenuineTauBarrel")),
    fSFGenuineTauEndcap(iConfig.getUntrackedParameter<double>("scalefactorGenuineTauEndcap")),
    fSFFakeTauBarrelElectron(iConfig.getUntrackedParameter<double>("scalefactorFakeTauBarrelElectron")),
    fSFFakeTauEndcapElectron(iConfig.getUntrackedParameter<double>("scalefactorFakeTauEndcapElectron")),
    fSFFakeTauBarrelMuon(iConfig.getUntrackedParameter<double>("scalefactorFakeTauBarrelMuon")),
    fSFFakeTauEndcapMuon(iConfig.getUntrackedParameter<double>("scalefactorFakeTauEndcapMuon")),
    fSFFakeTauBarrelJet(iConfig.getUntrackedParameter<double>("scalefactorFakeTauBarrelJet")),
    fSFFakeTauEndcapJet(iConfig.getUntrackedParameter<double>("scalefactorFakeTauEndcapJet")),
    // Systematic uncertainties for tau ID and X->tau fakes mis-ID
    fSystematicsGenuineTauBarrel(iConfig.getUntrackedParameter<double>("systematicsGenuineTauBarrel")),
    fSystematicsGenuineTauEndcap(iConfig.getUntrackedParameter<double>("systematicsGenuineTauEndcap")),
    fSystematicsFakeTauBarrelElectron(iConfig.getUntrackedParameter<double>("systematicsFakeTauBarrelElectron")),
    fSystematicsFakeTauEndcapElectron(iConfig.getUntrackedParameter<double>("systematicsFakeTauEndcapElectron")),
    fSystematicsFakeTauBarrelMuon(iConfig.getUntrackedParameter<double>("systematicsFakeTauBarrelMuon")),
    fSystematicsFakeTauEndcapMuon(iConfig.getUntrackedParameter<double>("systematicsFakeTauEndcapMuon")),
    fSystematicsFakeTauBarrelJet(iConfig.getUntrackedParameter<double>("systematicsFakeTauBarrelJet")),
    fSystematicsFakeTauEndcapJet(iConfig.getUntrackedParameter<double>("systematicsFakeTauEndcapJet")),
    // Cut values for acceptance (taken from tau ID config)
    fPtAcceptance(tauIDConfig.getUntrackedParameter<double>("ptCut")),
    fEtaAcceptance(tauIDConfig.getUntrackedParameter<double>("etaCut"))
  {
    edm::Service<TFileService> fs;
    // Create histograms
    TFileDirectory myDir = fs->mkdir("FakeTauIdentifier_"+label);

    //    hTauMatchType = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauMatchType", "TauMatchType", 13, 0, 13);
    hTauMatchType = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauMatchType", "TauMatchType", kkNumberOfSelectedTauMatchTypes, 0, kkNumberOfSelectedTauMatchTypes);

    if (hTauMatchType->isActive()) {
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkNoMC, "NoMatch");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronToTau, "e#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronFromTauDecayToTau, "tau#rightarrowe#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonToTau, "#mu#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonFromTauDecayToTau, "tau#rightarrow#mu#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkTauToTau, "genuine hadr. #tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkOneProngTauToTau, "genuine 1-pr. hadr. #tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkJetToTau, "jet#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronToTauAndTauJetInsideAcceptance, "e#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronFromTauDecayToTauAndTauJetInsideAcceptance, "#tau#rightarrowe#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonToTauAndTauJetInsideAcceptance, "#mu#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonFromTauDecayToTauAndTauJetInsideAcceptance, "#tau#rightarrow#mu#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkTauToTauAndTauJetInsideAcceptance, "genuine hadr. #tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkOneProngTauToTauAndTauJetInsideAcceptance, "genuine 1-pr. hadr. #tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkJetToTauAndTauJetInsideAcceptance, "jet#rightarrow#tau, #tau outside");
    }
    hTauOrigin = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauOrigin", "TauOrigin", 7, 0, 7);
    if (hTauOrigin->isActive()) {
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tau#tau");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
    }
    hMuOrigin = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MuOrigin", "MuOrigin", 7, 0, 7);
    if (hMuOrigin->isActive()) {
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tautau");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
    }
    hElectronOrigin = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronOrigin", "ElectronOrigin", 7, 0, 7);
    if (hElectronOrigin->isActive()) {
      hElectronOrigin->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
      hElectronOrigin->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
      hElectronOrigin->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
      hElectronOrigin->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
      hElectronOrigin->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
      hElectronOrigin->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tautau");
      hElectronOrigin->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
    }
  }
  
  FakeTauIdentifier::~FakeTauIdentifier() {
    
  }
  
  FakeTauIdentifier::Data FakeTauIdentifier::matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau) {
    return privateMatchTauToMC(iEvent, tau, false);
  }
  
  FakeTauIdentifier::Data FakeTauIdentifier::silentMatchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau) {
    return privateMatchTauToMC(iEvent, tau, true);
  }
  
  FakeTauIdentifier::Data FakeTauIdentifier::privateMatchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau, bool silentMode) {
    Data output;

    // Return if event is real data
    if (iEvent.isRealData()) return output;

    bool isHadronicTau = false;
    bool isOneProngMCTau = false;
    bool isMCElectron = false; // any MC electron
    bool isMCMuon = false; // any MC muon
    bool isLeptonicTauDecay = false;
    size_t myTauIndex = 0;
    size_t myElectronIndex = 0;
    size_t myMuIndex = 0;
    // For embedding result (Note that acceptance is acceptance of MC tau lepton, not of MC visible tau)
    size_t nMatchedHadronicTausInAcceptance = 0;
    size_t nMatchedElectronicTausInAcceptance = 0;
    size_t nMatchedMuonicTausInAcceptance = 0;
    size_t nNonMatchedHadronicTausInAcceptance = 0;
    size_t nNonMatchedLeptonicTausInAcceptance = 0;

    // Check matching to visible MC taus
//     edm::Handle <std::vector<LorentzVector> > myMCVisibleTaus;
//     iEvent.getByLabel(fVisibleMCTauSrc, myMCVisibleTaus);
    // Load list of genParticles
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);

    // Collect ids of tau leptons
    std::vector<size_t> myTauIndices;
    for (size_t i=0; i < genParticles->size(); ++i) {
      // Look for a tau
      const reco::Candidate & p = (*genParticles)[i];
      if (std::abs(p.pdgId()) == 15) {
        // Ignore tau that is radiating before decay
        bool myVetoStatus = false;
        for (size_t im=0; im < p.numberOfDaughters(); ++im){
          if (std::abs(p.daughter(im)->pdgId()) == 15) myVetoStatus = true;
        }
        if (myVetoStatus) continue;
        // Store tau index
        myTauIndices.push_back(i);
      }
    }

    // Find taus, which match to the reconstructed tau (use visible tau momentum for the matching test)
    std::vector<size_t> myMatchingTauIndices;
    std::vector<size_t> myNonMatchingTauIndices;
    for (std::vector<size_t>::iterator idx = myTauIndices.begin(); idx != myTauIndices.end(); ++idx) {
      const reco::Candidate & p = (*genParticles)[*idx];
      // Obtain visible tau momentum vector (i.e. subtract neutrinoes)
      LorentzVector myVisibleTauMomentum = p.p4();
      for (size_t im=0; im < p.numberOfDaughters(); ++im) {
        int myAbsPdgId = std::abs(p.daughter(im)->pdgId());
        if (myAbsPdgId == 12 || myAbsPdgId == 14 || myAbsPdgId == 16)
          myVisibleTauMomentum -= p.daughter(im)->p4();
      }
      if (reco::deltaR(myVisibleTauMomentum, tau.p4()) < fMatchingConditionDeltaR) {
        myMatchingTauIndices.push_back(*idx);
      } else {
        myNonMatchingTauIndices.push_back(*idx);
      }
    }

    // Look at matched taus
    // Note that in rare cases multiple MC taus could be in the matching cone
    for (std::vector<size_t>::iterator idx = myMatchingTauIndices.begin(); idx != myMatchingTauIndices.end(); ++idx) {
      const reco::Candidate & p = (*genParticles)[*idx];
      // Obtain tau lepton momentum vector
      LorentzVector myTauLeptonMomentum = p.p4();
      // Check if tau decays to electron or muon
      bool tmpTauToElectron = false;
      bool tmpTauToMuon = false;
      for (size_t im=0; im < p.numberOfDaughters(); ++im) {
        int myAbsPdgId = std::abs(p.daughter(im)->pdgId());
        if (myAbsPdgId == 11) {
          tmpTauToElectron = true;
          isLeptonicTauDecay = true;
          if (!isHadronicTau) myTauIndex = *idx;
        }
        if (myAbsPdgId == 13) {
          tmpTauToMuon = true;
          isLeptonicTauDecay = true;
          if (!isHadronicTau) myTauIndex = *idx;
        }
      }
      // Find hadronic tau index
      if (!tmpTauToElectron && !tmpTauToMuon) {
        myTauIndex = *idx;
        isHadronicTau = true;
      }
      // Check acceptance
      if (myTauLeptonMomentum.pt() > fPtAcceptance && abs(myTauLeptonMomentum.eta()) < fEtaAcceptance) {
        if (tmpTauToElectron)
          ++nMatchedElectronicTausInAcceptance;
        else if (tmpTauToMuon)
          ++nMatchedMuonicTausInAcceptance;
        else
          ++nMatchedHadronicTausInAcceptance;
      }
    }

    // Look at non-matched taus
    for (std::vector<size_t>::iterator idx = myNonMatchingTauIndices.begin(); idx != myNonMatchingTauIndices.end(); ++idx) {
      const reco::Candidate & p = (*genParticles)[*idx];
      // Obtain tau lepton momentum vector
      LorentzVector myTauLeptonMomentum = p.p4();
      // Check if tau decays to electron or muon
      bool tmpTauToLeptons = false;
      for (size_t im=0; im < p.numberOfDaughters(); ++im) {
        int myAbsPdgId = std::abs(p.daughter(im)->pdgId());
        if (myAbsPdgId == 11 || myAbsPdgId == 13)
          tmpTauToLeptons = true;
      }
      // Check acceptance
      if (myTauLeptonMomentum.pt() > fPtAcceptance && abs(myTauLeptonMomentum.eta()) < fEtaAcceptance) {
        if (tmpTauToLeptons)
          ++nNonMatchedLeptonicTausInAcceptance;
        else
          ++nNonMatchedHadronicTausInAcceptance;
      }
    }

    // Check matching to visible MC 1-prong taus
    edm::Handle <std::vector<LorentzVector> > myMCVisibleOneProngTaus;
    iEvent.getByLabel(fVisibleMCTauOneProngSrc, myMCVisibleOneProngTaus);
    // Check matching to MC visible taus
    for (std::vector<LorentzVector>::const_iterator it = myMCVisibleOneProngTaus->begin(); it != myMCVisibleOneProngTaus->end(); ++it) {
      if (reco::deltaR((*it), tau.p4()) < fMatchingConditionDeltaR) {
        // Match found
        isOneProngMCTau = true;
      }
    }

    // Look for matching with MC electrons or MC muons
    //std::cout << "matchfinding:" << std::endl;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      int myAbsPdgId = std::abs(p.pdgId());
      if (myAbsPdgId == 11 || myAbsPdgId == 13) {
        // Check match with tau
        if (reco::deltaR(p.p4(), tau.p4()) < fMatchingConditionDeltaR) {
          if (p.pt() > 10.) { // Require some pT for enough low curvature
            //std::cout << "  match found, pid=" << p.pdgId() << " eta=" << std::abs(p.eta()) << " pt=" << p.pt() << std::endl;
            if (myAbsPdgId == 11) {
              isMCElectron = true;
              myElectronIndex = i;
            } else if (myAbsPdgId == 13) {
              isMCMuon = true;
              myMuIndex = i;
            }
          }
        }
      }
    }

    // Set result
    // Checking is done in following order: electron, muon, tau
    // If none of them matches to the reconstructed tau, jet->tau is assumed
    if (isMCElectron) {
      if (isLeptonicTauDecay) {
        if (!nNonMatchedHadronicTausInAcceptance) {
          output.fTauMatchType = kkElectronFromTauDecayToTau;
        } else {
          output.fTauMatchType = kkElectronFromTauDecayToTauAndTauJetInsideAcceptance;
        }
      } else {
        if (!nNonMatchedHadronicTausInAcceptance) {
          output.fTauMatchType = kkElectronToTau;
        } else {
          output.fTauMatchType = kkElectronToTauAndTauJetInsideAcceptance;
        }
      }
    } else if (isMCMuon) {
      if (isLeptonicTauDecay) {
        if (!nNonMatchedHadronicTausInAcceptance) {
          output.fTauMatchType = kkMuonFromTauDecayToTau;
        } else {
          output.fTauMatchType = kkMuonFromTauDecayToTauAndTauJetInsideAcceptance;
        }
      } else {
        if (!nNonMatchedHadronicTausInAcceptance) {
          output.fTauMatchType = kkMuonToTau;
        } else {
          output.fTauMatchType = kkMuonToTauAndTauJetInsideAcceptance;
        }
      }
    } else if (isHadronicTau) {
      if (!nNonMatchedHadronicTausInAcceptance) {
        output.fTauMatchType = kkTauToTau;
      } else {
        output.fTauMatchType = kkTauToTauAndTauJetInsideAcceptance;
      }
      if (isOneProngMCTau) {
        if (!nNonMatchedHadronicTausInAcceptance) {
          output.fTauMatchType = kkOneProngTauToTau;
        } else {
          output.fTauMatchType = kkOneProngTauToTauAndTauJetInsideAcceptance;
        }
      }
    } else {
      if (!nNonMatchedHadronicTausInAcceptance) {
        output.fTauMatchType = kkJetToTau;
      } else {
        output.fTauMatchType = kkJetToTauAndTauJetInsideAcceptance;
      }
    }

    // Determine if event goes to embedding or to EWK+tt with fake tau background
    output.fBackgroundType = kkUnknown;
    if (nMatchedHadronicTausInAcceptance == 0)
      output.fBackgroundType = kkEWKFakeTauLike;
    else if (nMatchedHadronicTausInAcceptance >= 1 && nNonMatchedHadronicTausInAcceptance == 0)
      output.fBackgroundType = kkEmbeddingLikeSingleTauInAcceptance;
    else if (nMatchedHadronicTausInAcceptance >= 1 && nNonMatchedHadronicTausInAcceptance >= 1)
      output.fBackgroundType = kkEmbeddingLikeMultipleTausInAcceptance;

    //std::cout << "Nmatched=" << myMatchingTauIndices.size() << " NmatchHadronic=" << nMatchedHadronicTausInAcceptance
    //  << " Nnonmatched=" << myNonMatchingTauIndices.size() << " NnonmatchHadronic=" << nNonMatchedHadronicTausInAcceptance << " bkgtype=" << output.fBackgroundType << std::endl;

    // Look at ancestor information
    output.fTauOriginType = kkUnknownOrigin;
    if (output.fTauMatchType != kkJetToTau) {
      size_t myIndex = 0;
      if (isMCElectron)
        myIndex = myElectronIndex;
      else if (isMCMuon)
        myIndex = myMuIndex;
      else if (isHadronicTau) {
        myIndex = myTauIndex;
      }
      bool myWStatus = false;
      bool myZStatus = false;
      bool myHPlusStatus = false;
      bool myTauStatus = false;
      //reco::Candidate* p = const_cast<reco::Candidate*>((*genParticles)[myIndex].mother());
      output.fTauMatchGenParticle = &((*genParticles)[myIndex]);
      const reco::Candidate* p = output.fTauMatchGenParticle->mother();
      while (p) {
        if (std::abs(p->pdgId()) == 15)
          myTauStatus = true;
        if (std::abs(p->pdgId()) == 24)
          myWStatus = true;
        if (std::abs(p->pdgId()) == 23)
          myZStatus = true;
        if (std::abs(p->pdgId()) == 37)
          myHPlusStatus = true;
        // move to next
        p = p->mother();
        //if (isMCElectron and p) std::cout << "e: mother = " << p->pdgId() << std::endl;
      }
      if (!myTauStatus) {
        if (myWStatus) output.fTauOriginType = kkFromW;
        else if (myZStatus) output.fTauOriginType = kkFromZ;
        else if (myHPlusStatus) output.fTauOriginType = kkFromHplus;
      } else {
        if (myWStatus) output.fTauOriginType = kkFromWTau;
        else if (myZStatus) output.fTauOriginType = kkFromZTauTau;
        else if (myHPlusStatus) output.fTauOriginType = kkFromHplusTau; 
      }
    }
    if (!silentMode) {
      // Fill histograms
      hTauMatchType->Fill(output.fTauMatchType);
      if (output.fTauMatchType == kkOneProngTauToTau) hTauMatchType->Fill(kkTauToTau);
      if (output.fTauMatchType == kkOneProngTauToTauAndTauJetInsideAcceptance) hTauMatchType->Fill(kkTauToTauAndTauJetInsideAcceptance);
      if (isMCElectron)
        hElectronOrigin->Fill(output.fTauOriginType);
      else if (isMCMuon)
        hMuOrigin->Fill(output.fTauOriginType);
      else if (isHadronicTau)
        hTauOrigin->Fill(output.fTauOriginType);
    }
    // Return result
    return output;
  }

  double FakeTauIdentifier::getFakeTauScaleFactor(FakeTauIdentifier::MCSelectedTauMatchType matchType, double eta) {
    if (matchType == FakeTauIdentifier::kkTauToTau ||
        matchType == FakeTauIdentifier::kkOneProngTauToTau ||
        matchType == FakeTauIdentifier::kkTauToTauAndTauJetInsideAcceptance ||
        matchType == FakeTauIdentifier::kkOneProngTauToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSFGenuineTauBarrel;
      } else {
        return fSFGenuineTauEndcap;
      }
    } else if (matchType == FakeTauIdentifier::kkElectronToTau ||
               matchType == FakeTauIdentifier::kkElectronToTauAndTauJetInsideAcceptance ||
               matchType == FakeTauIdentifier::kkElectronFromTauDecayToTau ||
               matchType == FakeTauIdentifier::kkElectronFromTauDecayToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSFFakeTauBarrelElectron;
      } else {
        return fSFFakeTauEndcapElectron;
      }
    } else if (matchType == FakeTauIdentifier::kkMuonToTau ||
               matchType == FakeTauIdentifier::kkMuonToTauAndTauJetInsideAcceptance ||
               matchType == FakeTauIdentifier::kkMuonFromTauDecayToTau ||
               matchType == FakeTauIdentifier::kkMuonFromTauDecayToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSFFakeTauBarrelMuon;
      } else {
        return fSFFakeTauEndcapMuon;
      }
    } else if (matchType == FakeTauIdentifier::kkJetToTau ||
               matchType == FakeTauIdentifier::kkJetToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSFFakeTauBarrelJet;
      } else {
        return fSFFakeTauEndcapJet;
      }
    }
    return 1.0;
  }

  double FakeTauIdentifier::getFakeTauSystematics(MCSelectedTauMatchType matchType, double eta) {
    if (matchType == FakeTauIdentifier::kkTauToTau ||
        matchType == FakeTauIdentifier::kkOneProngTauToTau ||
        matchType == FakeTauIdentifier::kkTauToTauAndTauJetInsideAcceptance ||
        matchType == FakeTauIdentifier::kkOneProngTauToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSystematicsGenuineTauBarrel;
      } else {
        return fSystematicsGenuineTauEndcap;
      }
    } else if (matchType == FakeTauIdentifier::kkElectronToTau ||
               matchType == FakeTauIdentifier::kkElectronToTauAndTauJetInsideAcceptance ||
               matchType == FakeTauIdentifier::kkElectronFromTauDecayToTau ||
               matchType == FakeTauIdentifier::kkElectronFromTauDecayToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSystematicsFakeTauBarrelElectron;
      } else {
        return fSystematicsFakeTauEndcapElectron;
      }
    } else if (matchType == FakeTauIdentifier::kkMuonToTau ||
               matchType == FakeTauIdentifier::kkMuonToTauAndTauJetInsideAcceptance ||
               matchType == FakeTauIdentifier::kkMuonFromTauDecayToTau ||
               matchType == FakeTauIdentifier::kkMuonFromTauDecayToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSystematicsFakeTauBarrelMuon;
      } else {
        return fSystematicsFakeTauEndcapMuon;
      }
    } else if (matchType == FakeTauIdentifier::kkJetToTau ||
               matchType == FakeTauIdentifier::kkJetToTauAndTauJetInsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSystematicsFakeTauBarrelJet;
      } else {
        return fSystematicsFakeTauEndcapJet;
      }
    }
    return 0.0;
  }

}
