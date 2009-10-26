#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackEcalHitPoint.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HitConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CaloTowerConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EcalClusterConverter.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyHit.h"

#include "DataFormats/TauReco/interface/CaloTau.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/BTauReco/interface/IsolatedTauTagInfo.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/PatternTools/interface/Trajectory.h"

#include "RecoTauTag/TauTagTools/interface/CaloTauElementsOperators.h"
#include "RecoTauTag/TauTagTools/interface/PFTauElementsOperators.h"
#include "JetMETCorrections/TauJet/interface/TauJetCorrector.h"

using reco::CaloTau;
using reco::PFTau;
using reco::IsolatedTauTagInfo;
using pat::Tau;

TauConverter::TauConverter(const TrackConverter& tc, const ImpactParameterConverter& ip, TrackEcalHitPoint& tehp, const CaloTowerConverter& ctc,
                           const EcalClusterConverter& ecc,
                           const TransientTrackBuilder& builder, const TauJetCorrector& tjc):
        trackConverter(tc),
        ipConverter(ip),
        trackEcalHitPoint(tehp),
        caloTowerConverter(ctc),
        ecalClusterConverter(ecc),
        transientTrackBuilder(builder),
        tauJetCorrection(tjc)
{}
TauConverter::~TauConverter() {}


MyJet TauConverter::convert(const CaloTau& recTau) {
        const CaloJet& caloJet = *(recTau.caloTauTagInfoRef()->calojetRef().get());

	MyJet tau(recTau.px(), recTau.py(), recTau.pz(), recTau.energy());

	vector<MyTrack> tracks;
	vector<MyHit> hits;

	vector<TransientTrack> transientTracks;
	if(trackConverter.getCollectionLabel() == "iterativeTracks") {
	  vector<Trajectory> associatedTrajectories;
	  vector<Track> associatedTracks = trackConverter.getTracksInCone(recTau.p4(),0.5,associatedTrajectories);
	  vector<Track>::const_iterator iTrack;
	  vector<Trajectory>::const_iterator iTrajectory = associatedTrajectories.begin();
          // Make sure, that each track has a trajectory; only this guarantees one to one correspondence
          bool myTrajectoryStatus = (associatedTracks.size() == associatedTrajectories.size());
	  int trackCounter = 0;
          for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); iTrack++){

                const TransientTrack transientTrack = transientTrackBuilder.build(*iTrack);
		transientTracks.push_back(transientTrack);

		MyTrack track = TrackConverter::convert(transientTrack);

                if (myTrajectoryStatus) {
			HitConverter::addHits(hits, *iTrajectory, trackCounter);
		}
                track.ip                = ipConverter.convert(transientTrack,caloJet);
                track.trackEcalHitPoint = trackEcalHitPoint.convert(transientTrack,caloJet);
                tracks.push_back(track);
		++iTrajectory;
		++trackCounter;
          }
	}else{
	  // at this point, adding MyHit information is not implemented for calotau data
	  const TrackRefVector associatedTracks = recTau.caloTauTagInfoRef()->Tracks();
	  RefVector<TrackCollection>::const_iterator iTrack;
	  for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); iTrack++){

                const TransientTrack transientTrack = transientTrackBuilder.build(*iTrack);

                MyTrack track           = TrackConverter::convert(transientTrack);
                track.ip                = ipConverter.convert(transientTrack,caloJet);
                track.trackEcalHitPoint = trackEcalHitPoint.convert(transientTrack,caloJet);
                tracks.push_back(track);
          }
	}

        tau.tracks = tracks;
	tau.hits   = hits;

        tag(recTau, tau.tagInfo);

        // Jet energy correction
        double jetEnergyCorrectionFactor = tauJetCorrection.correction(recTau.p4());
        tau.addEnergyCorrection("TauJet",jetEnergyCorrectionFactor);

        caloTowerConverter.convert(caloJet, tau.caloInfo);

	VertexConverter::addSecondaryVertices(transientTracks, tau.secVertices);

	ecalClusterConverter.addClusters(&tau);

        return tau;
}

MyJet TauConverter::convert(const IsolatedTauTagInfo& recTau) {
        const CaloJet& caloJet = *(dynamic_cast<const CaloJet*>(recTau.jet().get()));

        MyJet tau(caloJet.px(), caloJet.py(), caloJet.pz(), caloJet.energy());

	const TrackRefVector associatedTracks = recTau.allTracks();
	RefVector<TrackCollection>::const_iterator iTrack;
	vector<MyTrack> tracks;
	for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); iTrack++){

                const TransientTrack transientTrack = transientTrackBuilder.build(*iTrack);

		MyTrack track           = TrackConverter::convert(transientTrack);
		track.ip                = ipConverter.convert(transientTrack,caloJet);
		track.trackEcalHitPoint = trackEcalHitPoint.convert(transientTrack,caloJet);
		tracks.push_back(track);
	}
	tau.tracks = tracks;

        TauConverter::tag(recTau, tau.tagInfo);

        // FIXME
        // no secondary vertices?

        caloTowerConverter.convert(caloJet, tau.caloInfo);

	ecalClusterConverter.addClusters(&tau);

        return tau;
}

