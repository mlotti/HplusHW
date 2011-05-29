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
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"
#include "RecoTauTag/RecoTau/src/RecoTauVertexAssociator.cc"

#include "DataFormats/PatCandidates/interface/Tau.h"


namespace HPlus {
  template <typename ValueType>
  class TauLikeIsolationEmbedderTraits {
  public:
    typedef edm::Ptr<reco::Vertex> VertexPtr;

    explicit TauLikeIsolationEmbedderTraits(const edm::ParameterSet& iConfig):
      fPfCandSrc(iConfig.getParameter<edm::InputTag>("pfCandSrc")),
      fVertexSrc(iConfig.getParameter<edm::InputTag>("primaryVertexSrc")),
      fSignalCone(iConfig.getParameter<double>("signalCone")),
      fIsolationCone(iConfig.getParameter<double>("isolationCone")),
      fThrow(iConfig.getUntrackedParameter<bool>("throw", true))
    {}
    ~TauLikeIsolationEmbedderTraits() {}

    void beginEvent(const edm::Event& iEvent) {
      iEvent.getByLabel(fPfCandSrc, thePFCands);
      iEvent.getByLabel(fVertexSrc, theVertices);
    }
    
    VertexPtr getVertex(const ValueType& iCand) const {
      if(theVertices->empty()) {
        if(fThrow)
          throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty!" << std::endl;
        return VertexPtr();
      }
      return theVertices->ptrAt(0);
    }

    reco::PFCandidateRefVector isolationCands(const ValueType& iCand) const {
      reco::PFCandidateRefVector pfcands(thePFCands.id());
      for(size_t i=0; i<thePFCands->size(); ++i) {
        double dr = reco::deltaR(thePFCands->at(i), iCand);
        if(fSignalCone < dr && dr < fIsolationCone) {
          pfcands.push_back(reco::PFCandidateRef(thePFCands, i));
        }
      }
      return pfcands;
    }

    void endEvent() {
      thePFCands = edm::Handle<std::vector<reco::PFCandidate> >();
    }

  private:
    edm::InputTag fPfCandSrc;
    edm::InputTag fVertexSrc;

    double fSignalCone;
    double fIsolationCone;

    edm::Handle<std::vector<reco::PFCandidate> > thePFCands;
    edm::Handle<edm::View<reco::Vertex> > theVertices;

    bool fThrow;
  };


  template <>
  class TauLikeIsolationEmbedderTraits<pat::Tau> {
  public:
    typedef reco::VertexRef VertexPtr;

    explicit TauLikeIsolationEmbedderTraits(const edm::ParameterSet& iConfig):
      fVertexAssociator(iConfig.getParameter<edm::ParameterSet>("qualityCuts")),
      fThrow(iConfig.getUntrackedParameter<bool>("throw", true))
    {}

    ~TauLikeIsolationEmbedderTraits() {}
    void beginEvent(const edm::Event& iEvent) {}
    void endEvent() {}

    reco::VertexRef getVertex(const pat::Tau& iCand) const {
      reco::VertexRef pv = fVertexAssociator.associatedVertex(*iCand.pfJetRef());
      if(pv.isNull() && fThrow) {
        throw cms::Exception("LogicError") << "Null vertex ref" << std::endl;
      }
      return pv;
    }

    reco::PFCandidateRefVector isolationCands(const pat::Tau& iCand) const {
      return iCand.isolationPFCands();
    }

  private:
    reco::tau::RecoTauVertexAssociator fVertexAssociator;
    bool fThrow;
  };

  // Applying the Curiously Recurring Template Pattern
  template <typename InputCollection,
            typename ValueType>
  class TauLikeIsolationEmbedder: public edm::EDProducer {
    typedef std::vector<ValueType> OutputCollection;
    typedef typename TauLikeIsolationEmbedderTraits<ValueType>::VertexPtr VertexPtr;

  public:
    explicit TauLikeIsolationEmbedder(const edm::ParameterSet& iConfig):
      fTraits(iConfig),
      fCandSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
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
    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      edm::Handle<InputCollection> hcand;
      iEvent.getByLabel(fCandSrc, hcand);

      std::auto_ptr<OutputCollection> output(new OutputCollection());
      output->reserve(hcand->size());

      fTraits.beginEvent(iEvent);

      for(size_t iCand=0; iCand<hcand->size(); ++iCand) {
        VertexPtr thePV = fTraits.getVertex(hcand->at(iCand));

        size_t occupancy = 0;
        double sumPt = 0;
        double maxPt = 0;
        if(thePV.isNonnull()) {
          reco::PFCandidateRefVector pfcands = fTraits.isolationCands(hcand->at(iCand));

          reco::PFCandidateRefVector chargedCands = TauTagTools::filteredPFChargedHadrCands(pfcands,
                                                                                            this->fMinTrackPt,
                                                                                            this->fMinTrackPixelHits,
                                                                                            this->fMinTrackHits,
                                                                                            this->fMaxTransverseImpactParameter,
                                                                                            this->fMaxTrackChi2,
                                                                                            this->fMaxDeltaZ,
                                                                                            *thePV,
                                                                                            thePV->position().z());
          reco::PFCandidateRefVector gammaCands = TauTagTools::filteredPFGammaCands(pfcands, this->fMinGammaEt);


          occupancy = chargedCands.size() + gammaCands.size();
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
        }

        ValueType copy = hcand->at(iCand);
        copy.addUserInt(this->fOccupancyName, occupancy);
        copy.addUserFloat(this->fMaxPtName, maxPt);
        copy.addUserFloat(this->fSumPtName, sumPt);
        output->push_back(copy);

        /*
        if(copy.pt() > 30)
          std::cout << "Cand pt " << copy.pt() << " occupancy " << occupancy << " sumPt " << sumPt << " maxPt " << maxPt << std::endl;
        */
      }

      fTraits.endEvent();
      
      iEvent.put(output);
    }



  protected:
    TauLikeIsolationEmbedderTraits<ValueType> fTraits;

    edm::InputTag fCandSrc;
    
    std::string fOccupancyName;
    std::string fSumPtName;
    std::string fMaxPtName;

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
