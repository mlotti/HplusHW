// -*- c++ -*-
#ifndef Tools_PileupWeight_h
#define Tools_PileupWeight_h

#include "Framework/interface/ParameterSet.h"
#include "DataFormat/interface/Event.h"

#include <string>

class TH1;

class PileupWeight {
public:
  explicit PileupWeight(const ParameterSet& pset);
  ~PileupWeight();

  // Disable copying, assignment, and moving
  // Mainly because according to the design, there should be no need for them
  PileupWeight(const PileupWeight&) = delete;
  PileupWeight(PileupWeight&&) = delete;
  PileupWeight& operator=(const PileupWeight&) = delete;
  PileupWeight& operator=(PileupWeight&&) = delete;

  double getWeight(const Event& event);

private:
  const bool fEnabled;

  const TH1 *h_weight;
};
#endif
