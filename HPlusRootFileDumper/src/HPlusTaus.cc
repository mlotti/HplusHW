#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTaus.h"

#include <iostream>
#include <string>
#include<limits>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Tau.h"


HPlusTaus::HPlusTaus(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("Taus"),
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
        name = "leadingTrackMomentum";
        produces< std::vector<math::XYZVector> >(name).setBranchAlias(alias_prefix+name);
        name = "leadingIsolTrackMomentum";
        produces< std::vector<math::XYZVector> >(name).setBranchAlias(alias_prefix+name);

	for(size_t i = 0; i < vDiscriminators.size(); ++i){
                name = vDiscriminators[i].label();
		produces< std::vector<float> >(name).setBranchAlias(alias_prefix+name);
	}
//	produces< std::vector<float> >(alias = "discr").setBranchAlias(alias);
}

HPlusTaus::~HPlusTaus(){}

void HPlusTaus::beginJob(){}

void HPlusTaus::endJob(){}

bool HPlusTaus::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	fCounter->addCount(fAll);

	edm::Handle<edm::View<pat::Tau> > theHandle;
	iEvent.getByLabel(fCollectionName,theHandle);

        std::auto_ptr< std::vector<math::XYZVector> > momentum(new std::vector<math::XYZVector>);
        std::auto_ptr< std::vector<math::XYZVector> > ldgTrkMomentum(new std::vector<math::XYZVector>);
	std::auto_ptr< std::vector<math::XYZVector> > ldgIsolTrkMomentum(new std::vector<math::XYZVector>);
        for(edm::View<pat::Tau>::const_iterator i = theHandle->begin();
                                                i!= theHandle->end(); ++i){
                momentum->push_back(i->momentum());

                reco::TrackRef ldgTrk = i->leadTrack();
                if(ldgTrk.isNonnull()) {
                  ldgTrkMomentum->push_back(ldgTrk->momentum());
                }
                else {
                  const double nan = std::numeric_limits<double>::quiet_NaN();
                  ldgTrkMomentum->push_back(math::XYZVector(nan, nan, nan));
                }

		//leading track in the isolation cone
		double ptMax = 0;
		reco::TrackRefVector isolTracks = i->isolationTracks();
		reco::TrackRef ldgIsolTrk;// = *(isolTracks.begin());
		for(size_t jj = 0; jj < isolTracks.size(); ++jj){
			//std::cout << isolTracks[jj]->pt() << std::endl;
			if(isolTracks[jj]->pt() > ptMax){
				ptMax = isolTracks[jj]->pt();
				ldgIsolTrk = isolTracks[jj];
			}
		}
		if(ldgIsolTrk.isNonnull()) {
		  ldgIsolTrkMomentum->push_back(ldgIsolTrk->momentum());
                }
                else {
                  const double nan = std::numeric_limits<double>::quiet_NaN();
                  ldgIsolTrkMomentum->push_back(math::XYZVector(nan, nan, nan));
                }

		/*
                std::vector< std::pair<std::string,float> > discriminators = i->tauIDs();
                size_t nDiscr = discriminators.size();
                for(size_t id = 0; id < nDiscr; ++id){
                        std::cout << "discr " << discriminators[id].first << " "
                                              << discriminators[id].second << std::endl;
                }
                */
	}

	for(size_t ds = 0; ds < vDiscriminators.size(); ++ds){
                //std::cout << vDiscriminators[ds].label() << std::endl;
		std::auto_ptr< std::vector<float> > discr(new std::vector<float>);
		for(edm::View<pat::Tau>::const_iterator i = theHandle->begin();
                                                        i!= theHandle->end(); ++i){
			discr->push_back(i->tauID(vDiscriminators[ds].label()));
		}
		iEvent.put(discr,vDiscriminators[ds].label());
	}

/*

///////
	for(edm::View<pat::Tau>::const_iterator i = theHandle->begin(); 
                                                i!= theHandle->end(); ++i){
	  	momentum->push_back(i->momentum());

		std::cout << "Tau pt " << i->pt() << std::endl;

		std::vector< std::pair<std::string,float> > discriminators = i->tauIDs();
		size_t nDiscr = discriminators.size();
		for(size_t id = 0; id < nDiscr; ++id){
                        std::cout << "discr " << discriminators[id].first << " "
                                              << discriminators[id].second << std::endl;
//                        d->push_back(discriminators[id].second);
                }


		for(size_t ds = 0; ds < vDiscriminators.size(); ++ds){
			std::cout << vDiscriminators[ds].label() << std::endl;
			std::auto_ptr<float> discr(new float);
			*discr = i->tauID(vDiscriminators[ds].label());
//			iEvent.put(discr,vDiscriminators[ds].label());
		}
	}
*/
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

	iEvent.put(momentum, "momentum");
        iEvent.put(ldgTrkMomentum, "leadingTrackMomentum");
	iEvent.put(ldgIsolTrkMomentum, "leadingIsolTrackMomentum");
/*
	for(size_t n = 0; n < theHandle->size(); ++n) {
		iEvent.put(d, "discr");
	}
*/
	fCounter->addCount(fSelected);
	return 1;
}

DEFINE_FWK_MODULE(HPlusTaus);


