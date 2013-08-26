// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauLikeIsolationEmbedder_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauLikeIsolationEmbedder_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"
#include "RecoTauTag/RecoTau/interface/RecoTauVertexAssociator.h"
#include "RecoTauTag/RecoTau/interface/RecoTauQualityCuts.h"

#include "DataFormats/PatCandidates/interface/Tau.h"


namespace HPlus {
  template <typename ValueType>
  class TauLikeIsolationEmbedderTraits {
  public:
    explicit TauLikeIsolationEmbedderTraits(const edm::ParameterSet& iConfig):
      fPfCandSrc(iConfig.getParameter<edm::InputTag>("pfCandSrc")),
      fVertexSrc(iConfig.getParameter<edm::ParameterSet>("qualityCuts").getParameter<edm::InputTag>("primaryVertexSrc")),
      fSignalCone(iConfig.getParameter<double>("signalCone")),
      fIsolationCone(iConfig.getParameter<double>("isolationCone")),
      fThrow(iConfig.getUntrackedParameter<bool>("throw", true))
    {}
    ~TauLikeIsolationEmbedderTraits() {}

    void beginEvent(const edm::Event& iEvent) {
      iEvent.getByLabel(fPfCandSrc, thePFCands);
      iEvent.getByLabel(fVertexSrc, theVertices);
    }
    
    reco::VertexRef getVertex(const ValueType& iCand) const {
      if(theVertices->empty()) {
        if(fThrow)
          throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty!" << std::endl;
        return reco::VertexRef();
      }
      reco::VertexRef vertex(theVertices, 0);
      double maxDz = std::abs(iCand.vertex().z() - vertex->z());

      for(size_t iVertex=1; iVertex < theVertices->size(); ++iVertex) {
        double dz = std::abs(iCand.vertex().z() - theVertices->at(iVertex).z());
        if(dz < maxDz) {
          dz = maxDz;
          vertex = reco::VertexRef(theVertices, iVertex);
        }
      }

      return vertex;
    }

    reco::PFCandidateRefVector isolationChargedHadrCands(const ValueType& iCand) const {
      reco::PFCandidateRefVector pfcands(thePFCands.id());
      for(size_t i=0; i<thePFCands->size(); ++i) {
        double dr = reco::deltaR(thePFCands->at(i), iCand);
        if(thePFCands->at(i).particleId() == reco::PFCandidate::h && 
           fSignalCone < dr && dr < fIsolationCone) {
          pfcands.push_back(reco::PFCandidateRef(thePFCands, i));
        }
      }
      return pfcands;
    }

    reco::PFCandidateRefVector isolationGammaCands(const ValueType& iCand) const {
      reco::PFCandidateRefVector pfcands(thePFCands.id());
      for(size_t i=0; i<thePFCands->size(); ++i) {
        double dr = reco::deltaR(thePFCands->at(i), iCand);
        if(thePFCands->at(i).particleId() == reco::PFCandidate::gamma && 
           fSignalCone < dr && dr < fIsolationCone) {
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
    edm::Handle<std::vector<reco::Vertex> > theVertices;

    bool fThrow;
  };


  template <>
  class TauLikeIsolationEmbedderTraits<pat::Tau> {
  public:
    explicit TauLikeIsolationEmbedderTraits(const edm::ParameterSet& iConfig):
      fVertexAssociator(iConfig.getParameter<edm::ParameterSet>("qualityCuts")),
      fThrow(iConfig.getUntrackedParameter<bool>("throw", true))
    {}

    ~TauLikeIsolationEmbedderTraits() {}
    void beginEvent(const edm::Event& iEvent) {
      fVertexAssociator.setEvent(iEvent);
    }
    void endEvent() {}

    reco::VertexRef getVertex(const pat::Tau& iCand) const {
      reco::VertexRef pv = fVertexAssociator.associatedVertex(*iCand.pfJetRef());
      if(pv.isNull() && fThrow) {
        throw cms::Exception("LogicError") << "Null vertex ref" << std::endl;
      }
      return pv;
    }

    reco::PFCandidateRefVector isolationChargedHadrCands(const pat::Tau& iCand) const {
      return iCand.isolationPFChargedHadrCands();
    }
    reco::PFCandidateRefVector isolationGammaCands(const pat::Tau& iCand) const {
      return iCand.isolationPFGammaCands();
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

  public:
    explicit TauLikeIsolationEmbedder(const edm::ParameterSet& iConfig):
      fTraits(iConfig),
      fCandSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
      fQcuts(iConfig.getParameter<edm::ParameterSet>("qualityCuts").getParameter<edm::ParameterSet>("isolationQualityCuts"))
    {
      std::string embedPrefix = iConfig.getParameter<std::string>("embedPrefix");
      fChOccupancyName = embedPrefix+"ChargedOccupancy";
      fChSumPtName = embedPrefix+"ChargedSumPt";
      fChMaxPtName = embedPrefix+"ChargedMaxPt";

      fGamOccupancyName = embedPrefix+"GammaOccupancy";
      fGamSumPtName = embedPrefix+"GammaSumPt";
      fGamMaxPtName = embedPrefix+"GammaMaxPt";

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
        reco::VertexRef thePV = fTraits.getVertex(hcand->at(iCand));
        ValueType copy = hcand->at(iCand);
        if(thePV.isNonnull()) {
          fQcuts.setPV(thePV);

          reco::PFCandidateRefVector pfchcands = fTraits.isolationChargedHadrCands(hcand->at(iCand));
          reco::PFCandidateRefVector pfgammacands = fTraits.isolationGammaCands(hcand->at(iCand));

          reco::PFCandidateRefVector selectedChCands = fQcuts.filterRefs(pfchcands);
          reco::PFCandidateRefVector selectedGammaCands = fQcuts.filterRefs(pfgammacands);

          double sumPt = 0;
          double maxPt = 0;
          for(size_t i=0; i<selectedChCands.size(); ++i) {
            double pt = selectedChCands[i]->pt();
            sumPt += pt;
            maxPt = std::max(maxPt, pt);
          }
          copy.addUserInt(fChOccupancyName, selectedChCands.size());
          copy.addUserFloat(fChMaxPtName, maxPt);
          copy.addUserFloat(fChSumPtName, sumPt);
          maxPt = 0;
          sumPt = 0;

          for(size_t i=0; i<selectedGammaCands.size(); ++i) {
            double pt = selectedGammaCands[i]->pt();
            sumPt += pt;
            maxPt = std::max(maxPt, pt);
          }
          copy.addUserInt(fGamOccupancyName, selectedGammaCands.size());
          copy.addUserFloat(fGamMaxPtName, maxPt);
          copy.addUserFloat(fGamSumPtName, sumPt);
        }
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

    reco::tau::RecoTauQualityCuts fQcuts;
    
    std::string fChOccupancyName;
    std::string fChSumPtName;
    std::string fChMaxPtName;

    std::string fGamOccupancyName;
    std::string fGamSumPtName;
    std::string fGamMaxPtName;
  };
}


#endif
