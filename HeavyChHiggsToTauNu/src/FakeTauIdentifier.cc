#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeTauIdentifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  
  FakeTauIdentifier::FakeTauIdentifier(HPlus::HistoWrapper& histoWrapper, std::string label) {
    edm::Service<TFileService> fs;
    // Create histograms
    TFileDirectory myDir = fs->mkdir("FakeTauIdentifier_"+label);
    hTauMatchType = histoWrapper->makeTH<TH1F>(HistoWrapper::kVital, myDir, "TauMatchType", "TauMatchType", 9, 0, 9);
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkNoMC, "NoMatch");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkElectronToTau, "e#rightarrow#tau");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkMuonToTau, "#mu#rightarrow#tau");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkTauToTau, "genuine #tau");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkJetToTau, "jet#rightarrow#tau");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkElectronToTauAndTauOutsideAcceptance, "e#rightarrow#tau, #tau outside");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkMuonToTauAndTauOutsideAcceptance, "#mu#rightarrow#tau, #tau outside");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkTauToTauAndTauOutsideAcceptance, "genuine #tau, #tau outside");
    hTauMatchType->getHisto->GetXaxis()->SetBinLabel(1+kkJetToTauAndTauOutsideAcceptance, "jet#rightarrow#tau, #tau outside");
    hTauOrigin = histoWrapper->makeTH<TH1F>(HistoWrapper::kVital, myDir, "TauOrigin", "TauOrigin", 7, 0, 7);
    hTauOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
    hTauOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
    hTauOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
    hTauOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
    hTauOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
    hTauOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tautau");
    hTauOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
    hMuOrigin = histoWrapper->makeTH<TH1F>(HistoWrapper::kVital, myDir, "MuOrigin", "MuOrigin", 7, 0, 7);
    hMuOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
    hMuOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
    hMuOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
    hMuOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
    hMuOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
    hMuOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tautau");
    hMuOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
    hElectronOrigin = histoWrapper->makeTH<TH1F>(HistoWrapper::kVital, myDir, "ElectronOrigin", "ElectronOrigin", 7, 0, 7);
    hElectronOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkUnknownOrigin, "unknown");
    hElectronOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromW, "from W");
    hElectronOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromZ, "from Z");
    hElectronOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromHplus, "from H+");
    hElectronOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromWTau, "from W#rightarrow#tau");
    hElectronOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromZTauTau, "from Z#rightarrow#tautau");
    hElectronOrigin->getHisto->GetXaxis()->SetBinLabel(1+kkFromHplusTau, "from H+#rightarrow#tau");
  }
  
  FakeTauIdentifier::~FakeTauIdentifier() {
    
  }
  
  FakeTauIdentifier::MCSelectedTauMatchType FakeTauIdentifier::matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau) {
    FakeTauIdentifier::MCSelectedTauMatchType myMatchType = kkNoMC;
    if (iEvent.isRealData()) return kkNoMC;
    bool foundMCTauOutsideAcceptanceStatus = false;
    bool isMCTau = false;
    bool isMCElectron = false;
    bool isMCMuon = false;
    size_t myTauIndex = 0;
    size_t myElectronIndex = 0;
    size_t myMuIndex = 0;

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    //std::cout << "matchfinding:" << std::endl;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13 || std::abs(p.pdgId()) == 15) {
        // Check match with tau
        if (reco::deltaR(p, tau.p4()) < 0.1) {
          if (p.pt() > 10.) {
            //std::cout << "  match found, pid=" << p.pdgId() << " eta=" << std::abs(p.eta()) << " pt=" << p.pt() << std::endl;
            if (std::abs(p.pdgId()) == 15) {
              isMCTau = true;
              myTauIndex = i;
            } else if (std::abs(p.pdgId()) == 11) {
              isMCElectron = true;
              myElectronIndex = i;
            } else if (std::abs(p.pdgId()) == 13) {
              isMCMuon = true;
              myMuIndex = i;
            }
          }
        }
        // Check if there is a tau outside the acceptance in the event
        if (!foundMCTauOutsideAcceptanceStatus && std::abs(p.pdgId()) == 15) {
          if (p.pt() < 40 || abs(p.eta()) > 2.1)
            foundMCTauOutsideAcceptanceStatus = true;
        }
      }
    }
    if (!foundMCTauOutsideAcceptanceStatus) {
      if (isMCElectron) myMatchType = kkElectronToTau;
      else if (isMCMuon) myMatchType = kkMuonToTau;
      else if (isMCTau) myMatchType = kkTauToTau;
      else myMatchType = kkJetToTau;
    } else {
      if (isMCElectron) myMatchType = kkElectronToTauAndTauOutsideAcceptance;
      else if (isMCMuon) myMatchType = kkMuonToTauAndTauOutsideAcceptance;
      else if (isMCTau) myMatchType = kkTauToTauAndTauOutsideAcceptance;
      else myMatchType = kkJetToTauAndTauOutsideAcceptance;
    }
    // Look at ancestor information
    MCSelectedTauOriginType myOriginType = kkUnknownOrigin;
    if (myMatchType != kkJetToTau) {
      size_t myIndex = 0;
      if (isMCElectron)
        myIndex = myElectronIndex;
      else if (isMCMuon)
        myIndex = myMuIndex;
      else if (isMCTau)
        myIndex = myTauIndex;
      bool myWStatus = false;
      bool myZStatus = false;
      bool myHPlusStatus = false;
      bool myTauStatus = false;
      //reco::Candidate* p = const_cast<reco::Candidate*>((*genParticles)[myIndex].mother());
      const reco::Candidate* p = (*genParticles)[myIndex].mother();
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
      }
      if (!myTauStatus) {
        if (myWStatus) myOriginType = kkFromW;
        else if (myZStatus) myOriginType = kkFromZ;
        else if (myHPlusStatus) myOriginType = kkFromHplus;
      } else {
        if (myWStatus) myOriginType = kkFromWTau;
        else if (myZStatus) myOriginType = kkFromZTauTau;
        else if (myHPlusStatus) myOriginType = kkFromHplusTau; 
      }
    }
    
    // fill histograms
    hTauMatchType->Fill(myMatchType);
    if (isMCElectron)
      hElectronOrigin->Fill(myOriginType);
    else if (isMCMuon)
      hMuOrigin->Fill(myOriginType);
    else if (isMCTau)
      hTauOrigin->Fill(myOriginType);
    
    return myMatchType;
  }
  
}
