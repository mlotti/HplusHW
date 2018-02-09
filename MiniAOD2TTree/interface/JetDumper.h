#ifndef JetDumper_h
#define JetDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/FourVectorDumper.h"

#include "DataFormats/PatCandidates/interface/Jet.h"


class JetDumper : public BaseDumper {
    public:
	JetDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~JetDumper();

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

        std::vector<float> *discriminators;
        std::vector<double> *userfloats;
	int nUserfloats;
	std::vector<int> *userints;
	int nUserints;
        //std::vector<JetCorrectionUncertainty*> fJECUncertainty;

        std::vector<int> *hadronFlavour;
        std::vector<int> *partonFlavour;

        std::vector<bool> *jetIDloose;
        std::vector<bool> *jetIDtight;
        std::vector<bool> *jetIDtightLeptonVeto;

        std::vector<bool> *jetPUIDloose;
	std::vector<bool> *jetPUIDmedium;
	std::vector<bool> *jetPUIDtight;

        // MC origin
        std::vector<bool> *originatesFromW;
        std::vector<bool> *originatesFromZ;
        std::vector<bool> *originatesFromTop;
        std::vector<bool> *originatesFromChargedHiggs;
        std::vector<bool> *originatesFromUnknown;
        
        // 4-vector for generator jet
        FourVectorDumper *MCjet;
        
        // Systematics variations for tau 4-vector
	bool systVariations;
        FourVectorDumper *systJESup;
        FourVectorDumper *systJESdown;
        FourVectorDumper *systJERup;
        FourVectorDumper *systJERdown;	
};
#endif
