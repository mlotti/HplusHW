#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelectionFactorized.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TH1F.h"
#include "TH1I.h"
#include "TH2F.h"

namespace HPlus {
  TauSelectionFactorized::Data::Data(const TauSelectionFactorized *TauSelectionFactorized, bool passedEvent, const TauSelection::Data tauSelectionData):
    fTauSelectionFactorized(TauSelectionFactorized), fPassedEvent(passedEvent), fTauSelectionData(tauSelectionData) {}
  TauSelectionFactorized::Data::~Data() {}

  TauSelectionFactorized::TauSelectionFactorized(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, TauSelection& tauSelectionObject):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fPtCutCount(eventCounter.addSubCounter("Factorized Tau","tau pt cut")),
    fEtaCutCount(eventCounter.addSubCounter("Factorized Tau","tau eta cut")),
    fTauFoundCount(eventCounter.addSubCounter("Factorized Tau","tau found")),
    fEventWeight(eventWeight),
    fTauSelection(tauSelectionObject)
  {
    edm::Service<TFileService> fs;
    hPtSelectedTaus = fs->make<TH1F>("factorized_tau_pt", "tau_pt", 100, 0., 200.);
    hEtaSelectedTaus = fs->make<TH1F>("factorized_tau_eta", "tau_eta", 60, -3., 3.);
    hPtBeforeTauID = fs->make<TH1F>("factorization_calculation_pt_before_tauID", "tau_pt;#tau jet p_{T}, GeV/c;N", 20, 0., 200.);
    hPtAfterTauID = fs->make<TH1F>("factorization_calculation_pt_after_tauID", "tau_pt;#tau jet p_{T}, GeV/c;N", 20, 0., 200.);
    hEtaBeforeTauID = fs->make<TH1F>("factorization_calculation_eta_before_tauID", "tau_eta;#tau jet #eta;N", 60, -3., 3.);
    hEtaAfterTauID = fs->make<TH1F>("factorization_calculation_eta_after_tauID", "tau_eta;#tau jet #eta;N", 60, -3., 3.);
    hPtVsEtaBeforeTauID = fs->make<TH2F>("factorization_calculation_pt_vs_eta_before_tauID", "tau_pt_vs_eta;#tau jet p_{T}, GeV/c;#tau jet #eta", 20, 0., 200., 60, -3., 3.);
    hPtVsEtaAfterTauID = fs->make<TH2F>("factorization_calculation_pt_vs_eta_after_tauID", "tau_pt_vs_eta;#tau jet p_{T}, GeV/c;#tau jet #eta", 20, 0., 200., 60, -3., 3.);

    hCategory = fs->make<TH1F>("factorized_tau_category", "factorized_tau_category", 5, 0, 5);
    hCategory->GetXaxis()->SetBinLabel(1, "All events");
    hCategory->GetXaxis()->SetBinLabel(2, "No trigger matched taus");
    hCategory->GetXaxis()->SetBinLabel(3, "Only one trg matched tau");
    hCategory->GetXaxis()->SetBinLabel(4, "Highest tau that passed tauID");
    hCategory->GetXaxis()->SetBinLabel(5, "No tau after tauID; tau=highest trg match");
  }

  TauSelectionFactorized::~TauSelectionFactorized() {}

  TauSelectionFactorized::Data TauSelectionFactorized::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Reset variables
    bool passEvent = false;
    fFactorization = 1.0;
    fSelectedTau = edm::Ptr<pat::Tau>(); // initializes the tau with a zero pointer

    // Get tau collection
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);

    // Apply jet ET and eta cuts
    edm::PtrVector<pat::Tau> myFilteredTaus;
    const edm::PtrVector<pat::Tau>& myTaus(htaus->ptrVector());
    for(edm::PtrVector<pat::Tau>::const_iterator iter = myTaus.begin(); iter != myTaus.end(); ++iter) {
      edm::Ptr<pat::Tau> iTau = *iter;
      // Apply jet ET cut
      if(!(iTau->pt() > fPtCut)) continue;
      increment(fPtCutCount);
      // Apply jet eta cut 
      if(!(std::abs(iTau->eta()) < fEtaCut)) continue;
      increment(fEtaCutCount);
      // Store passed taus
      myFilteredTaus.push_back(iTau);
    }

    // Calculate tau ID to obtain factorization coefficients (for lookup table determination and/or cross-checking)
    TauSelection::Data myTauSelectionData = evaluateFactorizationCoefficients(iEvent, iSetup, myFilteredTaus);

    // Check if there are entries in the tau collection
    hCategory->Fill(0.0, fEventWeight.getWeight());
    if (!myFilteredTaus.size()) {
      hCategory->Fill(1.0, fEventWeight.getWeight());
      passEvent = false;
    } else {
      if (myFilteredTaus.size() == 1) {
        // Only one tau in the tau collection: take as tau the only tau object
        fSelectedTau = myFilteredTaus[0];
        hCategory->Fill(2.0, fEventWeight.getWeight());
      } else {
        // More than one tau exists in the tau collection
        // Strategy: apply tauID and see if any of the candidates pass
        passEvent = true;
        if (myTauSelectionData.passedEvent()) {
          // At least one tau object has passed tauID, take as tau the tau object with highest ET
          fSelectedTau = myTauSelectionData.getSelectedTaus()[0];
          hCategory->Fill(3.0, fEventWeight.getWeight());
        } else {
          // No tau objects have passed the tauID, take as tau the tau object with the highest ET
          fSelectedTau = myFilteredTaus[0];
          hCategory->Fill(4.0, fEventWeight.getWeight());
        }
      }
    }
    // Fill histograms for selected tau
    if (!fSelectedTau.isNull()) {
      hPtSelectedTaus->Fill(fSelectedTau->pt(), fEventWeight.getWeight());
      hEtaSelectedTaus->Fill(fSelectedTau->eta(), fEventWeight.getWeight());
      increment(fTauFoundCount);
    }
    // Obtain factorization constant from lookup table
    // FIXME: to be implemented

    return Data(this, passEvent, fTauSelection.setSelectedTau(fSelectedTau, passEvent));
  }
  
  TauSelection::Data TauSelectionFactorized::evaluateFactorizationCoefficients(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus) {
    // Loop over the before tau candidates before tauID
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      edm::Ptr<pat::Tau> iTau = *iter;
      hPtBeforeTauID->Fill(iTau->pt(), fEventWeight.getWeight());
      hEtaBeforeTauID->Fill(iTau->eta(), fEventWeight.getWeight());
      hPtVsEtaBeforeTauID->Fill(iTau->pt(), iTau->eta(), fEventWeight.getWeight());
    }
    // Do tau ID
    TauSelection::Data myTauSelectionData = fTauSelection.analyze(iEvent, iSetup, taus);
    
    // Loop over the taus that have passed tauID
    edm::PtrVector<pat::Tau> myPassedTaus = myTauSelectionData.getSelectedTaus();
    for(edm::PtrVector<pat::Tau>::const_iterator iter = myPassedTaus.begin(); iter != myPassedTaus.end(); ++iter) {
      edm::Ptr<pat::Tau> iTau = *iter;
      hPtAfterTauID->Fill(iTau->pt(), fEventWeight.getWeight());
      hEtaAfterTauID->Fill(iTau->eta(), fEventWeight.getWeight());
      hPtVsEtaAfterTauID->Fill(iTau->pt(), iTau->eta(), fEventWeight.getWeight());
    }

    // Return the tau selection data
    return myTauSelectionData;
  }
}
