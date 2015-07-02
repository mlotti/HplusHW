#ifndef GenParticleDumper_h
#define GenParticleDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "TLorentzVector.h"

#include "DataFormats/Math/interface/LorentzVector.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"

class GenParticleDumper : public BaseDumper {
   public:
    // tau decays                                                                                             
    enum  {undetermined,
	   electron,
	   muon,
	   pi,
	   K,
	   pi1pi0,
	   pinpi0,
	   tripi,
	   tripinpi0};
    // tau mother particles                                                                                   
    enum  {other,
	   gamma,
	   Z,
	   W,
	   HSM,
	   H0,
	   A0,
	   Hpm
    };
    public:
	GenParticleDumper(std::vector<edm::ParameterSet>);
	~GenParticleDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();
	
	int tauDecayChannel(const reco::Candidate*);
	int tauProngs(const reco::Candidate*);
	double spinEffects(const reco::Candidate*);
	double rtau(const reco::Candidate*);
	TLorentzVector leadingPionP4(const reco::Candidate*);
	TLorentzVector motherP4(const reco::Candidate*);
	TLorentzVector visibleTauP4(const reco::Candidate*);
	void printDescendants(const reco::Candidate*);
	bool bFromAssociatedT(const reco::Candidate*);
	bool associatedWithHpmProduction(const reco::Candidate*);
	bool topToHp(const reco::Candidate*);
	
    private:
	bool filter();

	edm::Handle<reco::GenParticleCollection> *handle;

        //std::vector<short> *status;
	std::vector<short> *mother;
	std::vector<short> *tauProng;
	std::vector<short> *associatedWithHpm;

	std::vector<double> *massHpm;

	std::vector<double> *tauVisiblePt;
	std::vector<double> *tauVisiblePhi;
	std::vector<double> *tauVisibleEta;
	
	std::vector<double> *tauPi0RtauW;
	std::vector<double> *tauPi0RtauHpm;
	std::vector<double> *tauPi1pi0RtauW;
	std::vector<double> *tauPi1pi0RtauHpm;
	std::vector<double> *tauPinpi0RtauW;
	std::vector<double> *tauPinpi0RtauHpm;

	std::vector<double> *tauSpinEffectsW;
	std::vector<double> *tauSpinEffectsHpm;
};
#endif
