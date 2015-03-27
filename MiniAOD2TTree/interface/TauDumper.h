#ifndef TauDumper_h
#define TauDumper_h

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
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"

class TauDumper : public BaseDumper {
    public:
	TauDumper(std::vector<edm::ParameterSet>);
	~TauDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();

	edm::Handle<edm::View<pat::Tau> > *handle;

        std::vector<double> *ltrackPt;
        std::vector<double> *ltrackEta;

	std::vector<int> *nProngs;
};
#endif
