#ifndef BaseDumper_h
#define BaseDumper_h

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
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

class BaseDumper {
    public:
	BaseDumper();
	BaseDumper(std::vector<edm::ParameterSet>& psets);
	~BaseDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

	std::vector<reco::Candidate::LorentzVector> selected();

    protected:
	bool filter();
        bool useFilter;
	bool booked;

	std::vector<edm::ParameterSet> inputCollections;

        std::vector<double> *pt;
        std::vector<double> *eta;            
        std::vector<double> *phi;
        std::vector<double> *e;
	std::vector<double> *et;

//	std::vector<reco::Candidate::LorentzVector> *p4;
	std::vector<short> *pdgId;
        std::vector<short> *status;

	int nDiscriminators;
	std::vector<bool> *discriminators;
};
#endif
