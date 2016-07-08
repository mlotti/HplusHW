#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTPFMHTEmulation.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

HLTPFMHTEmulation::HLTPFMHTEmulation(const edm::ParameterSet& iConfig) :
    pfjetSrc(iConfig.getParameter<edm::InputTag>("pfjetSrc"))
{}

HLTPFMHTEmulation::~HLTPFMHTEmulation(){}

void HLTPFMHTEmulation::setParameters(double theCut){
	mhtCut = theCut;
}

bool HLTPFMHTEmulation::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup){
//        edm::Handle<edm::View<reco::PFJet> > hjets;
	edm::Handle<edm::View<pat::Jet> > hjets;
        iEvent.getByLabel(pfjetSrc, hjets);

//	edm::PtrVector<reco::PFJet> jets = hjets->ptrVector();
	edm::PtrVector<pat::Jet> jets = hjets->ptrVector();

	double hx = 0,
               hy = 0;

//        for(edm::PtrVector<reco::PFJet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
//                edm::Ptr<reco::PFJet> iJet = *iter;
	for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
		edm::Ptr<pat::Jet> iJet = *iter;
		hx += iJet->px();
		hy += iJet->py();
	}

	double ht = sqrt(hx*hx + hy*hy);
        return ht > mhtCut;
}
