#include "RecoTauTag/RecoTau/interface/TauDiscriminationProducerBase.h"
//#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "RecoTauTag/TauTagTools/interface/PFTauQualityCutWrapper.h"
#include "FWCore/Utilities/interface/InputTag.h"

/* class PFRecoTauDiscriminationByDeltaE
 * created : August 30 2010,
 * contributors : Sami Lehti (sami.lehti@cern.ch ; HIP, Helsinki)
 * based on H+ tau ID by Lauri Wendland
 */

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"

#include "TLorentzVector.h"

using namespace reco;
using namespace std;

class PFRecoTauDiscriminationByDeltaE : public PFTauDiscriminationProducerBase  {
    public:
	explicit PFRecoTauDiscriminationByDeltaE(const ParameterSet& iConfig):PFTauDiscriminationProducerBase(iConfig){
		deltaEmin		= iConfig.getParameter<double>("deltaEmin");
		deltaEmax               = iConfig.getParameter<double>("deltaEmax");
		chargedPionMass         = 0.139;
		booleanOutput 		= iConfig.getParameter<bool>("BooleanOutput");
	}

      	~PFRecoTauDiscriminationByDeltaE(){}

	void beginEvent(const edm::Event&, const edm::EventSetup&);
	double discriminate(const reco::PFTauRef&);

    private:
	double DeltaE(const PFTauRef&);

	double chargedPionMass;

//	PFTauQualityCutWrapper qualityCuts_;

	double deltaEmin,deltaEmax;
	bool booleanOutput;
};

void PFRecoTauDiscriminationByDeltaE::beginEvent(const Event& iEvent, const EventSetup& iSetup){
}

double PFRecoTauDiscriminationByDeltaE::discriminate(const PFTauRef& tau){

	double dE = DeltaE(tau);
	if(booleanOutput) return ( dE > deltaEmin && dE < deltaEmax ? 1. : 0. );
	return dE;
}

double PFRecoTauDiscriminationByDeltaE::DeltaE(const PFTauRef& tau){
	double tracksE = 0;
	PFCandidateRefVector signalTracks = tau->signalPFChargedHadrCands();
	for(size_t i = 0; i < signalTracks.size(); ++i){
		TLorentzVector p4;
		p4.SetXYZM(signalTracks[i]->px(), 
                           signalTracks[i]->py(), 
                           signalTracks[i]->pz(), 
                           chargedPionMass);
		tracksE += p4.E();
	}
	return tracksE/tau->momentum().r() - 1;
}

DEFINE_FWK_MODULE(PFRecoTauDiscriminationByDeltaE);

