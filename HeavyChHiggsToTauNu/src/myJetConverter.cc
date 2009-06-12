
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"

MyJet MyEventConverter::myJetConverter(const Muon& recMuon){

        MyJet muon;
        muon.SetPx(recMuon.px());
        muon.SetPy(recMuon.py());
        muon.SetPz(recMuon.pz());
        muon.SetE(recMuon.p());
        muon.type = 13 * recMuon.charge();

	TrackRef track = recMuon.globalTrack();
	if(track.isNull()) track = recMuon.innerTrack();

	if(track.isNonnull()){
		const TransientTrack transientTrack = transientTrackBuilder->build(track);

		MyTrack muonTrack = myTrackConverter(transientTrack);
		muonTrack.ip = impactParameter(transientTrack);
		muon.tracks.push_back(muonTrack);

		muon.tracks = getTracks(muon);

		muon.tagInfo = muonTag(recMuon);
	}
	return muon;
}

MyJet MyEventConverter::myJetConverter(const pat::Muon& recMuon){

        MyJet muon;
        muon.SetPx(recMuon.px());
        muon.SetPy(recMuon.py());
        muon.SetPz(recMuon.pz());
        muon.SetE(recMuon.p());
        muon.type = 13 * recMuon.charge();

        TrackRef track = recMuon.globalTrack();
        if(track.isNull()) track = recMuon.innerTrack();

        if(track.isNonnull()){
                const TransientTrack transientTrack = transientTrackBuilder->build(track);

                MyTrack muonTrack = myTrackConverter(transientTrack);
                muonTrack.ip = impactParameter(transientTrack);
                muon.tracks.push_back(muonTrack);

                muon.tracks = getTracks(muon);

                muon.tagInfo = muonTag(recMuon);
        }
        return muon;
}

MyJet MyEventConverter::myJetConverter(const GsfElectron* recElectron){
	GsfTrackRef track = recElectron->gsfTrack();
        const TransientTrack transientTrack = transientTrackBuilder->build(track);

        MyJet electron;

        electron.SetPx(recElectron->px());
        electron.SetPy(recElectron->py());
        electron.SetPz(recElectron->pz());
        electron.SetE(recElectron->p());
        electron.type = 11 * (*track).charge();

	MyTrack electronTrack = myTrackConverter(transientTrack);
	electronTrack.ip = impactParameter(transientTrack);
	electron.tracks.push_back(electronTrack);
        electron.tracks = getTracks(electron);

        return electron;
}

MyJet MyEventConverter::myJetConverter(const pat::Electron& recElectron){
        GsfTrackRef track = recElectron.gsfTrack();
        const TransientTrack transientTrack = transientTrackBuilder->build(track);

	MyJet electron;

	electron.SetPx(recElectron.px());
        electron.SetPy(recElectron.py());
        electron.SetPz(recElectron.pz());
        electron.SetE(recElectron.p());
	electron.type = 11 * (*track).charge();

        MyTrack electronTrack = myTrackConverter(transientTrack);
        electronTrack.ip = impactParameter(transientTrack);
        electron.tracks.push_back(electronTrack);
        electron.tracks = getTracks(electron);

	electron.tagInfo = etag(recElectron);

	return electron;
}

MyJet MyEventConverter::myJetConverter(const Photon* recPhoton){

        MyJet photon;

        photon.SetPx(recPhoton->px());
        photon.SetPy(recPhoton->py());
        photon.SetPz(recPhoton->pz());
        photon.SetE(recPhoton->p());
        photon.type = 0; //unconverted

        photon.tracks = getTracks(photon);

	photon.tagInfo = photontag(recPhoton);

        return photon;
}

MyJet MyEventConverter::myJetConverter(const Conversion* recPhoton){

        MyJet photon;

        photon.SetPx(recPhoton->pairMomentum().x());
        photon.SetPy(recPhoton->pairMomentum().y());
        photon.SetPz(recPhoton->pairMomentum().z());
        photon.SetE(recPhoton->pairMomentum().mag());
	photon.type = 1; //converted

        vector<MyTrack> tracks;
	vector<TrackRef> associatedTracks = recPhoton->tracks();
	vector<TrackRef>::const_iterator iTrack;
        for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); ++iTrack){

                const TransientTrack transientTrack = transientTrackBuilder->build(**iTrack);

                MyTrack track           = myTrackConverter(transientTrack);
                track.ip                = impactParameter(transientTrack,recPhoton);
                track.trackEcalHitPoint = trackEcalHitPoint(transientTrack,recPhoton);
                tracks.push_back(track);
        }
        photon.tracks = tracks;

        photon.tagInfo = photontag(recPhoton);

        return photon;
}

MyJet MyEventConverter::myJetConverter(const CaloJet* caloJet){

        MyJet jet;

        jet.SetPx(caloJet->px());
        jet.SetPy(caloJet->py());
        jet.SetPz(caloJet->pz());
        jet.SetE(caloJet->energy());

        jet.tracks = getTracks(jet);

        // Jet energy corrections
        for(unsigned int i = 0; i < jetEnergyCorrectionTypes.size(); ++i){
                double jetEnergyCorrectionFactor = jetEnergyCorrections[i]->correction(*caloJet);
                string jetEnergyCorrectionName = jetEnergyCorrectionTypes[i].label();
                jet.setJetEnergyCorrection(jetEnergyCorrectionName,jetEnergyCorrectionFactor);
		cout << "    jet correction " << jetEnergyCorrectionName << " " 
                                              << jetEnergyCorrectionFactor << endl;
        }

        return jet;
}

