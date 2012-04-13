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
      fMassResolution(iConfig.getUntrackedParameter<double>("ZmassResolution")),
      //     fMassFromZll(iConfig.getUntrackedParameter<double>("ZmassFromZll")),
      fInvMassCutCount(eventCounter.addSubCounter("Jet-Tau invariant mass", "Jet-Tau invariant mass")),  
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    hTauJetMass = makeTH<TH1F>(*fs, "TauJetMass", "TauJetMass", 400, 0., 400.);
    hClosestMass = makeTH<TH1F>(*fs, "TauJetMassClosest", "TauJetMassClosest", 400, 0., 400.);
  }

  JetTauInvMass::~JetTauInvMass() {}
  
  JetTauInvMass::Data JetTauInvMass::analyze(const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<reco::Candidate>& jets ) {
    // Reset variables
    bool passEvent = false;
  
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
    passEvent = true;
    if(minMass < fMassResolution) passEvent = false;
    increment(fInvMassCutCount);

    return Data(this, passEvent);
  }
}
