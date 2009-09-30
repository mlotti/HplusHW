#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PhotonTag.h"

#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"

void PhotonTag::tag(const reco::Photon* photon, TagType& tagInfo){
/*
	tagInfo["e5x5"]		= photon->e5x5();
	tagInfo["r19"]		= photon->r19();
	tagInfo["r9"]		= photon->r9();	
*/
/** 210_pre8 DQMOffline/EGamma/src/PhotonAnalyzer.cc
    float e3x3=   EcalClusterTools::e3x3(  *(   (*iPho).superCluster()->seed()  ), &ecalRecHitCollection, &(*topology));
    float r9 =e3x3/( (*iPho).superCluster()->rawEnergy()+ (*iPho).superCluster()->preshowerEnergy());
*/
/*
	tagInfo["EoverPIn"]      = electron->eSuperClusterOverP();
        tagInfo["DeltaEtaIn"]    = electron->deltaEtaSuperClusterTrackAtVtx();
        tagInfo["DeltaPhiIn"]    = electron->deltaPhiSuperClusterTrackAtVtx();
        tagInfo["HoverE"]        = electron->hadronicOverEm();
        tagInfo["EoverPOut"]     = electron->eSeedClusterOverPout();
        tagInfo["DeltaPhiOut"]   = electron->deltaPhiSuperClusterTrackAtVtx();
        tagInfo["InvEMinusInvP"] = (1./electron->caloEnergy())-(1./electron->trackMomentumAtVtx().R());
        tagInfo["BremFraction"]  = electron->trackMomentumAtVtx().R()-electron->trackMomentumOut().R();

//	const reco::ClusterShapeRef& shapeRef = getClusterShape(electron,iEvent);
        tagInfo["E9overE25"]     = shapeRef->e3x3()/shapeRef->e5x5();
        tagInfo["SigmaEtaEta"]   = shapeRef->covEtaEta();
        tagInfo["SigmaPhiPhi"]   = shapeRef->covPhiPhi();
*/
}

void PhotonTag::tag(const reco::Conversion* photon, TagType& tagInfo){
	tagInfo["EoverP"]     		= photon->EoverP();
	tagInfo["nTracks"]     		= photon->nTracks();
        tagInfo["pairCotThetaSeparation"] = photon->pairCotThetaSeparation();
        tagInfo["pairInvariantMass"] 	= photon->pairInvariantMass();
//        tagInfo["pairMomentumX"] 	= photon->pairMomentum().x();
//        tagInfo["pairMomentumY"]        = photon->pairMomentum().y();
//        tagInfo["pairMomentumZ"]        = photon->pairMomentum().z();
	tagInfo["zOfPrimaryVertexFromTracks"] = photon->zOfPrimaryVertexFromTracks();
//        tagInfo["pairPtOverEtSC"] 	= photon->pairPtOverEtSC();
//        tagInfo["r9"]           	= photon->r9();
}
