// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_TriggerConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_TriggerConverter_h

#include "FWCore/Common/interface/TriggerNames.h"

#include<map>
#include<vector>
#include<string>

namespace edm { class Event; }
class MyEvent;

class TriggerConverter {
    public:
  	TriggerConverter(const edm::ParameterSet& iConfig);
  	~TriggerConverter();

//  	static void getTriggerResults(const edm::Event&, std::map<std::string, bool>&, bool print);
	void getTriggerResults(const edm::Event&, std::map<std::string, bool>&, bool print);
  	static void addTriggerObjects(MyEvent *, const edm::Event&);

	bool getTriggerDecision();

    private:
	std::vector<std::string> hlNames;
//	edm::TriggerNames* triggerNames;
	bool triggerDecision;
};

#endif
