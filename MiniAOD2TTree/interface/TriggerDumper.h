#ifndef TriggerDumper_h
#define TriggerDumper_h

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

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"

class TriggerDumper {
    public:
	TriggerDumper(edm::ParameterSet&);
	~TriggerDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
        void book(edm::Event&);

        bool filter();
	bool useFilter;
	bool booked;

	TTree* theTree;

	edm::InputTag triggerResults;
        edm::InputTag triggerObjects;
	edm::InputTag l1extra;

	bool *iBit; 
	edm::ParameterSet inputCollection;
	edm::Handle<edm::TriggerResults> handle;
	std::vector<std::string> triggerBits;

	double L1MET;
        double L1METphi;
	double HLTMET;
	double HLTMETphi;

        std::vector<double> HLTTau_pt;
        std::vector<double> HLTTau_eta;
        std::vector<double> HLTTau_phi;
        std::vector<double> HLTTau_e;
};
#endif
