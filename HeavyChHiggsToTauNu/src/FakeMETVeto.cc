#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  FakeMETVeto::Data::Data():
    fPassedEvent(false),
    fClosestDeltaPhi(999),
    fClosestDeltaPhiToJets(999),
    fClosestDeltaPhiToTaus(999) { }

  FakeMETVeto::Data::~Data() {}
  
  FakeMETVeto::FakeMETVeto(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fMinDeltaPhi(iConfig.getUntrackedParameter<double>("minDeltaPhi")) {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FakeMETVeto");
    
    hClosestDeltaPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Closest_DeltaPhi_of_MET_and_selected_jets_or_taus", "min DeltaPhi(MET,selected jets or taus);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    hClosestDeltaPhiToJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Closest_DeltaPhi_of_MET_and_selected_jets", "min DeltaPhi(MET,selected jets);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    hClosestDeltaPhiToTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Closest_DeltaPhi_of_MET_and_taus", "min DeltaPhi(MET,selected taus);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    
    hClosestDeltaPhiZoom = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Closest_DeltaPhi_of_MET_and_selected_jets_or_taus_Zoom", "min DeltaPhi(MET,selected jets or taus);min(#Delta#phi(MET,jets)), degrees;N / 2", 25, 0., 50.0);
    hClosestDeltaPhiToJetsZoom = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Closest_DeltaPhi_of_MET_and_selected_jets_Zoom", "min DeltaPhi(MET,selected jets);min(#Delta#phi(MET,jets)), degrees;N / 2", 25, 0., 50.0);
    hClosestDeltaPhiToTausZoom = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Closest_DeltaPhi_of_MET_and_taus_Zoom", "min DeltaPhi(MET,selected taus);min(#Delta#phi(MET,jets)), degrees;N / 2", 25, 0., 50.0);
  }

  FakeMETVeto::~FakeMETVeto() {}

  FakeMETVeto::Data FakeMETVeto::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau , const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, tau, jets, met);
  }

  FakeMETVeto::Data FakeMETVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau , const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, tau, jets, met);
  }

  FakeMETVeto::Data FakeMETVeto::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& tau , const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
    Data output;

    // Loop over selected taus
    //    for(edm::PtrVector<reco::Candidate>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
    output.fClosestDeltaPhiToTaus  = reco::deltaPhi(*met, *tau ) * 180./3.14159;
      //      if ( fabs(myDeltaPhi) < output.fClosestDeltaPhiToTaus)
      //        output.fClosestDeltaPhiToTaus = fabs(myDeltaPhi);
   
    hClosestDeltaPhiToTaus->Fill(output.fClosestDeltaPhiToTaus);
    hClosestDeltaPhiToTausZoom->Fill(output.fClosestDeltaPhiToTaus);
    
    // Loop over selected jets
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      double myDeltaPhi = reco::deltaPhi(*met, **iter) * 180./3.14159;
      if ( fabs(myDeltaPhi) < output.fClosestDeltaPhiToJets)
        output.fClosestDeltaPhiToJets = fabs(myDeltaPhi);
    }
    hClosestDeltaPhiToJets->Fill(output.fClosestDeltaPhiToJets);
    hClosestDeltaPhiToJetsZoom->Fill(output.fClosestDeltaPhiToJets);

    // Combine results - for now take just DeltaPhi(MET,jet) into account 
    //if (output.fClosestDeltaPhiToJets < output.fClosestDeltaPhiToTaus) {
    output.fClosestDeltaPhi = output.fClosestDeltaPhiToJets;
    //} else {
    //  output.fClosestDeltaPhi = output.fClosestDeltaPhiToTaus;
    //}

    // New: Don't combine results. Take deltaPhi(MET, jets)
    output.fClosestDeltaPhi = output.fClosestDeltaPhiToJets;
    hClosestDeltaPhi->Fill(output.fClosestDeltaPhi);
    hClosestDeltaPhiZoom->Fill(output.fClosestDeltaPhi);

    // Make cut
    output.fPassedEvent = !(output.fClosestDeltaPhi < fMinDeltaPhi);

    return output;
  }
}
