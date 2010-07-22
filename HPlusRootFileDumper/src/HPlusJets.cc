#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusJets.h"

#include <iostream>
#include <string>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


HPlusJets::HPlusJets(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("Jets"),
HPlusAnalysis::HPlusSelectionBase(iConfig) {
  	// Parse the list of triggers in the config file
  	if (iConfig.exists("CollectionName")) {
    		fCollectionName = iConfig.getParameter<edm::InputTag>("CollectionName");
		vDiscriminators = iConfig.getParameter<std::vector<edm::InputTag> >("Discriminators");
  	} else {
    		throw cms::Exception("Configuration") 
                  << "Taus: InputTag 'CollectionName' is missing in config!" << std::endl;
  	}

  	// Initialize counters  
	fAll      = fCounter->addCounter("all");
	fSelected = fCounter->addCounter("selected");

  	// Declare produced items
        std::string name;
        std::string alias_prefix = iConfig.getParameter<std::string>("@module_label") + "_";
        name = "momentum";
	produces< std::vector<math::XYZVector> >(name).setBranchAlias(alias_prefix+name);

	for(size_t i = 0; i < vDiscriminators.size(); ++i){
		name = vDiscriminators[i].label();
		produces< std::vector<float> >(name).setBranchAlias(alias_prefix+name);
	}
}

HPlusJets::~HPlusJets(){}

void HPlusJets::beginJob(){}

void HPlusJets::endJob(){}

bool HPlusJets::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	fCounter->addCount(fAll);

	edm::Handle<edm::View<pat::Jet> > theHandle;
	iEvent.getByLabel(fCollectionName,theHandle);

        std::auto_ptr< std::vector<math::XYZVector> > momentum(new std::vector<math::XYZVector>);
        for(edm::View<pat::Jet>::const_iterator i = theHandle->begin();
                                                i!= theHandle->end(); ++i){
                momentum->push_back(i->momentum());
		//std::cout << "check jet pt " << i->momentum()->rho() << std::endl;
	}
	iEvent.put(momentum, "momentum");

	for(size_t ds = 0; ds < vDiscriminators.size(); ++ds){
                //std::cout << vDiscriminators[ds].label() << std::endl;
		std::auto_ptr< std::vector<float> > discr(new std::vector<float>);
		for(edm::View<pat::Jet>::const_iterator i = theHandle->begin();
                                                        i!= theHandle->end(); ++i){
			discr->push_back(i->bDiscriminator(vDiscriminators[ds].label()));
		}
		iEvent.put(discr,vDiscriminators[ds].label());
	}

	fCounter->addCount(fSelected);
	return 1;
}

DEFINE_FWK_MODULE(HPlusJets);


