#ifndef TriggerDumper_h
#define TriggerDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>
#include <utility>

#include "TTree.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/L1Trigger/interface/Tau.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1Trigger/interface/EtSum.h"
//#include "DataFormats/L1Trigger/interface/BXVector.h"
//#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"

class TriggerDumper {
    public:
	TriggerDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset);
	~TriggerDumper();

	void book(TTree*);
        void book(const edm::Run&,HLTConfigProvider);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();
	void triggerMatch(int,std::vector<reco::Candidate::LorentzVector>);

	std::pair<int,int> counters(std::string);

    private:

        bool filter();
	bool useFilter;
	bool booked;

	bool isCorrectObject(int,std::string);


	TTree* theTree;

        bool *iBit; 
        int  *iCountAll;
        int  *iCountPassed;
        edm::ParameterSet inputCollection;
        edm::EDGetTokenT<edm::TriggerResults> trgResultsToken;
        edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trgObjectsToken;
        edm::EDGetTokenT<pat::PackedTriggerPrescales> trgPrescaleToken;
        edm::EDGetTokenT<l1t::TauBxCollection> l1TausToken;
        edm::EDGetTokenT<l1t::JetBxCollection> l1JetsToken;
        edm::EDGetTokenT<l1t::EtSumBxCollection> l1EtSumToken;
        edm::EDGetTokenT<std::vector<l1extra::L1EtMissParticle>> trgL1ETMToken;
        std::vector<std::string> triggerBits;
        std::vector<std::string> selectedTriggers;
        std::vector<std::string> trgMatchStr;
        std::vector<std::string> trgMatchBranches;
        std::vector<std::string> trgPrescalePaths;
	double trgMatchDr;

	edm::TriggerNames names;
	edm::Handle<pat::TriggerObjectStandAloneCollection> patTriggerObjects;

        double L1MET_l1extra_x;
        double L1MET_l1extra_y;
        double L1MET_pat_x;
        double L1MET_pat_y;
	double L1MET_x;
        double L1MET_y;
        bool bookL1EtSum;
	double HLTMET_x;
	double HLTMET_y;

        std::vector<double> L1Tau_pt; 
        std::vector<double> L1Tau_eta;
        std::vector<double> L1Tau_phi;
        std::vector<double> L1Tau_e;

        std::vector<double> L1IsoTau_pt;
        std::vector<double> L1IsoTau_eta;
        std::vector<double> L1IsoTau_phi;
        std::vector<double> L1IsoTau_e;
        bool bookL1Tau;

        std::vector<double> L1Jet_pt;
        std::vector<double> L1Jet_eta;
        std::vector<double> L1Jet_phi;
        std::vector<double> L1Jet_e;
        bool bookL1Jet;

        std::vector<double> HLTTau_pt;
        std::vector<double> HLTTau_eta;
        std::vector<double> HLTTau_phi;
        std::vector<double> HLTTau_e;
        
        std::vector<double> HLTMuon_pt;
        std::vector<double> HLTMuon_eta;
        std::vector<double> HLTMuon_phi;
        std::vector<double> HLTMuon_e;

	std::vector<double> HLTMuon_pt;
        std::vector<double> HLTMuon_eta;
        std::vector<double> HLTMuon_phi;
        std::vector<double> HLTMuon_e;

        //std::vector<double> HLTJet_pt;
        //std::vector<double> HLTJet_eta;
        //std::vector<double> HLTJet_phi;
        //std::vector<double> HLTJet_e;

        std::vector<double> HLTBJet_pt;
        std::vector<double> HLTBJet_eta;
        std::vector<double> HLTBJet_phi;
        std::vector<double> HLTBJet_e;

        int nTrgDiscriminators;
        std::vector<bool> *trgdiscriminators;
        std::vector<int> *trgprescales;
};
#endif
