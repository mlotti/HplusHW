#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusJets.h"

#include <iostream>
#include <string>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


HPlusJets::HPlusJets(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("Jetttest"),
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
	fAll      = fCounter->addCounter("Jets all");
	fSelected = fCounter->addCounter("Jets selected");

  	// Declare produced items
  	std::string alias;
	produces< std::vector<math::XYZVector> >(alias = "momentum").setBranchAlias(alias);

	for(size_t i = 0; i < vDiscriminators.size(); ++i){
		produces< std::vector<float> >(alias = vDiscriminators[i].label()).setBranchAlias(alias);
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
	}

	for(size_t ds = 0; ds < vDiscriminators.size(); ++ds){
		std::cout << vDiscriminators[ds].label() << std::endl;
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


