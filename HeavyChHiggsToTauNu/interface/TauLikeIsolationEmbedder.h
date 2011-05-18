// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauLikeIsolationEmbedder_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauLikeIsolationEmbedder_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"

namespace HPlus {
  template <typename InputCollection,
            typename ValueType>
    class TauLikeIsolationEmbedder: public edm::EDProducer {

    typedef std::vector<ValueType> OutputCollection;

  public:
    explicit TauLikeIsolationEmbedder(const edm::ParameterSet& iConfig):
      fCandSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
      fPfCandSrc(iConfig.getParameter<edm::InputTag>("pfCandSrc")),
      fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
      fSignalCone(iConfig.getParameter<double>("signalCone")),
      fIsolationCone(iConfig.getParameter<double>("isolationCone")),
      fMinTrackHits(iConfig.getParameter<uint32_t>("minTrackHits")),
      fMinTrackPt(iConfig.getParameter<double>("minTrackPt")),
      fMaxTrackChi2(iConfig.getParameter<double>("maxTrackChi2")),
      fMinTrackPixelHits(iConfig.getParameter<uint32_t>("minTrackPixelHits")),
      fMinGammaEt(iConfig.getParameter<double>("minGammaEt")),
      fMaxDeltaZ(iConfig.getParameter<double>("maxDeltaZ")),
      fMaxTransverseImpactParameter(iConfig.getParameter<double>("maxTransverseImpactParameter"))
    {
      std::string embedPrefix = iConfig.getParameter<std::string>("embedPrefix");
      fOccupancyName = embedPrefix+"Occupancy";
      fSumPtName = embedPrefix+"SumPt";
      fMaxPtName = embedPrefix+"MaxPt";

      produces<OutputCollection>();
    }

    ~TauLikeIsolationEmbedder() {}

  private:
    virtual void beginJob() {}

    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      edm::Handle<InputCollection> hcand;
      iEvent.getByLabel(fCandSrc, hcand);

      edm::Handle<std::vector<reco::PFCandidate> > hpfcand;
      iEvent.getByLabel(fPfCandSrc, hpfcand);

      edm::Handle<edm::View<reco::Vertex> > hvertex;
      iEvent.getByLabel(fVertexSrc, hvertex);

      edm::Ptr<reco::Vertex> thePV = hvertex->ptrAt(0);

      std::auto_ptr<OutputCollection> output(new OutputCollection());
      output->reserve(hcand->size());

      for(size_t iCand=0; iCand<hcand->size(); ++iCand) {
        
        // Select the PF cands between signal and isolation cones
        reco::PFCandidateRefVector pfcands(hpfcand.id());
        for(size_t i=0; i<hpfcand->size(); ++i) {
          double dr = reco::deltaR(hpfcand->at(i), hcand->at(iCand));
          if(fSignalCone < dr && dr < fIsolationCone) {
            pfcands.push_back(reco::PFCandidateRef(hpfcand, i));
          }
        }

        reco::PFCandidateRefVector chargedCands = TauTagTools::filteredPFChargedHadrCands(pfcands,
                                                                                          fMinTrackPt,
                                                                                          fMinTrackPixelHits,
                                                                                          fMinTrackHits,
                                                                                          fMaxTransverseImpactParameter,
                                                                                          fMaxTrackChi2,
                                                                                          fMaxDeltaZ,
                                                                                          *thePV,
                                                                                          thePV->position().z());
        reco::PFCandidateRefVector gammaCands = TauTagTools::filteredPFGammaCands(pfcands, fMinGammaEt);
      

        size_t occupancy = chargedCands.size() + gammaCands.size();
        double sumPt = 0;
        double maxPt = 0;
        
        for(size_t i=0; i<chargedCands.size(); ++i) {
          double pt = chargedCands[i]->pt();
          sumPt += pt;
          maxPt = std::max(maxPt, pt);
        }

        for(size_t i=0; i<gammaCands.size(); ++i) {
          double pt = gammaCands[i]->pt();
          sumPt += pt;
          maxPt = std::max(maxPt, pt);
        }

        ValueType copy = hcand->at(iCand);
        copy.addUserInt(fOccupancyName, occupancy);
        copy.addUserFloat(fMaxPtName, maxPt);
        copy.addUserFloat(fSumPtName, sumPt);
        output->push_back(copy);

        /*
        if(copy.pt() > 30)
          std::cout << "Cand pt " << copy.pt() << " occupancy " << occupancy << " sumPt " << sumPt << " maxPt " << maxPt << std::endl;
        */
      }

      
      iEvent.put(output);
    }

    virtual void endJob() {}


    edm::InputTag fCandSrc;
    edm::InputTag fPfCandSrc;
    edm::InputTag fVertexSrc;
    
    std::string fOccupancyName;
    std::string fSumPtName;
    std::string fMaxPtName;

    double fSignalCone;
    double fIsolationCone;

    uint32_t fMinTrackHits;
    double fMinTrackPt;
    double fMaxTrackChi2;
    uint32_t fMinTrackPixelHits;
    double fMinGammaEt;
    double fMaxDeltaZ;
    double fMaxTransverseImpactParameter;
    };
}

#endif
