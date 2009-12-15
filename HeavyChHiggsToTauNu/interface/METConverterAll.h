// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METConverter_h

#include<map>
#include<string>
#include<vector>

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"

namespace edm { class Event; }

class METConverterAll {
public:
  METConverterAll();
  ~METConverterAll();

  void convert(const edm::Event&, std::map<std::string, MyMET>&);
private:
};

#endif
