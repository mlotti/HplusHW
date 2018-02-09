#ifndef FatJetDumper_h
#define FatJetDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/FourVectorDumper.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
//#include "DataFormats/BTauReco/interface/CATopJetTagInfo.h"

class FatJetDumper : public BaseDumper {
    public:
        FatJetDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~FatJetDumper();

        void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
        void reset();

    private:
        /// Returns true, if the jet passes the specified jetID
        bool passJetID(int id, const pat::Jet& jet);
        
    private:
	edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken;
        edm::EDGetTokenT<edm::View<pat::Jet>> *jetToken;

        edm::EDGetTokenT<edm::View<pat::Jet>> *jetJESup;
        edm::EDGetTokenT<edm::View<pat::Jet>> *jetJESdown;
        edm::EDGetTokenT<edm::View<pat::Jet>> *jetJERup;
        edm::EDGetTokenT<edm::View<pat::Jet>> *jetJERdown;
	
	edm::EDGetTokenT<double> rho_token;
	edm::EDGetTokenT<reco::VertexCollection> vertex_token;
	
        std::vector<float> *discriminators;
        std::vector<double> *userfloats;
	int nUserfloats;
	std::vector<int> *userints;
	int nUserints;
	std::vector<double> *groomedmasses;
	int nGroomedMasses;
	std::vector<double> *userfloats_Puppi;
	int nUserfloats_Puppi;
	
        std::vector<int> *hadronFlavour;
        std::vector<int> *partonFlavour;

        std::vector<bool> *jetIDloose;
        std::vector<bool> *jetIDtight;
        std::vector<bool> *jetIDtightLeptonVeto;

        std::vector<bool> *jetPUIDloose;
	std::vector<bool> *jetPUIDmedium;
	std::vector<bool> *jetPUIDtight;

        // 4-vector for generator jet
        FourVectorDumper *MCjet;
        
	// Systematics variations for tau 4-vector
	bool systVariations;
        FourVectorDumper *systJESup;
        FourVectorDumper *systJESdown;
        FourVectorDumper *systJERup;
        FourVectorDumper *systJERdown;
	
	bool fillPuppi;
	
	std::string mcjecPath;
	std::string datajecPath;
	FactorizedJetCorrector *mcJEC;
	FactorizedJetCorrector *mcJEC_PUPPI;
	FactorizedJetCorrector *dataJEC;
	FactorizedJetCorrector *dataJEC_PUPPI;
	
	std::vector<double> *corrPrunedMass;
	std::vector<int> *numberOfDaughters;
	std::vector<int> *nSubjets;
	std::vector<double> *sdsubjet1_pt;
	std::vector<double> *sdsubjet1_eta;
	std::vector<double> *sdsubjet1_phi;
	std::vector<double> *sdsubjet1_mass;
	std::vector<double> *sdsubjet1_csv;
	
	std::vector<double> *sdsubjet2_pt;
	std::vector<double> *sdsubjet2_eta;
	std::vector<double> *sdsubjet2_phi;
	std::vector<double> *sdsubjet2_mass;
	std::vector<double> *sdsubjet2_csv;
	
	// PUPPI 
	std::vector<double> *corrPrunedMass_PUPPI;
	std::vector<double> *softdropMass_PUPPI;
	std::vector<int> *nSubjets_PUPPI;
	std::vector<double> *sdsubjet1_PUPPI_pt;
	std::vector<double> *sdsubjet1_PUPPI_eta;
	std::vector<double> *sdsubjet1_PUPPI_phi;
	std::vector<double> *sdsubjet1_PUPPI_mass;
	std::vector<double> *sdsubjet1_PUPPI_csv;
	
	std::vector<double> *sdsubjet2_PUPPI_pt;
	std::vector<double> *sdsubjet2_PUPPI_eta;
	std::vector<double> *sdsubjet2_PUPPI_phi;
	std::vector<double> *sdsubjet2_PUPPI_mass;
	std::vector<double> *sdsubjet2_PUPPI_csv;
	
};
#endif
