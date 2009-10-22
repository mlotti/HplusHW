// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_getParticles_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_getParticles_h

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

#include<vector>

template <class T, class Converter>
std::vector<MyJet> getParticles(const edm::InputTag& name, const edm::Event& iEvent, const Converter& converter) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(name, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << name << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet> ret;
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    ret.push_back(converter.convert(handle, i));
  }

  return ret;
}


#endif