MyJet TauConverter::convert(const pat::Tau& recTau) {
        MyJet tau(recTau.px(), recTau.py(), recTau.pz(), recTau.energy());

        vector<MyTrack> tracks;
        const PFCandidateRefVector pfSignalCandidates = recTau.signalPFCands();

	vector<TransientTrack> transientTracks;
        RefVector<PFCandidateCollection>::const_iterator iTrack;
        for(iTrack = pfSignalCandidates.begin(); iTrack!= pfSignalCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		const TransientTrack transientTrack = transientTrackBuilder.build(pfCand.trackRef());
                transientTracks.push_back(transientTrack);

                MyTrack track = TrackConverter::convert(pfCand);
                // FIXME
                // no impact parameter?
                // no ECAL hit point?
                tracks.push_back(track);
        }

        const PFCandidateRefVector pfIsolCandidates = recTau.isolationPFCands();
        for(iTrack = pfIsolCandidates.begin(); iTrack!= pfIsolCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		const TransientTrack transientTrack = transientTrackBuilder.build(pfCand.trackRef());
                transientTracks.push_back(transientTrack);

                MyTrack track = TrackConverter::convert(pfCand);
                // FIXME
                // no impact parameter?
                // no ECAL hit point?
                tracks.push_back(track);
        }

        tau.tracks = tracks;

        TauConverter::tag(recTau, tau.tagInfo);

	VertexConverter::addSecondaryVertices(transientTracks, tau.secVertices);

        // FIXME
        // no calotowers?

	ecalClusterConverter.addClusters(&tau);

	return tau;
}

MyJet TauConverter::convert(const PFTau& recTau) {
	MyJet tau(recTau.px(), recTau.py(), recTau.pz(), recTau.energy());

	vector<MyTrack> tracks;
        const PFCandidateRefVector pfSignalCandidates = recTau.signalPFCands();

	vector<TransientTrack> transientTracks;
        RefVector<PFCandidateCollection>::const_iterator iTrack;
        for(iTrack = pfSignalCandidates.begin(); iTrack!= pfSignalCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		if(pfCand.trackRef().isNonnull()){
                  const TransientTrack transientTrack = transientTrackBuilder.build(pfCand.trackRef());
                  transientTracks.push_back(transientTrack);
		}
		MyTrack track = TrackConverter::convert(pfCand);
		track.trackEcalHitPoint = TrackEcalHitPoint::convert(pfCand);
                // FIXME
                // no impact parameter?
                tracks.push_back(track);
        }

        const PFCandidateRefVector pfIsolCandidates = recTau.isolationPFCands();
        for(iTrack = pfIsolCandidates.begin(); iTrack!= pfIsolCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		if(pfCand.trackRef().isNonnull()){
                  const TransientTrack transientTrack = transientTrackBuilder.build(pfCand.trackRef());
                  transientTracks.push_back(transientTrack);
		}
                MyTrack track = TrackConverter::convert(pfCand);
		track.trackEcalHitPoint = TrackEcalHitPoint::convert(pfCand);
                // FIXME
                // no impact parameter?
                tracks.push_back(track);
        }

        tau.tracks = tracks;

        TauConverter::tag(recTau, tau.tagInfo);

	VertexConverter::addSecondaryVertices(transientTracks, tau.secVertices);

        // FIXME
        // no calotowers?

	ecalClusterConverter.addClusters(&tau);

	return tau;	
}


void TauConverter::tag(const IsolatedTauTagInfo& jet, TagType& tagInfo){
        const double matchingConeSize         = 0.1,
               signalConeSize           = 0.07,
               isolationConeSize        = 0.4,
               ptLeadingTrackMin        = 20,
               ptOtherTracksMin         = 1;

        tagInfo["discriminator"] = 
		jet.discriminator(matchingConeSize,
				  signalConeSize,
                                  isolationConeSize,
                                  ptLeadingTrackMin,
                                  ptOtherTracksMin);
}

