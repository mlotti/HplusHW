// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_getParticles_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_getParticles_h

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEvent.h"

#include<vector>

template <class T, class Converter>
void getParticles(MyEvent *saveEvent, const std::string& name, const edm::InputTag& label, const edm::Event& iEvent, Converter& converter) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(label, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << label << " with " << handle->size() << " particles" << std::endl;

  std::vector<MyJet>& ret(saveEvent->addCollection(name));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    ret.push_back(converter.convert(handle, i));
  }
}

// Version with additional tagger
template <class T, class Converter, class Tagger>
void getParticles(MyEvent *saveEvent, const std::string& name, const edm::InputTag& label, const edm::Event& iEvent, Converter& converter, const Tagger& tagger) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(label, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << label << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(name));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    MyJet jet = converter.convert(handle, i);
    tagger.tag(handle, i, jet.tagInfo);
    ret.push_back(jet);
  }
}

template <class T, class Converter, class Condition>
void getParticlesIf(MyEvent *saveEvent, const std::string& name, const edm::InputTag& label, const edm::Event& iEvent, Converter& converter, const Condition& condition) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(label, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << label << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(name));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    if(!condition((*handle)[i])) continue;
    ret.push_back(converter.convert(handle, i));
  }
}


#endif
