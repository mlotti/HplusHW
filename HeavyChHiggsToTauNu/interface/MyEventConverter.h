// Class to convert edm::Event to MyEvent
// 26.10.2007/S.Lehti

#ifndef MY_EVENTCONVERTER
#define MY_EVENTCONVERTER

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "RecoEgamma/ElectronIdentification/interface/CutBasedElectronID.h"
//#include "DataFormats/EgammaReco/interface/ClusterShape.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"

#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"

#include "DataFormats/EgammaReco/interface/BasicCluster.h" 
#include "DataFormats/EgammaReco/interface/BasicClusterFwd.h" 

#include "DataFormats/BTauReco/interface/IsolatedTauTagInfo.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
//#include "DataFormats/BTauReco/interface/PFIsolatedTauTagInfo.h"
#include "DataFormats/TauReco/interface/PFTau.h"
//#include "DataFormats/TauReco/interface/PFTauDiscriminatorByIsolation.h"
#include "DataFormats/TauReco/interface/CaloTau.h"


#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/Records/interface/TransientRecHitRecord.h"
#include "TrackingTools/PatternTools/interface/Trajectory.h"
#include "TrackingTools/PatternTools/interface/TrajectoryMeasurement.h"

#include "DataFormats/BTauReco/interface/TauImpactParameterInfo.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "JetMETCorrections/TauJet/interface/TauJetCorrector.h"

#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"

#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"

#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"

#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/CaloTowers/interface/CaloTowerDetId.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/JetReco/interface/GenJet.h"

//PAT
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


#include <iostream>
using namespace std;
using namespace edm;
using namespace reco;


#include "DataFormats/BTauReco/interface/JetTag.h"


#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEvent.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyRootTree.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauResolutionAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauMETTriggerAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackEcalHitPoint.h"


////double myDeltaR(double,double,double,double);
#include "Math/VectorUtil.h"

class MyEventConverter {
  public:
	MyEventConverter(const edm::ParameterSet&);
	~MyEventConverter();

	//void cfgInput(const edm::ParameterSet&);
	void eventSetup(const edm::EventSetup&);
	void convert(const edm::Event&,const edm::EventSetup&);

  private:

// functions

	void init(const edm::ParameterSet& iConfig);

	bool triggerDecision(const edm::Event&);
	bool primaryVertexFound(const edm::Event&);
//        bool primaryVertexFound();

        MyImpactParameter 	impactParameter(const TransientTrack&,const CaloJet&);
	MyImpactParameter 	impactParameter(const TransientTrack&,const Conversion&);
        MyImpactParameter 	impactParameter(const TransientTrack&);
	MyImpactParameter 	impactParameter(const TransientTrack&,const GlobalVector&);

	void                    getTriggerResults(const edm::Event&, const edm::InputTag&, std::map<std::string, bool>&);
	vector<MyJet>		getHLTObjects(const edm::Event&);
	vector<MyJet> 		getElectrons(const edm::Event&,const edm::EventSetup&, const edm::InputTag&);
	vector<MyJet>		getPATElectrons(const edm::Event&);
        vector<MyJet>           getPhotons(const edm::Event&);
        vector<MyJet> 		getMuons(const edm::Event&, const edm::InputTag&);
	vector<MyJet>           getPATMuons(const edm::Event&);
        vector<MyJet>           getTaus(const edm::Event&, const edm::InputTag&);
	vector<MyJet>		getPATTaus(const edm::Event&);
        vector<MyJet> 		getPFTaus(const edm::Event&, const edm::InputTag&);
        vector<MyJet> 		getJets(const edm::Event&, const edm::InputTag&);
	vector<MyJet>		getPATJets(const edm::Event&);
        void                    getTracks(const edm::Event&);
        void		        getTrajectories(const edm::Event&);
	vector<MyTrack>		getTracks(MyJet&);
	vector<Track> 		tracksInCone(const math::XYZTLorentzVector,double);
	vector<Track> 		tracksInCone(const math::XYZTLorentzVector,double,vector<Trajectory>*);
	std::map<std::string, MyMET> getMET(const edm::Event&);
        std::map<std::string, MyMET> getCaloMETs(const edm::Event&);
        MyMET                   getPFMET(const edm::Event&);
        MyMET                   getTCMET(const edm::Event&);
	MyMET			getPATMET(const edm::Event&);
	MyMET 			getMetFromCaloTowers(const edm::Event&);
	void			getCaloHits(const edm::Event&);
	void			getEcalClusters(const edm::Event&);
	vector<MyJet> 		getExtraObjects(const edm::Event&);

