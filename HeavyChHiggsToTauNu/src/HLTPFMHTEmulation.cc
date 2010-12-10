#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTPFMHTEmulation.h"

HLTPFMHTEmulation::HLTPFMHTEmulation(const edm::ParameterSet& iConfig) :
    jetSrc(iConfig.getParameter<edm::InputTag>("jetSrc"))
{}

HLTPFMHTEmulation::~HLTPFMHTEmulation(){}

void HLTPFMHTEmulation::setParameters(double theCut){
	mhtCut = theCut;
}

bool HLTPFMHTEmulation::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup){
        edm::Handle<edm::View<reco::PFJet> > hjets;
        iEvent.getByLabel(jetSrc, hjets);

	edm::PtrVector<reco::PFJet> jets = hjets->ptrVector();

	double hx = 0,
               hy = 0;

        for(edm::PtrVector<reco::PFJet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
                edm::Ptr<reco::PFJet> iJet = *iter;
		hx += iJet->px();
		hy += iJet->py();
	}

	double ht = sqrt(hx*hx + hy*hy);
        return ht > mhtCut;
}
