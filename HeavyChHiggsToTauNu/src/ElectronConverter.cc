#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackEcalHitPoint.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

using std::vector;
using std::string;
using std::pair;

using reco::GsfTrackRef;
using reco::TransientTrack;

ElectronConverter::ElectronConverter(const TransientTrackBuilder& builder, const ImpactParameterConverter& ip, EcalClusterLazyTools& tools):
  transientTrackBuilder(builder),
  ipConverter(ip),
  clusterTools(tools)
{}
ElectronConverter::~ElectronConverter() {}

MyJet ElectronConverter::convert(const reco::GsfElectron& recElectron) const {
	GsfTrackRef track = recElectron.gsfTrack();
        const TransientTrack transientTrack = transientTrackBuilder.build(track);

        MyJet electron(recElectron.px(), recElectron.py(), recElectron.pz(), recElectron.p()); // FIXME: should we use .energy() instead of .p()?
        electron.type = 11 * (*track).charge();

	MyTrack electronTrack = TrackConverter::convert(transientTrack);
	electronTrack.ip = ipConverter.convert(transientTrack);
	electronTrack.trackEcalHitPoint = TrackEcalHitPoint::convert(recElectron);
	electron.tracks.push_back(electronTrack);
        // FIXME
        //electron.tracks = getTracks(electron);

	vector<TLorentzVector> superClusters;
	superClusters.push_back(TLorentzVector(recElectron.superCluster()->x(),
	                                       recElectron.superCluster()->y(),
                                               recElectron.superCluster()->z(),
                                               recElectron.superCluster()->energy()));
	electron.clusters = superClusters;

        return electron;
}

MyJet ElectronConverter::convert(const pat::Electron& recElectron) const {
        GsfTrackRef track = recElectron.gsfTrack();
        const TransientTrack transientTrack = transientTrackBuilder.build(track);

	MyJet electron(recElectron.px(), recElectron.py(), recElectron.pz(), recElectron.p()); // FIXME: should we use .energy() instead of .p()?
	electron.type = 11 * (*track).charge();

        MyTrack electronTrack = TrackConverter::convert(transientTrack);
        electronTrack.ip = ipConverter.convert(transientTrack);
	electronTrack.trackEcalHitPoint = TrackEcalHitPoint::convert(recElectron);
        electron.tracks.push_back(electronTrack);
        // FIXME
        //electron.tracks = getTracks(electron);

        vector<TLorentzVector> superClusters;
        superClusters.push_back(TLorentzVector(recElectron.superCluster()->x(),
                                               recElectron.superCluster()->y(),
                                               recElectron.superCluster()->z(),
                                               recElectron.superCluster()->energy()));
        electron.clusters = superClusters;

	tag(recElectron, electron.tagInfo);

	return electron;
}

void ElectronConverter::tag(const reco::GsfElectron& electron, TagType& tagInfo) {

	tagInfo["EoverPIn"]      = electron.eSuperClusterOverP();
        tagInfo["DeltaEtaIn"]    = electron.deltaEtaSuperClusterTrackAtVtx();
        tagInfo["DeltaPhiIn"]    = electron.deltaPhiSuperClusterTrackAtVtx();
        tagInfo["HoverE"]        = electron.hadronicOverEm();
        tagInfo["EoverPOut"]     = electron.eSeedClusterOverPout();
        tagInfo["DeltaPhiOut"]   = electron.deltaPhiSuperClusterTrackAtVtx();
        tagInfo["InvEMinusInvP"] = (1./electron.caloEnergy())-(1./electron.trackMomentumAtVtx().R());
        tagInfo["BremFraction"]  = electron.trackMomentumAtVtx().R()-electron.trackMomentumOut().R();

	tagInfo["E9overE25"]     = clusterTools.e3x3(*(electron.superCluster()->seed()))/
                                   clusterTools.e5x5(*(electron.superCluster()->seed()));
	vector<float> vCov       = clusterTools.covariances(*(electron.superCluster()->seed()));
	tagInfo["SigmaEtaEta"]   = sqrt (vCov[0]);
	tagInfo["SigmaPhiPhi"]   = sqrt (vCov[1]);
/*
        tagInfo["E9overE25"]     = shapeRef->e3x3()/shapeRef->e5x5();
        tagInfo["SigmaEtaEta"]   = shapeRef->covEtaEta();
        tagInfo["SigmaPhiPhi"]   = shapeRef->covPhiPhi();
*/
}

void ElectronConverter::tag(const pat::Electron& electron, TagType& tagInfo) const {
	const vector<pat::Electron::IdPair>& electronIDs = electron.electronIDs();
	for(vector<pat::Electron::IdPair>::const_iterator i = electronIDs.begin();
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
