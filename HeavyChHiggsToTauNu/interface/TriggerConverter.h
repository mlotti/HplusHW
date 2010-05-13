// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerConverter_h

#include<map>
#include<string>

namespace edm { class Event; }
class MyEvent;

class TriggerConverter {
public:
  static void getTriggerResults(const edm::Event&, std::map<std::string, bool>&, bool print);
  static void addTriggerObjects(MyEvent *, const edm::Event&);
};

#endif
