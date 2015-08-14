#ifndef FourVectorDumper_h
#define FourVectorDumper_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"

#include <string>
#include <vector>

#include "TTree.h"

/// Class for storing generic 4-vectors (use case: systematic variations for taus and jets)
class FourVectorDumper {
public:
  virtual FourVectorDumper();
  ~FourVectorDumper();

  virtual void book(TTree* tree, const std::string& name, const std::string& postfix);
  virtual bool fill(edm::Event&, const edm::EventSetup&);
  virtual void add(const double _pt, const double _eta, const double _phi, const double _e);
  virtual void reset();

  virtual bool filter();
  
protected:
  bool useFilter;
  bool booked;

private:
  std::vector<double> pt;
  std::vector<double> eta;            
  std::vector<double> phi;
  std::vector<double> e;

};
#endif
