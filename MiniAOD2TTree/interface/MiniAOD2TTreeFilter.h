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
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "CommonTools/TriggerUtils/interface/PrescaleWeightProvider.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/EventInfoDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/SkimDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/TriggerDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/METNoiseFilterDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/TauDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/ElectronDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/MuonDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/JetDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/SoftBTagDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/TopDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/METDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/GenMETDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/TrackDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/GenJetDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/GenWeightDumper.h"

/**
	Class for making a tree from MiniAOD
	12112014/S.Lehti
*/

class MiniAOD2TTreeFilter : public edm::EDFilter {
    public:
        MiniAOD2TTreeFilter(const edm::ParameterSet&);
        ~MiniAOD2TTreeFilter();

        void beginRun(edm::Run const&, edm::EventSetup const&);
        void beginJob();
        bool filter(edm::Event&, const edm::EventSetup&);
        void endJob();

    private:
	void fill(edm::Event&, const edm::EventSetup&);
	void reset();
        void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&);
	bool isMC();

	std::string hltProcessName;
        HLTConfigProvider hltConfig;
        //PrescaleWeightProvider prescaleWeight;

	std::string outputFileName;
        std::string PUInfoInputFileName;
        std::string TopPtInputFileName;
	std::string codeVersion;
        std::string dataVersion;
	int cmEnergy;
	edm::ParameterSet eventInfoCollections;
	edm::ParameterSet skim;
	edm::ParameterSet trigger;
        edm::ParameterSet metNoiseFilter;
        std::vector<edm::ParameterSet> tauCollections;
	std::vector<edm::ParameterSet> electronCollections;
	std::vector<edm::ParameterSet> muonCollections;
	std::vector<edm::ParameterSet> jetCollections;
	std::vector<edm::ParameterSet> softBTagCollections;
        std::vector<edm::ParameterSet> topCollections;
	std::vector<edm::ParameterSet> metCollections;
	std::vector<edm::ParameterSet> genMetCollections;
	std::vector<edm::ParameterSet> genWeightCollections;
        std::vector<edm::ParameterSet> trackCollections;
        std::vector<edm::ParameterSet> genParticleCollections;
        std::vector<edm::ParameterSet> genJetCollections;


	TFile* fOUT;
	TTree* Events;

	EventInfoDumper *eventInfo;
	SkimDumper* skimDumper;
	TriggerDumper* trgDumper;
        METNoiseFilterDumper* metNoiseFilterDumper;
	TauDumper* tauDumper;
	ElectronDumper* electronDumper;
	MuonDumper* muonDumper;
	JetDumper* jetDumper;
	SoftBTagDumper* softBTagDumper;
        TopDumper* topDumper;
	METDumper* metDumper;
	GenMETDumper* genMetDumper;
        GenWeightDumper* genWeightDumper;
	TrackDumper* trackDumper;
	GenParticleDumper* genParticleDumper;
        GenJetDumper* genJetDumper;
};

#endif
