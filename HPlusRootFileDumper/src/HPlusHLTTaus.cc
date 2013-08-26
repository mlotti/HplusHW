#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusHLTTaus.h"

#include <iostream>
#include <string>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Tau.h"


HPlusHLTTaus::HPlusHLTTaus(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("HLTTaus"),
HPlusAnalysis::HPlusSelectionBase(iConfig) {
  	// Parse the list of triggers in the config file
  	if (iConfig.exists("CollectionName")) {
    		fCollectionName = iConfig.getParameter<edm::InputTag>("CollectionName");
  	} else {
    		throw cms::Exception("Configuration") 
                  << "Taus: InputTag 'CollectionName' is missing in config!" << std::endl;
  	}

  	// Initialize counters  
	fAll      = fCounter->addCounter("all");
	fSelected = fCounter->addCounter("selected");

  	// Declare produced items
  	std::string alias;
	produces< std::vector<math::XYZVector> >(alias = "momentum").setBranchAlias(alias);
}

HPlusHLTTaus::~HPlusHLTTaus(){}

void HPlusHLTTaus::beginJob(){}

void HPlusHLTTaus::endJob(){}

bool HPlusHLTTaus::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	fCounter->addCount(fAll);

	edm::Handle<edm::View<pat::Tau> > theHandle;
	iEvent.getByLabel(fCollectionName,theHandle);

        std::auto_ptr< std::vector<math::XYZVector> > momentum(new std::vector<math::XYZVector>);
        for(edm::View<pat::Tau>::const_iterator i = theHandle->begin();
                                                i!= theHandle->end(); ++i){
                momentum->push_back(i->momentum());

                std::vector< std::pair<std::string,float> > discriminators = i->tauIDs();
                size_t nDiscr = discriminators.size();
                for(size_t id = 0; id < nDiscr; ++id){
                        std::cout << "discr " << discriminators[id].first << " "
                                              << discriminators[id].second << std::endl;
                }
	}
	iEvent.put(momentum, "momentum");

	fCounter->addCount(fSelected);
	return 1;
}

DEFINE_FWK_MODULE(HPlusHLTTaus);


