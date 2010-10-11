#ifndef TAUHLTMATCHPRODUCER_H
#define TAUHLTMATCHPRODUCER_H

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include <string>
#include <vector>
#include <map>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

class TauHLTMatchProducer : public edm::EDProducer {
 public:
  TauHLTMatchProducer(const edm::ParameterSet& iConfig);
  ~TauHLTMatchProducer();

 private:
  virtual void beginJob() ;
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();
      
  edm::InputTag fTriggerSource;
  edm::InputTag fTriggerEventSource;
  edm::InputTag fTauSource;
  std::string fHLTTriggerName;

};

#endif
