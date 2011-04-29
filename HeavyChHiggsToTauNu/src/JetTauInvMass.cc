#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetTauInvMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

namespace HPlus {
  JetTauInvMass::Data::Data(const JetTauInvMass *jetTauInvMass, bool passedEvent):
    fJetTauInvMass(jetTauInvMass), fPassedEvent(passedEvent) {}
  JetTauInvMass::Data::~Data() {}
  
  JetTauInvMass::JetTauInvMass(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):    
      fMinMass(iConfig.getUntrackedParameter<double>("ZmassResolution")),
      fInvMassCutCount(eventCounter.addSubCounter("Jet-Tau invariant mass", "Jet-Tau invariant mass")),  
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    hTauJetMass = makeTH<TH1F>(*fs, "hTauJetMass", "hTauJetMass", 400, 0., 400.);
  }

  JetTauInvMass::~JetTauInvMass() {}
  
  JetTauInvMass::Data JetTauInvMass::analyze(const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets ) {
    // Reset variables
    bool passEvent = false;
  
    double minMass = 99999;
    size_t cleanPassed = 0;

    

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


	if (fabs(TauJetMass-90.3) < minMass ) {
	  minMass = fabs(TauJetMass-90.3);
	}	
      }
    }

    passEvent = true;
    if(minMass < fMinMass) passEvent = false;
    increment(fInvMassCutCount);

    return Data(this, passEvent);
  }
}