void TauConverter::tag(const CaloTau& tau, TagType& tagInfo){
	CaloTau theCaloTau = tau;
	CaloTauElementsOperators theCaloTauElementsOperators(theCaloTau);

        const double matchingConeSize         = 0.1,
               signalConeSize           = 0.07,
               isolationConeSize        = 0.4,
               ptLeadingTrackMin        = 20,
               ptOtherTracksMin         = 1;
        string metric = "DR"; // can be DR,angle,area
        unsigned int isolationAnnulus_Tracksmaxn = 0;

//	double d_trackIsolation = theCaloTauElementsOperators.discriminatorByIsolTracksN(0);
	double d_trackIsolation = theCaloTauElementsOperators.discriminatorByIsolTracksN(
                                metric,
                                matchingConeSize,
                                ptLeadingTrackMin,
                                ptOtherTracksMin,
                                metric,
                                signalConeSize,
                                metric,
                                isolationConeSize,
                                isolationAnnulus_Tracksmaxn);

        tagInfo["d_trackIsolation"]   = d_trackIsolation;
/*
	double d_leadingTrack = 1;
	if(!theCaloTau.leadTrack()) d_leadingTrack = 0;
        tagInfo["d_leadingTrack"]     = d_leadingTrack;
*/
}

void TauConverter::tag(const pat::Tau& tau, TagType& tagInfo){
	const vector< pair<string,float> > IDs = tau.tauIDs();
        for(vector< pair<string,float> >::const_iterator i = IDs.begin(); i!= IDs.end(); ++i){
                tagInfo[i->first] = i->second;
        }

        tagInfo["pat:trackIso"]           = tau.trackIso();
        tagInfo["pat:caloIso"]            = tau.caloIso();
        tagInfo["pat:ecalIso"]            = tau.ecalIso();
        tagInfo["pat:hcalIso"]            = tau.hcalIso();

        tagInfo["pat:particleIso"]        = tau.particleIso();       //all the PFCandidates
        tagInfo["pat:chargedHadronIso"]   = tau.chargedHadronIso();//charged PFCandidates
        tagInfo["pat:neutralHadronIso"]   = tau.neutralHadronIso();//neutral hadrons PFCandidates
        tagInfo["pat:photonIso"]          = tau.photonIso();  //gamma PFCandidates
}

