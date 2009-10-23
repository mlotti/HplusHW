
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HitConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauConverter.h"

MyJet MyEventConverter::myJetConverter(const CaloJet& caloJet){

        MyJet jet(caloJet.px(), caloJet.py(), caloJet.pz(), caloJet.energy());
        // FIXME
        //jet.tracks = getTracks(jet);

        // Jet energy corrections
        for(unsigned int i = 0; i < jetEnergyCorrectionTypes.size(); ++i){
                double jetEnergyCorrectionFactor = jetEnergyCorrections[i]->correction(caloJet);
                string jetEnergyCorrectionName = jetEnergyCorrectionTypes[i].label();
                jet.addEnergyCorrection(jetEnergyCorrectionName,jetEnergyCorrectionFactor);
		cout << "    jet correction " << jetEnergyCorrectionName << " " 
                                              << jetEnergyCorrectionFactor << endl;
        }

        return jet;
}

MyJet MyEventConverter::myJetConverter(const pat::Jet& recoJet){

        MyJet jet(recoJet.px(), recoJet.py(), recoJet.pz(), recoJet.energy());
        // FIXME
        //jet.tracks = getTracks(jet);

	return jet;
}

MyJet MyEventConverter::myJetConverter(const JetTag& recJet){
        const CaloJet* caloJet = dynamic_cast<const CaloJet*>(recJet.first.get());
        return myJetConverter(*caloJet);
}

MyJet MyEventConverter::myJetConverter(const IsolatedTauTagInfo& recTau){

        const CaloJet& caloJet = *(dynamic_cast<const CaloJet*>(recTau.jet().get()));

        MyJet tau(caloJet.px(), caloJet.py(), caloJet.pz(), caloJet.energy());

	const TrackRefVector associatedTracks = recTau.allTracks();
	RefVector<TrackCollection>::const_iterator iTrack;
	vector<MyTrack> tracks;
	for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); iTrack++){

                const TransientTrack transientTrack = transientTrackBuilder->build(*iTrack);

		MyTrack track           = TrackConverter::convert(transientTrack);
		track.ip                = ImpactParameterConverter(primaryVertex).convert(transientTrack,caloJet);
		track.trackEcalHitPoint = trackEcalHitPoint.convert(transientTrack,caloJet);
		tracks.push_back(track);
	}
	tau.tracks = tracks;

        TauConverter::tag(recTau, tau.tagInfo);

        // FIXME
	//tau.caloInfo = caloTowers(caloJet);

	addECALClusters(&tau);

        return tau;
}

MyJet MyEventConverter::myJetConverter(const pat::Tau& recTau){

        MyJet tau(recTau.px(), recTau.py(), recTau.pz(), recTau.energy());

        vector<MyTrack> tracks;
        const PFCandidateRefVector pfSignalCandidates = recTau.signalPFCands();

	vector<TransientTrack> transientTracks;
        RefVector<PFCandidateCollection>::const_iterator iTrack;
        for(iTrack = pfSignalCandidates.begin(); iTrack!= pfSignalCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		const TransientTrack transientTrack = transientTrackBuilder->build(pfCand.trackRef());
                transientTracks.push_back(transientTrack);

                MyTrack track = TrackConverter::convert(pfCand);
                tracks.push_back(track);
        }

        const PFCandidateRefVector pfIsolCandidates = recTau.isolationPFCands();
        for(iTrack = pfIsolCandidates.begin(); iTrack!= pfIsolCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		const TransientTrack transientTrack = transientTrackBuilder->build(pfCand.trackRef());
                transientTracks.push_back(transientTrack);

                MyTrack track = TrackConverter::convert(pfCand);
                tracks.push_back(track);
        }

        tau.tracks = tracks;

        TauConverter::tag(recTau, tau.tagInfo);

	VertexConverter::addSecondaryVertices(transientTracks, tau.secVertices);
	addECALClusters(&tau);

	return tau;
}

