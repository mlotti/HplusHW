#include "HiggsAnalysis/MiniAOD2TTree/interface/SkimDumper.h"

SkimDumper::SkimDumper(edm::ParameterSet& pset){
    inputCollection = pset;
    booked = false;
    tags = inputCollection.getParameter<std::vector<edm::InputTag> >("Counters");
}
SkimDumper::~SkimDumper(){}

void SkimDumper::book(){
    booked = true;

    hCounter = new TH1F("SkimCounter","",tags.size(),0,tags.size());
    for(size_t i = 0; i < tags.size(); ++i){
	hCounter->GetXaxis()->SetBinLabel(i+1,tags[i].label().c_str());
    }
}

#include "DataFormats/Common/interface/MergeableCounter.h"
bool SkimDumper::fill(const edm::LuminosityBlock& iLumi, const edm::EventSetup& iSetup){
    if (!booked) return true;

    for(size_t i = 0; i < tags.size(); ++i){
      std::cout << "check counters " << tags[i].label() << std::endl;
      edm::Handle<edm::MergeableCounter> count;
      iLumi.getByLabel(tags[i], count);

      if(count.isValid()){
        hCounter->Fill(i,count->value);
	std::cout << "check count " << count->value << std::endl;
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
