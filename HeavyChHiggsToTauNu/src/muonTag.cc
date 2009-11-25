#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

map<string,double> MyEventConverter::muonTag(const reco::Muon& muon){
	map<string,double> tagInfo;

	const MuonIsolation isolationR03 = muon.isolationR03();
        const MuonIsolation isolationR05 = muon.isolationR05();

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

        tagInfo["isGlobal"]     = muon.isGlobalMuon()     ? 1 : 0;
        tagInfo["isStandAlone"] = muon.isStandAloneMuon() ? 1 : 0;
        tagInfo["isTracker"]    = muon.isTrackerMuon()    ? 1 : 0;

	return tagInfo;
}

map<string,double> MyEventConverter::muonTag(const pat::Muon& muon){
        map<string,double> tagInfo;

        const MuonIsolation isolationR03 = muon.isolationR03();
        const MuonIsolation isolationR05 = muon.isolationR05();

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

        tagInfo["isGlobal"]     = muon.isGlobalMuon()     ? 1 : 0;
        tagInfo["isStandAlone"] = muon.isStandAloneMuon() ? 1 : 0;
        tagInfo["isTracker"]    = muon.isTrackerMuon()    ? 1 : 0;

        return tagInfo;
}

