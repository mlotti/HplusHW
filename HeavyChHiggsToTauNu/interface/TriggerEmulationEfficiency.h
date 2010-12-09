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

	int allEvents,l1tau,l1quad,hltTau,hltMet,hltpfmht,hlt3jets,hlt4jets;
};

#endif
