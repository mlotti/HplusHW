#include "RecoTauTag/RecoTau/interface/TauDiscriminationProducerBase.h"
//#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "RecoTauTag/TauTagTools/interface/PFTauQualityCutWrapper.h"

/* class PFRecoTauDiscriminationByTauPolarization
 * created : May 26 2010,
 * contributors : Sami Lehti (sami.lehti@cern.ch ; HIP, Helsinki)
 */

using namespace reco;
using namespace std;

class PFRecoTauDiscriminationByNProngs : public PFTauDiscriminationProducerBase  {
    public:
	explicit PFRecoTauDiscriminationByNProngs(const ParameterSet& iConfig):PFTauDiscriminationProducerBase(iConfig), 
                                                                               qualityCuts_(iConfig.getParameter<ParameterSet>("qualityCuts")){  // retrieve quality cuts    
		nprongs			= iConfig.getParameter<uint32_t>("nProngs");

		threeProngSelection	= iConfig.getParameter<bool>("threeProngSelection");
		deltaEmin		= iConfig.getParameter<double>("deltaEmin");
		deltaEmax               = iConfig.getParameter<double>("deltaEmax");
		invMassMin		= iConfig.getParameter<double>("invMassMin");
		invMassMax		= iConfig.getParameter<double>("invMassMax");
		flightPathSig		= iConfig.getParameter<double>("flightPathSig");
	}

      	~PFRecoTauDiscriminationByNProngs(){}

	void beginEvent(const Event&, const EventSetup&);
	double discriminate(const PFTauRef&);

    private:
	PFTauQualityCutWrapper qualityCuts_;

	uint32_t nprongs;

	bool threeProngSelection;
	double deltaEmin,deltaEmax;
	double invMassMin,invMassMax;
	double flightPathSig;
};

void PFRecoTauDiscriminationByNProngs::beginEvent(const Event& event, const EventSetup& eventSetup){}

double PFRecoTauDiscriminationByNProngs::discriminate(const PFTauRef& tau){

	bool accepted = false;
	int np = tau->signalTracks().size();

	if((np == 1 && (nprongs == 1 || nprongs == 0)) ||
           (np == 3 && (nprongs == 3 || nprongs == 0)) ) accepted = true;

	if(threeProngSelection){

	}

	if(!accepted) np = 0;
	return np;
}

DEFINE_FWK_MODULE(PFRecoTauDiscriminationByNProngs);

