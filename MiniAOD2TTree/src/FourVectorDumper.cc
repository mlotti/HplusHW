#include "HiggsAnalysis/MiniAOD2TTree/interface/FourVectorDumper.h"

FourVectorDumper::FourVectorDumper()
: booked(false) { }

FourVectorDumper::~FourVectorDumper() { }

void FourVectorDumper::book(TTree* tree, const std::string& name, const std::string& postfix) {
  booked = true;
  std::string modPostfix = "";
  if (!postfix.empty()) {
    modPostfix = postfix;
  }
  tree->Branch((name+"_pt"+modPostfix).c_str(),&pt);
  tree->Branch((name+"_eta"+modPostfix).c_str(),&eta);
  tree->Branch((name+"_phi"+modPostfix).c_str(),&phi);
  tree->Branch((name+"_e"+modPostfix).c_str(),&e);
}

bool FourVectorDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if(booked) return filter();
  return true;
}

bool FourVectorDumper::filter(){
  return true;
}

void FourVectorDumper::add(const double _pt, const double _eta, const double _phi, const double _e) {
  pt.push_back(_pt);
  eta.push_back(_eta);
  phi.push_back(_phi);
  e.push_back(_e);
}

void FourVectorDumper::reset(){
  if(booked){
    pt.clear();
    eta.clear();
    phi.clear();
    e.clear();
  }
}
