#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

map<string,double> MyEventConverter::muonTag(const Muon& muon){
	map<string,double> tagInfo;

	const MuonIsolation isolationR03 = muon.getIsolationR03();
        const MuonIsolation isolationR05 = muon.getIsolationR05();

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

	return tagInfo;
}
