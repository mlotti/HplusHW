// -*- c++ -*-
#ifndef Framework_EventWeight_h
#define Framework_EventWeight_h

/**
   Class for keeping the event weight (from prescale and from factorizing)
**/
class EventWeight {
public:
  EventWeight();
  ~EventWeight();

  void beginEvent() { fWeight = 1.0; }

  /// Adds a weight by multiplying the current weight
  void multiplyWeight(double w) { fWeight *= w; }
  /// Getter for weight
  double getWeight() const { return fWeight; }

private:
  double fWeight;
};

#endif
