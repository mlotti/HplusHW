// -*- c++ -*-
// Class to convert edm::Event to MyEvent
// 26.10.2007/S.Lehti

#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MyEventConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MyEventConverter_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackEcalHitPoint.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METConverterAll.h"

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

        void		        getTrajectories(const edm::Event&);
	void			getCaloMETs(const edm::Event&,std::map<std::string, MyMET>&);
	void			getPFMETs(const edm::Event&,std::map<std::string, MyMET>&);
	void		 	getMETs(const edm::Event&,std::map<std::string, MyMET>&);
	MyMET 			getMetFromCaloTowers(const edm::Event&);



// datafields

//        std::vector<edm::InputTag> HLTSelection;
        reco::Vertex primaryVertex;
        edm::InputTag vertexLabel;
        edm::InputTag trackCollectionSelection;

        std::vector<edm::InputTag> gsfElectronLabels;
        std::vector<edm::InputTag> patElectronLabels;
        //std::vector<edm::InputTag> photonLabels;
        std::vector<edm::InputTag> muonLabels;
        std::vector<edm::InputTag> patMuonLabels;
        std::vector<edm::InputTag> caloTauLabels;
        std::vector<edm::InputTag> pfTauLabels;
        std::vector<edm::InputTag> patTauLabels;
        std::vector<edm::InputTag> caloJetLabels;
        std::vector<edm::InputTag> patJetLabels;

        edm::InputTag muonReplacementMuonLabel;

        edm::InputTag genParticleLabel;
        edm::InputTag muonReplacementGenLabel;
        edm::InputTag genJetLabel;
        edm::InputTag simHitLabel;

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
        METConverterAll metConverter;

	bool printTrigger;
};
#endif
