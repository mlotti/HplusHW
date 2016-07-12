// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GenEmbedder_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GenEmbedder_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaR.h"

namespace HPlus {
  template <typename InputCollection,
            typename ValueType>
  class GenEmbedder: public edm::EDProducer {

    typedef std::vector<ValueType> OutputCollection;

  public:
    explicit GenEmbedder(const edm::ParameterSet& iConfig):
      fCandSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
      fGenSrc(iConfig.getParameter<edm::InputTag>("genParticleSrc")),
      fMaxDR(iConfig.getParameter<double>("maxDR")),
      fPdgId(iConfig.getParameter<uint32_t>("pdgId"))
    {
      std::string embedPrefix = iConfig.getParameter<std::string>("embedPrefix");
      fMotherName = embedPrefix+"MotherPdgId";
      fGrandMotherName = embedPrefix+"GrandMotherPdgId";

      produces<OutputCollection>();
    }

    ~GenEmbedder() {}

  private:
    virtual void beginJob() {}

    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      edm::Handle<InputCollection> hcand;
      iEvent.getByLabel(fCandSrc, hcand);

      edm::Handle<edm::View<reco::GenParticle> > hgen;
      iEvent.getByLabel(fGenSrc, hgen);

      std::auto_ptr<OutputCollection> output(new OutputCollection());
      output->reserve(hcand->size());

      for(size_t iCand=0; iCand<hcand->size(); ++iCand) {
        ValueType copy = hcand->at(iCand);

        if(!iEvent.isRealData()) {
          const reco::GenParticle *particle = findGenParticle(copy, hgen->begin(), hgen->end());
          if(particle) {
            const reco::GenParticle *mother = findGenParent(particle);
            if(mother) {
              copy.addUserInt(fMotherName, mother->pdgId());
              const reco::GenParticle *grandMother = findGenParent(mother);
              if(grandMother) {
                copy.addUserInt(fGrandMotherName, grandMother->pdgId());
              }
            }
          }
        }

        output->push_back(copy);
      }

      iEvent.put(output);
    }

    virtual void endJob() {}

    template <typename I>
    const reco::GenParticle *findGenParticle(const ValueType& cand, I begin, I end) const {
      const reco::GenParticle *ret = 0; 

      double maxDR = 9999;
      for(I iGen = begin; iGen != end; ++iGen) {
        uint32_t pdgId = std::abs(iGen->pdgId());
        if(pdgId == fPdgId) {
          double deltaR = reco::deltaR(cand, *iGen);
          if(deltaR < maxDR) {
            ret = &(*iGen);
            maxDR = deltaR;
          }
        }
      }

      return ret;
    }

    const reco::GenParticle *findGenParent(const reco::GenParticle *particle) const {
      int pdgId = particle->pdgId();
      const reco::GenParticle *mother = particle;
      while(mother && mother->pdgId() ==  pdgId)
        mother = dynamic_cast<const reco::GenParticle *>(mother->mother());
      return mother;
    }

    edm::InputTag fCandSrc;
    edm::InputTag fGenSrc;
    double fMaxDR;
    uint32_t fPdgId;
    std::string fMotherName;
    std::string fGrandMotherName;
  };
}

#endif
