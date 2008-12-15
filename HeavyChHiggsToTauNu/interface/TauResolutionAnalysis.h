#ifndef TAURESOLUTIONANALYSIS_H
#define TAURESOLUTIONANALYSIS_H

#include "FWCore/Framework/interface/Event.h"

#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"

class TauResolutionAnalysis {
  public:
  	TauResolutionAnalysis();
  	virtual ~TauResolutionAnalysis();

	bool analyse(const edm::Event&);
	void chargedTrackCounter(const edm::Event&);

  private:
        TFile* resoRootFile;

	int eventCounter;
        int mcTauCounter;
	int mcHadronicTauCounter;
	int mcVisibleTauCounter;
	int mcTauPtCutCounter;
	int caloTauCounter;
	int caloTauWithLeadingTrackCounter;
	int isolatedCaloTauCounter;
	int pfTauCounter;
	int pfTauWithLeadingTrackCounter;
	int isolatedPfTauCounter;

        TH1F* h_tauEnergyResolution;
	TH1F* h_tauDR;
        TH1F* h_tauDeta;
        TH1F* h_tauDphi;

        TH1F* h_pftauEnergyResolution;
        TH1F* h_pftauDR;
        TH1F* h_pftauDeta;
        TH1F* h_pftauDphi;
	
        TH1F* h_pfcandEnergyResolution;

	TH1F* h_mcRtau;

        TH1F* h_ntracksPfTau;
        TH1F* h_ntracksCaloTau;
        TH1F* h_ntracksPfInCaloTauCone;
        TH1F* h_ntracksPfTauMinusCaloTau;
}; 
#endif 

