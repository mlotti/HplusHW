// -*- c++ -*-
// Class to convert edm::Event to MyEvent
// 26.10.2007/S.Lehti

#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MyEventConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MyEventConverter_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackEcalHitPoint.h"

#include<vector>
#include<string>
#include<map>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}
class TransientTrackBuilder;
class TauJetCorrector;
class JetCorrector;
class Trajectory;

class MyRootTree;
class TauResolutionAnalysis;
class TauMETTriggerAnalysis;


class MyEventConverter {
  public:
	MyEventConverter(const edm::ParameterSet&);
	~MyEventConverter();

	void convert(const edm::Event&,const edm::EventSetup&);

  private:

// functions

	bool triggerDecision(const edm::Event&);
	bool primaryVertexFound(const edm::Event&);

	void                    getTriggerResults(const edm::Event&, const edm::InputTag&, std::map<std::string, bool>&);
	std::vector<MyJet>	getHLTObjects(const edm::Event&);
        void		        getTrajectories(const edm::Event&);
	void getMET(const edm::Event&, std::map<std::string, MyMET>&);
        void  getCaloMETs(const edm::Event&, std::map<std::string, MyMET>&);
	MyMET 			getMetFromCaloTowers(const edm::Event&);



// datafields

        std::vector<edm::InputTag> HLTSelection;
        reco::Vertex primaryVertex;
	bool PVFound;
        edm::InputTag trackCollectionSelection;

////        CutBasedElectronID* electronIdAlgo;
//	edm::InputTag barrelClusterShapeAssocProducer;
//	edm::InputTag endcapClusterShapeAssocProducer;
	edm::InputTag reducedBarrelRecHitCollection;
	edm::InputTag reducedEndcapRecHitCollection;
        const TransientTrackBuilder* transientTrackBuilder;
//	const TransientTrackingRecHitBuilder* TTRHBuilder;
        std::vector<const JetCorrector*> jetEnergyCorrections;
	const TauJetCorrector* tauJetCorrection;
        std::vector<std::string> jetEnergyCorrectionTypes;
        std::vector<std::string> btaggingAlgos;
	std::vector<edm::InputTag> metCollections;
        std::vector<edm::InputTag> electronIdLabels;
  //TrackCollection tracks;

	// ECAL clusters
	edm::InputTag barrelBasicClustersInput;
	edm::InputTag endcapBasicClustersInput;
	
	edm::Handle<std::vector<Trajectory> > myTrajectoryCollectionHandle;
 	edm::InputTag trajectoryInput; // Input for trajectory collection

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
