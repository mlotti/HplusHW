// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_getParticles_h
#define HiggsAnalysis_MyEventNTPLMaker_getParticles_h

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/MyEventNTPLMaker/interface/CollectionTraits.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEvent.h"

#include<vector>

// Select the label for structs containing InputTag, and the object itself in case of InputTag
template <typename T>
const edm::InputTag& getTag(const T& obj) {
        return obj.label;
}
template <>
const edm::InputTag& getTag<edm::InputTag>(const edm::InputTag& obj) {
        return obj;
}


template <class T, class Label, class Converter>
void getParticles(MyEvent *saveEvent, const Label& label, const edm::Event& iEvent, Converter& converter) {
  const edm::InputTag& tag = getTag(label);
  edm::Handle<typename CollectionTraits<T>::collection_type > handle;
  iEvent.getByLabel(tag, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << tag << " with " << handle->size() << " particles" << std::endl;

  std::vector<MyJet>& ret(saveEvent->addCollection(tag.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    ret.push_back(converter.convert(label, handle, i));
  }
}

// Version with additional modifier
template <class T, class Label, class Converter, class Modify>
void getParticles(MyEvent *saveEvent, const Label& label, const edm::Event& iEvent, Converter& converter, const Modify& modify, bool missingSilent=false) {
  const edm::InputTag& tag = getTag(label);
  edm::Handle<typename CollectionTraits<T>::collection_type > handle;
  iEvent.getByLabel(tag, handle);
  if(missingSilent && !handle.isValid())
    return;

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << tag << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(tag.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    MyJet jet = converter.convert(label, handle, i);
    modify(handle, i, &jet);
    ret.push_back(jet);
  }
}

// Version with conditition (if conditiion is true, add to collection)
template <class T, class Label, class Converter, class Condition>
void getParticlesIf(MyEvent *saveEvent, const Label& label, const edm::Event& iEvent, Converter& converter, const Condition& condition) {
  const edm::InputTag& tag = getTag(label);
  edm::Handle<typename CollectionTraits<T>::collection_type > handle;
  iEvent.getByLabel(tag, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << tag << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(tag.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    if(!condition((*handle)[i])) continue;
    ret.push_back(converter.convert(label, handle, i));
  }
}

// Version with condition and additional modifier
template <class T, class Label, class Converter, class Condition, class Modify>
void getParticlesIf(MyEvent *saveEvent, const Label& label, const edm::Event& iEvent, Converter& converter, const Condition& condition, const Modify& modify) {
  const edm::InputTag& tag = getTag(label);
  edm::Handle<typename CollectionTraits<T>::collection_type > handle;
  iEvent.getByLabel(tag, handle);

  if(edm::isDebugEnabled())
    LogDebug("MyEventConverter") << "Particle collection " << tag << " with " << handle->size() << " particles" << std::endl;


  std::vector<MyJet>& ret(saveEvent->addCollection(tag.label()));
  ret.reserve(handle->size());
  for(size_t i = 0; i<handle->size(); ++i) {
    if(!condition((*handle)[i])) continue;
    MyJet jet = converter.convert(label, handle, i);
    modify(handle, i, &jet);
    ret.push_back(jet);
  }
}


#endif
