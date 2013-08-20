#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include<memory>
#include<vector>

class HPlusPATJetViewBetaEmbedder: public edm::EDProducer {
public:
  explicit HPlusPATJetViewBetaEmbedder(const edm::ParameterSet& iConfig):
    fJetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
    fGeneralTracksSrc(iConfig.getParameter<edm::InputTag>("generalTracksSrc")),
    fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc"))
  {
    std::string embedPrefix = iConfig.getParameter<std::string>("embedPrefix");

    fBetaName = embedPrefix+"Beta";
    fBetaMaxName = embedPrefix+"BetaMax";
    fBetaStarName = embedPrefix+"BetaStar";
    fBetaUnassociatedName = embedPrefix+"BetaUnassociated";
    fVertexIdByBetaMaxName = embedPrefix+"VertexIndexByBetaMax";
    fLdgTrackBelongsToSelectedPVName = embedPrefix+"LdgTrackBelongsToSelectedPV";
    fDRMeanName = embedPrefix+"DRMean";
    fSumPtAllName = embedPrefix+"ChSumPtAll";
    fSumPtPvName = embedPrefix+"ChSumPtFromPV";
    fSumPtNovName = embedPrefix+"ChSumPtFromNoVertex";
    produces<std::vector<pat::Jet> >();
  }

