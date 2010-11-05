#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <iostream>
#include <fstream>
#include <vector>

class PickEventsDumper: public edm::EDAnalyzer {
    public:
  	explicit PickEventsDumper(const edm::ParameterSet&);
  	~PickEventsDumper();

    private:
	struct Info {
		int Run;
		int Lumi;
		int Event;
	};

  	virtual void beginJob();
  	virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  	virtual void endJob();

	std::vector<Info> events;

	std::string fOUTName;
	int counter;
};

PickEventsDumper::PickEventsDumper(const edm::ParameterSet& iConfig): 
fOUTName(iConfig.getUntrackedParameter<std::string>("FileName")),
counter(0)
{
}

PickEventsDumper::~PickEventsDumper() {}

void PickEventsDumper::beginJob() {
}

void PickEventsDumper::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
	Info event;
	event.Run   = iEvent.run();
	event.Lumi  = iEvent.luminosityBlock();
	event.Event = iEvent.id().event();
	events.push_back(event);
	++counter;
}

void PickEventsDumper::endJob() {
	std::cout << "Saving PickEvents list to " << fOUTName << std::endl;
	std::ofstream fOUT(fOUTName.c_str());
	for(size_t i = 0; i < events.size(); ++i){
		fOUT << events[i].Run << ":" 
                     << events[i].Lumi << ":"
                     << events[i].Event << std::endl;
	}
}

//define this as a plug-in
DEFINE_FWK_MODULE(PickEventsDumper);
