#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

//map<string,double> MyEventConverter::etag(const GsfElectron* electron,const ClusterShapeRef& shapeRef,map<string,double> tagInfo){
map<string,double> MyEventConverter::etag(const GsfElectron* electron,EcalClusterLazyTools& myEcalCluster,map<string,double> tagInfo){

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
	return tagInfo;
}