  HPlusPATJetViewBetaEmbedder() {}

  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fJetSrc, hjets);
    edm::Handle<edm::View<reco::Vertex> > hvertices;
    iEvent.getByLabel(fVertexSrc, hvertices);
    edm::Handle<reco::TrackCollection> trackCollection;
    iEvent.getByLabel(fGeneralTracksSrc, trackCollection);
    if(hvertices->empty())
      throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty" << std::endl;
    edm::PtrVector<reco::Vertex> vertices = hvertices->ptrVector();

    std::vector<double> myTrackPtInVertex;
    for (size_t i = 0; i < hvertices->size(); ++i) {
      myTrackPtInVertex.push_back(0.0);
    }

    std::auto_ptr<std::vector<pat::Jet> > prod(new std::vector<pat::Jet>());
    prod->reserve(hjets->size());
    for(size_t iJet=0; iJet<hjets->size(); ++iJet) {
      for (size_t iVtx = 0; iVtx < hvertices->size(); ++iVtx) {
        myTrackPtInVertex.at(iVtx) = 0.0;
      }
      double beta = -1.0;
      double betaStar = -1.0;
      double betaMax = -1.0;
      double betaUnassociated = -1.0;
      int vertexIdByBetaMax = 999;
      int ldgTrkBelongsToSelectedVertex = 0;

      // This one has to be a copy, see the note below
      pat::Jet jet = (*hjets)[iJet];
      double sumpt_all = 0.0; // sumpt of all pfcands
      double sumpt_PU = 0.0; // sumpt of tracks assigned to PU vertex
      double sumpt_not_selected_PV = 0.0; // sumpt of pfcands not assigned to chosen vertex
      double sumpt_nov = 0.0; // sumpt of pfcands not associated to a vertex
      double myDRmean = 0.0; // sum of ptcand/ptjet*DR(cand,jet)
      // Loop over PF candidates
      const std::vector<reco::PFCandidatePtr>& pfcands = jet.getPFConstituents();

      // Find leading track index
      size_t myLdgCandIndex = 9999;
      double myMax = -1.0;
      for(size_t iCand=0; iCand<pfcands.size(); ++iCand) {
        const reco::PFCandidate pfcand = *(pfcands[iCand]);
        if (pfcand.pt() > myMax) {
          myMax = pfcand.pt();
          myLdgCandIndex = iCand;
        }
      }
      for(size_t iCand=0; iCand<pfcands.size(); ++iCand) {
        const reco::PFCandidate pfcand = *(pfcands[iCand]);
        // Require that the PF candidate has a track (i.e. it is a charged hadron or a muon or an electron)
        if (pfcand.trackRef().isNull()) continue;
        sumpt_all += pfcand.pt();
        // Update DeltaR mean
        if (jet.pt() > 0.0) {
          myDRmean += pfcand.pt() / jet.pt() * reco::deltaR(pfcand, jet);
        }
        // Loop over vertices and tracks associated to them to see if the track was assigned to a vertex
        bool myTrackBelongsToAnyVertex = false;
        bool myTrackBelongsToSelectedVertex = false;
        for (size_t iVtx = 0; iVtx < hvertices->size(); ++iVtx) {
          // Loop over tracks in vertex
          for (std::vector<reco::TrackBaseRef>::const_iterator iVtxTrk = hvertices->at(iVtx).tracks_begin(); iVtxTrk != hvertices->at(iVtx).tracks_end(); ++iVtxTrk) {
            if (*iVtxTrk == reco::TrackBaseRef(pfcand.trackRef())) {
              //std::cout << "trkref matched" << std::endl;
              myTrackPtInVertex.at(iVtx) += pfcand.pt();
              myTrackBelongsToAnyVertex = true;
            }
          }
          if (iVtx == 0 && myTrackBelongsToAnyVertex) {
            myTrackBelongsToSelectedVertex = true;
          }
          //float myTrackWeight = vertices->at(iVtx)->trackWeight(pfcand.trackRef());
          //if (myTrackWeight > 0.5) {
          //}
        }
        if (myTrackBelongsToAnyVertex && !myTrackBelongsToSelectedVertex) {
          sumpt_PU += pfcand.pt();
        }
        if (!myTrackBelongsToAnyVertex) {
          // This track does not belong to any vertex, check if it is within 2 mm of the vertex z
          for (size_t iVtx = 0; iVtx < hvertices->size(); ++iVtx) {
            double myValue = fabs(hvertices->at(iVtx).z() - pfcand.trackRef()->vz());
            if (myValue < 0.2) { // 2 mm
              myTrackBelongsToAnyVertex = true;
              myTrackPtInVertex.at(iVtx) += pfcand.pt();
            }
            if (iVtx == 0 && myTrackBelongsToAnyVertex) {
              myTrackBelongsToSelectedVertex = true;
            }
          }
          // Check if track z is further than 2 mm of the chosen PV
          if (fabs(hvertices->at(0).z() - pfcand.trackRef()->vz()) > 0.2) {
            sumpt_not_selected_PV += pfcand.pt();
          }
          if (myTrackBelongsToAnyVertex && !myTrackBelongsToSelectedVertex) {
            sumpt_PU += pfcand.pt();
          }
        }
        if (iCand == myLdgCandIndex) {
          if (myTrackBelongsToSelectedVertex) {
            ldgTrkBelongsToSelectedVertex = 1;
          }
        }
        if (!myTrackBelongsToAnyVertex) {
          sumpt_nov += pfcand.pt();
        }
      } // end of pfcand loop
      // Calculate beta
      if (sumpt_all > 0.0) {
        beta = myTrackPtInVertex.at(0) / sumpt_all;
        for (size_t iVtx = 0; iVtx < hvertices->size(); ++iVtx) {
          double myValue = myTrackPtInVertex.at(iVtx) / sumpt_all;
          if (myValue > betaMax) {
            betaMax = myValue;
            vertexIdByBetaMax = iVtx;
          }
        }
        betaStar = sumpt_PU / sumpt_all;
        betaUnassociated = sumpt_nov / sumpt_all;
      }
      //std::cout << "Jet " << iJet << " sumpt_all " << sumpt_all << " sumpt_pv " << myTrackPtInVertex[0] << " sumpt_nov " << sumpt_nov << std::endl;
      //std::cout << "  beta " << beta << " betaMax " << betaMax << " betaStar " << betaStar << " vtxIdByBetaMax " << vertexIdByBetaMax << " ldgTrkBelongsToSelectedVertex " << ldgTrkBelongsToSelectedVertex << " DRmean " << myDRmean << std::endl;
      // Make a copy from the original, because otherwise we'll have
      // the pat::Jet::pfCandidatesTemp_ serialized (maybe it should
      // be a transient member in the first place?)
      pat::Jet copy = (*hjets)[iJet];
      copy.addUserFloat(fBetaName, beta);
      copy.addUserFloat(fBetaMaxName, betaMax);
      copy.addUserFloat(fBetaStarName, betaStar);
      copy.addUserFloat(fBetaUnassociatedName, betaUnassociated);
      copy.addUserInt(fVertexIdByBetaMaxName, vertexIdByBetaMax);
      copy.addUserInt(fLdgTrackBelongsToSelectedPVName, ldgTrkBelongsToSelectedVertex);
      copy.addUserFloat(fDRMeanName, myDRmean);
      prod->push_back(copy);
    }
    iEvent.put(prod);
  }

  // Taken from CommonTools/ParticleFlow/plugins/PFPileUp.cc
  /*edm::Ptr<reco::Vertex> findVertex(const edm::PtrVector<reco::Vertex>& vertices, const reco::PFCandidate& pfcand) {
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
  }*/


private:
  edm::InputTag fJetSrc;
  edm::InputTag fGeneralTracksSrc;
  edm::InputTag fVertexSrc;
  std::string fBetaName;
  std::string fBetaMaxName;
  std::string fBetaUnassociatedName;
  std::string fBetaStarName;
  std::string fVertexIdByBetaMaxName;
  std::string fLdgTrackBelongsToSelectedPVName;
  std::string fDRMeanName;
  std::string fSumPtAllName;
  std::string fSumPtPvName;
  std::string fSumPtNovName;
};

DEFINE_FWK_MODULE( HPlusPATJetViewBetaEmbedder );
