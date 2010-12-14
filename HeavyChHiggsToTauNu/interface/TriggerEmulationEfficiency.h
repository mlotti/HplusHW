#ifndef TriggerEmulationEfficiency_h
#define TriggerEmulationEfficiency_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::XYZTLorentzVector LorentzVector;

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/L1Emulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTTauEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTPFMHTEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTNJetsEmulation.h"


class TriggerEmulationEfficiency {
    public:
	TriggerEmulationEfficiency(const edm::ParameterSet&);
	~TriggerEmulationEfficiency();

	void analyse(const edm::Event&, const edm::EventSetup&);

    private:
	L1Emulation* l1Emulation;
	HLTTauEmulation* hltTauEmulation;
	HLTMETEmulation* hltMETEmulation;
	HLTPFMHTEmulation* hltPFMHTEmulation;
	HLTNJetsEmulation* hltNJetsEmulation;

	int allEvents;
	int passedL1tau,
	    passedL1_3j,
            passedL1quad,
	    passedhlttau,
	    passedhlttau3j,
	    passedhlttau4j,
	    passedhltMet,
	    passedhltpfmht,
	    passedhlt3jets,
	    passedhlt4jets;
	int passedTauMET,
            passedTauPFMHT,
            passedTau3j,
            passedTau3jMET,
            passedTau3jPFMHT,
            passedTau4j,
            passedTau4jMET,
            passedTau4jPFMHT;
};

#endif
