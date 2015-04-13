#ifndef TriggerEfficiency_BaseSelection_h
#define TriggerEfficiency_BaseSelection_h

#include "DataFormat/interface/Event.h"

#include <string>
#include <vector>

class BaseSelection {
 public:
  BaseSelection(){}
  ~BaseSelection(){}

  virtual bool offlineSelection(Event&) = 0;
  virtual bool onlineSelection(Event&) = 0;
  bool passedRunRange(Event&, bool);
  double xVariable() { return xvariable;}
  bool passedCtrlTtrigger(Event&);

 protected:

  void init(const ParameterSet&);

  double xvariable;

  std::string fdataera;
  //  float flumi;
  int frunMin;
  int frunMax;
  //  std::string fsample;
  //  std::vector<std::string> fcontrolTriggers;
  //  std::vector<std::string> fsignalTriggers;

  //  std::vector<std::string> tauDiscrs;
};

void BaseSelection::init(const ParameterSet& config){
  //  fdataera          = config.getParameter<std::string>("dataera");
  //  flumi             = config.getParameter<float>("lumi");
  if(config.getParameterOptional<int>("runMin")){
    frunMin           = *(config.getParameterOptional<int>("runMin"));
    frunMax           = *(config.getParameterOptional<int>("runMax"));
  }
  //  fsample           = config.getParameter<std::string>("sample");
  //  tauDiscrs         = config.getParameter<std::vector<std::string>>("tauDiscriminators");
  //  fcontrolTriggers  = config.getParameter<std::vector<std::string>>("controlTriggers");
  //  fsignalTriggers   = config.getParameter<std::vector<std::string>>("signalTriggers");
}

bool BaseSelection::passedCtrlTtrigger(Event& fEvent){
  return fEvent.configurableTriggerDecision();
}

//bool BaseSelection::onlineSelection(Event& fEvent){
//  return fEvent.configurableTriggerDecision2();
//}

bool BaseSelection::passedRunRange(Event& fEvent, bool isData){

  if(!isData) return true;

  bool passed = false;
  int run = fEvent.eventID().run();
  if(run >= frunMin && run <= frunMax){
    passed = true;
  }
  return passed;
}
#endif
