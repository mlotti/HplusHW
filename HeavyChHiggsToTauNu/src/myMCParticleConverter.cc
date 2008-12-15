#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyMCParticle MyEventConverter::myMCParticleConverter(const GenJet& genJet){
	MyMCParticle mcJet(genJet.px(),genJet.py(),genJet.pz(),genJet.energy());
	mcJet.pid = 0; //= genJet.pdgId();
	mcJet.status = 4;
	return mcJet;
}
