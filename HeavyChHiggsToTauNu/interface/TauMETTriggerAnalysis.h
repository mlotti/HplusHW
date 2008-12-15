#ifndef TAUMETRIGGERANALYSIS_H
#define TAUMETRIGGERANALYSIS_H

#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/L1Trigger/interface/L1ParticleMap.h"
using namespace l1extra;

#include "TLorentzVector.h"
#include <vector>

using namespace std;

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyRootTree.h"
#include "TFile.h"
#include "TH1F.h"

class TauMETTriggerAnalysis {
  public:
  	TauMETTriggerAnalysis();
        TauMETTriggerAnalysis(MyRootTree*);
  	virtual ~TauMETTriggerAnalysis();

	bool analyse(const edm::Event&);
        TH1F* triggerInfo();

  private:
        void init();
	bool genuineTau(math::XYZTLorentzVector);
	bool L1(const edm::Event&);
        bool L2MET(const edm::Event&);
        bool L2reco(const edm::Event&);
        bool L2ecalIso(const edm::Event&);
        bool L25(const edm::Event&);
        bool L3(const edm::Event&);

	void mcAnalysis(const edm::Event&);
	vector<TLorentzVector> visible_taus;

	int allEvents,
            l1Events,
            l1EventsTrue,
            l1EventsFalse,
	    metEvents,
	    metEventsTrue,
	    l2EventsReco,
            l2EventsRecoTrue,
            l2EventsRecoFalse,
            l2EventsEcalIso,
            l2EventsEcalIsoTrue,
            l2EventsEcalIsoFalse,
            l25Events,
            l25EventsTrue,
            l25EventsFalse,
            l3Events,
            l3EventsTrue,
            l3EventsFalse;

	L1JetParticleVectorRef L1jets;

	bool l1truetau;
        MyRootTree* userRootTree;
        TFile* 	taumetRootFile;
	TH1F*  	h_L1TauEt;
	TH1F*	h_MET;
	TH1F*	h_L3TauEt;

}; 
#endif 

