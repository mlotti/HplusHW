#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include <iostream>

class JetEnergyScaleVariation: public edm::EDProducer {
    public:
  	explicit JetEnergyScaleVariation(const edm::ParameterSet&);
  	~JetEnergyScaleVariation();

	typedef math::XYZTLorentzVector LorentzVector;

    private:

  	virtual void beginJob();
  	virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  	virtual void endJob();

	edm::InputTag jetSrc;
	edm::InputTag metSrc;
	double JESVariation;
};

JetEnergyScaleVariation::JetEnergyScaleVariation(const edm::ParameterSet& iConfig) :
	jetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
	metSrc(iConfig.getParameter<edm::InputTag>("metSrc")),
	JESVariation(iConfig.getParameter<double>("JESVariation"))
{
	produces<pat::JetCollection>();
	produces<pat::METCollection>();
}

JetEnergyScaleVariation::~JetEnergyScaleVariation() {}

void JetEnergyScaleVariation::beginJob() {
}

void JetEnergyScaleVariation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	std::auto_ptr<pat::JetCollection> rescaledJets(new pat::JetCollection);
	std::auto_ptr<pat::METCollection> rescaledMET(new pat::METCollection);

	// Jets
	edm::Handle<edm::View<pat::Jet> > hjets;
    	iEvent.getByLabel(jetSrc, hjets);
	const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());

	double dpx = 0,
	       dpy = 0;
	for(edm::PtrVector<pat::Jet>::iterator iter = jets.begin(); iter != jets.end(); ++iter) {
		edm::Ptr<pat::Jet> iJet = *iter;
		const LorentzVector& p4 = iJet->p4() * (1 + JESVariation);
		pat::Jet jet = *iJet;
		jet.setP4(p4);
		rescaledJets->push_back(jet);

		dpx = -iJet->px() * JESVariation; 
		dpy = -iJet->py() * JESVariation;
	}

	// MET
	edm::Handle<edm::View<reco::MET> > hmet;
	iEvent.getByLabel(metSrc, hmet);
	edm::Ptr<reco::MET> met = hmet->ptrAt(0);

	reco::MET scaledMet = *met;
	double newX = met->p4().Px() + dpx;
	double newY = met->p4().Py() + dpy;
	double newZ = 0;//met->p4().Pz();
	double newE = sqrt(newX*newX + newY*newY);//met->p4().E();

	const LorentzVector& p4(LorentzVector(newX,newY,newZ,newE));
	scaledMet.setP4(p4);

	rescaledMET->push_back(scaledMet);

	iEvent.put(rescaledJets);
	iEvent.put(rescaledMET);
}

void JetEnergyScaleVariation::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetEnergyScaleVariation);
