#ifndef ElectronDumper_h
#define ElectronDumper_h

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
#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/FourVectorDumper.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"


class ElectronDumper : public BaseDumper {
    public:
	ElectronDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~ElectronDumper();

        void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
        void reset();

    private:
	void fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Electron& ele);
	
        edm::EDGetTokenT<edm::View<pat::Electron>> *electronToken;
        edm::EDGetTokenT<edm::View<reco::GsfElectron>> *gsfElectronToken;
        edm::EDGetTokenT<double> *rhoToken;
        edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken;
        edm::EDGetTokenT<edm::ValueMap<bool>> *electronIDToken;
        
        std::vector<float> *relIsoDeltaBetaCorrected;
        std::vector<float> *effAreaIsoDeltaBetaCorrected;
	
	// Marina - start
	edm::EDGetTokenT<edm::View<pat::PackedCandidate> > *pfcandsToken;
	std::vector<float> *relMiniIso;
	std::vector<float> *effAreaMiniIso;
	// Marina - end
	
        // 4-vector for generator electron
        FourVectorDumper *MCelectron;
};
#endif