MyJet MyEventConverter::myJetConverter(const JetTag& recJet){
        const CaloJet* caloJet = dynamic_cast<const CaloJet*>(recJet.first.get());
        return myJetConverter(caloJet);
}

MyJet MyEventConverter::myJetConverter(const IsolatedTauTagInfo& recTau){

	const CaloJet* caloJet = dynamic_cast<const CaloJet*>(recTau.jet().get());

        MyJet tau;

	tau.SetPx(caloJet->px());
        tau.SetPy(caloJet->py());
        tau.SetPz(caloJet->pz());
        tau.SetE(caloJet->energy());

	const TrackRefVector associatedTracks = recTau.allTracks();
	RefVector<TrackCollection>::const_iterator iTrack;
	vector<MyTrack> tracks;
	for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); iTrack++){

                const TransientTrack transientTrack = transientTrackBuilder->build(*iTrack);

		MyTrack track           = myTrackConverter(transientTrack);
		track.ip                = impactParameter(transientTrack,caloJet);
		track.trackEcalHitPoint = trackEcalHitPoint(transientTrack,caloJet);
		tracks.push_back(track);
	}
	tau.tracks = tracks;

        tau.tagInfo = tauTag(recTau);

	tau.caloInfo = caloTowers(*caloJet);

        return tau;
}

MyJet MyEventConverter::myJetConverter(const CaloTau& recTau){

        const CaloJet* caloJet = recTau.caloTauTagInfoRef()->calojetRef().get();

	MyJet tau;

        tau.SetPx(recTau.px());
        tau.SetPy(recTau.py());
        tau.SetPz(recTau.pz());
        tau.SetE(recTau.energy());

	vector<MyTrack> tracks;
	vector<MyHit> hits;

	vector<TransientTrack> transientTracks;
	if(trackCollectionSelection.label() == "iterativeTracks"){
	  vector<Trajectory> associatedTrajectories;
	  vector<Track> associatedTracks = tracksInCone(recTau.p4(),0.5,&associatedTrajectories);
	  vector<Track>::const_iterator iTrack;
	  vector<Trajectory>::const_iterator iTrajectory = associatedTrajectories.begin();
          // Make sure, that each track has a trajectory; only this guarantees one to one correspondence
          bool myTrajectoryStatus = (associatedTracks.size() == associatedTrajectories.size());
	  int trackCounter = 0;
          for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); iTrack++){

                const TransientTrack transientTrack = transientTrackBuilder->build(*iTrack);
		transientTracks.push_back(transientTrack);

		MyTrack track = myTrackConverter(transientTrack);

                if (myTrajectoryStatus) {
			vector<MyHit> assocHits = getHits(*iTrajectory,trackCounter);
			hits.insert(hits.end(),assocHits.begin(),assocHits.end());
		}
                track.ip                = impactParameter(transientTrack,caloJet);
                track.trackEcalHitPoint = trackEcalHitPoint(transientTrack,caloJet);
                tracks.push_back(track);
		++iTrajectory;
		++trackCounter;
          }
	}else{
	  // at this point, adding MyHit information is not implemented for calotau data
	  const TrackRefVector associatedTracks = recTau.caloTauTagInfoRef()->Tracks();
	  RefVector<TrackCollection>::const_iterator iTrack;
	  for(iTrack = associatedTracks.begin(); iTrack!= associatedTracks.end(); iTrack++){

                const TransientTrack transientTrack = transientTrackBuilder->build(*iTrack);

                MyTrack track           = myTrackConverter(transientTrack);
                track.ip                = impactParameter(transientTrack,caloJet);
                track.trackEcalHitPoint = trackEcalHitPoint(transientTrack,caloJet);
                tracks.push_back(track);
          }
	}

        tau.tracks = tracks;

	tau.hits   = hits;

        tau.tagInfo = tauTag(recTau);

        // Jet energy correction
        double jetEnergyCorrectionFactor = tauJetCorrection->correction(recTau.p4());
        tau.setJetEnergyCorrection("TauJet",jetEnergyCorrectionFactor);

        tau.caloInfo = caloTowers(*caloJet);

	tau.secVertices = secondaryVertices(transientTracks);

        return tau;
}


MyJet MyEventConverter::myJetConverter(const PFTau& recTau){

	MyJet tau;

	tau.SetPx(recTau.px());
        tau.SetPy(recTau.py());
        tau.SetPz(recTau.pz());
        tau.SetE(recTau.energy());

	vector<MyTrack> tracks;
        const PFCandidateRefVector pfSignalCandidates = recTau.signalPFCands();

        RefVector<PFCandidateCollection>::const_iterator iTrack;
        for(iTrack = pfSignalCandidates.begin(); iTrack!= pfSignalCandidates.end(); iTrack++){

                PFCandidate pfCand = **iTrack;
                MyTrack track = myTrackConverter(pfCand);
                tracks.push_back(track);
        }

        const PFCandidateRefVector pfIsolCandidates = recTau.isolationPFCands();
        for(iTrack = pfIsolCandidates.begin(); iTrack!= pfIsolCandidates.end(); iTrack++){

                PFCandidate pfCand = **iTrack;
                MyTrack track = myTrackConverter(pfCand);
                tracks.push_back(track);
        }

        tau.tracks = tracks;

        tau.tagInfo = tauTag(recTau);

	return tau;	
}
