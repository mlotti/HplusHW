#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusMET.h"

#include <iostream>
#include <string>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/MET.h"

HPlusMET::HPlusMET(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("MET"),
HPlusAnalysis::HPlusSelectionBase(iConfig) {
  	// Parse the list of triggers in the config file
  	if (iConfig.exists("CollectionName")) {
    		fCollectionName = iConfig.getParameter<edm::InputTag>("CollectionName");
		fCut            = iConfig.getParameter<double>("METCut");
  	} else {
    		throw cms::Exception("Configuration") 
                  << "MET: InputTag 'CollectionName' is missing in config!" << std::endl;
  	}

  	// Initialize counters  
	fAll      = fCounter->addCounter("all");
	fSelected = fCounter->addCounter("selected");

  	// Declare produced items
        std::string name;
        std::string alias_prefix = iConfig.getParameter<std::string>("@module_label") + "_";

//  	produces<float>(alias = fCollectionName.label()).setBranchAlias(alias);
        name = "METx";
	produces<float>(name).setBranchAlias(alias_prefix+name);
        name = "METy";
	produces<float>(name).setBranchAlias(alias_prefix+name);
}

HPlusMET::~HPlusMET(){}

void HPlusMET::beginJob(){}

void HPlusMET::endJob(){}

bool HPlusMET::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	fCounter->addCount(fAll);

	edm::Handle<edm::View<pat::MET> > theHandle;
	iEvent.getByLabel(fCollectionName,theHandle);

	std::auto_ptr<float> metX(new float);
	std::auto_ptr<float> metY(new float);

	*metX = (*theHandle)[0].px();
	*metY = (*theHandle)[0].py();

    	iEvent.put(metX, "METx");
	iEvent.put(metY, "METy");

	if((*theHandle)[0].pt() < fCut) return 0; 
	fCounter->addCount(fSelected);
	return 1;
}

DEFINE_FWK_MODULE(HPlusMET);
