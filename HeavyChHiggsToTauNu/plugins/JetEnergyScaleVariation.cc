#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
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

	edm::InputTag tauSrc;
	edm::InputTag jetSrc;
	edm::InputTag metSrc;
	double JESVariation;
        double JESEtaVariation;
};

JetEnergyScaleVariation::JetEnergyScaleVariation(const edm::ParameterSet& iConfig) :
	tauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
	jetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
	metSrc(iConfig.getParameter<edm::InputTag>("metSrc")),
	JESVariation(iConfig.getParameter<double>("JESVariation")),
        JESEtaVariation(iConfig.getParameter<double>("JESEtaVariation"))
{
	produces<pat::TauCollection>();
	produces<pat::JetCollection>();
	produces<pat::METCollection>();
}

JetEnergyScaleVariation::~JetEnergyScaleVariation() {}

void JetEnergyScaleVariation::beginJob() {
}

void JetEnergyScaleVariation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	std::auto_ptr<pat::TauCollection> rescaledTaus(new pat::TauCollection);
	std::auto_ptr<pat::JetCollection> rescaledJets(new pat::JetCollection);
	std::auto_ptr<pat::METCollection> rescaledMET(new pat::METCollection);

	// Taus
        edm::Handle<edm::View<pat::Tau> > htaus;
        iEvent.getByLabel(tauSrc, htaus);
        const edm::PtrVector<pat::Tau>& taus(htaus->ptrVector());

        for(edm::PtrVector<pat::Tau>::iterator iter = taus.begin(); iter != taus.end(); ++iter) {
                edm::Ptr<pat::Tau> iTau = *iter;
                // Note: a tau can have mass, which must stay constant in the measurement
                // Hence only the momentum and energy are scaled
                double myM = iTau->p4().M();
                double myP = iTau->p4().P();
                // JES +- JESeta /eta
                double myChange = std::sqrt(JESVariation*JESVariation 
                  + JESEtaVariation*JESEtaVariation / iTau->eta() / iTau->eta());
                double myFactor = 1. + myChange;
                if (JESVariation < 0) myFactor = 1. - myChange;
                const LorentzVector p4(iTau->p4().X()*myFactor, iTau->p4().Y()*myFactor, iTau->p4().Z()*myFactor, std::sqrt(myM*myM + myP*myFactor*myP*myFactor)); 
                pat::Tau tau = *iTau;
                tau.setP4(p4);
                rescaledTaus->push_back(tau);
        }

	// Jets
	edm::Handle<edm::View<pat::Jet> > hjets;
    	iEvent.getByLabel(jetSrc, hjets);
	const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());

	double dpx = 0,
	       dpy = 0;
	for(edm::PtrVector<pat::Jet>::iterator iter = jets.begin(); iter != jets.end(); ++iter) {
		edm::Ptr<pat::Jet> iJet = *iter;
                // Note: a jet can have mass, which must stay constant in the measurement
                // Hence only the momentum and energy are scaled
                double myM = iJet->p4().M();
                double myP = iJet->p4().P();
                // JES +- 2%/eta
                double myChange = std::sqrt(JESVariation*JESVariation 
                  + JESEtaVariation*JESEtaVariation / iJet->eta() / iJet->eta());
                double myFactor = 1. + myChange;
                if (JESVariation < 0) myFactor = 1. - myChange;
                const LorentzVector p4(iJet->p4().X()*myFactor, iJet->p4().Y()*myFactor, iJet->p4().Z()*myFactor, std::sqrt(myM*myM + myP*myFactor*myP*myFactor)); 
		pat::Jet jet = *iJet;
		jet.setP4(p4);
		rescaledJets->push_back(jet);
                // Negative sign for MET correction comes from MET definition
		dpx += -iJet->px() * JESVariation; 
		dpy += -iJet->py() * JESVariation;
	}

	// MET
	edm::Handle<edm::View<reco::MET> > hmet;
	iEvent.getByLabel(metSrc, hmet);
	edm::Ptr<reco::MET> met = hmet->ptrAt(0);
/*
For the general case, you would basically do it in 3 steps (within a
loop over jets):
1. Add the x,y component of the jets to the x,y component of the MET:
   ME(X,Y) += JetP(X,Y)
2. Vary by X% the JES and obtain a new JetP(X,Y)
3. Then: ME(X,Y) -= JetP(X,Y)
*/
	reco::MET scaledMet = *met;
	double newX = met->p4().Px() + dpx;
	double newY = met->p4().Py() + dpy;
//double newX = met->p4().Px()*(1-JESVariation/fabs(JESVariation)*0.1); // MET scale 10%, sign from JESVariation 
//double newY = met->p4().Py()*(1-JESVariation/fabs(JESVariation)*0.1); // MET scale 10%, sign from JESVariation
	double newZ = 0;//met->p4().Pz();
	double newE = sqrt(newX*newX + newY*newY);//met->p4().E();

	const LorentzVector& p4(LorentzVector(newX,newY,newZ,newE));
	scaledMet.setP4(p4);

	rescaledMET->push_back(scaledMet);

	iEvent.put(rescaledTaus);
	iEvent.put(rescaledJets);
	iEvent.put(rescaledMET);
}

void JetEnergyScaleVariation::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetEnergyScaleVariation);
