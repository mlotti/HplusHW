#ifndef METDumper_h
#define METDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"

class METDumper {
    public:
	METDumper(std::vector<edm::ParameterSet>, bool isMC);
	~METDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
        bool useFilter;
	bool booked;

	std::vector<edm::ParameterSet> inputCollections;
	edm::Handle<edm::View<pat::MET> > *handle;

	bool ismc;

	double *MET;
	double *MET_phi;
        double caloMET_et;
        double caloMET_phi;
        double GenMET_et;
        double GenMET_phi;

};
#endif
