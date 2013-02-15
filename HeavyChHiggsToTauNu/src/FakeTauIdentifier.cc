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
  
  FakeTauIdentifier::FakeTauIdentifier(const edm::ParameterSet& iConfig, HPlus::HistoWrapper& histoWrapper, std::string label):
    fVisibleMCTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("visibleMCTauSrc")),
    fVisibleMCTauOneProngSrc(iConfig.getUntrackedParameter<edm::InputTag>("visibleMCTauOneProngSrc")),
    fMatchingConditionDeltaR(iConfig.getUntrackedParameter<double>("matchingConditionDeltaR")),
    fSFFakeTauBarrelElectron(iConfig.getUntrackedParameter<double>("scalefactorFakeTauBarrelElectron")),
    fSFFakeTauEndcapElectron(iConfig.getUntrackedParameter<double>("scalefactorFakeTauEndcapElectron")),
    fSFFakeTauBarrelMuon(iConfig.getUntrackedParameter<double>("scalefactorFakeTauBarrelMuon")),
    fSFFakeTauEndcapMuon(iConfig.getUntrackedParameter<double>("scalefactorFakeTauEndcapMuon")),
    fSFFakeTauBarrelJet(iConfig.getUntrackedParameter<double>("scalefactorFakeTauBarrelJet")),
    fSFFakeTauEndcapJet(iConfig.getUntrackedParameter<double>("scalefactorFakeTauEndcapJet")),
    fSystematicsFakeTauBarrelElectron(iConfig.getUntrackedParameter<double>("systematicsFakeTauBarrelElectron")),
    fSystematicsFakeTauEndcapElectron(iConfig.getUntrackedParameter<double>("systematicsFakeTauEndcapElectron")),
    fSystematicsFakeTauBarrelMuon(iConfig.getUntrackedParameter<double>("systematicsFakeTauBarrelMuon")),
    fSystematicsFakeTauEndcapMuon(iConfig.getUntrackedParameter<double>("systematicsFakeTauEndcapMuon")),
    fSystematicsFakeTauBarrelJet(iConfig.getUntrackedParameter<double>("systematicsFakeTauBarrelJet")),
    fSystematicsFakeTauEndcapJet(iConfig.getUntrackedParameter<double>("systematicsFakeTauEndcapJet"))
  {
    edm::Service<TFileService> fs;
    // Create histograms
    TFileDirectory myDir = fs->mkdir("FakeTauIdentifier_"+label);

    //    hTauMatchType = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TauMatchType", "TauMatchType", 13, 0, 13);
    hTauMatchType = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TauMatchType", "TauMatchType", kkNumberOfSelectedTauMatchTypes, 0, kkNumberOfSelectedTauMatchTypes);

    if (hTauMatchType->isActive()) {
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkNoMC, "NoMatch");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronToTau, "e#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronFromTauDecayToTau, "tau#rightarrowe#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonToTau, "#mu#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonFromTauDecayToTau, "tau#rightarrow#mu#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkTauToTau, "genuine hadr. #tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkOneProngTauToTau, "genuine 1-pr. hadr. #tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkJetToTau, "jet#rightarrow#tau");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronToTauAndTauOutsideAcceptance, "e#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkElectronFromTauDecayToTauAndTauOutsideAcceptance, "#tau#rightarrowe#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonToTauAndTauOutsideAcceptance, "#mu#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkMuonFromTauDecayToTauAndTauOutsideAcceptance, "#tau#rightarrow#mu#rightarrow#tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkTauToTauAndTauOutsideAcceptance, "genuine hadr. #tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkOneProngTauToTauAndTauOutsideAcceptance, "genuine 1-pr. hadr. #tau, #tau outside");
      hTauMatchType->GetXaxis()->SetBinLabel(1+kkJetToTauAndTauOutsideAcceptance, "jet#rightarrow#tau, #tau outside");
    }
    hTauOrigin = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TauOrigin", "TauOrigin", 7, 0, 7);
    if (hTauOrigin->isActive()) {
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tau#tau");
      hTauOrigin->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
    }
    hMuOrigin = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "MuOrigin", "MuOrigin", 7, 0, 7);
    if (hMuOrigin->isActive()) {
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tautau");
      hMuOrigin->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
    }
    hElectronOrigin = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "ElectronOrigin", "ElectronOrigin", 7, 0, 7);
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

    bool foundMCTauOutsideAcceptanceStatus = false;
    bool isHadronicTau = false;
    bool isOneProngMCTau = false;
    bool isMCElectron = false;
    bool isMCMuon = false;
    bool isLeptonicTauDecay = false;
    size_t myTauIndex = 0;
    size_t myElectronIndex = 0;
    size_t myMuIndex = 0;

    // Check matching to visible MC taus
    edm::Handle <std::vector<LorentzVector> > myMCVisibleTaus;
    iEvent.getByLabel(fVisibleMCTauSrc, myMCVisibleTaus);
    // Check matching to MC visible taus
    double tmpPt = 0;
    for (std::vector<LorentzVector>::const_iterator it = myMCVisibleTaus->begin(); it != myMCVisibleTaus->end(); ++it) {
      if (reco::deltaR((*it), tau.p4()) < fMatchingConditionDeltaR) {
        // Match found
        isHadronicTau = true;
        tmpPt = (*it).pt();
      }
      // Check if a MC tau is outside acceptance
      if ((*it).pt() < 41 || abs((*it).eta()) > 2.1)
        foundMCTauOutsideAcceptanceStatus = true;
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
    // Load list of genParticles and look for matching with MC electrons or MC muons
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    //std::cout << "matchfinding:" << std::endl;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13) {
        // Check match with tau
        if (reco::deltaR(p.p4(), tau.p4()) < fMatchingConditionDeltaR) {
          if (p.pt() > 10.) {
            //std::cout << "  match found, pid=" << p.pdgId() << " eta=" << std::abs(p.eta()) << " pt=" << p.pt() << std::endl;
            if (std::abs(p.pdgId()) == 11) {
              isMCElectron = true;
              myElectronIndex = i;
            } else if (std::abs(p.pdgId()) == 13) {
              isMCMuon = true;
              myMuIndex = i;
            }
          }
        }
      }
    }
    // Find MC tau lepton index corresponding to the MC visible tau
    if (isHadronicTau) {
      //std::cout << "start" << std::endl;
      for (size_t i=0; i < genParticles->size(); ++i) {
        const reco::Candidate & p = (*genParticles)[i];
        if (std::abs(p.pdgId()) == 15) {
          // Ignore tau that is radiating before decay
          bool myVetoStatus = false;
          for (size_t im=0; im < p.numberOfDaughters(); ++im){
            if (std::abs(p.daughter(im)->pdgId()) == 15) myVetoStatus = true;
          }
          if (myVetoStatus) continue;
          // Tau lepton found
          LorentzVector myVisibleTau;
          // Subtract neutrino momenta from tau lepton momentum
          for (size_t j=0; j < genParticles->size(); ++j) {
            // Consider only stable particles
            if ((*genParticles)[j].status() != 1) continue;
            // Skip neutrinos
            int myId = std::abs((*genParticles)[j].pdgId());
            if (myId == 12 || myId == 14 || myId == 16) continue;
            // Check if particles mother is the tau lepton on row i
            const reco::Candidate* ppmother = (*genParticles)[j].mother();
            bool myBelongsToTauStatus = false;
            while (ppmother) {
              if (ppmother->p4() == p.p4() && ppmother->pdgId() == p.pdgId()) {
                myBelongsToTauStatus = true;
              }
              // move to next
              ppmother = ppmother->mother();
            }
            if (myBelongsToTauStatus) {
              //std::cout << "   add " << (*genParticles)[j].pdgId() << " status=" << (*genParticles)[j].status() << std::endl;
              myVisibleTau += (*genParticles)[j].p4();
            }
          }
          if (reco::deltaR(myVisibleTau, tau.p4()) < fMatchingConditionDeltaR) {
            myTauIndex = i;
          }
          //std::cout <<" is tau, idx=" << myTauIndex << ", pt=" << tau.pt() << " vs. " << myVisibleTau.pt() << " vs. " << " vs. " << tmpPt << std::endl;
        }
      }
    }
    // If an electron or muon was matched, look if it comes from a tau decay
    if (isMCElectron || isMCMuon) {
      size_t myIndex = myMuIndex;
      if (isMCElectron) {
        myIndex = myElectronIndex;
      }
      const reco::Candidate* p = (*genParticles)[myIndex].mother();
      while (p) {
        if (std::abs(p->pdgId()) == 15)
          isLeptonicTauDecay = true;
        // move to next
        p = p->mother();
      }
    }
    // Set result
    if (!foundMCTauOutsideAcceptanceStatus) {
      if (isMCElectron) {
        if (isLeptonicTauDecay) {
          output.fTauMatchType = kkElectronFromTauDecayToTau;
        } else {
          output.fTauMatchType = kkElectronToTau;
        }
      } else if (isMCMuon) {
        if (isLeptonicTauDecay) {
          output.fTauMatchType = kkMuonFromTauDecayToTau;
        } else {
          output.fTauMatchType = kkMuonToTau;
        }
      } else if (isHadronicTau) {
        output.fTauMatchType = kkTauToTau;
        if (isOneProngMCTau) {
          output.fTauMatchType = kkOneProngTauToTau;
        }
      } else {
        output.fTauMatchType = kkJetToTau;
      }
    } else {
      if (isMCElectron) {
        if (isLeptonicTauDecay) {
          output.fTauMatchType = kkElectronFromTauDecayToTauAndTauOutsideAcceptance;
        } else {
          output.fTauMatchType = kkElectronToTauAndTauOutsideAcceptance;
        }
      } else if (isMCMuon) {
        if (isLeptonicTauDecay) {
          output.fTauMatchType = kkMuonFromTauDecayToTauAndTauOutsideAcceptance;
        } else {
          output.fTauMatchType = kkMuonToTauAndTauOutsideAcceptance;
        }
      } else if (isHadronicTau) {
        output.fTauMatchType = kkTauToTauAndTauOutsideAcceptance;
        if (isOneProngMCTau) {
          output.fTauMatchType = kkOneProngTauToTauAndTauOutsideAcceptance;
        }
      } else {
        output.fTauMatchType = kkJetToTauAndTauOutsideAcceptance;
      }
    }
    // Look at ancestor information
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
      if (output.fTauMatchType == kkOneProngTauToTauAndTauOutsideAcceptance) hTauMatchType->Fill(kkTauToTauAndTauOutsideAcceptance);
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
    if (matchType == FakeTauIdentifier::kkElectronToTau || matchType == FakeTauIdentifier::kkElectronToTauAndTauOutsideAcceptance ||
        matchType == FakeTauIdentifier::kkElectronFromTauDecayToTau || matchType == FakeTauIdentifier::kkElectronFromTauDecayToTauAndTauOutsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSFFakeTauBarrelElectron;
      } else {
        return fSFFakeTauEndcapElectron;
      }
    } else if (matchType == FakeTauIdentifier::kkMuonToTau || matchType == FakeTauIdentifier::kkMuonToTauAndTauOutsideAcceptance ||
               matchType == FakeTauIdentifier::kkMuonFromTauDecayToTau || matchType == FakeTauIdentifier::kkMuonFromTauDecayToTauAndTauOutsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSFFakeTauBarrelMuon;
      } else {
        return fSFFakeTauEndcapMuon;
      }
    } else if (matchType == FakeTauIdentifier::kkJetToTau || matchType == FakeTauIdentifier::kkJetToTauAndTauOutsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSFFakeTauBarrelJet;
      } else {
        return fSFFakeTauEndcapJet;
      }
    }
    return 1.0;
  }

  double FakeTauIdentifier::getFakeTauSystematics(MCSelectedTauMatchType matchType, double eta) {
    if (matchType == FakeTauIdentifier::kkElectronToTau || matchType == FakeTauIdentifier::kkElectronToTauAndTauOutsideAcceptance ||
        matchType == FakeTauIdentifier::kkElectronFromTauDecayToTau || matchType == FakeTauIdentifier::kkElectronFromTauDecayToTauAndTauOutsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSystematicsFakeTauBarrelElectron;
      } else {
        return fSystematicsFakeTauEndcapElectron;
      }
    } else if (matchType == FakeTauIdentifier::kkMuonToTau || matchType == FakeTauIdentifier::kkMuonToTauAndTauOutsideAcceptance ||
               matchType == FakeTauIdentifier::kkMuonFromTauDecayToTau || matchType == FakeTauIdentifier::kkMuonFromTauDecayToTauAndTauOutsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSystematicsFakeTauBarrelMuon;
      } else {
        return fSystematicsFakeTauEndcapMuon;
      }
    } else if (matchType == FakeTauIdentifier::kkJetToTau || matchType == FakeTauIdentifier::kkJetToTauAndTauOutsideAcceptance) {
      if (std::fabs(eta) < 1.5) {
        return fSystematicsFakeTauBarrelJet;
      } else {
        return fSystematicsFakeTauEndcapJet;
      }
    }
    return 0.0;
  }

}
