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


class MuonDumper : public BaseDumper {
    public:
	MuonDumper(std::vector<edm::ParameterSet>, const edm::InputTag& recoVertexTag);
	~MuonDumper();

        void book(TTree*);
        bool fill(edm::Event&, const edm::EventSetup&);
        void reset();

    private:
	const edm::InputTag offlinePrimaryVertexSrc;
        edm::Handle<edm::View<pat::Muon> > *handle;

        std::vector<bool> *isGlobalMuon;
        // Note that isSoftMuon and isHighPtMuon are at the moment not PF compatible
        std::vector<bool> *isLooseMuon;
        std::vector<bool> *isMediumMuon;
        std::vector<bool> *isTightMuon;
        
};
#endif
