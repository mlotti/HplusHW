#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTaus.h"

#include <iostream>
#include <string>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

HPlusTaus::HPlusTaus(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("METttest"),
HPlusAnalysis::HPlusSelectionBase(iConfig) {
  	// Parse the list of triggers in the config file
  	if (iConfig.exists("CollectionName")) {
    		fCollectionName = iConfig.getParameter<edm::InputTag>("CollectionName");
  	} else {
    		throw cms::Exception("Configuration") 
                  << "MET: InputTag 'CollectionName' is missing in config!" << std::endl;
  	}

  	// Initialize counters  
	fAll      = fCounter->addCounter("Taus all");
	fSelected = fCounter->addCounter("Taus selected");

  	// Declare produced items
  	std::string alias;
	produces< std::vector<math::XYZVector> >(alias = "p").setBranchAlias(alias);
	produces< std::vector<float> >(alias = "discr").setBranchAlias(alias);
}

HPlusTaus::~HPlusTaus(){}

void HPlusTaus::beginJob(){}

void HPlusTaus::endJob(){}

bool HPlusTaus::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	fCounter->addCount(fAll);

	edm::Handle<edm::View<pat::Tau> > theHandle;
	iEvent.getByLabel(fCollectionName,theHandle);

	std::auto_ptr< std::vector<math::XYZVector> > p(new std::vector<math::XYZVector>);
	size_t nDiscr = theHandle->begin()->tauIDs().size();
	std::auto_ptr< std::vector<float> > d(new std::vector<float>);

	for(edm::View<pat::Tau>::const_iterator i = theHandle->begin(); 
                                                i!= theHandle->end(); ++i){
	  	p->push_back(i->momentum());

		std::cout << "Tau pt " << i->pt() << std::endl;
		std::vector< std::pair<std::string,float> > discriminators = i->tauIDs();

		for(size_t id = 0; id < nDiscr; ++id){
                        std::cout << "discr " << discriminators[id].first << " "
                                              << discriminators[id].second << std::endl;
                        d->push_back(discriminators[id].second);
                }
	}

/*
	size_t nDiscr = theHandle->begin()->tauIDs().size();
	
	for(size_t id = 0; id < nDiscr; ++id){
		std::auto_ptr< std::vector<float> > d(new std::vector<float>);

		for(edm::View<pat::Tau>::const_iterator i = theHandle->begin();
                                                i!= theHandle->end(); ++i){
			
		}
	}
		for(size_t id = 0; id < nDiscr; ++id){
			
			std::cout << "discr " << discriminators[id].first << " " 
                                              << discriminators[id].second << std::endl;
			d->push_back(discriminators[id].second);
		}
*/
/*
		for(std::vector< std::pair<std::string,float> >::const_iterator id = discriminators.begin();
                                                          id!= discriminators.end(); ++id){
			std::cout << "discr " << id->first << " " << id->second << std::endl;
			
		}
		//TAUS: const std::vector< IdPair > & 	tauIDs () //Returns all the tau IDs in the form of <name,value> pairs 
*/
//	}

	iEvent.put(p, "p");
/*
	for(size_t n = 0; n < theHandle->size(); ++n) {
		iEvent.put(d, "discr");
	}
*/
	return 1;
}

DEFINE_FWK_MODULE(HPlusTaus);
