// -*- c++ -*-
#ifndef Tools_PileupWeight_h
#define Tools_PileupWeight_h

#include "DataFormat/interface/Event.h"
#include <string>

#include "TH1F.h"

class PileupWeight {
public:
  PileupWeight();
  ~PileupWeight();

  void set(std::string, std::string, std::string, bool);
  double getWeight(Event&);

private:
  std::string puHistoFileName_data;
  std::string puHistoFileName_mc;
  std::string puHistoPath;

  bool isdata;

  TH1F* h_weight;

  bool fSet;
};
#endif
