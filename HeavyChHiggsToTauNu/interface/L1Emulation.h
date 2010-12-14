#ifndef L1Emulation_h
#define L1Emulation_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticleFwd.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include <vector>
typedef math::XYZTLorentzVector LorentzVector;

class L1Emulation {
    public:
	L1Emulation(const edm::ParameterSet&);
	~L1Emulation();

	void setParameters(int,double,double);
	bool passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup);
	std::vector<LorentzVector> L1Jets();

    private:
    	edm::InputTag l1tauSrc;
    	edm::InputTag l1cenSrc;

	std::vector<LorentzVector> l1jets;

	int njets;
        double l1tauPtCut;
        double l1cenPtCut;
};

#endif
