// Disclaimer: this is very experimental code, do NOT use for physics results :)

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include <DataFormats/TrackReco/interface/Track.h>
#include <DataFormats/TrackReco/interface/TrackFwd.h>

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include <DataFormats/PatCandidates/interface/Jet.h>

#include "Math/GenVector/VectorUtil.h"
#include "DataFormats/Math/interface/Vector.h"

#include <vector>
#include <string>
#include <sstream>

class HPlusPileupFilter: public edm::EDProducer {
 public:
  enum CollectionType {
    kPatTaus,
    kPatJets
  };
  explicit HPlusPileupFilter(const edm::ParameterSet&);
  ~HPlusPileupFilter();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  bool makeDecision(const reco::Vertex& vertex, const reco::TrackRefVector &tracks);
  virtual void endJob();

  edm::InputTag vertexCollectionSrc;
  edm::InputTag patCollectionSrc;
  CollectionType fCollectionType;
};

HPlusPileupFilter::HPlusPileupFilter(const edm::ParameterSet& iConfig):
  vertexCollectionSrc(iConfig.getParameter<edm::InputTag>("vertexCollectionSrc")),
  patCollectionSrc(iConfig.getParameter<edm::InputTag>("patCollectionSrc"))
{
  std::string myCollectionString = iConfig.getParameter<std::string>("patCollectionType");
  if (myCollectionString == "patTau")
    fCollectionType = kPatTaus;
  else if (myCollectionString == "patJet")
    fCollectionType = kPatJets;
  else throw cms::Exception("Configuration") << "HPlusPileupFilter: no or unknown input collection type! Options are: 'patTau', 'patJet' (you chose '" << myCollectionString << "')" << std::endl;
  
  // Produces the following items
  std::stringstream myCollectionName;
  myCollectionName << "PileupFiltered" << patCollectionSrc.instance();
  /*if (fCollectionType == kPatTaus) {
    produces<pat::TauCollection>(myCollectionName.str());
  } else if (fCollectionType == kPatJets) {
    produces<pat::JetCollection>(myCollectionName.str());
  }*/
}

HPlusPileupFilter::~HPlusPileupFilter() {}

void HPlusPileupFilter::beginJob() {}

