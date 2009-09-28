#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronTag.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"

#include<vector>

using std::vector;
using std::string;
using std::pair;

void ElectronTag::tag(const reco::GsfElectron *electron, EcalClusterLazyTools& myEcalCluster, TagType& tagInfo){

	tagInfo["EoverPIn"]      = electron->eSuperClusterOverP();
        tagInfo["DeltaEtaIn"]    = electron->deltaEtaSuperClusterTrackAtVtx();
        tagInfo["DeltaPhiIn"]    = electron->deltaPhiSuperClusterTrackAtVtx();
        tagInfo["HoverE"]        = electron->hadronicOverEm();
        tagInfo["EoverPOut"]     = electron->eSeedClusterOverPout();
        tagInfo["DeltaPhiOut"]   = electron->deltaPhiSuperClusterTrackAtVtx();
        tagInfo["InvEMinusInvP"] = (1./electron->caloEnergy())-(1./electron->trackMomentumAtVtx().R());
        tagInfo["BremFraction"]  = electron->trackMomentumAtVtx().R()-electron->trackMomentumOut().R();

	tagInfo["E9overE25"]     = myEcalCluster.e3x3(*(electron->superCluster()->seed()))/
                                   myEcalCluster.e5x5(*(electron->superCluster()->seed()));
	vector<float> vCov       = myEcalCluster.covariances(*(electron->superCluster()->seed()));
	tagInfo["SigmaEtaEta"]   = sqrt (vCov[0]);
	tagInfo["SigmaPhiPhi"]   = sqrt (vCov[1]);
/*
        tagInfo["E9overE25"]     = shapeRef->e3x3()/shapeRef->e5x5();
        tagInfo["SigmaEtaEta"]   = shapeRef->covEtaEta();
        tagInfo["SigmaPhiPhi"]   = shapeRef->covPhiPhi();
*/
}

void ElectronTag::tag(const pat::Electron& electron, TagType& tagInfo) {
	const vector< pair<string,float> > electronIDs = electron.electronIDs();
	for(vector< pair<string,float> >::const_iterator i = electronIDs.begin();
	    i!= electronIDs.end(); ++i){
		tagInfo[i->first] = i->second;
	}

        tagInfo["pat:trackIso"]           = electron.trackIso();
        tagInfo["pat:caloIso"]            = electron.caloIso();
        tagInfo["pat:ecalIso"]            = electron.ecalIso();
        tagInfo["pat:hcalIso"]            = electron.hcalIso();

        tagInfo["pat:particleIso"]        = electron.particleIso();       //all the PFCandidates
        tagInfo["pat:chargedHadronIso"]   = electron.chargedHadronIso();//charged PFCandidates
        tagInfo["pat:neutralHadronIso"]   = electron.neutralHadronIso();//neutral hadrons PFCandidates
        tagInfo["pat:photonIso"]          = electron.photonIso();  //gamma PFCandidates
}
