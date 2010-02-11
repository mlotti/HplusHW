// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_getParticles_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_getParticles_h

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEvent.h"

#include<vector>

template <class T, class Converter>
void getParticles(MyEvent *saveEvent, const edm::InputTag& label, const edm::Event& iEvent, Converter& converter) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(label, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << label << " with " << handle->size() << " particles" << std::endl;

  std::vector<MyJet>& ret(saveEvent->addCollection(label.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    ret.push_back(converter.convert(label, handle, i));
  }
}

// Version with additional modifier
template <class T, class Converter, class Modify>
void getParticles(MyEvent *saveEvent, const edm::InputTag& label, const edm::Event& iEvent, Converter& converter, const Modify& modify) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(label, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << label << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(label.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    MyJet jet = converter.convert(label, handle, i);
    modify(handle, i, &jet);
    ret.push_back(jet);
  }
}

// Version with conditition (if conditiion is true, add to collection)
template <class T, class Converter, class Condition>
void getParticlesIf(MyEvent *saveEvent, const edm::InputTag& label, const edm::Event& iEvent, Converter& converter, const Condition& condition) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(label, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << label << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(label.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    if(!condition((*handle)[i])) continue;
    ret.push_back(converter.convert(label, handle, i));
  }
}

// Version with condition and additional modifier
template <class T, class Converter, class Condition, class Modify>
void getParticlesIf(MyEvent *saveEvent, const edm::InputTag& label, const edm::Event& iEvent, Converter& converter, const Condition& condition, const Modify& modify) {
  edm::Handle<edm::View<T> > handle;
  iEvent.getByLabel(label, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << label << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(label.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    if(!condition((*handle)[i])) continue;
    MyJet jet = converter.convert(label, handle, i);
    modify(handle, i, &jet);
    ret.push_back(jet);
  }
}


#endif
