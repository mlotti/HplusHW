#ifndef GenJetDumper_h
#define GenJetDumper_h

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
#include "DataFormats/JetReco/interface/GenJet.h"

class GenJetDumper : public BaseDumper {
    public:
	GenJetDumper(std::vector<edm::ParameterSet>);
	~GenJetDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();

	edm::Handle<reco::GenJetCollection> *handle;

        std::vector<short> *status;
};
#endif
