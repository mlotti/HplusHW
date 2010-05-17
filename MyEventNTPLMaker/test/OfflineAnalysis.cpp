// system include files
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include <iostream>
using namespace std;

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventConverter.h"

#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

class OfflineAnalysis : public edm::EDAnalyzer {
  public:
  	explicit OfflineAnalysis(const edm::ParameterSet&);
  	~OfflineAnalysis() {}

  	virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  	virtual void beginJob();
  	virtual void endJob();
  private:
	MyEventConverter* myEventConverter;
};

OfflineAnalysis::OfflineAnalysis(const edm::ParameterSet& iConfig){
	myEventConverter = new MyEventConverter(iConfig);
}

void OfflineAnalysis::beginJob(){
}

void OfflineAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
	myEventConverter->convert(iEvent,iSetup);
}

void OfflineAnalysis::endJob(){
	delete myEventConverter;
}

DEFINE_FWK_MODULE(OfflineAnalysis);
