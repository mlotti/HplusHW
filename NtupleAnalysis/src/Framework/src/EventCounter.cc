#include "Framework/interface/EventCounter.h"
#include "Framework/interface/EventWeight.h"
#include <boost/concept_check.hpp>

#include <TDirectory.h>
#include <TH1F.h>

#include <stdexcept>
#include <algorithm>
#include <iostream>

// Count
Count::Count(EventCounter *ec, size_t counterIndex, size_t countIndex):
  fEventCounter(ec), fCounterIndex(counterIndex), fCountIndex(countIndex) {}
Count::~Count() {}

// Counter
EventCounter::Counter::Counter(const std::string& n):
  name(n),
  counter(nullptr),
  weightedCounter(nullptr)
{}
bool EventCounter::Counter::contains(const std::string& l) const {
  return std::find(labels.begin(), labels.end(), l) != labels.end();
}
size_t EventCounter::Counter::getLabelIndex(const std::string& l) const {
  for (size_t i = 0; i < labels.size(); ++i) {
    if (l == labels[i])
      return i;
  }
  return -1;
}
size_t EventCounter::Counter::insert(const std::string& label, int initialValue) {
  if(counter)
    throw std::logic_error("May not call addCounter() after setOutput()");

  size_t index = labels.size();
  labels.push_back(label);
  values.push_back(initialValue);
  weights.push_back(0);
  weightsSquared.push_back(0);
  return index;
}
void EventCounter::Counter::incrementCount(size_t countIndex, double weight) {
  short sign = 1;
  if(weight < 0) sign = -1;
  values[countIndex] += sign;
  weights[countIndex] += weight;
  weightsSquared[countIndex] += (weight*weight);
}
long int EventCounter::Counter::value(size_t countIndex) {
  return values[countIndex];
}
void EventCounter::Counter::book(TDirectory *dir) {
  if(labels.empty())
    return;

  counter = new TH1F(name.c_str(), name.c_str(), labels.size(), 0, labels.size());
  counter->SetDirectory(dir);
  for(size_t i=0; i<labels.size(); ++i)
    counter->GetXaxis()->SetBinLabel(i+1, labels[i].c_str());
}
void EventCounter::Counter::bookWeighted(TDirectory *dir) {
  if(labels.empty())
    return;

  weightedCounter = new TH1F(name.c_str(), ("Weighted "+name).c_str(), labels.size(), 0, labels.size());
  weightedCounter->SetDirectory(dir);
  for(size_t i=0; i<labels.size(); ++i)
    weightedCounter->GetXaxis()->SetBinLabel(i+1, labels[i].c_str());
}
void EventCounter::Counter::serialize() {
  if (counter == nullptr) return;
  for(size_t i=0; i<labels.size(); ++i) {
    size_t bin = i+1;
    counter->SetBinContent(bin, values[i]);
    weightedCounter->SetBinContent(bin, weights[i]);
    weightedCounter->SetBinError(bin, std::sqrt(weightsSquared[i]));
  }
}

// EventCounter
EventCounter::EventCounter(const EventWeight& weight):
  fWeight(weight),
  fIsEnabled(true),
  fOutputHasBeenSet(false)
{
  fCounters.emplace_back("counter");
}

EventCounter::~EventCounter() {}

Count EventCounter::addCounter(const std::string& name, double initialValue) {
  if(fOutputHasBeenSet)
    throw std::logic_error("May not call addCounter() after setOutput()");
  // std::cout << "=== EventCounter::addCounter\n\tAdding counter \"" << name << "\" with initial value " << initialValue << std::endl;
  size_t index = fCounters[0].insert(name, initialValue);
  return Count(this, 0, index);
}
Count EventCounter::addSubCounter(const std::string& subcounterName, const std::string& countName, double initialValue) {
  if(fOutputHasBeenSet)
    throw std::logic_error("May not call addSubCounter() after setOutput()");

  size_t counterIndex = findOrInsertCounter(subcounterName);
  size_t countIndex = fCounters[counterIndex].insert(countName, initialValue);
  return Count(this, counterIndex, countIndex);
}

void EventCounter::incrementCount(size_t counterIndex, size_t countIndex) {
  fCounters[counterIndex].incrementCount(countIndex, fWeight.getWeight());
}
int EventCounter::value(size_t counterIndex, size_t countIndex) {
  return fCounters[counterIndex].value(countIndex);
}

void EventCounter::setOutput(TDirectory *dir) {
  fOutputHasBeenSet = true;
  TDirectory *subdir = dir->mkdir("counters");
  for(auto& counter: fCounters)
    counter.book(subdir);

  subdir = subdir->mkdir("weighted");
  for(auto& counter: fCounters)
    counter.bookWeighted(subdir);
}

void EventCounter::serialize() {
  for(auto& counter: fCounters)
    counter.serialize();
}
long int EventCounter::getValueByName(const std::string& name) {
  for (auto it = fCounters.begin(); it != fCounters.end(); ++it) {
    if (it->contains(name)) {
      size_t i = it->getLabelIndex(name);
      return it->value(i);
    }
  }
  return -1;
}
bool EventCounter::contains(const std::string& name) {
  for (auto it = fCounters.begin(); it != fCounters.end(); ++it) {
    if (it->contains(name))
      return true;
  }
  return false;
}
size_t EventCounter::findOrInsertCounter(const std::string& name) {
  auto found = std::find_if(fCounters.begin(), fCounters.end(), [&](const Counter& c) {
      return c.getName() == name;
    });
  if(found != fCounters.end())
    return found - fCounters.begin();
  size_t index = fCounters.size();
  fCounters.emplace_back(name);
  return index;
}
