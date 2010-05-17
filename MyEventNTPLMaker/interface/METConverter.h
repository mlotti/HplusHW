// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_METConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_METConverter_h

#include<map>
#include<string>
#include<vector>

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyMET.h"

#include "FWCore/Utilities/interface/InputTag.h"

namespace edm { class Event; }

class METConverter {
public:
  METConverter(const std::vector<edm::InputTag>& caloMetLabels, const edm::InputTag& pfMetLabel, const edm::InputTag& tcMetLabel);
  ~METConverter();

  void convert(const edm::Event&, std::map<std::string, MyMET>&);
private:
  const std::vector<edm::InputTag>& caloMets;
  const edm::InputTag& pfMet;
  const edm::InputTag& tcMet;
};

#endif
