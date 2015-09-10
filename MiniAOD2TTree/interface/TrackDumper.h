#ifndef TrackDumper_h
#define TrackDumper_h

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
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"

class TrackDumper : public BaseDumper {
    public:
	TrackDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& );
	~TrackDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
	edm::EDGetTokenT<edm::View<pat::PackedCandidate>> *token;
        
        std::vector<float> *fIPTwrtPV;
        std::vector<float> *fIPzwrtPV;
        std::vector<float> *fIPTSignif;
        std::vector<float> *fIPzSignif;
};
#endif
