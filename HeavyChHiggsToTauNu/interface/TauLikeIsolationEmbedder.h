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

#include "DataFormats/PatCandidates/interface/Tau.h"


namespace HPlus {
  template <typename ValueType>
  class TauLikeIsolationEmbedderTraits {
  public:
    explicit TauLikeIsolationEmbedderTraits(const edm::ParameterSet& iConfig):
      fPfCandSrc(iConfig.getParameter<edm::InputTag>("pfCandSrc")),
      fSignalCone(iConfig.getParameter<double>("signalCone")),
      fIsolationCone(iConfig.getParameter<double>("isolationCone"))
    {}
    ~TauLikeIsolationEmbedderTraits() {}

    void beginEvent(const edm::Event& iEvent) {
      iEvent.getByLabel(fPfCandSrc, thePFCands);
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

    double fSignalCone;
    double fIsolationCone;

    edm::Handle<std::vector<reco::PFCandidate> > thePFCands;
  };


  template <>
  class TauLikeIsolationEmbedderTraits<pat::Tau> {
  public:
    explicit TauLikeIsolationEmbedderTraits(const edm::ParameterSet& iConfig) {}
    ~TauLikeIsolationEmbedderTraits() {}
    void beginEvent(const edm::Event& iEvent) {}
    void endEvent() {}

    reco::PFCandidateRefVector isolationCands(const pat::Tau& iCand) const {
      return iCand.isolationPFCands();
    }
  };

  // Applying the Curiously Recurring Template Pattern
  template <typename InputCollection,
            typename ValueType>
  class TauLikeIsolationEmbedder: public edm::EDProducer {
  protected:
    typedef std::vector<ValueType> OutputCollection;

  public:
    explicit TauLikeIsolationEmbedder(const edm::ParameterSet& iConfig):
      fTraits(iConfig),
      fCandSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
      fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
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

      edm::Handle<edm::View<reco::Vertex> > hvertex;
      iEvent.getByLabel(fVertexSrc, hvertex);
      thePV = hvertex->ptrAt(0);

      fTraits.beginEvent(iEvent);


      std::auto_ptr<OutputCollection> output(new OutputCollection());
      output->reserve(hcand->size());

      for(size_t iCand=0; iCand<hcand->size(); ++iCand) {
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
    edm::InputTag fVertexSrc;
    
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

    edm::Ptr<reco::Vertex> thePV;
  };
}


#endif