	MyJet			myJetConverter(const reco::Muon&);
	MyJet			myJetConverter(const pat::Muon&);
        MyJet                   myJetConverter(const GsfElectron&);
	MyJet			myJetConverter(const pat::Electron&);
        MyJet                   myJetConverter(const Photon&);
        MyJet                   myJetConverter(const Conversion&);
        MyJet                   myJetConverter(const JetTag&);
	MyJet 			myJetConverter(const CaloJet&);
	MyJet			myJetConverter(const pat::Jet&);
        MyJet                   myJetConverter(const IsolatedTauTagInfo&);
        MyJet                   myJetConverter(const CaloTau&);
	MyJet			myJetConverter(const pat::Tau&);
//        MyJet                   myJetConverter(const PFIsolatedTauTagInfo&);
	MyJet 			myJetConverter(const PFTau&);
	void                    addECALClusters(MyJet* jet);

//	map<string,double> 	etag(const GsfElectron*,const ClusterShapeRef&,map<string,double>);

	vector<MyCaloTower>	caloTowers(const CaloJet&);
	const TVector3 		getCellMomentum(const CaloCellGeometry*,double&);


// datafields

        vector<InputTag> HLTSelection;
        Vertex primaryVertex;
	bool PVFound;
        InputTag trackCollectionSelection;

////        CutBasedElectronID* electronIdAlgo;
//	InputTag barrelClusterShapeAssocProducer;
//	InputTag endcapClusterShapeAssocProducer;
	InputTag reducedBarrelRecHitCollection;
	InputTag reducedEndcapRecHitCollection;
        const TransientTrackBuilder* transientTrackBuilder;
//	const TransientTrackingRecHitBuilder* TTRHBuilder;
        vector<const JetCorrector*> jetEnergyCorrections;
	const TauJetCorrector* tauJetCorrection;
        vector<InputTag> jetEnergyCorrectionTypes;
        vector<InputTag> btaggingAlgos;
	vector<InputTag> metCollections;
	vector<InputTag> electronIdLabels;
        TrackCollection tracks;

        const CaloSubdetectorGeometry* EB;
        const CaloSubdetectorGeometry* EE;
        const CaloSubdetectorGeometry* HB;
        const CaloSubdetectorGeometry* HE;
        const CaloSubdetectorGeometry* HO;
        const CaloSubdetectorGeometry* HF;

        Handle<EBRecHitCollection>   EBRecHits;
        Handle<EERecHitCollection>   EERecHits;

	// ECAL clusters
	InputTag BarrelBasicClustersInput;
	InputTag EndcapBasicClustersInput;
	Handle<BasicClusterCollection> theBarrelBCCollection;
	Handle<BasicClusterCollection> theEndcapBCCollection;
	
        Handle<HBHERecHitCollection> HBHERecHits;
        Handle<HORecHitCollection>   HORecHits;
        Handle<HFRecHitCollection>   HFRecHits;

	Handle<vector<Trajectory> > myTrajectoryCollectionHandle;
 	InputTag trajectoryInput; // Input for trajectory collection

	int allEvents;
	int triggeredEvents;
	int eventsWithPrimaryVertex;
	int savedEvents;

	MyRootTree* userRootTree;

	TauResolutionAnalysis* tauResolutionAnalysis;
	TauMETTriggerAnalysis* tauMETTriggerAnalysis;
        TrackEcalHitPoint trackEcalHitPoint;

	bool printTrigger;
};
#endif
