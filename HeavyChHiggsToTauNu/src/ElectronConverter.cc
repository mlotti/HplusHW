#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackEcalHitPoint.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

using std::vector;
using std::string;
using std::pair;

using reco::GsfTrackRef;
using reco::TransientTrack;

ElectronConverter::ElectronConverter(const TransientTrackBuilder& builder, const ImpactParameterConverter& ip, EcalClusterLazyTools& tools,
                                     const edm::Event& event, const std::vector<edm::InputTag>& labels):
  transientTrackBuilder(builder),
  ipConverter(ip),
  clusterTools(tools),
  iEvent(event),
  tagLabels(labels)
{}
ElectronConverter::~ElectronConverter() {}

template<class T>
MyJet ElectronConverter::helper(const edm::Ref<edm::View<T> >& iElectron) {
        const T& recElectron = *iElectron;

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

	electron.clusters.push_back(TLorentzVector(recElectron.superCluster()->x(),
                                                   recElectron.superCluster()->y(),
                                                   recElectron.superCluster()->z(),
                                                   recElectron.superCluster()->energy()));
	tag(iElectron, electron.tagInfo);

        return electron;
}

MyJet ElectronConverter::convert(edm::Handle<edm::View<reco::GsfElectron> >& handle, size_t i) {
        return helper(edm::Ref<edm::View<reco::GsfElectron> >(handle, i));
}

MyJet ElectronConverter::convert(edm::Handle<edm::View<pat::Electron> >& handle, size_t i) {
        return helper(edm::Ref<edm::View<pat::Electron> >(handle, i));
}

void ElectronConverter::tag(const edm::Ref<edm::View<reco::GsfElectron> >& iElectron, TagType& tagInfo) {
        const reco::GsfElectron& electron = *iElectron;

        edm::Handle<edm::ValueMap<float> > electronIdHandle;
        for(unsigned int ietag = 0; ietag < tagLabels.size(); ++ietag){
                iEvent.getByLabel(tagLabels[ietag], electronIdHandle );

                const edm::ValueMap<float>& electronId = *electronIdHandle;

                tagInfo[tagLabels[ietag].label()] = electronId[iElectron];
        }

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

void ElectronConverter::tag(const edm::Ref<edm::View<pat::Electron> >& iElectron, TagType& tagInfo) {
        const pat::Electron& electron = *iElectron;

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
