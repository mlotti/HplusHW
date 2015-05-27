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


class ElectronDumper : public BaseDumper {
    public:
	ElectronDumper(std::vector<edm::ParameterSet>);
	~ElectronDumper();

	bool fill(edm::Event&, const edm::EventSetup&);

    private:
	edm::Handle<edm::View<pat::Electron> > *handle;
};
#endif
