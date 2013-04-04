#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"

namespace HPlus {
  JetTauInvMass::Data::Data():
    fPassedEvent(false) {}
  JetTauInvMass::Data::~Data() {}
  
  JetTauInvMass::JetTauInvMass(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fMassResolution(iConfig.getUntrackedParameter<double>("ZmassResolution")),
    //     fMassFromZll(iConfig.getUntrackedParameter<double>("ZmassFromZll")),
    fInvMassCutCount(eventCounter.addSubCounter("Jet-Tau invariant mass", "Jet-Tau invariant mass"))
  {
    edm::Service<TFileService> fs;
    hTauJetMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "TauJetMass", "TauJetMass", 400, 0., 400.);
    hClosestMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "TauJetMassClosest", "TauJetMassClosest", 400, 0., 400.);
  }

  JetTauInvMass::~JetTauInvMass() {}
  
  JetTauInvMass::Data JetTauInvMass::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, taus, jets);
  }

  JetTauInvMass::Data JetTauInvMass::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, taus, jets);
  }

  JetTauInvMass::Data JetTauInvMass::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets) {
    Data output;
    // Reset variables
    double minMass = 99999;
    //size_t cleanPassed = 0;
    double closestMass = -999;
    

    for(edm::PtrVector<reco::Candidate>::const_iterator iterjet = jets.begin(); iterjet != jets.end(); ++iterjet) {
      edm::Ptr<reco::Candidate> iJet = *iterjet;

      for(edm::PtrVector<reco::Candidate>::const_iterator itertau = taus.begin(); itertau != taus.end(); ++itertau) {
        edm::Ptr<reco::Candidate> iTau = *itertau;

	//      if(iJet->pt()< fPtCut) continue;
	//      if(std::abs(iJet->eta()) > fEtaCut)) continue;
	
	double TauJetMass2 = (iJet->p() + iTau->p())*(iJet->p() + iTau->p())
	  -(iJet->px() + iTau->px())*(iJet->px() + iTau->px())
	  -(iJet->py() + iTau->py())*(iJet->py() + iTau->py())
	  -(iJet->pz() + iTau->pz())*(iJet->pz() + iTau->pz());
	double TauJetMass = -999; 	  
	if ( TauJetMass2 > 0)  TauJetMass = sqrt(TauJetMass2);
	hTauJetMass->Fill(TauJetMass);


  	if (fabs(TauJetMass-91.2) < minMass ) {
	//	if (fabs(TauJetMass-fMassFromZll) < minMass ) {
	  minMass = fabs(TauJetMass-91.2);
	  //	  minMass = fabs(TauJetMass-fMassFromZll);
	  closestMass = TauJetMass; 
	}	
      }
    }
    hClosestMass->Fill(closestMass);
    if(minMass < fMassResolution) {
      output.fPassedEvent = false;
    } else {
      output.fPassedEvent = true;
      increment(fInvMassCutCount);
    }
    return output;
  }
}
