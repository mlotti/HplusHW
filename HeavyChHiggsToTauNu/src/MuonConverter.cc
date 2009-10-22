#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

using reco::TrackRef;
using reco::TransientTrack;

MuonConverter::MuonConverter(const TransientTrackBuilder& builder, const ImpactParameterConverter& ip):
        transientTrackBuilder(builder),
        ipConverter(ip)
{}
MuonConverter::~MuonConverter() {}

template <class T>
MyJet MuonConverter::helper(const T& recMuon) const {
        MyJet muon(recMuon.px(), recMuon.py(), recMuon.pz(), recMuon.p()); // FIXME: should we use .energy() instead of .p()?
        muon.type = 13 * recMuon.charge();

	TrackRef track = recMuon.globalTrack();
	if(track.isNull()) track = recMuon.innerTrack();
	if(track.isNull()) track = recMuon.combinedMuon();

	if(track.isNonnull()){
		const TransientTrack transientTrack = transientTrackBuilder.build(track);

		MyTrack muonTrack = TrackConverter::convert(transientTrack);
		muonTrack.ip = ipConverter.convert(transientTrack);
		muon.tracks.push_back(muonTrack);

                // FIXME
		//muon.tracks = getTracks(muon);
	}

        tag(recMuon, muon.tagInfo);

	return muon;
}

MyJet MuonConverter::convert(const reco::Muon& recMuon) const {
        return helper(recMuon);
}

MyJet MuonConverter::convert(const pat::Muon& recMuon) const {
        return helper(recMuon);
}


template <class T>
void MuonConverter::tagHelper(const T& muon, TagType& tagInfo) const {
	const reco::MuonIsolation& isolationR03 = muon.isolationR03();
        const reco::MuonIsolation& isolationR05 = muon.isolationR05();

	tagInfo["isolationR03.emEt"]    = isolationR03.emEt;
        tagInfo["isolationR03.hadEt"]   = isolationR03.hadEt;
        tagInfo["isolationR03.hoEt"]    = isolationR03.hoEt;
        tagInfo["isolationR03.nJets"]   = isolationR03.nJets;
        tagInfo["isolationR03.nTracks"] = isolationR03.nTracks;
        tagInfo["isolationR03.sumPt"]   = isolationR03.sumPt;

        tagInfo["isolationR05.emEt"]    = isolationR05.emEt;
        tagInfo["isolationR05.hadEt"]   = isolationR05.hadEt;
        tagInfo["isolationR05.hoEt"]    = isolationR05.hoEt;
        tagInfo["isolationR05.nJets"]   = isolationR05.nJets;
        tagInfo["isolationR05.nTracks"] = isolationR05.nTracks;
        tagInfo["isolationR05.sumPt"]   = isolationR05.sumPt;
}

void MuonConverter::tag(const reco::Muon& muon, TagType& tagInfo) const {
        tagHelper(muon, tagInfo);
}

void MuonConverter::tag(const pat::Muon& muon, TagType& tagInfo) const {
        tagHelper(muon, tagInfo);

/* not working, no member function muonIDs() (yet?) 
        const vector< pair<string,float> > IDs = muon.muonIDs();
        for(vector< pair<string,float> >::const_iterator i = IDs.begin();
            i!= IDs.end(); ++i){
                tagInfo[i->first] = i->second;
        }
*/
	tagInfo["pat:trackIso"]		  = muon.trackIso();
	tagInfo["pat:caloIso"]		  = muon.caloIso();
	tagInfo["pat:ecalIso"]		  = muon.ecalIso();
	tagInfo["pat:hcalIso"]		  = muon.hcalIso();

	tagInfo["pat:particleIso"]        = muon.particleIso();       //all the PFCandidates
	tagInfo["pat:chargedHadronIso"]   = muon.chargedHadronIso();//charged PFCandidates
	tagInfo["pat:neutralHadronIso"]   = muon.neutralHadronIso();//neutral hadrons PFCandidates
        tagInfo["pat:photonIso"]	  = muon.photonIso();  //gamma PFCandidates
}