void HPlusPileupFilter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // Obtain primary vertex with highest sum(track pT)
  edm::Handle<edm::View<reco::Vertex> > hvertex;
  iEvent.getByLabel(vertexCollectionSrc, hvertex);
  //std::auto_ptr<reco::VertexCollection> prod(new reco::VertexCollection());
  //prod->push_back((*hvertex)[0]);
  std::cout << "event: " << iEvent.id().event() << " vertices: " << hvertex->ptrVector().size() << std::endl; 
  
  double myFirstVertexPt = 0;
  double myAllVertexPtSum = 0;
  int myVertexIndex = 0;
  for (edm::PtrVector<reco::Vertex>::const_iterator iVertex = hvertex->ptrVector().begin(); 
       iVertex != hvertex->ptrVector().end(); ++iVertex) {
    // Loop over tracks assigned to vertex
    for (std::vector<reco::TrackBaseRef>::const_iterator iVertexTrack = (*iVertex)->tracks_begin(); 
       iVertexTrack != (*iVertex)->tracks_end(); ++iVertexTrack) {
      // Calculate sum p_T^2 of tracks assigned to vertex
      if ((*iVertex)->trackWeight(*iVertexTrack) > 0.01) {
        if (myVertexIndex == 0) {
          myFirstVertexPt += (*iVertexTrack)->momentum().Perp2();
        }
        myAllVertexPtSum += (*iVertexTrack)->momentum().Perp2();
      }
      //std::cout << "    track pt=" << std::sqrt((**iVertexTrack).momentum().Perp2()) << std::endl;
    }
    ++myVertexIndex;
  }
  std::cout << "PV pt: " << (*hvertex)[0].p4().pt() 
            << " calc pt:" << std::sqrt(myFirstVertexPt) 
            << " ratio: " << (myFirstVertexPt / myAllVertexPtSum) << std::endl;  
    
  // Match taus or jets to primary vertex
  if (fCollectionType == kPatTaus) {
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(patCollectionSrc, htaus);
    int myTauIndex = 0;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = htaus->ptrVector().begin();
      iter != htaus->ptrVector().end(); ++iter) {
      double myPtSum = 0;
      int myTrackCount = 0;
      for (reco::TrackRefVector::const_iterator iTrack = (*iter)->signalTracks().begin();
         iTrack != (*iter)->signalTracks().end(); ++iTrack) {
        if ((*hvertex)[0].trackWeight(*iTrack) > 0.5) {
          myPtSum += (*iTrack)->momentum().Perp2();
          ++myTrackCount;
        }
      }
      ++myTauIndex;
      if (std::abs((*iter)->eta())<2.5 && (*iter)->pt()>10) {
        std::cout << "  Tau " << myTauIndex << " pt=" << (*iter)->pt()
          << " eta=" << (*iter)->eta() << " phi=" << (*iter)->phi() << ": belonging to vertex: " 
          << myTrackCount << "/" << (*iter)->signalTracks().size()
          << ", " << " of pt: " << std::sqrt(myPtSum) / (*iter)->pt() << std::endl;
      }
    }
  } else if (fCollectionType == kPatJets) {
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(patCollectionSrc, hjets);
    int myTauIndex = 0;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = hjets->ptrVector().begin();
      iter != hjets->ptrVector().end(); ++iter) {
      double myPt2Sum = 0;
      math::XYZVector myPSum(0,0,0);
      int myTrackCount = 0;
      for (reco::TrackRefVector::const_iterator iTrack = (*iter)->associatedTracks().begin();
         iTrack != (*iter)->associatedTracks().end(); ++iTrack) {
        if ((*hvertex)[0].trackWeight(*iTrack) > 0.01) {
          myPt2Sum += (*iTrack)->momentum().Perp2();
          myPSum += (*iTrack)->momentum();
          ++myTrackCount;
        }
      }
      ++myTauIndex;
      if (std::abs((*iter)->eta())<2.5 && (*iter)->pt()>10) {
        std::cout << "  Jet " << myTauIndex << " pt=" << (*iter)->pt()
          << " eta=" << (*iter)->eta() << " phi=" << (*iter)->phi() << ": belonging to vertex: " 
          << myTrackCount << "/" << (*iter)->chargedMultiplicity() << "/" << (*iter)->associatedTracks().size()
          << ", " << " of pt2: " << std::sqrt(myPSum.Perp2()) / (*iter)->chargedHadronEnergy() << " or " << std::sqrt(myPSum.Perp2()) / (*iter)->pt() << std::endl;
      }
    }
  
  }
  /*
  // Loop over collection
  if (fCollectionType == kPatTaus) {
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(patCollectionSrc, htaus);
    for(edm::PtrVector<pat::Tau>::const_iterator iter = htaus->ptrVector().begin();
      iter != htaus->ptrVector().end(); ++iter) {
      makeDecision((*hvertex)[0], (*iter)->signalTracks());
    }
  } else if (fCollectionType == kPatJets) {
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(patCollectionSrc, hjets);
    for(edm::PtrVector<pat::Jet>::const_iterator iter = hjets->ptrVector().begin();
        iter != hjets->ptrVector().end(); ++iter) {
      makeDecision((*hvertex)[0], (*iter)->associatedTracks());
    }
  }
  */

  //  iEvent.put(prod);
}

bool HPlusPileupFilter::makeDecision(const reco::Vertex& vertex, const reco::TrackRefVector &tracks) {
  /*std::cout << "vertex ptsum=" << vertex.p4().pt() << std::endl;
  for (std::vector<reco::TrackBaseRef>::const_iterator iVertexTrack = vertex.tracks_begin(); 
       iVertexTrack != vertex.tracks_end(); ++iVertexTrack) {
    //if (vertex.trackWeight(
    for (reco::TrackRefVector::const_iterator iTrack = tracks.begin();
         iTrack != tracks.end(); ++iTrack) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR((**iVertexTrack).momentum(), (**iTrack).momentum());
      if (myDeltaR < 0.01) {
        std::cout << "found match" << std::endl;
      }
    }
  }*/
  return true;
}

void HPlusPileupFilter::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusPileupFilter);
