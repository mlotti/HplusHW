#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include<memory>
#include<vector>

// FIXME: Add here a user float that is used for identifying if the jet is from chosen (i.e. first) PV or a PU vertex
/*
for each jet :
   reco::TrackRefVector tracks = jet.getTrackRefs();
   for each itrack in tracks :
      for each vertex :
           for ( jtrack = vertex.tracks_begin(); jtrack !=
vertex.tracks_end(); ++jtrack ) {
               if ( *itrack == *jtrack ) { // found the vertex the
track belongs to
                     if ( vertex is first ) { leading++;}
                     else { subleading++;}
               }
           }
    if ( subleading == 0 ) { countAsPrimary(); }   /// case 1
    else if ( leading == 0 ) { countAsPiluep(); }   /// case 2
    else {
       ChristianHasToDecide() ;    /// you pick yourself what this
third category means.
    }
*/
// FIXME: Add cut of 2 mm to track-vertex association in DeltaZ
// FIXME: Add beta star


class HPlusPATJetViewBetaEmbedder: public edm::EDProducer {
public:
  explicit HPlusPATJetViewBetaEmbedder(const edm::ParameterSet& iConfig):
    fJetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
    fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc"))
  {
    std::string embedPrefix = iConfig.getParameter<std::string>("embedPrefix");
    fBetaName = embedPrefix+"Beta";
    fBetaIncorrectName = embedPrefix+"BetaPV";
    fSumPtAllName = embedPrefix+"ChSumPtAll";
    fSumPtPvName = embedPrefix+"ChSumPtFromPV";
    fSumPtNovName = embedPrefix+"ChSumPtFromNoVertex";

    produces<std::vector<pat::Jet> >();
  }

  ~HPlusPATJetViewBetaEmbedder() {}

  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fJetSrc, hjets);

    edm::Handle<edm::View<reco::Vertex> > hvertices;
    iEvent.getByLabel(fVertexSrc, hvertices);

    if(hvertices->empty())
      throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty" << std::endl;
    edm::PtrVector<reco::Vertex> vertices = hvertices->ptrVector();

    std::auto_ptr<std::vector<pat::Jet> > prod(new std::vector<pat::Jet>());
    prod->reserve(hjets->size());
    for(size_t iJet=0; iJet<hjets->size(); ++iJet) {
      // This one has to be a copy, see the note below
      pat::Jet jet = (*hjets)[iJet];

      double sumpt_all = 0; // sumpt of all pfcands
      double sumpt_pv = 0;  // sumpt of pfcands from primary vertex
      double sumpt_nov = 0; // sumpt of pfcands without vertex assignment
      const std::vector<reco::PFCandidatePtr>& pfcands = jet.getPFConstituents();
      for(size_t iCand=0; iCand<pfcands.size(); ++iCand) {
        const reco::PFCandidate pfcand = *(pfcands[iCand]);
        if(pfcand.particleId() != reco::PFCandidate::h)
          continue;

        sumpt_all += pfcand.pt();
        
        edm::Ptr<reco::Vertex> vertex = findVertex(vertices, pfcand);
        if(vertex.isNull())
          sumpt_nov += pfcand.pt();
        else if(vertex.key() == 0)
          sumpt_pv += pfcand.pt();
      }

      //std::cout << "Jet " << iJet << " sumpt_all " << sumpt_all << " sumpt_pv " << sumpt_pv << " sumpt_nov " << sumpt_nov << std::endl;
      double beta = -1.0;
      double betaIncorrect = -1.0;
      if (sumpt_all > 0.0) {
        beta = (sumpt_pv+sumpt_nov) / sumpt_all;
        betaIncorrect = sumpt_pv / sumpt_all;
      }
      //std::cout << "  beta " << beta << " betaIncorrect " << betaIncorrect << std::endl;
      
      // Make a copy from the original, because otherwise we'll have
      // the pat::Jet::pfCandidatesTemp_ serialized (maybe it should
      // be a transient member in the first place?)
      pat::Jet copy = (*hjets)[iJet];
      copy.addUserFloat(fBetaName, beta);
      copy.addUserFloat(fBetaIncorrectName, betaIncorrect); 
      prod->push_back(copy);
    }

    iEvent.put(prod);
  }


  // Taken from CommonTools/ParticleFlow/plugins/PFPileUp.cc
  edm::Ptr<reco::Vertex> findVertex(const edm::PtrVector<reco::Vertex>& vertices, const reco::PFCandidate& pfcand) {
    edm::Ptr<reco::Vertex> theVertex;
    reco::TrackBaseRef(pfcand.trackRef());

    float wmax = 0;
    for(edm::PtrVector<reco::Vertex>::const_iterator iVertex=vertices.begin(); iVertex!=vertices.end(); ++iVertex) {
      float w = (*iVertex)->trackWeight(pfcand.trackRef());
      if(w > wmax) {
        wmax = w;
        theVertex = *iVertex;
      }
    }
    return theVertex;
  }


private:
  edm::InputTag fJetSrc;
  edm::InputTag fVertexSrc;
  std::string fBetaName;
  std::string fBetaIncorrectName;
  std::string fSumPtAllName;
  std::string fSumPtPvName;
  std::string fSumPtNovName;
};

DEFINE_FWK_MODULE( HPlusPATJetViewBetaEmbedder );
