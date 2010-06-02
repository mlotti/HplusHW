#include "RecoTauTag/RecoTau/interface/TauDiscriminationProducerBase.h"
//#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "RecoTauTag/TauTagTools/interface/PFTauQualityCutWrapper.h"
#include "FWCore/Utilities/interface/InputTag.h"

/* class PFRecoTauDiscriminationByNProngs
 * created : May 26 2010,
 * contributors : Sami Lehti (sami.lehti@cern.ch ; HIP, Helsinki)
 * based on H+ tau ID by Lauri Wendland
 */

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"

#include "TLorentzVector.h"

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

		PVProducer		= iConfig.getParameter<edm::InputTag>("PrimaryVertex");
		chargedPionMass = 0.139;
	}

      	~PFRecoTauDiscriminationByNProngs(){}

	void beginEvent(const edm::Event&, const edm::EventSetup&);
	double discriminate(const reco::PFTauRef&);

    private:
	double threeProngDeltaE(const PFTauRef&);
	double threeProngInvMass(const PFTauRef&);
	double threeProngFlightPathSig(const PFTauRef&);
	double vertexSignificance(reco::Vertex&,TransientVertex&);


	double chargedPionMass;

	PFTauQualityCutWrapper qualityCuts_;

	uint32_t nprongs;

	bool threeProngSelection;
	double deltaEmin,deltaEmax;
	double invMassMin,invMassMax;
	double flightPathSig;

	reco::Vertex primaryVertex;
	const TransientTrackBuilder* transientTrackBuilder;
	edm::InputTag PVProducer;
};

void PFRecoTauDiscriminationByNProngs::beginEvent(const Event& iEvent, const EventSetup& iSetup){

//Primary vertex
	edm::Handle<edm::View<reco::Vertex> > vertexHandle;
	iEvent.getByLabel(PVProducer, vertexHandle);
        const edm::View<reco::Vertex>& vertexCollection(*vertexHandle);
        
        primaryVertex = *(vertexCollection.begin());

	// Transient Tracks
	edm::ESHandle<TransientTrackBuilder> builder;
        iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",builder);
        transientTrackBuilder = builder.product();

}

double PFRecoTauDiscriminationByNProngs::discriminate(const PFTauRef& tau){

	bool accepted = false;
	int np = tau->signalTracks().size();

	if((np == 1 && (nprongs == 1 || nprongs == 0)) ||
           (np == 3 && (nprongs == 3 || nprongs == 0)) ) accepted = true;

	if(threeProngSelection){
		double dE = threeProngDeltaE(tau);
		if(dE < deltaEmin || dE > deltaEmax) accepted = false;

		double invMass = threeProngInvMass(tau);
		if(invMass < invMassMin || invMass > invMassMax) accepted = false;

		double fSig = threeProngFlightPathSig(tau);
		if(fSig < flightPathSig) accepted = false;  
	}

	if(!accepted) np = 0;
	return np;
}

double PFRecoTauDiscriminationByNProngs::threeProngDeltaE(const PFTauRef& tau){
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

double PFRecoTauDiscriminationByNProngs::threeProngInvMass(const PFTauRef& tau){
	TLorentzVector sum;
	PFCandidateRefVector signalTracks = tau->signalPFChargedHadrCands();
        for(size_t i = 0; i < signalTracks.size(); ++i){                        
                TLorentzVector p4;
                p4.SetXYZM(signalTracks[i]->px(), 
                           signalTracks[i]->py(),
                           signalTracks[i]->pz(),
                           chargedPionMass);
                sum += p4;
        }
	return sum.M();
}

double PFRecoTauDiscriminationByNProngs::threeProngFlightPathSig(const PFTauRef& tau){
	double flightPathSignificance = 0;

//Secondary vertex	
	const PFCandidateRefVector pfSignalCandidates = tau->signalPFCands();
	vector<TransientTrack> transientTracks;
	RefVector<PFCandidateCollection>::const_iterator iTrack;
        for(iTrack = pfSignalCandidates.begin(); iTrack!= pfSignalCandidates.end(); iTrack++){
		const PFCandidate& pfCand = *(iTrack->get());
		if(pfCand.trackRef().isNonnull()){
                  const TransientTrack transientTrack = transientTrackBuilder->build(pfCand.trackRef());
                  transientTracks.push_back(transientTrack);
                }
	}
        if(transientTracks.size() > 1){
                KalmanVertexFitter kvf(true);
                TransientVertex tv = kvf.vertex(transientTracks);

                if(tv.isValid()){
			flightPathSignificance = vertexSignificance(primaryVertex,tv);
                }
        }
	return flightPathSignificance;
}

double PFRecoTauDiscriminationByNProngs::vertexSignificance(reco::Vertex& pv, TransientVertex& sv){
	return 0;
}

DEFINE_FWK_MODULE(PFRecoTauDiscriminationByNProngs);