MyJet MyEventConverter::myJetConverter(const PFTau& recTau){

	MyJet tau(recTau.px(), recTau.py(), recTau.pz(), recTau.energy());

	vector<MyTrack> tracks;
        const PFCandidateRefVector pfSignalCandidates = recTau.signalPFCands();

	vector<TransientTrack> transientTracks;
        RefVector<PFCandidateCollection>::const_iterator iTrack;
        for(iTrack = pfSignalCandidates.begin(); iTrack!= pfSignalCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		if(pfCand.trackRef().isNonnull()){
                  const TransientTrack transientTrack = transientTrackBuilder->build(pfCand.trackRef());
                  transientTracks.push_back(transientTrack);
		}
		MyTrack track = TrackConverter::convert(pfCand);
		track.trackEcalHitPoint = TrackEcalHitPoint::convert(pfCand);
                tracks.push_back(track);
        }

        const PFCandidateRefVector pfIsolCandidates = recTau.isolationPFCands();
        for(iTrack = pfIsolCandidates.begin(); iTrack!= pfIsolCandidates.end(); iTrack++){

                const PFCandidate& pfCand = *(iTrack->get());
		if(pfCand.trackRef().isNonnull()){
                  const TransientTrack transientTrack = transientTrackBuilder->build(pfCand.trackRef());
                  transientTracks.push_back(transientTrack);
		}
                MyTrack track = TrackConverter::convert(pfCand);
		track.trackEcalHitPoint = TrackEcalHitPoint::convert(pfCand);
                tracks.push_back(track);
        }

        tau.tracks = tracks;

        TauConverter::tag(recTau, tau.tagInfo);

	VertexConverter::addSecondaryVertices(transientTracks, tau.secVertices);
	addECALClusters(&tau);

	return tau;	
}

void MyEventConverter::addECALClusters(MyJet* jet) {
  // Loops over barrel and endcap ECAL cluster
  // and stores to jet those, which are within specified DR to
  // leading track hit point on ECAL surface

  const MyTrack *myLeadingTrack = jet->leadingTrack();
  if (!myLeadingTrack || myLeadingTrack->Pt() < 0.0001) return;
  MyGlobalPoint myECALHitPoint = myLeadingTrack->ecalHitPoint();
  //double myLdgEta = myECALHitPoint.Eta();
  //double myLdgPhi = myECALHitPoint.Phi();

  // Loop over barrel ECAL clusters
  unsigned int myBarrelCollectionSize = theBarrelBCCollection->size();
  for(unsigned int i_BC=0; i_BC != myBarrelCollectionSize; ++i_BC) { 
    BasicClusterRef theBasicClusterRef(theBarrelBCCollection, i_BC);    
    if (theBasicClusterRef.isNull()) continue;  
    if (ROOT::Math::VectorUtil::DeltaR(math::XYZPoint(myECALHitPoint), (*theBasicClusterRef).position()) <= 0.7) {
      TLorentzVector myCluster((*theBasicClusterRef).position().x(),
			       (*theBasicClusterRef).position().y(),
			       (*theBasicClusterRef).position().z(),
			       (*theBasicClusterRef).energy());
      jet->clusters.push_back(myCluster);
    }
  }
  // Loop over endcap ECAL clusters
  unsigned int myEndcapCollectionSize = theEndcapBCCollection->size();
  for(unsigned int i_BC=0; i_BC != myEndcapCollectionSize; ++i_BC) { 
    BasicClusterRef theBasicClusterRef(theEndcapBCCollection, i_BC);    
    if (theBasicClusterRef.isNull()) continue;  
    if (ROOT::Math::VectorUtil::DeltaR(math::XYZPoint(myECALHitPoint), (*theBasicClusterRef).position()) <= 0.7) {
      TLorentzVector myCluster((*theBasicClusterRef).position().x(),
			       (*theBasicClusterRef).position().y(),
			       (*theBasicClusterRef).position().z(),
			       (*theBasicClusterRef).energy());
      jet->clusters.push_back(myCluster);
    }
  }
}
