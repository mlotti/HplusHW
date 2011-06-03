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
#include "DataFormats/Math/interface/deltaR.h"

#include <iostream>
#include <algorithm>
#include <functional>

namespace {
  template<typename T>
  struct JetTauEqTraits {
    static const T& toRef(const T& obj) {
      return obj;
    }
  };

  template<typename T>
  struct JetTauEqTraits<edm::Ptr<T> > {
    static const T& toRef(const edm::Ptr<T>& ptr) {
      return *ptr;
    }
  };

  template<typename Jet, typename Tau>
  struct JetTauEq: public std::binary_function<Jet, Tau, bool> {
    explicit JetTauEq(double mc): matchingCone(mc) {}

    bool operator()(const Jet& jet, const Tau& tau) const {
      return reco::deltaR(JetTauEqTraits<Jet>::toRef(jet),
                          JetTauEqTraits<Tau>::toRef(tau)) < matchingCone;
    }

    double matchingCone;
  };
}

class JetEnergyScaleVariation: public edm::EDProducer {
    public:
  	explicit JetEnergyScaleVariation(const edm::ParameterSet&);
  	~JetEnergyScaleVariation();

	typedef math::XYZTLorentzVector LorentzVector;

    private:

  enum JetVariationMode {
    kAll,
    kOnlyTauMatching,
    kOnlyNoTauMatching
  };

  	virtual void beginJob();
  	virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  	virtual void endJob();

	edm::InputTag tauSrc;
	edm::InputTag jetSrc;
	edm::InputTag metSrc;
	double JESVariation;
        double JESEtaVariation;
        double unclusteredMETVariation;
  double tauJetMatchingDR;
  JetVariationMode jetVariationMode;
};

JetEnergyScaleVariation::JetEnergyScaleVariation(const edm::ParameterSet& iConfig) :
	tauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
	jetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
	metSrc(iConfig.getParameter<edm::InputTag>("metSrc")),
	JESVariation(iConfig.getParameter<double>("JESVariation")),
        JESEtaVariation(iConfig.getParameter<double>("JESEtaVariation")),
        unclusteredMETVariation(iConfig.getParameter<double>("unclusteredMETVariation")),
        tauJetMatchingDR(iConfig.getParameter<double>("tauJetMatchingDR"))
{
	produces<pat::TauCollection>();
	produces<pat::JetCollection>();
	produces<pat::METCollection>();
        // Check validity of provided values
        if (JESVariation < -1. || JESVariation > 1.) {
          throw cms::Exception("Configuration") << "JetEnergyScaleVariation: Invalid value for JESVariation! Please provide a value between -1..1 (value=" << JESVariation << ").";  
        }
        if (JESEtaVariation < -1. || JESEtaVariation > 1.) {
          throw cms::Exception("Configuration") << "JetEnergyScaleVariation: Invalid value for JESEtaVariation! Please provide a value between -1..1 (value=" << JESEtaVariation << ").";  
        }
        if (unclusteredMETVariation < -1. || unclusteredMETVariation > 1.) {
          throw cms::Exception("Configuration") << "JetEnergyScaleVariation: Invalid value for unclusteredMETVariation! Please provide a value between -1..1 (value=" << unclusteredMETVariation << ").";  
        }

        std::string mode = iConfig.getParameter<std::string>("jetVariationMode");
        if(mode == "all")
          jetVariationMode = kAll;
        else if(mode == "onlyTauMatching")
          jetVariationMode = kOnlyTauMatching;
        else if(mode == "onlyNoTauMatching")
          jetVariationMode = kOnlyNoTauMatching;
        else
          throw cms::Exception("Configuration") << "JetEnergyScaleVaration: Invalid value for jetVariationMode '"
                                                << mode
                                                << "', valid values are 'all', 'onlyTauMatching', 'onlyNoTauMatching'"
                                                << std::endl;
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

        LorentzVector myJetSum(0., 0., 0., 0.);
        LorentzVector myVariatedJetSum(0., 0., 0., 0.);
	for(edm::PtrVector<pat::Jet>::iterator iter = jets.begin(); iter != jets.end(); ++iter) {
		edm::Ptr<pat::Jet> iJet = *iter;
		pat::Jet jet = *iJet;

                bool variateJet = true;
                if(jetVariationMode != kAll) {
                  bool jetTauMatch = std::find_if(taus.begin(), taus.end(),
                                                  std::bind1st(JetTauEq<pat::Jet, edm::Ptr<pat::Tau> >(tauJetMatchingDR), *iJet)) != taus.end();
                  if(jetVariationMode == kOnlyTauMatching)
                    variateJet = jetTauMatch;
                  else if(jetVariationMode == kOnlyNoTauMatching)
                    variateJet = !jetTauMatch;
                }

                if(variateJet) {
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
                  jet.setP4(p4);
                }
		rescaledJets->push_back(jet);
                // Negative sign for MET correction comes from MET definition
                myJetSum -= iJet->p4();
                myVariatedJetSum -= jet.p4();
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
/*	double newX = met->p4().Px() + dpx;
	double newY = met->p4().Py() + dpy;
*/
       
// Substract jet component from MET to obtain the unclustered MET
        LorentzVector myVariatedMET = met->p4();
        myVariatedMET -= myJetSum;
// Variate the unclustered MET
        myVariatedMET*= (1. + unclusteredMETVariation);
// Then add the variated jet component
        myVariatedMET += myVariatedJetSum;
        myVariatedMET.SetPz(0.);
        myVariatedMET.SetE(std::sqrt(myVariatedMET.Perp2()));

// Set new MET value
	const LorentzVector& p4(myVariatedMET);
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
