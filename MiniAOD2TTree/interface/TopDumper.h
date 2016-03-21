#ifndef TopDumper_h
#define TopDumper_h

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

#include "DataFormats/BTauReco/interface/CATopJetTagInfo.h"

class TopDumper : public BaseDumper {
    public:
	TopDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~TopDumper();

        void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
        void reset();

    private:
        edm::EDGetTokenT<edm::View<reco::CATopJetTagInfo>> topToken;

	std::vector<double> *minMass;
	std::vector<double> *topMass;
	std::vector<double> *wMass;
	std::vector<int>    *nSubJets;
};
#endif
