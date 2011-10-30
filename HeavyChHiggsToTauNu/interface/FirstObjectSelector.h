// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FirstObjectSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FirstObjectSelector_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/PtrVector.h"

#include<vector>

namespace HPlus {
  namespace fos {
    template <typename T, typename C>
    void append(std::vector<T>& output, edm::Handle<C>& handle, size_t index) {
      output.push_back((*handle)[index]);
    }

    template <typename T>
    void append(edm::PtrVector<T>& output, edm::Handle<edm::View<T> >& handle, size_t index) {
      output.push_back(handle->ptrAt(index));
    }
  }

  template <typename T,
            typename Output=std::vector<T> >
  class FirstObjectSelector: public edm::EDProducer {
  public:
    explicit FirstObjectSelector(const edm::ParameterSet& iConfig):
      src_(iConfig.getParameter<edm::InputTag>("src")),
      throw_(iConfig.getUntrackedParameter<bool>("throw", true))
    {
      produces<Output>();
    }
    ~FirstObjectSelector() {}

    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      edm::Handle<edm::View<T> > hcand;
      iEvent.getByLabel(src_, hcand);

      std::auto_ptr<Output> prod(new Output());
      if(!hcand->empty())
        fos::append(*prod, hcand, 0);
      else if(throw_)
        throw cms::Exception("LogicError") << "Input collection " << src_.encode() << " is empty" << std::endl;

      iEvent.put(prod);
    }

  private:
    edm::InputTag src_;
    bool throw_;
  };
}

#endif
