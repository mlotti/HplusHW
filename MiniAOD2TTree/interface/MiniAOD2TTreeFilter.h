#ifndef MiniAOD2TTreeFilter_h
#define MiniAOD2TTreeFilter_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"
        
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"  
#include "DataFormats/Common/interface/View.h"
        
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/EventInfoDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/TauDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/ElectronDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/MuonDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/JetDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/METDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleDumper.h"


/**
	Class for making a tree from MiniAOD
	12112014/S.Lehti
*/

class MiniAOD2TTreeFilter : public edm::EDFilter {
    public:
        MiniAOD2TTreeFilter(const edm::ParameterSet&);
        ~MiniAOD2TTreeFilter();

        void beginJob();
        bool filter(edm::Event&, const edm::EventSetup&);
        void endJob();

    private:
	void fill(edm::Event&, const edm::EventSetup&);
	void reset();

	std::string outputFileName;
	std::string codeVersion;
        std::string dataVersion;
	edm::ParameterSet eventInfoCollections;
	edm::ParameterSet trigger;
        std::vector<edm::ParameterSet> tauCollections;
	std::vector<edm::ParameterSet> electronCollections;
	std::vector<edm::ParameterSet> muonCollections;
	std::vector<edm::ParameterSet> jetCollections;
	std::vector<edm::ParameterSet> metCollections;
        std::vector<edm::ParameterSet> genParticleCollections;


	TFile* fOUT;
	TTree* Events;

	EventInfoDumper *eventInfo;
	TriggerDumper* trgDumper;
	TauDumper* tauDumper;
	ElectronDumper* electronDumper;
	MuonDumper* muonDumper;
	JetDumper* jetDumper;
	METDumper* metDumper;
	GenParticleDumper* genParticleDumper;
};

#endif
