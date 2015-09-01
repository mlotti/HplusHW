#include "HiggsAnalysis/MiniAOD2TTree/interface/SkimDumper.h"

SkimDumper::SkimDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset){
    inputCollection = pset;
    booked = false;
    std::vector<edm::InputTag> tags = inputCollection.getParameter<std::vector<edm::InputTag> >("Counters");
    
    token = new edm::EDGetTokenT<edm::MergeableCounter>[tags.size()];
    for(size_t i = 0; i < tags.size(); ++i) {
      // Use edm::InLumi in consumes template to signal that the counters are read from lumiblock instead of event
      token[i] = iConsumesCollector.consumes<edm::MergeableCounter, edm::InLumi>(tags[i]);
    }
}
SkimDumper::~SkimDumper(){}

void SkimDumper::book(){
    booked = true;
    std::vector<edm::InputTag> tags = inputCollection.getParameter<std::vector<edm::InputTag> >("Counters");
    hCounter = new TH1F("SkimCounter","",tags.size(),0,tags.size());
    for(size_t i = 0; i < tags.size(); ++i){
	hCounter->GetXaxis()->SetBinLabel(i+1,tags[i].label().c_str());
    }
}

#include "DataFormats/Common/interface/MergeableCounter.h"
bool SkimDumper::fill(const edm::LuminosityBlock& iLumi, const edm::EventSetup& iSetup){
    if (!booked) return true;

    std::vector<edm::InputTag> tags = inputCollection.getParameter<std::vector<edm::InputTag> >("Counters");
    for(size_t i = 0; i < tags.size(); ++i){
//      std::cout << "check counters " << tags[i].label() << std::endl;
      edm::Handle<edm::MergeableCounter> count;
      iLumi.getByToken(token[i], count);

      if(count.isValid()){
        hCounter->Fill(i,count->value);
//	std::cout << "check count " << count->value << std::endl;
      }
    }
    return true;
}

void SkimDumper::reset(){
    if(booked){
    }
}

TH1F* SkimDumper::getCounter(){
    return hCounter;
}
