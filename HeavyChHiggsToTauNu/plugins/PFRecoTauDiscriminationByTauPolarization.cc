#include "RecoTauTag/RecoTau/interface/TauDiscriminationProducerBase.h"
//#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "RecoTauTag/TauTagTools/interface/PFTauQualityCutWrapper.h"

/* class PFRecoTauDiscriminationByTauPolarization
 * created : May 26 2010,
 * contributors : Sami Lehti (sami.lehti@cern.ch ; HIP, Helsinki)
 */

using namespace reco;
using namespace std;

class PFRecoTauDiscriminationByTauPolarization : public PFTauDiscriminationProducerBase  {
    public:
	explicit PFRecoTauDiscriminationByTauPolarization(const ParameterSet& iConfig):PFTauDiscriminationProducerBase(iConfig), 
                                                                               qualityCuts_(iConfig.getParameter<ParameterSet>("qualityCuts")){  // retrieve quality cuts    
		rTauMin = iConfig.getParameter<double>("rtau");
		booleanOutput = iConfig.getParameter<bool>("BooleanOutput");
	}

      	~PFRecoTauDiscriminationByTauPolarization(){}

	void beginEvent(const Event&, const EventSetup&);
	double discriminate(const PFTauRef&);

    private:
	PFTauQualityCutWrapper qualityCuts_;

	bool booleanOutput;
	double rTauMin;
};

void PFRecoTauDiscriminationByTauPolarization::beginEvent(const Event& event, const EventSetup& eventSetup){}

double PFRecoTauDiscriminationByTauPolarization::discriminate(const PFTauRef& tau){

	double rTau = 0;
	//if(tau->p() > 0) rTau = tau->leadTrack()->p()/tau->p();
	if(tau.isNonnull() && tau->p() > 0 && tau->leadTrack().isNonnull()) rTau = tau->leadTrack()->p()/tau->p();

	if(booleanOutput) return ( rTau > rTauMin ? 1. : 0. );
	return rTau;
}

DEFINE_FWK_MODULE(PFRecoTauDiscriminationByTauPolarization);

