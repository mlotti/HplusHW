#ifndef TriggerEfficiency_BaseSelection_h
#define TriggerEfficiency_BaseSelection_h

#include "DataFormat/interface/Event.h"

class BaseSelection {
 public:
  BaseSelection(){}
  ~BaseSelection(){}

  virtual bool offlineSelection(Event&) = 0;
  virtual bool onlineSelection(Event&) = 0;

  double xVariable() { return xvariable;}

 protected:

  bool passedCtrlTtrigger(Event&);

  double xvariable;
};

bool BaseSelection::passedCtrlTtrigger(Event& fEvent){
  return true;
}
#endif
