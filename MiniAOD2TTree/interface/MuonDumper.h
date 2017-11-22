#ifndef MuonDumper_h
#define MuonDumper_h

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

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/FourVectorDumper.h"

namespace reco {
  class Vertex;
}

class MuonDumper : public BaseDumper {
    public:
	MuonDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets, const edm::InputTag& recoVertexTag);
	~MuonDumper();

        void book(TTree*);
        bool fill(edm::Event&, const edm::EventSetup&);
        void reset();

    private:
	void fillMCMatchInfo(size_t ic, edm::Handle<reco::GenParticleCollection>& genParticles, const pat::Muon& muon);
	
        edm::EDGetTokenT<edm::View<pat::Muon>> *muonToken;
        edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken;
        edm::EDGetTokenT<edm::View<reco::Vertex>> vertexToken;

        std::vector<short> *q;

        std::vector<bool> *isGlobalMuon;
        // Note that isSoftMuon and isHighPtMuon are at the moment not PF compatible
        std::vector<bool> *isLooseMuon;
        std::vector<bool> *isMediumMuon;
        std::vector<bool> *isTightMuon;
        std::vector<float> *relIsoDeltaBetaCorrected03; // isol cone 0.3
        std::vector<float> *relIsoDeltaBetaCorrected04; // isol cone 0.4

	// Marina - start
	edm::EDGetTokenT<double> *rhoToken;
	edm::EDGetTokenT<edm::View<pat::PackedCandidate> > *pfcandsToken;
	std::vector<float> *relMiniIso;
	std::vector<float> *effAreaMiniIso;
        // Marina - end     

        // 4-vector for generator muon
        FourVectorDumper *MCmuon;

};
#endif