void TauConverter::tag(const PFTau& tau, TagType& tagInfo){
	PFTau thePFTau = tau;
	PFTauElementsOperators thePFTauElementsOperators(thePFTau);

        const double matchingConeSize         = 0.1,
               signalConeSize           = 0.07,
               isolationConeSize        = 0.4,
               ptLeadingTrackMin        = 20,
               ptOtherTracksMin         = 1,
	       useOnlyChargedHadrforleadPFCand	= true,
	       IsolPFCands_maxEtSum	= 0;
        string metric = "DR"; // can be DR,angle,area
        unsigned int isolationAnnulus_Tracksmaxn = 0,
		     IsolPFCands_maxN = 0;

//	double d_trackIsolation   = thePFTauElementsOperators.discriminatorByIsolTracksN(0);
	double d_trackIsolation = thePFTauElementsOperators.discriminatorByIsolTracksN(
                                metric,
                                matchingConeSize,
                                ptLeadingTrackMin,
                                ptOtherTracksMin,
                                metric,
                                signalConeSize,
                                metric,
                                isolationConeSize,
                                isolationAnnulus_Tracksmaxn);
        tagInfo["d_trackIsolation"]   = d_trackIsolation;

	double d_pftrackIsolation = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN(0);
        tagInfo["d_pftrackIsolation"] = d_pftrackIsolation;

	double d_ecalIsolation = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN(0);
        tagInfo["d_ecalIsolation"]    = d_ecalIsolation;

	double d_IsolPFCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFCandsEtSum (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
        tagInfo["d_IsolPFCandsEtSum_1"] = d_IsolPFCandsEtSum_1;

// second discrimintor d_IsolPFCandsEtSum
	double d_IsolPFCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFCandsEtSum (metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
        tagInfo["d_IsolPFCandsEtSum_2"] = d_IsolPFCandsEtSum_2;

// third discrimintor d_IsolPFCandsEtSum
	double d_IsolPFCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFCandsEtSum (IsolPFCands_maxEtSum);
        tagInfo["d_IsolPFCandsEtSum_3"] = d_IsolPFCandsEtSum_3;



	double d_IsolPFCandsN_1  = thePFTauElementsOperators.discriminatorByIsolPFCandsN(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFCandsN_1"] = d_IsolPFCandsN_1;

//Second discriminator d_IsolPFCandsN, can't be used simultanieosly

double d_IsolPFCandsN_2  = thePFTauElementsOperators.discriminatorByIsolPFCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFCandsN_2"] = d_IsolPFCandsN_2;


//Third d_IsolPFCandsN discriminator

double d_IsolPFCandsN_3  = thePFTauElementsOperators.discriminatorByIsolPFCandsN  ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFCandsN_3"] = d_IsolPFCandsN_3;

	double 	d_IsolPFChargedHadrCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsEtSum 					(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFChargedHadrCandsEtSum_1"] = d_IsolPFChargedHadrCandsEtSum_1;

// Second discriminator d_IsolPFChargedHadrCandsEtSum

	double 	d_IsolPFChargedHadrCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsEtSum(
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFChargedHadrCandsEtSum_2"] = d_IsolPFChargedHadrCandsEtSum_2;	

// Third discriminator d_IsolPFChargedHadrCandsEtSum

double 	d_IsolPFChargedHadrCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsEtSum (
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFChargedHadrCandsEtSum_3"] = d_IsolPFChargedHadrCandsEtSum_3;


double 	d_IsolPFGammaCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsEtSum (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFGammaCandsEtSum_1"] = d_IsolPFGammaCandsEtSum_1;

//Second discriminator d_IsolPFGammaCandsEtSum

double 	d_IsolPFGammaCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsEtSum (
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFGammaCandsEtSum_2"] = d_IsolPFGammaCandsEtSum_2;


//Third discriminator d_IsolPFGammaCandsEtSum

double 	d_IsolPFGammaCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsEtSum (
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFGammaCandsEtSum_3"] = d_IsolPFGammaCandsEtSum_3;


	double d_IsolPFChargedHadrCandsN_1  = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN 					(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFChargedHadrCandsN_1"] = d_IsolPFChargedHadrCandsN_1;

//Second discriminator d_IsolPFChargedHadrCandsN

double d_IsolPFChargedHadrCandsN_2  = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFChargedHadrCandsN_2"] = d_IsolPFChargedHadrCandsN_2;


//Third d_IsolPFCandsN discriminator
double d_IsolPFChargedHadrCandsN_3  = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN  ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFChargedHadrCandsN_3"] = d_IsolPFChargedHadrCandsN_3;


double 	d_IsolPFNeutrHadrCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsEtSum 					(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFNeutrHadrCandsEtSum_1"] = d_IsolPFNeutrHadrCandsEtSum_1;

//Second discriminator d_IsolPFNeutrHadrCandsEtSum
double 	d_IsolPFNeutrHadrCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsEtSum (
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFNeutrHadrCandsEtSum_2"] = d_IsolPFNeutrHadrCandsEtSum_2;

//Third discriminator d_IsolPFNeutrHadrCandsEtSum
double 	d_IsolPFNeutrHadrCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsEtSum (
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFNeutrHadrCandsEtSum_3"] = d_IsolPFNeutrHadrCandsEtSum_3;



double d_IsolPFGammaCandsN_1  = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFGammaCandsN_1"] = d_IsolPFGammaCandsN_1;

//Second discriminator d_IsolPFGammaCandsN
double d_IsolPFGammaCandsN_2  = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFGammaCandsN_2"] = d_IsolPFGammaCandsN_2;


//Third d_IsolPFCandsN discriminator
double d_IsolPFGammaCandsN_3  = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN  ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFGammaCandsN_3"] = d_IsolPFGammaCandsN_3;



double d_IsolPFNeutrHadrCandsN_1 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsN (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFNeutrHadrCandsN_1"] = d_IsolPFNeutrHadrCandsN_1;

//Second discriminator d_IsolPFNeutrHadrCandsN
double d_IsolPFNeutrHadrCandsN_2 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFNeutrHadrCands_2"] = d_IsolPFNeutrHadrCandsN_2;

//Third d_IsolPFNeutrHadrCandsN discriminator
double d_IsolPFNeutrHadrCandsN_3 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsN ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFNeutrHadrCandsN_3"] = d_IsolPFNeutrHadrCandsN_3;



//----------------------------------------------------------------
//------------------end of discriminators-------------------------
//----------------------------------------------------------------

/*
	double d_leadingTrack = 1;
	if(!thePFTau.leadTrack()) d_leadingTrack = 0;
        tagInfo["d_leadingTrack"]     = d_leadingTrack;

        double d_leadingPFTrack = 1;
        if(!thePFTau.leadPFChargedHadrCand()) d_leadingPFTrack = 0;
        tagInfo["d_leadingPFTrack"]   = d_leadingPFTrack;
*/
/*
	cout << "check MyEventConverter::tauTag " << d_trackIsolation << " " 
		<< d_pftrackIsolation << " "
		<< d_ecalIsolation << " "
		<< d_leadingTrack << " "
		<< d_leadingPFTrack << endl;
*/
/*
        double Rmatch  = 0.1,
               Rsignal = 0.07,
               Riso    = 0.4,
               pT_LT   = 6,
               pT_min  = 1;

        tagInfo["discriminator"] =
                jet.discriminatorByIsolPFChargedHadrCandsN(Rmatch,
                                                           Rsignal,
                                                           Riso,
                                                           true,
                                                           pT_LT,
                                                           pT_min);
*/
}

